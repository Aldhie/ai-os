# Planner

| Field | Value |
|---|---|
| **Title** | AI-OS Planner Module Specification |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines the Planner module, which decomposes complex user requests into structured, executable subtasks. The Planner is the first stage in the AI-OS runtime pipeline, responsible for understanding intent and generating an actionable plan before execution.

---

## Scope

- Triggered on: multi-step tasks, ambiguous requests, research queries, project planning
- Output: structured plan consumed by execution loop
- Applies to: Nemotron Ultra 550B via NVIDIA NIM

---

## Planner Architecture

```text
User Input
    │
    ▼
[Intent Classifier]
    │
    ├── Simple Query ──────────────────► Direct Response
    │
    └── Complex Task ───────────────► [Planner]
                                            │
                                      [Plan Output]
                                            │
                                      [Executor]
                                            │
                                      [Reflection]
                                            │
                                      [Critic]
                                            │
                                       Final Output
```

---

## Plan Output Schema

```json
{
  "goal": "string",
  "steps": [
    {
      "id": 1,
      "action": "string",
      "tool": "string | null",
      "depends_on": [],
      "expected_output": "string"
    }
  ],
  "constraints": ["string"],
  "success_criteria": "string"
}
```

---

## Planner Prompt

See: `prompts/nemotron-ultra/planner.txt`

---

## Planner Parameters

| Parameter | Value | Reason |
|---|---|---|
| Temperature | 0.3 | Structured, deterministic plans |
| Max Tokens | 4096 | Allow full plan generation |
| Format | JSON | Machine-parsable output |

---

## Trigger Conditions

The Planner is activated when:

1. Query contains 3+ distinct subtasks.
2. Query requires tool use.
3. Query involves multi-document research.
4. Query is explicitly: "create a plan", "outline", "steps to".

---

## Dependencies

- `prompts/nemotron-ultra/planner.txt`
- `docs/20_RUNTIME/Reflection.md`
- `docs/20_RUNTIME/Critic.md`
- `docs/20_RUNTIME/Workflow.md`

---

## References

- [ReAct: Synergizing Reasoning and Acting in LLMs](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)

---

## TODO

- [ ] Write planner prompt in `prompts/nemotron-ultra/planner.txt`
- [ ] Define intent classifier logic
- [ ] Test plan schema validation
- [ ] Build plan visualization for debugging
- [ ] Measure planner quality vs direct response
