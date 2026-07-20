# Tool Budget Specification

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Tool Usage Policy

Each tool call MAY require a NIM API round-trip. Tool usage must be budgeted against the RPM limit.

---

## Tool Budget Matrix

| Task Class | Max Tool Calls | Tools Allowed |
|------------|---------------|---------------|
| Greeting | 0 | None |
| Simple fact | 0 | None |
| Research | 3 | search, knowledge, memory |
| Architecture | 4 | knowledge, memory, code_runner, planner |
| Coding | 3 | knowledge, code_runner, memory |
| Debugging | 3 | code_runner, knowledge, memory |
| Business | 2 | memory, knowledge |
| Planning | 3 | memory, planner, knowledge |

---

## Tool Call Efficiency Rules

1. **Batch tool results**: If 3 tools are called, consolidate all results before the NEXT NIM call
2. **Avoid tool chains > 3**: Tool A → Tool B → Tool C → NIM → Tool D is usually wrong
3. **Cache tool results**: If same tool called with same params, use cache (Redis, 5min TTL)
4. **Skip tool if budget exhausted**: Degrade gracefully; note the limitation in response

---

## Free Tier Tool Budget Impact

```
Each tool chain call = 1 additional NIM request
A response with 3 tool calls = up to 4 NIM requests total (3 tool + 1 final)

At 15 conversations/day, 7.5 turns, avg 2 tool calls per complex turn:
  15 × 7.5 × 1 (base) = 112 requests
  + 5 complex turns × 2 tool calls = +10 requests
  Total: ~122 requests/day ← SAFE (< 1000 limit)
```

---

*File: runtime/openwebui/performance/tool_budget.md | Last updated: 2026-07-20*
