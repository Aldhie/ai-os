# REQ-INDEX: Engineering Requirements Traceability Matrix
## NVIDIA Nemotron Ultra 550B × Open WebUI

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | REQ-INDEX |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Related Documents

- ↑ [AI-0001 Engineering Spec](./AI-0001-Nemotron-Engineering-Spec.md)
- ↑ [AI-0002 NIM API Reference](./AI-0002-NVIDIA-NIM-API.md)
- ↑ [AI-0003 Compatibility Matrix](./AI-0003-OpenWebUI-Compatibility.md)
- ↑ [AI-0004 Benchmark Framework](./AI-0004-Benchmark.md)
- ↑ [AI-0005 Free Tier Strategy](./AI-0005-FreeTier-Strategy.md)
- ↓ [benchmark/tests/](../../benchmark/tests/)
- ↓ [docs/05_EXPERIMENTS/](../05_EXPERIMENTS/)

---

## REQ-AI-0001: Model Identity and Version Control

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0001 |
| **Title** | Model identity and version must be pinned and verified |
| **Priority** | 🔴 Critical |
| **Status** | ✅ Implemented |
| **Source Document** | AI-0001 §1, AI-0002 §2 |

**Purpose:** Ensure that the model deployed is always the intended model. Version drift can cause silent behaviour changes.

**Engineering Decision:** Pin model_id to `nvidia/nemotron-3-ultra-550b-a55b`. Never use `latest` aliases.

**Rationale:** NVIDIA may update model weights behind the same API endpoint. Pinning ensures reproducibility.

**Verification Method:** API response must return `model: "nvidia/nemotron-3-ultra-550b-a55b"` in every completion response header.

**Benchmark Reference:** NIM-TC-0001 (model identity check)

**OpenWebUI Impact:** Model ID field in OW model configuration must match exactly.

**Memory Impact:** None — model identity is stateless.

**Risk:** NVIDIA may deprecate model ID. Monitor NVIDIA changelog.

**Dependencies:** REQ-AI-0002 (API correctness)

**Future Improvement:** Automate model identity assertion in pre-run benchmark checklist.

---

## REQ-AI-0002: API Parameter Correctness

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0002 |
| **Title** | All API parameters must be validated against official NIM documentation |
| **Priority** | 🔴 Critical |
| **Status** | ✅ Implemented (v1.2.0 configs) |
| **Source Document** | AI-0002 §3, AI-0003 §4 |

**Purpose:** Prevent silent failures caused by unsupported parameters being ignored by NIM.

**Engineering Decision:** Maintain `unsupported_parameters_do_not_use` list in parameters.json. Remove `top_k` and `repetition_penalty` (both silently ignored by NIM).

**Rationale:** NIM does not return errors for unknown parameters — it silently ignores them. This can mask configuration bugs.

**Verification Method:** Test each parameter by sending it and verifying the response changes predictably. Parameters that produce no change under all conditions are likely ignored.

**Benchmark Reference:** BM-12 (temperature comparison), CODE-TC-0002 (parameter validation)

**OpenWebUI Impact:** OW Advanced Parameters UI may expose top_k and repetition_penalty. These must not be configured.

**Memory Impact:** None.

**Risk:** NIM API may add support for previously unsupported parameters in future versions — review on NIM updates.

**Dependencies:** None

**Future Improvement:** Automated parameter validation script that detects unsupported params in parameters.json.

---

## REQ-AI-0003: Temperature Configuration

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0003 |
| **Title** | Temperature must be set to 1.0 for all profiles |
| **Priority** | 🔴 Critical |
| **Status** | ✅ Implemented |
| **Source Document** | AI-0002 §3.1, EXP-0001 |

**Purpose:** Maximize output quality and diversity without introducing instability.

**Engineering Decision:** temperature = 1.0 for all profiles. This is the official NVIDIA default and recommendation.

**Rationale:** Official NVIDIA NIM documentation shows temperature=1.0 in all example requests. Temperature < 1.0 reduces diversity and may suppress valid reasoning paths. Temperature > 1.0 increases instability without quality benefit.

