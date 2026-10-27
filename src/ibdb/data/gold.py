"""Markers shared by the v2 gold tables (pre-registration entry 10).

A gold row's regular reflex is a relative unit, `None` when the cited source states that the sound
has no reflex (lost), or `NO_SOURCE` when the source says nothing about it (unknown). The v2 scorer
treats a token containing a no-source phoneme as unrecoverable; the yardsticks break the text there.
"""

NO_SOURCE = "<no source>"


def old_semantics(regular: dict) -> dict:
    """The same map as the harness read it before entry 10: no-source rows as `None` (lost)."""
    return {k: (None if v == NO_SOURCE else v) for k, v in regular.items()}
