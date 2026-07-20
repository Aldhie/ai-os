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
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-0001 Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0003 Compatibility Matrix](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [EXP-0004 System Prompt Experiment](../05_EXPERIMENTS/EXP-0004-SystemPrompt.md)
- [AI-9001 Documentation Standard](AI-9001-Documentation-Standard.md)

---

## 1. Purpose

Defines standards for writing, versioning, testing, and evaluating system prompts and user-facing prompts in this repository. Every prompt used in production must conform to this standard.

---

## 2. Prompt Classification

| Type | Description | File Location |
|------|-------------|---------------|
| System Prompt | Role-level instruction for model persona and behavior | `prompts/system/` |
| Task Prompt | Specific task instruction (e.g., summarize, classify) | `prompts/tasks/` |
| Chain Prompt | Multi-step chain-of-thought scaffolding | `prompts/chains/` |
| RAG Prompt | Template for RAG-augmented retrieval queries | `prompts/rag/` |
| Tool Prompt | System prompt optimized for tool-calling agents | `prompts/tools/` |
| Evaluation Prompt | Used by critic/evaluator agents | `prompts/eval/` |

---

## 3. Mandatory Prompt Metadata

Every prompt file MUST contain a YAML frontmatter block:

```yaml
---
prompt_id: SP-0001
title: Nemotron Ultra General Assistant
type: system
version: 1.0.0
status: active
model: nvidia/nemotron-3-ultra-550b-a55b
thinking_mode: OFF  # ON | OFF | medium_effort
temperature: 1.0
top_p: 0.95
max_tokens: 4096
tested_in: [EXP-0004]
benchmark_score: null  # fill after benchmark
created: 2026-07-20
updated: 2026-07-20
owner: Aldhie
---
```

---

## 4. Prompt Quality Rules

### 4.1 Thinking Mode Declaration

Every system prompt for Nemotron Ultra 550B MUST include an explicit thinking mode directive.

**[FACT]** NVIDIA official docs confirm two valid methods:

```
# Method 1 — System prompt directive (use in Open WebUI)
/think        → enables reasoning trace
/nothink      → disables reasoning trace

# Method 2 — API extra_body (use in Pipelines)
extra_body={"chat_template_kwargs": {"enable_thinking": True}}
extra_body={"chat_template_kwargs": {"enable_thinking": False}}
```

Reference: [NVIDIA NIM API Docs](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b)

### 4.2 Role Clarity

System prompts MUST establish:
1. Model persona (who the model is)
2. Behavioral constraints (what it must not do)
3. Output format (how responses should be structured)
4. Scope (what topics are in/out of scope)

### 4.3 Token Budget Awareness

System prompts MUST stay within the configured `system_prompt_budget_tokens` (default: 500 tokens).
Prompts exceeding this budget must be approved with a documented justification in the prompt metadata.

### 4.4 No Hallucination Anchors

System prompts MUST NOT contain factual claims that could be confused with model knowledge:
- No dates that could be misinterpreted
- No specific numbers without context
- No references to external systems without explicit framing

---

## 5. Prompt Versioning

Every prompt change requires:
1. Version bump in frontmatter
2. Changelog entry
3. Re-run of linked benchmark test cases
4. Update of `tested_in` references if new experiment created

---

## 6. Thinking Mode Selection Guide

**[FACT]** Based on NVIDIA documentation and model architecture:

| Use Case | Thinking Mode | Rationale |
|----------|--------------|----------|
| Complex reasoning, math, logic | ON (`/think`) | Full CoT trace improves accuracy |
| RAG answer synthesis | OFF (`/nothink`) | Less token waste; doc is the authority |
| Code generation (simple) | OFF | Speed; simple code doesn't need reasoning |
| Code generation (complex) | ON | Architecture decisions benefit from CoT |
| Customer service | OFF | Conversational; speed matters |
| Strategic planning | ON with `medium_effort` | Balance quality vs cost |
| Debugging | ON | Root cause analysis requires chain-of-thought |
| Classification | OFF | Deterministic; CoT not needed |

**[HYPOTHESIS]** `medium_effort` may reduce token cost by 30–60% vs full thinking ON, at 5–15% quality loss on complex reasoning. Pending EXP-0003 validation.

---

## 7. Prompt Testing Protocol

Before marking any prompt `Active`:
1. Run linked benchmark test cases (minimum 3 TCs per prompt)
2. Achieve minimum average score of 3.5/5.0
3. Document result in linked EXP-xxxx document
4. Peer review by at least one other engineer

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
