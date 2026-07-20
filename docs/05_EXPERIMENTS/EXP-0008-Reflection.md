# EXP-0008: Self-Reflection and Error Correction Capability

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0008 |
| **Title** | Self-Reflection and Error Correction |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Agentic Capability |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [EXP-0007](EXP-0007-Planner.md) | Planning capability |
| [EXP-0009](EXP-0009-Critic.md) | Critic capability |
| [benchmark/reasoning/](../../benchmark/tests/reasoning/) | Reasoning benchmark TCs |

---

## 1. Objective

Measure whether Nemotron Ultra 550B can identify and correct its own errors when prompted to reflect on a previous response. This validates the model's suitability for multi-turn agentic workflows where self-correction is required.

---

## 2. Hypothesis

**H1:** When shown its own incorrect answer and asked to reflect, the model corrects the error ≥ 80% of the time with thinking mode ON. [HYPOTHESIS]

**H2:** Reflection quality correlates with thinking mode: thinking ON produces deeper corrections than thinking OFF. [HYPOTHESIS]

**H3:** The model can identify the specific step in its reasoning where the error was introduced. [HYPOTHESIS]

---

## 3. Test Procedure

**Phase 1: Generate initial answer** (deliberately inject difficult questions with known correct answers)

**Phase 2: Inject reflection prompt**
```
Please review your previous answer carefully. 
Identify any errors or weaknesses. 
Provide a corrected and improved response.
```

**Phase 3: Evaluate**
- Did the model identify the error?
- Was the corrected answer better?
- Was the reasoning trace in `<think>` deeper on the second attempt?

---

## 4. Task Set

| Task | Type | Known Correct Answer |
|------|------|---------------------|
| Math logic puzzle | Reasoning | Verifiable |
| Incorrect code review | Code | Known correct code |
| Factual claim verification | Knowledge | Verifiable fact |
| Architecture flaw identification | Design | Expert review |

---

## 5. Actual Results

> **Status: PENDING EXECUTION**

---

## 6. Conclusion

> **PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial experiment design |
