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
| **Last Updated** | 2026-07-20 |
| **Category** | Governance |

---

## Cross References

- [AI-0001 — Nemotron Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0006 — Architecture Decision Record](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md)
- [AI-9008 — Engineering Decision Record Standard](AI-9008-Engineering-Decision-Record-Standard.md)

---

## 1. Purpose

Defines the non-negotiable architectural principles for the `ai-os` system. Every architecture decision, configuration change, and engineering document must be consistent with these principles. When a decision conflicts with a principle, the conflict must be explicitly documented as an ADR.

---

## 2. Core Principles

### P-001: Evidence Before Configuration

> No configuration parameter is set without L1 or L2 evidence that it (a) is supported by the target model/API, and (b) improves the target metric.

**Rationale:** The AI-0003-Audit discovered that `top_k` and `repetition_penalty` were silently ignored by NVIDIA NIM, creating false confidence in the system configuration. This principle prevents recurrence.

**Implication:** Every parameter in `configs/` must cite its evidence source in the `_metadata.audit` field.

---

### P-002: Benchmark Before Production

> No feature is marked Active or promoted to production configuration until a benchmark test case (TC-xxx) has been executed and passed.

**Rationale:** Features marked [UNKNOWN] or [HYPOTHESIS] in AI-0003 represent operational risk. Benchmarks convert uncertainty into engineering fact.

**Implication:** `capabilities.json` fields cannot be `enabled: true` without a corresponding `TC-xxx` result.

---

### P-003: Explicit Reasoning Mode

> Every agent, pipeline, and model profile must explicitly declare its reasoning mode (`/think`, `/nothink`, `medium_effort`, or `reasoning_budget`).

**Rationale:** Default reasoning mode behavior is model-version dependent and can change with NIM updates. Undeclared mode = undefined behavior.

**Evidence:** [NVIDIA NIM Official Docs](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b) — `enable_thinking` parameter is not on by default for all deployment configurations.

---

### P-004: Separation of Concerns — OW vs NIM

> Open WebUI features are classified as either OW-side (processed before the NIM API call) or NIM-side (sent in the API payload). These must never be conflated in documentation or configuration.

**Rationale:** This distinction is the foundation of AI-0003 and prevents misattribution of failures. A RAG failure is an OW-side failure; a parameter rejection is a NIM-side failure.

---

### P-005: Token Budget Awareness

> Every prompt, RAG configuration, and conversation setting must be designed with explicit awareness of the token budget split.

**Rationale:** Nemotron Ultra 550B defaults to 256K context on Cloud NIM (not 1M — see AI-0003-Audit NEW-04). Uncontrolled context growth causes request failures and unpredictable cost.

---

### P-006: Pipeline Over Workaround

> When Open WebUI UI cannot expose a required NIM parameter (e.g., `extra_body.chat_template_kwargs`), the solution is a validated Pipeline, not an undocumented workaround.

**Rationale:** Pipelines are first-class Open WebUI features with version control, logging, and testability. Undocumented workarounds accumulate as technical debt.

---

### P-007: Fail Loudly, Not Silently

> System configurations and pipelines must be designed to surface errors explicitly (400, 422, 429 from NIM) rather than allowing silent failures.

**Rationale:** The discovery that `top_k` is silently dropped by NIM illustrates the danger of silent failures. A system that fails loudly is debuggable; one that fails silently is not.

---

### P-008: No Orphan Documents

> Every document must link to at least two other related documents. Every configuration file must cite its engineering spec.

**Rationale:** An isolated document is undiscoverable and unmaintainable. Cross-references create a navigable knowledge graph.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial architecture principles — derived from AI-0003-Audit findings |
