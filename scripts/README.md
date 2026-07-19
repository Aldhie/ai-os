# Scripts

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | scripts/README.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This directory contains utility scripts for the AI OS engineering workflow. Scripts cover benchmark execution, dataset preprocessing, configuration validation, and reporting.

---

## Scope

- Benchmark execution scripts
- Dataset preprocessing utilities
- Configuration validation scripts
- Report generation tools

---

## Dependencies

- Python 3.10+
- `requests` library for NIM API calls
- `openai` SDK (OpenAI-compatible client for NIM)

---

## Planned Scripts

| Script | Language | Purpose | Status |
|--------|----------|---------|--------|
| `run_benchmark.py` | Python | Execute benchmark cases against NIM API | Planned |
| `evaluate_results.py` | Python | Score benchmark results | Planned |
| `validate_config.py` | Python | Validate JSON config files | Planned |
| `preprocess_dataset.py` | Python | Clean and format datasets | Planned |
| `generate_report.py` | Python | Generate benchmark reports | Planned |
| `count_tokens.py` | Python | Count tokens in prompts | Planned |

---

## Script Conventions

- All scripts must include a `--help` flag
- All scripts must handle errors gracefully
- All scripts must be documented with a header comment block
- Use environment variables for secrets (never hardcode credentials)

---

## Environment Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install openai requests python-dotenv

# Set environment variables
export NVIDIA_API_KEY=your_key_here
```

---

## TODO

- [ ] Write `run_benchmark.py`
- [ ] Write `evaluate_results.py`
- [ ] Write `validate_config.py`
- [ ] Add requirements.txt
- [ ] Add Makefile for common commands
