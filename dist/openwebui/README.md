# OpenWebUI Import Package

> **Status**: DISTRIBUTION | **Version**: 1.0.0 | **Owner**: Chief AI Systems Architect

---

## Purpose

This directory contains production-ready artifacts for direct import into Open WebUI.

Everything here is **output** — generated, not hand-written.

---

## Contents

```
dist/openwebui/
├── system_prompt_standard.txt   → compiled standard system prompt
├── system_prompt_coding.txt     → compiled coding-mode system prompt  
├── parameter_profiles/
│   ├── profile_minimal.json      → greeting/simple tasks
│   ├── profile_standard.json     → most tasks
│   ├── profile_deep.json         → complex analysis
│   └── profile_maximum.json      → hardest tasks
├── model_config.json           → NIM model configuration
└── README.md
```

---

## How to Import into Open WebUI

### System Prompt
1. Open WebUI → Admin Panel → Models
2. Select Nemotron Ultra
3. Paste contents of `system_prompt_standard.txt` into System Prompt field
4. Save

### Parameter Profile
1. For a chat session: click the ⚙️ gear icon → Advanced Parameters
2. Apply values from the appropriate `profile_*.json`
3. Or: create a Model Preset with these values

### Regenerate Prompts
```bash
python scripts/prompt_compiler/compile.py --profile standard
python scripts/prompt_compiler/compile.py --profile standard --mode coding
```

---

*File: dist/openwebui/README.md | Last updated: 2026-07-20*
