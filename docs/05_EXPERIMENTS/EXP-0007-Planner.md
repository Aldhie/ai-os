# EXP-0007: Agentic Planner Quality

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0007 |
| **Title** | Agentic Planner: Task Decomposition and Plan Execution Quality |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | High |

---

## Cross References

- [AI-0001 — Nemotron Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0003 — Compatibility, Section 4](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [EXP-0003 — Thinking Mode](EXP-0003-Thinking.md)
- [TC-PLAN-0001](../../benchmark/tests/planning/TC-PLAN-0001.md)

---

## 1. Objective

Measure Nemotron Ultra 550B performance as a planner agent: ability to decompose complex tasks into executable subtasks, sequence them correctly, and produce a structured plan.

---

## 2. Hypothesis

> `[HYPOTHESIS]` With `/think` enabled, Nemotron Ultra 550B produces higher-quality plans (more comprehensive, correctly sequenced) than with `/nothink`. Full thinking mode is necessary for plans with >5 steps.

---

## 3. Variables

### Task Types

| Task | Complexity |
|------|------------|
| Plan a hotel room inventory audit | Medium (5–8 steps) |
| Plan deployment of Open WebUI to production Docker | High (10+ steps) |
| Plan a multi-agent RAG system architecture | Expert (>15 steps) |

### Thinking Modes Tested

- OFF (`/nothink`)
- ON (`/think`)
- medium_effort

---

## 4. Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| All necessary steps present | 40% |
| Steps in correct order | 30% |
| Steps are actionable (not vague) | 20% |
| Edge cases and failure modes addressed | 10% |

---

## 5. Actual Result

> `[PENDING]`

---

## 6. Decision

> `[PENDING]` Define planner agent system prompt and thinking mode based on results.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
