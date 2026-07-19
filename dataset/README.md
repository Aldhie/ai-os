# Dataset Storage

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | dataset/README.md |
| **Version** | 0.1.0 |
| **Status** | Empty |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This directory holds small reference datasets, sample files, and data schemas for the AI OS. Large datasets (> 10MB) must be stored externally and cataloged in `docs/30_DATASET/README.md`.

---

## Scope

- Small reference and sample datasets
- Data format schemas
- Dataset catalog (see docs/30_DATASET/README.md for full catalog)

---

## Storage Policy

| File Size | Storage Location |
|-----------|------------------|
| < 1MB | This directory |
| 1MB – 10MB | This directory with Git LFS |
| > 10MB | External storage (HuggingFace, GCS, S3) |

---

## File Naming Convention

```
<dataset-id>-<name>-v<version>.<format>

Example:
DS-001-instruction-following-v0.1.jsonl
DS-003-evaluation-benchmark-v0.1.jsonl
```

---

## TODO

- [ ] Add first sample dataset
- [ ] Define Git LFS configuration for medium datasets
- [ ] Document external dataset access credentials management
- [ ] Create dataset validation schema
