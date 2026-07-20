# Import Guide

> **Version**: 1.0.0

---

## Import Sequence

Import artifacts in this order:

1. `exports/model.json` → Admin Panel → Models → Import
2. `exports/knowledge.json` → Workspace → Knowledge (manual setup, JSON is reference only)
3. `exports/tools.json` → Workspace → Tools (manual setup, JSON is reference only)
4. `exports/filters.json` → Admin Panel → Pipelines (code in Sprint 1.1)

---

## What Can Be Imported Directly

| Artifact | Direct Import | Notes |
|----------|--------------|-------|
| `model.json` | ✅ Yes | Via Admin Panel → Models |
| `parameters.json` | ⚠️ Manual | Reference only; apply values in model editor |
| `capabilities.json` | ❌ No | Informational only |
| `memory.json` | ⚠️ Manual | Open WebUI memory config is in Admin Panel |
| `knowledge.json` | ⚠️ Manual | Create collections manually; JSON is config spec |
| `tools.json` | ⚠️ Manual | Enable tools in Workspace → Tools |
| `workflow.json` | ❌ No | Informational; Pipeline code in Sprint 1.1 |
| `filters.json` | ❌ No | Pipeline code in Sprint 1.1 |
| `profile.json` | ❌ No | Apply via model parameter presets manually |
