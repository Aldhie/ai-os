# AI-0003 — Open WebUI Compatibility

| Field | Value |
|---|---|
| **Title** | Open WebUI Compatibility Specification |
| **Document ID** | AI-0003 |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Documents compatibility requirements, known issues, and configuration guidance for running Nemotron Ultra 550B via NVIDIA NIM inside Open WebUI. Serves as the integration specification between frontend and inference backend.

---

## Scope

- Open WebUI v0.4.x and later
- NVIDIA NIM as OpenAI-compatible external backend
- Features: Chat, Tools, RAG, Memory, Filters, Functions

---

## Integration Method

Open WebUI connects to NVIDIA NIM via the **OpenAI-compatible external connection** feature:

```text
Settings > Connections > OpenAI API
  Base URL: https://integrate.api.nvidia.com/v1
  API Key:  {NVIDIA_API_KEY}
```

Once configured, Nemotron Ultra will appear in the model selector.

---

## Feature Compatibility Matrix

| Feature | Supported | Notes |
|---|---|---|
| Chat Completions | ✅ Yes | Full support |
| Streaming | ✅ Yes | SSE native |
| System Prompt | ✅ Yes | Via messages[0] |
| Tool Calling | ⚠️ Partial | Verify schema |
| JSON Mode | ✅ Yes | response_format |
| RAG / Knowledge | ✅ Yes | Via Open WebUI |
| Memory | ✅ Yes | Open WebUI manages |
| Image Input | ❌ No | Text only |
| Audio Input | ❌ No | Not supported |
| Function Calling | ⚠️ Partial | Test required |
| Filters/Pipelines | ✅ Yes | Pre/post processing |

---

## Open WebUI Configuration

See `/configs/openwebui/` for all configuration files:

- `parameters.json` — Model parameters
- `capabilities.json` — Feature flags
- `filters.json` — Input/output filters

---

## Known Issues

| Issue | Severity | Status | Workaround |
|---|---|---|---|
| Tool schema mismatch | Medium | Investigating | Test manually |
| Long context truncation | Low | Open | Monitor tokens |
| SSE keepalive timeout | Low | Open | Set timeout >60s |

---

## Dependencies

- [AI-0002-NVIDIA-NIM-API.md](AI-0002-NVIDIA-NIM-API.md)
- `/configs/openwebui/parameters.json`
- `/configs/openwebui/capabilities.json`

---

## References

- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
- [Open WebUI Discord](https://discord.gg/5rJgQTnV4s)

---

## TODO

- [ ] Confirm tool calling schema compatibility
- [ ] Test RAG with Nemotron Ultra context window
- [ ] Document memory integration behavior
- [ ] Test filters pipeline with large outputs
- [ ] Document Open WebUI version requirements
