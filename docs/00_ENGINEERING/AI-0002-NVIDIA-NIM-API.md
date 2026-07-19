# AI-0002 — NVIDIA NIM API Contract

| Field | Value |
|---|---|
| **Title** | NVIDIA NIM API Contract |
| **Document ID** | AI-0002 |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines the complete API contract between AI-OS and NVIDIA Cloud NIM. This document covers authentication, endpoint specification, request/response schema, error handling, streaming, and rate limits.

---

## Scope

- NVIDIA Cloud NIM public API
- Model: `nvidia/nemotron-ultra-253b-v1`
- Transport: HTTPS REST
- Excludes: On-premise NIM deployments

---

## Authentication

```text
Method:    Bearer Token
Header:    Authorization: Bearer {NVIDIA_API_KEY}
Token:     Obtained from https://build.nvidia.com/
Expiry:    Per key policy (check dashboard)
```

**Security Rule:** API keys must NEVER be committed to this repository. Use environment variables only.

```bash
export NVIDIA_API_KEY="nvapi-xxxxxxxxxxxx"
```

---

## Endpoints

### Chat Completions

```text
POST https://integrate.api.nvidia.com/v1/chat/completions
```

### Models List

```text
GET https://integrate.api.nvidia.com/v1/models
```

---

## Request Schema

```json
{
  "model": "nvidia/nemotron-ultra-253b-v1",
  "messages": [
    {
      "role": "system | user | assistant | tool",
      "content": "string"
    }
  ],
  "temperature": 0.6,
  "top_p": 0.95,
  "max_tokens": 4096,
  "stream": false,
  "tools": [],
  "tool_choice": "auto | none | required",
  "response_format": {
    "type": "text | json_object"
  },
  "stop": ["string"],
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "seed": null
}
```

---

## Response Schema

```json
{
  "id": "chatcmpl-xxxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "nvidia/nemotron-ultra-253b-v1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "string",
        "tool_calls": []
      },
      "finish_reason": "stop | length | tool_calls | content_filter"
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

## Streaming

Set `"stream": true` to receive Server-Sent Events (SSE):

```text
data: {"id":"...","object":"chat.completion.chunk","choices":[{"delta":{"content":"tok"}}]}
data: [DONE]
```

Open WebUI natively supports SSE streaming.

---

## Error Codes

| HTTP Code | Meaning | Action |
|---|---|---|
| 400 | Bad Request | Check request schema |
| 401 | Unauthorized | Verify API key |
| 429 | Rate Limited | Back-off, see AI-0005 |
| 500 | Server Error | Retry with exponential back-off |
| 503 | Service Unavailable | Retry after delay |

---

## Rate Limits (Free Tier)

| Limit | Value |
|---|---|
| Requests per minute | TBD (check NVIDIA dashboard) |
| Tokens per minute | TBD |
| Requests per day | TBD |
| Context window max | 128K tokens |

See [AI-0005-FreeTier-Strategy.md](AI-0005-FreeTier-Strategy.md) for mitigation strategies.

---

## Dependencies

- [AI-0001-Nemotron-Engineering-Spec.md](AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0005-FreeTier-Strategy.md](AI-0005-FreeTier-Strategy.md)

---

## References

- [NVIDIA NIM API Docs](https://docs.api.nvidia.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) (compatible schema)

---

## TODO

- [ ] Confirm actual rate limits from NVIDIA dashboard
- [ ] Test tool calling with Open WebUI format
- [ ] Document streaming behavior in Open WebUI
- [ ] Add retry logic recommendation for scripts
- [ ] Validate JSON mode output consistency
