# AGENTS.md — rules for AI coding agents on FreshFlow

Coding agents (Claude Code, Codex, Cursor, etc.) should follow these rules in this repo.

## Lean-code ladder (ponytail)
Before writing code, stop at the first rung that holds:
1. Does this need to exist? → no: skip it (YAGNI)
2. Already in this codebase? → reuse it, don't rewrite
3. Stdlib / PySpark built-in does it? → use it
4. Native platform feature? → use it
5. Installed dependency does it? → use it
6. One line? → one line
7. Only then: the minimum that works

Lazy about the solution, **never** about correctness: data-quality checks, schema
enforcement, error handling, and clear naming are never cut.

> To install the real ponytail plugin in Claude Code:
> `/plugin marketplace add DietrichGebert/ponytail` then `/plugin install ponytail@ponytail`

## House rules
- Type hints everywhere; short docstrings; one job per function.
- Must pass `ruff`, `black --check`, `mypy`, and `pytest`.
- Explain non-trivial Spark concepts to the developer (this is a learning project).
- Never fabricate results, metrics, or data.
