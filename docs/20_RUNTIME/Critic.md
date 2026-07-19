# Critic

| Field | Value |
|---|---|
| **Title** | AI-OS Critic Module Specification |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines the Critic module, which performs the final quality gate before a response is delivered to the user. The Critic evaluates outputs against predefined rubrics, assigning scores and blocking responses that fall below threshold.

---

## Scope

- Final stage in AI-OS runtime pipeline
- Evaluates: response quality, safety, format compliance, factual integrity
- Output: Pass/Block decision + structured critique

---

## Critic Rubric

| Dimension | Weight | Description |
|---|---|---|
| Accuracy | 30% | Are facts correct and verifiable? |
| Relevance | 25% | Does the response address the query? |
| Format | 15% | Is formatting appropriate and Markdown-valid? |
| Safety | 20% | Is the response safe and policy-compliant? |
| Conciseness | 10% | Is the response appropriately concise? |

**Passing Score:** ≥80% weighted average.

---

## Critic Output Schema

```json
{
  "critique": {
    "accuracy": {"score": 0.0, "comment": "string"},
    "relevance": {"score": 0.0, "comment": "string"},
    "format": {"score": 0.0, "comment": "string"},
    "safety": {"score": 0.0, "comment": "string"},
    "conciseness": {"score": 0.0, "comment": "string"},
    "weighted_score": 0.0,
    "decision": "pass | block | revise",
    "revision_guidance": "string"
  }
}
```

---

## Critic Prompt

See: `prompts/nemotron-ultra/critic.txt`

---

## Critic Parameters

| Parameter | Value | Reason |
|---|---|---|
| Temperature | 0.2 | Highly deterministic scoring |
| Max Tokens | 1024 | Concise critique only |
| Format | JSON | Machine-parsable scores |

---

## Decision Rules

| Weighted Score | Decision | Action |
|---|---|---|
| ≥80% | Pass | Deliver response to user |
| 60–79% | Revise | Send back to reflection loop |
| <60% | Block | Regenerate from scratch |
| Safety <0.8 | Block | Immediate block regardless of other scores |

---

## Dependencies

- `prompts/nemotron-ultra/critic.txt`
- `docs/20_RUNTIME/Reflection.md`
- `docs/20_RUNTIME/Planner.md`

---

## References

- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)
- [RLHF and Reward Modeling](https://arxiv.org/abs/2203.02155)

---

## TODO

- [ ] Write critic prompt in `prompts/nemotron-ultra/critic.txt`
- [ ] Implement weighted scoring calculator
- [ ] Test critic with known good and bad responses
- [ ] Tune safety dimension threshold
- [ ] Build critic audit log for quality tracking
