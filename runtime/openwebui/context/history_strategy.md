# Chat History Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## History Loading Rules

```yaml
default_turns_loaded: 5
max_turns_verbatim: 3       # last 3 turns always verbatim
max_turns_compressed: 7     # turns 4-10 compressed
max_turns_total: 10         # beyond 10: summarize entire history to 500 tokens
```

---

## History Relevance Scoring

Not all history is equally relevant. Score each turn:

| Factor | Weight |
|--------|--------|
| Recency (most recent = 1.0) | 40% |
| Semantic similarity to current query | 40% |
| Contains user preference update | +0.3 bonus |
| Contains key decision or fact | +0.2 bonus |

Load turns above score threshold 0.5, up to budget.

---

## When to Skip History

```
- Greeting messages (no history needed)
- Simple isolated facts
- User explicitly starts with "Mulai baru:" or "New topic:"
- Topic shift detected (semantic distance > 0.8 from last 3 turns)
```

---

## Long Conversation Handling

When conversation exceeds 10 turns:
1. Summarize turns 1-7 into a "Conversation Summary" block (max 500 tokens)
2. Keep turns 8-10 verbatim
3. Keep current message
4. The summary replaces the individual old turns in context

---

*File: runtime/openwebui/context/history_strategy.md | Last updated: 2026-07-20*
