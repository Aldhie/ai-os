# Tool Routing

> **Version**: 1.0.0
> **Module**: Tool Orchestration
> **Spec Ref**: AI-0001-Part2 §6, AI-0005-FreeTier-Strategy.md

---

## Routing Philosophy

Every tool invocation consumes one or more NIM API RPM slots.
On NVIDIA Free Tier (40 RPM / 1,000/day), tool calls compete directly with user responses.
Therefore: **a tool must be justified before it is called.**

---

## Routing Decision Tree

```
User query received
  │
  ├── Can this be answered from model knowledge with ≥95% confidence?
  │     YES → Answer directly. No tool call.
  │     NO  → continue
  │
  ├── Is the information time-sensitive (current prices, live status, today's news)?
  │     YES → web_search tool
  │     NO  → continue
  │
  ├── Does the query reference a specific document?
  │     YES → RAG (knowledge system, not tool call)
  │     NO  → continue
  │
  ├── Does the query require computation or code execution?
  │     YES → code_interpreter tool
  │     NO  → continue
  │
  └── Default: Answer from model knowledge. Flag uncertainty if present.
```

---

## Tool Catalog

| Tool | Trigger | RPM Cost | Notes |
|------|---------|----------|-------|
| `web_search` | Time-sensitive or external data | 1 | Do not use for knowledge in RAG |
| `code_interpreter` | Computation, code execution | 1 | Only for non-trivial computation |
| `file_reader` | User-uploaded file analysis | 0 | Local, no NIM call |
| `calculator` | Simple math | 0 | Use directly; never use LLM for arithmetic |
| `diagram_generator` | Architecture diagrams | 1 | Architecture profile only |

---

## Anti-Patterns

- Calling `web_search` for information clearly in training data
- Calling `code_interpreter` for simple arithmetic (use calculator)
- Chaining tools without necessity
- Re-calling the same tool with the same query
