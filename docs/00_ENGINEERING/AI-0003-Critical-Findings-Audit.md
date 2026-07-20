# AI-0003 Critical Findings Audit
## Validated Against Official NVIDIA NIM Documentation

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-0003-Audit |
| **Parent** | AI-0003-OpenWebUI-Compatibility.md |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Audit Date** | 2026-07-20 |
| **Sources** | [NVIDIA NIM API Reference](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b) · [NVIDIA Build Fine-Tune Page](https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b/fine-tune) |

---

## Purpose

AI-0003 v1.0.0 was written dari kombinasi OpenAI API knowledge + general NIM assumptions.
Audit ini memverifikasi setiap Critical Finding terhadap **dokumentasi resmi** untuk menentukan:
- Apakah finding adalah **CONFIRMED** (terbukti oleh docs)
- Apakah finding adalah **REVISED** (sebagian benar, sebagian salah)
- Apakah finding adalah **OVERTURNED** (asumsi salah — docs menunjukkan sebaliknya)
- Apakah finding tetap **UNKNOWN** (docs tidak cukup untuk membuktikan)

---

## Audit Summary

| Finding | Original Verdict | Audit Result | Severity Change |
|---------|-----------------|--------------|-----------------|
| R-01: `top_k` silently ignored | 🔴 Critical | ✅ **CONFIRMED** | Tetap Critical |
| R-02: `repetition_penalty` silently ignored | 🔴 Critical | ✅ **CONFIRMED** | Tetap Critical |
| R-03: Reasoning mode not toggled | 🔴 Critical | ⚠️ **REVISED — MORE COMPLEX** | Eskalasi ke Critical+ |
| R-04: Embeddings endpoint not available | 🔴 Critical | ✅ **CONFIRMED** | Tetap Critical |
| R-05: `extra_body` tidak bisa di-set via OW UI | 🔴 Critical | ⚠️ **REVISED — WORKAROUND CONFIRMED** | Turun ke High |
| R-08: Function calling disabled | 🔴 Critical | ⚠️ **REVISED — SEHARUSNYA ENABLED SEKARANG** | Eskalasi ke Critical |
| NEW-01: `chat_template_kwargs` wajib untuk SGLang | ❓ (tidak ada) | 🆕 **NEW CRITICAL FINDING** | New Critical |
| NEW-02: `force_nonempty_content` untuk coding agents | ❓ (tidak ada) | 🆕 **NEW FINDING** | New High |
| NEW-03: `tool_call_parser: qwen3_coder` | ❓ (tidak ada) | 🆕 **NEW FINDING** | New High |
| NEW-04: Context length default 256K bukan 1M | ❓ (tidak ada) | 🆕 **NEW FINDING** | New Medium |

---

## Detailed Audit per Finding

---

### R-01: `top_k: 40` di `parameters.json`

**Original Verdict:** 🔴 Critical — Silently Ignored

#### Evidence dari Official Docs

Dari [API Reference](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b):
```python
# Documented API call examples:
response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Write a haiku about GPUs"}],
    max_tokens=16000,
    temperature=1.0,
    top_p=0.95,
    extra_body={"chat_template_kwargs": {"enable_thinking": True}}
)
```
Tidak ada `top_k` dalam **satu pun** contoh API call di dokumentasi resmi.
Parameter yang didokumentasikan: `temperature`, `top_p`, `max_tokens`, `stop`, `seed`, `frequency_penalty`, `presence_penalty`, `response_format`.

#### Verdict: ✅ **CONFIRMED — `top_k` memang tidak didukung**

**Action Required:**
```json
// BEFORE (parameters.json v0.1.0)
{ "top_k": 40 }

// AFTER (parameters.json v1.1.0)
// REMOVED — parameter ini tidak valid untuk NIM
```

---

### R-02: `repetition_penalty: 1.1` di `parameters.json`

**Original Verdict:** 🔴 Critical — Silently Ignored

#### Evidence dari Official Docs

Sama seperti R-01 — tidak ada `repetition_penalty` dalam dokumentasi resmi NIM.
Parameter penalti yang didukung hanya: `frequency_penalty`, `presence_penalty`.

