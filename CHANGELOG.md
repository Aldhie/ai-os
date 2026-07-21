# AI-OS Changelog

All notable changes to this project will be documented in this file.
Format: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.

---

## [Unreleased] — Sprint C

- Agent orchestration implementations (Planner, Critic, Reflector)
- GitHub Actions CI pipeline for automated benchmarks
- RAG pipeline integration

---

## [0.2.0] — 2026-07-21 — Sprint B Complete

### Added

#### Open WebUI Filter Stack
- `runtime/openwebui/filters/rpm_guard.py` — Enforce 32 RPM NIM Free Tier ceiling
- `runtime/openwebui/filters/credential_scrub.py` — Redact credentials pre-NIM
- `runtime/openwebui/filters/task_classifier.py` — Classify queries into 9 task classes
- `runtime/openwebui/filters/profile_selector.py` — Apply parameter profile per task class
- `runtime/openwebui/filters/context_budget.py` — Proactive context truncation
- `runtime/openwebui/filters/outlet_monitors.py` — Quality instrumentation

#### Benchmark Execution Harness
- `runtime/openwebui/benchmark/runner.py` — Full CLI benchmark runner with NIM client, scorer, reporter
- `runtime/openwebui/benchmark/fixtures/` — 6 benchmark fixtures covering DQ, RS, AR, CD, TU, LC dimensions

---

## [0.1.0] — 2026-07-20 — Sprint A Complete

### Added

#### Architecture and Documentation
- `docs/architecture/` — AI-OS system architecture documentation
- `docs/benchmark/suite.json` — Benchmark suite definition (13 dimensions, scoring weights)
- `runtime/openwebui/tools/` — Tool orchestration documentation
- `runtime/openwebui/profiles/` — Parameter profile JSON definitions (9 task classes)
- `runtime/openwebui/filters/` — Filter documentation (specs, rationale, install guide)
- `runtime/openwebui/agents/` — Agent system documentation

#### Configuration
- `runtime/openwebui/config/` — Runtime configuration files
- `.github/` — Repository configuration

---

## [0.0.1] — 2026-07-19 — Repository Initialised

### Added
- Initial repository structure
- `README.md` with project overview
