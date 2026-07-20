# Deployment Overview

> **Version**: 1.0.0
> **Sprint**: 1.0
> **Target**: Open WebUI + NVIDIA Cloud NIM

---

## What This Directory Contains

| File | Purpose |
|------|---------|
| `OpenWebUI-Deployment.md` | Step-by-step Open WebUI setup for Nemotron Ultra |
| `Import-Guide.md` | How to import runtime artifacts into Open WebUI |
| `Configuration-Guide.md` | Parameter and profile configuration reference |
| `Upgrade-Guide.md` | How to upgrade runtime versions safely |
| `Rollback-Guide.md` | How to rollback to a previous version |

---

## Prerequisites

- Open WebUI instance running (local Docker or cloud)
- NVIDIA NIM API key from [build.nvidia.com](https://build.nvidia.com)
- API key has access to `nvidia/nemotron-3-ultra-550b-a55b`
- Free Tier quota: 1,000 req/day, 40 RPM

Ref: AI-0002-NVIDIA-NIM-API.md, AI-0005-FreeTier-Strategy.md
