# Dataset Catalog

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | docs/30_DATASET/README.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This directory documents all datasets used for training, evaluation, and fine-tuning the AI OS. Large dataset files are stored separately (not in this repository); this document catalogs their sources, formats, and intended use.

---

## Scope

- Dataset catalog and metadata
- Dataset format specifications
- Dataset acquisition and preprocessing
- Dataset versioning

---

## Dependencies

- `docs/40_FINETUNE/README.md` — datasets used for fine-tuning
- `docs/90_TESTING/Evaluation.md` — evaluation datasets
- `dataset/` directory — small reference datasets only

---

## Dataset Catalog

| ID | Name | Type | Size | Format | Use Case | Source | Status |
|----|------|------|------|--------|----------|--------|---------|
| DS-001 | TBD | Instruction-Following | TBD | JSONL | Fine-tuning | TBD | Planned |
| DS-002 | TBD | Conversation | TBD | JSONL | Fine-tuning | TBD | Planned |
| DS-003 | TBD | Evaluation | TBD | JSONL | Benchmark | TBD | Planned |

---

## Dataset Format Standard

### Instruction-Following Format (JSONL)

```json
{
  "instruction": "<task instruction>",
  "input": "<optional context input>",
  "output": "<expected response>"
}
```

### Conversation Format (JSONL)

```json
{
  "messages": [
    {"role": "system", "content": "<system prompt>"},
    {"role": "user", "content": "<user message>"},
    {"role": "assistant", "content": "<assistant response>"}
  ]
}
```

---

## Storage Policy

- Dataset files > 10MB must use Git LFS or be stored externally
- All datasets must have a corresponding entry in this catalog
- Include checksum (SHA256) for data integrity verification

---

## TODO

- [ ] Identify and source instruction-following datasets
- [ ] Curate domain-specific conversation datasets
- [ ] Define data quality standards and filtering criteria
- [ ] Set up dataset versioning system
- [ ] Build dataset preprocessing pipeline
