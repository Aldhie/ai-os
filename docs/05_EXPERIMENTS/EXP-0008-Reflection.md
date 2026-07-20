# EXP-0008: Reflection and Self-Correction Behavior

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0008 |
| **Title** | Reflection — Model Self-Correction Quality Under Explicit Critique |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related REQ** | REQ-AI-0009 (reflection agent) |
| **Cross-References** | [EXP-0009](EXP-0009-Critic.md) · [EXP-0003](EXP-0003-Thinking.md) |

---

## 1. Objective

Evaluate Nemotron Ultra 550B's ability to reflect on its own output and self-correct when given:
1. Explicit critique
2. Contradictory evidence
3. A request to "think again"

Determines whether a reflection agent pattern is viable for this model.

---

## 2. Hypothesis

> **H1:** Nemotron Ultra 550B will improve response quality by ≥1 point when given explicit critique in reasoning ON mode.
>
> **H2:** Self-correction will be more substantive (not just superficial rewording) in reasoning ON vs. OFF mode.
>
> **H3:** Model will not hallucinate confidence — it will acknowledge errors when evidence contradicts its initial response.

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | Critique type | None, Vague critique, Specific critique, Contradictory evidence |
| **Independent** | Reasoning mode | OFF, ON |
| **Dependent** | Quality improvement (delta score) | Score after reflection - Score before |
| **Dependent** | Substantive change (vs. superficial) | Binary |
| **Dependent** | Hallucination resistance | Binary |

---

## 4. Procedure

1. Get initial response to a factual or reasoning question
2. Provide critique: "That's incorrect. Reconsider your answer."
3. Provide specific critique: "Step 3 of your plan is wrong because X."
4. Provide contradictory evidence: "According to [source], the answer is Y."
5. Score each reflection response vs. initial
6. Determine if changes are substantive (logic changed) or superficial (rewording)

---

## 5. Expected Result

- Vague critique: minimal improvement (~+0.3 points)
- Specific critique: meaningful improvement (~+1.5 points)
- Contradictory evidence: model should defer to evidence (+1.0 to +2.0)
- Reasoning ON: better quality improvement than reasoning OFF (+0.5 delta)

---

## 6–12. Actual Result through Benchmark Table

> **STATUS: PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
