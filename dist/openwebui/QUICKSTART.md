# AI-OS · Open WebUI Quick Start Guide

**Version**: 2.1.0  
**Sprint**: C  
**Time to deploy**: ~15 minutes

---

## Prerequisites

| Requirement | Details |
|-------------|--------|
| Open WebUI | v0.4.x or later |
| NVIDIA NIM API key | Free Tier at [build.nvidia.com](https://build.nvidia.com) |
| Admin access | Open WebUI Admin Panel |

---

## Step 1 — Add NIM as a Connection

1. Open WebUI → **Admin Panel** → **Settings** → **Connections**
2. Add an OpenAI-compatible connection:
   - **Name**: `NVIDIA NIM`
   - **Base URL**: `https://integrate.api.nvidia.com/v1`
   - **API Key**: your `nvapi-...` key
3. Save and verify connection

---

## Step 2 — Install Filters (in order)

For each file in `dist/openwebui/filters/`, in this order:

1. Open WebUI → **Admin Panel** → **Functions** → **+ New Function**
2. Set type: **Filter**
3. Paste the file contents
4. Save and **Enable**

| Order | File | 
|-------|------|
| 1 | `filters/rpm_guard.py` |
| 2 | `filters/credential_scrub.py` |
| 3 | `filters/profile_selector.py` |
| 4 | `filters/context_budget_enforcer.py` |
| 5 | `filters/response_quality_monitor.py` |

---

## Step 3 — Create the Model

1. Open WebUI → **Admin Panel** → **Models** → **+ New Model**
2. Configure:
   - **Model ID**: `ai-os-nemotron-ultra`
   - **Display Name**: `AI-OS · Nemotron Ultra`
   - **Base Model**: select `nvidia/nemotron-ultra-253b-v1` from the NIM connection
   - **System Prompt**: paste the entire contents of `compiled_prompt_v2.md`
3. Under **Parameters**, set:
   - **Temperature**: `0.6`
   - **Top P**: `0.95`
   - **Max Tokens**: `4096`
4. Under **Filters**, assign all 5 filters installed in Step 2
5. Save

---

## Step 4 — Enable Capabilities

In the model settings, enable:
- [x] Web Search
- [x] RAG / Knowledge
- [x] Memory
- [ ] Image input (leave **disabled** — model is text-only)
- [ ] Arena mode (leave **disabled** — wastes 2× RPM)

---

## Step 5 — Verify Deployment

Send this test message to the model:

```
What is the CAP theorem?
```

**Expected behaviour:**
- Response begins with the direct answer (not "The CAP theorem states that..." preamble)
- No filler affirmations ("Sure!", "Great!", etc.)
- Response is 200–400 words
- No trailing "Is there anything else I can help with?"

**Verify RPM guard is active** by sending 33 messages in rapid succession — the 33rd should be blocked with:
```
[AI-OS RPM Guard] NIM Free Tier limit reached (32 RPM). Please wait approximately N seconds.
```

---

## Step 6 — Run Benchmark (Optional but Recommended)

```bash
pip install requests
python runtime/openwebui/benchmark/harness.py \
  --base-url http://localhost:3000 \
  --api-key YOUR_OPENWEBUI_API_KEY \
  --model-id ai-os-nemotron-ultra
```

Expected result: **score ≥ 70** (PASS).

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| 429 from NIM | RPM Guard not installed | Install `rpm_guard.py` as priority-1 filter |
| Responses start with "Sure!" | System prompt not applied | Re-paste `compiled_prompt_v2.md` into model System Prompt |
| Context overflow errors | Context Budget Enforcer not active | Verify `context_budget_enforcer.py` is enabled |
| Very high latency (>30s) | Context approaching 65K tokens | Normal on Free Tier; enforcer will truncate next turn |
| Model responds as generic assistant | Wrong base model selected | Select `nvidia/nemotron-ultra-253b-v1` specifically |
