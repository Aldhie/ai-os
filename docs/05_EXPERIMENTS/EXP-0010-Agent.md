# EXP-0010: Full Agentic Workflow End-to-End

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0010 |
| **Title** | Full Agentic Workflow End-to-End |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Agentic Capability |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) | Model spec — agentic capability |
| [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) | Tool use compatibility |
| [EXP-0007](EXP-0007-Planner.md) | Planner component |
| [EXP-0008](EXP-0008-Reflection.md) | Reflection component |
| [EXP-0009](EXP-0009-Critic.md) | Critic component |
| [benchmark/openwebui/](../../benchmark/tests/openwebui/) | Integration benchmark TCs |

---

## 1. Objective

Validate that Nemotron Ultra 550B can complete a full agentic workflow within Open WebUI:
1. **Plan** a multi-step task using tool calling
2. **Execute** tools (web search, code execution, document retrieval)
3. **Reflect** on results and adjust
4. **Produce** a final synthesized answer

This is the highest-complexity integration test in the benchmark suite.

---

## 2. Background

Nemotron Ultra 550B is described as suitable for "complex agentic workflows". [FACT: Official Doc — NVIDIA Build page]

The Open WebUI + NIM integration has the following known constraints for agentic use:
- Tool calling requires `function_calling.enabled: true` [CONFIRMED: needs to be set]
- `chat_template_kwargs` may be required for tools + reasoning (SGLang backend) [HYPOTHESIS: NEW-01 from AI-0003-Audit]
- Tool call parser is `qwen3_coder` — format compatibility with OW needs validation [HYPOTHESIS: NEW-03]

---

## 3. Hypothesis

**H1:** A full Plan-Execute-Reflect-Synthesize cycle can be completed in ≤ 5 tool calls on a medium-complexity task. [HYPOTHESIS]

**H2:** Tool call format from Cloud NIM is compatible with Open WebUI's tool result injection mechanism. [HYPOTHESIS]

**H3:** Thinking mode ON (`/think`) during planning produces materially better task decomposition than OFF. [HYPOTHESIS]

**H4:** Memory injection during agentic tasks does not cause context overflow for tasks < 30 messages. [HYPOTHESIS]

---

## 4. Test Scenario: Hotel Competitor Analysis

**Goal:** Research and summarize competitor pricing strategy for a boutique hotel.

**Available Tools:**
- Web search (Tavily/DuckDuckGo)
- Document retrieval (RAG from hotel knowledge base)
- Python calculator (for pricing math)

**Expected Agent Flow:**
```
1. Plan: Identify what data is needed
2. Tool call: web_search("boutique hotel pricing strategy 2026")
3. Tool call: knowledge_search("our hotel room rates")
4. Tool call: calculate(competitor_avg - our_rate / our_rate * 100)
5. Synthesize: Produce pricing recommendation
```

**Success Criteria:**
- All 5 steps complete without error
- Tool results correctly incorporated into final answer
- Final answer is actionable and specific
- Total tokens ≤ 16,000

---

## 5. Test Scenario: Code Review + Fix

**Goal:** Review a Python function, identify bugs, fix them, and run tests.

**Available Tools:**
- Code execution sandbox
- Web search for documentation

**Expected Agent Flow:**
```
1. Analyze code with /think
2. Identify bugs
3. Write fixed code
4. Execute code to verify
5. Return passing test result
```

---

## 6. Environment

| Component | Value |
|-----------|-------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Tools enabled | web_search, code_execution, knowledge_search |
| function_calling.enabled | true |
| Pipeline | Deployed with extra_body injection |
| Max agent iterations | 10 |

---

## 7. Actual Results

> **Status: PENDING EXECUTION**
>
> Pre-conditions: EXP-0003 complete + BM-09 benchmark complete (tool call format verified)

---

## 8. Conclusion

> **PENDING**

---

## 9. Decision

> **PENDING** — If agent workflow validates, promote agentic use case to production.
> Will define maximum recommended agent complexity (tool calls, iterations, token budget).

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial experiment design |
