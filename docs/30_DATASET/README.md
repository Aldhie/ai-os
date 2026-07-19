# Dataset Documentation

| Field | Value |
|---|---|
| **Title** | AI-OS Dataset Documentation |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Documents the structure, curation process, quality standards, and usage guidelines for all datasets used in AI-OS evaluation, fine-tuning, and regression testing.

---

## Scope

- Evaluation datasets (benchmark and regression)
- Fine-tuning datasets (instruction tuning)
- Conversation datasets (curated chat logs)
- Excludes: Raw/unprocessed data (see `dataset/raw/` — gitignored)

---

## Dataset Types

### 1. Instruction Following (IF)

**Format:** JSONL `{"prompt": "...", "response": "...", "category": "..."}`

**Purpose:** Train/evaluate instruction adherence.

**Minimum Size:** 500 samples.

**Quality Bar:** Human-reviewed, 4+/5 quality score.

---

### 2. Conversation (CONV)

**Format:** JSONL multi-turn `{"messages": [{"role": "...", "content": "..."}]}`

**Purpose:** Multi-turn conversation quality.

**Minimum Size:** 200 conversations.

---

### 3. Evaluation (EVAL)

**Format:** JSONL `{"prompt": "...", "ideal_response": "...", "rubric": "..."}`

**Purpose:** Benchmark scoring and regression testing.

**Minimum Size:** 100 samples across all categories.

---

### 4. Adversarial (ADV)

**Format:** JSONL `{"prompt": "...", "expected_behavior": "refuse | handle", "category": "..."}`

**Purpose:** Safety and robustness testing.

**Minimum Size:** 50 samples.

---

## Data Quality Standards

1. No personally identifiable information (PII).
2. No harmful, offensive, or illegal content.
3. All samples reviewed by owner before commit.
4. Each sample tagged with: version, date, source, category.
5. Duplicates removed before commit.

---

## Dataset Registry

| Dataset ID | Type | Size | Status | Location |
|---|---|---|---|---|
| DS-001 | IF | TBD | Planned | `dataset/instruction/` |
| DS-002 | CONV | TBD | Planned | `dataset/conversation/` |
| DS-003 | EVAL | TBD | Planned | `dataset/evaluation/` |
| DS-004 | ADV | TBD | Planned | `dataset/adversarial/` |

---

## Dependencies

- `dataset/` directory
- `docs/40_FINETUNE/README.md`
- `docs/90_TESTING/BenchmarkCases.md`

---

## References

- [Hugging Face Datasets](https://huggingface.co/docs/datasets/)
- [FLAN Dataset Paper](https://arxiv.org/abs/2109.01652)

---

## TODO

- [ ] Collect initial instruction following dataset
- [ ] Curate conversation dataset from Open WebUI logs
- [ ] Build evaluation dataset from benchmark cases
- [ ] Create adversarial dataset v1
- [ ] Build dataset validation script
