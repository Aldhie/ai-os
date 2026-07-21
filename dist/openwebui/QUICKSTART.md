# AI-OS · Open WebUI Quick Start Guide

**Version**: 1.0.0  
**Model**: NVIDIA Nemotron-3-Ultra-550B-A55B  
**Provider**: NVIDIA Cloud NIM  
**Target**: Open WebUI 0.6.x+

---

## Prerequisites

- Open WebUI running (self-hosted or cloud)
- NVIDIA Cloud NIM API key (`nvapi-...`) — [get one at build.nvidia.com](https://build.nvidia.com)
- Admin access to Open WebUI

---

## Step 1 — Add NVIDIA NIM Connection

1. Open WebUI → **Admin Panel** → **Connections**
2. Add OpenAI-compatible connection:
   - **Base URL**: `https://integrate.api.nvidia.com/v1`
   - **API Key**: `nvapi-YOUR_KEY_HERE`
3. Save and verify connection shows green.

---

## Step 2 — Create the Model

1. **Admin Panel** → **Models** → **+ Add Model**
2. Set:
   - **Model ID**: `ai-os-nemotron-ultra`
   - **Base Model**: `nvidia/nemotron-3-ultra-550b-a55b`
   - **Name**: `AI-OS · Nemotron Ultra`
3. In **System Prompt**, paste the full contents of:
   `runtime/openwebui/model/compiled_prompt_v1.md`
   (remove the HTML comment header before pasting)
4. Set parameters:
   - Temperature: `0.7`
   - Top P: `0.95`
   - Max Tokens: `4096`
   - Frequency Penalty: `0.1`
5. Save.

---

## Step 3 — Enable Thinking (Reasoning Budget)

Open WebUI passes `extra_body` to OpenAI-compatible providers.  
In the model's **Advanced Parameters**:

```json
{
  "extra_body": {
    "chat_template_kwargs": { "enable_thinking": true },
    "reasoning_budget": 4096
  }
}
```

If your Open WebUI version does not support `extra_body` in the UI, apply it via the Open WebUI API or a Filter.

---

## Step 4 — Import Parameter Profiles

For task-optimised parameters, use the profiles in `dist/openwebui/parameter_profiles/` or `runtime/openwebui/profiles/`.  
Switch profiles manually by adjusting model parameters, or automate via the Profile Selector Filter (`runtime/openwebui/config/filters.json`).

---

## Step 5 — Verify

Send a test message: **"Explain the architecture of a distributed rate limiter."**

Expected behaviour:
- Response follows: Reasoning → Requirements → Constraints → Components → Interfaces → Failure Modes → Trade-offs
- No filler affirmations
- Answer comes first, not preamble
- Response length ≤ 2500 tokens

---

## Free Tier Limits

| Limit | Value | Mitigation |
|-------|-------|------------|
| RPM | 32 | Batch all tools before single NIM call |
| Context ceiling (recommended) | 64K tokens | Context Budget Enforcer Filter |
| Concurrent requests | Shared infra | RPM Guard Filter rejects >32/min |

---

## Files Reference

| File | Purpose |
|------|---------|
| `runtime/openwebui/model/compiled_prompt_v1.md` | System prompt — paste into model |
| `runtime/openwebui/config/model.json` | Full model config |
| `runtime/openwebui/config/parameters.json` | Default + override parameters |
| `runtime/openwebui/config/memory.json` | Memory orchestration policy |
| `runtime/openwebui/config/knowledge.json` | Knowledge/RAG policy |
| `runtime/openwebui/config/tools.json` | Tool routing policy |
| `runtime/openwebui/config/workflow.json` | 9-stage processing pipeline |
| `runtime/openwebui/config/filters.json` | Filter chain spec |
| `runtime/openwebui/config/capabilities.json` | Verified capability flags |
| `runtime/openwebui/config/profiles.json` | Profile index |
| `runtime/openwebui/profiles/*.json` | 7 task-specific profiles |
| `runtime/openwebui/benchmark/suite.json` | Benchmark suite |
