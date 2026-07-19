# AI Operating System Engineering Repository

> **Version:** 0.1.0 | **Status:** Active | **Owner:** Aldhie | **License:** MIT

This repository is the **engineering backbone** for building an AI Assistant based on **NVIDIA Nemotron 3 Ultra 550B** via **Open WebUI** + **NVIDIA Cloud NIM**.

It contains **no application source code**. Instead, it houses:

- Engineering specifications and architecture decisions
- System configuration (prompts, parameters, capabilities)
- Runtime behavior design (planner, critic, reflection, workflow)
- Dataset management and fine-tuning strategy
- Benchmarks and evaluation cases
- Scripts for automation and maintenance

---

## Repository Purpose

This repository serves as the **single source of truth** for designing, configuring, operating, and improving an AI OS. It is intended to be maintained for **years**, evolving with the model, tooling, and use-case requirements.

---

## Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                   AI OS ENGINEERING LIFECYCLE               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [00] ENGINEERING  →  Specs, ADR, API, Architecture        │
│           ↓                                                 │
│   [10] CONFIGURATION →  System Prompt, Parameters, Policy   │
│           ↓                                                 │
│   [20] RUNTIME      →  Planner, Critic, Reflection          │
│           ↓                                                 │
│   [30] DATASET      →  Curated Inputs, Labels, Splits       │
│           ↓                                                 │
│   [40] FINE TUNE    →  LoRA, PEFT, Training Config          │
│           ↓                                                 │
│   [90] BENCHMARK    →  Regression, Evaluation, Cases        │
│           ↓                                                 │
│         RELEASE     →  Tag, Changelog, Deploy               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                        │
│                    Open WebUI (Self-hosted / Cloud)                │
└───────────────────────────┬────────────────────────────────────────┘
                            │  REST / WebSocket
┌───────────────────────────▼────────────────────────────────────────┐
│                       RUNTIME LAYER                                │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────┐  │
│  │   Planner   │  │   Critic     │  │ Reflection │  │ Workflow │  │
│  └──────┬──────┘  └──────┬───────┘  └─────┬──────┘  └────┬─────┘  │
│         └────────────────┴────────────────┴──────────────┘        │
│                           ↓ Prompt Construction                    │
└───────────────────────────┬────────────────────────────────────────┘
                            │  OpenAI-compatible API
┌───────────────────────────▼────────────────────────────────────────┐
│                    NVIDIA CLOUD NIM LAYER                          │
│            nvidia/llama-3.1-nemotron-ultra-253b-v1                 │
│                   (Nemotron Ultra 550B equiv.)                     │
└───────────────────────────┬────────────────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────────────────┐
│                   KNOWLEDGE & MEMORY LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  RAG / Docs  │  │  Tool Calls  │  │  Long-term Memory Store  │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
ai-os/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── 00_ENGINEERING/       # Specs, API, ADR, Benchmarks
│   ├── 10_CONFIGURATION/     # Prompts, Parameters, Policies
│   ├── 20_RUNTIME/           # Planner, Critic, Reflection
│   ├── 30_DATASET/           # Dataset strategy
│   ├── 40_FINETUNE/          # Fine-tuning strategy
│   └── 90_TESTING/           # Regression, Evaluation
├── prompts/
│   └── nemotron-ultra/       # Production prompt files
├── configs/
│   └── openwebui/            # Open WebUI JSON configs
├── benchmark/                # Benchmark results
├── dataset/                  # Curated datasets
└── scripts/                  # Utility scripts
```

---

## Roadmap

| Version | Milestone | Target | Status |
|---------|-----------|--------|--------|
| 0.1.0 | Repository initialization, structure, templates | Q3 2026 | ✅ Done |
| 0.2.0 | Complete engineering specs & architecture decisions | Q3 2026 | 🔄 In Progress |
| 0.3.0 | System prompt v1 + parameters tuned | Q3 2026 | 📋 Planned |
| 0.4.0 | Runtime planner + critic + reflection operational | Q4 2026 | 📋 Planned |
| 0.5.0 | Initial dataset curation | Q4 2026 | 📋 Planned |
| 0.6.0 | Benchmark baseline established | Q4 2026 | 📋 Planned |
| 0.7.0 | Fine-tuning experiment v1 | Q1 2027 | 📋 Planned |
| 1.0.0 | Stable production-ready AI OS configuration | Q2 2027 | 📋 Planned |

---

## Versioning

This repository uses [Semantic Versioning](https://semver.org/):

- **MAJOR** — Breaking changes to system architecture or prompt interface
- **MINOR** — New features, policies, or components
- **PATCH** — Fixes, clarifications, typo corrections

---

## Contribution Guide

### Filing Issues

1. Use the GitHub Issues tracker.
2. Label clearly: `bug`, `enhancement`, `documentation`, `benchmark`.
3. Include version, context, and expected vs. actual behavior.

### Submitting Changes

1. Fork the repository.
2. Create a branch: `feat/your-feature` or `fix/your-fix`.
3. Follow the file header template (Title, Purpose, Scope, Version, Status, Owner, Dependencies, References, TODO).
4. Run Markdown lint before committing.
5. Open a Pull Request with a clear description.

### Commit Convention

```
feat:     New feature or document
fix:      Bug fix or correction
docs:     Documentation only changes
chore:    Maintenance, tooling
benchmark: Benchmark additions or updates
config:   Configuration changes
```

### File Naming Convention

- English only
- Kebab-case for folders: `00_ENGINEERING`
- PascalCase for Markdown files: `SystemPrompt.md`
- Prefix engineering docs: `AI-XXXX-Title.md`
- Lowercase with hyphens for prompt/config files

---

## Dependencies

| Component | Version | Purpose |
|-----------|---------|----------|
| Open WebUI | ≥ 0.4.x | AI frontend and orchestration |
| NVIDIA NIM | Cloud API | Nemotron Ultra inference |
| Nemotron Ultra 550B | Latest | Core language model |

---

## References

- [NVIDIA NIM Documentation](https://docs.api.nvidia.com/)
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Nemotron Model Card](https://huggingface.co/nvidia/Llama-3_1-Nemotron-Ultra-253B-v1)
- [Semantic Versioning](https://semver.org/)
