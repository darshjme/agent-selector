"""Concrete selection strategies."""

from __future__ import annotations

import random
from collections import Counter
from typing import List

from .candidate import Candidate
from .selector import Selector


class RoundRobinSelector(Selector):
    """Cycles through candidates in registration order."""

    def __init__(self, candidates: List[Candidate] | None = None) -> None:
        super().__init__(candidates)
        self._index: int = 0

    def select(self, context: dict | None = None) -> Candidate:
        self._require_candidates()
        candidate = self._candidates[self._index % len(self._candidates)]
        self._index += 1
        return candidate

    def reset(self) -> None:
        """Reset the round-robin cursor to the beginning."""
        self._index = 0


class RandomSelector(Selector):
    """Selects a candidate at random, weighted by ``candidate.weight``."""

    def select(self, context: dict | None = None) -> Candidate:
        self._require_candidates()
        weights = [c.weight for c in self._candidates]
        (chosen,) = random.choices(self._candidates, weights=weights, k=1)
        return chosen


class CheapestSelector(Selector):
    """Always picks the candidate with the lowest ``cost_per_call``."""

    def select(self, context: dict | None = None) -> Candidate:
        self._require_candidates()
        return min(self._candidates, key=lambda c: c.cost_per_call)


class TagSelector(Selector):
    """Returns the first candidate whose tags are a superset of *context[\"tags\"]*.

    If ``context`` is ``None`` or has no ``"tags"`` key, falls back to the first
    candidate (if any), otherwise raises ``ValueError``.
    """

    def select(self, context: dict | None = None) -> Candidate:
        self._require_candidates()

        required_tags: set[str] = set()
        if context and "tags" in context:
            required_tags = set(context["tags"])

        for candidate in self._candidates:
            if required_tags.issubset(set(candidate.tags)):
                return candidate

        raise ValueError(
            f"No candidate found whose tags include all of {sorted(required_tags)}."
        )


class LoadBalancedSelector(Selector):
    """Tracks per-candidate call counts and picks the least-used one.

    Ties are broken by insertion order (first registered wins).
    """

    def __init__(self, candidates: List[Candidate] | None = None) -> None:
        super().__init__(candidates)
        self._call_counts: Counter[str] = Counter()

    def add(self, candidate: Candidate) -> "LoadBalancedSelector":
        super().add(candidate)
        return self

    def select(self, context: dict | None = None) -> Candidate:
        self._require_candidates()
        # Pick candidate with minimum call count (stable: first in list wins ties)
        chosen = min(self._candidates, key=lambda c: self._call_counts[c.name])
        self._call_counts[chosen.name] += 1
        return chosen

    def call_counts(self) -> dict[str, int]:
        """Return a dict mapping candidate names to their call counts."""
        return dict(self._call_counts)

    def reset_counts(self) -> None:
        """Zero all call counters."""
        self._call_counts.clear()
