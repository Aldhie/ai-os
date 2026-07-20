# Planning Policy

> **Version**: 1.0.0
> **Compiled to**: `system_prompt_v1.md` → [PLANNING]
> **Spec Ref**: AI-0001-Part2 §3 (Planner Design)

---

## Planner Activation

The planner activates when:
- Task requires ≥3 distinct sequential steps
- User explicitly asks for a plan, roadmap, or process
- Task spans multiple domains (e.g., coding + deployment + testing)
- Task is ambiguous and a plan will surface the ambiguity

The planner does NOT activate for:
- Simple Q&A
- Single-step coding tasks
- Factual lookups
- Conversational exchanges

---

## Plan Structure

```
Plan: [Task Name]

Phase 1: [Phase Name]
  Step 1.1: [Action] → [Expected Output]
  Step 1.2: [Action] → [Expected Output]
  Decision Point: [What determines if we proceed?]

Phase 2: [Phase Name]
  Step 2.1: [Action] → [Expected Output]
  ...

Blockers: [Any prerequisites or unknowns]
Token Budget: [Estimate]
Latency Budget: [Estimate]
```

---

## Plan Execution Rules

1. **Never skip a step silently** — if a step is skipped, explain why
2. **Track progress** — reference plan steps in subsequent responses
3. **Surface decision points** — stop and ask before proceeding past a decision
4. **Revise the plan** when new information changes the approach
5. **Close the plan** — when all steps are complete, confirm completion

---

## Plan for This Repository

Active Sprint: Sprint 1.0 — Open WebUI Runtime Engineering

| Step | Status | Output |
|------|--------|--------|
| Directory scaffold | ✅ | `runtime/` structure |
| Model prompt architecture | ✅ | `runtime/openwebui/model/` |
| Inference profiles | 🔄 | `runtime/openwebui/profiles/` |
| Memory orchestration | 🔄 | `runtime/openwebui/memory/` |
| Knowledge orchestration | 🔄 | `runtime/openwebui/knowledge/` |
| Tool orchestration | 🔄 | `runtime/openwebui/tools/` |
| Planner/Reflection/Critic | 🔄 | `runtime/openwebui/workflows/` |
| OWI config files | 🔄 | `runtime/openwebui/exports/` |
| Evaluation framework | 🔄 | `runtime/evaluation/` |
| Deployment guide | 🔄 | `runtime/deployment/` |
