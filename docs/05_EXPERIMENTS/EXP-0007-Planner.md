# EXP-0007: Planner Agent Effectiveness

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0007 |
| **Title** | Planner Agent — Task Decomposition Quality and Multi-Step Execution |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-0001 § Agentic Workflows](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0003 §4 Tool Use Matrix](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [EXP-0003 Thinking](EXP-0003-Thinking.md)
- [EXP-0010 Agent](EXP-0010-Agent.md)
- [benchmark/tests/planning/TC-0001.md](../../benchmark/tests/planning/TC-0001.md)

---

## 1. Objective

Evaluate Nemotron Ultra 550B's ability to decompose complex multi-step tasks into executable plans, and measure plan quality, completeness, and step ordering correctness.

---

## 2. Background

**[FACT]** Nemotron Ultra 550B is described as "Best For: complex agentic workflows" in official NVIDIA model card.

**[HYPOTHESIS]** Thinking ON (`/think`) significantly improves plan quality vs OFF for tasks with >5 steps.

**[HYPOTHESIS]** Structured system prompts specifying output format (numbered steps, prerequisites) improve plan executability.

---

## 3. Hypotheses

| ID | Hypothesis |
|----|----------|
| H1 | Thinking ON improves plan completeness score by >= 1.0 on 5-point scale for complex tasks |
| H2 | Plans generated with tool definitions available are more actionable than without |
| H3 | Explicit "think step by step" user instructions improve planning without thinking mode ON |

---

## 4. Procedure

**Task Set:**
- TC-planning-0001: Plan a Docker-based deployment of Open WebUI with NIM integration
- TC-planning-0002: Plan a RAG pipeline setup from scratch
- TC-planning-0003: Plan a debugging workflow for a failing API integration

**Variables:** thinking mode (ON vs OFF), tool definitions available (yes/no), system prompt structure

**Scoring Criteria:**
- Step completeness: are all necessary steps present?
- Step ordering: are dependencies correctly sequenced?
- Actionability: can a junior engineer execute each step without further research?
- Tool accuracy: are correct tools called in the plan?

---

## 5. Expected Results

| Config | Expected Plan Score |
|--------|--------------------|
| Thinking ON, tools available | 4.5/5 |
| Thinking ON, no tools | 4.0/5 |
| Thinking OFF, tools available | 3.5/5 |
| Thinking OFF, no tools | 3.0/5 |

---

## 6–13. Actual Result through Benchmark Results

> ⏳ **PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
