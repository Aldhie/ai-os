# EXP-0010: Agentic Workflow End-to-End Test

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0010 |
| **Title** | Agentic Workflow — End-to-End Tool Calling, Planning, RAG, and Memory |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [EXP-0007 Planner](EXP-0007-Planner.md)
- [EXP-0008 Reflection](EXP-0008-Reflection.md)
- [EXP-0009 Critic](EXP-0009-Critic.md)
- [EXP-0005 Memory](EXP-0005-Memory.md)
- [EXP-0006 RAG](EXP-0006-RAG.md)
- [AI-0003 §4 Tool Use Matrix](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [AI-0003-Critical-Findings-Audit NEW-01, NEW-02, NEW-03](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md)
- [benchmark/tests/nim/TC-0001.md](../../benchmark/tests/nim/TC-0001.md)

---

## 1. Objective

Validate the complete agentic workflow: Nemotron Ultra 550B using tools, retrieving from RAG, recalling memory, and generating a multi-step response — all in a single session via Open WebUI.

This is the integration test for all capabilities validated in EXP-0003 through EXP-0009.

---

## 2. Background

**[FACT]** Nemotron Ultra 550B officially supports tool calling. Tool call parser: `qwen3_coder`. (AI-0003-Critical-Findings-Audit)

**[FACT]** `force_nonempty_content: true` is required for coding agents per NVIDIA docs.

**[FACT]** Cloud NIM backend parser is server-side; client does not need to specify parser.

**[BENCHMARK-REQUIRED]** BM-09: Verify `qwen3_coder` output format is compatible with Open WebUI tool call parsing.

**[BENCHMARK-REQUIRED]** BM-10: Verify Cloud NIM context limit (256K vs 1M).

---

## 3. Hypotheses

| ID | Hypothesis |
|----|----------|
| H1 | Tool calling works reliably via Open WebUI with Cloud NIM |
| H2 | RAG + tool calling in same session does not cause context confusion |
| H3 | Memory + RAG injection together stays within 256K context limit for typical sessions |
| H4 | Agentic loop (plan → tool call → observe → respond) completes within 3 API calls on average |

---

## 4. End-to-End Scenario

**Scenario: AI Engineering Assistant**

User asks: *"Based on our repository documentation, what are the highest-priority benchmark tests I should run first? Search for any recent discussions about this and create a prioritized action plan."*

Expected agentic behavior:
1. RAG retrieval from ai-os repo docs (via knowledge base)
2. Memory recall: user preferences for priority ordering
3. Web search tool call (if enabled)
4. Synthesis and plan generation with thinking ON
5. Structured response with numbered action plan

---

## 5. Benchmark Test Cases

| TC | Focus | Success Condition |
|----|-------|------------------|
| BM-09 | Tool call format | OW correctly parses tool_calls from NIM response |
| BM-10 | Context limit | Request with 200K token context succeeds |
| BM-11 | medium_effort Pipeline | Pipeline injection of extra_body works |
| BM-12 | temp=1.0 vs 0.6 | Empirical quality comparison |

---

## 6. Environment Prerequisites

```yaml
requirements:
  - Open WebUI Pipeline for extra_body injection (built)
  - Embedding provider configured (nomic-embed-text or equivalent)
  - Knowledge base indexed with ai-os docs
  - function_calling.enabled: true in capabilities.json
  - At least 5 memory entries seeded for recall test
```

---

## 7–13. Actual Result through Benchmark Results

> ⏳ **PENDING** — All prerequisite experiments (EXP-0003 through EXP-0009) must complete first.

**This is the final integration validation for the entire ai-os engineering stack.**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design — integration test for full agentic stack |
