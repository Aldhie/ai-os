# Reflection

| Field | Value |
|---|---|
| **Title** | AI-OS Reflection Module Specification |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines the Reflection module, which enables AI-OS to self-evaluate its own outputs before presenting them to the user. Reflection implements a meta-cognitive loop that checks for accuracy, completeness, and alignment with the user's intent.

---

## Scope

- Applied after each major output generation
- Operates on: reasoning traces, factual claims, plan steps, code
- Consumed by: Critic module for final quality gate

---

## Reflection Loop

```text
Draft Response
    │
    ▼
[Reflection Module]
    │
    ├── Accuracy Check:     Are all facts verifiable?
    ├── Completeness Check: Does this fully answer the question?
    ├── Alignment Check:    Does this match the user's intent?
    ├── Constraint Check:   Are all persona/policy rules respected?
    └── Quality Check:      Is this the best possible response?
    │
    ├── PASS ───► [Critic]
    └── FAIL ───► [Re-generation with context]
```

---

## Reflection Output Schema

```json
{
  "reflection": {
    "accuracy": {"score": 0.0, "issues": []},
    "completeness": {"score": 0.0, "missing": []},
    "alignment": {"score": 0.0, "issues": []},
    "constraints": {"score": 0.0, "violations": []},
    "overall": "pass | fail",
    "revision_notes": "string"
  }
}
```

---

## Reflection Prompt

See: `prompts/nemotron-ultra/reflection.txt`

---

## Reflection Parameters

| Parameter | Value | Reason |
|---|---|---|
| Temperature | 0.4 | Semi-deterministic evaluation |
| Max Tokens | 2048 | Reflection notes are concise |
| Format | JSON | Machine-parsable |

---

## Pass/Fail Thresholds

| Check | Pass Threshold |
|---|---|
| Accuracy | ≥0.85 |
| Completeness | ≥0.80 |
| Alignment | ≥0.90 |
| Constraints | 1.00 (no violations) |

---

## Max Iterations

- Maximum reflection-regeneration cycles: **3**
- After 3 failures: escalate to user with honest acknowledgment of limitations.

---

## Dependencies

- `prompts/nemotron-ultra/reflection.txt`
- `docs/20_RUNTIME/Planner.md`
- `docs/20_RUNTIME/Critic.md`

---

## References

- [Self-Refine: Iterative Refinement with LLMs](https://arxiv.org/abs/2303.17651)
- [Reflexion: Language Agents with Verbal Reinforcement](https://arxiv.org/abs/2303.11366)

---

## TODO

- [ ] Write reflection prompt in `prompts/nemotron-ultra/reflection.txt`
- [ ] Implement reflection score parser
- [ ] Define regeneration strategy on failure
- [ ] Test reflection loop with adversarial inputs
- [ ] Measure quality improvement vs no-reflection baseline
