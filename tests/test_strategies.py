"""Tests for concrete selector strategies."""

import pytest
from agent_selector import (
    Candidate,
    RoundRobinSelector,
    RandomSelector,
    CheapestSelector,
    TagSelector,
    LoadBalancedSelector,
)


def noop(*a, **k):
    return None


def make_candidates():
    return [
        Candidate("alpha", noop, cost_per_call=0.05, tags=["fast"]),
        Candidate("beta",  noop, cost_per_call=0.01, tags=["cheap", "fast"]),
        Candidate("gamma", noop, cost_per_call=0.10, tags=["vision"]),
    ]


# ==================================================================
# RoundRobinSelector
# ==================================================================

class TestRoundRobin:
    def test_cycles_in_order(self):
        sel = RoundRobinSelector(make_candidates())
        names = [sel.select().name for _ in range(6)]
        assert names == ["alpha", "beta", "gamma", "alpha", "beta", "gamma"]

    def test_fluent_add(self):
        sel = RoundRobinSelector()
        c = make_candidates()[0]
        result = sel.add(c)
        assert result is sel
        assert sel.select().name == "alpha"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            RoundRobinSelector().select()

    def test_reset(self):
        sel = RoundRobinSelector(make_candidates())
        sel.select()
        sel.select()
        sel.reset()
        assert sel.select().name == "alpha"


# ==================================================================
# RandomSelector
# ==================================================================

class TestRandom:
    def test_returns_candidate(self):
        sel = RandomSelector(make_candidates())
        c = sel.select()
        assert c.name in {"alpha", "beta", "gamma"}

    def test_weighted_distribution(self):
        heavy = Candidate("heavy", noop, weight=1000.0)
        light = Candidate("light", noop, weight=0.001)
        sel = RandomSelector([heavy, light])
        results = [sel.select().name for _ in range(200)]
        assert results.count("heavy") > 190  # overwhelmingly heavy

    def test_single_candidate(self):
        c = Candidate("only", noop)
        sel = RandomSelector([c])
        assert sel.select().name == "only"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            RandomSelector().select()


# ==================================================================
# CheapestSelector
# ==================================================================

class TestCheapest:
    def test_picks_cheapest(self):
        sel = CheapestSelector(make_candidates())
        assert sel.select().name == "beta"   # cost 0.01

    def test_tie_picks_first(self):
        c1 = Candidate("x", noop, cost_per_call=0.0)
        c2 = Candidate("y", noop, cost_per_call=0.0)
        sel = CheapestSelector([c1, c2])
        assert sel.select().name == "x"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            CheapestSelector().select()


# ==================================================================
# TagSelector
# ==================================================================

class TestTag:
    def test_match_single_tag(self):
        sel = TagSelector(make_candidates())
        c = sel.select({"tags": ["vision"]})
        assert c.name == "gamma"

    def test_match_multi_tag(self):
        sel = TagSelector(make_candidates())
        c = sel.select({"tags": ["cheap", "fast"]})
        assert c.name == "beta"

    def test_no_tags_in_context_returns_first(self):
        sel = TagSelector(make_candidates())
        # empty required_tags -> issubset of everything -> first candidate
        c = sel.select({})
        assert c.name == "alpha"

    def test_none_context_returns_first(self):
        sel = TagSelector(make_candidates())
        c = sel.select(None)
        assert c.name == "alpha"

    def test_no_match_raises(self):
        sel = TagSelector(make_candidates())
        with pytest.raises(ValueError, match="No candidate"):
            sel.select({"tags": ["nonexistent"]})

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            TagSelector().select({"tags": ["fast"]})


# ==================================================================
# LoadBalancedSelector
# ==================================================================

class TestLoadBalanced:
    def test_distributes_evenly(self):
        sel = LoadBalancedSelector(make_candidates())
        names = [sel.select().name for _ in range(6)]
        # Each of 3 candidates should be picked exactly twice
        assert sorted(names) == sorted(["alpha", "beta", "gamma"] * 2)

    def test_call_counts(self):
        sel = LoadBalancedSelector(make_candidates())
        sel.select(); sel.select(); sel.select()
        counts = sel.call_counts()
        assert sum(counts.values()) == 3
        assert all(v == 1 for v in counts.values())

    def test_reset_counts(self):
        sel = LoadBalancedSelector(make_candidates())
        sel.select(); sel.select()
        sel.reset_counts()
        assert sum(sel.call_counts().values()) == 0

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            LoadBalancedSelector().select()
