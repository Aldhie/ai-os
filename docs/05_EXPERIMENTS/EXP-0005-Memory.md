# EXP-0005: Open WebUI Memory System

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0005 |
| **Title** | Open WebUI Memory: Retention Accuracy and Recall Precision |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | High |

---

## Cross References

- [AI-0003 — Open WebUI Compatibility, Section 6](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [TC-MEMO-0001 — Memory Retention](../../benchmark/tests/memory/TC-MEMO-0001.md)
- [TC-MEMO-0002 — Memory Recall](../../benchmark/tests/memory/TC-MEMO-0002.md)

---

## 1. Objective

Measure Open WebUI memory system accuracy: (1) what facts are saved to long-term memory, (2) how accurately they are recalled in future sessions, (3) whether incorrect memories can pollute future responses.

---

## 2. Hypothesis

> `[HYPOTHESIS]` Open WebUI memory auto-save correctly captures user-stated facts 85%+ of the time. Recall precision (relevant memories retrieved vs irrelevant) is 70%+. Contradictory memory entries cause measurable response degradation.

---

## 3. Variables

### Test Scenarios

| Scenario | Description |
|----------|-------------|
| S-1 | State explicit fact; verify it appears in next session |
| S-2 | State preference; verify it influences recommendation |
| S-3 | State contradictory facts across sessions; measure resolution |
| S-4 | State 10 facts in one session; test recall of all 10 |
| S-5 | Test memory isolation between users (security) |

---

## 4. Environment

| Component | Value |
|-----------|-------|
| Open WebUI | Latest stable |
| Memory: auto_save | `true` |
| Memory: auto_recall | `true` |
| Memory: retention | 7-day short-term, unlimited long-term |
| Model | `nvidia/nemotron-3-ultra-550b-a55b` |

---

## 5. Expected Result

- S-1, S-2: >85% save accuracy
- S-3: Model surfaces conflict; requests clarification
- S-4: >70% recall across 10 facts
- S-5: Zero cross-user leakage

---

## 6. Actual Result

> `[PENDING]`

---

## 7. Decision

> `[PENDING]` Update memory configuration based on accuracy results.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
