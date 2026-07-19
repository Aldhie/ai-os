# Planner

| Field | Value |
|-------|-------|
| **Title** | Runtime Planner |
| **Purpose** | Define how the AI OS plans multi-step tasks before execution |
| **Scope** | Planning algorithm, decomposition strategy, plan format, integration with tools |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | ToolPolicy.md, SystemPrompt.md, Workflow.md |
| **References** | ReAct Paper (Yao et al. 2022), Plan-and-Solve (Wang et al. 2023) |

---

## 1. When to Plan

Activate the planner when the user request:

- Requires more than 3 sequential steps
- Involves multiple tools or external data sources
- Has ambiguous requirements that need clarification before execution
- Is a project-level task spanning multiple sessions

---

## 2. Planning Algorithm

```
1. UNDERSTAND — Parse user intent and identify goals
2. DECOMPOSE — Break into atomic, executable sub-tasks
3. SEQUENCE — Order sub-tasks by dependency
4. ESTIMATE — Predict effort, tokens, and tool calls needed
5. VALIDATE — Check plan against tool availability and constraints
6. EXECUTE — Run sub-tasks with Critic review at each step
7. REPORT — Summarize results and next steps
```

---

## 3. Plan Format

```markdown
## Plan: [Task Title]

**Goal:** [What success looks like]
**Steps:**
1. [Action] → [Expected output]
2. [Action] → [Expected output]
3. [Action] → [Expected output]

**Tools Required:** [list]
**Estimated Tokens:** [estimate]
**Risk:** [any uncertainty]
```

---

## 4. Plan Storage

- Active plans stored in conversation context
- Long-running plans stored in memory
- Completed plans archived with outcome

---

## TODO

- [ ] Implement planner prompt in `prompts/nemotron-ultra/planner.txt`
- [ ] Test planner with 5+ step engineering tasks
- [ ] Define plan interruption and recovery behavior
- [ ] Integrate plan with Critic for step-level review
- [ ] Benchmark planner accuracy on structured task decomposition
