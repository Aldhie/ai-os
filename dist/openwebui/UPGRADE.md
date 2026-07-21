# AI-OS · Upgrade Guide

**Version**: 2.0.0  
**Sprint**: C

---

## Before Upgrading

1. **Note your current versions**: Check `compiled_prompt_v2.md` header comment for current version tag.
2. **Run benchmark baseline**: `python runtime/openwebui/benchmark/harness.py` — record current score.
3. **Export current model config**: Admin → Models → Export (if your OWU version supports it).
4. **Read the changelog** in the new `compiled_prompt_v2.md` header before proceeding.

---

## Upgrading the System Prompt

1. Open **Admin Panel** → **Models** → `AI-OS · Nemotron Ultra` → Edit
2. Replace **System Prompt** with full contents of the new `compiled_prompt_v2.md`
3. Save
4. Send verification message: `What is the CAP theorem?`
5. Run benchmark — confirm score ≥ previous baseline

---

## Upgrading a Filter

1. Admin → Functions → locate the filter by name
2. Edit → replace entire code with new version
3. Save (filter updates take effect immediately for new conversations)
4. Existing active conversations continue with the old filter until the user starts a new chat

---

## Version Compatibility Matrix

| Component | Backward Compatible | Notes |
|-----------|---------------------|-------|
| compiled_prompt v2 → v1 | No | v2 has stricter tool batching rules; downgrading removes them |
| Filters v1.x → v1.y | Yes | Patch versions are backward compatible |
| parameter_profiles v1 | Yes | Profile additions are additive |

---

## Rollback

If the new version produces lower benchmark scores, see `ROLLBACK.md`.
