# AI-0003: Open WebUI × NVIDIA Nemotron Ultra Compatibility Matrix

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-0003 |
| **Title** | Open WebUI × NVIDIA Nemotron Ultra Compatibility Matrix |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | Open WebUI (latest stable) × NVIDIA Nemotron Ultra 550B Cloud NIM |

---

## Purpose

This document classifies every Open WebUI setting and feature against NVIDIA Nemotron Ultra 550B (Cloud NIM) with full engineering context: compatibility status, explanation, root cause, recommendation, risk level, and priority. It is the authoritative reference for what works, what breaks, what is silently ignored, and what needs validation.

---

## Classification Legend

| Status | Icon | Meaning |
|--------|------|---------|
| **Supported** | ✅ | Feature works end-to-end between Open WebUI and NIM |
| **Unsupported** | ❌ | Feature cannot work; NIM does not provide the required capability |
| **Ignored** | ⚠️ | Open WebUI sends the parameter; NIM accepts but silently drops it |
| **Unknown** | ❓ | Behavior not yet verified from official docs or testing |
| **Need Benchmark** | 🔬 | Feature may work but requires empirical testing to confirm |

## Priority Legend

| Priority | Icon | Meaning |
|----------|------|---------|
| **Critical** | 🔴 | Will cause failures or silent wrong behavior in production |
| **High** | 🟡 | Significant impact on user experience or system reliability |
| **Medium** | 🟢 | Noticeable gap but has a workaround |
| **Low** | ⚪ | Minor impact; acceptable as-is |

---

## Dependencies

- `AI-0002-NVIDIA-NIM-API.md` — complete NIM API parameter reference
- `AI-0001-Nemotron-Engineering-Spec.md` — model capabilities
- `configs/openwebui/parameters.json` — current runtime configuration
- `configs/openwebui/capabilities.json` — current feature flags

---

## 1. Inference Parameters Matrix

These are the parameters Open WebUI sends directly in the `POST /v1/chat/completions` payload.

| Parameter | OW Setting | NIM Status | Explain | Reason | Recommendation | Risk | Priority |
|-----------|------------|------------|---------|--------|----------------|------|----------|
| `temperature` | Inference → Temperature | ✅ Supported | Controls output randomness. Range `0.0–2.0`. | NIM fully supports. NVIDIA recommends `0.6` (reasoning ON) or `0.0` (reasoning OFF). | Set `0.6` for reasoning tasks; `0.0` for RAG/classification. Current config uses `0.6` ✅ | Misconfiguration → incoherent or deterministic outputs | 🔴 Critical |
| `top_p` | Inference → Top P | ✅ Supported | Nucleus sampling. Range `0.0–1.0`. | NIM fully supports. NVIDIA recommends `0.95` with reasoning ON. | Set `0.95` for reasoning ON. Current config correct ✅ | Minor quality impact if misconfigured | 🟡 High |
| `top_k` | Inference → Top K | ❌ Unsupported (Ignored) | Top-K sampling not a supported NIM parameter. | NVIDIA NIM `/v1/chat/completions` does not expose `top_k`. Parameter will be sent by Open WebUI but silently dropped by NIM. | **Remove `top_k: 40` from `parameters.json`** — it is dead config creating false confidence. | Silent wrong behavior: engineer believes top_k is active when it is not. | 🔴 Critical |
| `max_tokens` | Inference → Max Tokens | ✅ Supported | Hard cap on output tokens. Range `1–1,048,576` for Ultra 550B. | NIM fully supports. | Set to task-appropriate value. `2048` default is acceptable but low for reasoning traces. Consider `4096–8192` for reasoning ON. | Response truncation if too low; cost overrun if too high | 🟡 High |
| `stream` | Inference → Stream | ✅ Supported | SSE streaming. | NIM fully supports identical SSE format. Open WebUI handles streaming natively. | Keep `true` for all interactive use. ✅ | None | 🔴 Critical |
| `stop` | Inference → Stop Sequences | ✅ Supported | Up to 4 stop tokens. | NIM supports stop sequences. | Keep `[]` (empty) unless specific stop tokens required. | Premature response truncation if stop tokens collide with content | 🟢 Medium |
| `frequency_penalty` | Inference → Frequency Penalty | ✅ Supported | Penalizes frequent tokens. Range `-2.0–2.0`. | NIM supports. | Leave at `0.0` (default) unless repetition is observed. | Minor quality impact | 🟢 Medium |
| `presence_penalty` | Inference → Presence Penalty | ✅ Supported | Encourages topic diversity. Range `-2.0–2.0`. | NIM supports. | Leave at `0.0` default. | Minor quality impact | 🟢 Medium |
| `repetition_penalty` | Inference → Repetition Penalty | ❌ Unsupported (Ignored) | Hugging Face-style repetition penalty. Different from `frequency_penalty`. | Not an OpenAI API parameter. NIM does not support this field. Open WebUI sends it; NIM drops it. | **Remove `repetition_penalty: 1.1` from `parameters.json`**. Use `frequency_penalty` instead. | Silent: engineer believes repetition is controlled, but it is not. | 🔴 Critical |
| `seed` | Inference → Seed | ✅ Supported | Reproducible outputs (best-effort). | NIM supports seed parameter. | Use for deterministic testing and debugging. Not required for production. | None if omitted | ⚪ Low |
| `n` | (Not exposed in OW UI) | ❌ Unsupported | Multiple completions per request. | NIM only supports `n=1`. Open WebUI doesn't typically send `n>1`. | Do not set `n > 1` anywhere in pipeline code. | Hard `400` error from NIM if sent | 🔴 Critical |
| `logprobs` | Advanced → Logprobs | 🔬 Need Benchmark | Log probabilities of tokens. | NIM claims support; Open WebUI may not expose this in UI but can send via model params. | Not needed for standard use. Test before enabling. | None for typical use | ⚪ Low |
| `response_format` | Model → Response Format | ✅ Supported | Forces JSON output mode. | NIM supports `{type: "json_object"}`. Open WebUI can be configured to request JSON mode. | Enable per-model in agents requiring structured JSON output. | Model may produce malformed JSON without careful prompting | 🟢 Medium |

