# AI-9006: Repository Structure

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9006 |
| **Title** | Repository Structure and Navigation Guide |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | Full repository `Aldhie/ai-os` |
| **Cross-References** | [AI-9001](AI-9001-Documentation-Standard.md) · [AI-9004](AI-9004-Versioning-Policy.md) |

---

## 1. Purpose

This document is the canonical navigation map for the `Aldhie/ai-os` repository. Every new contributor must read this first. Every new folder must be registered here.

---

## 2. Repository Root Structure

```
Aldhie/ai-os/
├── README.md                    # Entry point — engineering overview
├── LICENSE
├── .gitignore
│
├── benchmark/                   # Test cases and benchmark results
│   ├── tests/
│   │   ├── reasoning/           # TC-0001 to TC-0003 reasoning tests
│   │   ├── coding/              # TC-0001 to TC-0003 coding tests
│   │   ├── discussion/          # TC-0001 to TC-0003 discussion tests
│   │   ├── planning/            # TC-0001 to TC-0003 planning tests
│   │   ├── architecture/        # TC-0001 to TC-0003 architecture tests
│   │   ├── debugging/           # TC-0001 to TC-0003 debugging tests
│   │   ├── hospitality/         # TC-0001 to TC-0003 hospitality tests
│   │   ├── business/            # TC-0001 to TC-0003 business tests
│   │   ├── docker/              # TC-0001 to TC-0003 docker tests
│   │   ├── openwebui/           # TC-0001 to TC-0003 OW integration tests
│   │   ├── nim/                 # TC-0001 to TC-0003 NIM API tests
│   │   ├── memory/              # TC-0001 to TC-0003 memory tests
│   │   └── rag/                 # TC-0001 to TC-0003 RAG tests
│   └── results/                 # Benchmark result records
│
├── configs/                     # Runtime configuration files
│   ├── openwebui/
│   │   ├── parameters.json      # v1.1.0 — API inference parameters
│   │   └── capabilities.json    # Feature flags
│   └── README.md               # Config documentation
│
├── dataset/                     # Training/evaluation datasets
│
├── docs/
│   ├── 00_ENGINEERING/          # Core engineering specifications
│   │   ├── AI-0001-*.md         # Nemotron Engineering Spec (Parts 1+2)
│   │   ├── AI-0002-*.md         # NVIDIA NIM API Reference
│   │   ├── AI-0003-*.md         # Open WebUI Compatibility Matrix + Audit
│   │   ├── AI-0004-*.md         # Benchmark Framework
│   │   ├── AI-0005-*.md         # Free Tier Strategy
│   │   ├── AI-0006-*.md         # Architecture Decision Record
│   │   ├── REQ-INDEX.md         # Requirement Traceability Index
│   │   └── AUDIT-*.md          # Repository audit records
│   │
│   ├── 05_EXPERIMENTS/          # Experiment records (EXP-xxxx)
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
│   ├── 10_CONFIGURATION/        # Configuration documentation
│   ├── 20_RUNTIME/              # Runtime and deployment docs
│   ├── 30_DATASET/              # Dataset documentation
│   ├── 40_FINETUNE/             # Fine-tuning documentation
│   ├── 90_TESTING/              # Testing documentation
│   └── 99_GOVERNANCE/           # Engineering standards
│       ├── AI-9001-Documentation-Standard.md
│       ├── AI-9002-Benchmark-Standard.md
│       ├── AI-9003-Prompt-Engineering-Standard.md
│       ├── AI-9004-Versioning-Policy.md
│       ├── AI-9005-Release-Process.md
│       ├── AI-9006-Repository-Structure.md    ← YOU ARE HERE
│       ├── AI-9007-Architecture-Principles.md
│       └── AI-9008-Engineering-Decision-Record-Standard.md
│
├── prompts/                     # System prompt templates
└── scripts/                     # Automation scripts
```

---

## 3. Document Dependency Graph

```
AI-0001 (Model Spec)
    ↓
AI-0002 (NIM API Reference)
    ↓
AI-0003 (OW Compatibility Matrix)
    ↓           ↓
AI-0003-Audit  AI-0004 (Benchmark)
    ↓               ↓
AI-0005         EXP-0001 to EXP-0010
(Free Tier)         ↓
    ↓           benchmark/tests/
    ↓
Configs (parameters.json, capabilities.json)
    ↓
Prompts (system prompt templates)
    ↓
AI-9001 to AI-9008 (Governance)
```

---

## 4. Key Engineering Files Quick Reference

| File | Purpose | Last Updated |
|------|---------|-------------|
| `configs/openwebui/parameters.json` | Production inference parameters | v1.1.0 — 2026-07-20 |
| `configs/openwebui/capabilities.json` | Feature flags | Needs update: enable function_calling |
| `docs/00_ENGINEERING/AI-0001-*.md` | Nemotron model spec (Part 1) | 2026-07-20 |
| `docs/00_ENGINEERING/AI-0001-*-Part2.md` | Nemotron model spec (Part 2) | 2026-07-20 |
| `docs/00_ENGINEERING/AI-0002-*.md` | NIM API parameters | 2026-07-20 |
| `docs/00_ENGINEERING/AI-0003-*.md` | OW compatibility matrix | v1.0.0 — 2026-07-20 |
| `docs/00_ENGINEERING/AI-0003-*-Audit.md` | Critical findings audit | v1.0.0 — 2026-07-20 |
| `docs/00_ENGINEERING/REQ-INDEX.md` | Requirement traceability | 2026-07-20 |

---

## 5. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release — production architecture refactor |
