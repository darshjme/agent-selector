"""agent-selector: Strategy-based model and agent selection for LLM applications."""

from .candidate import Candidate
from .selector import Selector
from .strategies import (
    RoundRobinSelector,
    RandomSelector,
    CheapestSelector,
    TagSelector,
    LoadBalancedSelector,
)
from .chain import SelectorChain

__all__ = [
    "Candidate",
    "Selector",
    "RoundRobinSelector",
    "RandomSelector",
    "CheapestSelector",
    "TagSelector",
    "LoadBalancedSelector",
    "SelectorChain",
]

__version__ = "0.1.0"
