# EXP-0010: Agentic Capability — Tool Calling and Multi-Turn Agent Loops

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0010 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0005 |
| **BM** | BM-01, BM-02, BM-03, BM-09 |

## Related Documents

- ↑ [REQ-AI-0005](../00_ENGINEERING/REQ-INDEX.md#req-ai-0005)
- ↑ [AI-0003 Compatibility Matrix](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- → [EXP-0007 Planner](./EXP-0007-Planner.md)
- → [EXP-0009 Critic](./EXP-0009-Critic.md)

---

## Objective

Validate the full agentic capability of Nemotron Ultra 550B through Open WebUI: tool discovery, tool call generation in correct format, result consumption, and multi-turn agent loops. Identify any format incompatibilities between qwen3_coder tool format and OW expectations.

---

## Hypothesis

**H1:** The model generates syntactically correct tool call JSON compatible with OW's tool calling pipeline in a standard single-tool scenario.

**H2:** Parallel tool calls (multiple tools in one response) work correctly with OW's tool calling pipeline.

**H3:** If Cloud NIM uses SGLang backend, tool calls + thinking ON simultaneously requires extra Pipeline configuration (chat_template_kwargs injection).

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| Tool count | Independent | 1 tool, 2 tools (parallel) |
| Thinking mode | Independent | OFF, ON |
| Backend | Observed | vLLM, SGLang (whichever Cloud NIM uses) |
| Tool type | Independent | Simple function, RAG retrieval, Web search |

---

## Procedure

1. **BM-09 (Format test):**
   - Define 1 simple tool (get_weather with location parameter).
   - Send request that requires the tool.
   - Observe tool_call JSON format in OW response.
   - Verify OW correctly parses and routes to tool executor.

2. **BM-01 (Parallel tool calls):**
   - Define 2 tools simultaneously.
   - Ask question requiring both tools.
   - Verify both tool_calls present in single response.

3. **Multi-turn loop:**
   - Tool call → provide result → model continues → observe next action.
   - Verify model correctly uses tool result in continued reasoning.

4. **BM-02 (Agentic RAG):**
   - Enable RAG collection.
   - Ask question requiring both knowledge retrieval and tool call.
   - Verify both work in single conversation turn.

---

## Expected Result

| Test | Expected |
|------|----------|
| BM-09 | Tool call in qwen3_coder format, OW parses correctly |
| BM-01 | Two parallel tool_calls in response |
| Multi-turn | Model uses tool result, produces final answer |
| BM-02 | RAG context + tool call both work |

---

## Actual Result

*Status: Not yet executed.*

| Test | Result | Format OK | OW Compatible |
|------|--------|-----------|---------------|
| BM-09 | TBD | TBD | TBD |
| BM-01 | TBD | TBD | TBD |
| BM-02 | TBD | TBD | TBD |

---

## Analysis

*Pending execution. Key risk: SGLang backend incompatibility requiring Pipeline workaround.*

---

## Conclusion

*Pending execution.*

---

## Decision

*Current: function_calling enabled per capabilities.json. BM-09 will determine if Pipeline workaround needed.*

---

## Future Work

- If BM-09 fails: implement OW Pipeline for tool call format normalization.
- Extend to MCP tool server (BM-03) after basic tool calling validated.
- Design autonomous agent loop: plan → tool → reflect → plan → ...

---

## Benchmark Result

*Pending BM-01, BM-02, BM-03, BM-09 execution.*

---

*EXP-0010 v1.0.0 — Created 2026-07-20*
