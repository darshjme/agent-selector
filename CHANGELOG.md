# Changelog

All notable changes to **agent-selector** are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.1.0] — 2026-03-24

### Added
- `Candidate` — selectable option with name, handler, cost, tags, and weight.
- `Selector` — abstract base class with fluent `.add()` builder.
- `RoundRobinSelector` — cycles candidates in registration order.
- `RandomSelector` — weighted-random selection via `candidate.weight`.
- `CheapestSelector` — always picks lowest `cost_per_call` candidate.
- `TagSelector` — subset-match on `context["tags"]`.
- `LoadBalancedSelector` — tracks call counts, picks least-used candidate.
- `SelectorChain` — composes selectors with fallback semantics.
- 35 pytest tests (100 % passing).
- Zero runtime dependencies (Python stdlib only: `random`, `collections`).