---

## 2. Chat Features Matrix

| Feature | Open WebUI | NIM Status | Explain | Reason | Recommendation | Risk | Priority |
|---------|------------|------------|---------|--------|----------------|------|----------|
| Basic chat completion | Chat → Send | ✅ Supported | Standard `POST /v1/chat/completions`. | Core feature. Full parity. | No action needed. | None | 🔴 Critical |
| Streaming responses | Chat → Stream toggle | ✅ Supported | SSE chunks with `data: {...}` prefix. | NIM SSE format identical to OpenAI. Open WebUI handles it natively. | Keep streaming enabled. ✅ | None | 🔴 Critical |
| System prompt | Model → System Prompt | ✅ Supported | Injected as `{role: "system"}` message. | NIM processes system role correctly. | For reasoning ON: set system prompt to `"detailed thinking on"`. For OFF: `"detailed thinking off"`. | Wrong reasoning mode if system prompt not set correctly | 🔴 Critical |
| Multi-turn conversation | Chat history | ✅ Supported | Conversation history sent as messages array. | NIM is stateless; Open WebUI manages history client-side and sends full array. | Implement context trimming before 128K limit is hit (Super 49B) or 1M limit (Ultra 550B). | Context overflow causes `422` or truncated history | 🟡 High |
| Multi-model side-by-side | Chat → Multi-model | ✅ Supported (OW-side) | Open WebUI makes separate API calls per model. | Each model gets its own request. NIM handles each independently. | No action needed. Cost doubles per message. | Higher token cost | 🟢 Medium |
| File & image upload | Chat → Attach | ⚠️ Partial | File content extracted and injected as text. Images: ❌ not supported by NIM text models. | Nemotron Ultra 550B is text-only. Image uploads will be extracted as text if possible, or ignored. | Disable image upload for NIM models. Enable file-to-text extraction (PDFs, docs). Display clear error for images. | User confusion when images silently fail | 🟡 High |
| Voice input (STT) | Chat → Microphone | ✅ Supported (OW-side) | Speech transcribed locally or via Whisper; text sent to NIM. | STT is processed before the NIM API call. NIM only receives text. | No action needed. ✅ | Transcription accuracy depends on STT engine | 🟢 Medium |
| Text-to-speech (TTS) | Chat → Speaker | ✅ Supported (OW-side) | NIM response text converted to audio by TTS engine. | TTS is post-processing in Open WebUI. NIM only produces text. | No action needed. ✅ | TTS quality depends on engine | 🟢 Medium |
| Image generation | Chat → Image gen | ❌ Unsupported | Requires separate image generation model (DALL-E, etc.). | Nemotron Ultra is text-only. Image generation is a separate NIM endpoint. | Disable for this model. Connect a separate image gen provider if needed. | User-facing error or silent failure | 🟡 High |
| Code execution | Chat → Code block run | ✅ Supported (OW-side) | Open Terminal or browser sandbox. | Code execution happens in Open WebUI's sandboxed environment. NIM only generates the code. | No action needed. ✅ | Code execution security depends on sandbox config | 🟢 Medium |
| Web search | Chat → Web search | ✅ Supported (OW-side) | Search results injected into context before NIM call. | Open WebUI fetches search results; injects as context messages. NIM processes augmented prompt. | Verify search context fits within token budget. Monitor context size. | Context overflow from long search results | 🟡 High |
| Message queue | Chat → Queue | ✅ Supported (OW-side) | Open WebUI queues messages while model is responding. | Client-side feature. Transparent to NIM. | No action needed. ✅ | None | ⚪ Low |
| Thinking/Reasoning mode | System prompt control | ✅ Supported (via workaround) | Nemotron Ultra 550B: use `extra_body.chat_template_kwargs.enable_thinking`. Open WebUI: use system prompt `"detailed thinking on/off"`. | Open WebUI does not natively support `extra_body`. Must use system prompt method as a workaround. | Set system prompt in model config: `"detailed thinking on"` for reasoning tasks. | Inconsistent reasoning behavior without explicit control | 🔴 Critical |
| Automations / scheduled prompts | Admin → Automations | ✅ Supported (OW-side) | Cron-like scheduling within Open WebUI. | Transparent to NIM — just scheduled API calls. | Monitor token consumption for automated prompts. | Quota exhaustion from unmonitored automations | 🟡 High |

