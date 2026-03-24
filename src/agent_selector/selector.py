"""Base Selector abstract class."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from .candidate import Candidate


class Selector(ABC):
    """Abstract base class for all selection strategies.

    Args:
        candidates: Optional initial list of Candidate objects.
    """

    def __init__(self, candidates: List[Candidate] | None = None) -> None:
        self._candidates: List[Candidate] = list(candidates) if candidates else []

    # ------------------------------------------------------------------
    # Fluent builder
    # ------------------------------------------------------------------

    def add(self, candidate: Candidate) -> "Selector":
        """Add a candidate and return *self* for fluent chaining.

        Raises:
            TypeError: If *candidate* is not a Candidate instance.
        """
        if not isinstance(candidate, Candidate):
            raise TypeError(f"Expected Candidate, got {type(candidate).__name__}.")
        self._candidates.append(candidate)
        return self

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def select(self, context: dict | None = None) -> Candidate:
        """Select and return one Candidate.

        Args:
            context: Optional dict with runtime hints (e.g. ``{"tags": ["fast"]}``)

        Returns:
            The chosen Candidate.

        Raises:
            ValueError: If no candidates are available or none match.
        """

    # ------------------------------------------------------------------
    # Property
    # ------------------------------------------------------------------

    @property
    def candidates(self) -> List[Candidate]:
        """Read-only view of the registered candidates."""
        return list(self._candidates)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _require_candidates(self) -> None:
        if not self._candidates:
            raise ValueError("No candidates registered.")
