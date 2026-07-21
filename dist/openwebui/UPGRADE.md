# AI-OS · Open WebUI Upgrade Guide

**Version**: 2.1.0  
**Sprint**: C

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-21 | Initial Sprint A release. Prompt compiler, 15 model modules, benchmark framework. |
| 2.0.0 | 2026-07-21 | Sprint B. 5 Python filters, benchmark harness (harness.py). |
| 2.1.0 | 2026-07-21 | Sprint C. Full runtime config (9 JSON configs), compiled_prompt_v2 with hardened tool batching, 20-turn long-context floor, explicit v2.1.0 constraints table. |

---

## Upgrading from v2.0.0 to v2.1.0

### What Changed

1. **compiled_prompt_v2.md** replaces compiled_prompt_v1.md
   - Tool batching rule is now a HARD CONSTRAINT (3 calls/turn maximum, explicit)
   - Long-context floor raised from 10 to 20 turns for decision summary
   - Critic threshold expanded: now mandatory for any irreversible action (not just architecture/security)
   - Hallucination guard extended: version numbers, release dates, benchmark scores now always require `[verify]`
   - Two new response length hard maximums added (1.5× rule made explicit)

2. **New runtime/openwebui/config/** directory
   - 9 production JSON configs: model, parameters, memory, knowledge, workflow, capabilities, tools, filters, profiles
   - Every config has a `why` field explaining its design rationale

3. **3 additional dist filters**
   - credential_scrub, context_budget_enforcer, response_quality_monitor now in `dist/`

### Upgrade Steps

1. **Update System Prompt**
   - Open WebUI → Models → `ai-os-nemotron-ultra` → Edit
   - Replace System Prompt with contents of `dist/openwebui/compiled_prompt_v2.md`
   - Save

2. **Install 3 new filters** (if upgrading from v2.0.0)
   - `dist/openwebui/filters/credential_scrub.py` — priority 2
   - `dist/openwebui/filters/context_budget_enforcer.py` — priority 4
   - `dist/openwebui/filters/response_quality_monitor.py` — priority 5

3. **Verify filter chain order** (priority 1 → 5)

4. **Run benchmark** to confirm score ≥ 70
   ```bash
   python runtime/openwebui/benchmark/harness.py \
     --base-url http://localhost:3000 \
     --api-key YOUR_KEY \
     --model-id ai-os-nemotron-ultra
   ```

---

## Pre-Upgrade Checklist

- [ ] Current benchmark score recorded (baseline)
- [ ] Current system prompt backed up
- [ ] Filter list exported from Open WebUI
- [ ] Test conversation saved for regression comparison

## Post-Upgrade Validation

- [ ] Benchmark score ≥ 70
- [ ] RPM Guard blocks at turn 33 in rapid-fire test
- [ ] Credential in test message is redacted
- [ ] Code question uses temperature 0.2 (check filter outlet metadata)
- [ ] Response does not start with "I" or filler affirmation
