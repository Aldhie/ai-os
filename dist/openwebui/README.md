# AI-OS · Open WebUI Runtime Distribution Package

**Version**: 2.1.0  
**Sprint**: C  
**Status**: Production Ready

This directory contains everything needed to deploy the AI-OS runtime into Open WebUI.
All files are production-grade. No placeholders. No TODOs.

---

## Contents

```
dist/openwebui/
├── README.md                        This file
├── QUICKSTART.md                    Deploy in ~15 minutes
├── IMPORT_GUIDE.md                  Detailed artifact-by-artifact import
├── UPGRADE.md                       Version history + upgrade steps
├── ROLLBACK.md                      Rollback procedures and emergency recovery
├── compiled_prompt_v2.md            System prompt — paste into Open WebUI model
├── model_config.json                Model identity and NIM connection reference
└── filters/
    ├── rpm_guard.py                 Filter 1 (inlet) — 32 RPM enforcement
    ├── credential_scrub.py          Filter 2 (inlet) — credential redaction
    ├── profile_selector.py          Filter 3 (inlet) — task classification + params
    ├── context_budget_enforcer.py   Filter 4 (inlet) — 65K token ceiling
    └── response_quality_monitor.py  Filter 5 (outlet) — quality scoring
```

---

## Deployment Summary

| Component | Status | Where in Open WebUI |
|-----------|--------|--------------------|
| System Prompt v2.1.0 | ✅ Ready | Model > System Prompt |
| RPM Guard | ✅ Ready | Admin > Functions (Filter) |
| Credential Scrub | ✅ Ready | Admin > Functions (Filter) |
| Profile Selector | ✅ Ready | Admin > Functions (Filter) |
| Context Budget Enforcer | ✅ Ready | Admin > Functions (Filter) |
| Quality Monitor | ✅ Ready | Admin > Functions (Filter) |

---

## Runtime Architecture (What Happens on Each Turn)

```
User Message
    ↓
[Filter 1] RPM Guard         ← reject if > 32 req/min
    ↓
[Filter 2] Credential Scrub  ← redact secrets
    ↓
[Filter 3] Profile Selector  ← classify task, set temperature/tokens/reasoning_budget
    ↓
[Filter 4] Context Enforcer  ← truncate if > 65K tokens
    ↓
NVIDIA Cloud NIM (Nemotron Ultra)  ← inference with thinking enabled
    ↓
[Filter 5] Quality Monitor   ← measure response quality, attach metadata
    ↓
User Response
```

---

## Source Repository

All source files (with full documentation and comments) are at:
`runtime/openwebui/` in the [Aldhie/ai-os](https://github.com/Aldhie/ai-os) repository.

This `dist/` directory contains production copies optimised for direct paste into Open WebUI.

---

## Quick Start

See `QUICKSTART.md` for the 6-step deployment process (~15 minutes).
