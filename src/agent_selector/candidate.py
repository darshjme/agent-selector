"""Candidate — a selectable option (model, agent variant, etc.)."""

from __future__ import annotations
from typing import Callable, Any


class Candidate:
    """Represents a selectable option such as an LLM model or agent variant.

    Args:
        name: Unique identifier for this candidate.
        handler: Callable that handles requests routed to this candidate.
        cost_per_call: Estimated monetary cost per invocation (default 0.0).
        tags: Optional list of capability/category tags.
        weight: Relative selection weight for weighted-random strategies (default 1.0).
    """

    def __init__(
        self,
        name: str,
        handler: Callable[..., Any],
        cost_per_call: float = 0.0,
        tags: list[str] | None = None,
        weight: float = 1.0,
    ) -> None:
        if not name:
            raise ValueError("Candidate name must be a non-empty string.")
        if not callable(handler):
            raise TypeError("handler must be callable.")
        if cost_per_call < 0:
            raise ValueError("cost_per_call must be >= 0.")
        if weight <= 0:
            raise ValueError("weight must be > 0.")

        self.name = name
        self.handler = handler
        self.cost_per_call = cost_per_call
        self.tags: list[str] = list(tags) if tags else []
        self.weight = weight

    def to_dict(self) -> dict:
        """Return a serialisable representation (handler excluded)."""
        return {
            "name": self.name,
            "cost_per_call": self.cost_per_call,
            "tags": self.tags,
            "weight": self.weight,
        }

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"Candidate(name={self.name!r}, cost={self.cost_per_call}, "
            f"tags={self.tags}, weight={self.weight})"
        )
