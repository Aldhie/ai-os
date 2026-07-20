# AI-9003: Prompt Engineering Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9003 |
| **Title** | Prompt Engineering Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Category** | Governance |

---

## Cross References

- [AI-9001 — Documentation Standard](AI-9001-Documentation-Standard.md)
- [AI-0001 — Nemotron Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0002 — NVIDIA NIM API Reference](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md)
- [EXP-0004 — System Prompt Experiment](../05_EXPERIMENTS/EXP-0004-SystemPrompt.md)
- [prompts/](../../prompts/)

---

## 1. Purpose

Defines standards for authoring, versioning, and validating system prompts for Nemotron Ultra 550B via NVIDIA Cloud NIM. Prompt engineering decisions have direct impact on reasoning quality, token consumption, and agent behavior. Every prompt in this repository is a production artifact, not a scratchpad.

---

## 2. Prompt Classification

| Type | Description | Location |
|------|-------------|----------|
| System Prompt | Model persona and behavioral contract | `prompts/system/` |
| Task Prompt | Specific task instruction template | `prompts/tasks/` |
| RAG Prompt | Context injection template | `prompts/rag/` |
| Tool Prompt | Tool selection and format guidance | `prompts/tools/` |
| Reasoning Control | Thinking mode directives | Inline in system prompt |

---

## 3. Reasoning Mode Control — Documented Methods

> **Evidence Level: L1** — Source: [NVIDIA NIM Official Docs](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b)

### Method 1: System Prompt Token (Primary Open WebUI Method)

```python
# Reasoning ON
{"role": "system", "content": "You are a helpful assistant. /think"}

# Reasoning OFF
{"role": "system", "content": "You are a helpful assistant. /nothink"}
```

### Method 2: `extra_body.chat_template_kwargs` (Pipeline Method)

```python
# Full reasoning
extra_body={"chat_template_kwargs": {"enable_thinking": True}}

# Medium effort — RECOMMENDED as starting point
extra_body={"chat_template_kwargs": {"enable_thinking": True, "medium_effort": True}}

# Reasoning OFF
extra_body={"chat_template_kwargs": {"enable_thinking": False}}
```

### Method 3: `reasoning_budget` Hard Cap

```python
# Hard cap on reasoning trace tokens (closes trace at next newline before budget)
result = client.chat_completion(
    model="nvidia/nemotron-3-ultra-550b-a55b",
    messages=[...],
    reasoning_budget=512,
    max_tokens=1024,
)
```

> **Warning:** If no newline found within 500 tokens of budget, trace closes abruptly.

### Method 4: Force Non-Empty Content (Coding Agents)

```python
# Required for coding agents to prevent content: null responses
extra_body={"chat_template_kwargs": {
    "enable_thinking": True,
    "force_nonempty_content": True
}}
```

---

## 4. System Prompt Template Standard

Every system prompt file must:

1. Declare its reasoning mode: `/think` or `/nothink`
2. Declare its intended agent profile (`reasoning`, `creative`, `code`, `general`)
3. Include a version comment
4. Be benchmarked against EXP-0004 before promotion to Active

### Example Structure

```markdown
<!-- Prompt ID: SP-001 | Version: 1.0.0 | Profile: reasoning | Mode: /think -->
You are an expert AI assistant specializing in [domain]. /think

You must:
1. [Behavioral directive 1]
2. [Behavioral directive 2]

You must NOT:
1. [Prohibition 1]

Output Format: [Specification]
```

---

## 5. Token Budget Planning

> **Evidence Level: L1** — Context window default is 256K tokens on Cloud NIM.

For every system prompt, calculate the budget split:

| Component | Budget (tokens) | Configurable |
|-----------|----------------|--------------|
| System Prompt | ≤ 500 | Yes |
| Conversation History | ≤ 8,192 | Yes |
| RAG Context | ≤ 4,096 | Yes |
| Output Reserved | ≤ 4,096 | Yes |
| **Total Used** | **≤ 16,884** | — |
| **Available Buffer** | **~239,116** | — |

For long-context tasks, expand `RAG Context` up to 128K tokens while monitoring cost.

---

## 6. Prompt Versioning

All prompts follow SemVer:
- **Major:** Behavioral change (different task, different persona)
- **Minor:** Quality improvement (better instruction, added constraint)
- **Patch:** Typo fix, formatting fix

Prompts must be committed with a message format:
```
prompt(SP-001): [description of change] — profile:reasoning v1.1.0
```

---

## 7. Prompt Anti-Patterns (Prohibited)

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| `Be helpful and harmless` | Too vague | Specify exact behavioral constraints |
| `Think step by step` | Redundant with `/think` | Remove — use `/think` token instead |
| `As an AI language model...` | Role confusion | Define specific persona |
| Prompt > 1000 tokens for simple tasks | Token waste | Audit and trim |
| No reasoning mode declaration | Undefined behavior | Always declare `/think` or `/nothink` |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial prompt engineering standard — incorporates AI-0003-Audit findings |