---

## 3. Knowledge & RAG Matrix

| Feature | Open WebUI | NIM Status | Explain | Reason | Recommendation | Risk | Priority |
|---------|------------|------------|---------|--------|----------------|------|----------|
| Document upload (RAG) | Knowledge → Upload | ✅ Supported (OW-side) | Documents chunked, embedded, stored in vector DB. Relevant chunks injected into context. | Open WebUI handles all RAG pipeline. NIM only sees the augmented prompt. | Configure `chunk_size: 512`, `top_k: 5` as per `capabilities.json`. ✅ | Chunk quality affects answer accuracy | 🟡 High |
| Vector database | Knowledge → Vector DB | ✅ Supported (OW-side) | ChromaDB (default), PGVector, Qdrant, etc. | Entirely client-side in Open WebUI. Transparent to NIM. | Use ChromaDB for local; PGVector for production. | DB reliability affects RAG quality | 🟢 Medium |
| Hybrid search (BM25 + vector) | Knowledge → Hybrid | ✅ Supported (OW-side) | BM25 keyword + vector semantic search with reranking. | Managed by Open WebUI. Transparent to NIM. | Enable hybrid search for better recall on domain-specific docs. | Reranker model adds latency | 🟢 Medium |
| Embeddings endpoint | Knowledge → Embedding model | ❌ Unsupported on Cloud NIM | `/v1/embeddings` endpoint not available on NVIDIA Cloud NIM for Nemotron Ultra. | NVIDIA Cloud NIM does not expose an embeddings endpoint for this model. | Use a separate embedding provider: `nomic-embed-text`, `mxbai-embed-large`, or local Ollama embedding model. | RAG will fail silently if embeddings endpoint is misconfigured | 🔴 Critical |
| Full context injection | Knowledge → Full doc mode | ✅ Supported | Inject entire documents without chunking. | Sends full document text in context. NIM supports up to 1M tokens (Ultra 550B). | Use for critical documents where chunking may miss context. Monitor token cost. | Very high token cost; potential context overflow | 🟡 High |
| Agentic retrieval | Knowledge → Agentic | 🔬 Need Benchmark | Model autonomously calls retrieval tools. Requires tool calling support from NIM. | Depends on NIM tool calling being functional. Ultra 550B supports tool calling per spec. | Test with a simple retrieval tool first. Verify tool call round-trip works. | If tool calling has latency issues, agentic RAG will be slow | 🔬 Need Benchmark |
| Reranking model | Knowledge → Reranker | ❓ Unknown | Cross-encoder reranking of retrieved chunks. | Reranker is a separate model call inside Open WebUI. NIM is not involved. | Use a local reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) or none. | Poor reranker degrades RAG quality | 🟢 Medium |

