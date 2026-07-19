# AI-0002: NVIDIA NIM API Integration Specification

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-0002 |
| **Title** | NVIDIA NIM API Integration Specification |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines how the AI OS connects to NVIDIA Cloud NIM for inference. It covers authentication, endpoint configuration, request/response schema, error handling, and rate limit management.

---

## Scope

- NIM API authentication and credentials management
- OpenAI-compatible API interface
- Request parameters and schema
- Error codes and retry strategy
- Rate limiting and quota management

---

## Dependencies

- `AI-0001-Nemotron-Engineering-Spec.md` — model specification
- `AI-0005-FreeTier-Strategy.md` — quota and cost management
- `configs/openwebui/parameters.json` — runtime parameter configuration

---

## References

- [NVIDIA NIM API Reference](https://docs.nvidia.com/nim/)
- [NVIDIA Build Platform](https://build.nvidia.com/)
- [OpenAI API Compatibility](https://platform.openai.com/docs/api-reference)

---

## API Configuration

### Base URL

```
https://integrate.api.nvidia.com/v1
```

### Authentication

```http
Authorization: Bearer <NVIDIA_API_KEY>
```

> **Security Note:** Never commit API keys to this repository. Store credentials in environment variables or a secret manager.

### Endpoint

```
POST /chat/completions
```

---

## Request Schema

```json
{
  "model": "nvidia/nemotron-super-49b-v1",
  "messages": [
    {
      "role": "system",
      "content": "<system_prompt>"
    },
    {
      "role": "user",
      "content": "<user_message>"
    }
  ],
  "temperature": 0.6,
  "top_p": 0.95,
  "max_tokens": 4096,
  "stream": true
}
```

---

## Response Schema

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "nvidia/nemotron-super-49b-v1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "<response>"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 200,
    "total_tokens": 300
  }
}
```

---

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Bad Request | Fix request schema |
| 401 | Unauthorized | Check API key |
| 429 | Rate Limited | Backoff and retry |
| 500 | Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | Retry after delay |

### Retry Strategy

```
Attempt 1: immediate
Attempt 2: +2s
Attempt 3: +4s
Attempt 4: +8s
Max attempts: 4
```

---

## Open WebUI Integration

Open WebUI connects to NIM via its **OpenAI-compatible API** configuration:

1. Navigate to **Settings > Connections**
2. Add new connection:
   - **Base URL:** `https://integrate.api.nvidia.com/v1`
   - **API Key:** `<NVIDIA_API_KEY>`
3. Select model: `nvidia/nemotron-3-ultra-550b` (verify exact model slug)

---

## TODO

- [ ] Confirm exact model slug for Nemotron 3 Ultra 550B on NIM
- [ ] Document streaming SSE response format
- [ ] Add token counting guidance for context management
- [ ] Document function calling / tool use schema on NIM
- [ ] Test and document connection setup steps in Open WebUI
