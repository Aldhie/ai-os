# AI-0003 — Open WebUI Compatibility

| Field | Value |
|-------|-------|
| **Title** | Open WebUI Compatibility with NVIDIA NIM |
| **Purpose** | Document how to configure Open WebUI to connect with NVIDIA NIM and Nemotron Ultra |
| **Scope** | Open WebUI setup, model connection, feature compatibility, known issues |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | AI-0001, AI-0002 |
| **References** | [Open WebUI Docs](https://docs.openwebui.com/), [Open WebUI GitHub](https://github.com/open-webui/open-webui) |

---

## 1. Open WebUI Overview

Open WebUI is a self-hosted, extensible web interface for interacting with LLMs. It supports OpenAI-compatible APIs, making it fully compatible with NVIDIA NIM.

| Property | Value |
|----------|-------|
| Minimum Version | 0.4.x |
| Deployment | Docker / Local / Cloud |
| API Protocol | OpenAI-compatible |
| Auth | API Key via environment variable |

---

## 2. Connection Configuration

In Open WebUI Admin Panel:

```
Settings → Connections → OpenAI API
  URL: https://integrate.api.nvidia.com/v1
  Key: nvapi-xxxxxxxxxxxxxxxxxxxx
```

Or via environment variable:

```bash
OPENAI_API_BASE_URL=https://integrate.api.nvidia.com/v1
OPENAI_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxx
```

---

## 3. Feature Compatibility Matrix

| Feature | Open WebUI | NIM | Compatible |
|---------|------------|-----|------------|
| Chat completions | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ |
| System prompts | ✅ | ✅ | ✅ |
| Tool/function calling | ✅ | ✅ | ✅ |
| RAG (document Q&A) | ✅ | N/A | ✅ |
| Image generation | ✅ | ❌ | ❌ |
| Voice input | ✅ | ❌ | ❌ |
| Vision (image input) | ✅ | ❌ | ❌ |
| Web search | ✅ | N/A | ✅ |
| Extended thinking | ❌ native | ✅ | ⚠️ Partial |

---

## 4. Model Selection in Open WebUI

After connection, select:

```
nvidia/llama-3.1-nemotron-ultra-253b-v1
```

This model ID must be used exactly as listed in the NVIDIA NIM model catalog.

---

## 5. Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| Extended thinking tokens visible in output | Low | Strip `<think>` tags in filter |
| Rate limit 429 shows as generic error | Medium | Monitor API logs |
| Long system prompts may reduce response quality | Medium | Optimize prompt, see SystemPrompt.md |

---

## TODO

- [ ] Test Docker deployment on local machine
- [ ] Document Open WebUI filter setup for thinking tokens
- [ ] Test RAG pipeline with Nemotron Ultra
- [ ] Create automated connection test script
- [ ] Document Open WebUI version upgrade procedure
