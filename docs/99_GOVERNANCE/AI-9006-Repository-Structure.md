# AI-9006: Repository Structure

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9006 |
| **Title** | Repository Structure |
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
| [AI-9004](AI-9004-Versioning-Policy.md) | Versioning |
| [AI-9005](AI-9005-Release-Process.md) | Release |

---

## 1. Purpose

This document defines the authoritative directory structure for the `ai-os` repository and the purpose of each folder and file.

---

## 2. Directory Tree

```
ai-os/
├── README.md                          # Repository overview and quick start
├── CHANGELOG.md                       # Repository-level changelog
├── docs/
│   ├── 00_ENGINEERING/                # Core engineering specifications
│   │   ├── AI-0001-*.md               # Model engineering spec
│   │   ├── AI-0002-*.md               # NIM API spec
│   │   ├── AI-0003-*.md               # Open WebUI compatibility
│   │   ├── AI-0003-Critical-*.md      # Compatibility audit findings
│   │   ├── AI-0005-*.md               # Workflows
│   │   ├── AI-0006-*.md               # Architecture Decision Records
│   │   ├── REQ-INDEX.md               # Requirement traceability index
│   │   └── AI-XXXX-*.md               # Future engineering specs
│   ├── 05_EXPERIMENTS/                # Experiments (hypothesis-driven)
│   │   ├── EXP-0001-Temperature.md
│   │   ├── EXP-0002-TopP.md
│   │   ├── EXP-0003-Thinking.md
│   │   ├── EXP-0004-SystemPrompt.md
│   │   ├── EXP-0005-Memory.md
│   │   ├── EXP-0006-RAG.md
│   │   ├── EXP-0007-Planner.md
│   │   ├── EXP-0008-Reflection.md
│   │   ├── EXP-0009-Critic.md
│   │   └── EXP-0010-Agent.md
│   └── 99_GOVERNANCE/                 # Standards, policies, processes
│       ├── AI-9001-Documentation-Standard.md
│       ├── AI-9002-Benchmark-Standard.md
│       ├── AI-9003-Prompt-Engineering-Standard.md
│       ├── AI-9004-Versioning-Policy.md
│       ├── AI-9005-Release-Process.md
│       ├── AI-9006-Repository-Structure.md
│       ├── AI-9007-Architecture-Principles.md
│       └── AI-9008-Engineering-Decision-Record-Standard.md
├── configs/
│   └── openwebui/
│       ├── parameters.json            # Validated inference parameters
│       └── prompts/                   # Versioned system prompts
├── benchmark/
│   ├── README.md                  # Benchmark suite overview
│   ├── tests/
│   │   ├── discussion/
│   │   ├── reasoning/
│   │   ├── planning/
│   │   ├── architecture/
│   │   ├── coding/
│   │   ├── debugging/
│   │   ├── hospitality/
│   │   ├── business/
│   │   ├── docker/
│   │   ├── openwebui/
│   │   ├── nim/
│   │   ├── memory/
│   │   └── rag/
│   └── results/                   # Timestamped benchmark run outputs
└── pipeline/                      # Open WebUI pipeline code
```

---

## 3. Naming Conventions

| Artifact | Convention | Example |
|----------|-----------|--------|
| Engineering spec | `AI-XXXX-Kebab-Title.md` | `AI-0001-Nemotron-Engineering-Spec.md` |
| Experiment | `EXP-XXXX-Kebab-Title.md` | `EXP-0001-Temperature.md` |
| Governance | `AI-9XXX-Kebab-Title.md` | `AI-9001-Documentation-Standard.md` |
| Benchmark TC | `TC-XXXX.md` | `TC-0001.md` |
| Config | `kebab-case.json` | `parameters.json` |
| Benchmark results | `YYYY-MM-DD-category-summary.md` | `2026-07-20-reasoning-summary.md` |

---

## 4. File Ownership

| Path | Owner | Access |
|------|-------|--------|
| `docs/00_ENGINEERING/` | Aldhie | Write: Owner only |
| `docs/05_EXPERIMENTS/` | Aldhie | Write: Owner |
| `docs/99_GOVERNANCE/` | Aldhie | Write: Owner |
| `configs/` | Aldhie | Write: Owner after benchmark validation |
| `benchmark/tests/` | Aldhie | Write: Owner |
| `benchmark/results/` | Aldhie | Write: Append-only |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial repository structure |
