"""Headline 1 re-run with Rao et al.'s (2009) estimator (post hoc; methods frozen).

Regenerates the Indus-point corpora of the `full` (seeds 0-2) and `replication` (seeds 3-5) runs under
both calibration regimes (`full`, `holdout`) exactly as the runs built them, checks each regenerated
corpus against the stored record's statistics, and computes Rao's relative conditional entropy
(modified Kneser-Ney, C / ln N; ibdb.rao_kn) over all signs and over the 417 most frequent signs.
Sproat's attested non-linguistic systems are scored the same way (native size and 2,906-text samples).
The frozen plug-in conditional-to-unigram entropy ratio is reported alongside from the stored records.

Usage: python scripts/rao_kn_indus_point.py  -> reports/rao_kn/{records.jsonl,indus_point.md}
"""

from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context

import numpy as np

from ibdb import config
from ibdb.paths import ensure, reports_dir

OUT = ensure(reports_dir() / "rao_kn")
POINTS = [("full", "size", "full"), ("full", "regime", "holdout"),
          ("replication", "size", "full"), ("replication", "regime", "holdout")]


def _one(args):
    os.environ.setdefault("IBDB_SISTER_VERSION", "v1")
    prof, rec = args
    from ibdb.generator.build import make_corpus
    from ibdb.generator.calibrate import load_knobs
    from ibdb.rao_kn import conditional_entropy_kn
    from ibdb.stats import corpus_stats
    j = rec["job"]
    knobs, spec = load_knobs(j["regime"], j["source"], j["script_type"], rec.get("generator_version", "v1"))
    median = float(config.regime_targets(j["regime"])["median_length"]["value"]) if j["sweep"] == "regime" else None
    corpus, key, info = make_corpus(j["source"], spec, j["n_texts"], j["mean_length"], j["seed"], knobs,
                                    median_length=median, generator_version=rec.get("generator_version", "v1"))
    logical = [t.tolist() for t in corpus.logical()]
    st = corpus_stats(logical, config.targets()["targets"], seed=j["seed"])
    same = all(st[k] == rec["stats"][k] for k in ("n_tokens", "sign_inventory", "duplicate_text_fraction"))
    a = conditional_entropy_kn(logical)
    b = conditional_entropy_kn(logical, 417)
    return {"profile": prof, "regime": j["regime"], "source": j["source"], "script_type": j["script_type"],
            "seed": j["seed"], "kind": rec["truth"]["kind"], "regenerated_matches_record": same,
            "rel_all": a["relative"], "C_all": a["C"], "N_all": a["N"], "rel_417": b["relative"],
            "plugin_ratio_full_set": None, "plugin_ratio_top100": rec["A"]["rao2009_entropy"]["score"]}


def sproat_rows():
    from ibdb.data import sproat
    from ibdb.rao_kn import conditional_entropy_kn
    rows = []
    for s in sproat.SYSTEMS:
        texts = sproat.load_texts(s)
        sets = [("native", texts)] + [(f"2906 s{k}", t) for k, t in
                                      enumerate(sproat.indus_size_samples(texts, 2906, [0, 1, 2]))]
        for tag, t in sets:
            a = conditional_entropy_kn(t)
            b = conditional_entropy_kn(t, 417)
            rows.append({"profile": "sproat", "regime": tag, "source": s, "kind": "attested_nonling",
                         "disputed": s in sproat.DISPUTED, "rel_all": a["relative"], "N_all": a["N"],
                         "rel_417": b["relative"], "tokens": a["tokens"]})
    return rows


def main() -> None:
    from ibdb.evaluate import load_records
    jobs = []
    for prof, sweep, reg in POINTS:
        ip = config.experiment()["profiles"][prof]["indus_point"]
        for r in load_records(prof):
            j = r.get("job", {})
            if "error" in r or j["sweep"] != sweep or j["regime"] != reg or j["n_texts"] != ip["n_texts"] \
                    or abs(j["mean_length"] - ip["mean_length"]) > 1e-9:
                continue
            jobs.append((prof, r))
    print(f"[rao_kn] {len(jobs)} corpora", flush=True)
    with ProcessPoolExecutor(int(os.environ.get("WORKERS", "4")), mp_context=get_context("spawn")) as ex:
        rows = list(ex.map(_one, jobs, chunksize=4))
    rows += sproat_rows()
    with open(OUT / "records.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"[rao_kn] regenerated-matches-record: {sum(r.get('regenerated_matches_record', True) for r in rows)}/{len(rows)}")


if __name__ == "__main__":
    main()