---

## 4. Tool Use & Function Calling Matrix

| Feature | Open WebUI | NIM Status | Explain | Reason | Recommendation | Risk | Priority |
|---------|------------|------------|---------|--------|----------------|------|----------|
| Function calling (basic) | Tools → Enable tools | ✅ Supported | NIM accepts `tools` array in OpenAI schema format. Ultra 550B supports tool calling. | NIM Cloud supports tool calling per official API reference. `finish_reason: tool_calls` is returned. | Enable in `capabilities.json` — change `function_calling.enabled: false` to `true`. | Tool schema errors cause `400` responses | 🔴 Critical |
| `tool_choice: auto` | Tools → Auto | ✅ Supported | Model decides whether to call a tool. | NIM supports `tool_choice: auto`. | Default behavior. Use for general agents. | Model may skip tool when it should call it | 🟢 Medium |
| `tool_choice: required` | Tools → Force | ✅ Supported | Forces model to always call a tool. | NIM supports `tool_choice: required`. | Use when you must guarantee a structured output via tool schema. | Model always calls tool even when unnecessary | 🟢 Medium |
| Parallel tool calls | Tools → Parallel | ⚠️ Partial / Unknown | Multiple tools called in one response. | NIM behavior varies by model. Ultra 550B may support parallel tool calls but not verified. | Test explicitly. Default to sequential tool calls for safety. | Race condition or missed tool results if parallel handling is buggy | 🔬 Need Benchmark |
| Streaming tool calls | Stream + Tools | ✅ Supported | Tool call deltas streamed as `delta.tool_calls` chunks. | NIM supports streaming with tool calls. Accumulate chunks client-side. | Implement tool call accumulator in pipeline. | Incomplete tool calls if stream is interrupted | 🟡 High |
| Python tools (OW built-in) | Tools → Python scripts | ✅ Supported (OW-side) | Open WebUI executes Python tools; results injected as `{role: "tool"}` messages. | NIM only sees the tool result in the messages array. Transparent. | Great for web search, calculator, date tools. ✅ | Tool execution security depends on sandbox | 🟢 Medium |
| MCP (Model Context Protocol) | Extensibility → MCP | 🔬 Need Benchmark | Open WebUI supports Streamable HTTP MCP servers. Tools from MCP exposed to model. | Whether NIM correctly handles MCP-derived tool schemas needs verification. | Test with a simple MCP tool server before deploying complex MCP integrations. | Schema incompatibility could cause tool calling failures | 🔬 Need Benchmark |
| OpenAPI tool servers | Extensibility → OpenAPI | 🔬 Need Benchmark | Auto-discover tools from OpenAPI endpoints. | Same dependency on NIM tool calling as above. | Test with a simple REST endpoint first. | Schema incompatibility | 🔬 Need Benchmark |
| Web search tool | Tools → Web search | ✅ Supported (OW-side) | Tavily, DuckDuckGo, etc. Results injected as context. | Transparent to NIM — just text injection. No tool call required. | Use context injection mode (not function calling mode) for reliability. | Context overflow from long search results | 🟡 High |

---

## 5. Model & Agent Configuration Matrix

