# System Prompt Compiler

> **Version**: 1.0.0
> **Spec Ref**: AI-0001, AI-0003-OpenWebUI-Compatibility

---

## Purpose

This document defines how the compiled `system_prompt_v1.md` is assembled from modular policy components. When any policy module changes, this compiler document governs what gets regenerated.

---

## Compilation Architecture

```
behavior_spec.md          → [IDENTITY] + [BEHAVIORAL CORE]
reasoning_policy.md       → [REASONING]
memory_policy_v1.md       → [MEMORY]
knowledge_loading.md      → [KNOWLEDGE]
tool_routing.md           → [TOOLS]
conversation_policy.md    → [CONVERSATION]
coding_policy.md          → [CODING]
planning_policy.md        → [PLANNING]
quality_policy.md         → [SELF-CRITIQUE]
response_policy.md        → [RESPONSE FORMAT]
behavior_spec.md          → [CONSTRAINTS]
                              ↓
                    system_prompt_v1.md (compiled)
```

---

## Compilation Rules

### Rule 1 — Module Order
Modules must compile in this order:
1. IDENTITY (behavior_spec)
2. BEHAVIORAL CORE (behavior_spec)
3. REASONING (reasoning_policy)
4. MEMORY (memory_policy_v1)
5. KNOWLEDGE (knowledge_loading)
6. TOOLS (tool_routing)
7. CONVERSATION (conversation_policy)
8. CODING (coding_policy)
9. PLANNING (planning_policy)
10. SELF-CRITIQUE (quality_policy)
11. RESPONSE FORMAT (response_policy)
12. CONSTRAINTS (behavior_spec + NIM params from AI-0001)

### Rule 2 — No Duplication
Each concept appears in exactly one module. If a concept is referenced in two modules, it must be resolved to a canonical location and cross-referenced only.

### Rule 3 — Parameter Traceability
Every parameter in [CONSTRAINTS] must have a source reference:
- Model parameters → AI-0001-Nemotron-Engineering-Spec.md
- API parameters → AI-0002-NVIDIA-NIM-API.md  
- Compatibility issues → AI-0003-OpenWebUI-Compatibility.md

### Rule 4 — Version Bump
When any source policy changes, increment the compiled prompt version.

| Policy Change | Version Bump |
|---------------|-------------|
| Minor wording | patch (v1.0.x) |
| Behavior change | minor (v1.x.0) |
| Architecture restructure | major (vX.0.0) |

### Rule 5 — Token Budget
The compiled system prompt must not exceed 800 tokens in production.
This preserves context budget for:
- User messages: ~1,000 tokens average
- Assistant response: ~2,000 tokens average
- Memory injection: ~500 tokens
- Knowledge chunks: ~2,000 tokens
- Remaining context: ~122,200 tokens (128K window)

---

## Compilation Triggers

| Trigger | Action |
|---------|--------|
| Any policy file modified | Re-run compilation, bump version |
| NIM API update detected | Re-check [CONSTRAINTS] block |
| New benchmark result shows degradation | Review source policy module |
| User feedback pattern | Update conversation_policy.md first |

---

## Future: Automated Compiler

Target: Python script `runtime/scripts/compile_prompt.py` that:
1. Reads each policy module
2. Extracts the canonical section for each module
3. Assembles in order
4. Validates token count
5. Writes `system_prompt_v{N}.md`

*Not yet implemented — manual compilation in v1.0.0.*
