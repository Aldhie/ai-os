# Context Budget Specification

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Budget Tiers

```yaml
budgets:

  tier_minimal:     # greeting, simple fact
    total: 4000
    system_prompt: 2000
    message: 1000
    response_reserve: 1000

  tier_standard:    # most conversations
    total: 16000
    system_prompt: 2500
    history: 3000
    memory: 2000
    rag: 4000
    message: 1500
    response_reserve: 3000

  tier_deep:        # architecture, analysis, complex tasks
    total: 32000
    system_prompt: 3000
    history: 5000
    memory: 3000
    rag: 8000
    message: 2000
    planner: 2000
    reflection: 2000
    response_reserve: 5000

  tier_maximum:     # document analysis, rare
    total: 64000
    # Use only when explicitly requested
    # Incurs significant latency and token cost
    # Not recommended on free tier
```

---

## Budget Selection

| Task Classification | Budget Tier |
|--------------------|-------------|
| Greeting | minimal |
| Simple fact | minimal |
| Casual conversation | standard |
| Business analysis | standard |
| Research synthesis | deep |
| Architecture design | deep |
| Document analysis | maximum |
| Debugging | standard |
| Creative writing | standard |

---

## Free Tier Guard

```
Daily token budget: estimate 1M total tokens
1000 requests/day × average 1000 tokens = 1M tokens

If request would exceed daily estimate:
  → Degrade to tier_minimal
  → Disable planner, reflection, critic
  → Truncate RAG to top-2 chunks
  → Notify user if degradation is significant
```

---

*File: runtime/openwebui/context/context_budget.md | Last updated: 2026-07-20*
