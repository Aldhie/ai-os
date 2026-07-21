# Prompt Compiler Specification
> **Role**: HOW modules are assembled into a production system prompt | **Version**: 1.0.0

---

## Compilation Order

```
01_identity.md       → WHO the AI is
02_behavior.md       → HOW it responds to uncertainty, risk, failure
03_conversation.md   → HOW conversation flows
04_reasoning.md      → HOW it thinks
05_planning.md       → HOW it decomposes multi-step tasks
06_coding.md         → HOW it writes and reviews code  [mode: coding]
07_architecture.md   → HOW it designs systems          [mode: architecture]
08_response.md       → HOW responses are sized and structured
09_memory.md         → HOW memory integrates
10_knowledge.md      → HOW RAG integrates
11_tools.md          → HOW tools are selected
12_quality.md        → HOW response quality is self-enforced
13_constraints.md    → WHAT it will not do
14_thinking.md       → HOW thinking tokens are used
```

## Compilation Profiles

| Profile | Modules Included |
|---------|------------------|
| `standard` | 01-05, 08-14 |
| `coding` | 01-06, 08-14 |
| `architecture` | 01-05, 07-14 |
| `full` | 01-14 |

## Compilation Rules

1. Extract the body of each module (strip YAML frontmatter and `---` separators)
2. Prepend a `## SECTION` header from the module role line
3. Assemble in canonical order
4. Insert section dividers between modules
5. Prepend generation header: model, profile, compiled timestamp, git SHA
6. No module may contain `TODO`, `PLACEHOLDER`, `[TBD]`, or `[FILL]`
7. Total compiled prompt target: < 3,000 tokens (standard profile)

## Token Budget for Compiled Prompt

```
standard profile:    ~2,200 tokens
coding profile:      ~2,500 tokens
architecture profile: ~2,600 tokens
full profile:        ~3,000 tokens
```

The compiled prompt is the single source of truth for the system prompt. Never edit `compiled_prompt_v1.md` directly — regenerate from modules.
