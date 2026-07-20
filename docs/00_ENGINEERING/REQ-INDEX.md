# Requirements Traceability Index
## Aldhie/ai-os — NVIDIA Nemotron Ultra 550B AI Engineering System

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | REQ-INDEX |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related** | AI-0001, AI-0002, AI-0003, AI-0004, AI-0005, AI-0006 |

---

## Purpose

Every engineering requirement in the ai-os system has a unique REQ-ID. This index is the master traceability document linking requirements to their source specification, verification method, benchmark reference, and implementation status.

---

## REQ-AI-0001 — Model Architecture Understanding

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0001 |
| **Title** | Full documentation of Nemotron Ultra 550B architecture |
| **Purpose** | Engineers must understand the model before configuring or prompting it |
| **Priority** | 🔴 Critical |
| **Source Document** | AI-0001-Nemotron-Engineering-Spec.md |
| **Engineering Decision** | Document all architectural details: LatentMoE, Mamba-2, SWA, attention hybrid |
| **Rationale** | Architecture directly determines which configurations are valid |
| **Verification Method** | Review against official NVIDIA documentation |
| **Benchmark Reference** | BM-12: Temperature quality comparison |
| **OpenWebUI Impact** | Understanding architecture prevents misconfiguration |
| **Memory Impact** | None direct |
| **Risk** | Outdated if NVIDIA updates model architecture |
| **Dependencies** | REQ-AI-0002 (API), REQ-AI-0003 (Compatibility) |
| **Status** | ✅ Implemented (AI-0001 v2.0.0) |
| **Future Improvement** | Add architecture diagram, add Mamba-2 vs Transformer comparison |

---

## REQ-AI-0002 — Inference Parameter Correctness

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0002 |
| **Title** | All inference parameters must be NIM-validated |
| **Purpose** | Prevent silent parameter errors that produce wrong outputs without errors |
| **Priority** | 🔴 Critical |
| **Source Document** | AI-0002-NVIDIA-NIM-API.md, AI-0003-Critical-Findings-Audit.md |
| **Engineering Decision** | Only use parameters documented in official NIM API reference |
| **Rationale** | Confirmed: top_k and repetition_penalty are silently dropped by NIM |
| **Verification Method** | Send request with known parameter; verify response behavior |
| **Benchmark Reference** | BM-01 (tool calls), BM-12 (temperature) |
| **OpenWebUI Impact** | parameters.json must not contain invalid params |
| **Memory Impact** | None |
| **Risk** | NIM API may change silently |
| **Dependencies** | REQ-AI-0001 |
| **Status** | ⚠️ In Progress — configs not yet fixed |
| **Future Improvement** | Add parameter validation script |

---

## REQ-AI-0003 — Temperature Calibration

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0003 |
| **Title** | Temperature must be set to 1.0 for Nemotron Ultra 550B |
| **Purpose** | Optimal generation quality for this specific model |
| **Priority** | 🔴 Critical |
| **Source Document** | AI-0003-Critical-Findings-Audit.md |
| **Engineering Decision** | Set temperature=1.0 — confirmed by official NVIDIA docs (all examples use 1.0) |
| **Rationale** | Official docs show temperature=1.0 in all code examples. 0.6 was an undocumented assumption |
| **Verification Method** | EXP-0001-Temperature.md — empirical comparison |
| **Benchmark Reference** | BM-12 |
| **OpenWebUI Impact** | Update parameters.json from 0.6 to 1.0 |
| **Memory Impact** | None |
| **Risk** | Task-specific deviation may be needed (deterministic tasks: 0.0–0.3) |
| **Dependencies** | REQ-AI-0002 |
| **Status** | ⚠️ In Progress — config not yet updated |
| **Future Improvement** | Task-specific temperature profiles per EXP-0001 results |

---

