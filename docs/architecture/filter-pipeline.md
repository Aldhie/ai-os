# AI-OS Filter Pipeline — Architecture Reference

> Version: 1.0.0 | Sprint C | Last updated: 2026-07-21

## Canonical Pipeline (Gen 2)

Install these filters in Open WebUI in the following order. Order matters — inlet filters run top-to-bottom, outlet filters run bottom-to-top.

```
Request (user message)
        ↑
  [INLET 1]  credential_scrub         v1.0.0  -- redact secrets before NIM sees them
  [INLET 2]  rpm_guard                v1.0.0  -- reject if 32 RPM ceiling reached
  [INLET 3]  context_budget_enforcer  v1.1.0  -- truncate oldest msgs if > 65,536 tokens
  [INLET 4]  profile_selector         v1.3.0  -- apply temperature + max_tokens by task_class
        ↓
  [NIM INFERENCE]
        ↓
  [OUTLET 4] profile_selector         v1.3.0  -- pass-through
  [OUTLET 3] context_budget_enforcer  v1.1.0  -- pass-through
  [OUTLET 2] rpm_guard                v1.0.0  -- pass-through
  [OUTLET 1] response_quality_monitor v1.2.0  -- score quality, store in self._state
        ↓
Response (assistant message)
```

> Note: `response_quality_monitor` is installed as a **separate filter** after the pipeline above, outlet-only. It does not have an inlet role.

## Inter-Filter Communication

| From | To | Channel | Key |
|---|---|---|---|
| `profile_selector` | `response_quality_monitor` | Module-level registry | `_TASK_CLASS_REGISTRY[user_id]` |

No filter writes task_class or quality data to `body` top-level or `body["metadata"]`. Body is passed through unmodified except for:
- `credential_scrub`: mutates `body["messages"][-1]["content"]` (last user msg only) if credential detected
- `context_budget_enforcer`: mutates `body["messages"]` (truncation) if over ceiling
- `profile_selector`: writes `body["temperature"]` and `body["max_tokens"]` (OpenAI-spec top-level keys)

## Deprecated Filters (Gen 1 — Do Not Install)

| File | Replaced By | Reason |
|---|---|---|
| `task_classifier.py` | `profile_selector.py` | Used `body["metadata"]` contract |
| `outlet_monitors.py` | `response_quality_monitor.py` | Depended on Gen 1 metadata |
| `context_budget.py` | `context_budget_enforcer.py` | Duplicate — double-truncation risk |

Deprecated files are renamed to `DEPRECATED_*.py.txt` to prevent accidental installation.

## Valve Reference

### credential_scrub
| Valve | Default | Description |
|---|---|---|
| `enabled` | `True` | Enable/disable scrubbing |
| `redaction_placeholder` | `[REDACTED-CREDENTIAL]` | Replacement string |

### rpm_guard
| Valve | Default | Description |
|---|---|---|
| `enabled` | `True` | Enable/disable RPM guard |
| `max_rpm` | `32` | NIM Free Tier ceiling |
| `window_seconds` | `60` | Rolling window |

### context_budget_enforcer
| Valve | Default | Description |
|---|---|---|
| `enabled` | `True` | Enable/disable truncation |
| `max_context_tokens` | `65536` | Token ceiling |
| `tokens_per_char_estimate` | `0.25` | ~4 chars/token |
| `min_history_turns` | `3` | Min turn-pairs to preserve |

### profile_selector
| Valve | Default | Description |
|---|---|---|
| `enabled` | `True` | Enable/disable profile selection |
| `default_profile` | `discussion` | Fallback task class |
| `enable_thinking` | **`False`** | **Keep False on NIM Free Tier** |

### response_quality_monitor
| Valve | Default | Description |
|---|---|---|
| `enabled` | `True` | Enable/disable monitoring |
| `log_to_console` | `False` | Debug print to server console |

## NIM Free Tier Constraints

- **32 RPM hard ceiling** — enforced by `rpm_guard`
- **65,536 token practical context limit** — enforced by `context_budget_enforcer`
- **`enable_thinking` not supported** — keep `profile_selector` Valve at `False`
- **`chat_template_kwargs` rejected** — only injected when `enable_thinking=True`
- **`num_predict` rejected** — use `max_tokens` (OpenAI spec)
- **`options` key rejected** — write params to body top-level directly
