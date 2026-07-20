# EXP-0010: End-to-End Agentic Workflow

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0010 |
| **Title** | End-to-End Agentic Workflow: Planner + RAG + Tool Calls + Reflection |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | Critical |

---

## Cross References

- [EXP-0007 — Planner](EXP-0007-Planner.md)
- [EXP-0006 — RAG](EXP-0006-RAG.md)
- [EXP-0008 — Reflection](EXP-0008-Reflection.md)
- [EXP-0009 — Critic](EXP-0009-Critic.md)
- [AI-0003 — Compatibility, Section 4](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [AI-0003-Audit — NEW-01, NEW-02, NEW-03](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md)

---

## 1. Objective

Validate a complete agentic workflow using Nemotron Ultra 550B via Open WebUI:
1. User provides a complex multi-step task
2. Planner decomposes into subtasks
3. Each subtask may require: RAG retrieval, tool calls (web search, calculator), or model reasoning
4. Reflection step reviews the assembled answer
5. Final output delivered to user

This is the integration test of EXP-0003 through EXP-0009.

---

## 2. Hypothesis

> `[HYPOTHESIS]` The end-to-end pipeline with `/think` enabled and proper `chat_template_kwargs` injection (NEW-01) will complete complex agentic tasks with >75% quality score. The most common failure mode will be tool call parsing (NEW-03, BM-09).

---

## 3. Task Scenarios

| Scenario | Components Required |
|----------|--------------------|
| Hotel guest complaint resolution | RAG (policy docs) + reasoning + structured output |
| Docker deployment plan generation | Planning + code generation + reflection |
| Competitive analysis with web search | Web search tool + reasoning + synthesis |
| Multi-document summarization | RAG (multiple docs) + long-context synthesis |

---

## 4. Pre-conditions

This experiment requires:
- [ ] EXP-0003 complete (thinking mode policy set)
- [ ] EXP-0006 complete (RAG pipeline validated)
- [ ] BM-09 complete (tool call format verified)
- [ ] Pipeline for `extra_body` injection deployed

---

## 5. Actual Result

> `[PENDING — blocked on pre-conditions]`

---

## 6. Decision

> `[PENDING]` Gate production deployment on this experiment achieving >75% quality score.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design — integration test of EXP-0003 through EXP-0009 |
