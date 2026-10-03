"""Blind challenge: public and hidden tiers, key commitments, scoring, leaderboard data.

Design rules (Judge fix #6, adapted to a static site with no backend):

* Challenge corpora are NOT generated from the public plaintext. Each source is first
  "disguised" with a secret seed: regular sound changes plus lexical replacement turn it into
  an unattested sister language. Otherwise anyone could match the hidden corpora against the
  public DCS / Project Madurai / CDLI / Gutenberg texts and "decipher" them trivially.
* Public tier: corpora AND keys are released, for development.
* Hidden tier: corpora are released, keys stay in private/ (git-ignored). Each key's SHA-256 is
  published in advance (commitments.json), so the maintainer cannot change a key after seeing
  submissions.
* One scored submission per team per hidden round, enforced by the scorer against
  leaderboard/data.json. New rounds use fresh secret seeds, so repeated probing of one round
  gains nothing. A static leaderboard cannot rate-limit, so this policy relies on the maintainer
  running the scorer offline.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import secrets
import time
import zlib
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np

from . import config
from .corpus import AnswerKey, Corpus
from .generator import build as gbuild
from .generator.calibrate import load_knobs
from .knowledge import _change_unit, sound_change_map
from .ml import balanced_accuracy
from .paths import ensure, private_dir, project_root
from .scoring import score_sign_values

TIERS = ("public", "hidden")


def _secret(round_id: str, tier: str) -> int:
    """Per-round secret. Public tier: derived from the round name (reproducible by anyone).
    Hidden tier: random, stored only in private/."""
    if tier == "public":
        return zlib.crc32(f"ibdb-public-{round_id}".encode())
    p = ensure(private_dir() / "challenge") / f"secret-{round_id}.txt"
    if not p.exists():
        p.write_text(str(secrets.randbits(31)))
    return int(p.read_text())


def disguise(source: str, secret: int, rate: float = 0.35, lex: float = 0.25) -> str:
    """Register a disguised copy of a language's segments; return its cache name."""
    name = f"{source}~{secret}"
    if name in gbuild._DISGUISED:
        return name
    d = deepcopy(gbuild._segments(source))
    pmap = sound_change_map(source, rate, secret)
    rng = np.random.default_rng([secret, zlib.crc32(source.encode())])
    words = d["words"]
    by_len: dict[int, list[int]] = {}
    for i, w in enumerate(words):
        by_len.setdefault(len(w[2]), []).append(i)
    new_words = []
    for i, (form, phon, syl, sem) in enumerate(words):
        src = i
        if rng.random() < lex:  # unrelated replacement word, then the same sound changes
            pool = by_len[len(syl)]
            src = pool[int(rng.integers(len(pool)))]
        f2, p2, s2, _ = words[src]
        new_form = _change_unit(f2, source, pmap) + ("" if src == i else f"·{i % 97}")
        new_words.append([new_form, [_change_unit(p, source, pmap) for p in p2],
                          [_change_unit(s, source, pmap) for s in s2], sem])
    d["words"] = new_words
    gbuild._DISGUISED[name] = d
    return name


def build_round(round_id: str, tier: str, n_corpora: int = 24, out_root: Path | None = None) -> Path:
    prof = config.experiment()["profiles"]["full"]
    secret = _secret(round_id, tier)
    rng = np.random.default_rng(secret)
    root = ensure((out_root or project_root() / "challenge") / tier / round_id)
    ensure(root / "corpora")
    key_dir = ensure(root / "keys") if tier == "public" else ensure(private_dir() / "challenge" / round_id)
    manifest, commitments = [], {}
    pool = [(l, st) for l in prof["languages"] for st in prof["script_types"]] + \
           [(c, "emblem") for c in prof["controls"]]
    for i in range(n_corpora):
        src, st = pool[int(rng.integers(len(pool)))]
        ip = prof["indus_point"]
        n = int(rng.choice([1548, ip["n_texts"], ip["n_texts"], 20000]))
        knobs, spec = load_knobs("full", src, st)
        gen_src = disguise(src, secret) if src in gbuild.LANGUAGES else src
        cid = f"{tier[0]}{round_id}-{i:03d}-" + hashlib.sha1(f"{secret}-{i}".encode()).hexdigest()[:6]
        corpus, key, _ = gbuild.make_corpus(gen_src, spec, n, ip["mean_length"], int(rng.integers(1 << 30)), knobs,
                                           corpus_id=cid)
        key.source = src
        key.family = gbuild.source_family(src)
        key.kind = gbuild.source_kind(src)
        key.is_linguistic = key.kind == "language"
        key.params = {"round": round_id, "tier": tier, "n_texts": n}  # generator details stay private
        corpus.meta.update({"tier": tier})
        corpus.save(root / "corpora" / f"{cid}.json.gz")
        commitments[cid] = key.save(key_dir / f"{cid}.key.json.gz")
        manifest.append({"corpus_id": cid, "n_texts": n, "direction": corpus.direction})
    (root / "manifest.json").write_text(json.dumps({
        "round": round_id, "tier": tier, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tasks": {"A": "is_linguistic (bool)", "B": "script_type in logographic|syllabic|logosyllabic|alphabetic",
                  "C": "family in indo-european|dravidian|isolate|uralic", "D": "sign_values: {sign_id: value}"},
        "corpora": manifest}, indent=1))
    (root / "commitments.json").write_text(json.dumps({"algorithm": "sha256 of the uncompressed key JSON",
                                                       "keys": commitments}, indent=1))
    return root


