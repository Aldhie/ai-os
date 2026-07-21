# AI-OS · Quick Start Guide

**Version**: 2.0.0  
**Sprint**: C  
**Target**: Open WebUI + NVIDIA Cloud NIM Free Tier

This guide deploys the complete AI-OS runtime into a running Open WebUI instance in under 15 minutes.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Open WebUI running | v0.4.x or later |
| NVIDIA API key | Get free at [build.nvidia.com](https://build.nvidia.com) |
| Admin access to Open WebUI | Required for model and filter configuration |

---

## Step 1 — Add NIM Connection

1. Open WebUI → **Admin Panel** → **Settings** → **Connections**
2. Click **+ Add Connection**
3. Fill in:
   - **URL**: `https://integrate.api.nvidia.com/v1`
   - **API Key**: your NVIDIA API key
4. Click **Verify** — confirm the connection shows green
5. Save

---

## Step 2 — Create the Model

1. Open WebUI → **Admin Panel** → **Models** → **+ Add Model**
2. Configure:
   - **Model ID**: `ai-os-nemotron-ultra`
   - **Name**: `AI-OS · Nemotron Ultra`
   - **Base Model**: `nvidia/nemotron-3-ultra-550b` (from NIM connection)
3. In **System Prompt**: paste the full contents of `compiled_prompt_v2.md`
4. In **Parameters**, set:
   - Temperature: `0.7`
   - Max Tokens: `4096`
5. Save

---

## Step 3 — Install Filters (in order)

For each filter file below, go to **Admin Panel** → **Functions** → **+ New Function** → type: **Filter**:

| Order | File | Direction |
|-------|------|-----------|
| 1 | `filters/rpm_guard.py` | Inlet |
| 2 | `filters/credential_scrub.py` | Inlet |
| 3 | `filters/profile_selector.py` | Inlet |
| 4 | `filters/context_budget_enforcer.py` | Inlet |
| 5 | `filters/response_quality_monitor.py` | Outlet |

After installing each filter:
1. **Enable** the filter (toggle to ON)
2. **Assign** it to the `AI-OS · Nemotron Ultra` model

---

## Step 4 — Verify NIM Parameters

Open WebUI sends parameters to NIM via OpenAI-compatible API. For extended thinking, the NIM endpoint requires:

```json
{
  "extra_body": {
    "chat_template_kwargs": { "enable_thinking": true },
    "reasoning_budget": 4096
  }
}
```

This is injected automatically by `profile_selector.py`. No manual action required.

---

## Step 5 — Send Verification Message

Send this exact message to the model:

```
What is the CAP theorem?
```

**Expected result:**
- Response begins with a direct answer (not "Sure!" or "I will...")
- No filler affirmations
- Response is under 900 tokens
- Extended thinking block visible (if UI shows thinking)

If the response fails any of these, check that `compiled_prompt_v2.md` was pasted correctly as the System Prompt.

---

## Step 6 — Run Benchmark (Optional)

```bash
pip install requests
cd runtime/openwebui/benchmark/
python harness.py \
  --base-url http://localhost:3000 \
  --api-key YOUR_OPENWEBUI_API_KEY \
  --model-id ai-os-nemotron-ultra
```

Passing score: ≥ 70. A score < 70 indicates a configuration issue.