**Verification Method:** EXP-0001 (Temperature experiment) — empirical comparison of 0.0, 0.6, 1.0.

**Benchmark Reference:** BM-12

**OpenWebUI Impact:** OW temperature slider default. Must be set to 1.0 in model config.

**Memory Impact:** Indirectly affects memory recall quality (higher diversity = better memory extraction).

**Risk:** NVIDIA may change default recommendation. Review on model updates.

**Dependencies:** REQ-AI-0002

**Future Improvement:** Measure temperature effect on reasoning chain quality (EXP-0001).

---

## REQ-AI-0004: Thinking Mode Control

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0004 |
| **Title** | Thinking mode must be controllable per-request via system prompt directives |
| **Priority** | 🔴 Critical |
| **Status** | ✅ Implemented |
| **Source Document** | AI-0001 §4, AI-0002 §4 |

**Purpose:** Allow selective activation of reasoning mode to balance quality vs token cost.

**Engineering Decision:** Use `/think` and `/nothink` system prompt directives as documented by NVIDIA. Advanced control (medium_effort, reasoning_budget) requires Pipeline injection.

**Rationale:** Reasoning mode increases token cost by 8–20×. Blanket activation would exhaust free tier quota. Per-request control optimizes quality/cost ratio.

**Verification Method:** EXP-0003 — verify /think activates visible `<think>` block in response. Verify /nothink suppresses it.

**Benchmark Reference:** BM-11 (medium_effort), REAS-TC-0001 (reasoning activation)

**OpenWebUI Impact:** System prompt field must begin with `/think` or `/nothink`. OW must not strip the directive.

**Memory Impact:** Thinking traces are NOT persisted to memory. Only final response is memory-eligible.

**Risk:** NVIDIA may change directive syntax. Review on model updates.

**Dependencies:** REQ-AI-0002, REQ-AI-0011

**Future Improvement:** Expose thinking mode toggle in OW chat UI via custom Pipeline.

---

## REQ-AI-0005: Tool Calling and Agentic Capability

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0005 |
| **Title** | Tool calling must work end-to-end through Open WebUI |
| **Priority** | 🔴 Critical |
| **Status** | ⚠️ Partially Verified — BM-09 pending |
| **Source Document** | AI-0003 §5, AI-0002 §5 |

**Purpose:** Enable agentic workflows: model can call tools, receive results, and continue reasoning.

**Engineering Decision:** Enable function_calling in capabilities.json. Verify qwen3_coder tool call format compatibility with OW.

**Rationale:** Ultra 550B natively supports tool calling per NVIDIA documentation. OW wraps this transparently in standard chat completions. However, Cloud NIM may use SGLang backend requiring additional chat_template_kwargs injection.

**Verification Method:** BM-09 — send tool definition, observe tool_call in response, send tool result, observe final answer.

**Benchmark Reference:** BM-01 (parallel tool calls), BM-02 (agentic RAG), BM-03 (MCP), BM-09 (format)

**OpenWebUI Impact:** OW Tools tab must be enabled. Tool schema auto-registration must work with NIM qwen3_coder format.

**Memory Impact:** Tool call/result pairs should not be stored in memory unless explicitly relevant.

**Risk:** qwen3_coder format may not be OW-compatible. Fallback: manual tool call parsing via Pipeline.

**Dependencies:** REQ-AI-0002, REQ-AI-0004

**Future Improvement:** Custom Pipeline for reliable tool call parsing regardless of backend format.

---

## REQ-AI-0006: RAG and Embeddings

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0006 |
| **Title** | RAG must work with separate embedding provider (NIM does not provide embeddings) |
| **Priority** | 🔴 Critical |
| **Status** | ⚠️ Partially Configured — embedding provider must be set |
| **Source Document** | AI-0003 §7, capabilities.json |

**Purpose:** Enable document-grounded responses without hallucination.

