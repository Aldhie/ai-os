# Memory Orchestration
> **Role**: Complete runtime memory behaviour | **Version**: 1.0.0

---

## Why Memory Orchestration Exists

Memory without a policy is noise. Loading all memories every request wastes tokens and introduces irrelevant context. Loading no memory loses personalization. The orchestration layer decides — per request — exactly which memories load, when they expire, and how conflicts resolve.

---

## Loading Decision

```
Load memory IF:
  ✔ Request references user preferences, history, or ongoing project
  ✔ Task class is: explanation, business, architecture, coding, debugging, research, planning
  ✔ Conversation turn > 1 AND topic suggests personalization benefit

Skip memory IF:
  ✗ Greeting or acknowledgment
  ✗ Simple factual question ("What is REST?")
  ✗ First turn of a new session with no established context
  ✗ User explicitly says "forget previous context" or starts fresh
```

## Retrieval Parameters

```yaml
top_k:          5          # max entries retrieved per request
min_score:      0.70       # semantic similarity threshold
max_tokens:     2000       # total memory budget in context
per_entry_max:  150        # tokens per entry after key-facts extraction
cache_ttl:      300s       # 5-minute cache per user + query hash
```

---

## Compression Policy

When memory budget exceeds 2,000 tokens:
1. Drop entries with score < 0.80 first
2. For remaining entries: extract title + key facts only (drop narrative)
3. Target: ≤ 100 tokens per entry after compression
4. Never compress the most recent 2 entries

---

## Summarization Policy

Memory summarization triggers when a session ends and > 5 significant facts were established:

```
Summary format:
  [Session {date}]
  Context: {one sentence about what was discussed}
  Decisions made:
    - {decision 1}
    - {decision 2}
  Preferences established:
    - {preference}
  Active projects:
    - {project name}: {current state}
```

Summaries are stored as memory entries with type `session_summary`.

---

## Cache Policy

| Cache Layer | TTL | Key | Invalidation |
|------------|-----|-----|-------------|
| L1 in-process | 60s | user_id + query_hash | New memory write |
| L2 Redis | 300s | user_id + query_hash | New memory write |
| Session context | Session end | user_id | Always |

---

## Priority Policy

When multiple memories are relevant, rank by:
1. Recency (most recent = highest score: 1.0 → decays by 0.1 per week)
2. Semantic similarity to current query (weight: 0.40)
3. Type priority: `decision` > `preference` > `fact` > `session_summary`
4. Explicit user confirmation (boosted +0.3)

---

## Conversation Persistence

- Within a session: conversation history is the primary context source (memory supplements it)
- Across sessions: memory is the primary context source for continuity
- At session start: load top-3 memories to re-establish context silently
- Do NOT load full previous conversation — use session summary instead

---

## Memory Expiration

```yaml
default_ttl:        forever    # memories persist until explicit expiration or deletion
project_memory:     90 days    # project-specific context expires after 90 days of inactivity
preference:         forever    # user preferences never expire unless updated
fact:               365 days
session_summary:    365 days
credential:         never_stored
```

---

## Conflict Resolution

| Scenario | Resolution |
|----------|------------|
| Two memories contradict each other | Use more recent; flag conflict to user |
| Memory contradicts current user statement | Current statement wins; offer to update memory |
| Memory contradicts RAG knowledge | RAG wins for factual claims; memory wins for preferences |
| Memory score tie | Prefer the entry with type `decision` or `preference` |

---

## Memory Confidence

Each memory entry has a confidence score:
```yaml
high:    0.90+   # user explicitly confirmed this
medium:  0.70-0.89  # inferred from conversation; not explicitly confirmed
low:     0.50-0.69  # weak signal; do not use without user confirmation
```

Entries with confidence < 0.70 are loaded only when no higher-confidence entries exist for the query.

---

## Long Conversation Design

For conversations > 10 turns:
1. Compress turns 1–77 into a session summary block (≤ 400 tokens)
2. Write the summary to memory with type `session_summary`
3. Keep turns 8-10 verbatim in context
4. At turn 20: compress turns 8-15 into a second summary block
5. This prevents context bloat in very long conversations

---

## Token Budgeting

```
Total context: 32,000 tokens (deep tier)
Memory allocation: 2,000 tokens
  - 5 entries × 150 tokens avg = 750 tokens typical
  - Compressed session summary: 400 tokens
  - Total realistic memory usage: ~1,150 tokens
  - Buffer for retrieval variance: ~850 tokens
```

---

*File: runtime/openwebui/memory/orchestration.md | Last updated: 2026-07-21*
