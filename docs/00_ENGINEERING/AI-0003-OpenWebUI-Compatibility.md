# AI-0003: Open WebUI Compatibility Specification

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-0003 |
| **Title** | Open WebUI Compatibility Specification |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the compatibility requirements between Open WebUI and the NVIDIA NIM/Nemotron backend, covering feature support, known gaps, configuration requirements, and version pinning.

---

## Scope

- Open WebUI version requirements
- Feature compatibility matrix
- Configuration requirements
- Known issues and workarounds
- Upgrade policy

---

## Dependencies

- `AI-0002-NVIDIA-NIM-API.md` — API connection layer
- `configs/openwebui/` — all configuration files

---

## References

- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
- [Open WebUI Changelog](https://github.com/open-webui/open-webui/releases)

---

## Version Requirements

| Component | Minimum Version | Recommended Version |
|-----------|----------------|--------------------|
| Open WebUI | 0.3.0 | Latest stable |
| Docker | 24.0 | Latest stable |
| Browser | Chrome 120+ / Firefox 120+ | Latest |

---

## Feature Compatibility Matrix

| Feature | Open WebUI Support | NIM Support | Status |
|---------|-------------------|-------------|--------|
| Chat completions | ✅ | ✅ | Working |
| Streaming responses | ✅ | ✅ | Working |
| System prompt | ✅ | ✅ | Working |
| Function calling | ✅ | ⚠️ TBD | Verify |
| Multi-modal (images) | ✅ | ❌ | Not supported |
| Embeddings | ✅ | ⚠️ TBD | Verify |
| Memory (RAG) | ✅ | N/A | Via OWUI |
| Tool use | ✅ | ⚠️ TBD | Verify |
| Web search | ✅ | N/A | Via OWUI |
| Code execution | ✅ | N/A | Via OWUI |

---

## Configuration Requirements

### Model Connection

Open WebUI must be configured with:

```
API Base URL: https://integrate.api.nvidia.com/v1
API Key: <NVIDIA_API_KEY>
Model ID: <nemotron-model-slug>
```

### Recommended Settings

See `configs/openwebui/parameters.json` for the full parameter set.

---

## Known Issues

| Issue | Status | Workaround |
|-------|--------|------------|
| TBD | TBD | TBD |

---

## TODO

- [ ] Verify function calling compatibility between Open WebUI and NIM
- [ ] Test embedding endpoint availability on NIM
- [ ] Document Docker Compose setup for Open WebUI + NIM
- [ ] Pin Open WebUI version for stable operation
- [ ] Document RAG (Retrieval Augmented Generation) configuration
