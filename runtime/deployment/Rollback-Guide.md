# Rollback Guide

> **Version**: 1.0.0

---

## When to Rollback

Rollback is triggered when:
- Evaluation scores drop >10% after an upgrade
- Critical bug detected in system prompt or parameters
- NIM API changes break parameter compatibility
- User-reported quality regression confirmed

---

## Rollback Process

### Fast Rollback (System Prompt Only)

1. Identify the last known-good commit in `main`
2. Copy `runtime/openwebui/model/system_prompt_v{N-1}.md`
3. Paste into Open WebUI model editor
4. Save

### Full Rollback (Config + Prompt)

1. Restore Open WebUI backup from `Upgrade-Guide.md` Step 2
2. Checkout previous runtime version from git:
   ```bash
   git log --oneline runtime/openwebui/exports/
   git show {commit}:runtime/openwebui/exports/model.json > model_rollback.json
   ```
3. Import `model_rollback.json` via Admin Panel → Models
4. Re-run verification from `OpenWebUI-Deployment.md` Step 7

---

## Rollback Versioning

Every compiled system prompt version is preserved:
- `system_prompt_v1.md`, `system_prompt_v2.md`, etc.
- Never delete old versions
- Git history provides the full audit trail
