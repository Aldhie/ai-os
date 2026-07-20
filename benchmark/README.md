# AI-OS Benchmark Suite

A comprehensive benchmark framework for evaluating AI model performance across
domain-specific tasks relevant to the AI-OS project.

---

## Structure

```
benchmark/
├── README.md                    # This file
├── templates/
│   └── scorecard.md             # Blank scorecard for new runs
├── results/                     # Completed scorecards (per run)
│   └── README.md
└── tests/
    ├── general/                 # Factual accuracy, reasoning, math
    ├── architecture/            # Coding, system design, debugging
    ├── hospitality/             # Hotel and restaurant AI scenarios
    ├── business/                # Financial analysis, strategy, negotiation
    ├── docker/                  # Docker Compose, Dockerfile, container ops
    ├── openwebui/               # Open WebUI config, Modelfiles, Pipelines
    ├── nim/                     # NVIDIA NIM API, rate limits, thinking mode
    ├── memory/                  # Long-term memory, preferences, privacy
    └── rag/                     # RAG retrieval, citation, hallucination
```

---

## Test Case Summary

| Category | Tests | Difficulties |
|----------|-------|--------------|
| General | 3 | Easy, Medium, Hard |
| Architecture | 3 | Hard, Hard, Medium |
| Hospitality | 3 | Medium, Medium, Medium |
| Business | 3 | Hard, Hard, Hard |
| Docker | 3 | Hard, Medium, Hard |
| Open WebUI | 3 | Hard, Medium, Expert |
| NIM | 3 | Medium, Medium, Hard |
| Memory | 3 | Medium, Hard, Expert |
| RAG | 3 | Hard, Medium, Expert |
| **Total** | **27** | |

---

## How to Run a Benchmark

1. Copy `templates/scorecard.md` → `results/RUN-YYYY-MM-DD-NNN.md`
2. Fill in Run Metadata (model, temperature, thinking mode)
3. For each test case:
   - Submit the **Question** exactly as written to the model
   - Evaluate the response against **Expected Behaviour**
   - Score using the **Evaluation Criteria** weights
   - Note specific observations
4. Calculate category averages and overall score
5. Commit the completed scorecard to `results/`

---

## Scoring System

- **0–3**: Failing — significant gaps in capability
- **4–5**: Developing — partial capability, major gaps
- **6–7**: Proficient — competent with minor gaps
- **8–9**: Excellent — strong performance, minor improvements possible
- **10**: Exceptional — exceeds expected behavior

---

## Governance

Benchmark standards defined in:
[AI-9002: Benchmark Standard](../docs/99_GOVERNANCE/AI-9002-Benchmark-Standard.md)

---

*Benchmark Suite Version: 1.0.0 | Created: 2026-07-20*
