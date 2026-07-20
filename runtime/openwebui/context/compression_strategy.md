# Context Compression Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## When Compression is Triggered

Compression triggers when accumulated context exceeds the budget defined in `context_budget.md`.

Compression order (compress lower priority first):
```
1. Extended history (turns > 5) → summarize to 200 tokens per 3 turns
2. RAG chunks → reduce from top-5 to top-3
3. Memory entries → reduce from top-5 to top-3
4. Reflection output → truncate to first 500 tokens
5. Planner output → truncate to task list only
```

Never compress:
```
- System prompt
- Current user message
- Immediate last 2 turns (verbatim)
```

---

## Compression Techniques

### History Compression

For turns older than 3, convert to:
```
[Turn N summary]: User asked about X. AI provided Y. Key facts: Z.
```
Target: 100-200 tokens per old turn (from typical 500-1500 tokens).

### RAG Chunk Compression

Trim each chunk to the 3 most relevant sentences based on semantic proximity to the current query.

### Memory Compression

Exclude memories with relevance score < 0.7.
For included memories, retain: title + key facts only (drop full narrative).

---

## Compression Quality Guarantee

After compression:
- The factual content of the answer must not change
- The key user preference context must be preserved
- The most recent 2 turns must be verbatim

---

*File: runtime/openwebui/context/compression_strategy.md | Last updated: 2026-07-20*
