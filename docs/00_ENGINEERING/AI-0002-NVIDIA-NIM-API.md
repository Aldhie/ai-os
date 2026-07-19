# AI-0002 — NVIDIA NIM API Reference

| Field | Value |
|-------|-------|
| **Title** | NVIDIA NIM API Reference |
| **Purpose** | Document the API interface, authentication, endpoints, and usage patterns for NVIDIA NIM |
| **Scope** | REST API, authentication, request/response schema, rate limits, error handling |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | AI-0001 (Model Spec) |
| **References** | [NVIDIA NIM API Docs](https://docs.api.nvidia.com/), [OpenAI API Reference](https://platform.openai.com/docs/api-reference) |

---

## 1. Base Configuration

| Parameter | Value |
|-----------|-------|
| Base URL | `https://integrate.api.nvidia.com/v1` |
| API Compatibility | OpenAI-compatible |
| Authentication | Bearer token (NVIDIA API Key) |
| Content-Type | `application/json` |

---

## 2. Authentication

```http
Authorization: Bearer nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

API keys are obtained from [NVIDIA Build](https://build.nvidia.com/). Store keys in environment variables — never commit to repository.

```bash
export NVIDIA_API_KEY="nvapi-xxxxxxxxxxxxxxxxxxxx"
```

---

## 3. Chat Completions Endpoint

### Request

```http
POST https://integrate.api.nvidia.com/v1/chat/completions
```

```json
{
  "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1",
  "messages": [
    {"role": "system", "content": "<system_prompt>"},
    {"role": "user", "content": "<user_message>"}
  ],
  "temperature": 0.6,
  "top_p": 0.95,
  "max_tokens": 4096,
  "stream": true
}
```

### Extended Thinking Mode

```json
{
  "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1",
  "messages": [...],
  "thinking": {"type": "enabled", "budget_tokens": 10000},
  "max_tokens": 16384,
  "stream": true
}
```

### Structured Output

```json
{
  "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1",
  "messages": [...],
  "response_format": {"type": "json_object"}
}
```

---

## 4. Tool Calling

```json
{
  "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1",
  "messages": [...],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_time",
        "description": "Get the current date and time",
        "parameters": {
          "type": "object",
          "properties": {
            "timezone": {"type": "string", "description": "IANA timezone"}
          },
          "required": ["timezone"]
        }
      }
    }
  ],
  "tool_choice": "auto"
}
```

---

## 5. Rate Limits (Free Tier)

| Limit Type | Value |
|------------|-------|
| Requests per minute (RPM) | 10 |
| Tokens per minute (TPM) | TBD |
| Tokens per day (TPD) | TBD |
| Max context per request | 128K tokens |

> See AI-0005 for Free Tier optimization strategy.

---

## 6. Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Bad Request | Check request schema |
| 401 | Unauthorized | Verify API key |
| 429 | Rate Limited | Implement exponential backoff |
| 500 | Server Error | Retry with backoff |
| 503 | Service Unavailable | Retry after delay |

---

## TODO

- [ ] Confirm exact rate limits for Free Tier
- [ ] Document token pricing tiers
- [ ] Test streaming response handling in Open WebUI
- [ ] Document embedding endpoint if available
- [ ] Add Python SDK example
