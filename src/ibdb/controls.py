"""Non-linguistic control sign systems (Judge fix #3: structurally independent generators).

None of these is derived from a natural-language text. Each ``make_text(rng, L)`` returns a
sequence of exactly L element tokens. The generator then writes each element with a sign
(script type 'emblem'), with the same allograph machinery as the language corpora, so the
controls are calibrated to the same Indus targets.

heraldry       armorial bearings: field, ordinary, charge groups, marks; rule of tincture;
               one token per VISUAL element (never per word of a blazon)
admin_tags     fixed-slot tags: office, commodity, numeral, measure, place, period, owner
emblem_markov  sparse first-order Markov chain with positional start/end preferences
adversarial    Markov chain tuned so its conditional/unigram entropy ratio matches natural
               language (a Sproat-style counterexample to entropy-based tests)
rao_type1      Rao et al. (2009) Type 1: rigid, every sign has one fixed successor
rao_type2      Rao et al. (2009) Type 2: i.i.d. equiprobable signs
"""

from __future__ import annotations

import numpy as np


def _zipf(n: int, s: float) -> np.ndarray:
    w = 1.0 / (np.arange(1, n + 1) ** s)
    return w / w.sum()


class Control:
    name = "control"
    kind = "structural"

    def __init__(self, seed: int, concentration: float = 1.0):
        self.seed = seed
        self.concentration = concentration
        self.rng0 = np.random.default_rng(seed)

    def make_text(self, rng: np.random.Generator, L: int) -> list[str]:
        raise NotImplementedError


class Heraldry(Control):
    name = "heraldry"
    METALS = ["or", "argent"]
    COLOURS = ["gules", "azure", "vert", "sable", "purpure"]
    FURS = ["ermine", "vair"]
    DIVISIONS = ["per-pale", "per-fess", "per-bend", "per-saltire", "quarterly", "per-chevron", "gyronny"]
    ORDINARIES = ["fess", "pale", "bend", "bend-sinister", "chevron", "cross", "saltire", "chief",
                  "pile", "pall", "bordure", "orle", "canton", "pairle"]
    ATTITUDES = ["rampant", "passant", "statant", "sejant", "displayed", "couchant", "salient", ""]

    def __init__(self, seed: int, concentration: float = 1.0):
        super().__init__(seed, concentration)
        self.charges = [f"charge{i}" for i in range(90)]
        self.animate = set(self.rng0.choice(90, size=30, replace=False).tolist())
        self.p_charge = _zipf(90, 1.0 * concentration)

    def _tinct(self, rng, contrast_with: str | None) -> str:
        # Rule of tincture: metal on colour or colour on metal.
        if contrast_with in self.METALS:
            pool = self.COLOURS
        elif contrast_with in self.COLOURS:
            pool = self.METALS
        else:
            pool = self.METALS + self.COLOURS + self.FURS
        return pool[int(rng.integers(len(pool)))]

    def _elements(self, rng) -> list[str]:
        el: list[str] = []
        field = self._tinct(rng, None)
        if rng.random() < 0.35:
            el.append("D:" + self.DIVISIONS[int(rng.integers(len(self.DIVISIONS)))])
            el.append("T:" + field)
            el.append("T:" + self._tinct(rng, field))
        else:
            el.append("T:" + field)
        if rng.random() < 0.55:
            el.append("O:" + self.ORDINARIES[int(rng.integers(len(self.ORDINARIES)))])
            el.append("T:" + self._tinct(rng, field))
        for _ in range(int(rng.integers(1, 3))):
            c = int(rng.choice(90, p=self.p_charge))
            n = int(rng.choice([1, 2, 3, 3, 3, 4, 6]))
            el.append(f"N:{n}")
            el.append("C:" + self.charges[c])
            if c in self.animate:
                att = self.ATTITUDES[int(rng.integers(len(self.ATTITUDES)))]
                if att:
                    el.append("A:" + att)
            el.append("T:" + self._tinct(rng, field))
        if rng.random() < 0.15:
            el.append("M:cadency" + str(int(rng.integers(1, 10))))
        return el

    def make_text(self, rng, L):
        el = self._elements(rng)
        while len(el) < L:  # marshalling: further quarters until long enough
            el += ["Q:quarter"] + self._elements(rng)
        return el[:L]


