# Runtime Critic

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | Critic.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the Critic component of the AI OS runtime. The Critic evaluates planned steps and generated outputs against quality and safety standards before execution or delivery.

---

## Scope

- Critic design and role
- Evaluation rubric
- Integration with Planner and Reflection
- Override and escalation policy

---

## Dependencies

- `docs/20_RUNTIME/Planner.md` — plans evaluated by Critic
- `docs/20_RUNTIME/Reflection.md` — outputs refined with Critic feedback
- `docs/20_RUNTIME/Workflow.md` — Critic position in the workflow
- `prompts/nemotron-ultra/critic.txt` — critic prompt

---

## References

- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)
- [LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)

---

## Critic Role

The Critic acts as an internal quality gate:

```
Plan or Draft Response
    ↓
[CRITIC] Evaluate against rubric
    ↓
Approved? → Proceed
Rejected? → Return to Planner / Reflector with feedback
```

---

## Evaluation Rubric

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Safety | Critical | No harmful, illegal, or unethical content |
| Accuracy | High | Factually correct and supported |
| Relevance | High | Directly addresses the user's request |
| Quality | Medium | Well-structured, clear, and concise |
| Completeness | Medium | All parts of the request addressed |

---

## Override Policy

- Safety violations are **non-negotiable** — the Critic always blocks unsafe outputs
- Quality issues trigger revision, not hard block
- Maximum 2 revision cycles before delivering best available response

---

## TODO

- [ ] Write critic prompt v0.1.0
- [ ] Define scoring thresholds for each dimension
- [ ] Test Critic with adversarial benchmark cases
- [ ] Measure false positive rate (good responses blocked)
- [ ] Log all Critic interventions for analysis
