# Model Parameters Specification

| Field | Value |
|---|---|
| **Title** | AI-OS Model Parameters Specification |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines the inference parameters used when calling Nemotron Ultra 550B via NVIDIA NIM. Documents the rationale for each value and the constraints within which they should be tuned.

---

## Scope

- NVIDIA NIM API call parameters
- Open WebUI model parameter configuration
- Applies to all operational modes (chat, plan, reflect, critique)

---

## Parameter Definitions

### Temperature

| Property | Value |
|---|---|
| Parameter | `temperature` |
| Type | Float |
| Range | 0.0 – 2.0 |
| **AI-OS Default** | **0.6** |
| Min (deterministic) | 0.0 |
| Max (creative) | 1.2 |

**Rationale:** 0.6 balances creativity and consistency. Lower values for Critic and Planner modes; higher for creative tasks.

---

### Top-P (Nucleus Sampling)

| Property | Value |
|---|---|
| Parameter | `top_p` |
| Type | Float |
| Range | 0.0 – 1.0 |
| **AI-OS Default** | **0.95** |

**Rationale:** Standard value for high-quality generation. Do not combine with very low temperature.

---

### Max Tokens

| Property | Value |
|---|---|
| Parameter | `max_tokens` |
| Type | Integer |
| **AI-OS Default** | **2048** |
| Minimum | 256 |
| Maximum | 8192 |

**Rationale:** 2048 covers most responses while conserving API quota. Increase for long-form documents.

---

### Frequency Penalty

| Property | Value |
|---|---|
| Parameter | `frequency_penalty` |
| **AI-OS Default** | **0.1** |
| Range | -2.0 – 2.0 |

**Rationale:** Slight positive value reduces repetition in long outputs.

---

### Presence Penalty

| Property | Value |
|---|---|
| Parameter | `presence_penalty` |
| **AI-OS Default** | **0.0** |
| Range | -2.0 – 2.0 |

**Rationale:** Neutral default; increase if model tends to avoid topic shifts.

---

### Stream

| Property | Value |
|---|---|
| Parameter | `stream` |
| **AI-OS Default** | **true** |

**Rationale:** Streaming improves perceived responsiveness. Always enabled in Open WebUI.

---

## Mode-Specific Parameter Sets

| Mode | Temperature | Max Tokens | Notes |
|---|---|---|---|
| Chat | 0.6 | 2048 | General conversation |
| Planner | 0.3 | 4096 | Structured output needed |
| Reflection | 0.4 | 2048 | Self-evaluation |
| Critic | 0.2 | 1024 | Deterministic grading |
| Creative | 1.0 | 4096 | Creative writing |
| Code | 0.2 | 4096 | Precise generation |

---

## Configuration File

See: `configs/openwebui/parameters.json`

---

## Dependencies

- `configs/openwebui/parameters.json`
- [AI-0002-NVIDIA-NIM-API.md](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md)
- [AI-0005-FreeTier-Strategy.md](../00_ENGINEERING/AI-0005-FreeTier-Strategy.md)

---

## References

- [NVIDIA NIM Parameter Docs](https://docs.api.nvidia.com/)
- [Temperature & Sampling Guide](https://platform.openai.com/docs/guides/text-generation)

---

## TODO

- [ ] Validate defaults against Nemotron Ultra behavior
- [ ] Tune Critic mode temperature after baseline testing
- [ ] Build parameter sweep test for optimal chat settings
- [ ] Document seed usage for reproducibility testing
- [ ] Add stop sequence recommendations
