# AI-0002 — NVIDIA NIM API Integration

| Field | Value |
|-------|-------|
| **Title** | NVIDIA NIM API Integration Guide |
| **Purpose** | Document API endpoints, authentication, and integration patterns for NVIDIA Cloud NIM |
| **Scope** | REST API, authentication, request/response schema, error handling, rate limits |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie / Global Telko Informatika |
| **Created** | 2026-07-19 |
| **Dependencies** | AI-0001-Nemotron-Engineering-Spec.md |
| **References** | https://docs.api.nvidia.com, OpenAI API specification |

---

## 1. Base URL

```
https://integrate.api.nvidia.com/v1
```

## 2. Authentication

```http
Authorization: Bearer $NVIDIA_API_KEY
```

Store the key in environment variable `NVIDIA_API_KEY`. Never commit to version control.

## 3. Chat Completions Endpoint

### Request

```http
POST /chat/completions
Content-Type: application/json
Authorization: Bearer $NVIDIA_API_KEY
```

```json
{
  "model": "nvidia/nemotron-3-ultra-550b",
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
  "temperature": 0.2,
  "top_p": 0.9,
  "max_tokens": 4096,
  "stream": true
}
```

### Response (non-stream)

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1720000000,
  "model": "nvidia/nemotron-3-ultra-550b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 512,
    "completion_tokens": 256,
    "total_tokens": 768
  }
}
```

## 4. Streaming

Set `"stream": true` to receive Server-Sent Events (SSE). Each chunk follows OpenAI streaming format:

```
data: {"choices":[{"delta":{"content":"..."}}]}
```

Terminated by:

```
data: [DONE]
```

## 5. Error Codes

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Bad request (malformed JSON, invalid params) | Fix request schema |
| 401 | Unauthorized (invalid API key) | Check NVIDIA_API_KEY |
| 429 | Rate limit exceeded | Implement exponential backoff |
| 500 | Internal server error | Retry with backoff |
| 503 | Service unavailable | Check NVIDIA status page |

## 6. Rate Limits (Free Tier)

| Limit | Value |
|-------|-------|
| Requests per minute | TBD |
| Tokens per minute | TBD |
| Tokens per day | TBD |

> **See AI-0005-FreeTier-Strategy.md** for optimization strategies.

## 7. Open WebUI Integration

Open WebUI connects to NIM via its **OpenAI-compatible API** settings:

- Base URL: `https://integrate.api.nvidia.com/v1`
- API Key: `$NVIDIA_API_KEY`
- Model ID: `nvidia/nemotron-3-ultra-550b`

---

## TODO

- [ ] Confirm exact model ID from NVIDIA NIM catalog
- [ ] Document actual rate limits for free and paid tiers
- [ ] Test streaming with Open WebUI
- [ ] Implement retry wrapper for 429 and 503 errors
- [ ] Document function calling schema if supported
