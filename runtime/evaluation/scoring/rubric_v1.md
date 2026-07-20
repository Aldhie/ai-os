# Scoring Rubric v1

> **Version**: 1.0.0
> **Spec Ref**: AI-9002-Benchmark-Standard.md

---

## Numeric Scoring Scale

All scores are 0.0–10.0 (one decimal place).

| Score | Meaning |
|-------|---------|
| 10.0 | Perfect. No errors, no omissions, exceeds expectation |
| 9.0-9.9 | Excellent. Correct, complete, minimal issues |
| 8.0-8.9 | Good. Correct with minor gaps or stylistic issues |
| 7.0-7.9 | Adequate. Mostly correct; some notable gaps |
| 6.0-6.9 | Marginal. Partially correct; significant gaps |
| 5.0-5.9 | Poor. More wrong than right |
| <5.0 | Fail. Incorrect, misleading, or dangerous |

---

## Component-Specific Rubrics

### System Prompt Quality
- Factual accuracy of responses: 40%
- Behavioral compliance (follows policy): 30%
- Response format quality: 15%
- Anti-pattern avoidance: 15%

### RAG Quality (RAGAS-aligned)
- Context recall: 25%
- Context precision: 25%
- Answer relevance: 25%
- Faithfulness: 25%

### Memory Quality
- Preference recall rate: 50%
- Privacy isolation: 30%
- Update accuracy: 20%

### Code Quality
- First-run success rate: 40%
- Error handling coverage: 30%
- Type correctness: 20%
- Documentation quality: 10%

---

## Minimum Passing Scores

| Component | Minimum Score | Regression Threshold |
|-----------|-------------|---------------------|
| System Prompt | 8.0 | -5% vs baseline |
| RAG | 7.5 | -5% vs baseline |
| Memory | 8.5 | -5% vs baseline |
| Code | 8.0 | -5% vs baseline |
| Latency (p50) | n/a | +20% vs baseline |
