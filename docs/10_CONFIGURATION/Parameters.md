# Parameters

| Field | Value |
|-------|-------|
| **Title** | Model Parameters Configuration |
| **Purpose** | Document and justify all inference parameters used for Nemotron Ultra |
| **Scope** | Temperature, top_p, max_tokens, presence/frequency penalty, streaming |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | AI-0002 (NIM API), AI-0005 (Free Tier Strategy) |
| **References** | `configs/openwebui/parameters.json` |

---

## Parameter Reference

| Parameter | Current Value | Range | Rationale |
|-----------|---------------|-------|-----------|
| `temperature` | 0.6 | 0.0–1.0 | Balanced creativity and consistency |
| `top_p` | 0.95 | 0.0–1.0 | Nucleus sampling, high diversity |
| `max_tokens` | 4096 | 1–32768 | Sufficient for most responses |
| `presence_penalty` | 0.0 | -2.0–2.0 | No penalty by default |
| `frequency_penalty` | 0.0 | -2.0–2.0 | No penalty by default |
| `stream` | true | bool | Enables streaming response |
| `top_k` | 50 | 1–1000 | NVIDIA-specific parameter |

---

## Parameter Profiles

### Creative Mode

```json
{"temperature": 0.9, "top_p": 0.95, "max_tokens": 8192}
```

### Precise Mode (Default)

```json
{"temperature": 0.6, "top_p": 0.95, "max_tokens": 4096}
```

### Analytical / Reasoning Mode

```json
{"temperature": 0.3, "top_p": 0.9, "max_tokens": 16384, "thinking": {"type": "enabled", "budget_tokens": 10000}}
```

### Fast / Summary Mode

```json
{"temperature": 0.5, "top_p": 0.9, "max_tokens": 1024}
```

---

## Tuning History

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| 0.1.0 | 2026-07-20 | Initial defaults | Baseline |

---

## TODO

- [ ] Run A/B test: temperature 0.6 vs 0.7
- [ ] Benchmark reasoning mode with thinking enabled
- [ ] Determine optimal max_tokens for daily use
- [ ] Test frequency_penalty effect on repetition
