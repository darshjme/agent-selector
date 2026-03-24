"""SelectorChain — tries selectors in order until one succeeds."""

from __future__ import annotations

from typing import List

from .candidate import Candidate
from .selector import Selector


class SelectorChain:
    """Attempts each selector in sequence; returns the first successful result.

    This is useful for fallback logic, e.g. try TagSelector first, then
    CheapestSelector if no tag match is found.

    Args:
        selectors: Ordered list of Selector instances to try.

    Raises:
        ValueError: If all selectors raise or return nothing.
    """

    def __init__(self, selectors: List[Selector]) -> None:
        if not selectors:
            raise ValueError("SelectorChain requires at least one selector.")
        self._selectors = list(selectors)

    def select(self, context: dict | None = None) -> Candidate:
        """Try each selector in order; return the first successful Candidate.

        Raises:
            ValueError: If every selector in the chain fails.
        """
        last_exc: Exception | None = None
        for selector in self._selectors:
            try:
                return selector.select(context)
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                continue

        raise ValueError(
            f"All selectors in the chain failed. Last error: {last_exc}"
        ) from last_exc

    @property
    def selectors(self) -> List[Selector]:
        """Read-only view of the registered selectors."""
        return list(self._selectors)
