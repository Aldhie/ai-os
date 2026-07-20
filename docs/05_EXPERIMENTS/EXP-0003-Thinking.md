# EXP-0003: Thinking Mode Comparison

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0003 |
| **Title** | Thinking Mode Comparison: OFF vs ON vs medium_effort vs reasoning_budget |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | Critical |

---

## Cross References

- [AI-0001 — Nemotron Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0003-Audit — Critical Findings](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) — R-03 Revised, NEW-01
- [AI-9003 — Prompt Engineering Standard](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md)
- [EXP-0001 — Temperature](EXP-0001-Temperature.md)

---

## 1. Objective

Quantify the quality-cost tradeoff across four thinking modes for Nemotron Ultra 550B:
1. **OFF** — `/nothink` (no reasoning trace)
2. **ON** — `/think` (full reasoning trace)
3. **medium_effort** — `enable_thinking: true, medium_effort: true`
4. **reasoning_budget** — `reasoning_budget: 512` (hard cap)

---

## 2. Hypothesis

> `[HYPOTHESIS]` For simple factual questions, `thinking: OFF` produces equivalent accuracy to `thinking: ON` at ~60% of the token cost. For multi-step reasoning problems, `thinking: ON` produces measurably higher accuracy. `medium_effort` achieves 80–90% of the accuracy of full thinking at ~50% of reasoning token cost.

---

## 3. Variables

### Independent Variable

| Mode | Implementation | Via OW |
|------|---------------|--------|
| OFF | System prompt: `/nothink` | Yes — native |
| ON | System prompt: `/think` | Yes — native |
| medium_effort | `extra_body.chat_template_kwargs.medium_effort: true` | No — Pipeline required |
| budget_512 | `reasoning_budget: 512` | No — Pipeline required |

### Controlled Variables

| Parameter | Value |
|-----------|-------|
| `temperature` | `1.0` |
| `top_p` | `0.95` |
| `max_tokens` | `4096` |
| `seed` | Not fixed (stochastic by design) |

### Dependent Variables

- Answer accuracy (correct/incorrect for factual tasks)
- Reasoning quality score (1–5 rubric for analysis tasks)
- Reasoning trace token count
- Total tokens (prompt + completion)
- Time to first token (TTFT)
- Cost per correct answer (token count proxy)

---

## 4. Environment

| Component | Value |
|-----------|-------|
| API Endpoint | `https://integrate.api.nvidia.com/v1/chat/completions` |
| Model | `nvidia/nemotron-3-ultra-550b-a55b` |
| Pipeline | Custom OW Pipeline for `extra_body` injection (medium_effort, budget modes) |
| Date | `[PENDING]` |

---

## 5. Procedure

**Task set — three difficulty levels:**

**Simple (factual):** `"What is the capital of Indonesia?"`

**Medium (multi-step):** `"A train travels at 80 km/h for 2 hours, then 120 km/h for 1.5 hours. What is the average speed for the entire journey?"`

**Hard (analytical):** `"Analyze the systemic risks of a monorepo architecture for a 50-person engineering team. Include version management, CI/CD complexity, and blast radius of a bad commit."`

For each task:
1. Run with all 4 modes
2. 5 runs per mode per task (n=5 for statistical stability)
3. Record: accuracy, reasoning token count, TTFT, total tokens
4. Calculate: cost-accuracy tradeoff curve

---

## 6. Expected Result

| Task | Best Mode | Expected Accuracy | Reasoning Tokens |
|------|-----------|-------------------|------------------|
| Simple | OFF | 100% | ~0 |
| Medium | medium_effort | ~95% | ~200–500 |
| Hard | ON (full) | ~85% | ~1000–3000 |

---

## 7. Actual Result

> `[PENDING]`

---

## 8. Analysis

> `[PENDING]`

---

## 9. Conclusion

> `[PENDING]`

---

## 10. Decision

> `[PENDING]` Define thinking mode selection policy in `parameters.json` profiles based on task classification.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design — created from AI-0003-Audit R-03 revised and NEW-01 |
