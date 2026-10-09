"""Shared helpers for the v2 allograph-merging scripts: rebuild a sensitivity-sweep corpus exactly as
the sweep built it (same pool, same assembly), plus the hidden allograph map."""
from __future__ import annotations

from ibdb.generator.build import make_corpus
from ibdb.generator.calibrate import load_knobs
from ibdb.sensitivity import POOL_FACTORS, PoolExhausted, SensJob, allograph_knobs, assemble


def sweep_corpus(job: SensJob, u: float):
    knobs, spec = load_knobs("full", job.source, job.script_type)
    k = allograph_knobs(knobs, u)
    cid = f"sens-{job.source}-{job.script_type}-s{job.seed}-d{job.dup:.2f}-i{job.inventory}"
    for factor in POOL_FACTORS:
        pool, pkey, pinfo = make_corpus(job.source, spec, factor * job.n_texts, job.mean_length, job.seed, k,
                                        corpus_id="pool")
        try:
            c, key, info = assemble(pool, pkey, job.n_texts, job.mean_length, job.dup, job.seed, cid)
            return c, key, pinfo["_allographs"], spec
        except PoolExhausted:
            continue
    raise PoolExhausted("pool too small")
