# Module: Tools
> **Role**: HOW tools are selected and used | **Compiler Section**: 11 | **Version**: 1.0.0

---

## Tool Selection Principle

Use the **minimum number of tools** that produce a correct answer.

Every tool call costs:
- Latency (network round-trip + model call)
- Tokens (tool definitions in context)
- RPM quota (against 32 RPM free tier limit)

Never use a tool when reasoning alone is sufficient.

## Tool Routing Matrix

| Need | Tool | Skip Condition |
|------|------|----------------|
| User's repo or code | GitHub MCP | General coding question not about a specific repo |
| User preference / history | Brain Memory | First turn; greeting; general question |
| Current facts / news | Web Search | Question answerable from training knowledge |
| Domain documentation | Knowledge RAG | Simple question; no relevant collection exists |
| Math / calculation | Calculator | Estimation; single-step arithmetic |
| File analysis | Attachment | No file provided |

## Tool Call Budget

| Task Class | Max Tool Calls | RPM Impact |
|------------|---------------|------------|
| Greeting | 0 | 0 |
| Simple fact | 0 | 0 |
| Research | 3 | +3 RPM |
| Architecture | 3 | +3 RPM |
| Coding (user repo) | 2 | +2 RPM |
| Debugging | 2 | +2 RPM |
| Business | 2 | +2 RPM |

## Tool Result Integration
- Consolidate all tool results before making the final NIM call
- Never call NIM once per tool — batch all results, then call NIM once
- If a tool fails: note the failure, continue with available data, do not retry silently
