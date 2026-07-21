# AI-OS · Open WebUI Import Guide

**Version**: 2.1.0  
**Sprint**: C

This guide covers manual import of each runtime artifact. For automated deployment, see `QUICKSTART.md`.

---

## Artifact Map

| Artifact | Location | Import Method | Target in Open WebUI |
|----------|----------|--------------|---------------------|
| Compiled System Prompt | `dist/openwebui/compiled_prompt_v2.md` | Paste into Model > System Prompt | Model settings |
| RPM Guard Filter | `dist/openwebui/filters/rpm_guard.py` | Admin > Functions > New Filter | Assign to model |
| Credential Scrub Filter | `dist/openwebui/filters/credential_scrub.py` | Admin > Functions > New Filter | Assign to model |
| Profile Selector Filter | `dist/openwebui/filters/profile_selector.py` | Admin > Functions > New Filter | Assign to model |
| Context Budget Filter | `dist/openwebui/filters/context_budget_enforcer.py` | Admin > Functions > New Filter | Assign to model |
| Quality Monitor Filter | `dist/openwebui/filters/response_quality_monitor.py` | Admin > Functions > New Filter | Assign to model |
| Parameter Profiles | `runtime/openwebui/config/profiles.json` | Reference only — applied by profile_selector.py | N/A |
| Workflow Config | `runtime/openwebui/config/workflow.json` | Reference only — documents pipeline order | N/A |

---

## System Prompt Import

1. Open `dist/openwebui/compiled_prompt_v2.md`
2. Copy **all content** including the HTML comment header
3. Open WebUI → Admin Panel → Models → `ai-os-nemotron-ultra` → Edit
4. Paste into **System Prompt** field
5. Save

> The HTML comment block at the top is not rendered by the model. It serves as version metadata for operators.

---

## Filter Import

Filters must be imported in priority order to ensure correct pipeline execution:

```
priority 1: rpm_guard         (inlet)  blocks excess RPM before any processing
priority 2: credential_scrub  (inlet)  redacts secrets before NIM receives them
priority 3: profile_selector  (inlet)  classifies task + sets parameters
priority 4: context_enforcer  (inlet)  truncates context at 65K token ceiling
priority 5: quality_monitor   (outlet) measures response quality post-NIM
```

For each filter:
1. Admin Panel → Functions → **+ New Function**
2. Type: **Filter**
3. Paste file contents
4. **Name** must match the display name in `filters.json`
5. Save → Enable
6. Go to the model → Edit → Filters tab → assign the filter

---

## Valve Configuration

Each filter exposes configurable valves. Production defaults are set correctly.
Change only if your deployment conditions differ:

| Filter | Valve | Production Default | Change When |
|--------|-------|--------------------|-------------|
| RPM Guard | `max_rpm` | `32` | NIM tier changes |
| Context Enforcer | `max_context_tokens` | `65536` | Free Tier improves |
| Profile Selector | `default_profile` | `discussion` | Primary use case changes |
| Quality Monitor | `append_quality_metadata` | `false` | Debugging benchmark runs only |

---

## Verifying Import

After importing all artifacts, run the verification check from `QUICKSTART.md` Step 5.

A fully imported and functional AI-OS runtime will:
1. Answer directly without preamble
2. Match language (EN/ID) automatically
3. Block messages when 32 RPM is exceeded
4. Redact credentials silently
5. Apply lower temperature automatically for code questions
6. Truncate context gracefully in long conversations
