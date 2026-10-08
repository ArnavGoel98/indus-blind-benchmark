"""Positive control: frozen EM (benchmark settings) on English letter-substitution ciphers.

Setting follows Knight et al. (2006, Sec. 3) as closely as our frozen interface allows: an English
letter-bigram plaintext model with word boundaries known (their P(space|SPACE) = 1), a 1:1 substitution
of the 26 letters, out-of-domain ciphertext, plaintext-model data of 70,000 or 1.5 million characters.
Their baseline (bigram EM/Viterbi, 417-letter encyclopedia article) made 68 errors (83.7% correct).
Plaintext: Project Gutenberg (public domain in the USA). Reference model: Pride and Prejudice (#1342)
and Moby Dick (#2701). Ciphertext: passages from On the Origin of Species (#1228).
Methods are imported unchanged from frozen-v1. Analysis only.
Usage: python scripts/positive_control_em.py > reports/positive_controls/em_substitution.md
"""
import re
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np

from ibdb.corpus import AnswerKey, Corpus
from ibdb.methods.base import Knowledge, Reference
from ibdb.methods.decipher import KnightEM, KnightEMOriginal
from ibdb.scoring import score_sign_values

RAW = Path("data/raw/english")
BOOKS = {"pride": 1342, "moby": 2701, "origin": 1228}
LENGTHS = [100, 200, 417, 1000, 2000, 5000]
TRIALS = 10


def fetch(name, gid):
    RAW.mkdir(parents=True, exist_ok=True)
    p = RAW / f"pg{gid}.txt"
    if not p.exists():
        url = f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt"
        p.write_bytes(urllib.request.urlopen(url, timeout=120).read())
    t = p.read_text(encoding="utf-8", errors="ignore")
    a = t.find("*** START"); b = t.find("*** END")
    t = t[t.find("\n", a) + 1: b] if a >= 0 and b > a else t
    return re.findall(r"[a-z]+", t.lower())


def take_chars(words, n):
    out, c = [], 0
    for w in words:
        if c >= n:
            break
        out.append(w); c += len(w) + 1
    return out


def main():
    ref_words = fetch("pride", 1342) + fetch("moby", 2701)
    origin = fetch("origin", 1228)
    refs = {"70k chars": take_chars(ref_words, 70_000), "1.5M chars": take_chars(ref_words, 1_500_000)}
    letters = [chr(c) for c in range(97, 123)]
    print("# Positive control: frozen EM on English letter-substitution ciphers\n")
    print("Knight et al. (2006, Sec. 3) setting: English letter bigrams with known word boundaries, 1:1 "
          "substitution of 26 letters, out-of-domain ciphertext. Their bigram EM/Viterbi baseline on a "
          "417-letter article: 68 errors = 83.7% correct (2.4% error with trigrams, cubing and smoothing). "
          "Ours: frozen `frozen-v1` EM, benchmark settings (3 restarts, 60 iterations). Plaintext model from "
          "Pride and Prejudice + Moby Dick; ciphertext from On the Origin of Species (Project Gutenberg). "
          f"{TRIALS} random passages and random keys per length. Letter accuracy = share of cipher letters "
          "decoded correctly.\n")
    print("| Plaintext-model data | Cipher length (letters) | Original rule: mean [min, max] | Revised rule: mean [min, max] |")
    print("|---|---|---|---|")
    rng = np.random.default_rng(2006)
    for rlabel, rw in refs.items():
        ref = Reference("english", "indo-european", [list(w) for w in rw], dict(Counter(tuple(w) for w in rw)))
        kn = Knowledge("related", "alphabetic", [ref])
        for L in LENGTHS:
            res = {"o": [], "r": []}
            for _ in range(TRIALS):
                start = int(rng.integers(0, len(origin) - 5000))
                ws, c = [], 0
                for w in origin[start:]:
                    if c >= L:
                        break
                    ws.append(w); c += len(w)
                perm = rng.permutation(26) + 100
                enc = {l: int(perm[i]) for i, l in enumerate(letters)}
                texts = [np.array([enc[ch] for ch in w]) for w in ws]
                corpus = Corpus("cipher", texts, "ltr")
                plain = [list(w) for w in ws]
                key = AnswerKey("cipher", "english", "indo-european", "language", True, "alphabetic",
                                {enc[l]: [l] for l in letters}, plain, [[0]] * len(plain))
                logical = [t.tolist() for t in corpus.logical()]
                for tag, M in (("o", KnightEMOriginal), ("r", KnightEM)):
                    p = M(restarts=3, iterations=60).analyze(corpus, kn)
                    res[tag].append(score_sign_values(p.sign_values, key, logical)["token_acc"])
            f = lambda xs: f"{100*np.mean(xs):.1f}% [{100*min(xs):.0f}, {100*max(xs):.0f}]"  # noqa: E731
            print(f"| {rlabel} | {L:,} | {f(res['o'])} | {f(res['r'])} |", flush=True)
    print("\nReference point (Knight et al. 2006): bigram EM/Viterbi, 417 letters, 83.7% correct; best "
          "configuration 97.6%. Their decoding uses Viterbi over the whole text; ours maps each cipher "
          "letter to one plaintext letter (sign-level assignment), so the two are close but not identical "
          "measures.")


if __name__ == "__main__":
    main()
