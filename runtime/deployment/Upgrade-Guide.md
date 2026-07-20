# Upgrade Guide

> **Version**: 1.0.0

---

## Upgrade Process

### Step 1 — Evaluate Before Upgrading

Before promoting any new runtime version:
1. Run evaluation framework against `runtime/evaluation/`
2. Compare scores against `runtime/evaluation/baseline/`
3. All scores must meet minimum passing scores (see `scoring/rubric_v1.md`)
4. No metric may regress by more than 5%

### Step 2 — Backup Current Config

```bash
# Export current Open WebUI config before upgrading
# Admin Panel → Settings → Export
```

### Step 3 — Apply Updates

1. Pull latest from `main` branch
2. Check `CHANGELOG.md` for breaking changes
3. Import updated `model.json` if changed
4. Update system prompt if `system_prompt_v1.md` changed
5. Update parameters if `parameters.json` changed

### Step 4 — Verify

Run the deployment verification steps from `OpenWebUI-Deployment.md` Step 7.

---

## Version Compatibility

| Runtime Version | Open WebUI Version | NIM API Version |
|-----------------|-------------------|----------------|
| 1.0.0 | ≥ 0.4.x | v1 |
