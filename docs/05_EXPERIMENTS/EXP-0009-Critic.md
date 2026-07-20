# EXP-0009: Critic Role Capability

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0009 |
| **Title** | Critic Role Capability |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Agentic Capability |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [EXP-0008](EXP-0008-Reflection.md) | Reflection capability |
| [EXP-0010](EXP-0010-Agent.md) | Full agent capability |

---

## 1. Objective

Measure Nemotron Ultra 550B's ability to act as a **critic**: evaluate another agent's output, identify weaknesses, assign structured scores, and provide actionable improvement recommendations.

---

## 2. Background

In multi-agent LLM architectures (Planner → Executor → Critic pattern), the critic role is critical for quality control. [HYPOTHESIS: Nemotron Ultra 550B can effectively fill the critic role in a multi-agent pipeline — needs validation]

Key quality dimensions for a critic model:
- **Accuracy:** Does it correctly identify errors?
- **Calibration:** Is its confidence in its criticism appropriate?
- **Actionability:** Are its suggestions implementable?
- **Non-agreement bias:** Does it avoid sycophancy (agreeing with poor answers)?

---

## 3. Hypothesis

**H1:** With thinking mode ON, the model correctly identifies ≥ 85% of deliberate errors injected into test documents. [HYPOTHESIS]

**H2:** The model exhibits sycophancy (rates incorrect answers as correct) < 15% of the time. [HYPOTHESIS]

**H3:** Using a structured critic system prompt (with explicit scoring rubric) improves criticism quality by >25% vs an unstructured prompt. [HYPOTHESIS]

---

## 4. Critic System Prompt Template

```
/think
You are a rigorous technical critic. Your role is to evaluate the provided answer.

Evaluation framework:
1. Accuracy (0-10): Is the answer factually correct?
2. Completeness (0-10): Does it address all aspects of the question?
3. Clarity (0-10): Is the reasoning clear and well-structured?
4. Actionability (0-10): Are recommendations specific and implementable?

Process:
- Score each dimension independently
- Cite specific evidence for each score
- Identify the top 3 improvements
- Provide a final verdict: PASS (>28/40) or FAIL (≤28/40)

Do NOT be lenient. An incorrect answer that sounds confident is worse than an honest "I don't know."
```

---

## 5. Test Cases

| Input | Deliberate Flaw | Expected Critic Response |
|-------|----------------|-------------------------|
| Code with bug | Runtime error | Identify bug, correct it |
| Architecture doc with security hole | Missing auth | Flag auth gap |
| Business plan with wrong math | ROI calculation error | Catch math error |
| Correct, high-quality answer | None | High score, no major issues |
| Vague, unhelpful answer | No specifics | Low actionability score |

---

## 6. Actual Results

> **Status: PENDING EXECUTION**

---

## 7. Conclusion

> **PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial experiment design |
