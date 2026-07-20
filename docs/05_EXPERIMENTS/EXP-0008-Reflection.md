# EXP-0008: Reflection Loop Effectiveness

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0008 |
| **Title** | Reflection Loop — Self-Correction and Iterative Quality Improvement |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [EXP-0009 Critic](EXP-0009-Critic.md)
- [EXP-0007 Planner](EXP-0007-Planner.md)
- [EXP-0010 Agent](EXP-0010-Agent.md)
- [benchmark/tests/reasoning/TC-0003.md](../../benchmark/tests/reasoning/TC-0003.md)

---

## 1. Objective

Measure whether a reflection loop (model reviews its own output and revises) improves output quality for Nemotron Ultra 550B. Determine optimal reflection depth (1, 2, or 3 iterations) and evaluate diminishing returns.

---

## 2. Background

**[HYPOTHESIS]** Reflection (asking the model to critique its own response and revise) improves quality by 0.5–1.0 score points at the cost of 2–3x token usage.

**[HYPOTHESIS]** Nemotron Ultra 550B's built-in reasoning (thinking ON) may already perform implicit self-reflection, reducing the marginal benefit of an explicit reflection loop.

---

## 3. Hypotheses

| ID | Hypothesis |
|----|----------|
| H1 | 1 reflection iteration improves score by >= 0.5 points |
| H2 | 2+ iterations show diminishing returns (< 0.2 additional improvement) |
| H3 | Reflection benefit is lower when thinking mode is ON (internal CoT already reflects) |

---

## 4. Reflection Protocol

**Iteration 0 (Baseline):** Generate initial response.

**Iteration 1 (Reflect):**
```
User: Review your previous response. Identify: (1) any incorrect claims, (2) missing important points, (3) logical gaps. Then provide an improved response.
```

**Iteration 2 (Deep Reflect):**
```
User: You have now reviewed your response once. Perform a final quality check: is this response complete, accurate, and actionable? Provide your final answer.
```

---

## 5. Procedure

1. Run TC-reasoning-0001, TC-architecture-0001, TC-coding-0001 with 0, 1, and 2 reflection iterations
2. Score each iteration independently (blind review)
3. Record token count delta per iteration
4. Compare: thinking ON + 0 reflections vs thinking OFF + 1 reflection

---

## 6. Expected Results

| Config | Expected Score | Token Cost |
|--------|---------------|------------|
| No reflection, thinking OFF | 3.0/5 | 1x |
| No reflection, thinking ON | 4.5/5 | 5x |
| 1 reflection, thinking OFF | 3.8/5 | 3x |
| 1 reflection, thinking ON | 4.7/5 | 10x |

---

## 7–13. Actual Result through Benchmark Results

> ⏳ **PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
