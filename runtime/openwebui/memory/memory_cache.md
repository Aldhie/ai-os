# Memory Cache

> **Version**: 1.0.0
> **Spec Ref**: AI-0005-FreeTier-Strategy.md
> **Objective**: Minimize redundant memory lookups within and across sessions

---

## Cache Architecture

```
Session-Level Cache (L1):
  - Scope: Single conversation
  - TTL: Session duration
  - Contents: All loaded memory for this session
  - Size limit: 500 tokens
  - Hit: Do not re-query memory store during session

Process-Level Cache (L2):
  - Scope: Same-day sessions (same user)
  - TTL: 24 hours
  - Contents: T1, T4 items (stable preferences)
  - Hit: Skip memory store lookup for stable items

Cold Storage (L3):
  - Scope: Archived/compressed items
  - TTL: Indefinite (until eviction policy triggers)
  - Access: Explicit lookup only
```

---

## Cache Hit Strategy

| Cache Level | Hit Rate Target | LLM Calls Saved |
|-------------|----------------|------------------|
| L1 (session) | ~100% after first load | High |
| L2 (daily) | ~80% for stable prefs | Moderate |
| L3 (archive) | N/A (on-demand) | None |

---

## Cache Invalidation

| Event | Invalidation Scope |
|-------|-------------------|
| User updates a preference | L1 + L2 for that item |
| User says "forget" | L1 + L2 + L3 for that item |
| Session ends | L1 cleared |
| 24h elapsed | L2 cleared |

---

## RPM Impact

Ref: AI-0005-FreeTier-Strategy.md — 40 RPM, 1,000/day limit

With L1+L2 cache:
- Memory lookup does NOT count as an NIM API call
- Cache hits have zero RPM cost
- Estimated RPM savings: ~10-15% of total session requests
