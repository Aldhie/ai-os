# EXP-0009: Critic Role — External Evaluation and Quality Judgment

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0009 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0004, REQ-AI-0008 |

## Related Documents

- ↑ [REQ-AI-0004](../00_ENGINEERING/REQ-INDEX.md#req-ai-0004)
- → [EXP-0008 Reflection](./EXP-0008-Reflection.md)
- → [EXP-0010 Agent](./EXP-0010-Agent.md)

---

## Objective

Evaluate the model's ability to act as an external critic — judging the quality of text, code, or plans produced by itself or another agent. Determine if system-prompt role assignment as "Critic" produces reliably critical (rather than sycophantic) evaluation.

---

## Hypothesis

**H1:** Without explicit critic role in system prompt, the model defaults to sycophantic evaluation ("Great work! Minor suggestion...").

**H2:** With critic role in system prompt, the model produces substantively critical evaluations identifying real weaknesses.

**H3:** Thinking ON reduces sycophancy by allowing the model to reason through quality criteria before responding.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| System prompt role | Independent | No role, Evaluator, Strict critic |
| Thinking mode | Independent | OFF, ON |
| Input quality | Independent | Poor, Average, Excellent |
| Domain | Controlled | Code review, Essay evaluation |

---

## Procedure

1. Create 6 inputs: 2 poor, 2 average, 2 excellent (code and text).
2. Ask model to evaluate each under 3 system prompt conditions.
3. Measure: (a) sycophancy rate (positive tone on poor inputs), (b) false negative rate (calling poor input excellent), (c) specific feedback quality (actionable vs generic), (d) score calibration.
4. Compare thinking ON vs OFF.

---

## Expected Result

| System Prompt | Sycophancy (poor input) | False Negative | Feedback Quality |
|---------------|------------------------|----------------|------------------|
| No role | High | High | Generic |
| Evaluator | Medium | Medium | Moderate |
| Strict critic + think ON | Low | Low | Specific |

---

## Actual Result

*Status: Not yet executed.*

---

## Benchmark Result

*Pending execution.*

---

*EXP-0009 v1.0.0 — Created 2026-07-20*
