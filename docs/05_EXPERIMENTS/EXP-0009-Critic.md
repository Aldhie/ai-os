# EXP-0009: Critic Agent Quality

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0009 |
| **Title** | Critic Agent: External Critique Accuracy and Calibration |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | High |

---

## Cross References

- [EXP-0008 — Reflection](EXP-0008-Reflection.md)
- [EXP-0007 — Planner](EXP-0007-Planner.md)
- [AI-0001 — Nemotron Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)

---

## 1. Objective

Measure the quality of Nemotron Ultra 550B acting as an external critic for another model's output: accuracy of critique, calibration (does it criticize bad outputs more than good ones?), and actionability of feedback.

---

## 2. Hypothesis

> `[HYPOTHESIS]` With `/think` enabled, Nemotron Ultra 550B in critic role correctly identifies >80% of logical errors in provided text. Calibration is good (criticizes bad texts more than good texts). Critique is actionable (provides specific corrections).

---

## 3. Test Cases

| Input Type | Description |
|------------|-------------|
| Good output | High-quality, correct response (expect minimal critique) |
| Logically flawed | Contains a valid-sounding but incorrect argument |
| Factually flawed | Contains specific false claims |
| Code with bug | Python function with an off-by-one error |
| Ambiguous | Partially correct; critic should identify what is missing |

---

## 4. Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Correctly identifies flaws in flawed inputs | 40% |
| Does not hallucinate flaws in good inputs | 30% |
| Critique is specific and actionable | 20% |
| Critique is concise (not verbose) | 10% |

---

## 5. Actual Result

> `[PENDING]`

---

## 6. Decision

> `[PENDING]` Decide on critic agent integration in agentic workflow.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