| Feature | Open WebUI | NIM Status | Explain | Reason | Recommendation | Risk | Priority |
|---------|------------|------------|---------|--------|----------------|------|----------|
| Model presets / system prompts | Models → System Prompt | ✅ Supported | Custom system prompts per agent. | Sent as `{role: "system"}` — fully supported by NIM. | Use to set reasoning mode, persona, and output format per agent. | Incorrect system prompt breaks reasoning toggle | 🔴 Critical |
| Dynamic variables (`{{ USER_NAME }}`) | Models → Variables | ✅ Supported (OW-side) | Open WebUI resolves variables before sending to NIM. | Variable substitution is client-side. NIM sees resolved text. | No action needed. ✅ | Variable resolution failures cause malformed prompts | 🟢 Medium |
| Bound tools per model | Models → Bound Tools | 🔬 Need Benchmark | Force-enable specific tools for this model. | Depends on tool calling compatibility (see Section 4). | Enable after tool calling is validated. | Tool schema errors cause 400s | 🔬 Need Benchmark |
| Knowledge binding per model | Models → Knowledge | ✅ Supported (OW-side) | RAG injection per model. | Handled by Open WebUI pre-processing. | Bind domain-specific knowledge bases to specialized agents. | Token budget overflow if docs are large | 🟡 High |
| Model access control (RBAC) | Admin → Users/Groups | ✅ Supported (OW-side) | User/group restrictions on model access. | Entirely within Open WebUI auth layer. Transparent to NIM. | Configure role-based access to NIM model. | Misconfigured RBAC exposes API to unauthorized users | 🟡 High |
| Custom model parameter overrides | Models → Params | ✅ Supported | Per-model overrides of temperature, max_tokens, etc. | Merged into API payload by Open WebUI. NIM sees final merged values. | Define per-agent profiles: `reasoning`, `creative`, `code`. ✅ | Parameter conflicts between global and model-level settings | 🟡 High |
| `extra_body` injection | (Not in UI) | ❌ Not in OW UI | `extra_body.chat_template_kwargs.enable_thinking` cannot be set via Open WebUI UI. | Open WebUI does not expose `extra_body` in model settings UI. | **Workaround:** Use system prompt `"detailed thinking on/off"` to control reasoning mode. This is the primary method for Nemotron Super 49B and works for Ultra 550B as well. | Reasoning mode cannot be toggled dynamically without a custom pipeline | 🔴 Critical |
| Pipelines (filter/transform) | Extensibility → Pipelines | ✅ Supported (OW-side) | Pre/post processing of messages and responses. | Open WebUI pipelines intercept messages before NIM. Can inject `extra_body`, strip params, transform responses. | **Use a Pipeline to inject `extra_body.chat_template_kwargs`** for reasoning toggle. This is the correct solution for `extra_body` limitation. | Pipeline bugs can corrupt payloads | 🟡 High |

---

## 6. Memory & Personalization Matrix

| Feature | Open WebUI | NIM Status | Explain | Reason | Recommendation | Risk | Priority |
|---------|------------|------------|---------|--------|----------------|------|----------|
| Long-term memory | Memory → Enable | ✅ Supported (OW-side) | Open WebUI stores user facts; injects relevant memories into context. | Memory retrieval and injection is client-side. NIM only sees the augmented prompt. | Keep `auto_save: true`, `auto_recall: true` as configured. ✅ | Memory injection increases token cost per message | 🟢 Medium |
| Memory retention policy | Memory → Retention | ✅ Supported (OW-side) | 7-day short-term, unlimited long-term as configured. | Managed by Open WebUI's database. Transparent to NIM. | Current config acceptable. Review if memory size grows. | Large memory set increases context size | ⚪ Low |
| Per-user memory isolation | Memory → User scope | ✅ Supported (OW-side) | Memories are per-user in Open WebUI. | User identity managed by Open WebUI auth. Transparent to NIM. | No action needed. ✅ | None | ⚪ Low |

---

## 7. Administration & Observability Matrix

