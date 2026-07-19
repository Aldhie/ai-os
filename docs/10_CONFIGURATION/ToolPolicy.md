# Tool Policy

| Field | Value |
|---|---|
| **Title** | AI-OS Tool Usage Policy |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines which tools the AI-OS can invoke, when they should be used, and safety guardrails around tool execution. Prevents unnecessary tool calls that consume tokens and API quota.

---

## Scope

- Open WebUI tool integrations
- NVIDIA NIM function calling
- All user sessions

---

## Tool Registry

| Tool | Enabled | Trigger Condition | Risk Level |
|---|---|---|---|
| Web Search | Yes | User asks for current info | Low |
| Calculator | Yes | Math operations requested | Low |
| Code Execution | Restricted | Explicit code run request | Medium |
| File Read | Yes | User provides file | Low |
| File Write | No | Not allowed without review | High |
| Email Send | No | Not allowed | Critical |
| API Calls | Restricted | Explicit request only | High |

---

## Tool Usage Rules

1. **Prefer no tool** — Only call a tool when the task genuinely requires it.
2. **Explain before calling** — Tell the user what tool is being invoked and why.
3. **Validate output** — Tool results must be verified before presenting to user.
4. **Token awareness** — Tool output counts toward context. Summarize long results.
5. **Error handling** — If a tool fails, report clearly and offer alternatives.
6. **No chained destructive tools** — Never chain file-write, API-call, or delete tools.

---

## Tool Invocation Template

When deciding to call a tool, the AI should reason:

```text
Thought: The user asked for X. To answer accurately, I need Y.
Tool: [tool_name]
Input: {"query": "..."}
Reason: Without this tool, I cannot provide accurate current information.
```

---

## Configuration File

See: `configs/openwebui/filters.json`

---

## Dependencies

- `configs/openwebui/capabilities.json`
- `configs/openwebui/filters.json`
- [AI-0005-FreeTier-Strategy.md](../00_ENGINEERING/AI-0005-FreeTier-Strategy.md)

---

## References

- [Open WebUI Tools Docs](https://docs.openwebui.com/features/plugin/tools)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

---

## TODO

- [ ] Implement web search tool in Open WebUI
- [ ] Configure tool call schema for Nemotron Ultra
- [ ] Test tool calling with `capabilities.json` flags
- [ ] Define tool result summarization rules
- [ ] Add tool audit logging
