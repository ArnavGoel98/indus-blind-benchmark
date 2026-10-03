"""Shared plug-in interface for decipherment / analysis methods.

Every method implements ``analyze(corpus, knowledge) -> Prediction``. A method may fill any
subset of the four task outputs:

  A  ``ling_score``     larger = more language-like (a threshold is learned by the evaluator
                        with leave-one-source-out cross-validation, so no method sees its
                        test corpus's source when its decision rule is set)
  B  ``script_type`` or ``script_features`` (the evaluator trains a classifier on features)
  C  ``family`` (+ ``family_scores``)
  D  ``sign_values``    sign ID -> predicted value (a unit string)

Methods never see the answer key. ``Knowledge`` is what a decipherer is assumed to know for
the given knowledge tier (Judge fix #4).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ..corpus import Corpus


@dataclass
class Reference:
    """A known language, in the same unit level as the script being attacked."""

    name: str
    family: str
    texts: list[list[str]]                       # unit sequences (one per clause)
    words: dict[tuple[str, ...], int]            # word (as units) -> count
    to_hidden: dict[str, str] = field(default_factory=dict)  # reference unit -> hidden-language cognate


@dataclass
class Knowledge:
    tier: str = "none"                   # related | candidates | none
    script_type: str | None = None       # oracle script type (an optimistic assumption; see README)
    references: list[Reference] = field(default_factory=list)


@dataclass
class Prediction:
    method: str
    features: dict[str, float] = field(default_factory=dict)
    ling_score: float | None = None
    script_type: str | None = None
    script_features: dict[str, float] | None = None
    family: str | None = None
    family_scores: dict[str, float] = field(default_factory=dict)
    sign_values: dict[int, str] | None = None
    segmentation: list[list[int]] | None = None
    extra: dict[str, Any] = field(default_factory=dict)


class Method(ABC):
    name: str = "method"
    tasks: tuple[str, ...] = ()
    paper: str = ""
    deviations: str = ""
    needs_knowledge: bool = False
    decision: str = "threshold"          # how the evaluator turns ling_score into a Task-A label

    @abstractmethod
    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction: ...

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "tasks": list(self.tasks), "paper": self.paper, "deviations": self.deviations}
