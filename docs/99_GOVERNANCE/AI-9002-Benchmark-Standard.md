# AI-9002: Benchmark Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9002 |
| **Title** | Benchmark Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-0004 Benchmark Framework](../00_ENGINEERING/AI-0004-Benchmark.md)
- [AI-9001 Documentation Standard](AI-9001-Documentation-Standard.md)
- [AI-9003 Prompt Engineering Standard](AI-9003-Prompt-Engineering-Standard.md)
- [benchmark/tests/](../../benchmark/tests/)

---

## 1. Purpose

Defines the mandatory structure, scoring methodology, environment specification, and reporting format for every benchmark test case in this repository. All benchmark evidence cited in engineering documents MUST conform to this standard.

---

## 2. Benchmark Test Case Structure

Every benchmark file (`TC-xxxx.md`) MUST contain all of the following sections:

### 2.1 Header

```markdown
## TC-[NNNN]: [Title]

| Field | Value |
|-------|-------|
| ID | TC-NNNN |
| Category | discussion / reasoning / planning / architecture / coding / debugging / hospitality / business / docker / openwebui / nim / memory / rag |
| Difficulty | Easy / Medium / Hard / Expert |
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Required Capability | [list of capabilities] |
| Evidence Basis | [FACT / HYPOTHESIS / BENCHMARK-REQUIRED] |
| References | [AI-0001], [AI-0003], [EXP-0001], etc. |
```

### 2.2 Question / Prompt

Exact prompt text sent to the model. No paraphrase — exact string.

```markdown
## Question

**System Prompt:**
```
[exact system prompt]
```

**User Message:**
```
[exact user message]
```

**Parameters:**
- temperature: X
- top_p: X
- max_tokens: X
- thinking: ON/OFF
```

### 2.3 Expected Behaviour

What a correct response looks like. Must be specific and measurable, not vague.

### 2.4 Evaluation Criteria

| Criterion | Weight | Measurement Method |
|-----------|--------|--------------------|
| Correctness | 40% | Manual or automated check |
| Completeness | 20% | Checklist of required elements |
| Format compliance | 15% | Structural comparison |
| Reasoning quality | 15% | Reasoning chain audit |
| Efficiency | 10% | Token count vs expected |

### 2.5 Scoring

| Score | Meaning |
|-------|---------|
| 5 | Perfect — all criteria met |
| 4 | Good — minor gaps |
| 3 | Acceptable — functional but incomplete |
| 2 | Marginal — significant gaps |
| 1 | Fail — wrong or harmful output |
| 0 | Hard fail — error, refusal, or crash |

### 2.6 Failure Conditions

Explicit conditions that constitute automatic failure (score = 0):
- Model returns HTTP error
- Model refuses the request
- Model hallucinates a fact that contradicts `[FACT]`-tagged content
- Response truncated due to token limit

### 2.7 Success Conditions

Minimum score and criteria for a test to be counted as PASS.

### 2.8 Actual Result

Filled in post-execution. Never left empty in Active status.

```markdown
## Actual Result

**Date:** YYYY-MM-DD
**Score:** N/5
**PASS/FAIL:** PASS
**Response Excerpt:**
> [first 200 chars of model response]

**Notes:**
[observations]
```

### 2.9 Analysis

Why the model scored what it did. Connects to experiment documents.

### 2.10 Benchmark Reference

Links to EXP-xxxx documents that interpret these results.

---

## 3. Benchmark Categories

| Category | Focus Area | Key Capability |
|----------|-----------|----------------|
| `discussion` | Open-ended reasoning and conversation quality | Coherence, depth, multi-turn |
| `reasoning` | Logical deduction, math, structured thinking | Chain-of-thought, accuracy |
| `planning` | Multi-step task decomposition | Plan quality, step validation |
| `architecture` | System design and technical recommendation | Engineering accuracy |
| `coding` | Code generation, debugging, refactoring | Correctness, style, tests |
| `debugging` | Finding and fixing bugs | Root cause accuracy |
| `hospitality` | Customer service and empathy scenarios | Tone, resolution quality |
| `business` | Business analysis, reporting, strategy | Domain accuracy, format |
| `docker` | Docker/container operations and Dockerfiles | Command accuracy, best practice |
| `openwebui` | Open WebUI configuration and troubleshooting | Config accuracy, OW-specific knowledge |
| `nim` | NVIDIA NIM API usage and integration | API correctness, parameter handling |
| `memory` | Long-term memory recall and context management | Recall accuracy, injection quality |
| `rag` | Retrieval-augmented generation | Retrieval precision, answer grounding |

---

## 4. Environment Specification

Every benchmark result MUST record:

```yaml
environment:
  model: nvidia/nemotron-3-ultra-550b-a55b
  endpoint: https://integrate.api.nvidia.com/v1
  openwebui_version: [version]
  date: YYYY-MM-DD
  temperature: 1.0
  top_p: 0.95
  max_tokens: [value used]
  thinking_mode: ON / OFF / medium_effort
  system_prompt: [exact prompt or reference]
  notes: [any deviations from standard config]
```

---

## 5. Benchmark Lifecycle

```
Designed → Pending → Running → Completed → Archived
```

| Status | Meaning |
|--------|---------|
| Designed | TC written, not yet run |
| Pending | Queued for execution |
| Running | Currently being executed |
| Completed | Result filled in, analysis done |
| Archived | Superseded by newer test |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