## REQ-AI-0004 — Reasoning Mode Control

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0004 |
| **Title** | Reasoning mode (thinking on/off/budget) must be explicitly controlled per agent |
| **Purpose** | Prevent token waste on non-reasoning tasks; ensure deep reasoning on complex tasks |
| **Priority** | 🔴 Critical |
| **Source Document** | AI-0001, AI-0002, AI-0003-Audit |
| **Engineering Decision** | Use system prompt `/think` or `/nothink` via Open WebUI. Use Pipeline for `medium_effort` and `reasoning_budget`. |
| **Rationale** | `extra_body` not exposed in OW UI. System prompt method is officially documented. Pipeline needed for advanced controls. |
| **Verification Method** | EXP-0003-Thinking.md |
| **Benchmark Reference** | BM-11 (medium_effort pipeline), EXP-0003 |
| **OpenWebUI Impact** | Per-agent system prompt must include `/think` or `/nothink` |
| **Memory Impact** | Thinking traces consume significant tokens — memory budget must account for this |
| **Risk** | Inconsistent reasoning if system prompt is overridden by user |
| **Dependencies** | REQ-AI-0002, REQ-AI-0003 |
| **Status** | ⚠️ In Progress |
| **Future Improvement** | Pipeline implementation for `medium_effort` and `reasoning_budget` |

---

## REQ-AI-0005 — Tool Calling Enablement

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0005 |
| **Title** | Function calling must be enabled and validated |
| **Purpose** | Enable agent workflows, structured output, and agentic RAG |
| **Priority** | 🔴 Critical |
| **Source Document** | AI-0003-OpenWebUI-Compatibility.md, AI-0003-Audit |
| **Engineering Decision** | Enable `function_calling.enabled: true` in capabilities.json after BM-09 validation |
| **Rationale** | NIM confirmed to support tool calling. qwen3_coder parser used server-side. |
| **Verification Method** | BM-09: qwen3_coder format verification |
| **Benchmark Reference** | BM-01, BM-02, BM-09 |
| **OpenWebUI Impact** | Update capabilities.json + test tool round-trip |
| **Memory Impact** | Tool results injected as context — increase memory budget |
| **Risk** | qwen3_coder format may not be fully compatible with OW tool call parser |
| **Dependencies** | REQ-AI-0002 |
| **Status** | ⚠️ In Progress — pending BM-09 |
| **Future Improvement** | Parallel tool calls (BM-01), MCP integration (BM-03) |

---

## REQ-AI-0006 — RAG Embedding Provider

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0006 |
| **Title** | Separate embedding provider must be configured for RAG |
| **Purpose** | Cloud NIM does not expose /v1/embeddings — RAG will fail without separate embedder |
| **Priority** | 🔴 Critical |
| **Source Document** | AI-0003-OpenWebUI-Compatibility.md, AI-0003-Audit |
| **Engineering Decision** | Use nomic-embed-text via Ollama (local) or nvidia/nv-embedqa-e5-v5 (cloud) |
| **Rationale** | Confirmed: NIM Ultra 550B is text generation only. No embeddings endpoint. |
| **Verification Method** | Attempt /v1/embeddings call to NIM — should return 404 or 405 |
| **Benchmark Reference** | BM-02 (Agentic RAG), BM-10 (context limit) |
| **OpenWebUI Impact** | Configure separate embedding model in OW settings |
| **Memory Impact** | Embedding quality directly affects memory recall precision |
| **Risk** | Latency added by external embedding call |
| **Dependencies** | REQ-AI-0005 |
| **Status** | ❌ Not implemented |
| **Future Improvement** | EXP-0006-RAG.md — compare embedding models |

---

## REQ-AI-0007 — Context Window Budget Management

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0007 |
| **Title** | Context window must be explicitly managed to prevent overflow |
| **Purpose** | Prevent 422 errors and silent truncation from context overflow |
| **Priority** | 🟡 High |
| **Source Document** | AI-0001, AI-0003, Audit |
| **Engineering Decision** | Default context limit: 256K tokens. Implement sliding window for long conversations. |
| **Rationale** | Default deployment is 256K per audit. 1M requires specific server flag not confirmed on Cloud NIM. |
| **Verification Method** | BM-10: Send 260K token request to Cloud NIM endpoint — measure behavior |
| **Benchmark Reference** | BM-10 |
| **OpenWebUI Impact** | Set history_budget_tokens appropriately in parameters.json |
| **Memory Impact** | Memory injection must not exceed remaining context budget |
| **Risk** | Over-budgeting leads to silent truncation; under-budgeting wastes available context |
| **Dependencies** | REQ-AI-0006 |
| **Status** | ⚠️ In Progress — default set but 1M limit unverified |
| **Future Improvement** | Implement context summarization pipeline |

---

