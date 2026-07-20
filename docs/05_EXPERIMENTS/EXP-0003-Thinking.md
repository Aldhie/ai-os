# EXP-0003: Reasoning Mode Comparison

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0003 |
| **Title** | Reasoning Mode Comparison: OFF vs. ON vs. medium_effort |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related BM** | BM-11, BM-12 |
| **Related REQ** | REQ-AI-0001 (reasoning mode) |
| **Cross-References** | [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) · [AI-0003-Audit](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) · [AI-9003](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md) |

---

## 1. Objective

Quantify the quality and cost trade-off between three reasoning modes for NVIDIA Nemotron Ultra 550B:
1. **OFF** (`/nothink`): No thinking trace. Fastest, cheapest.
2. **ON** (`/think`): Full reasoning trace. Highest quality, most tokens.
3. **medium_effort**: Reduced thinking trace. Balanced quality/cost.

**Engineering Questions:**
- What is the quality delta between reasoning OFF and reasoning ON?
- What percentage of token savings does `medium_effort` provide vs full `think`?
- For which task types is reasoning mode worth the token cost?

---

## 2. Hypothesis

> **H1:** Reasoning ON will score ≥1.5 points higher than reasoning OFF on complex multi-step problems.
>
> **H2:** `medium_effort` will consume ~40–60% fewer thinking tokens than full `think` mode while retaining ≥90% of the quality gain over OFF mode. [HYPOTHESIS — NVIDIA says "significantly fewer tokens", exact percentage unknown]
>
> **H3:** For simple factual questions, reasoning ON and OFF will produce equivalent quality (thinking trace wasted).
>
> **H4:** For coding tasks, reasoning ON will produce meaningfully fewer bugs than OFF mode.

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | Reasoning mode | OFF (/nothink), ON (/think), medium_effort (Pipeline) |
| **Dependent** | Quality score (1-10) | Human rubric |
| **Dependent** | Thinking tokens consumed | From API `usage` field |
| **Dependent** | Total tokens (prompt + completion) | From API `usage` field |
| **Dependent** | Response latency (TTFT, TTLT) | Measured |
| **Controlled** | `temperature` | 1.0 |
| **Controlled** | `top_p` | 0.95 |
| **Controlled** | Task types | reasoning, coding, factual, creative |
| **Controlled** | Prompts | Identical across modes |

---

## 4. Environment

| Component | Config |
|-----------|--------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| OFF mode | System prompt: `/nothink` via Open WebUI |
| ON mode | System prompt: `/think` via Open WebUI |
| medium_effort | Requires Pipeline injection of `extra_body.chat_template_kwargs.medium_effort: true` |
| Runs per condition | 5 per task type per mode |

**Note:** `medium_effort` test depends on successful Pipeline implementation (BM-11). Cannot be tested via Open WebUI UI alone.

---

## 5. Procedure

1. Build and deploy Open WebUI Pipeline for `extra_body` injection
2. Create three model profiles in Open WebUI:
 - Profile A: `/nothink` system prompt
 - Profile B: `/think` system prompt
 - Profile C: `/think` + Pipeline `medium_effort: true`
3. Run 5 identical prompts per mode per task category
4. Record: response text, quality score, token counts, latency
5. Compare quality scores and token efficiency ratios

---

## 6. Expected Result

| Mode | Quality (Reasoning) | Quality (Factual) | Tokens | Latency |
|------|--------------------|--------------------|--------|----------|
| OFF | 6.5/10 | 8.0/10 | Baseline | Fast |
| ON | 9.0/10 | 8.1/10 | 3–5x | Slow |
| medium_effort | 8.0/10 | 8.0/10 | 1.5–2x | Medium |

---

## 7. Actual Result

> **STATUS: PENDING** — Blocked on Pipeline implementation (BM-11).

---

## 8–12. Analysis / Conclusion / Decision / Future Work / Benchmark Table

> **PENDING**

Decision on completion: Update `parameters.json` with task-specific mode profiles. Populate `medium_effort` profile parameters.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design; BM-11 dependency noted |
