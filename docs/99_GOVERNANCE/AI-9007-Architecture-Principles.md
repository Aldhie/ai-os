# AI-9007: Architecture Principles

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9007 |
| **Title** | Architecture Principles |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Governance |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-9008](AI-9008-Engineering-Decision-Record-Standard.md) | EDR standard (implements these principles) |
| [AI-0006](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md) | Active EDRs |
| [AI-9001](AI-9001-Documentation-Standard.md) | Documentation standard |

---

## 1. Purpose

This document defines the fundamental architecture principles that govern all engineering decisions in the `ai-os` system. Any EDR, configuration change, or system design that violates these principles requires explicit justification and acceptance.

---

## 2. Core Principles

### Principle 1: Evidence-First Engineering

> Every engineering configuration must be supported by evidence.

| Aspect | Rule |
|--------|------|
| Configuration values | Must be traceable to FACT, Benchmark, or Experiment |
| Architecture decisions | Must have EDR with rationale |
| Parameter choices | Must have benchmark baseline |

Anti-pattern: Setting `temperature=0.6` because it "feels right" — this is the exact mistake identified in AI-0003-Audit. [FACT: AI-0003-Audit]

---

### Principle 2: Minimal Coupling to Platform

> The system logic must not be tightly coupled to any specific hosting platform.

The AI behavior (model behavior, memory policy, tool usage) MUST be independent from the Open WebUI layer.

| Layer | Responsibility |
|-------|---------------|
| NIM API | Model inference |
| Pipeline | Advanced parameter injection, tool orchestration |
| Open WebUI | UI, memory, RAG |
| This Repository | Configuration, documentation, benchmarks |

No business logic lives in the UI layer. Configuration belongs in `configs/`. Documentation belongs in `docs/`.

---

### Principle 3: Thinking Mode as First-Class Citizen

> Reasoning capability is the primary differentiation of Nemotron Ultra 550B. It must be explicitly controlled.

- Every system prompt MUST explicitly set thinking mode [FACT: AI-0003]
- Thinking mode ON is the default for analytical tasks
- Thinking mode OFF is the explicit choice for simple/RAG tasks (not the default)
- Token budget for thinking MUST be considered in every profile [HYPOTHESIS: see EXP-0003]

---

### Principle 4: No Configuration Without Validation

> No configuration change ships to `main` without a benchmark run.

This prevents configuration drift — where parameters gradually change based on intuition rather than evidence.

Enforced by: [AI-9002](AI-9002-Benchmark-Standard.md) Regression Policy.

---

### Principle 5: Traceability

> Every requirement has an ID. Every decision has an EDR. Every claim has a fact label.

Full traceability chain:
```
User Need
  ↓
Requirement (REQ-AI-XXXX in REQ-INDEX.md)
  ↓
Engineering Decision (EDR-XXX in AI-0006)
  ↓
Configuration (configs/openwebui/parameters.json)
  ↓
Benchmark Validation (benchmark/tests/*/TC-XXXX.md)
  ↓
Experiment Evidence (docs/05_EXPERIMENTS/EXP-XXXX.md)
```

---

### Principle 6: Preserve Knowledge

> Engineering knowledge accumulated in this repository is never deleted — only superseded.

- Deprecated documents are marked `Deprecated` and kept
- Archived benchmark results are never deleted
- Old configurations are kept in changelog format
- git history is never force-pushed or rebased on `main`

---

### Principle 7: Explicit Over Implicit

> Behavior must be explicit. Defaults are documented, not assumed.

Every configuration value, whether explicitly set or relying on default, MUST be documented in AI-0003 compatibility matrix with its effective value and the reason it is or is not explicitly set.

---

## 3. Principle Precedence

When principles conflict:

1. Evidence-First (P1) trumps all others
2. No Configuration Without Validation (P4) is non-negotiable
3. Traceability (P5) is non-negotiable
4. All others can be traded off with explicit EDR justification

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial architecture principles |
