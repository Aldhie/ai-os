# Memory Compression

> **Version**: 1.0.0
> **Spec Ref**: AI-0005-FreeTier-Strategy.md

---

## When to Compress

Compression is triggered when:
- A memory namespace exceeds 10,000 tokens total
- A single project's T3 memory exceeds 2,000 tokens
- Memory age > 30 days AND no recent access

---

## Compression Strategy

### Level 1 — Deduplication
Remove duplicate or near-duplicate entries (semantic similarity > 0.95).
Cost: 0 LLM calls.

### Level 2 — Summarization
For T3 (Project State) items older than 7 days:
- Group by project
- Summarize into a single "Project Snapshot" entry
- Discard individual entries
Cost: 1 LLM call per project (use Mode 0, no thinking).

### Level 3 — Archive
For T5/T6 items older than 24 hours:
- Move to cold storage
- Do not load unless explicitly requested
Cost: 0 LLM calls.

---

## Token Budget for Compression

Compression operations must stay within the free tier budget:
- Max 5 compression calls per day
- Schedule during low-usage periods (e.g., midnight)
- Never trigger compression during active session

---

## Compression Output Format

```json
{
  "type": "project_snapshot",
  "project": "ai-os",
  "snapshot_date": "2026-07-20",
  "summary": "Sprint 1.0 in progress. Runtime directory structure created. Model policies complete. Next: profiles, memory, knowledge, tools.",
  "compressed_from": 12,
  "token_count": 85,
  "original_token_count": 1840
}
```
