# Contributing to agent-selector

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/darshjme-codes/agent-selector
cd agent-selector
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All 35 tests must pass before submitting a PR.

## Adding a New Strategy

1. Create a class in `src/agent_selector/strategies.py` that inherits from `Selector`.
2. Implement `select(self, context=None) -> Candidate`.
3. Export it from `src/agent_selector/__init__.py`.
4. Add ≥ 4 tests in `tests/test_strategies.py`.
5. Document it in `README.md`.

## Code Style

- Follow PEP 8.
- Type-annotate all public methods.
- Write docstrings for public classes and methods.
- No runtime dependencies — stdlib only.

## Pull Request Process

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-new-strategy`.
3. Commit your changes with clear messages.
4. Open a PR against `main`.
5. Ensure CI is green.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
