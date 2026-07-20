# Memory Priority

> **Version**: 1.0.0
> **Spec Ref**: AI-0001-Part2 §4

---

## Priority Ranking

When memory budget is constrained, items are prioritized by:

| Priority | Tier | Type | Weight |
|----------|------|------|--------|
| 1 | T1 | Identity Facts | 100 (always included) |
| 2 | T4 | Behavioral Preferences | 90 |
| 3 | T2 | Domain Expertise | 80 |
| 4 | T3 | Project State (active) | 75 |
| 5 | T3 | Project State (recent) | 60 |
| 6 | T5 | Session Context | 50 |
| 7 | T3 | Project State (old) | 30 |
| 8 | T6 | Transient | 10 |

---

## Priority Boosters

A memory item's priority is boosted when:
- Referenced by the current query (semantic similarity > 0.85): +30
- Was accessed in the last 3 sessions: +20
- Marked as `pinned` by the user: +50 (overrides all)

---

## Conflict Resolution

When two memory items contradict each other:
1. **Most recent wins** — use the timestamp to resolve
2. **Explicit overrides implicit** — direct statement beats inferred preference
3. **Session > Memory** — current session statement always overrides stored memory
4. **Never average** — do not produce a blend of contradictory preferences

Ref: benchmark/tests/memory/TC-0002.md — Memory Update and Contradiction Handling
