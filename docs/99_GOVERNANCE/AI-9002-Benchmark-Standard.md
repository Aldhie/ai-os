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
| [AI-9001](AI-9001-Documentation-Standard.md) | Documentation standard |
| [AI-9003](AI-9003-Prompt-Engineering-Standard.md) | Prompt standard |
| [benchmark/](../../benchmark/) | Benchmark suite root |

---

## 1. Purpose

This document defines the engineering standard for all benchmark test cases in the `ai-os` repository. Every engineering claim that is marked `[FACT: Benchmark]` MUST have a corresponding benchmark TC in this suite.

Benchmarks in this repository serve three purposes:
1. **Validation:** Verify claims made in engineering specs
2. **Regression:** Detect quality degradation across model versions or configuration changes
3. **Comparison:** Enable evidence-based comparison between configurations

---

## 2. Benchmark Categories

| Category | Path | Description |
|----------|------|-------------|
| Discussion | `benchmark/tests/discussion/` | Open-ended reasoning and discussion |
| Reasoning | `benchmark/tests/reasoning/` | Multi-step logical and mathematical reasoning |
| Planning | `benchmark/tests/planning/` | Task decomposition and planning |
| Architecture | `benchmark/tests/architecture/` | Software architecture design |
| Coding | `benchmark/tests/coding/` | Code generation and review |
| Debugging | `benchmark/tests/debugging/` | Bug identification and fixing |
| Hospitality | `benchmark/tests/hospitality/` | Domain-specific hotel/hospitality tasks |
| Business | `benchmark/tests/business/` | Business strategy and operations |
| Docker | `benchmark/tests/docker/` | Container and infrastructure tasks |
| OpenWebUI | `benchmark/tests/openwebui/` | Open WebUI integration behavior |
| NIM | `benchmark/tests/nim/` | NVIDIA NIM API-specific behavior |
| Memory | `benchmark/tests/memory/` | Memory injection and recall |
| RAG | `benchmark/tests/rag/` | Retrieval-augmented generation quality |

---

## 3. Mandatory TC Structure

Every benchmark test case (TC) MUST use this structure:

```markdown
# TC-XXXX: [Short Title]

## Metadata
| Field | Value |
|-------|-------|
| TC ID | TC-XXXX |
| Category | [category] |
| Difficulty | Easy / Medium / Hard / Expert |
| Required Capability | [capability ID] |
| Created | YYYY-MM-DD |
| Last Run | YYYY-MM-DD |
| Status | Active / Archived |

## Question
[The exact prompt or task to send to the model]

## Context (if RAG/Memory)
[Context documents if required]

## Expected Behaviour
[Description of what a correct, high-quality response contains]

## Evaluation Criteria
| Criterion | Weight | Description |
|-----------|--------|-------------|
| Accuracy | X% | |
| Completeness | X% | |
| Format | X% | |
| Reasoning quality | X% | |

## Scoring
| Score | Description |
|-------|-------------|
| 100 | Perfect — all criteria met |
| 80-99 | High quality — minor gaps |
| 60-79 | Acceptable — significant gaps |
| <60 | FAIL — unacceptable |

## Success Condition
[Minimum score to pass]

## Failure Condition
[What constitutes a clear fail]

## References
[Links to related documents, experiments, requirements]

## Results History
| Date | Model | Config | Score | Notes |
|------|-------|--------|-------|-------|
```

---

## 4. Scoring Standard

| Dimension | Measurement Method |
|-----------|-------------------|
| Accuracy | Compare to ground truth; 0-10 integer score |
| Completeness | Does response cover all required elements? 0-10 |
| Format | Does output match required format? Pass/Fail |
| Reasoning quality | Is `<think>` trace relevant and correct? 0-10 |
| Composite | Weighted average per TC definition |

**Minimum pass score:** 70/100 (unless TC specifies otherwise)

---

## 5. Benchmark Execution Rules

1. **Isolation:** Run each TC in isolation (no shared conversation history unless explicitly testing multi-turn)
2. **Controlled environment:** Use exact config specified in TC metadata
3. **Multi-run:** Run each TC a minimum of 3 times; report mean and std deviation
4. **Seed:** Use `seed=42` where supported for reproducibility
5. **Record everything:** Store raw outputs in `benchmark/results/YYYY-MM-DD/`

---

## 6. Regression Policy

- Any config change to `parameters.json` or system prompts MUST be followed by re-running the full relevant category benchmark
- A regression is defined as: any TC score drops by ≥5 points or any previously passing TC now fails
- A regression blocks promotion to `main` unless explicitly accepted with an EDR

---

## 7. Relationship to Experiments

Benchmark TCs provide **reusable, repeatable measurements**. Experiments provide **hypothesis-driven, one-time investigations**.

| Aspect | Benchmark TC | Experiment |
|--------|-------------|------------|
| Purpose | Regression + validation | Discovery |
| Frequency | Every config change | Once (or few times) |
| Format | Standardized | Flexible |
| Results | Always recorded | Can be pending |
| Promotes | Engineering fact | Hypothesis resolution |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial benchmark standard |
