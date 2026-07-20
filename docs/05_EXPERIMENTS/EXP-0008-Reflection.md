# EXP-0008: Reflection and Self-Correction

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0008 |
| **Title** | Reflection Agent: Self-Correction and Output Improvement Quality |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | High |

---

## Cross References

- [EXP-0007 — Planner](EXP-0007-Planner.md)
- [EXP-0009 — Critic](EXP-0009-Critic.md)
- [AI-0001 — Nemotron Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)

---

## 1. Objective

Measure Nemotron Ultra 550B ability to detect and correct errors in its own previous output when given a reflection prompt. Determine whether reflection improves accuracy beyond first-pass thinking.

---

## 2. Hypothesis

> `[HYPOTHESIS]` A reflection step ("Review your answer and identify any errors") applied to full-thinking outputs improves accuracy by >10% on math and logic tasks. Reflection applied to creative tasks may reduce quality (over-editing).

---

## 3. Test Cases

| Type | Description | Reflection Prompt |
|------|-------------|-------------------|
| Math error | Prompt designed to elicit calculation mistake | "Review your calculation step by step. Identify any error." |
| Logic error | Syllogism with hidden fallacy | "Examine your logic. Is each step valid?" |
| Factual error | Prompt about recent AI model specs (verifiable) | "Are you confident in your answer? What could be wrong?" |
| Code bug | Buggy Python code review | "Test your code mentally with these inputs: [2, 5, 0, -1]." |

---

## 4. Actual Result

> `[PENDING]`

---

## 5. Decision

> `[PENDING]` Decide whether to include reflection loops in agentic workflows.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
