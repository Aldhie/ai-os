# AI-OS — AI Operating System Engineering Repository

> **Version:** 0.1.0  
> **Status:** Active Development  
> **Owner:** Aldhie  
> **License:** MIT

---

## Purpose

This repository is the **single source of truth** for engineering, configuring, and evolving an AI Operating System built on:

- **Model:** NVIDIA Nemotron 3 Ultra 550B
- **Inference:** NVIDIA Cloud NIM (API-compatible)
- **Frontend:** Open WebUI

This is **NOT** application source code. It is an engineering documentation, architecture, benchmark, prompt, configuration, and dataset repository — designed to be maintainable for years.

---

## Architecture Diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│                        AI-OS STACK                              │
├─────────────────────────────────────────────────────────────────┤
│  USER INTERFACE                                                 │
│  └── Open WebUI  (Browser / PWA)                                │
├─────────────────────────────────────────────────────────────────┤
│  RUNTIME LAYER                                                  │
│  ├── Planner     (Task decomposition & goal tracking)           │
│  ├── Reflection  (Self-evaluation & correction loop)            │
│  └── Critic      (Output quality gating)                        │
├─────────────────────────────────────────────────────────────────┤
│  CONFIGURATION LAYER                                            │
│  ├── System Prompt  (Persona, rules, tone)                      │
│  ├── Parameters     (Temperature, top-p, max tokens, etc.)      │
│  ├── Memory Policy  (What to remember & for how long)           │
│  ├── Knowledge Policy (RAG sources, retrieval rules)            │
│  └── Tool Policy    (Which tools are enabled & when)            │
├─────────────────────────────────────────────────────────────────┤
│  INFERENCE ENGINE                                               │
│  └── NVIDIA Cloud NIM  (Nemotron 3 Ultra 550B endpoint)         │
├─────────────────────────────────────────────────────────────────┤
│  DATA LAYER                                                     │
│  ├── Dataset    (Curated training & evaluation data)            │
│  └── Fine-tune  (LoRA / PEFT adapters and recipes)              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Engineering Lifecycle

```text
  ┌──────────────┐
  │  Engineering │  ← Architecture decisions, specs, API contracts
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │Configuration │  ← System prompt, parameters, policies
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │   Runtime    │  ← Planner, Reflection, Critic, Workflow
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │   Dataset    │  ← Conversation logs, curated Q&A, eval sets
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │  Fine-Tune   │  ← LoRA recipes, PEFT scripts, adapter registry
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │  Benchmark   │  ← Regression, evaluation, performance tracking
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │   Release    │  ← Semantic version tag, changelog, deployment
  └──────────────┘
```

---

## Repository Structure

```text
ai-os/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── 00_ENGINEERING/         # Specs, ADR, API contracts
│   ├── 10_CONFIGURATION/       # System prompt, parameters, policies
│   ├── 20_RUNTIME/             # Planner, Reflection, Critic, Workflow
│   ├── 30_DATASET/             # Dataset documentation
│   ├── 40_FINETUNE/            # Fine-tuning recipes
│   └── 90_TESTING/             # Regression, evaluation, benchmark cases
├── prompts/
│   └── nemotron-ultra/         # Raw prompt files
├── configs/
│   └── openwebui/              # Open WebUI JSON configurations
├── benchmark/                  # Benchmark results and runner
├── dataset/                    # Curated datasets
└── scripts/                    # Automation and utility scripts
```

---

## Roadmap

### Phase 1 — Foundation (v0.1.x)

- [x] Repository initialized
- [ ] Engineering spec completed
- [ ] System prompt v1 finalized
- [ ] Parameters baseline established
- [ ] NVIDIA NIM API integration documented

### Phase 2 — Runtime Intelligence (v0.2.x)

- [ ] Planner workflow implemented
- [ ] Reflection loop documented
- [ ] Critic evaluation rules defined
- [ ] Memory & Knowledge policy v1

### Phase 3 — Data & Evaluation (v0.3.x)

- [ ] Dataset v1 curated (min 1,000 samples)
- [ ] Benchmark baseline established
- [ ] Regression test suite running
- [ ] Evaluation metrics defined

### Phase 4 — Fine-Tuning (v0.4.x)

- [ ] LoRA recipe for Nemotron Ultra documented
- [ ] PEFT adapter registry created
- [ ] Fine-tune evaluation pipeline ready

### Phase 5 — Release Candidate (v1.0.0)

- [ ] All documentation complete
- [ ] Benchmark scores acceptable
- [ ] Contribution guide reviewed
- [ ] First stable release tagged

---

## Versioning

This repository uses [Semantic Versioning](https://semver.org/):

- `MAJOR` — Breaking changes to architecture or API contracts
- `MINOR` — New features, new documents, new capabilities
- `PATCH` — Fixes, corrections, minor updates

---

## Contribution Guide

### Principles

1. **English only** for filenames, headers, and code.
2. **Markdown lint-friendly** — use standard Markdown, avoid raw HTML.
3. **Every file must have a header block** with: Title, Purpose, Scope, Version, Status, Owner, Dependencies, References, TODO.
4. **Semantic commits** — follow [Conventional Commits](https://www.conventionalcommits.org/).

### Commit Message Format

```text
<type>(<scope>): <subject>

Types: feat | fix | docs | refactor | test | chore
Scope: engineering | config | runtime | dataset | finetune | benchmark

Examples:
  feat(config): add memory policy v1
  docs(engineering): update NIM API spec
  fix(benchmark): correct evaluation metric formula
```

### Branch Strategy

```text
main          ← stable, tagged releases only
develop       ← integration branch
feature/*     ← new features and documents
fix/*         ← corrections and patches
```

### Pull Request Checklist

- [ ] File has complete header block
- [ ] Markdown lints cleanly
- [ ] References are linked
- [ ] TODO items are tracked
- [ ] Version bumped if applicable

---

## References

- [NVIDIA Nemotron Model Card](https://huggingface.co/nvidia/Nemotron-3-8B-Base-4k)
- [NVIDIA Cloud NIM Documentation](https://docs.api.nvidia.com/)
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
