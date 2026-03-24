"""Tests for SelectorChain."""

import pytest
from agent_selector import (
    Candidate,
    SelectorChain,
    TagSelector,
    CheapestSelector,
    RoundRobinSelector,
)


def noop(*a, **k):
    return None


def make_candidates():
    return [
        Candidate("alpha", noop, cost_per_call=0.05, tags=["fast"]),
        Candidate("beta",  noop, cost_per_call=0.01, tags=["cheap"]),
    ]


class TestSelectorChain:
    def test_first_selector_succeeds(self):
        chain = SelectorChain([CheapestSelector(make_candidates())])
        assert chain.select().name == "beta"

    def test_falls_back_on_failure(self):
        # TagSelector with "nonexistent" will fail; CheapestSelector catches
        tag_sel = TagSelector(make_candidates())
        cheap_sel = CheapestSelector(make_candidates())
        chain = SelectorChain([tag_sel, cheap_sel])
        c = chain.select({"tags": ["nonexistent"]})
        assert c.name == "beta"

    def test_all_fail_raises(self):
        # Both selectors have no candidates
        chain = SelectorChain([TagSelector(), CheapestSelector()])
        with pytest.raises(ValueError, match="All selectors"):
            chain.select({"tags": ["fast"]})

    def test_empty_selectors_list_raises(self):
        with pytest.raises(ValueError, match="at least one"):
            SelectorChain([])

    def test_selectors_property(self):
        s1 = RoundRobinSelector(make_candidates())
        s2 = CheapestSelector(make_candidates())
        chain = SelectorChain([s1, s2])
        assert len(chain.selectors) == 2

    def test_context_forwarded(self):
        tag_sel = TagSelector(make_candidates())
        chain = SelectorChain([tag_sel])
        c = chain.select({"tags": ["fast"]})
        assert c.name == "alpha"