class AdminTags(Control):
    name = "admin_tags"

    def __init__(self, seed: int, concentration: float = 1.0):
        super().__init__(seed, concentration)
        s = concentration
        self.slots = {
            "office": (40, 1.1 * s), "commodity": (80, 1.0 * s), "measure": (10, 1.2 * s),
            "place": (120, 0.9 * s), "period": (12, 0.5 * s), "owner": (400, 0.8 * s),
        }
        self.p = {k: _zipf(n, e) for k, (n, e) in self.slots.items()}

    def _draw(self, rng, slot):
        n = len(self.p[slot])
        return f"{slot}{int(rng.choice(n, p=self.p[slot]))}"

    def make_text(self, rng, L):
        out = [self._draw(rng, "office")]
        if rng.random() < 0.5:
            out.append(self._draw(rng, "owner"))
        while len(out) < L:
            out.append(self._draw(rng, "commodity"))
            out.append(f"num{int(rng.choice(12, p=_zipf(12, 1.3)) + 1)}")
            out.append(self._draw(rng, "measure"))
            if rng.random() < 0.4:
                out.append(self._draw(rng, "place"))
        if L >= 3 and rng.random() < 0.6:
            out = out[: L - 1] + [self._draw(rng, "period")]
        return out[:L]


class MarkovEmblem(Control):
    name = "emblem_markov"

    def __init__(self, seed: int, concentration: float = 1.0, V: int = 500, branch: tuple = (3, 15)):
        super().__init__(seed, concentration)
        r = self.rng0
        self.V = V
        uni = _zipf(V, 1.0 * concentration)
        self.T = np.zeros((V, V))
        for i in range(V):
            k = int(r.integers(branch[0], branch[1] + 1))
            succ = r.choice(V, size=k, replace=False, p=uni)
            self.T[i, succ] = r.dirichlet(np.ones(k) * 0.5)
        self.start = np.zeros(V)
        s_idx = r.choice(V, size=60, replace=False, p=uni)
        self.start[s_idx] = _zipf(60, 1.0)
        self.enders = r.choice(V, size=25, replace=False)

    def make_text(self, rng, L):
        x = int(rng.choice(self.V, p=self.start))
        out = [x]
        while len(out) < L - 1:
            x = int(rng.choice(self.V, p=self.T[x]))
            out.append(x)
        if L > 1:
            out.append(int(self.enders[int(rng.integers(len(self.enders)))]))
        return [f"e{v}" for v in out[:L]]


class Adversarial(MarkovEmblem):
    """Sparse Markov chain whose entropy profile is tuned toward language (Sproat 2014 argument).

    ``mix`` interpolates between a Zipfian i.i.d. source (ratio H(X2|X1)/H(X1) near 1) and a
    sparse chain (ratio low). ``tune_mix`` bisects ``mix`` to hit a target ratio measured on
    the linguistic corpora.
    """

    name = "adversarial"
    kind = "adversarial"

    def __init__(self, seed: int, concentration: float = 1.0, mix: float = 0.5):
        super().__init__(seed, concentration, V=450, branch=(2, 8))
        self.uni = _zipf(self.V, 1.0 * concentration)
        self.set_mix(mix)

    def set_mix(self, mix: float):
        self.mix = mix
        self.P = (1 - mix) * self.T + mix * self.uni[None, :]
        self.P /= self.P.sum(axis=1, keepdims=True)

    def make_text(self, rng, L):
        x = int(rng.choice(self.V, p=self.start))
        out = [x]
        while len(out) < L:
            x = int(rng.choice(self.V, p=self.P[x]))
            out.append(x)
        return [f"a{v}" for v in out]

    def tune_mix(self, target_ratio: float, ratio_fn, n: int = 3000, mean_len: float = 4.6):
        lo, hi = 0.0, 1.0
        rng = np.random.default_rng(self.seed + 7)
        for _ in range(12):
            mid = 0.5 * (lo + hi)
            self.set_mix(mid)
            texts = [self.make_text(rng, max(2, int(round(rng.exponential(mean_len))))) for _ in range(n)]
            r = ratio_fn(texts)
            if r < target_ratio:
                lo = mid
            else:
                hi = mid
        self.set_mix(0.5 * (lo + hi))
        return self.mix


class RaoType1(Control):
    name = "rao_type1"
    kind = "trivial"

    def __init__(self, seed: int, concentration: float = 1.0, V: int = 420):
        super().__init__(seed, concentration)
        self.V = V
        self.succ = self.rng0.permutation(V)

    def make_text(self, rng, L):
        x = int(rng.integers(self.V))
        out = [x]
        for _ in range(L - 1):
            x = int(self.succ[x])
            out.append(x)
        return [f"r{v}" for v in out]


class RaoType2(Control):
    name = "rao_type2"
    kind = "trivial"

    def __init__(self, seed: int, concentration: float = 1.0, V: int = 420):
        super().__init__(seed, concentration)
        self.V = V

    def make_text(self, rng, L):
        return [f"u{int(v)}" for v in rng.integers(self.V, size=L)]


CONTROLS = {c.name: c for c in [Heraldry, AdminTags, MarkovEmblem, Adversarial, RaoType1, RaoType2]}