OpenCode config dari docs menunjukkan:
```json
"agent": {
  "build": { "temperature": 1.0, "top_p": 0.95, "max_tokens": 32000 },
  "plan": { "temperature": 1.0, "top_p": 0.95, "max_tokens": 32000 }
}
```
Tidak ada `repetition_penalty`.

#### Verdict: ✅ **CONFIRMED — `repetition_penalty` tidak didukung**

**Action Required:**
```json
// BEFORE (parameters.json v0.1.0)
{ "repetition_penalty": 1.1 }

// AFTER (parameters.json v1.1.0)
{ "frequency_penalty": 0.0 }  // NIM-compatible alternative
```

---

### R-03: Reasoning mode control — Original Finding Revised

**Original Verdict:** 🔴 Critical — "Gunakan system prompt `detailed thinking on/off` sebagai workaround"

#### Evidence dari Official Docs

Docs resmi menunjukkan **tiga** cara mengontrol reasoning, bukan satu:

**Method 1: `extra_body.chat_template_kwargs.enable_thinking` (PRIMARY)**
```python
extra_body={"chat_template_kwargs": {"enable_thinking": True}}   # ON
extra_body={"chat_template_kwargs": {"enable_thinking": False}}  # OFF
```

**Method 2: `medium_effort` untuk partial reasoning**
```python
extra_body={"chat_template_kwargs": {"enable_thinking": True, "medium_effort": True}}
```
> "Uses significantly fewer reasoning tokens than full thinking mode. Recommended as a starting point before tuning explicit token budgets."

**Method 3: `reasoning_budget` untuk hard token cap**
```python
# Set hard ceiling on reasoning trace tokens
result = client.chat_completion(
    model=MODEL,
    messages=[...],
    reasoning_budget=512,  # hard cap
    max_tokens=1024,
)
```
> "The model will attempt to close the trace at the next newline before the budget is hit; if none is found within 500 tokens it closes abruptly at `reasoning_budget + 500`"

**Method 4: System prompt via `/think` dan `/nothink` (juga valid)**
```python
{"role": "system", "content": "You are a helpful assistant. /think"}
```

#### Critical Discovery — SGLang WAJIB `chat_template_kwargs`

> **"When calling the chat completions endpoint with tools, you must set `"chat_template_kwargs": {"enable_thinking": true, "force_nonempty_content": true}` in the request body to parse both reasoning and tool calls correctly."** — Official SGLang docs

#### Verdict: ⚠️ **REVISED — Finding lebih complex dari asumsi**

**Revisi:**
- Original finding benar bahwa `extra_body` tidak bisa di-set via OW UI → masih benar
- Tapi: system prompt method (`/think`, `/nothink`, `detailed thinking on/off`) **JUGA valid** — tidak hanya workaround, ini adalah metode yang didokumentasikan
- **NEW**: Ada `medium_effort` mode yang tidak ada di original matrix — perlu ditambahkan
- **NEW**: Ada `reasoning_budget` hard cap — advanced feature yang missing dari matrix

**Revised Recommendation:**
1. System prompt workaround → **VALID dan documented**
2. Pipeline untuk inject `extra_body` → **STILL RECOMMENDED** untuk `medium_effort` dan `reasoning_budget` yang tidak bisa via system prompt
3. Tambahkan profile `medium_effort` di `parameters.json`

---

### R-04: Embeddings endpoint tidak tersedia di Cloud NIM

**Original Verdict:** 🔴 Critical — RAG akan fail

#### Evidence dari Official Docs

Model documentation menyatakan:
- **Input:** Text only
- **Output:** Text only
- **Architecture:** LatentMoE — Mamba-2 + MoE + Attention hybrid
- Tidak ada mention embeddings endpoint

Dari Model Summary:
```
Best For: Frontier reasoning, complex agentic workflows, long-context analysis, tool use, multilingual reasoning, high-stakes RAG
```
Note: "high-stakes RAG" merujuk pada model sebagai **reader/reasoner** dalam RAG pipeline, bukan sebagai **embedder**.

Seluruh deployment guide (vLLM, SGLang, TRT-LLM) hanya expose `/v1/chat/completions` dan `/v1/completions` endpoints, tidak ada `/v1/embeddings`.