**Engineering Decision:** RAG enabled in OW. Embedding provider must be configured separately (not NIM). Recommended: nomic-embed-text via Ollama for development.

**Rationale:** Cloud NIM endpoint does NOT expose /v1/embeddings. Using NIM URL for embeddings will silently fail or return 404. Separate embedding provider is architecturally required.

**Verification Method:** BM-02 — upload document, ask question about document content, verify grounded response.

**Benchmark Reference:** BM-02, MEM-TC-0001, EXP-0006

**OpenWebUI Impact:** OW Embeddings Settings must be configured with non-NIM provider. Critical configuration step.

**Memory Impact:** RAG context injection counts against context budget (REQ-AI-0007).

**Risk:** Embedding provider outage breaks RAG entirely. Mitigation: local Ollama embedding as fallback.

**Dependencies:** REQ-AI-0007

**Future Improvement:** Hybrid search evaluation (BM-02 extension).

---

## REQ-AI-0007: Context Window Management

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0007 |
| **Title** | Total context must be managed to stay within confirmed limits |
| **Priority** | 🟡 High |
| **Status** | ✅ Implemented (conservative 32K budget vs 256K limit) |
| **Source Document** | AI-0001 §2, parameters.json context_budget |

**Purpose:** Prevent context overflow errors and ensure predictable token costs.

**Engineering Decision:** Conservative 32K total context budget. Default NIM context = 256K. 1M context unconfirmed for Cloud NIM public endpoint.

**Rationale:** Using < 32K of available 256K is conservative by design during development. Prevents runaway costs. BM-10 will verify actual Cloud NIM limit.

**Verification Method:** BM-10 — send context approaching 256K, verify response. Then approach 1M, verify error or success.

**Benchmark Reference:** BM-10

**OpenWebUI Impact:** OW history compression settings should match context budget. Memory injection size must be constrained.

**Memory Impact:** Each memory injection reduces available tokens for output.

**Risk:** Conservative budget may limit use cases requiring long document analysis.

**Dependencies:** REQ-AI-0006, REQ-AI-0011

**Future Improvement:** Dynamic context budget allocation via Pipeline based on task type.

---

## REQ-AI-0008: System Prompt Engineering

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0008 |
| **Title** | System prompt must be structured, versioned, and validated |
| **Priority** | 🟡 High |
| **Status** | ✅ Implemented |
| **Source Document** | configs/prompts/system-prompt.md, EXP-0004 |

**Purpose:** Ensure consistent, predictable model behaviour across sessions.

**Engineering Decision:** System prompt maintained as versioned document. First line must be `/think` or `/nothink` directive. Prompt must be under 500 tokens.

**Rationale:** System prompt is the primary behavioural control surface. Unversioned prompts cause unreproducible behaviour.

**Verification Method:** EXP-0004 — A/B test prompt variants, measure output quality.

**Benchmark Reference:** All benchmark categories (system prompt affects all tests)

**OpenWebUI Impact:** OW System Prompt field. Must be set in model config, not per-session.

**Memory Impact:** System prompt tokens counted against context budget.

**Risk:** Overly long system prompt reduces available context for task content.

**Dependencies:** REQ-AI-0004, REQ-AI-0007

**Future Improvement:** Automated system prompt token counting in CI.

---

## REQ-AI-0009: Memory Policy

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0009 |
| **Title** | Memory must follow explicit retention and injection policies |
| **Priority** | 🟡 High |
| **Status** | ✅ Implemented |
| **Source Document** | docs/00_ENGINEERING/MemoryPolicy.md |

**Purpose:** Prevent stale memory from polluting context. Ensure memory injection is purposeful.

**Engineering Decision:** Auto-save enabled. Auto-recall enabled. Short-term: 7 days. Long-term: unlimited. Memory injection capped at 2,048 tokens.

**Rationale:** Unconstrained memory recall can silently consume context budget. 2K injection cap ensures memory assists without dominating context.

**Verification Method:** EXP-0005 — test memory recall accuracy, staleness, and injection impact on context.