## REQ-AI-0008 — System Prompt Engineering Standard

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0008 |
| **Title** | System prompts must follow engineering standard |
| **Purpose** | Consistent, predictable model behavior across all agents |
| **Priority** | 🟡 High |
| **Source Document** | prompts/ directory, EXP-0004 |
| **Engineering Decision** | System prompts must include: (1) thinking mode directive, (2) output format, (3) persona scope |
| **Rationale** | Without explicit directives, model uses default behavior which may not match task needs |
| **Verification Method** | EXP-0004-SystemPrompt.md |
| **Benchmark Reference** | EXP-0004 |
| **OpenWebUI Impact** | Per-model system prompt in OW model config |
| **Memory Impact** | System prompt tokens count against context budget |
| **Risk** | User-injected instructions override system prompt — test RLHF boundary |
| **Dependencies** | REQ-AI-0004 |
| **Status** | ⚠️ In Progress |
| **Future Improvement** | Automated system prompt testing |

---

## REQ-AI-0009 — API Key Security

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0009 |
| **Title** | API keys must never be stored in Open WebUI database |
| **Purpose** | Prevent credential exposure |
| **Priority** | 🔴 Critical |
| **Source Document** | AI-0003-OpenWebUI-Compatibility.md |
| **Engineering Decision** | Store NVIDIA_API_KEY in environment variable; configure OW to read from env |
| **Rationale** | OW database keys exposed in DB backups, logs, and API responses |
| **Verification Method** | Inspect OW settings — key field should show masked env reference |
| **Benchmark Reference** | N/A (security requirement) |
| **OpenWebUI Impact** | Connection settings use `${NVIDIA_API_KEY}` pattern |
| **Memory Impact** | None |
| **Risk** | Key rotation requires env var update + OW restart |
| **Dependencies** | None |
| **Status** | ❌ Not implemented |
| **Future Improvement** | Integration with secret manager (Vault, AWS Secrets Manager) |

---

## REQ-AI-0010 — Observability and Telemetry

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0010 |
| **Title** | All AI interactions must be observable via OTel or equivalent |
| **Purpose** | Debug, performance analysis, cost tracking |
| **Priority** | 🟡 High |
| **Source Document** | AI-0003 Section 7 |
| **Engineering Decision** | Enable OpenTelemetry in Open WebUI; track TTFT, token counts, error rates |
| **Rationale** | Without telemetry, production issues are invisible |
| **Verification Method** | Verify OTel traces appear in collector after request |
| **Benchmark Reference** | All BM-* items depend on telemetry for timing |
| **OpenWebUI Impact** | OTel configuration in OW deployment |
| **Memory Impact** | None |
| **Risk** | OTel overhead negligible; trace volume may be high at scale |
| **Dependencies** | None |
| **Status** | ⚠️ In Progress |
| **Future Improvement** | Custom OTel spans for reasoning trace tokens |

---

## REQ-AI-0011 — Free Tier Token Budget

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0011 |
| **Title** | Token usage must stay within NVIDIA NIM free tier limits |
| **Purpose** | Avoid unexpected costs; maximize development on free tier |
| **Priority** | 🟡 High |
| **Source Document** | AI-0005-FreeTier-Strategy.md |
| **Engineering Decision** | Implement token budget per agent profile; use 256K context sparingly; thinking OFF by default |
| **Rationale** | Free tier has request and token limits. Reasoning ON multiplies token cost 3-10x. |
| **Verification Method** | Monitor token usage in OW analytics |
| **Benchmark Reference** | EXP-0003 (thinking token cost) |
| **OpenWebUI Impact** | max_tokens caps per profile in parameters.json |
| **Memory Impact** | Memory injection increases token cost |
| **Risk** | Quota exhaustion blocks development |
| **Dependencies** | REQ-AI-0010 |
| **Status** | ⚠️ In Progress |
| **Future Improvement** | Auto-throttling pipeline when approaching limits |

---

## REQ-AI-0012 — Benchmark Coverage