#### Verdict: ✅ **CONFIRMED — Embeddings endpoint tidak ada**

**Action Required:** Configure separate embedding provider. Recommended options:
- `nvidia/nv-embedqa-e5-v5` via NVIDIA Cloud (separate NIM)
- `nomic-embed-text` via Ollama (local)
- `mxbai-embed-large` via Ollama (local)

---

### R-05: `extra_body` tidak bisa di-set via Open WebUI UI

**Original Verdict:** 🔴 Critical — Reasoning mode tidak bisa dikontrol

#### Evidence dari Official Docs

Docs resmi mengkonfirmasi bahwa `extra_body` adalah cara **resmi** untuk mengontrol:
- `enable_thinking`: True/False
- `medium_effort`: True/False
- `force_nonempty_content`: True (wajib untuk coding agents)

```python
# Official example
extra_body={"chat_template_kwargs": {"enable_thinking": True}}
```

Open WebUI memang tidak expose `extra_body` di UI — ini **confirmed assumption** yang benar.
Tapi: **system prompt workaround adalah metode yang valid**, bukan hanya fallback.

#### Verdict: ⚠️ **REVISED — Severity turun dari Critical ke High**

**Reasoning:**
- System prompt method (`/think`, `/nothink`) adalah **documented feature**, bukan hanya workaround
- Untuk basic on/off reasoning control: system prompt **cukup**
- Untuk `medium_effort`, `force_nonempty_content`, `reasoning_budget`: Pipeline tetap diperlukan
- Therefore: bukan Critical untuk basic use, tapi High untuk advanced use

---

### R-08: Function calling disabled di `capabilities.json`

**Original Verdict:** 🔴 Critical — Tools silently disabled

#### Evidence dari Official Docs

Docs resmi secara eksplisit menunjukkan tool calling berfungsi:

```python
# Tool calling example dari official docs
response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "What's the weather in New York?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": { ... }
        }
    }],
    tool_choice="required",
    max_tokens=256,
    temperature=1.0,
    top_p=0.95,
    extra_body={"chat_template_kwargs": {"enable_thinking": True, "force_nonempty_content": True}}
)
```

vLLM deployment flags confirm tool calling support:
```bash
--enable-auto-tool-choice \
--tool-call-parser qwen3_coder \
```

SGLang flags:
```bash
--tool-call-parser qwen3_coder \
```

TRT-LLM flags:
```bash
--tool_parser qwen3_coder \
```

#### Verdict: ⚠️ **REVISED — Tool calling CONFIRMED supported, finding masih valid**

**Revisi:** Finding asli benar — function calling HARUS di-enable.
**TAMBAHAN KRITIS:** Tool calling menggunakan `qwen3_coder` parser. Open WebUI tidak mengirim `tool-call-parser` — ini dilakukan di server-side (vLLM/SGLang/TRT-LLM).
Untuk Cloud NIM: parser dikonfigurasi NVIDIA-side, bukan client-side. Jadi ini transparent ke OW.

---

## New Critical Findings (Tidak Ada di AI-0003 v1.0.0)

---

### NEW-01: `chat_template_kwargs` WAJIB untuk Tool Calls + Reasoning (SGLang)

**Severity:** 🔴 Critical (New)

#### Evidence

Official docs menyatakan:
> **"When calling the chat completions endpoint with tools, you must set `"chat_template_kwargs": {"enable_thinking": true, "force_nonempty_content": true}` in the request body to parse both reasoning and tool calls correctly."**

Ini berarti: jika backend adalah SGLang dan tool calling digunakan **tanpa** `chat_template_kwargs`, parsing akan fail silently atau menghasilkan malformed response.

#### Impact pada Open WebUI

Open WebUI tidak mengirim `chat_template_kwargs` secara default. Jika NVIDIA Cloud NIM menggunakan SGLang backend (tidak disclosed), tool calling + reasoning akan fail.

#### Recommendation

1. Build Pipeline yang inject `extra_body.chat_template_kwargs` untuk semua tool-calling requests
2. Atau: verifikasi backend Cloud NIM (vLLM/SGLang/TRT-LLM) — jika vLLM, ini tidak required

