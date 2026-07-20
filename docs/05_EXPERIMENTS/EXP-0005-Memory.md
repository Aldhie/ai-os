# EXP-0005: Open WebUI Memory System Behavior

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0005 |
| **Title** | Open WebUI Long-Term Memory — Injection Quality and Token Impact |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related REQ** | REQ-AI-0006 (memory policy) |
| **Cross-References** | [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) · [EXP-0006](EXP-0006-RAG.md) |

---

## 1. Objective

Characterize how Open WebUI's memory system (long-term memory injection) affects:
1. Context token consumption
2. Response personalization quality
3. Interference with reasoning (does memory injection confuse the model?)
4. Behavior when memory conflicts with current user message

---

## 2. Hypothesis

> **H1:** Memory injection adds 200–800 tokens per conversation depending on memory set size.
>
> **H2:** Relevant memory injection will improve response personalization score by ≥1 point vs. no-memory baseline.
>
> **H3:** Irrelevant memory injection (when no relevant memories exist) will not degrade response quality if memory is well-filtered by Open WebUI.
>
> **H4:** Memory-context conflicts (user says X, memory says not-X) will be handled differently in reasoning ON vs. OFF mode.

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | Memory enabled | True, False |
| **Independent** | Memory set size | 0, 5, 20, 50 memories |
| **Independent** | Memory relevance | Relevant, Irrelevant, Conflicting |
| **Dependent** | Tokens consumed by memory injection | Counted from API payload |
| **Dependent** | Personalization score | 1-10 rubric |
| **Dependent** | Response accuracy when memory conflicts | 1-10 rubric |

---

## 4. Environment

| Component | Config |
|-----------|--------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Open WebUI Memory | auto_save: true, auto_recall: true |
| Memory backend | Open WebUI internal |
| Runs | 5 per condition |

---

## 5. Procedure

1. Create 3 memory test scenarios: empty, 20 relevant memories, 20 irrelevant memories
2. Run identical prompts against each scenario
3. Log exact `messages` payload sent to NIM to count memory tokens
4. Score personalization quality
5. Test conflict scenario: seed memory "User is a Python developer" then ask Java question

---

## 6. Expected Result

- Memory tokens: ~150–500 tokens for 20-memory set
- Personalization: +1 to +2 points with relevant memory
- Irrelevant memory: ≤0.5 point degradation
- Conflict: Reasoning ON expected to handle better than reasoning OFF

---

## 7–12. Actual Result through Benchmark Table

> **STATUS: PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
