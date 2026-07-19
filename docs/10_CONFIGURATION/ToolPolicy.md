# Tool Policy

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | ToolPolicy.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the tool use policy for the AI OS. It specifies which tools are available, when they should be used, usage guidelines, and error handling.

---

## Scope

- Available tools catalog
- Tool invocation policy
- Error handling and fallback
- Tool security considerations

---

## Dependencies

- `docs/10_CONFIGURATION/SystemPrompt.md` — tool instructions in system prompt
- `configs/openwebui/capabilities.json` — enabled capabilities

---

## References

- [Open WebUI Tools Documentation](https://docs.openwebui.com/features/tools/)
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)

---

## Available Tools

| Tool | Category | Status | Description |
|------|----------|--------|-------------|
| Web Search | Information | Active | Search the web for current information |
| Code Execution | Computation | Active | Execute Python code in sandbox |
| RAG / Knowledge | Knowledge | Active | Query the knowledge base |
| Memory Read | Memory | Active | Read stored memories |
| Memory Write | Memory | Active | Write new memories |
| Calculator | Utility | Active | Perform calculations |
| Date/Time | Utility | Active | Get current date and time |

---

## Tool Invocation Policy

### When to Use Tools

- **Use web search** for real-time information, current events, facts that may have changed
- **Use code execution** for calculations, data analysis, visualizations
- **Use RAG** when the question relates to documents in the knowledge base
- **Use memory** to recall or store user-specific information

### When NOT to Use Tools

- Do not call tools unnecessarily for questions answerable from training knowledge
- Do not chain multiple tool calls without user awareness
- Do not use tools to bypass safety constraints

---

## Tool Error Handling

| Error Type | Response |
|------------|----------|
| Tool unavailable | Inform user, proceed without tool |
| Tool timeout | Retry once, then inform user |
| Tool error | Explain error, offer alternative |
| Permission denied | Inform user of access limitation |

---

## TODO

- [ ] Define tool authorization levels (which tools require user confirmation)
- [ ] Document tool schemas for each available tool
- [ ] Test tool invocation with Nemotron 550B via NIM
- [ ] Define tool usage rate limits
- [ ] Add MCP (Model Context Protocol) tool support evaluation
