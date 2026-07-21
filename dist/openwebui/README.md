# AI-OS · Open WebUI Deployment Package

**Version**: 2.0.0  
**Sprint**: C  
**Model**: NVIDIA Nemotron-3-Ultra-550B via NIM Free Tier  
**Runtime**: Open WebUI

This directory is the **deployable output** of the AI-OS runtime. It contains everything needed to deploy the runtime into Open WebUI with minimal manual work.

---

## Directory Structure

```
dist/openwebui/
├── compiled_prompt_v2.md          ← paste as System Prompt in OWU
├── model_config.json               ← model connection reference
├── filters/
│   ├── rpm_guard.py                ← inlet filter 1
│   ├── credential_scrub.py         ← inlet filter 2
│   ├── profile_selector.py         ← inlet filter 3
│   ├── context_budget_enforcer.py  ← inlet filter 4
│   └── response_quality_monitor.py ← outlet filter 5
├── parameter_profiles/
│   ├── discussion.json
│   ├── coding.json
│   ├── architecture.json
│   ├── analysis.json
│   ├── creative.json
│   ├── research.json
│   └── debugging.json
├── QUICKSTART.md                   ← start here
├── IMPORT_GUIDE.md
├── UPGRADE.md
└── ROLLBACK.md
```

---

## Deployment Time

Full deployment from zero: **10–15 minutes**.

See `QUICKSTART.md` for step-by-step instructions.

---

## Source of Truth

This `dist/` directory is generated from:

```
runtime/openwebui/
├── model/          ← prompt source modules + compiled prompts
├── filters/        ← filter source (full version with docs)
├── config/         ← all runtime config JSON
└── benchmark/      ← benchmark harness
```

Never edit `dist/` files directly. Edit source and regenerate.

---

## Quality Gate

Before promoting any change to `dist/`:

```
✓ Benchmark score ≥ 70
✓ All 5 filters install without error in Open WebUI
✓ Verification message passes: "What is the CAP theorem?"
✓ No placeholder text, no TODO, no unfinished sections
✓ model_config.json model ID matches actual NIM model name
```
