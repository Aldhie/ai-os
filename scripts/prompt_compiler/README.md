# Prompt Compiler

> **Status**: IMPLEMENTATION | **Version**: 1.0.0 | **Owner**: Chief AI Systems Architect

---

## Purpose

The Prompt Compiler generates `system_prompt_v1.txt` deterministically from modular source files.

**No hand-written monolithic prompts.**  
**No copy-paste between files.**  
One source of truth per capability.

---

## Input Sources

```
runtime/openwebui/persona/identity.md          → WHO the AI is
runtime/openwebui/persona/conversation_style.md → HOW it talks
runtime/openwebui/persona/reasoning_style.md   → HOW it thinks
runtime/openwebui/persona/coding_mode.md       → coding behavior
runtime/openwebui/persona/architecture_mode.md → architecture behavior
runtime/openwebui/reasoning/thinking_profiles.md (reference)
runtime/openwebui/token/response_budget.md     (reference)
```

---

## Output

```
dist/openwebui/system_prompt_v1.txt    → production system prompt
dist/openwebui/system_prompt_v1.md     → human-readable annotated version
```

---

## Usage

```bash
cd scripts/prompt_compiler
python compile.py --profile standard --output ../../dist/openwebui/
python compile.py --profile coding --output ../../dist/openwebui/
python compile.py --validate          # validate all sources exist
python compile.py --diff              # diff against last compiled version
```

---

## Compilation Rules

1. Each section is extracted from its source file
2. Sections are assembled in the canonical order (see `compile.py`)
3. The output is deterministic: same input → same output always
4. The output includes a header comment with the source manifest
5. Whitespace and formatting are normalized
6. Any TODO or PLACEHOLDER in source files will cause compile to FAIL

---

*File: scripts/prompt_compiler/README.md | Last updated: 2026-07-20*
