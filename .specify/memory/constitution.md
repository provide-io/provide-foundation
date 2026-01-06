# provide-foundation Constitution

## 0) Purpose

This repository is developed using a spec-driven workflow. Specs and decisions are first-class artifacts.

## 1) Workflow (default order)

1. Clarify requirements and constraints when they materially affect APIs, data models, or persistence.
2. Write/update a spec (problem, goals/non-goals, acceptance criteria).
3. Produce a plan (architecture + approach) that maps to the spec.
4. Produce tasks that are independently checkable.
5. Implement only after tasks exist.

If steps are skipped, the reason must be recorded in `DECISIONS.md`.

## 2) Repo layout conventions

- Specs live under `specs/<id>-<slug>/` and contain:
  - `spec.md` (what/why + acceptance criteria)
  - `plan.md` (how)
  - `tasks.md` (what to do)
  - optional: `notes.md` (research links, experiments)

- Decisions are appended to `DECISIONS.md` as short entries:
  - Date, decision, rationale, consequences.

## 3) Tooling constraints

- Python: 3.11+ (prefer 3.12+ features when the repo baseline allows).
- Packaging/exec: `uv` is the default tool runner and dependency manager.
- Lint/format: `ruff` is the default linter/formatter.
- Type checking: `mypy` is the default type checker.
- Tests: `pytest` is the default test runner.
- Testing: `provide-testkit` is required for Foundation-specific test fixtures.

If a different tool is required, record the rationale in `DECISIONS.md`.

## 4) Project-specific constraints

- **No backward compatibility**: This is a pre-release project. Implement features in their target state without migration logic, compatibility shims, or transition code. Some APIs may change during the pre-release series.
- **Absolute imports only**: Never use relative imports. All imports must be absolute.
- **No inline defaults**: Defaults must be stored in `defaults.py` or `constants.py` files, never inline in field definitions.

## 5) Output constraints for assistants/agents

- Do not generate code or patches unless explicitly requested.
- Prefer concise, actionable guidance over narrative.
- When asked to create/update/delete files, output **one** self-contained bash script:
  - starts with `set -eo pipefail`
  - uses emoji-prefixed logging functions
  - uses `mkdir -p` for directories
  - writes complete file contents via `cat <<'EOF' > path`
  - deletes files via `rm -f`
  - uses paths **relative to repo root**

## 6) Engineering standards (definition of done)

A change is "done" when:
- `uv run ruff check .` passes
- `uv run ruff format .` has been applied (or formatting is already compliant)
- `uv run mypy src/` passes
- `uv run pytest -q` passes (if tests exist for the touched area)
- Coverage threshold (80%) is maintained for modified code

Security gate:
- `uv run bandit -r src/` passes (excluding test directories)

## 7) Decision policy (when to ask vs decide)

Ask a clarifying question when:
- the choice affects a public API, wire format, schema, or persisted data
- the change may break existing functionality
- there are multiple valid approaches with different tradeoffs

Decide autonomously when:
- the choice is internal-only and reversible
- conventions already exist in this repo
- performance/security implications are minimal and testable

## 8) Change policy for specs

- Specs may evolve, but acceptance criteria must remain testable.
- If implementation deviates from spec, update the spec and record why in `DECISIONS.md`.

---

**Version**: 1.0.0 | **Ratified**: 2025-12-19 | **Last Amended**: 2025-12-19
