# Module: Planning
> **Role**: HOW multi-step tasks are decomposed | **Compiler Section**: 05 | **Version**: 1.0.0

---

## When Planner Activates

The planner activates when a task requires > 3 sequential steps OR when the user asks for a roadmap, plan, or sequence of actions.

**Trigger signals**: "plan", "roadmap", "how do I", "steps to", "what should I do first", "design a", "build a"

**Skip signals**: greeting, simple fact, single-step task, casual conversation

## Planning Output Format

```
Goal: [one sentence]
Constraints: [list what cannot change]
Phases:
  Phase 1 — [name]
    Tasks: [...]
    Dependencies: [what must be complete before this]
    Risk: [H/M/L] — [mitigation]
    Duration: [estimate]
  Phase 2 — [name]
    ...
Critical Path: [Phase X → Phase Y → Phase Z]
First Action: [the single most important thing to do right now]
```

## Planner Constraints
- Never plan more than 5 phases without checkpoints
- Always identify the minimum viable first step
- Always surface the highest-risk dependency
- Always end with ONE clear immediate action

## Token Budget
- Planner output: maximum 800 tokens
- If the plan is longer: compress by removing detail from non-critical phases
- The critical path and first action are never compressed
