# AI-0003 — Open WebUI Compatibility

| Field | Value |
|-------|-------|
| **Title** | Open WebUI Compatibility |
| **Document ID** | AI-0003 |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | @Aldhie |
| **Created** | 2026-07-19 |
| **Updated** | 2026-07-19 |
| **Dependencies** | AI-0002 |

---

## Purpose

Defines how AI-OS is integrated with Open WebUI as the user interface layer. Covers version requirements, model connection, feature flags, tool/filter compatibility, and known issues.

---

## Scope

- Open WebUI version requirements
- Connection configuration to NVIDIA NIM
- Supported features in AI-OS context
- Tools and filters integration
- Memory and RAG integration
- Known compatibility issues

---

## Version Requirements

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| Open WebUI | 0.5.0 | Latest stable |
| Python | 3.11 | 3.12 |
| Docker | 24.x | Latest |
| Node.js (dev) | 20.x | 22.x |

---

## Connection Setup

### Step 1: Add NVIDIA NIM as OpenAI Connection

In Open WebUI: **Admin Panel → Settings → Connections → OpenAI API**

| Field | Value |
|-------|-------|
| API Base URL | `https://integrate.api.nvidia.com/v1` |
| API Key | `nvapi-xxxxxxxxxxxxxxxxxxxx` |

### Step 2: Enable the Model

In **Admin Panel → Models**, enable:

- `nvidia/nemotron-3-ultra-550b-instruct`

### Step 3: Apply System Prompt

Set the system prompt from `prompts/nemotron-ultra/system.txt` in:

**Admin Panel → Settings → Interface → Default System Prompt**

---

## Supported Features

| Feature | Supported | Notes |
|---------|-----------|-------|
| Streaming | ✅ | Enabled by default |
| System Prompt | ✅ | Set at model or user level |
| Tool Calling | ✅ | Requires Open WebUI >= 0.5 |
| RAG (Web) | ✅ | Native Open WebUI feature |
| Memory | ✅ | Via Brain Memory MCP |
| Image Input | ⚠️ | Model-dependent |
| Function Filters | ✅ | See `configs/openwebui/filters.json` |

---

## Configuration Files

| File | Purpose |
|------|---------|
| `configs/openwebui/parameters.json` | Inference parameter overrides |
| `configs/openwebui/capabilities.json` | Feature capability flags |
| `configs/openwebui/filters.json` | Input/output filter rules |

---

## Known Issues

| Issue | Status | Workaround |
|-------|--------|------------|
| Long system prompts may truncate at UI layer | Open | Keep system prompt < 2000 tokens |
| Tool call schema differences vs OpenAI | Open | Use standardized schema in ToolPolicy.md |

---

## References

- [Open WebUI Documentation](https://docs.openwebui.com)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
- AI-0002-NVIDIA-NIM-API.md
- docs/10_CONFIGURATION/ToolPolicy.md

---

## TODO

- [ ] Test with Open WebUI 0.6.x when available
- [ ] Document MCP server connection setup
- [ ] Add screenshot guide for UI configuration
- [ ] Test filter pipeline end-to-end
- [ ] Document Ollama vs OpenAI API mode differences
