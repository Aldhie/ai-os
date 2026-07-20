# Memory Eviction

> **Version**: 1.0.0
> **Spec Ref**: AI-0005-FreeTier-Strategy.md

---

## Eviction Triggers

| Trigger | Action |
|---------|---------|
| Total memory > 50,000 tokens | Evict lowest-priority items until < 40,000 |
| T6 item age > 24h | Auto-evict |
| T5 session ends | Evict T5 unless user explicitly saves |
| T3 project inactive > 90 days | Compress then evict if > 180 days |
| User explicitly says "forget this" | Immediate eviction |

---

## Eviction Order

1. T6 Transient (expire first)
2. T5 Session (on session end)
3. T3 Old projects (>90 days, inactive)
4. T3 Recent projects (>30 days, low access)
5. T2 Domain (only if critically over budget)
6. T4 Behavioral (never auto-evict; user must confirm)
7. T1 Identity (never auto-evict)

---

## Safe Eviction Rules

- Never evict T1 or T4 automatically
- Always compress before evicting T3
- Log all evictions to `memory_audit_log`
- Notify user at next session start if significant memory was evicted

---

## Recovery

If a user references evicted content:
1. Inform the user that the memory was archived
2. Offer to restore from archive if available
3. If not available, ask the user to re-state