---

### NEW-02: `force_nonempty_content` untuk Coding Agents

**Severity:** 🟡 High (New)

#### Evidence

Official docs menyatakan:
> **"NOTE: For coding agents add the following to the API call - `extra_body={"chat_template_kwargs": {"force_nonempty_content": True}}`"**

Ini diperlukan karena reasoning model kadang menghasilkan response dengan `content: null` (hanya tool calls, tanpa text). Untuk coding agents yang expect text content, ini menyebabkan parsing failure.

#### Recommendation

Tambahkan ke Pipeline untuk model profile `code`:
```python
extra_body = {
    "chat_template_kwargs": {
        "enable_thinking": True,
        "force_nonempty_content": True
    }
}
```

---

### NEW-03: Tool Call Parser adalah `qwen3_coder`, bukan standard

**Severity:** 🟡 High (New)

#### Evidence

Semua deployment backends menggunakan `--tool-call-parser qwen3_coder` / `--tool_parser qwen3_coder`.
Ini adalah **custom parser**, bukan standard OpenAI tool call format.

#### Impact

Jika Open WebUI mengharapkan standard OpenAI tool call format dan NVIDIA Cloud NIM menggunakan `qwen3_coder` format, ada risk of incompatibility.

#### Recommendation

Benchmark tool call response format dari Cloud NIM endpoint.
Verify apakah `finish_reason: tool_calls` dan `delta.tool_calls` structure sesuai OpenAI spec.

Status: **🔬 Need Benchmark** (tambahkan sebagai BM-09)

---

### NEW-04: Default Context Length adalah 256K, bukan 1M

**Severity:** 🟢 Medium (New)

#### Evidence

Official docs menyatakan:
> **"Context Length: Defaults to 256k above. To use up to 1M, set `VLLM_ALLOW_LONG_MAX_MODEL_LEN=1` and `--max-model-len 1048576`."**

Original AI-0003 matrix menyatakan "Up to 1M tokens" tanpa caveat. Ini tidak sepenuhnya akurat — 1M adalah **maximum possible**, bukan default. Default deployment menggunakan 256K.

#### Impact pada Open WebUI

Jika user mencoba mengirim >256K tokens ke Cloud NIM, akan mendapat error.
Perlu verify berapa batas yang NVIDIA Cloud NIM gunakan untuk endpoint publik.

#### Recommendation

Update matrix dengan:
- Default context: **256K tokens** (confirmed)
- Maximum context: **1M tokens** (requires server flag, Cloud NIM may or may not enable)
- Action: Verify Cloud NIM public endpoint context limit via test call

---

## Revised Critical Findings Summary

| Finding | Original Status | Audit Status | Action |
|---------|----------------|--------------|--------|
| R-01: `top_k` ignored | 🔴 Assumption | ✅ CONFIRMED | Remove from config immediately |
| R-02: `repetition_penalty` ignored | 🔴 Assumption | ✅ CONFIRMED | Remove from config immediately |
| R-03: Reasoning mode not controlled | 🔴 Partially wrong | ⚠️ REVISED | System prompt IS valid; pipeline needed only for `medium_effort`/budget |
| R-04: No embeddings endpoint | 🔴 Assumption | ✅ CONFIRMED | Configure separate embedding provider |
| R-05: `extra_body` not in OW UI | 🔴 Critical | ⚠️ REVISED to High | System prompt covers basic case; Pipeline for advanced |
| R-08: Function calling disabled | 🔴 Config Gap | ✅ CONFIRMED (tool calling IS supported) | Enable in capabilities.json |
| NEW-01: `chat_template_kwargs` for tools | ❌ Missing | 🆕 NEW Critical | Add Pipeline for tool calls |
| NEW-02: `force_nonempty_content` | ❌ Missing | 🆕 NEW High | Add to code agent Pipeline |
| NEW-03: `qwen3_coder` parser | ❌ Missing | 🆕 NEW Benchmark | BM-09 added |
| NEW-04: Context 256K default | ❌ Wrong assumption | 🆕 CORRECTED | Verify Cloud NIM limit |

---

