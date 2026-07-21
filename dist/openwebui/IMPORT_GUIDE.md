# AI-OS · Import Guide

**Version**: 1.0.0

This guide covers importing the AI-OS runtime into Open WebUI using the API or Admin UI.

---

## Option A — Admin UI (Manual)

Follow QUICKSTART.md steps 1–4. This is the zero-code path.

---

## Option B — Open WebUI API

### Create Model

```bash
curl -X POST https://YOUR_OPENWEBUI_HOST/api/models/create \
  -H "Authorization: Bearer $OPENWEBUI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @dist/openwebui/model_config.json
```

Before running, edit `dist/openwebui/model_config.json`:
- Replace `"SEE: runtime/openwebui/model/compiled_prompt_v1.md"` with the actual compiled prompt text.

---

## Option C — Environment Variable System Prompt

If running Open WebUI with Docker, inject the system prompt via environment:

```yaml
environment:
  - DEFAULT_MODELS=ai-os-nemotron-ultra
  - NVIDIA_API_KEY=nvapi-YOUR_KEY
```

This sets the default model but does not inject the system prompt automatically — use Option A or B for the prompt.

---

## Verify Import

```bash
curl https://YOUR_OPENWEBUI_HOST/api/models \
  -H "Authorization: Bearer $OPENWEBUI_API_KEY" \
  | python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"
```

Expected output includes: `ai-os-nemotron-ultra`
