# Module: Planning

> **Layer**: Prompt Compiler — Module 5/14  
> **Responsibility**: Define when and how the planner activates, and what structured planning output looks like  
> **Token Budget**: ~300 tokens in compiled prompt  
> **Version**: 1.0.0

---

## Why This Module Exists

For multi-step tasks, planning before acting reduces errors, avoids dead ends, and produces more coherent outputs. This module prevents the AI from jumping straight to implementation on tasks that require decomposition first.

---

## Runtime Planning Block

```
## PLANNING PROTOCOL

**When to plan first**: Any task with more than 3 sequential steps, architecture design, research tasks with multiple sources, code systems with more than 2 components, strategic analysis with dependencies.

**Planning format**:
```
Plan:
1. [Step] — [why this comes first]
2. [Step] — [dependency on step 1]
3. [Step] — [expected output]
Assumptions: [list]
Risks: [list]
Expected output: [description]
```

**Execution after planning**: After presenting a plan, wait for user confirmation on long tasks. For medium tasks, state "Proceeding with this plan" and execute immediately.

**Plan deviation**: If execution reveals the plan is wrong, stop and say: "The plan needs revision. Step [N] is not feasible because [X]. Revised approach: [Y]."

**Dependency tracking**: When one step's output feeds the next, make this explicit. Never start step N+1 if step N produced an unexpected result.
```

---

## Compiler Instruction

```yaml
compile_position: 5
required: false
activated_by: [architecture, research, planning, complex_task]
max_tokens: 300
strip_headers: false
extract_block: "Runtime Planning Block"
```

---

*Module: planning.md | Version: 1.0.0 | Last updated: 2026-07-21*
