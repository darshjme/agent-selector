# agent-selector

**Strategy-based model and agent selection for LLM applications.**

Stop writing `if model == "gpt4" ... elif model == "claude" ...` chains.
`agent-selector` gives you pluggable, composable routing strategies to decide which LLM or agent variant handles each request.

---

## Installation

```bash
pip install agent-selector
```

Python ≥ 3.10 required. Zero runtime dependencies.

---

## Quick Start — Multi-Model LLM Routing

```python
from agent_selector import (
    Candidate,
    TagSelector,
    CheapestSelector,
    RoundRobinSelector,
    LoadBalancedSelector,
    RandomSelector,
    SelectorChain,
)

# ── 1. Define your models as Candidates ──────────────────────────────────────

def call_gpt4o(prompt: str) -> str:
    # your openai client call here
    return f"[gpt-4o] {prompt}"

def call_claude3(prompt: str) -> str:
    # your anthropic client call here
    return f"[claude-3-opus] {prompt}"

def call_gemini(prompt: str) -> str:
    # your google client call here
    return f"[gemini-1.5-pro] {prompt}"

def call_local_llama(prompt: str) -> str:
    # ollama / llama.cpp call here
    return f"[llama-3-8b-local] {prompt}"

gpt4o     = Candidate("gpt-4o",          call_gpt4o,      cost_per_call=0.01,  tags=["powerful", "vision"])
claude3   = Candidate("claude-3-opus",   call_claude3,    cost_per_call=0.015, tags=["powerful", "reasoning"])
gemini    = Candidate("gemini-1.5-pro",  call_gemini,     cost_per_call=0.007, tags=["fast", "vision"])
llama_local = Candidate("llama-3-8b",   call_local_llama, cost_per_call=0.0,  tags=["fast", "cheap"])

# ── 2. Pick a strategy ───────────────────────────────────────────────────────

# Always cheapest first
cheapest = CheapestSelector([gpt4o, claude3, gemini, llama_local])
print(cheapest.select().name)          # → llama-3-8b  (cost 0.0)

# Tag-based: pick by capability required
tag_sel = TagSelector([gpt4o, claude3, gemini, llama_local])
model = tag_sel.select({"tags": ["vision"]})
print(model.name)                      # → gpt-4o  (first with "vision" tag)

# Round-robin across two primary models
rr = RoundRobinSelector([gpt4o, claude3])
for _ in range(4):
    print(rr.select().name)            # gpt-4o, claude-3-opus, gpt-4o, claude-3-opus

# Load balanced — fewest calls wins
lb = LoadBalancedSelector([gpt4o, claude3, gemini])
for _ in range(5):
    print(lb.select().name)
print(lb.call_counts())                # {'gpt-4o': 2, 'claude-3-opus': 2, 'gemini-1.5-pro': 1}

# ── 3. Chain strategies as fallbacks ─────────────────────────────────────────

# Try tag match first; if nothing matches, fall back to cheapest
chain = SelectorChain([
    TagSelector([gpt4o, claude3, gemini, llama_local]),
    CheapestSelector([gpt4o, claude3, gemini, llama_local]),
])

# Request requiring "reasoning" capability
chosen = chain.select({"tags": ["reasoning"]})
print(chosen.name)                     # → claude-3-opus

# Request with an unmatchable tag → falls back to cheapest
chosen = chain.select({"tags": ["unknown-capability"]})
print(chosen.name)                     # → llama-3-8b

# ── 4. Use the handler directly ──────────────────────────────────────────────

user_prompt = "Explain transformers in one paragraph."
selected_model = chain.select({"tags": ["powerful"]})
response = selected_model.handler(user_prompt)
print(response)
```

---

## Strategies

| Strategy | Description |
|---|---|
| `RoundRobinSelector` | Cycles through candidates in registration order |
| `RandomSelector` | Weighted-random selection (`candidate.weight`) |
| `CheapestSelector` | Always picks the lowest `cost_per_call` candidate |
| `TagSelector` | Picks first candidate whose tags are a superset of `context["tags"]` |
| `LoadBalancedSelector` | Tracks call counts; picks the least-used candidate |
| `SelectorChain` | Tries selectors in order; first success wins |

---

## API Reference

### `Candidate`

```python
Candidate(
    name: str,
    handler: callable,
    cost_per_call: float = 0.0,
    tags: list[str] = None,
    weight: float = 1.0,
)
```

- `.to_dict()` → serialisable dict (handler excluded)

### `Selector` (base)

- `.add(candidate) -> Selector` — fluent
- `.select(context=None) -> Candidate` — abstract
- `.candidates -> list[Candidate]`

### `SelectorChain`

```python
SelectorChain(selectors: list[Selector])
chain.select(context=None) -> Candidate
```

---

## License

MIT © Darshankumar Joshi
