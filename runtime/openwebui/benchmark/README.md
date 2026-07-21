# AI-OS · Benchmark Suite

**Version**: 1.0.0  
**Sprint**: B

---

## Files

| File | Purpose |
|------|---------|
| `suite.json` | Benchmark dimension definitions, scoring rubrics, weights |
| `harness.py` | Executable test runner that scores against a live Open WebUI endpoint |

---

## Running the Benchmark

### Prerequisites

```bash
pip install requests
```

### Full Suite

```bash
python harness.py \
  --base-url http://localhost:3000 \
  --api-key YOUR_OPENWEBUI_API_KEY \
  --model-id ai-os-nemotron-ultra
```

### Single Dimension

```bash
python harness.py \
  --base-url http://localhost:3000 \
  --api-key YOUR_OPENWEBUI_API_KEY \
  --model-id ai-os-nemotron-ultra \
  --dimension coding
```

---

## Interpreting Results

| Score | Status | Action |
|-------|--------|---------|
| ≥ 70 | **PASS** | Sprint complete. Proceed to next sprint. |
| 50–69 | **WARNING** | Investigate failing dimensions. Fix before promoting. |
| < 50 | **FAIL** | Rollback candidate. Do not promote to production. |

---

## Probe Prompts

Each dimension uses one deterministic probe prompt designed to produce a response that
can be scored without human evaluation:

| Dimension | Probe Strategy |
|-----------|----------------|
| `discussion_quality` | Simple factual question — scores answer-first, no filler, length |
| `reasoning` | Analysis question requiring named framework |
| `architecture` | System design question requiring all 6 sections |
| `coding` | Code generation — syntax check + docstring presence |
| `tool_usage` | Simple factual — verifies no unnecessary tool calls |
| `conversation_consistency` | References prior context — verifies memory awareness |

---

## RPM Awareness

The harness inserts a 2-second delay between probes.  
At 6 dimensions, full suite = ~12 seconds + NIM latency per probe.  
Total estimated runtime: **3–8 minutes** on Free Tier.

The harness never exceeds 30 RPM (one probe every 2 seconds).
