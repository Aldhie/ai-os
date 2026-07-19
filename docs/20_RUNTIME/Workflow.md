# Workflow

| Field | Value |
|---|---|
| **Title** | AI-OS Runtime Workflow Specification |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Documents the end-to-end runtime workflow of AI-OS, showing how each module (Planner, Executor, Reflection, Critic) interacts to process a user request from input to final output.

---

## Scope

- Complete request-response lifecycle
- All runtime modes: Simple, Planned, Tool-Augmented
- Open WebUI + NVIDIA NIM integration

---

## Runtime Workflow

```text
┌────────────────────────────────────────────────┐
│                    USER INPUT                          │
└──────────────────────┬─────────────────────────┘
                       │
          ┌──────────┴──────────┐
          │   PRE-PROCESSING FILTER    │  (Open WebUI Filter)
          │   - Input sanitization      │
          │   - Token count check       │
          │   - Memory injection        │
          │   - RAG retrieval           │
          └──────────┬──────────┘
                       │
          ┌──────────┴──────────┐
          │     INTENT CLASSIFIER      │
          └───┬───────────────┬───┘
              │                 │
         Simple               Complex
              │                 │
         ┌───┴───┐      ┌───┴───┐
         │ DIRECT  │      │ PLANNER │
         │GENERATE │      │  LOOP  │
         └───┬───┘      └───┬───┘
              │                 │
              └──────▼──────┘
                       │
          ┌──────────┴──────────┐
          │       REFLECTION          │
          └──────────┬──────────┘
                       │
          ┌──────────┴──────────┐
          │         CRITIC            │
          └───┬───────────────┬───┘
         Pass                      Fail
              │                 │
   ┌─────────┴───┐   ┌────┴─────────┐
   │ POST-PROCESS   │   │   REVISION  │
   │ FILTER        │   │   (max 3x)  │
   └──────┬──────┘   └────────────┘
              │
   ┌─────────┴─────────┐
   │       USER OUTPUT       │
   └───────────────────┘
```

---

## Workflow States

| State | Description |
|---|---|
| `INPUT_RECEIVED` | Raw user message received |
| `PRE_PROCESSED` | Filters applied, memory injected |
| `CLASSIFIED` | Intent classified (simple/complex) |
| `PLANNED` | Plan generated (complex only) |
| `GENERATING` | Model generating response |
| `REFLECTING` | Reflection check in progress |
| `CRITIQUING` | Critic scoring in progress |
| `REVISING` | Revision cycle triggered |
| `POST_PROCESSED` | Output filters applied |
| `DELIVERED` | Final response sent to user |
| `FAILED` | Max retries exceeded |

---

## Dependencies

- `docs/20_RUNTIME/Planner.md`
- `docs/20_RUNTIME/Reflection.md`
- `docs/20_RUNTIME/Critic.md`
- `configs/openwebui/filters.json`

---

## References

- [Open WebUI Pipelines](https://docs.openwebui.com/pipelines/)
- [LangGraph Workflow Patterns](https://langchain-ai.github.io/langgraph/)

---

## TODO

- [ ] Implement workflow as Open WebUI pipeline
- [ ] Build state machine for workflow tracking
- [ ] Add telemetry for each workflow stage
- [ ] Implement max-retry logic
- [ ] Build workflow visualization dashboard
