# Tool Policy

| Field | Value |
|-------|-------|
| **Title** | Tool Usage Policy |
| **Purpose** | Define which tools the AI OS uses, when to use them, and safety constraints |
| **Scope** | Tool inventory, invocation rules, error handling, safety limits |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | SystemPrompt.md, AI-0002 |
| **References** | Open WebUI Tools Documentation |

---

## 1. Tool Inventory

| Tool | Purpose | When to Use | Safety Level |
|------|---------|------------|-------------|
| `web_search` | Search the internet | Time-sensitive or fact-checking queries | Low |
| `code_execution` | Run Python code | Calculations, data analysis | Medium |
| `memory_read` | Read long-term memory | Session start, ambiguous context | Low |
| `memory_write` | Write to memory | New persistent information detected | Low |
| `file_read` | Read user files | User requests document analysis | Low |
| `calendar` | Read/write calendar | Scheduling and time-related tasks | Medium |

---

## 2. Tool Invocation Rules

### ALWAYS use a tool when:

- User asks about current events (use `web_search`)
- User asks for calculations involving large datasets (use `code_execution`)
- User references past context not in conversation (use `memory_read`)

### NEVER use a tool when:

- Answer is definitively known from model knowledge
- Tool usage would reveal sensitive information
- Cost (tokens, latency) exceeds benefit

### ASK BEFORE using a tool when:

- Tool would make external API calls with user data
- Tool would write or modify persistent data

---

## 3. Tool Error Handling

| Error Type | Action |
|------------|--------|
| Tool not available | Acknowledge and answer from knowledge |
| Tool timeout | Retry once, then acknowledge failure |
| Tool returns empty result | Acknowledge and offer alternative |
| Tool returns error | Log, acknowledge, do not retry infinitely |

---

## TODO

- [ ] Finalize tool list based on Open WebUI capabilities
- [ ] Test each tool with edge cases
- [ ] Define token cost estimates per tool call
- [ ] Implement tool usage logging
- [ ] Review safety boundaries for code execution
