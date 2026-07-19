# AI Operating System (AI-OS)

> **Engineering Repository** — Architecture, Benchmark, Prompts, Configuration & Dataset for NVIDIA Nemotron Ultra 550B via Open WebUI + NVIDIA Cloud NIM

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-active--development-yellow.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Purpose

This repository is **not source code**. It is the engineering backbone of an AI Operating System — a curated collection of:

- Engineering specifications and architecture decisions
- System prompts, planner, critic, and reflection prompts
- Configuration files for Open WebUI + NVIDIA Cloud NIM
- Benchmark cases, evaluation criteria, and regression tests
- Dataset schemas and fine-tuning strategies

The target model is **NVIDIA Nemotron 3 Ultra 550B** served via **NVIDIA Cloud NIM**, integrated with **Open WebUI**.

---

## Engineering Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI-OS Engineering Lifecycle                   │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│  1. Engineer │ 2. Configure │  3. Runtime  │   4. Dataset       │
│              │              │              │                    │
│  Spec, ADR,  │  SysPrompt,  │  Planner,    │  Collect, Label,   │
│  NIM API,    │  Params,     │  Critic,     │  Schema, Version   │
│  Arch Docs   │  Persona     │  Reflection  │                    │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────────┘
       │              │              │                │
       ▼              ▼              ▼                ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────────────┐
│ 5. Fine-Tune │ │6.Benchmark│ │  7. Release  │ │  8. Maintain     │
│              │ │          │ │              │ │                  │
│ LoRA, RLHF,  │ │ Eval,    │ │ Changelog,   │ │ Versioning,      │
│ SFT Dataset  │ │ Regress. │ │ Tag, Deploy  │ │ ADR updates      │
└──────────────┘ └──────────┘ └──────────────┘ └──────────────────┘
```

---

## Repository Structure

```
ai-os/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .gitignore                         # Ignored files
│
├── docs/
│   ├── 00_ENGINEERING/                # Core engineering specs
│   │   ├── AI-0001-Nemotron-Engineering-Spec.md
│   │   ├── AI-0002-NVIDIA-NIM-API.md
│   │   ├── AI-0003-OpenWebUI-Compatibility.md
│   │   ├── AI-0004-Benchmark.md
│   │   ├── AI-0005-FreeTier-Strategy.md
│   │   └── AI-0006-Architecture-Decision-Record.md
│   ├── 10_CONFIGURATION/              # Prompt & parameter configuration
│   │   ├── SystemPrompt.md
│   │   ├── Parameters.md
│   │   ├── MemoryPolicy.md
│   │   ├── KnowledgePolicy.md
│   │   ├── ToolPolicy.md
│   │   └── Persona.md
│   ├── 20_RUNTIME/                    # Runtime behavior
│   │   ├── Planner.md
│   │   ├── Reflection.md
│   │   ├── Critic.md
│   │   └── Workflow.md
│   ├── 30_DATASET/                    # Dataset documentation
│   │   └── README.md
│   ├── 40_FINETUNE/                   # Fine-tuning documentation
│   │   └── README.md
│   └── 90_TESTING/                    # Testing & evaluation
│       ├── Regression.md
│       ├── Evaluation.md
│       └── BenchmarkCases.md
│
├── prompts/
│   └── nemotron-ultra/                # Model-specific prompts
│       ├── system.txt
│       ├── planner.txt
│       ├── critic.txt
│       └── reflection.txt
│
├── configs/
│   └── openwebui/                     # Open WebUI configuration
│       ├── parameters.json
│       ├── capabilities.json
│       └── filters.json
│
├── benchmark/                         # Benchmark results
│   └── README.md
│
├── dataset/                           # Dataset files
│   └── README.md
│
└── scripts/                           # Utility scripts
    └── README.md
```

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                    User Interface                     │
│                    Open WebUI                         │
└───────────────────────┬──────────────────────────────┘
                        │  REST / WebSocket
┌───────────────────────▼──────────────────────────────┐
│               AI-OS Runtime Layer                     │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Planner │  │  Critic  │  │Reflection│             │
│  └────┬────┘  └────┬─────┘  └────┬─────┘             │
│       └────────────┴─────────────┘                   │
│                    │ Orchestration                    │
└────────────────────┼─────────────────────────────────┘
                     │  OpenAI-Compatible API
┌────────────────────▼─────────────────────────────────┐
│              NVIDIA Cloud NIM                         │
│         Nemotron 3 Ultra 550B Instruct                │
└──────────────────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│           Supporting Services                         │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │  Vector DB  │  │   Web Tools  │  │   Memory    │  │
│  │  (RAG)      │  │   (Search)   │  │   (Brain)   │  │
│  └─────────────┘  └──────────────┘  └─────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## Roadmap

| Version | Status | Description |
|---------|--------|-------------|
| v0.1.0  | ✅ Active | Initial engineering scaffold — specs, prompts, configs |
| v0.2.0  | 🔲 Planned | Complete system prompt v1 + NIM API integration spec |
| v0.3.0  | 🔲 Planned | Runtime workflow — Planner + Critic + Reflection loop |
| v0.4.0  | 🔲 Planned | Benchmark suite v1 — first 50 evaluation cases |
| v0.5.0  | 🔲 Planned | Dataset schema v1 + first labeled dataset |
| v0.6.0  | 🔲 Planned | Fine-tuning strategy — LoRA / SFT pipeline doc |
| v1.0.0  | 🔲 Planned | Production-ready AI-OS release |

---

## Versioning

This repository follows [Semantic Versioning 2.0.0](https://semver.org/).

- **MAJOR**: Breaking changes to architecture or prompt contract
- **MINOR**: New features, new docs, new benchmark sets
- **PATCH**: Fixes, clarifications, typo corrections

---

## Contribution Guide

### Adding a Document

1. Place the file in the correct `docs/` subfolder.
2. Follow the naming convention: `AI-XXXX-Title-In-Title-Case.md`
3. Every document must contain the standard header block (see any existing doc).
4. Use Markdown lint-friendly syntax (no trailing spaces, blank line before lists).

### Adding a Prompt

1. Place in `prompts/nemotron-ultra/` as a `.txt` file.
2. Document the prompt intent in `docs/10_CONFIGURATION/SystemPrompt.md`.
3. Version the prompt in the file header comment.

### Commit Convention

```
feat:     New feature or document
fix:      Fix error or outdated content
docs:     Documentation-only changes
refactor: Restructure without content change
benchmark: Benchmark-related additions
dataset:  Dataset changes
chore:    Maintenance tasks
```

### Pull Request

- One PR per logical change.
- Reference the relevant `AI-XXXX` document number in the PR description.
- All Markdown files must pass `markdownlint`.

---

## Owner

- **Owner**: [@Aldhie](https://github.com/Aldhie)
- **Created**: 2026-07-19
- **Version**: 0.1.0
- **Status**: Active Development
