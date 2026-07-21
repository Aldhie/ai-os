# AI-OS · Open WebUI Filters

**Version**: 1.0.0  
**Sprint**: B

This directory contains production Python Filter implementations for Open WebUI.
Each filter has a single responsibility and can be installed, enabled, or disabled independently.

---

## Installation

1. Open WebUI → **Admin Panel** → **Functions** → **+ New Function**
2. Set type: **Filter**
3. Paste the contents of the `.py` file
4. Save and enable
5. Assign to the `AI-OS · Nemotron Ultra` model

---

## Filter Chain (Install in This Order)

| Priority | File | Responsibility | Type |
|----------|------|----------------|------|
| 1 | `rpm_guard.py` | Enforce 32 RPM NIM Free Tier ceiling | Inlet |
| 2 | `credential_scrub.py` | Redact API keys and secrets before NIM | Inlet |
| 3 | `profile_selector.py` | Classify task + apply parameter profile | Inlet |
| 4 | `context_budget_enforcer.py` | Truncate context at 65,536 token ceiling | Inlet |
| 5 | `response_quality_monitor.py` | Measure quality signals on outlet | Outlet |

---

## Filter Dependencies

- `profile_selector.py` writes `_ai_os_task_class` to body — read by `response_quality_monitor.py`
- `context_budget_enforcer.py` reads `_ai_os_task_class` (optional, for per-profile budget)
- `response_quality_monitor.py` reads `_ai_os_rag_used` (set by RAG pipeline if applicable)

---

## Configurable Valves

Each filter exposes `Valves` that can be adjusted per-user or globally in Open WebUI:

| Filter | Key Valve | Default | Notes |
|--------|-----------|---------|-------|
| RPM Guard | `max_rpm` | 32 | Change only if NIM tier changes |
| Credential Scrub | `redaction_placeholder` | `[REDACTED-CREDENTIAL]` | |
| Profile Selector | `default_profile` | `discussion` | |
| Context Enforcer | `max_context_tokens` | 65536 | Adjust if Free Tier improves |
| Quality Monitor | `append_quality_metadata` | `false` | Set `true` for benchmark debug runs |

---

## Testing Filters Locally

```python
# Example: test profile_selector.py
from profile_selector import Filter

f = Filter()
body = {
    "messages": [{"role": "user", "content": "Write a Python function to parse JSON"}],
    "options": {}
}
result = f.inlet(body)
assert result["_ai_os_task_class"] == "coding"
assert result["options"]["temperature"] == 0.2
assert result["extra_body"]["reasoning_budget"] == 4096
print("PASS")
```
