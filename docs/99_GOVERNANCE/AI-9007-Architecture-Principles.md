# AI-9007: Architecture Principles

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9007 |
| **Title** | AI Engineering Architecture Principles |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | All engineering decisions in `Aldhie/ai-os` |
| **Cross-References** | [AI-9008](AI-9008-Engineering-Decision-Record-Standard.md) · [AI-0006](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md) · [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md) |

---

## 1. Purpose

These principles are the non-negotiable engineering constraints that govern every architecture decision in this repository. When two valid technical approaches conflict, these principles determine which path to take.

---

## 2. Core Principles

### P-01: Evidence Over Assumption

> **Every engineering decision must be grounded in verified evidence: official documentation, reproducible benchmark, or controlled experiment.**

Rationale: AI engineering is full of plausible-sounding assumptions that break in production. A single benchmark run costs less than a production incident.

Implication: Before deploying a configuration, run the relevant experiment from `docs/05_EXPERIMENTS/`. If no experiment exists, create one.

---

### P-02: Explicit Over Implicit

> **System behavior must be explicitly configured, not inferred from defaults.**

Rationale: NVIDIA Nemotron Ultra 550B has reasoning mode, multiple thinking strategies, and tool calling — all with different defaults depending on backend (vLLM/SGLang/TRT-LLM). Implicit behavior is undefined behavior.

Implication: Every deployed model profile must explicitly declare `/think` or `/nothink` in its system prompt. Reasoning mode must never be left to default.

---

### P-03: Fail Loudly Over Fail Silently

> **A configuration that produces wrong results silently is worse than one that produces an error.**

Rationale: `top_k` and `repetition_penalty` were silently ignored by NIM. Engineers believed they were active. This is the most dangerous failure mode in AI system engineering.

Implication: Any parameter not confirmed by official docs must be removed from production configs. Unknown = removed, not kept.

---

### P-04: Separation of Concerns

> **Model capabilities, API integration, UI configuration, and business logic must be independently specified and testable.**

Layers:
1. **Model Layer** — AI-0001 (what the model can do)
2. **API Layer** — AI-0002 (what the API exposes)
3. **Integration Layer** — AI-0003 (what Open WebUI passes through)
4. **Configuration Layer** — `configs/` (runtime decisions)
5. **Application Layer** — `prompts/` (task-specific behavior)

Implication: A bug in layer 3 must not require changes in layer 1.

---

### P-05: Traceability

> **Every engineering decision must link to the requirement that mandated it, the experiment that validated it, and the configuration that implements it.**

Implementation: Every config value has a `REQ-AI-xxxx` in `REQ-INDEX.md`. Every REQ links to an `EXP-xxxx`. Every EXP links to a `TC-xxxx`.

---

### P-06: Cost Awareness

> **Token consumption is a production resource. Every configuration decision must account for token cost.**

Nemotron Ultra 550B reasoning mode generates thinking traces that can consume thousands of tokens before the visible response. Every profile must specify `max_tokens` with awareness of thinking trace overhead.

Implication: Reasoning profiles must have `max_tokens ≥ 16000` to accommodate thinking traces. Never set `max_tokens: 2048` for a reasoning profile.

---

### P-07: Security by Default

> **Production deployments must follow the principle of least privilege. No credential must exist in any committed file.**

Implementation:
- `NVIDIA_API_KEY` stored in env var, never in `parameters.json`
- Separate keys for dev/staging/prod environments
- Secret scanning before every push (CI gate)

---

### P-08: Progressive Enhancement

> **The system must function at a baseline level before advanced features are enabled.**

Deployment order:
1. Basic chat (confirmed working) → enable streaming → enable system prompts → test reasoning → enable tools → enable RAG → enable agents

Implication: Function calling (R-08) must not be enabled until BM-09 (tool call format verification) is complete.

---

## 3. Principle Violation Escalation

| Violation | Severity | Response |
|-----------|----------|----------|
| Silent config error (P-03) | 🔴 Critical | Immediate hotfix; add to audit report |
| Unverified assumption in Active doc (P-01) | 🔴 Critical | Reclassify to `[ASSUMPTION]`; create EXP |
| Missing REQ link (P-05) | 🟡 High | Add REQ before next release |
| No reasoning mode declaration (P-02) | 🟡 High | Update system prompt before next deploy |
| Missing cost estimate (P-06) | 🟢 Medium | Document in profile config |

---

## 4. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release — 8 core principles |