| Field | Value |
|-------|-------|
| **ID** | REQ-AI-0012 |
| **Title** | Every capability must have at least one benchmark test case |
| **Purpose** | Verify capabilities work as documented; detect regressions |
| **Priority** | 🟡 High |
| **Source Document** | AI-0004-Benchmark.md, benchmark/tests/ |
| **Engineering Decision** | 36 test cases across 12 categories, executed before any config change |
| **Rationale** | Engineering claims must be verifiable |
| **Verification Method** | Run benchmark suite; compare to baseline |
| **Benchmark Reference** | All BM-* |
| **OpenWebUI Impact** | Benchmark runner integrates with OW API |
| **Memory Impact** | Benchmark sessions should not pollute memory |
| **Risk** | Benchmarks become stale if model or config changes |
| **Dependencies** | All REQ-* |
| **Status** | ❌ Not implemented |
| **Future Improvement** | Automated CI benchmark on config change |

---

## Requirements Status Summary

| REQ-ID | Title | Priority | Status |
|--------|-------|----------|--------|
| REQ-AI-0001 | Model Architecture Understanding | 🔴 Critical | ✅ Implemented |
| REQ-AI-0002 | Inference Parameter Correctness | 🔴 Critical | ⚠️ In Progress |
| REQ-AI-0003 | Temperature Calibration | 🔴 Critical | ⚠️ In Progress |
| REQ-AI-0004 | Reasoning Mode Control | 🔴 Critical | ⚠️ In Progress |
| REQ-AI-0005 | Tool Calling Enablement | 🔴 Critical | ⚠️ In Progress |
| REQ-AI-0006 | RAG Embedding Provider | 🔴 Critical | ❌ Not Implemented |
| REQ-AI-0007 | Context Window Budget | 🟡 High | ⚠️ In Progress |
| REQ-AI-0008 | System Prompt Standard | 🟡 High | ⚠️ In Progress |
| REQ-AI-0009 | API Key Security | 🔴 Critical | ❌ Not Implemented |
| REQ-AI-0010 | Observability | 🟡 High | ⚠️ In Progress |
| REQ-AI-0011 | Free Tier Budget | 🟡 High | ⚠️ In Progress |
| REQ-AI-0012 | Benchmark Coverage | 🟡 High | ❌ Not Implemented |

---

## Cross-Reference Map

```
REQ-AI-0001 (Architecture)
  └─ implements ──► AI-0001 (Spec)
  └─ validates ──► REQ-AI-0002 (Parameters)
  └─ informs ───► REQ-AI-0004 (Reasoning)

REQ-AI-0002 (Parameters)
  └─ implements ──► AI-0002 (API), parameters.json
  └─ requires ───► REQ-AI-0003 (Temperature)
  └─ validates ──► EXP-0001, EXP-0002

REQ-AI-0003 (Temperature)
  └─ implements ──► parameters.json profile.temperature=1.0
  └─ validates ──► EXP-0001-Temperature.md
  └─ evidence ───► AI-0003-Critical-Findings-Audit.md

REQ-AI-0004 (Reasoning)
  └─ implements ──► System prompts /think /nothink
  └─ validates ──► EXP-0003-Thinking.md
  └─ advanced ───► Pipeline (medium_effort, reasoning_budget)

REQ-AI-0005 (Tool Calling)
  └─ implements ──► capabilities.json function_calling.enabled=true
  └─ validates ──► BM-09, BM-01, BM-03
  └─ depends ────► REQ-AI-0002

REQ-AI-0006 (RAG Embeddings)
  └─ implements ──► Separate embedding provider
  └─ validates ──► EXP-0006-RAG.md
  └─ depends ────► REQ-AI-0005

REQ-AI-0007 (Context Budget)
  └─ implements ──► parameters.json context budgets
  └─ validates ──► BM-10
  └─ depends ────► REQ-AI-0006

REQ-AI-0008 (System Prompt)
  └─ implements ──► prompts/ directory
  └─ validates ──► EXP-0004-SystemPrompt.md
  └─ depends ────► REQ-AI-0004

REQ-AI-0009 (Security)
  └─ implements ──► env var NVIDIA_API_KEY
  └─ validates ──► Security review

REQ-AI-0010 (Observability)
  └─ implements ──► OTel configuration
  └─ validates ──► Trace verification test

REQ-AI-0011 (Free Tier)
  └─ implements ──► max_tokens per profile
  └─ validates ──► OW analytics monitoring
  └─ depends ────► REQ-AI-0010

REQ-AI-0012 (Benchmarks)
  └─ implements ──► benchmark/tests/
  └─ validates ──► All BM-* results
  └─ depends ────► All REQ-*
```

---

*REQ-INDEX v1.0.0 — 2026-07-20*
