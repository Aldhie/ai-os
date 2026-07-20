# Repository Rules

> **Effective**: 2026-07-20
> **Sprint**: 1.0 (Implementation Phase)

---

## Documentation is FROZEN

Engineering specifications are complete as of Sprint 1.0.

The following directories are READ-ONLY for new files:

```
docs/00_ENGINEERING/
docs/01_ARCHITECTURE/  
docs/02_RESEARCH/
```

Exceptions (require explicit justification):
- Correction of a factual error in an existing spec
- A new spec required by an undocumented NIM API capability

---

## Future Work Priority Order

1. **Runtime** — `runtime/openwebui/` artifacts
2. **Evaluation** — `runtime/evaluation/` scoring and benchmarks
3. **Benchmark** — `benchmark/tests/` test execution
4. **Optimization** — prompt tuning, parameter tuning based on eval results
5. **Deployment** — production hardening

NOT acceptable as future work:
- Additional theoretical documents
- Generic AI pattern documentation
- Repeated documentation of already-documented specs

---

## Commit Message Convention

```
feat(runtime):  new runtime artifact
fix(runtime):   bug fix in runtime config
eval(eval):     evaluation run results
bench(bench):   benchmark execution
opt(prompt):    system prompt optimization
deploy:         deployment configuration
docs(fix):      factual correction in frozen docs (requires justification comment)
```

---

## Quality Gates

Every runtime artifact must be:
- **production-oriented** — no placeholders, no TODOs
- **traceable** — must reference a spec document
- **benchmark-driven** — target metrics must be stated
- **RPM-aware** — must account for NVIDIA Free Tier limits
- **NIM-aware** — must not use forbidden parameters
- **OpenWebUI-aware** — must be compatible with OWI's API surface