**Benchmark Reference:** MEM-TC-0001, MEM-TC-0002, EXP-0005

**OpenWebUI Impact:** OW Memory settings must match policy. Auto-save and auto-recall enabled.

**Memory Impact:** Direct — this requirement defines memory behaviour.

**Risk:** Memory injection of irrelevant context can decrease response quality.

**Dependencies:** REQ-AI-0007

**Future Improvement:** Memory relevance scoring before injection.

---

## REQ-AI-0010: Knowledge Policy

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0010 |
| **Title** | Knowledge base documents must be versioned and validated before ingestion |
| **Priority** | 🟡 High |
| **Status** | 📋 Planned |
| **Source Document** | docs/00_ENGINEERING/KnowledgePolicy.md |

**Purpose:** Prevent incorrect or outdated knowledge from contaminating RAG responses.

**Engineering Decision:** All knowledge documents must have metadata headers (version, date, source). Ingestion validation script required.

**Rationale:** RAG grounds responses in ingested documents. Incorrect documents produce confidently wrong answers — more dangerous than no RAG.

**Verification Method:** EXP-0006 — test RAG with intentionally outdated document, verify model cites source date.

**Benchmark Reference:** MEM-TC-0003, EXP-0006

**OpenWebUI Impact:** OW Collections must be organized by domain and version.

**Memory Impact:** Knowledge base documents are distinct from memory. Both count against context.

**Risk:** Knowledge base grows unbounded over time, increasing retrieval noise.

**Dependencies:** REQ-AI-0006, REQ-AI-0007

**Future Improvement:** Automated knowledge base staleness detection.

---

## REQ-AI-0011: Token Budget Monitoring

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0011 |
| **Title** | Token usage must be monitored and bounded in development |
| **Priority** | 🟡 High |
| **Status** | ✅ Policy defined — monitoring manual |
| **Source Document** | AI-0005, capabilities.json |

**Purpose:** Prevent free tier quota exhaustion during development.

**Engineering Decision:** Profile assignment strategy: escalate from general → medium_effort → reasoning only when task requires it. Monitor OW analytics.

**Rationale:** Reasoning mode 8–20× token multiplier can exhaust daily free tier in 6–10 requests.

**Verification Method:** Track actual daily token usage via OW analytics for 1 week.

**Benchmark Reference:** EXP-0003 (token cost measurement)

**OpenWebUI Impact:** OW Admin Analytics must be checked daily during development.

**Memory Impact:** Memory injection adds to per-request token cost.

**Risk:** Accidental reasoning mode activation in automated workflow could exhaust quota.

**Dependencies:** REQ-AI-0004

**Future Improvement:** Token budget alert via OW webhook when 70% consumed.

---

## REQ-AI-0012: Benchmark-Driven Development

| Field | Value |
|-------|-------|
| **REQ ID** | REQ-AI-0012 |
| **Title** | Every engineering claim must be verifiable by a benchmark |
| **Priority** | 🟡 High |
| **Status** | ✅ Framework defined — tests pending execution |
| **Source Document** | AI-0004 |

**Purpose:** Prevent undocumented assumptions from becoming engineering decisions.

**Engineering Decision:** Benchmark framework defined in AI-0004. Every AI-000X document must reference at least one BM-ID or TC-ID.

**Rationale:** Engineering claims without evidence are assumptions. Assumptions without labels are bugs.

**Verification Method:** REQ traceability audit — every claim in AI-0001 through AI-0005 must have a BM-ID or [ASSUMPTION] label.

**Benchmark Reference:** AI-0004 (entire framework)

**OpenWebUI Impact:** Benchmark results stored in OW Collections for team reference.

**Memory Impact:** Benchmark run context must not use session memory (must clear before each run).

**Risk:** Benchmark suite maintenance cost increases as repository grows.

**Dependencies:** All REQ-AI-000X

**Future Improvement:** Automated benchmark runner via GitHub Actions.

---

*REQ-INDEX v1.0.0 — Created 2026-07-20*
