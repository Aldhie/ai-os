# EXP-0010: Full Agentic Workflow

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0010 |
| **Title** | End-to-End Agentic Workflow — Plan → Execute → Reflect → Deliver |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related BM** | BM-01, BM-02, BM-03, BM-09 |
| **Related REQ** | REQ-AI-0011 (agentic workflow) |
| **Depends On** | EXP-0007 (Planner), EXP-0008 (Reflection), EXP-0009 (Critic), BM-09 (tool call format) |
| **Cross-References** | [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) · [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) |

---

## 1. Objective

Validate a complete agentic workflow using Nemotron Ultra 550B as the backbone:

```
User Request
    ↓
[Planner Agent] — decomposes task into steps
    ↓
[Executor] — executes steps using tools (web search, code, RAG)
    ↓
[Critic Agent] — reviews output quality
    ↓
[Reflector] — revises if critic finds issues
    ↓
Final Delivery to User
```

**Engineering Question:** Is Nemotron Ultra 550B capable of sustained multi-step agentic execution without tool call failures, context overflow, or reasoning collapse?

---

## 2. Hypothesis

> **H1:** A 5-step agentic workflow will complete successfully with ≥80% task accuracy on technical tasks.
>
> **H2:** Tool calling will work reliably for web search and code execution with the `qwen3_coder` parser via Cloud NIM.
>
> **H3:** Context overflow will be the primary failure mode for tasks requiring >10 tool calls due to accumulating message history.
>
> **H4:** Critic-reflection loop will add 20–40% quality improvement on the final output vs. single-pass execution.

---

## 3. Test Scenarios

1. **Research + Summarize:** Search web for topic → summarize → critique → refine
2. **Code + Debug:** Write code → analyze for bugs → fix → verify
3. **Plan + Execute:** Break down task → execute each step with tools → verify completeness
4. **RAG + Analyze:** Retrieve docs → analyze → critic checks accuracy → deliver

---

## 4. Prerequisites

- [ ] BM-09 complete (tool call format verified)
- [ ] EXP-0007 complete (planner validated)
- [ ] EXP-0009 complete (critic validated)
- [ ] Embedding provider configured (EDR-0005)
- [ ] Open WebUI Pipeline deployed for `extra_body` injection

---

## 5. Procedure

1. Build workflow in Open WebUI using Pipelines or Agents feature
2. Configure Planner, Executor, Critic as separate model profiles
3. Run each test scenario 3 times
4. Score end-to-end task completion quality
5. Log token consumption and latency per phase
6. Document failure modes and recovery behavior

---

## 6. Expected Result

| Scenario | Expected Quality | Expected Tokens | Expected Latency |
|----------|-----------------|----------------|------------------|
| Research | 7.5/10 | ~8,000 total | 45–90s |
| Code+Debug | 8.0/10 | ~12,000 total | 60–120s |
| Plan+Execute | 7.0/10 | ~10,000 total | 60–120s |
| RAG+Analyze | 8.5/10 | ~6,000 total | 30–60s |

---

## 7–12. Actual Result through Benchmark Table

> **STATUS: PENDING** — Blocked on BM-09 and all prerequisite experiments.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design; prerequisites documented |