| Feature | Open WebUI | NIM Status | Explain | Reason | Recommendation | Risk | Priority |
|---------|------------|------------|---------|--------|----------------|------|----------|
| Usage analytics (token tracking) | Admin → Analytics | ✅ Supported (OW-side) | Open WebUI tracks token usage from NIM responses (`usage` field). | NIM returns `usage: {prompt_tokens, completion_tokens, total_tokens}` in non-streaming responses. In streaming, usage may not be in every chunk. | Enable analytics. Note: streaming usage tracking may be incomplete. Consider non-streaming for billing-critical jobs. | Inaccurate token counts in streaming mode | 🟡 High |
| Model arena / A/B testing | Admin → Evaluation | ✅ Supported (OW-side) | Side-by-side evaluation between models. | Open WebUI makes parallel calls. NIM handles each independently. | Useful for comparing Nemotron Super 49B vs Ultra 550B. | Higher cost from parallel calls | 🟢 Medium |
| Webhooks | Admin → Webhooks | ✅ Supported (OW-side) | Notifications on completion, sign-up, etc. | Entirely within Open WebUI. Transparent to NIM. | No action needed. ✅ | None | ⚪ Low |
| OpenTelemetry / observability | Deploy → OTel | ✅ Supported (OW-side) | Traces and metrics from Open WebUI to OTel collector. | OW-side instrumentation. NIM is an external endpoint in traces. | Enable OTel for TTFT (time-to-first-token) tracking. | None | 🟢 Medium |
| Rate limit display | UI feedback | ❓ Unknown | Whether Open WebUI surfaces NIM 429 errors cleanly to users. | Depends on Open WebUI's error handling for upstream 429. | Add custom error message for 429: "NVIDIA quota exceeded — retrying in X seconds." | Poor UX: user sees raw error without guidance | 🟡 High |
| Request logging | Admin → Logs | ✅ Supported (OW-side) | Open WebUI logs request metadata. | NIM request IDs not surfaced in standard logs. | Log NIM response headers (including `request-id`) for debugging. | Difficult to debug NIM-side issues without request IDs | 🟢 Medium |

---

## 8. Authentication & Security Matrix

| Feature | Open WebUI | NIM Status | Explain | Reason | Recommendation | Risk | Priority |
|---------|------------|------------|---------|--------|----------------|------|----------|
| API key storage | Settings → Connections | ✅ Supported | API key stored in Open WebUI DB; injected into NIM requests. | Open WebUI handles auth header injection. | Store key in env var (`NVIDIA_API_KEY`); configure OW to read from env. Never hardcode in UI. | Key exposure in DB, logs, or UI if not using env vars | 🔴 Critical |
| SSO / OIDC | Admin → Auth | ✅ Supported (OW-side) | User authentication via federated identity. | OW-layer auth. Transparent to NIM. | Configure OIDC for team deployments. | None | 🟡 High |
| RBAC for model access | Admin → Permissions | ✅ Supported (OW-side) | Role-based access to Nemotron model. | OW auth layer enforces access before API call is made. | Restrict NIM model to authorized roles only. | Unauthorized NIM API calls if RBAC misconfigured | 🟡 High |
| API key per environment | Multi-env setup | ✅ Recommended | Separate keys for dev/staging/prod. | Each key has independent quota. | Configure three separate keys and environments. | Quota exhaustion in prod from dev testing | 🔴 Critical |

---

## 9. Engineering Risk Register

| # | Risk | Category | Likelihood | Impact | Mitigation |
|---|------|----------|------------|--------|------------|
| R-01 | `top_k` silently ignored — engineers believe it is active | Config Bug | High | Medium | Remove from `parameters.json` immediately |
| R-02 | `repetition_penalty` silently ignored — repetition control is ineffective | Config Bug | High | Medium | Replace with `frequency_penalty` in `parameters.json` |
| R-03 | Reasoning mode not toggled — all requests use default mode | Config Gap | High | High | Set system prompt explicitly per agent profile |
| R-04 | Embeddings endpoint not available on Cloud NIM — RAG will fail | Integration Gap | High | Critical | Configure separate embedding provider before enabling RAG |
| R-05 | `extra_body` cannot be set via OW UI — thinking budget unusable from UI | UX Gap | Medium | Medium | Build a Pipeline to inject `extra_body` |
| R-06 | Context overflow on long conversations — no trimming implemented | Implementation Gap | Medium | High | Implement sliding window or summarization trimming |
| R-07 | Streaming usage not tracked accurately — token analytics unreliable | Observability Gap | Medium | Medium | Use non-streaming for billing jobs; supplement with manual tracking |
| R-08 | Function calling not enabled in `capabilities.json` — tools silently disabled | Config Gap | High | High | Enable after benchmark validation |
| R-09 | Rate limit (429) not surfaced as user-friendly error in Open WebUI | UX Gap | Low | Medium | Add custom error message pipeline |
| R-10 | API key stored in OW DB rather than env var — security exposure | Security Gap | Medium | Critical | Migrate key to env var / secret manager |

