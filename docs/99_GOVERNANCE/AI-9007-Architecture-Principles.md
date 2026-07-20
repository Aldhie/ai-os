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

## Cross-References

- [AI-0001 Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0006 Architecture Decision Record](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md)
- [AI-9008 EDR Standard](AI-9008-Engineering-Decision-Record-Standard.md)
- [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md)

---

## 1. Purpose

Defines non-negotiable architectural principles for the `ai-os` system. Every engineering decision that deviates from these principles requires a documented Architecture Decision Record (ADR) with explicit justification.

---

## 2. Core Principles

### P-01: Fact Over Assumption

**Statement:** Every system configuration, parameter, and integration choice must be backed by verifiable evidence (official documentation, benchmark result, or experiment). Assumptions must be explicitly tagged and resolved within 14 days.

**Rationale:** Silent assumptions in AI system configurations lead to production failures that are difficult to debug. Example: `top_k` appearing to work while being silently ignored by the NIM backend.

**Enforcement:** AI-9001 §4.1 tagging rules. AUDIT cycles.

---

### P-02: Single Source of Truth

**Statement:** For every configuration parameter, there is exactly one authoritative source document. All other references point to it.

**Rationale:** Conflicting parameter values across documents cause inconsistent deployments.

**Enforcement:** `parameters.json` is the authoritative runtime source. `AI-0002` is the authoritative API reference. `AI-0003` is the authoritative compatibility reference.

---

### P-03: Minimal Surface Area

**Statement:** The system only sends parameters to NIM that are confirmed supported. Unsupported parameters are never sent.

**Rationale:** Sending unsupported parameters creates false confidence in engineers reviewing configurations.

**Enforcement:** `parameters.json` v1.1.0+ removes all unsupported parameters. Any addition to this file requires `[FACT]` tag with NIM API reference.

---

### P-04: Explicit Reasoning Mode Control

**Statement:** Every model profile must explicitly specify reasoning mode (ON/OFF/medium_effort). Implicit defaults are not acceptable.

**Rationale:** Nemotron Ultra 550B reasoning mode significantly affects output quality, token cost, and response latency. Implicit defaults risk wrong mode for task type.

**Enforcement:** All model profiles in `parameters.json` must have `system_prompt` field with `/think` or `/nothink`. AI-9003 §4.1.

---

### P-05: Defense in Depth for API Keys

**Statement:** API keys must never be stored in repository files, UI fields, or logs. Keys are managed exclusively via environment variables or secrets managers.

**Rationale:** Keys committed to git or stored in application DB are an unacceptable security risk, especially for paid API endpoints.

**Enforcement:** `parameters.json` uses `api_key_env` field (pointer to env var), never inline key value.

---

### P-06: Benchmark Before Production

**Statement:** No configuration change that affects model output quality is deployed to production without at least one benchmark test case result.

**Rationale:** LLM output quality is non-deterministic. Changes that appear correct in development may degrade in production without empirical validation.

**Enforcement:** AI-9005 §2.2 Benchmark Gate.

---

### P-07: Context Budget Discipline

**Statement:** The system always tracks and enforces token budgets across all context components (system prompt, history, RAG, output reservation).

**Rationale:** Nemotron Ultra 550B default context is 256K tokens. Unbounded context injection causes `422` errors and unpredictable truncation.

**Enforcement:** `parameters.json` `context` block defines all budgets. No pipeline may bypass these budgets without explicit override documented in ADR.

---

### P-08: Experiment-Driven Optimization

**Statement:** Optimization decisions (parameter tuning, prompt changes, RAG configuration) are made based on experiment results, not intuition.

**Rationale:** LLM behavior is counterintuitive. Example: `temperature: 0.6` appeared correct for reasoning but NVIDIA docs show `1.0` for this specific model.

**Enforcement:** EXP-xxxx documents must be completed before parameter changes are merged to `main`.

---

### P-09: Graceful Degradation

**Statement:** Every integration point with NIM has defined fallback behavior for: HTTP 429 (rate limit), HTTP 422 (validation error), HTTP 500 (server error), and connection timeout.

**Rationale:** NVIDIA Cloud NIM free tier has strict rate limits. Production systems must handle these gracefully.

**Enforcement:** Error handling requirements documented in AI-0005. Pipeline implementations must handle all listed error codes.

---

### P-10: Zero Placeholder Policy

**Statement:** No document in `Active` status may contain placeholder content (TODO without linked issue, empty tables, or template sections with example text).

**Rationale:** Placeholder content creates false confidence in document completeness and misleads engineers relying on these documents.

**Enforcement:** AI-9001 §4.5 prohibited content rules. Pre-release checklist AI-9005 §2.1.

---

## 3. Principle Traceability Matrix

| Principle | Enforced By | Verified In | Risk if Violated |
|-----------|-------------|-------------|------------------|
| P-01 Fact Over Assumption | AI-9001 §4.1 | AUDIT cycles | Silent wrong behavior |
| P-02 Single Source of Truth | AI-9006 structure | Cross-reference review | Config drift |
| P-03 Minimal Surface Area | parameters.json + audit | API response inspection | False confidence |
| P-04 Explicit Reasoning Mode | AI-9003 §4.1 | EXP-0003 | Wrong mode → wrong output |
| P-05 API Key Security | parameters.json structure | Security audit | Key exposure |
| P-06 Benchmark Before Prod | AI-9005 §2.2 | Pre-release checklist | Quality regression |
| P-07 Context Budget | parameters.json context block | Token tracking | 422 errors, truncation |
| P-08 Experiment-Driven | EXP-xxxx workflow | Experiment results | Suboptimal parameters |
| P-09 Graceful Degradation | AI-0005 + pipelines | Error injection test | User-facing crashes |
| P-10 Zero Placeholder | AI-9001 §4.5 | Document review | Misleading docs |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release — 10 architecture principles |
