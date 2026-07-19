# AI-OS — AI Operating System Engineering Repository

> **Version:** 0.1.0 | **Status:** Active | **Owner:** Aldhie | **License:** MIT

This repository is the **engineering documentation hub** for building an AI Operating System powered by **NVIDIA Nemotron Ultra 550B** through **Open WebUI** and **NVIDIA Cloud NIM**.

It is **not** application source code. It contains:

- Engineering specifications and architecture decisions
- System prompt templates and persona definitions
- Runtime orchestration patterns (Planner, Critic, Reflection)
- Benchmark cases and evaluation frameworks
- Dataset schemas and fine-tuning guides
- Configuration files for Open WebUI and NIM APIs

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Operating System                    │
├──────────────┬──────────────┬──────────────┬───────────────┤
│   PLANNER    │    CRITIC    │  REFLECTION  │   WORKFLOW    │
│  (Strategy)  │  (Evaluate)  │   (Improve)  │  (Execution)  │
├──────────────┴──────────────┴──────────────┴───────────────┤
│              SYSTEM PROMPT + PERSONA + MEMORY               │
├─────────────────────────────────────────────────────────────┤
│          NVIDIA Nemotron Ultra 550B via NIM API             │
├─────────────────────────────────────────────────────────────┤
│                Open WebUI (Frontend Interface)              │
└─────────────────────────────────────────────────────────────┘
```

---

## Engineering Lifecycle

```
Engineering
     │
     ▼
Configuration
     │
     ▼
Runtime
     │
     ▼
Dataset
     │
     ▼
Fine Tune
     │
     ▼
Benchmark
     │
     ▼
Release
```

| Phase | Folder | Description |
|---|---|---|
| Engineering | `docs/00_ENGINEERING/` | Specs, ADRs, API docs, compatibility |
| Configuration | `docs/10_CONFIGURATION/` | Prompts, parameters, policies |
| Runtime | `docs/20_RUNTIME/` | Planner, Critic, Reflection, Workflow |
| Dataset | `docs/30_DATASET/` | Schema, sources, curation policy |
| Fine Tune | `docs/40_FINETUNE/` | Fine-tuning strategy and procedures |
| Benchmark | `docs/90_TESTING/` | Regression, evaluation, benchmark cases |
| Release | `CHANGELOG.md` | Semantic versioned release notes |

---

## Repository Structure

```
ai-os/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── 00_ENGINEERING/       # Core engineering specs and ADRs
│   ├── 10_CONFIGURATION/     # System prompt, parameters, policies
│   ├── 20_RUNTIME/           # Runtime orchestration patterns
│   ├── 30_DATASET/           # Dataset documentation
│   ├── 40_FINETUNE/          # Fine-tuning documentation
│   └── 90_TESTING/           # Benchmark and evaluation
├── prompts/
│   └── nemotron-ultra/       # Prompt templates for Nemotron Ultra
├── configs/
│   └── openwebui/            # Open WebUI configuration files
├── benchmark/                # Benchmark results and scripts
├── dataset/                  # Dataset samples and schemas
└── scripts/                  # Utility and automation scripts
```

---

## Roadmap

### v0.1.0 — Foundation (Current)

- [x] Repository structure initialized
- [x] Engineering specs drafted (AI-0001 to AI-0006)
- [x] System prompt and persona templates
- [x] Open WebUI base configuration

### v0.2.0 — Runtime

- [ ] Planner/Critic/Reflection prompts finalized
- [ ] Workflow automation documented
- [ ] Initial benchmark baseline established

### v0.3.0 — Dataset

- [ ] Dataset schema defined
- [ ] Curation pipeline documented
- [ ] First dataset version released

### v0.4.0 — Fine-Tune

- [ ] Fine-tuning strategy approved
- [ ] Training configuration documented
- [ ] Evaluation framework ready

### v1.0.0 — Production Release

- [ ] All specs reviewed and approved
- [ ] Benchmark baselines met
- [ ] Full documentation complete

---

## Contribution Guide

### Getting Started

1. Fork this repository.
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Follow the document template structure (Title, Purpose, Scope, Version, Status, Owner, Dependencies, References, TODO).
4. Use Markdown lint-friendly formatting (no trailing spaces, blank line before headings).
5. Submit a pull request with a clear description.

### Document Naming Convention

- Engineering specs: `AI-XXXX-Title.md` (e.g., `AI-0001-Nemotron-Engineering-Spec.md`)
- Configuration docs: `PascalCase.md` (e.g., `SystemPrompt.md`)
- Prompt files: `lowercase.txt` (e.g., `system.txt`)
- Config files: `lowercase.json` (e.g., `parameters.json`)

### Semantic Versioning

This repository follows [SemVer](https://semver.org/):

- **MAJOR**: Breaking architecture changes
- **MINOR**: New features or documents added
- **PATCH**: Corrections, clarifications, small updates

### Commit Message Format

```
feat: add new prompt template for critic
fix: correct parameter range in parameters.json
docs: update ADR-006 with new decision
chore: update .gitignore
```

---

## Dependencies

| Component | Version | Notes |
|---|---|---|
| NVIDIA Nemotron Ultra 550B | latest | Via NVIDIA Cloud NIM |
| Open WebUI | latest | Self-hosted or cloud |
| NVIDIA NIM API | v1 | REST API |

---

## License

MIT License. See [LICENSE](LICENSE).
