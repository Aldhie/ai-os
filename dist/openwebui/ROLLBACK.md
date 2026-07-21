# AI-OS · Rollback Guide

**Version**: 2.0.0  
**Sprint**: C

---

## When to Rollback

Rollback is warranted when:
- Benchmark score drops > 10 points vs previous baseline
- Filters produce unexpected rejections (RPM guard triggering on < 32 RPM)
- System prompt produces prohibited patterns consistently (filler affirmations, question restatement)

---

## Rollback Procedure

### System Prompt Rollback

1. Retrieve previous prompt from git:
   ```bash
   git show HEAD~1:dist/openwebui/compiled_prompt_v2.md > prompt_previous.md
   # or for v1:
   git show HEAD~1:runtime/openwebui/model/compiled_prompt_v1.md > prompt_v1.md
   ```
2. Paste previous prompt into Admin → Models → AI-OS · Nemotron Ultra → System Prompt
3. Save and verify

### Filter Rollback

```bash
# Get previous version of a specific filter
git show HEAD~1:dist/openwebui/filters/profile_selector.py > profile_selector_prev.py
```

Then paste into Admin → Functions → the affected filter → Edit → replace code.

### Emergency: Disable All Filters

If a filter is causing hard failures (500 errors, rejected messages):
1. Admin → Functions → toggle the problematic filter to **Disabled**
2. The model continues to work without the filter
3. Investigate and fix before re-enabling

---

## Post-Rollback

1. Run benchmark: confirm score returns to previous baseline
2. Open a GitHub issue in `Aldhie/ai-os` describing the regression
3. Tag the commit that caused the regression with `regression/<filter-or-prompt-name>`
