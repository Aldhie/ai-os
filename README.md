# AI Operating System (AI-OS)

> **Engineering Repository** for building an AI Assistant based on **NVIDIA Nemotron 3 Ultra 550B** via Open WebUI + NVIDIA Cloud NIM.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Status](https://img.shields.io/badge/status-active-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Overview

This repository is **NOT source code**. It is the engineering backbone of the AI-OS project:

- Engineering specifications and architecture decisions
- System prompt design, parameter tuning, and runtime policies
- Benchmark cases and evaluation datasets
- Fine-tuning datasets and training configuration
- Operational scripts and automation helpers

All documentation is written in Markdown and follows semantic versioning.

---

## Lifecycle

```
Engineering
     |
     v
Configuration
     |
     v
Runtime
     |
     v
Dataset
     |
     v
Fine Tune
     |
     v
Benchmark
     |
     v
Release
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI-OS Stack                              │
│                                                                 │
│  ┌────────────────┐      ┌────────────────────────────────┐    │
│  │  Open WebUI    │─────▶│  NVIDIA Cloud NIM (API)        │    │
│  │  (Frontend)    │      │  Nemotron-3-Ultra-550B         │    │
│  └────────────────┘      └────────────────────────────────┘    │
│          │                              │                       │
│          ▼                              ▼                       │
│  ┌────────────────┐      ┌────────────────────────────────┐    │
│  │  System Prompt │      │  Knowledge Base / RAG          │    │
│  │  + Persona     │      │  (Datasets / Embeddings)       │    │
│  └────────────────┘      └────────────────────────────────┘    │
│          │                              │                       │
│          ▼                              ▼                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          Runtime: Planner → Reflection → Critic         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          Benchmark & Evaluation Pipeline                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
ai-os/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── 00_ENGINEERING/      # Specs, NIM API, OpenWebUI, Benchmark strategy
│   ├── 10_CONFIGURATION/    # Prompts, parameters, policies
│   ├── 20_RUNTIME/          # Planner, Reflection, Critic, Workflow
│   ├── 30_DATASET/          # Dataset management
│   ├── 40_FINETUNE/         # Fine-tuning strategy
│   └── 90_TESTING/          # Regression, evaluation, benchmark cases
├── prompts/
│   └── nemotron-ultra/      # Raw prompt files
├── configs/
│   └── openwebui/           # JSON configuration for Open WebUI
├── benchmark/               # Benchmark results and scripts
├── dataset/                 # Raw and processed datasets
└── scripts/                 # Utility and automation scripts
```

---

## Roadmap

| Version | Milestone | Status |
|---------|-----------|--------|
| v0.1.0 | Repository initialization, base structure | ✅ Done |
| v0.2.0 | Complete engineering spec (Nemotron, NIM API) | 🔄 In Progress |
| v0.3.0 | System prompt v1 + parameter tuning | ⏳ Planned |
| v0.4.0 | Runtime framework (Planner, Reflection, Critic) | ⏳ Planned |
| v0.5.0 | Benchmark baseline (first 50 test cases) | ⏳ Planned |
| v0.6.0 | Dataset v1 (curated Q&A and reasoning pairs) | ⏳ Planned |
| v0.7.0 | Fine-tuning experiment #1 | ⏳ Planned |
| v1.0.0 | Production-ready AI-OS release | ⏳ Planned |

---

## Contribution Guide

1. **Fork** the repository and create a feature branch: `git checkout -b feat/your-feature`
2. Follow the **file template** — all docs must include: Title, Purpose, Scope, Version, Status, Owner, Dependencies, References, TODO.
3. Use **Markdown lint-friendly** syntax (no trailing spaces, single blank line between sections).
4. Name files in **English**, using kebab-case or PascalCase as per existing convention.
5. Commit messages follow **Conventional Commits**: `feat:`, `fix:`, `docs:`, `chore:`.
6. Open a **Pull Request** with a clear description of the change.
7. All PRs require at least one review before merge.

---

## Owner

- **Project**: AI Operating System (AI-OS)
- **Maintainer**: Aldhie / Global Telko Informatika
- **Version**: 0.1.0
- **Last Updated**: 2026-07-19
