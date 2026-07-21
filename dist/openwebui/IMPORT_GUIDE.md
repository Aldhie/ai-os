# AI-OS · Import Guide

**Version**: 2.0.0  
**Sprint**: C

This guide describes what each file in this `dist/openwebui/` directory does and where it goes in Open WebUI.

---

## File Map

| File | Destination in Open WebUI | Action |
|------|--------------------------|--------|
| `compiled_prompt_v2.md` | Admin → Models → AI-OS · Nemotron Ultra → System Prompt | Paste full contents |
| `model_config.json` | Reference only | Use values to manually configure model record |
| `filters/rpm_guard.py` | Admin → Functions → New Filter | Paste and enable |
| `filters/credential_scrub.py` | Admin → Functions → New Filter | Paste and enable |
| `filters/profile_selector.py` | Admin → Functions → New Filter | Paste and enable |
| `filters/context_budget_enforcer.py` | Admin → Functions → New Filter | Paste and enable |
| `filters/response_quality_monitor.py` | Admin → Functions → New Filter | Paste and enable |
| `parameter_profiles/*.json` | Reference only | Values already embedded in profile_selector.py |
| `QUICKSTART.md` | — | Read first |
| `UPGRADE.md` | — | Read before upgrading |
| `ROLLBACK.md` | — | Read before rollback |

---

## Configuration Source of Truth

All runtime configuration lives in `runtime/openwebui/config/`:  
`model.json` → `parameters.json` → `memory.json` → `knowledge.json` → `workflow.json` → `capabilities.json` → `tools.json` → `profiles.json` → `filters.json`

The `dist/` files are the **deployable output** of those configs. Never edit `dist/` files directly — edit the source in `runtime/openwebui/config/` and regenerate.

---

## Open WebUI Version Compatibility

| Feature | Min OWU Version |
|---------|----------------|
| Filter (Python) | 0.3.x |
| Model System Prompt | 0.1.x |
| Extended Thinking UI | 0.4.x |
| Tool Assignment | 0.3.x |
