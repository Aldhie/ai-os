# EXP-0008: Reflection Capability — Self-Correction and Error Detection

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0008 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0004 |

## Related Documents

- ↑ [REQ-AI-0004](../00_ENGINEERING/REQ-INDEX.md#req-ai-0004)
- → [EXP-0007 Planner](./EXP-0007-Planner.md)
- → [EXP-0009 Critic](./EXP-0009-Critic.md)

---

## Objective

Evaluate the model's ability to reflect on its own outputs, detect errors, and self-correct when explicitly asked to review its previous response. Determine whether reflection prompts improve final output quality.

---

## Hypothesis

**H1:** When asked to "review and improve your previous answer", the model identifies and corrects >70% of planted errors.

**H2:** Reflection with thinking ON detects more subtle errors than reflection with thinking OFF.

**H3:** Multiple reflection rounds (reflect-once vs reflect-twice) produce diminishing returns after the first reflection.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| Reflection rounds | Independent | 0 (no reflection), 1, 2 |
| Error type | Independent | Factual, Logical, Code bug, Missing step |
| Thinking mode | Independent | OFF, ON |
| Error visibility | Independent | Obvious, Subtle |

---

## Procedure

1. Create 5 initial responses with planted errors (factual, logical, code).
2. Ask model to: "Review your previous response and identify any errors. Provide a corrected version."
3. Measure: (a) error detection rate, (b) correction accuracy, (c) introduction of new errors during correction.
4. Repeat with thinking ON vs OFF.
5. For promising configurations: run second reflection round, measure improvement delta.

---

## Expected Result

| Config | Detection Rate | Correction Rate | New Errors Introduced |
|--------|---------------|-----------------|----------------------|
| Think OFF | ~60% | ~50% | ~10% |
| Think ON | ~80% | ~75% | ~5% |
| Think ON, round 2 | ~82% | ~77% | ~5% |

---

## Actual Result

*Status: Not yet executed.*

---

## Benchmark Result

*Pending execution.*

---

*EXP-0008 v1.0.0 — Created 2026-07-20*
