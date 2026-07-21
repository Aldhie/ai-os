# AI-OS · Upgrade Guide

**Version**: 1.0.0  

---

## Before Upgrading

1. Note the current `compiled_prompt_v1.md` SHA from the model's System Prompt field.
2. Export current model config via Open WebUI API: `GET /api/models`
3. Record any active parameter overrides.

---

## Upgrade Steps

1. Pull latest from `Aldhie/ai-os` `main` branch.
2. Check `runtime/openwebui/model/compiled_prompt_v1.md` for changes (look at the `<!-- COMPILED: version=... -->` header).
3. If version changed, replace the System Prompt in Open WebUI with the new compiled prompt.
4. If `runtime/openwebui/profiles/*.json` changed, update model parameters for the relevant profiles.
5. If `runtime/openwebui/config/*.json` changed, update Filter implementations accordingly.
6. Run benchmark suite (`runtime/openwebui/benchmark/suite.json`) against the new version.
7. Compare scores to previous run. Investigate any dimension that dropped > 5 points.

---

## Version Compatibility

| AI-OS Version | Compiled Prompt Version | Open WebUI Minimum | NIM Model ID |
|---|---|---|---|
| Sprint A | 2.0.0 | 0.6.x | nvidia/nemotron-3-ultra-550b-a55b |

---

## Rollback Trigger

Rollback if any benchmark dimension scores below 50/100 after upgrade, or if NIM returns > 5% error rate in first 30 minutes.
