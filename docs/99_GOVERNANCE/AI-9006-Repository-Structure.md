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
| [AI-9001](AI-9001-Documentation-Standard.md) | Document naming standard |
| [AI-9002](AI-9002-Benchmark-Standard.md) | Benchmark structure |
| [AI-9004](AI-9004-Versioning-Policy.md) | Version scheme |

---

## 1. Full Repository Map

```
Aldhie/ai-os/
│
├── README.md                          # Repository entry point
├── .gitignore
├── LICENSE
│
├── configs/                           # Runtime configuration files
│   └── openwebui/
│       ├── parameters.json            # Inference parameters (versioned)
│       └── capabilities.json          # Feature flags (versioned)
│
├── prompts/                           # Prompt library
│   ├── system/                        # System prompts per profile
│   └── task/                          # Task-specific prompts
│
├── benchmark/                         # Benchmark test cases
│   └── tests/
│       ├── discussion/
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
├── dataset/                           # Training and evaluation datasets
│
├── scripts/                           # Automation scripts
│
└── docs/
    ├── 00_ENGINEERING/                # Engineering specifications
    │   ├── AI-0001-Nemotron-Engineering-Spec.md
    │   ├── AI-0001-Nemotron-Engineering-Spec-Part2.md
    │   ├── AI-0002-NVIDIA-NIM-API.md
    │   ├── AI-0003-OpenWebUI-Compatibility.md
    │   ├── AI-0003-Critical-Findings-Audit.md
    │   ├── AI-0004-Benchmark.md
    │   ├── AI-0005-FreeTier-Strategy.md
    │   ├── AI-0006-Architecture-Decision-Record.md
    │   ├── REQ-INDEX.md
    │   └── AUDIT-2026-07-20.md
    │
    ├── 05_EXPERIMENTS/                # Experiment records
    │   ├── EXP-0001-Temperature.md
    │   ├── EXP-0002-TopP.md
    │   ├── EXP-0003-Thinking.md
    │   ├── EXP-0004-SystemPrompt.md
    │   ├── EXP-0005-Memory.md
    │   ├── EXP-0006-RAG.md
    │   ├── EXP-0007-Planner.md
    │   ├── EXP-0008-Reflection.md
    │   ├── EXP-0009-Critic.md
    │   └── EXP-0010-Agent.md
    │
    ├── 10_CONFIGURATION/              # Configuration documentation
    ├── 20_RUNTIME/                    # Operational runbooks
    ├── 30_DATASET/                    # Dataset documentation
    ├── 40_FINETUNE/                   # Fine-tuning specifications
    ├── 90_TESTING/                    # Test plans
    │
    └── 99_GOVERNANCE/                 # Standards and policies
        ├── AI-9001-Documentation-Standard.md
        ├── AI-9002-Benchmark-Standard.md
        ├── AI-9003-Prompt-Engineering-Standard.md
        ├── AI-9004-Versioning-Policy.md
        ├── AI-9005-Release-Process.md
        ├── AI-9006-Repository-Structure.md  ← you are here
        ├── AI-9007-Architecture-Principles.md
        └── AI-9008-Engineering-Decision-Record-Standard.md
```

---

## 2. Document ID Allocation

| Range | Category | Status |
|-------|----------|--------|
| AI-0001 – AI-0009 | Core Engineering Specs | Active allocation |
| AI-0010 – AI-0099 | Extended Engineering | Available |
| AI-9001 – AI-9009 | Governance | Active allocation |
| EXP-0001 – EXP-0099 | Experiments | Active allocation |
| BM-0001 – BM-9999 | Benchmark tracking | Active allocation |
| REQ-AI-0001 – REQ-AI-9999 | Requirements | Active allocation |

---

## 3. Naming Rules

| Rule | Pattern | Example |
|------|---------|--------|
| Engineering Spec | `AI-XXXX-Short-Title.md` | `AI-0001-Nemotron-Engineering-Spec.md` |
| Experiment | `EXP-XXXX-Short-Title.md` | `EXP-0001-Temperature.md` |
| Benchmark TC | `TC-XXXX.md` inside category folder | `reasoning/TC-0001.md` |
| Config file | `lowercase-hyphen.json` | `parameters.json` |
| Prompt file | `profile-type.md` | `reasoning-system.md` |

---

## 4. Folder Ownership

| Folder | Owner | Write Policy |
|--------|-------|--------------|
| `docs/00_ENGINEERING/` | Lead AI Architect | Requires review |
| `docs/05_EXPERIMENTS/` | All Engineers | Self-service |
| `docs/99_GOVERNANCE/` | Lead AI Architect | Restricted |
| `configs/` | Lead AI Architect | Requires version bump |
| `benchmark/` | All Engineers | Self-service |
| `prompts/` | All Engineers | Requires benchmark |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial structure document |
