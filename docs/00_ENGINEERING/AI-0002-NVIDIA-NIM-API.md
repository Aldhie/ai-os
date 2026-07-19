# AI-0002 — NVIDIA NIM API Integration

| Field | Value |
|-------|-------|
| **Title** | NVIDIA NIM API Integration |
| **Document ID** | AI-0002 |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | @Aldhie |
| **Created** | 2026-07-19 |
| **Updated** | 2026-07-19 |
| **Dependencies** | AI-0001, AI-0003 |

---

## Purpose

Documents how AI-OS integrates with NVIDIA Cloud NIM via the OpenAI-compatible REST API. Covers authentication, endpoint configuration, request/response structure, error handling, and rate limit management.

---

## Scope

- API base URL and authentication
- Chat completions endpoint usage
- Streaming vs non-streaming
- Error codes and retry strategy
- Rate limit tracking
- Model listing

---

## API Configuration

| Property | Value |
|----------|-------|
| **Base URL** | `https://integrate.api.nvidia.com/v1` |
| **Auth Header** | `Authorization: Bearer {NVIDIA_API_KEY}` |
| **API Compatibility** | OpenAI SDK v1.x compatible |
| **Protocol** | HTTPS |
| **Format** | JSON |

---

## Chat Completions Endpoint

```
POST /chat/completions
Content-Type: application/json
Authorization: Bearer {NVIDIA_API_KEY}
```

### Request Schema

```json
{
  "model": "nvidia/nemotron-3-ultra-550b-instruct",
  "messages": [
    {"role": "system", "content": "<system_prompt>"},
    {"role": "user", "content": "<user_message>"}
  ],
  "temperature": 0.6,
  "top_p": 0.9,
  "max_tokens": 4096,
  "stream": true
}
```

### Response Schema (Non-streaming)

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "model": "nvidia/nemotron-3-ultra-550b-instruct",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "..."},
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

| HTTP Code | Meaning | Retry Strategy |
|-----------|---------|----------------|
| 400 | Bad Request | Fix payload; no retry |
| 401 | Unauthorized | Check API key |
| 429 | Rate Limited | Exponential backoff: 1s, 2s, 4s, 8s |
| 500 | Server Error | Retry up to 3x with 2s delay |
| 503 | Unavailable | Retry with 5s delay |

---

## Rate Limit Strategy

See `AI-0005-FreeTier-Strategy.md` for full free tier management.

| Tier | RPM | TPM | Strategy |
|------|-----|-----|----------|
| Free | ~10 | ~50K | Queue + cache + deduplicate |
| Build | Higher | Higher | TBD |

---

## Open WebUI Integration

Open WebUI connects to NIM as an OpenAI-compatible endpoint:

1. Set **API Base URL** to `https://integrate.api.nvidia.com/v1`
2. Set **API Key** to your `NVIDIA_API_KEY`
3. Select model `nvidia/nemotron-3-ultra-550b-instruct`

See `AI-0003-OpenWebUI-Compatibility.md` for full Open WebUI setup.

---

## References

- [NVIDIA NIM API Reference](https://docs.api.nvidia.com)
- [NVIDIA Build Portal](https://build.nvidia.com)
- AI-0001-Nemotron-Engineering-Spec.md
- AI-0005-FreeTier-Strategy.md

---

## TODO

- [ ] Document function calling schema examples
- [ ] Test JSON mode structured output
- [ ] Add Python snippet using `openai` SDK
- [ ] Track and document actual rate limits per tier
- [ ] Add token counting utility reference
