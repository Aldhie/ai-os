# Prompt Compiler Specification
> **Module ID**: M-COMPILER | **Version**: 2.0.0 | **Responsibility**: Define the deterministic assembly rules that transform individual policy modules into a single executable system prompt
> **Why this module exists**: A single monolithic system prompt cannot be independently tested, versioned, or selectively deployed per task profile. The compiler enables modular updates, regression testing, and profile-specific prompt variants without manual editing.

---

## Compilation Pipeline

```
Identity (M-IDENTITY)
    ↓
Behaviour (M-BEHAVIOUR)
    ↓
Conversation (M-CONVERSATION)
    ↓
Reasoning (M-REASONING)
    ↓
Planning (M-PLANNING)
    ↓
Memory (M-MEMORY)
    ↓
Knowledge (M-KNOWLEDGE)
    ↓
Tools (M-TOOLS)
    ↓
Response (M-RESPONSE)
    ↓
Quality (M-QUALITY)
    ↓
Constraints (M-CONSTRAINTS)
    ↓
Thinking (M-THINKING) [injected as runtime parameter, not prompt text]
    ↓
[ COMPILED PROMPT ]
```

---

## Module Registry

| Module ID | File | Required | Max Tokens (compiled contribution) |
|---|---|---|---|
| M-IDENTITY | identity.md | YES | 80 |
| M-BEHAVIOUR | behavior.md | YES | 300 |
| M-CONVERSATION | conversation.md | YES | 200 |
| M-REASONING | reasoning.md | YES | 250 |
| M-PLANNING | planning.md | CONDITIONAL | 150 |
| M-MEMORY | memory.md | YES | 150 |
| M-KNOWLEDGE | knowledge.md | YES | 150 |
| M-TOOLS | tools.md | YES | 200 |
| M-RESPONSE | response.md | YES | 200 |
| M-QUALITY | quality.md | YES | 150 |
| M-CONSTRAINTS | constraints.md | YES | 150 |
| M-THINKING | thinking.md | RUNTIME PARAM | 0 (not injected as text) |

**Total compiled prompt target**: ≤ 1,800 tokens. Exceeding this wastes context budget on every request.

---

## Compilation Rules

1. **Order is fixed**. The pipeline sequence above is non-negotiable. Behaviour must precede Conversation; Memory must precede Knowledge.
2. **Each module contributes a single section**. Modules may not repeat content already expressed in an earlier module.
3. **No prose duplication**. If the same rule appears in two modules, the later module defers to the earlier.
4. **Conditional modules** (Planning, Architecture, Coding) are only compiled into the prompt when the active profile requires them. They are omitted for `discussion` and `creative` profiles to reduce token footprint.
5. **Thinking is a runtime API parameter** — it is never compiled into prompt text. The compiler emits a `thinking_config` object alongside the prompt, not within it.
6. **Version header is mandatory**. Every compiled prompt must begin with a machine-readable header:
   ```
   <!-- COMPILED: version=X.Y.Z | profile=<name> | sha256=<hash-of-sources> | date=YYYY-MM-DD -->
   ```
7. **Validation before commit**: The compiler must verify:
   - No module contains the string `TODO`, `PLACEHOLDER`, or `TBD`
   - Total token count ≤ 1,800 (measured by tiktoken cl100k_base)
   - All required modules are present
   - No module exceeds its individual token budget by > 20%

---

## Profile Variants

| Profile | Modules Included | Notes |
|---|---|---|
| standard | All required | General-purpose baseline |
| coding | + coding.md, architecture.md | Activates code-specific reasoning sections |
| architecture | + architecture.md, planning.md | Deep system design mode |
| discussion | Required only (no planning/coding/arch) | Minimum token footprint |
| research | + knowledge.md expanded | Expanded RAG citation policy |

---

## Upgrade Protocol

1. Edit the source module only.
2. Run the compiler.
3. Verify token counts and validation gates.
4. Update version header (patch for wording; minor for behaviour change; major for structural change).
5. Commit as `feat(prompt): upgrade M-<ID> to v<X.Y.Z>`.
6. Run behaviour benchmark suite against prior compiled version.
7. If benchmark regression detected: revert the module, not the compiled prompt.
