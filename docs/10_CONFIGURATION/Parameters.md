# Model Parameter Configuration

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | Parameters.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the model inference parameters used for Nemotron 3 Ultra 550B in the AI OS. It explains each parameter, its purpose, recommended values, and the rationale for each choice.

---

## Scope

- Inference parameters and their effects
- Recommended values per use case
- Configuration file reference

---

## Dependencies

- `configs/openwebui/parameters.json` — the deployed configuration
- `AI-0002-NVIDIA-NIM-API.md` — API request schema

---

## References

- [NIM Inference Parameters](https://docs.nvidia.com/nim/)
- [Temperature and Sampling Guide](https://huggingface.co/blog/how-to-generate)

---

## Parameter Reference

| Parameter | Type | Range | Recommended | Description |
|-----------|------|-------|-------------|-------------|
| `temperature` | float | 0.0–2.0 | 0.6 | Randomness of output. Lower = more deterministic. |
| `top_p` | float | 0.0–1.0 | 0.95 | Nucleus sampling. Limits token selection to top P probability mass. |
| `top_k` | int | 0–100 | 40 | Limits token selection to top K tokens. |
| `max_tokens` | int | 1–8192 | 2048 | Maximum tokens in the completion. |
| `repetition_penalty` | float | 1.0–2.0 | 1.1 | Penalizes repetition. Values > 1.0 reduce repetition. |
| `stream` | bool | true/false | true | Enable token streaming for better UX. |
| `stop` | array | strings | [] | Stop sequences to end generation early. |

---

## Use Case Profiles

### General Conversation

```json
{
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 1024,
  "repetition_penalty": 1.05
}
```

### Reasoning / Analysis

```json
{
  "temperature": 0.3,
  "top_p": 0.9,
  "max_tokens": 4096,
  "repetition_penalty": 1.1
}
```

### Creative Writing

```json
{
  "temperature": 1.0,
  "top_p": 0.98,
  "max_tokens": 2048,
  "repetition_penalty": 1.0
}
```

### Code Generation

```json
{
  "temperature": 0.2,
  "top_p": 0.85,
  "max_tokens": 4096,
  "repetition_penalty": 1.15
}
```

---

## TODO

- [ ] Validate parameter values with benchmark results
- [ ] Add parameter sensitivity analysis
- [ ] Document min/max effective values from testing
- [ ] Create per-task parameter profiles
- [ ] Sync with `configs/openwebui/parameters.json`
