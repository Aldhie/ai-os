# AI-OS · Open WebUI Rollback Guide

**Version**: 2.1.0  
**Sprint**: C

---

## When to Rollback

Initiate rollback if, after an upgrade, any of the following are observed:

- Benchmark score drops below 60 (was previously ≥ 70)
- RPM Guard is not blocking at 32 RPM
- Responses contain filler affirmations on > 20% of turns
- NIM inference errors spike above 5% of requests
- Context overflow errors appear on conversations < 30K tokens

---

## Rollback: System Prompt

To rollback to v1.0.0 compiled prompt:

1. Open WebUI → Admin Panel → Models → `ai-os-nemotron-ultra` → Edit
2. Replace System Prompt with contents of:
   `runtime/openwebui/model/compiled_prompt_v1.md`
3. Save
4. Send the CAP theorem test query and verify direct answer format

To rollback to v2.0.0 compiled prompt:

1. Same steps, use `dist/openwebui/compiled_prompt_v2.md` from the v2.0.0 git tag
   ```bash
   git show v2.0.0:runtime/openwebui/model/compiled_prompt_v1.md
   ```

---

## Rollback: Filters

If a specific filter is causing issues:

1. Open WebUI → Admin Panel → Functions
2. Locate the problematic filter
3. Toggle **Disable** (do not delete — preserves configuration)
4. Test the model without the filter
5. If issue resolves, the filter is the cause

To fully remove a filter:
1. Unassign from the model first (Model → Edit → Filters)
2. Then delete from Functions

**Safe to disable without service interruption:**
- `response_quality_monitor` (outlet only, never modifies response)
- `credential_scrub` (security impact: secrets may reach NIM; disable only for debugging)

**Do not disable without a fallback plan:**
- `rpm_guard` (disabling risks 429 errors from NIM)
- `profile_selector` (disabling reverts to default parameters for all tasks)
- `context_budget_enforcer` (disabling risks context overflow on long conversations)

---

## Rollback: Full Runtime

To roll back the entire AI-OS runtime to a previous git state:

```bash
# 1. Identify the target version
git log --oneline runtime/

# 2. Export compiled prompt from that commit
git show <commit-sha>:runtime/openwebui/model/compiled_prompt_v1.md > /tmp/rollback_prompt.md

# 3. Replace system prompt in Open WebUI with /tmp/rollback_prompt.md contents

# 4. For filter rollback, export from git and reinstall
git show <commit-sha>:runtime/openwebui/filters/rpm_guard.py > /tmp/rpm_guard_rollback.py
# Reinstall via Open WebUI Admin > Functions
```

---

## Emergency: NIM is Unresponsive

If NIM Free Tier is down or rate-limiting aggressively:

1. Disable `rpm_guard.py` temporarily (stops blocking users if RPM counter is miscounting)
2. Check NIM status: [status.nvidia.com](https://status.nvidia.com) `[verify]`
3. If downtime exceeds SLA tolerance, configure a fallback model:
   - Open WebUI → Admin Panel → Models → `ai-os-nemotron-ultra` → Edit
   - Temporarily change Base Model to an available alternative
   - The system prompt and filters remain active and compatible with any OpenAI-compatible model
