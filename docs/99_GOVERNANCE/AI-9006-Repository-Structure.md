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
| **Last Updated** | 2026-07-20 |
| **Category** | Governance |

---

## Cross References

- [AI-9001 — Documentation Standard](AI-9001-Documentation-Standard.md)
- [AI-9004 — Versioning Policy](AI-9004-Versioning-Policy.md)

---

## 1. Directory Tree

```
Aldhie/ai-os/
├── README.md                          # Repository overview
├── CHANGELOG.md                       # Release history
├── .gitignore
├── LICENSE
│
├── benchmark/
│   └── tests/
│       ├── discussion/                # TC-DISC-xxxx
│       ├── reasoning/                 # TC-REAS-xxxx
│       ├── planning/                  # TC-PLAN-xxxx
│       ├── architecture/              # TC-ARCH-xxxx
│       ├── coding/                    # TC-CODE-xxxx
│       ├── debugging/                 # TC-DEBG-xxxx
│       ├── hospitality/               # TC-HOSP-xxxx
│       ├── business/                  # TC-BUSI-xxxx
│       ├── docker/                    # TC-DOCK-xxxx
│       ├── openwebui/                 # TC-OWUI-xxxx
│       ├── nim/                       # TC-NIM-xxxx
│       ├── memory/                    # TC-MEMO-xxxx
│       └── rag/                       # TC-RAG-xxxx
│
├── configs/
│   └── openwebui/
│       ├── parameters.json            # v1.1.0 — production parameters
│       └── capabilities.json          # v1.1.0 — feature flags
│
├── dataset/                           # Training/fine-tune datasets
│
├── docs/
│   ├── 00_ENGINEERING/                # Core engineering specs
│   │   ├── AI-0001-Nemotron-Engineering-Spec.md
│   │   ├── AI-0001-Nemotron-Engineering-Spec-Part2.md
│   │   ├── AI-0002-NVIDIA-NIM-API.md
│   │   ├── AI-0003-OpenWebUI-Compatibility.md
│   │   ├── AI-0003-Critical-Findings-Audit.md
│   │   ├── AI-0004-Benchmark.md
│   │   ├── AI-0005-FreeTier-Strategy.md
│   │   └── AI-0006-Architecture-Decision-Record.md
│   ├── 05_EXPERIMENTS/                # Empirical investigation records
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
│   ├── 10_CONFIGURATION/              # Config documentation
│   ├── 20_RUNTIME/                    # Operational runbooks
│   ├── 30_DATASET/                    # Dataset documentation
│   ├── 40_FINETUNE/                   # Fine-tuning documentation
│   ├── 90_TESTING/                    # Testing documentation
│   └── 99_GOVERNANCE/                 # Standards and policies
│       ├── AI-9001-Documentation-Standard.md
│       ├── AI-9002-Benchmark-Standard.md
│       ├── AI-9003-Prompt-Engineering-Standard.md
│       ├── AI-9004-Versioning-Policy.md
│       ├── AI-9005-Release-Process.md
│       ├── AI-9006-Repository-Structure.md
│       ├── AI-9007-Architecture-Principles.md
│       └── AI-9008-Engineering-Decision-Record-Standard.md
│
├── prompts/
│   ├── system/                        # System prompts
│   ├── tasks/                         # Task-specific templates
│   ├── rag/                           # RAG context injection templates
│   └── tools/                         # Tool selection guidance
│
└── scripts/                           # Automation scripts
```

---

## 2. Naming Conventions

| Pattern | Example | Rule |
|---------|---------|------|
| Engineering spec | `AI-0001-Title.md` | Hyphen-separated, title case |
| Experiment | `EXP-0001-Title.md` | Three-digit number |
| Benchmark | `TC-[CAT]-[NUM].md` | Category code + 4-digit number |
| Config | `parameters.json`, `capabilities.json` | Lowercase |
| Prompt | `SP-001-reasoning.md` | SP + 3-digit + profile |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial structure definition |
