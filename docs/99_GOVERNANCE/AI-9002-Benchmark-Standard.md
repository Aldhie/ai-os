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
| **Category** | Governance |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-9001](AI-9001-Documentation-Standard.md) | Parent standard |
| [AI-9003](AI-9003-Prompt-Engineering-Standard.md) | Prompt format for benchmarks |
| [AI-0004](../00_ENGINEERING/AI-0004-Benchmark.md) | Benchmark execution records |
| [benchmark/](../../benchmark/) | All benchmark test cases |

---

## 1. Purpose

This standard defines the mandatory structure, scoring methodology, and lifecycle for all benchmark test cases in `Aldhie/ai-os`. Benchmarks are the **primary mechanism** for converting hypotheses into validated engineering facts.

**Engineering Principle:** A claim that cannot be benchmarked is an assumption. An assumption that is not tracked is a risk.

---

## 2. Benchmark Categories

| Category | Path | Scope |
|----------|------|-------|
| `discussion` | `benchmark/tests/discussion/` | General conversational quality |
| `reasoning` | `benchmark/tests/reasoning/` | Multi-step logical reasoning |
| `planning` | `benchmark/tests/planning/` | Task planning and decomposition |
| `architecture` | `benchmark/tests/architecture/` | System design and ADR quality |
| `coding` | `benchmark/tests/coding/` | Code generation and debugging |
| `debugging` | `benchmark/tests/debugging/` | Bug identification and resolution |
| `hospitality` | `benchmark/tests/hospitality/` | Domain-specific: hospitality industry |
| `business` | `benchmark/tests/business/` | Business analysis and strategy |
| `docker` | `benchmark/tests/docker/` | Containerization and deployment |
| `openwebui` | `benchmark/tests/openwebui/` | Open WebUI integration behavior |
| `nim` | `benchmark/tests/nim/` | NVIDIA NIM API behavior |
| `memory` | `benchmark/tests/memory/` | Long-term memory and recall |
| `rag` | `benchmark/tests/rag/` | Retrieval-Augmented Generation |

---

## 3. Mandatory Test Case Structure

Every test case file MUST follow this exact template:

```markdown
# [CATEGORY]-TC-[XXXX]: [Short Title]

---

## Metadata

| Field | Value |
|-------|-------|
| **TC ID** | [CATEGORY]-TC-[XXXX] |
| **Category** | [category] |
| **Difficulty** | [Trivial / Easy / Medium / Hard / Expert] |
| **Required Capability** | [list of model capabilities tested] |
| **Status** | [Pending / Running / Complete / Retired] |
| **Created** | [YYYY-MM-DD] |
| **Last Run** | [YYYY-MM-DD or N/A] |
| **References** | [links to relevant docs, APIs, papers] |

---

## Objective

[1-2 sentences: what specific behavior this test validates]

---

## Hypothesis

[Specific, falsifiable claim: "The model will X when given Y"]

---

## Question / Prompt

```
[Exact prompt text that will be sent to the model]
```

---

## Environment

| Parameter | Value |
|-----------|-------|
| **Model** | nvidia/nemotron-3-ultra-550b-a55b |
| **Temperature** | [value] |
| **Top-P** | [value] |
| **Max Tokens** | [value] |
| **Thinking Mode** | [on / off / medium_effort] |
| **System Prompt** | [text or reference] |
| **Open WebUI Version** | [version] |
| **NIM Endpoint** | https://integrate.api.nvidia.com/v1 |

---

## Expected Behavior

[Precise description of what a correct response looks like]

---

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| [criterion 1] | [0-100] | [what counts as passing] |
| [criterion 2] | [0-100] | [what counts as passing] |

---

## Scoring

| Score | Label | Meaning |
|-------|-------|---------|
| 90-100 | PASS | Meets all criteria |
| 70-89 | PARTIAL | Meets major criteria, misses minor |
| 50-69 | WEAK | Partially correct, significant gaps |
| 0-49 | FAIL | Does not meet criteria |

---

## Success Condition

[Score ≥ X AND specific observable output Y]

---

## Failure Condition

[Score < X OR observable failure pattern Z]

---

## Actual Result

> Status: PENDING

```
[Actual model output when run]
```

---

## Score

| Criterion | Score | Notes |
|-----------|-------|-------|
| [criterion 1] | PENDING | |

**Total Score: PENDING**

---

## Analysis

[What the result reveals about model capability]

---

## Conclusion

[Pass/Fail verdict with evidence-tagged claim]

---

## Decision

[Engineering action taken based on result]

---

## References

- [links]
```

---

## 4. Difficulty Scale

| Level | Meaning | Expected Pass Rate |
|-------|---------|-------------------|
| `Trivial` | Any competent LLM should pass | > 95% |
| `Easy` | Standard capability, well-documented | > 80% |
| `Medium` | Requires reasoning or domain knowledge | 60-80% |
| `Hard` | Requires advanced reasoning + domain expertise | 40-60% |
| `Expert` | State-of-the-art capability required | < 40% |

---

## 5. Benchmark Execution Protocol

1. **Pre-run:** Verify environment parameters match TC spec
2. **Isolation:** Run each TC independently (no shared context)
3. **Repetition:** For stochastic tests, run minimum 3 times and report median
4. **Recording:** Copy exact model output verbatim into `Actual Result` section
5. **Scoring:** Apply criteria independently before reading score
6. **Post-run:** Update `Last Run` date and promote TC to `Complete`
7. **Failure:** If FAIL, open a GitHub Issue tagged `benchmark-failure`

---

## 6. Benchmark-to-Requirement Linking

Every benchmark TC MUST link to at least one requirement in [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md).

Every requirement with `Verification Method: Benchmark` MUST have at least one TC assigned.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial benchmark standard |
