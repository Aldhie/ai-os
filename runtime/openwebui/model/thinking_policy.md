# Thinking Policy

> **Version**: 1.0.0
> **Compiled to**: Cross-referenced by `reasoning_policy.md` and `behavior_spec.md`
> **Spec Ref**: AI-0001-Part2 §2, AI-0002-NVIDIA-NIM-API.md §4, AI-0003-OpenWebUI-Compatibility.md §4.3
> **Experiment Ref**: EXP-0003-Thinking.md

---

## Thinking Mode Architecture

Nemotron Ultra 550B supports extended internal reasoning via the `budget_tokens` parameter.
This is a first-class capability that distinguishes it from standard LLM deployments.

### Correct Activation (API Level)

```json
{
  "extra_body": {
    "thinking": {
      "type": "enabled",
      "budget_tokens": 10000
    }
  }
}
```

### Incorrect Activations (Prohibited)

```python
# WRONG: top-level parameter — silently ignored by NIM
response = client.chat.completions.create(
    thinking=True,  # ← FORBIDDEN
    ...
)

# WRONG: Open WebUI native parameter field
# Setting "thinking": true in Open WebUI parameter UI → ignored
```

Ref: AI-0003-OpenWebUI-Compatibility.md §4.3 — the `thinking` parameter audit finding.

---

## Open WebUI Integration

Open WebUI does not natively support `extra_body` injection.
The correct integration path is via the Open WebUI Pipelines API.

See: `runtime/openwebui/filters/thinking_pipeline.py` (Sprint 1.1)

For now, thinking mode can be activated by:
1. Prepending `/think` to the user's message (if a pipeline is installed)
2. Injecting `extra_body` in a custom pipeline's `inlet()` method
3. Direct API calls bypassing Open WebUI

---

## Budget Token Decision Matrix

| User Signal | Detected Complexity | Budget Tokens |
|-------------|--------------------|--------------|
| `/nothink` prefix | Any | 0 (disabled) |
| `/think` prefix | Any | 16,000 |
| No prefix | Low (factual, casual) | 0 |
| No prefix | Medium (technical, analytical) | 8,000 |
| No prefix | High (proof, design, debug) | 16,000 |
| No prefix | Expert (research, architecture) | 32,000 |

---

## Free Tier Token Conservation

Ref: AI-0005-FreeTier-Strategy.md

Thinking tokens count toward the total token budget per request.
On NVIDIA Free Tier (1,000 req/day):

| Scenario | Daily Budget Impact |
|----------|-------------------|
| All requests with 32K thinking | ~50-100 effective complex queries/day |
| Mixed: 50% Mode 0, 50% Mode 1 (8K) | ~200-300 effective queries/day |
| Recommended profile | 70% Mode 0, 25% Mode 1, 5% Mode 2 |

Use `/nothink` explicitly for:
- Simple factual lookups
- Quick code formatting
- Casual conversation
- Any query where depth is not required
