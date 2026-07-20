# EXP-0007: Multi-Step Planning Capability

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0007 |
| **Title** | Multi-Step Planning Capability |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Agentic Capability |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) | Model spec — agentic capability section |
| [EXP-0003](EXP-0003-Thinking.md) | Thinking mode validation |
| [benchmark/planning/](../../benchmark/tests/planning/) | Planning benchmark TCs |

---

## 1. Objective

Measure Nemotron Ultra 550B's ability to decompose complex goals into executable step-by-step plans. Validate whether thinking mode (`/think`) produces materially better plans than non-thinking mode.

---

## 2. Hypothesis

**H1:** With thinking mode ON, the model produces plans that are:
- More complete (cover all subtasks)
- More sequentially correct (right dependency order)
- More specific (actionable steps vs vague directions)
compared to thinking mode OFF. [HYPOTHESIS]

**H2:** Providing a planning template in the system prompt increases plan quality by >20% on completeness score. [HYPOTHESIS]

**H3:** The model can correctly identify and flag task dependencies and blockers in a multi-agent scenario. [HYPOTHESIS]

---

## 3. Task Set

| Task | Complexity | Domain |
|------|-----------|--------|
| Build a REST API with auth | Medium | Software Engineering |
| Plan a hotel marketing campaign | Medium | Hospitality |
| Design a RAG pipeline architecture | Hard | AI Engineering |
| Debug a distributed system failure | Hard | Systems Engineering |
| Create a 30-day business launch plan | Hard | Business |

---

## 4. Evaluation Criteria

| Criterion | Weight | Measurement |
|-----------|--------|-------------|
| Completeness | 30% | All major steps present |
| Sequential correctness | 25% | Steps in logical order |
| Actionability | 25% | Steps are executable, not vague |
| Dependency identification | 20% | Blockers and dependencies noted |

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