def _key_dir(round_id: str, tier: str, keys_dir: Path | None) -> Path:
    if keys_dir:
        return keys_dir
    return (project_root() / "challenge" / tier / round_id / "keys") if tier == "public" else private_dir() / "challenge" / round_id


def score_submission(sub: dict, round_id: str, tier: str, keys_dir: Path | None = None) -> dict[str, Any]:
    root = project_root() / "challenge" / tier / round_id
    kdir = _key_dir(round_id, tier, keys_dir)
    commits = json.loads((root / "commitments.json").read_text())["keys"]
    ya, pa, b_ok, c_ok, d_acc = [], [], [], [], []
    for cid, digest in commits.items():
        kp = kdir / f"{cid}.key.json.gz"
        blob = gzip.decompress(kp.read_bytes())
        if hashlib.sha256(blob).hexdigest() != digest:
            raise RuntimeError(f"key {cid} does not match its published commitment")
        key = AnswerKey.load(kp)
        pred = sub.get("predictions", {}).get(cid, {})
        if key.kind != "nl_derived" and "is_linguistic" in pred:
            ya.append(key.is_linguistic)
            pa.append(bool(pred["is_linguistic"]))
        if key.is_linguistic:
            b_ok.append(pred.get("script_type") == key.script_type)
            c_ok.append(pred.get("family") == key.family)
            corpus = Corpus.load(root / "corpora" / f"{cid}.json.gz")
            sv = {int(k): v for k, v in (pred.get("sign_values") or {}).items()}
            d_acc.append(score_sign_values(sv, key, [t.tolist() for t in corpus.logical()])["token_acc"])
    return {"A_balanced_acc": balanced_accuracy(np.array(ya), np.array(pa)) if ya else None,
            "B_acc": float(np.mean(b_ok)) if b_ok else None, "C_acc": float(np.mean(c_ok)) if c_ok else None,
            "D_token_acc": float(np.mean(d_acc)) if d_acc else None,
            "n_corpora": len(commits), "n_linguistic": len(b_ok)}


def leaderboard_path() -> Path:
    return ensure(project_root() / "leaderboard") / "data.json"


def record_score(sub: dict, scores: dict, round_id: str, tier: str, force: bool = False) -> None:
    p = leaderboard_path()
    data = json.loads(p.read_text()) if p.exists() else {"entries": []}
    team = sub.get("team", "anonymous")
    if tier == "hidden" and not force and any(e["team"] == team and e["round"] == round_id and e["tier"] == "hidden"
                                              for e in data["entries"]):
        raise RuntimeError(f"team {team!r} already has a scored submission for hidden round {round_id}")
    data["entries"].append({"team": team, "method": sub.get("method", ""), "url": sub.get("url", ""),
                            "round": round_id, "tier": tier, "claims_indus_decipherment": bool(sub.get("claims_indus_decipherment", False)),
                            "scored_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **scores})
    p.write_text(json.dumps(data, indent=1))


def score_main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="ibdb-score", description="Score a challenge submission against answer keys.")
    ap.add_argument("submission", type=Path)
    ap.add_argument("--round", required=True)
    ap.add_argument("--tier", choices=TIERS, default="hidden")
    ap.add_argument("--keys-dir", type=Path, default=None, help="where the answer keys are (maintainer only for hidden)")
    ap.add_argument("--record", action="store_true", help="append the score to leaderboard/data.json")
    ap.add_argument("--force", action="store_true", help="allow a second hidden-tier submission (maintainer override)")
    a = ap.parse_args(argv)
    sub = json.loads(a.submission.read_text())
    scores = score_submission(sub, a.round, a.tier, a.keys_dir)
    print(json.dumps(scores, indent=1))
    if a.record:
        record_score(sub, scores, a.round, a.tier, a.force)
