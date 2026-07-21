# AI-OS · Rollback Guide

**Version**: 1.0.0

---

## Rollback Conditions

Initiate rollback if any of the following occur:

- Benchmark dimension score drops below 50/100 after upgrade
- NIM API error rate exceeds 5% over any 30-minute window
- RPM Guard triggers > 10 times per hour (indicates over-aggressive tool use)
- Compiled prompt causes NIM to ignore behaviour rules (verify with discussion_quality benchmark)

---

## Rollback Steps

1. Identify the last known-good `compiled_prompt_v1.md` version from the HTML comment header.
2. Find that commit in `Aldhie/ai-os` git history: `git log runtime/openwebui/model/compiled_prompt_v1.md`
3. Checkout the file: `git checkout <commit_sha> -- runtime/openwebui/model/compiled_prompt_v1.md`
4. Replace System Prompt in Open WebUI with rolled-back version.
5. Restore parameter profiles from the same commit if they also changed.
6. Re-run benchmark. Score must return to pre-upgrade baseline ± 3 points.
7. Open a GitHub issue in `Aldhie/ai-os` documenting the rollback reason and affected dimensions.

---

## Prevention

- Never deploy a new compiled prompt without running the full benchmark suite first.
- Compiled prompt version in the HTML comment header must be incremented on every change.
- Module changes must be reflected in `prompt_compiler.md` module list before recompile.
