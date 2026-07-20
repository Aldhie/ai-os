# Open WebUI Deployment

> **Version**: 1.0.0
> **Spec Ref**: AI-0003-OpenWebUI-Compatibility.md

---

## Step 1 — Deploy Open WebUI

```bash
docker run -d \
  --name open-webui \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --add-host=host.docker.internal:host-gateway \
  ghcr.io/open-webui/open-webui:main
```

Access at: `http://localhost:3000`

---

## Step 2 — Configure NVIDIA NIM Connection

1. Go to **Admin Panel → Settings → Connections**
2. Add OpenAI-compatible connection:
   - **URL**: `https://integrate.api.nvidia.com/v1`
   - **API Key**: your NVIDIA NIM API key
   - **Model**: `nvidia/nemotron-3-ultra-550b-a55b`
3. Click **Verify Connection**
4. Confirm model appears in model list

Ref: AI-0002-NVIDIA-NIM-API.md £2

---

## Step 3 — Import Model Configuration

1. Go to **Admin Panel → Models**
2. Click **Import**
3. Upload `runtime/openwebui/exports/model.json`
4. Verify model name: **Nemotron Ultra 550B — AI-OS**

---

## Step 4 — Configure System Prompt

1. Open the imported model in model editor
2. Paste content from `runtime/openwebui/model/system_prompt_v1.md` (code block content only)
3. Save

---

## Step 5 — Set Parameters

Apply the following in **Model Parameters**:

| Parameter | Value |
|-----------|-------|
| Temperature | 1.0 |
| Top P | 0.95 |
| Max Tokens | 4096 |
| Presence Penalty | 0.0 |
| Frequency Penalty | 0.0 |

**Do NOT set**: `top_k`, `repetition_penalty`, `thinking` (top-level), `stop: [</s>]`

Ref: AI-0003-OpenWebUI-Compatibility.md §4

---

## Step 6 — Configure Knowledge (RAG)

1. Go to **Workspace → Knowledge**
2. Create collection: **AI-OS Engineering Specs**
3. Upload all files from `docs/00_ENGINEERING/`
4. Assign collection to your model

---

## Step 7 — Verify Deployment

Test with these prompts:

```
# Basic connectivity
Hello. What model are you?

# Thinking mode test  
/think Explain the architecture of Nemotron Ultra 550B.

# Memory test
My preferred programming language is Python. Remember this.
[new session]
What language should I use for this script?

# RAG test
Based on the engineering specs, what are the forbidden parameters for this model?
```

Expected results per benchmark/tests/ test cases.
