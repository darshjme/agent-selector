"""Tests for Candidate."""

import pytest
from agent_selector import Candidate


def noop(*args, **kwargs):
    return None


# --- construction ---

def test_candidate_basic_creation():
    c = Candidate("gpt-4o", noop)
    assert c.name == "gpt-4o"
    assert c.cost_per_call == 0.0
    assert c.tags == []
    assert c.weight == 1.0


def test_candidate_with_all_params():
    c = Candidate("claude-3", noop, cost_per_call=0.01, tags=["fast", "vision"], weight=2.5)
    assert c.cost_per_call == 0.01
    assert c.tags == ["fast", "vision"]
    assert c.weight == 2.5


def test_candidate_to_dict():
    c = Candidate("gemini", noop, cost_per_call=0.002, tags=["cheap"], weight=3.0)
    d = c.to_dict()
    assert d == {"name": "gemini", "cost_per_call": 0.002, "tags": ["cheap"], "weight": 3.0}


def test_candidate_empty_name_raises():
    with pytest.raises(ValueError, match="non-empty"):
        Candidate("", noop)


def test_candidate_non_callable_handler_raises():
    with pytest.raises(TypeError, match="callable"):
        Candidate("x", "not_a_function")  # type: ignore[arg-type]


def test_candidate_negative_cost_raises():
    with pytest.raises(ValueError, match="cost_per_call"):
        Candidate("x", noop, cost_per_call=-1.0)


def test_candidate_zero_weight_raises():
    with pytest.raises(ValueError, match="weight"):
        Candidate("x", noop, weight=0.0)


def test_candidate_tags_are_copied():
    original = ["a", "b"]
    c = Candidate("x", noop, tags=original)
    original.append("c")
    assert c.tags == ["a", "b"]