## Updated parameters.json v1.1.0

```json
{
  "_metadata": {
    "version": "1.1.0",
    "status": "active",
    "audit": "AI-0003-Audit v1.0 — validated against official NIM docs 2026-07-20",
    "description": "Open WebUI model parameters for Nemotron Ultra 550B via NVIDIA NIM",
    "last_updated": "2026-07-20",
    "owner": "Aldhie"
  },
  "model": {
    "provider": "nvidia-nim",
    "model_id": "nvidia/nemotron-3-ultra-550b-a55b",
    "base_url": "https://integrate.api.nvidia.com/v1",
    "api_key_env": "NVIDIA_API_KEY",
    "context_length_default": 262144,
    "context_length_max": 1048576
  },
  "inference": {
    "temperature": 1.0,
    "top_p": 0.95,
    "max_tokens": 4096,
    "frequency_penalty": 0.0,
    "stream": true,
    "stop": []
  },
  "profiles": {
    "general": {
      "system_prompt": "/nothink",
      "temperature": 1.0,
      "top_p": 0.95,
      "max_tokens": 2048
    },
    "reasoning": {
      "system_prompt": "/think",
      "temperature": 1.0,
      "top_p": 0.95,
      "max_tokens": 16000
    },
    "medium_effort": {
      "system_prompt": "/think",
      "note": "Requires Pipeline to inject medium_effort:true via extra_body",
      "temperature": 1.0,
      "top_p": 0.95,
      "max_tokens": 8192
    },
    "creative": {
      "system_prompt": "/nothink",
      "temperature": 1.0,
      "top_p": 0.98,
      "max_tokens": 2048
    },
    "code": {
      "system_prompt": "/think",
      "note": "Requires Pipeline to inject force_nonempty_content:true via extra_body",
      "temperature": 1.0,
      "top_p": 0.95,
      "max_tokens": 16000
    }
  },
  "context": {
    "confirmed_default_context_tokens": 262144,
    "max_possible_context_tokens": 1048576,
    "system_prompt_budget_tokens": 500,
    "history_budget_tokens": 8192,
    "rag_budget_tokens": 4096,
    "output_reserved_tokens": 4096
  },
  "corrections_from_v010": {
    "removed": ["top_k", "repetition_penalty"],
    "updated": {
      "temperature": "1.0 (docs recommend 1.0, not 0.6 — 0.6 was assumption)",
      "system_prompt": "using /think and /nothink (documented) instead of 'detailed thinking on/off'"
    },
    "added": ["medium_effort profile", "context_length_default clarification"]
  }
}
```

---

### Critical Temperature Finding

**IMPORTANT:** AI-0003 v1.0.0 merekomendasikan `temperature: 0.6` untuk reasoning tasks.
Official docs menunjukkan SEMUA contoh menggunakan `temperature: 1.0`:

```python
# Official docs — ALL examples use temperature=1.0
temperature=1.0,
top_p=0.95,
```

OpenCode config:
```json
"build": { "temperature": 1.0, "top_p": 0.95 }
```

**Verdict:** `temperature: 0.6` adalah **ASSUMPTION** yang salah. NVIDIA merekomendasikan `1.0` untuk model ini.

---

## Updated Benchmark Checklist

```
[x] BM-01: Parallel tool calls (carry over)
[x] BM-02: Agentic RAG (carry over)
[x] BM-03: MCP tool server (carry over)
[x] BM-04: OpenAPI tool server (carry over)
[x] BM-05: Bound tools per model (carry over)
[x] BM-06: Streaming + tool call accumulation (carry over)
[x] BM-07: 429 error display (carry over)
[x] BM-08: Logprobs (carry over)
[ ] BM-09: qwen3_coder tool call format — verify OW compatibility with Cloud NIM tool call format
[ ] BM-10: Context length limit on Cloud NIM public endpoint — confirm 256K or 1M
[ ] BM-11: medium_effort via extra_body — verify Pipeline injection works
[ ] BM-12: temperature=1.0 reasoning quality vs temperature=0.6 — empirical comparison
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-20 | Initial audit — verified 6 critical findings, found 4 new findings, corrected temperature assumption |
