# Memory Policy v1

> **Version**: 1.0.0
> **Module**: Memory Orchestration
> **Spec Ref**: AI-0001-Part2 §4 (Memory Design), AI-0005-FreeTier-Strategy.md
> **Experiment Ref**: EXP-0005-Memory.md
> **Benchmark Ref**: benchmark/tests/memory/

---

## Purpose

Memory is the mechanism that transforms a stateless model into a personalized cognitive runtime. This policy defines when, what, and how memory is loaded, prioritized, compressed, and evicted.

---

## Memory Taxonomy

| Tier | Type | Examples | Persistence |
|------|------|---------|-------------|
| T1 | Identity Facts | Name, role, language preference | Permanent |
| T2 | Domain Expertise | Tech stack, industry, skill level | Long-term |
| T3 | Project State | Active projects, sprint status | Medium-term |
| T4 | Behavioral Preferences | Response style, verbosity, format | Long-term |
| T5 | Session Context | Current task, recent decisions | Session-only |
| T6 | Transient | One-off requests, immediate context | Ephemeral |

---

## Load Triggers

Memory SHOULD load when:
- New session starts (always load T1, T2, T4)
- User references a project by name (load T3 for that project)
- User asks a domain question matching a known expertise area
- First message complexity requires project state context

Memory SHOULD NOT load when:
- Simple factual Q&A with no user-specific dimension
- Anonymous or public API calls
- Token budget is critically low (<5,000 remaining)

---

## Loading Strategy

Ref: `memory_loading_strategy.md`

Default load sequence per session:
```
1. T1 (Identity) — always, ~100 tokens
2. T4 (Behavioral) — always, ~150 tokens
3. T2 (Domain) — if domain detected, ~200 tokens
4. T3 (Project) — if project referenced, ~200 tokens
5. T5 (Session) — accumulated during session
```

Total load budget: **500 tokens maximum** (ref: behavior_spec.md [CONSTRAINTS])

---

## Privacy and Isolation

- Memory is scoped to `user_id` at storage level
- Cross-user memory access is FORBIDDEN
- Memory must not leak between users even if both use the same model instance
- Explicit sharing is only possible via deliberate user action

Ref: benchmark/tests/memory/TC-0003.md — Memory Privacy Boundaries
