# Context Priority Matrix

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Priority Order (Highest to Lowest)

When context budget is constrained, load in this order and stop when budget is reached:

```
Priority 1: System Prompt (identity + active mode)
Priority 2: Current user message
Priority 3: Immediate conversation (last 2 turns)
Priority 4: Retrieved memory (top 3 relevant entries)
Priority 5: Retrieved knowledge / RAG chunks (top 3-5 chunks)
Priority 6: Extended conversation history (turns 3-10, compressed)
Priority 7: Planner output
Priority 8: Reflection output
Priority 9: Critic output
```

---

## Token Budget Allocation

```yaml
total_context_budget: 32000  # conservative for free tier (128K max)

allocation:
  system_prompt: 3000        # fixed
  current_message: 2000      # variable
  immediate_history: 4000    # last 2 turns
  memory: 2000               # top 3 entries
  rag_chunks: 8000           # top 5 chunks
  extended_history: 6000     # compressed older turns
  planner: 2000              # optional
  reflection: 2000           # optional
  critic: 1000               # optional
  response_buffer: 2000      # reserved for answer
```

---

## Conflict Resolution

When two context sources provide contradictory information:

| Scenario | Resolution |
|----------|------------|
| Memory vs. RAG conflict | Prefer RAG (document-grounded) |
| Memory vs. Chat history | Prefer most recent |
| RAG vs. Model knowledge | Prefer RAG (grounded) |
| Explicit user statement vs. memory | Prefer current message (user updates memory) |
| Older memory vs. newer memory | Prefer newer |

---

*File: runtime/openwebui/context/priority_matrix.md | Last updated: 2026-07-20*
