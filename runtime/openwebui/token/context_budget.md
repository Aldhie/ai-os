# Token Context Budget (Operational)

> **Status**: RUNTIME | **Version**: 1.0.0

See `../context/context_budget.md` for the authoritative context budget specification.

This file provides the token-level implementation view.

---

## Token Counting Reference

```yaml
# Approximate token counts for planning

components:
  system_prompt_full:     2500  # full identity + active mode
  system_prompt_minimal:  500   # identity core only
  memory_entry:           150   # per entry, key facts
  rag_chunk_full:         600   # full chunk
  rag_chunk_trimmed:      200   # 3 sentences
  history_turn:           400   # avg per turn
  history_turn_summary:   150   # compressed
  planner_output:         500   # task list
  reflection_output:      400   # assessment
  critic_output:          300   # verdict + reason
  user_message_avg:       200   # average input

# Total standard session (5-turn, standard tier):
# 2500 + 200 (5 mem) + 1800 (3 RAG) + 1600 (4 turns) + 200 msg = ~6300 tokens input
# + 6000 thinking + 1000 output = ~13,300 total tokens per request
```

---

*File: runtime/openwebui/token/context_budget.md | Last updated: 2026-07-20*
