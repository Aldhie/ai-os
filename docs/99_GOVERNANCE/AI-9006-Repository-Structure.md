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

## Cross-References

- [AI-9001 Documentation Standard](AI-9001-Documentation-Standard.md)
- [AI-9004 Versioning Policy](AI-9004-Versioning-Policy.md)
- [AI-9007 Architecture Principles](AI-9007-Architecture-Principles.md)

---

## 1. Purpose

Defines the canonical directory structure and naming conventions for `Aldhie/ai-os`. Every engineer working on this repository must follow this structure.

---

## 2. Full Repository Map

```
Aldhie/ai-os/
│
├── README.md                         ← Repository index and quick-start
├── LICENSE
├── .gitignore
│
├── docs/
│   ├── 00_ENGINEERING/               ← Core engineering specs, ADRs, requirements
│   │   ├── AI-0001-*.md              ← Nemotron Engineering Spec
│   │   ├── AI-0002-*.md              ← NVIDIA NIM API Reference
│   │   ├── AI-0003-*.md              ← Open WebUI Compatibility Matrix
│   │   ├── AI-0004-*.md              ← Benchmark Framework
│   │   ├── AI-0005-*.md              ← Free Tier Strategy
│   │   ├── AI-0006-*.md              ← Architecture Decision Record
│   │   ├── REQ-INDEX.md              ← All requirements (traceability index)
│   │   └── AUDIT-YYYY-MM-DD.md      ← Periodic audit reports
│   │
│   ├── 05_EXPERIMENTS/               ← Experiment design and results
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
│   │
│   ├── 10_CONFIGURATION/             ← Configuration documentation
│   │   └── CFG-0001-OpenWebUI.md
│   │
│   ├── 20_RUNTIME/                   ← Runtime procedures and runbooks
│   │   └── RUN-0001-Deployment.md
│   │
│   ├── 30_DATASET/                   ← Dataset documentation
│   │   └── DS-0001-Index.md
│   │
│   ├── 40_FINETUNE/                  ← Fine-tuning documentation
│   │   └── FT-0001-Strategy.md
│   │
│   ├── 90_TESTING/                   ← Test plans and test results
│   │   └── TST-0001-Plan.md
│   │
│   └── 99_GOVERNANCE/               ← Standards and governance
│       ├── AI-9001-Documentation-Standard.md
│       ├── AI-9002-Benchmark-Standard.md
│       ├── AI-9003-Prompt-Engineering-Standard.md
│       ├── AI-9004-Versioning-Policy.md
│       ├── AI-9005-Release-Process.md
│       ├── AI-9006-Repository-Structure.md  ← THIS FILE
│       ├── AI-9007-Architecture-Principles.md
│       └── AI-9008-Engineering-Decision-Record-Standard.md
│
├── benchmark/
│   └── tests/
│       ├── discussion/
│       │   ├── TC-0001.md
│       │   ├── TC-0002.md
│       │   └── TC-0003.md
│       ├── reasoning/
│       ├── planning/
│       ├── architecture/
│       ├── coding/
│       ├── debugging/
│       ├── hospitality/
│       ├── business/
│       ├── docker/
│       ├── openwebui/
│       ├── nim/
│       ├── memory/
│       └── rag/
│
├── configs/
│   └── openwebui/
│       ├── parameters.json           ← Active inference parameters
│       └── capabilities.json         ← Active feature flags
│
├── prompts/
│   ├── system/                       ← System prompts
│   ├── tasks/                        ← Task-specific prompts
│   ├── chains/                       ← Chain-of-thought scaffolds
│   ├── rag/                          ← RAG-augmented prompts
│   ├── tools/                        ← Tool-calling prompts
│   └── eval/                         ← Evaluation/critic prompts
│
├── dataset/                          ← Training and evaluation datasets
├── scripts/                          ← Automation and utility scripts
└── .github/
    └── workflows/                    ← CI/CD workflows
```

---

## 3. Naming Conventions

| Artifact | Convention | Example |
|----------|------------|--------|
| Engineering docs | `AI-NNNN-Short-Title.md` | `AI-0001-Nemotron-Engineering-Spec.md` |
| Experiment docs | `EXP-NNNN-Topic.md` | `EXP-0001-Temperature.md` |
| Benchmark TCs | `TC-NNNN.md` | `TC-0001.md` |
| Config files | `kebab-case.json` | `parameters.json` |
| Prompt files | `SP-NNNN-title.md` | `SP-0001-general-assistant.md` |
| Scripts | `snake_case.py/.sh` | `run_benchmark.py` |

---

## 4. Prohibited Structure Changes

1. Do not move `docs/00_ENGINEERING/` — all cross-references depend on this path
2. Do not rename files without updating ALL cross-references
3. Do not create `docs/01_*` through `docs/04_*` — reserved for future expansion
4. Do not store binary files in `docs/` — use `assets/` subdirectory

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
