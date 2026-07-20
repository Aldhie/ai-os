# EXP-0009: Critic Agent Effectiveness

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0009 |
| **Title** | Critic Agent — External Evaluation Quality and Calibration |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [EXP-0008 Reflection](EXP-0008-Reflection.md)
- [EXP-0010 Agent](EXP-0010-Agent.md)
- [AI-9003 Prompt Engineering Standard](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md)
- [benchmark/tests/reasoning/](../../benchmark/tests/reasoning/)

---

## 1. Objective

Evaluate whether using Nemotron Ultra 550B as its own critic (evaluating and scoring a second response) produces reliable quality assessments. Measure critic calibration against human scores.

---

## 2. Background

**[HYPOTHESIS]** A separate critic instance (same model, different system prompt) can reliably score responses on a 1–5 scale with < 0.5 deviation from human ground truth.

**[HYPOTHESIS]** Using thinking ON for the critic improves score calibration vs thinking OFF.

---

## 3. Critic System Prompt Design

```
# Role
You are a strict quality evaluator for AI-generated responses.

# Task
You will receive: (1) an original question, (2) an AI-generated response.
Evaluate the response on a 1-5 scale per criterion:
- Correctness: Is every factual claim accurate?
- Completeness: Are all required elements present?
- Clarity: Is the response easy to understand?
- Actionability: Can the reader immediately act on this information?
- Conciseness: Is the response appropriately brief (no padding)?

# Output Format
Return ONLY a JSON object:
{"correctness": N, "completeness": N, "clarity": N, "actionability": N, "conciseness": N, "overall": N, "critical_issues": ["..."]}

/think
```

---

## 4. Hypotheses

| ID | Hypothesis |
|----|----------|
| H1 | Critic score correlates with human score (r > 0.8) on factual tasks |
| H2 | Critic overestimates scores when evaluating same-model output (self-leniency bias) |
| H3 | Thinking ON critic is more calibrated than thinking OFF |
| H4 | Critic identifies factual errors with > 70% precision |

---

## 5. Procedure

1. Generate 30 responses to TC benchmark questions (varied quality intentionally)
2. Human annotators score each response independently (ground truth)
3. Run critic agent on same 30 responses
4. Compute: Pearson correlation, mean absolute error, precision on error detection
5. Compare: critic with thinking ON vs OFF

---

## 6. Expected Results

| Metric | Expected Value |
|--------|---------------|
| Human-critic correlation | r > 0.75 |
| Mean absolute error | < 0.6 points |
| Error detection precision | > 65% |
| Self-leniency bias | +0.3–0.5 score inflation |

---

## 7–13. Actual Result through Benchmark Results

> ⏳ **PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
