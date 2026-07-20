# Reasoning Policy

> **Version**: 1.0.0
> **Compiled to**: `system_prompt_v1.md` → [REASONING]
> **Spec Ref**: AI-0001-Part2 §2 (Thinking Mode), AI-0002-NVIDIA-NIM-API.md §4 (extra_body)
> **Experiment Ref**: EXP-0003-Thinking.md

---

## Reasoning Modes

### Mode 0 — Direct (No Thinking)
For simple factual, conversational, and classification queries.
- budget_tokens: disabled
- Trigger: `/nothink` prefix OR simple query detection
- Latency: ~2-5s
- Token cost: minimal

### Mode 1 — Standard Thinking
For complex analysis, technical explanation, multi-step problems.
- budget_tokens: 5,000–10,000
- Trigger: default for complex queries
- Latency: ~15-30s
- Token cost: moderate

### Mode 2 — Deep Thinking
For proofs, debugging complex systems, architecture design, research synthesis.
- budget_tokens: 16,000–32,000
- Trigger: `/think` prefix OR explicit high-complexity detection
- Latency: ~45-90s
- Token cost: high

---

## Activation via extra_body

Per AI-0002 and AI-0003-OpenWebUI-Compatibility.md:

```python
# Standard thinking
extra_body = {
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
    }
}

# Deep thinking
extra_body = {
    "thinking": {
        "type": "enabled",
        "budget_tokens": 32000
    }
}

# Disabled
extra_body = {
    "thinking": {
        "type": "disabled"
    }
}
```

**Never** use `thinking=True` as a top-level API parameter (ref: AI-0003 §4.3).

---

## Reasoning Process (Internal)

When thinking is active, the model follows this internal sequence:
1. **Decompose** — break the problem into sub-problems
2. **Identify Assumptions** — list what is being assumed
3. **Generate Candidates** — produce 2-3 candidate approaches
4. **Evaluate** — score candidates against accuracy and efficiency
5. **Select** — commit to best candidate
6. **Validate** — check for errors, contradictions, missing cases
7. **Respond** — produce final output only

The user sees only the final output (step 7), not the internal process.

---

## Budget Token Allocation by Task Type

| Task | Budget Tokens | Mode |
|------|--------------|------|
| Factual question | 0 (disabled) | Mode 0 |
| Summarization | 2,000 | Mode 1 |
| Code explanation | 5,000 | Mode 1 |
| Code debugging | 10,000–16,000 | Mode 1-2 |
| System design | 16,000 | Mode 2 |
| Mathematical proof | 32,000 | Mode 2 |
| Research synthesis | 16,000 | Mode 2 |
| Business analysis | 10,000 | Mode 1-2 |
| Creative writing | 5,000 | Mode 1 |

Ref: benchmark/tests/nim/TC-0003.md for empirical validation targets.
