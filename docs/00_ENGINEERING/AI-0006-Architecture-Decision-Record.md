# AI-0006 — Architecture Decision Record

| Field | Value |
|-------|-------|
| **Title** | Architecture Decision Record |
| **Document ID** | AI-0006 |
| **Version** | 0.1.0 |
| **Status** | Living Document |
| **Owner** | @Aldhie |
| **Created** | 2026-07-19 |
| **Updated** | 2026-07-19 |
| **Dependencies** | All AI-00xx documents |

---

## Purpose

Records all significant architectural decisions made for AI-OS, including the context, options considered, decision made, and consequences. Follows the [MADR format](https://adr.github.io/madr/).

---

## Scope

All decisions related to:

- Model selection
- Integration architecture
- Prompt engineering strategy
- Runtime design
- Tooling choices

---

## ADR-0001: Use NVIDIA Nemotron Ultra 550B as Core Model

**Date**: 2026-07-19
**Status**: Accepted

### Context

Needed to select a high-capability LLM for an AI Operating System that can handle complex reasoning, tool use, and long-context understanding.

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| GPT-4o | High capability, mature API | Closed, cost |
| Claude 3.5 | Strong reasoning | Closed, cost |
| Llama 3.1 405B | Open weights | Requires own infra |
| **Nemotron Ultra 550B** | NVIDIA-optimized, NIM API, free tier | Less community doc |

### Decision

Use **Nemotron Ultra 550B** via NVIDIA Cloud NIM. Primary rationale: NVIDIA-first stack coherence, NIM free tier availability, and 128K context window.

### Consequences

- Must manage NIM free tier limits carefully
- Must document NIM-specific behaviors
- Cannot use OpenAI-only features (e.g., Assistants API)

---

## ADR-0002: Use Open WebUI as Interface Layer

**Date**: 2026-07-19
**Status**: Accepted

### Context

Needed a user interface that supports OpenAI-compatible backends, tool calling, RAG, and is self-hostable.

### Decision

Use **Open WebUI** as the primary UI layer.

### Consequences

- UI is decoupled from model provider
- Must configure NIM as OpenAI-compatible endpoint
- Feature set limited to Open WebUI capabilities

---

## ADR-0003: Planner-Critic-Reflection Runtime Pattern

**Date**: 2026-07-19
**Status**: Draft

### Context

Needed a runtime pattern that improves output quality through self-correction without requiring separate model calls for each step.

### Decision

Implement a **Planner → Execute → Critic → Reflect** loop within a single model (Nemotron Ultra), using structured prompt templates for each role.

### Consequences

- Increases token usage per response
- Requires careful prompt design
- Improves output quality measurably (to be benchmarked)

---

## References

- [MADR: Markdown Any Decision Records](https://adr.github.io/madr/)
- All AI-00xx engineering specs

---

## TODO

- [ ] Add ADR-0004: Memory architecture decision
- [ ] Add ADR-0005: Dataset format decision
- [ ] Add ADR-0006: Fine-tuning approach decision
- [ ] Review ADR-0003 after Planner/Critic benchmarks
