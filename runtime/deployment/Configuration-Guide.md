# Configuration Guide

> **Version**: 1.0.0
> **Spec Ref**: AI-0003-OpenWebUI-Compatibility.md, runtime/openwebui/exports/

---

## Parameter Configuration

See `runtime/openwebui/exports/parameters.json` for the complete parameter matrix.

### Critical: Forbidden Parameters

Never configure these in Open WebUI for Nemotron Ultra:

| Parameter | Status | Reason |
|-----------|--------|--------|
| `top_k` | ❌ FORBIDDEN | NIM API error |
| `repetition_penalty` | ❌ FORBIDDEN | NIM API error |
| `thinking: true` (top-level) | ❌ FORBIDDEN | Silently ignored; use extra_body |
| `stop: ["</s>"]` | ❌ FORBIDDEN | Wrong model family |

---

## Profile Configuration

Profiles define parameter sets per task type.

To switch profiles manually:
1. Open the model
2. Click the (⚙️) gear icon in the chat
3. Apply parameters from the relevant profile JSON

Profile JSONs: `runtime/openwebui/profiles/`

---

## Thinking Mode Configuration

Thinking mode cannot be toggled via Open WebUI's native interface.

Current workarounds:
1. Use `/think` prefix in your message (requires Sprint 1.1 pipeline)
2. Direct API call with `extra_body.thinking`

Full pipeline code in Sprint 1.1.
Ref: `runtime/openwebui/model/thinking_policy.md`
