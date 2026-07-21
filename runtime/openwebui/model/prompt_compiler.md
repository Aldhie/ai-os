# Prompt Compiler Specification

> **Layer**: Compilation Engine  
> **Responsibility**: Define the assembly order, rules, and output format for generating compiled_prompt_v1.md  
> **Version**: 1.0.0

---

## Assembly Order

```
Section 1: identity      (required, ~300 tokens)
Section 2: behavior      (required, ~500 tokens)
Section 3: conversation  (required, ~350 tokens)
Section 4: reasoning     (required, ~400 tokens)
Section 5: planning      (conditional: complex tasks)
Section 6: coding        (conditional: coding profile)
Section 7: architecture  (conditional: architecture profile)
Section 8: memory        (required, ~200 tokens)
Section 9: knowledge     (required, ~200 tokens)
Section 10: tools        (required, ~200 tokens)
Section 11: response     (required, ~250 tokens)
Section 12: quality      (required, ~250 tokens)
Section 13: constraints  (required, ~150 tokens)
Section 14: thinking     (required, ~150 tokens)
```

---

## Profile → Module Inclusion Map

| Profile | Modules Included |
|---------|------------------|
| standard | 1,2,3,4,8,9,10,11,12,13,14 |
| discussion | 1,2,3,4,8,9,10,11,12,13,14 |
| coding | 1,2,3,4,6,8,9,10,11,12,13,14 |
| architecture | 1,2,3,4,5,7,8,9,10,11,12,13,14 |
| research | 1,2,3,4,5,8,9,10,11,12,13,14 |
| creative | 1,2,3,4,8,10,11,12,13,14 |
| debugging | 1,2,3,4,6,8,9,10,11,12,13,14 |

---

## Compilation Rules

1. Extract only the `Runtime [Name] Block` from each module
2. Strip YAML frontmatter and module metadata
3. Assemble in order with single blank line between sections
4. Insert header comment: `# AI-OS Compiled Prompt — Profile: {profile} — v1.0.0`
5. No TODOs, no placeholders, no unfinished sections — FAIL if found
6. Hash the output and record in `compiled_manifest.json`
7. Token count the output and verify it is within the profile's system prompt budget

---

## Token Budget Targets (compiled output)

| Profile | Target Tokens | Hard Max |
|---------|--------------|----------|
| standard | 2,500 | 3,200 |
| coding | 3,000 | 3,800 |
| architecture | 3,200 | 4,000 |
| research | 2,800 | 3,500 |

---

*Module: prompt_compiler.md | Version: 1.0.0 | Last updated: 2026-07-21*
