from collections import Counter

import numpy as np

from ibdb.corpus import Corpus
from ibdb.evaluate import all_methods
from ibdb.generator.build import Knobs, make_corpus
from ibdb.generator.script import ScriptSpec
from ibdb.methods.base import Knowledge, Reference
from ibdb.methods.decipher import KnightEM
from ibdb.scoring import score_sign_values


def test_every_method_runs_and_documents_itself(toy_source):
    c, k, _ = make_corpus(toy_source, ScriptSpec(script_type="syllabic"), 500, 4.4, 0, Knobs())
    units = [[u for w in t.split() for u in [w]] for t in k.plaintext]
    ref = Reference("toy", "indo-european", [list(v) for v in k.token_values], Counter(tuple([u]) for t in units for u in t))
    kn = Knowledge("related", "syllabic", [ref])
    for m in all_methods():
        d = m.describe()
        assert d["paper"] and d["deviations"], f"{m.name} must cite its paper and state deviations"
        p = m.analyze(c, kn if m.needs_knowledge else None)
        if "A" in m.tasks:
            assert p.ling_score is not None or p.extra.get("vector") is not None
        if "D" in m.tasks:
            assert isinstance(p.sign_values, dict)


def test_em_solves_a_plain_substitution_cipher():
    """Sanity: with the exact plaintext LM and a 1:1 cipher, EM must recover most tokens."""
    rng = np.random.default_rng(0)
    V = 12
    T = rng.dirichlet(np.ones(V) * 0.3, size=V)
    texts = []
    for _ in range(3000):
        x = int(rng.integers(V))
        seq = [x]
        for _ in range(int(rng.integers(3, 8))):
            x = int(rng.choice(V, p=T[x]))
            seq.append(x)
        texts.append(seq)
    perm = rng.permutation(V) + 500
    from ibdb.corpus import AnswerKey
    plain = [[f"u{x}" for x in t] for t in texts]
    corpus = Corpus("c", [np.array([perm[x] for x in t]) for t in texts], "ltr")
    key = AnswerKey("c", "s", "f", "language", True, "syllabic", {int(perm[x]): [f"u{x}"] for x in range(V)}, plain, [[0]] * len(plain))
    ref = Reference("r", "f", plain[:1500], {})
    p = KnightEM(restarts=3, iterations=80).analyze(corpus, Knowledge("related", "syllabic", [ref]))
    acc = score_sign_values(p.sign_values, key, [t.tolist() for t in corpus.logical()])["token_acc"]
    assert acc > 0.8
