# Tool Priority

> **Version**: 1.0.0

---

## Priority Order

When multiple tools could serve a request:

| Priority | Tool | Rationale |
|----------|------|----------|
| 1 | `calculator` / local compute | Zero RPM cost |
| 2 | `file_reader` | Local, zero latency |
| 3 | `code_interpreter` | Controlled, verifiable |
| 4 | `web_search` | External, unverifiable, costs RPM |
| 5 | `diagram_generator` | High cost, use only in architecture profile |

---

## Budget Allocation

Ref: `tool_budget.md` for daily limits.

Principle: minimize RPM-costly tools. Use local/cheap tools first.