---

## 10. Configuration Remediation Guide

### 10.1 `parameters.json` — Required Fixes

```json
{
  "_metadata": {
    "version": "1.0.0",
    "status": "active",
    "description": "Open WebUI model parameters for Nemotron Ultra 550B via NVIDIA NIM",
    "last_updated": "2026-07-20",
    "owner": "Aldhie"
  },
  "model": {
    "provider": "nvidia-nim",
    "model_id": "nvidia/nemotron-3-ultra-550b-a55b",
    "base_url": "https://integrate.api.nvidia.com/v1",
    "api_key_env": "NVIDIA_API_KEY"
  },
  "inference": {
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 4096,
    "frequency_penalty": 0.0,
    "stream": true,
    "stop": []
  },
  "profiles": {
    "general": {
      "system_prompt": "detailed thinking off",
      "temperature": 0.6,
      "top_p": 0.95,
      "max_tokens": 2048
    },
    "reasoning": {
      "system_prompt": "detailed thinking on",
      "temperature": 0.6,
      "top_p": 0.95,
      "max_tokens": 8192
    },
    "creative": {
      "system_prompt": "detailed thinking off",
      "temperature": 1.0,
      "top_p": 0.98,
      "max_tokens": 2048
    },
    "code": {
      "system_prompt": "detailed thinking on",
      "temperature": 0.6,
      "top_p": 0.95,
      "max_tokens": 8192
    }
  },
  "context": {
    "system_prompt_budget_tokens": 500,
    "history_budget_tokens": 8192,
    "rag_budget_tokens": 4096,
    "output_reserved_tokens": 4096
  }
}
```

**Changes from v0.1.0:**
- ❌ Removed `top_k: 40` — not supported by NIM
- ❌ Removed `repetition_penalty: 1.1` — not supported by NIM; replaced with `frequency_penalty: 0.0`
- ✅ Added `system_prompt` per profile to control reasoning mode
- ✅ Increased `max_tokens` to `4096` default, `8192` for reasoning profiles
- ✅ Fixed model slug to `nvidia/nemotron-3-ultra-550b-a55b` (with `-a55b` suffix)
- ✅ Increased `history_budget_tokens` and `rag_budget_tokens` to leverage Ultra 550B's large context

### 10.2 `capabilities.json` — Required Fixes

```json
{
  "capabilities": {
    "function_calling": {
      "enabled": true,
      "note": "NIM supports tool calling. Enable after validating tool schema round-trip."
    },
    "rag": {
      "embedding_provider": "separate",
      "embedding_note": "Cloud NIM does not provide /v1/embeddings. Configure a separate embedding model (e.g., nomic-embed-text via Ollama)."
    }
  }
}
```

---

## 11. Benchmark Checklist

The following items are marked `🔬 Need Benchmark` and must be tested before production:

```
[ ] BM-01: Parallel tool calls — does Ultra 550B return multiple tool_calls in one response?
[ ] BM-02: Agentic RAG — does tool calling work reliably enough for autonomous document retrieval?
[ ] BM-03: MCP tool server — does Open WebUI MCP → NIM tool calling round-trip work?
[ ] BM-04: OpenAPI tool server — does auto-discovered OpenAPI schema work with NIM?
[ ] BM-05: Bound tools per model — does forcing tools in model config work with NIM?
[ ] BM-06: Streaming + tool call accumulation — is the accumulator implementation correct?
[ ] BM-07: 429 error display — does Open WebUI show a user-friendly message on rate limit?
[ ] BM-08: Logprobs — does Open WebUI expose logprobs and does NIM return them correctly?
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-07-20 | Initial draft — minimal skeleton |
| 1.0.0 | 2026-07-20 | Complete compatibility matrix: 60+ settings classified across 8 categories. Risk register, remediation guide, benchmark checklist. |
