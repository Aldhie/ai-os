# AI-0003 — Open WebUI Compatibility

| Field | Value |
|-------|-------|
| **Title** | Open WebUI Compatibility and Configuration Guide |
| **Purpose** | Document how Open WebUI integrates with NVIDIA NIM and AI-OS runtime |
| **Scope** | Open WebUI version compatibility, model connection, system prompt injection, UI configuration |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie / Global Telko Informatika |
| **Created** | 2026-07-19 |
| **Dependencies** | AI-0002-NVIDIA-NIM-API.md |
| **References** | https://docs.openwebui.com |

---

## 1. Open WebUI Version Requirements

| Requirement | Value |
|-------------|-------|
| Minimum Version | 0.4.x |
| Recommended Version | Latest stable |
| Deployment | Docker (self-hosted) or cloud |
| Node.js (build) | 18+ |
| Database | SQLite (default) or PostgreSQL |

## 2. Model Connection Setup

### Step 1: Add OpenAI-compatible connection

1. Go to **Settings → Connections → OpenAI API**
2. Set **Base URL**: `https://integrate.api.nvidia.com/v1`
3. Set **API Key**: `$NVIDIA_API_KEY`
4. Save and verify connection

### Step 2: Select Model

1. Go to **Models** and select `nvidia/nemotron-3-ultra-550b`
2. Assign the system prompt from `prompts/nemotron-ultra/system.txt`

## 3. System Prompt Injection

Open WebUI supports system prompt injection at three levels:

| Level | Scope | Priority |
|-------|-------|----------|
| Global system prompt | All conversations | Lowest |
| Model-level system prompt | Per model | Medium |
| Conversation system prompt | Per chat session | Highest |

For AI-OS, use **model-level system prompt** as the primary injection point.

## 4. Supported Features

| Feature | Supported | Notes |
|---------|-----------|-------|
| Streaming | ✅ | SSE via OpenAI format |
| Multi-turn conversation | ✅ | Native |
| System prompt | ✅ | Model-level and global |
| File upload / RAG | ✅ | Requires embedding model |
| Function calling | 🔄 | Depends on NIM support |
| Image input | ❓ | Verify with Nemotron 550B |
| Voice input | ✅ | Requires Whisper integration |

## 5. Parameters Configuration

See `configs/openwebui/parameters.json` for the full parameter set.

Key parameters to tune in Open WebUI model settings:

- `temperature`
- `top_p`
- `max_tokens`
- `system_prompt`
- `context_length`

## 6. Known Issues

- Some Open WebUI versions do not pass `frequency_penalty` to external APIs — verify before deploying.
- Streaming may timeout on very long responses — configure `WEBUI_REQUEST_TIMEOUT` accordingly.

---

## TODO

- [ ] Test Open WebUI Docker deployment with NIM endpoint
- [ ] Validate system prompt injection at model level
- [ ] Configure RAG with embedding model for knowledge base
- [ ] Document WEBUI_REQUEST_TIMEOUT recommendation
- [ ] Test function calling if NIM supports it
