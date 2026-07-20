# Thinking Profiles Specification

> **Status**: RUNTIME | **Version**: 1.0.0 | **Owner**: Chief AI Systems Architect

---

## Profile Registry

```yaml
profiles:

  NONE:
    description: "Thinking disabled — direct retrieval/response"
    thinking_enabled: false
    budget_tokens: 0
    extra_body: {"thinking": {"type": "disabled"}}
    use_when: [greeting, simple_fact, short_command]

  LIGHT:
    description: "Minimal thinking for quick structured responses"
    thinking_enabled: true
    budget_tokens: 2000
    extra_body: {"thinking": {"type": "enabled", "budget_tokens": 2000}}
    use_when: [casual_question, simple_explanation, recommendation]

  STANDARD:
    description: "Standard analytical depth"
    thinking_enabled: true
    budget_tokens: 6000
    extra_body: {"thinking": {"type": "enabled", "budget_tokens": 6000}}
    use_when: [business_analysis, technical_explanation, research]

  DEEP:
    description: "Deep reasoning for complex tasks"
    thinking_enabled: true
    budget_tokens: 12000
    extra_body: {"thinking": {"type": "enabled", "budget_tokens": 12000}}
    use_when: [architecture_design, debugging, code_review, strategy]

  MAXIMUM:
    description: "Full reasoning budget for hardest problems"
    thinking_enabled: true
    budget_tokens: 20000
    extra_body: {"thinking": {"type": "enabled", "budget_tokens": 20000}}
    use_when: [mathematical_proof, complex_synthesis, expert_analysis]
    warning: "High latency + token cost — use sparingly on free tier"
```

---

## Profile Selection Logic

```python
def select_thinking_profile(task_class: str, user_override: str = None) -> str:
    if user_override in ["/think", "/nothink"]:
        return "MAXIMUM" if user_override == "/think" else "NONE"
    return TASK_PROFILE_MAP[task_class]
```

---

*File: runtime/openwebui/reasoning/thinking_profiles.md | Last updated: 2026-07-20*
