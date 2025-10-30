# Repository Guidelines

## Project Structure & Module Organization
Source modules live under `src/provide/foundation/` grouped by capability (e.g., `logger/`, `config/`, `transport/`). Tests mirror runtime modules inside `tests/` with integration and chaos suites alongside focused unit packages; cache artifacts such as `htmlcov/` stay out of review. Runnable examples reside in `examples/`, MkDocs sources in `docs/`, and automation scripts in `scripts/`. Prefer absolute imports and keep new modules aligned with their domain directories.

## Build, Test, and Development Commands
Bootstrap with `uv venv` and `uv sync`, then `source .venv/bin/activate`. Use `make lint` for `ruff format` plus lint fixes, `make typecheck` for mypy, and `make test` for the default pytest matrix (excludes `integration`, `slow`, `benchmark`, `time_sensitive`). Generate coverage reports via `make coverage`. Targeted runs: `uv run python -m pytest tests/logger/test_structlog.py` or `uv run ruff check src/provide/foundation/logger`.

## Coding Style & Naming Conventions
Write Python 3.11+ with `attrs` dataclasses and async-first patterns when feasible. Follow `ruff` defaults: four-space indentation, max line length 111, double quotes, and comprehensive type hints. Modules remain lowercase with underscores, classes PascalCase, fixtures lowercase. Document public APIs with focused docstrings and keep comments minimal but clarifying.

## Testing Guidelines
Pytest powers all suites; name files `test_*.py` or `*_test.py` and functions `test_*`. Use markers (`@pytest.mark.integration`, `slow`, etc.) consistently. Maintain ≥83% coverage; add or update tests when adjusting behavior or introducing new modules. Leverage `provide-testkit` utilities such as `reset_foundation_setup_for_testing` to isolate global state.

## Commit & Pull Request Guidelines
Adhere to Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`...) with one logical change per commit. PRs should link to relevant issues, describe behavior changes, call out new tests or docs, and include CLI output or screenshots for user-facing updates. Ensure `make lint typecheck test` passes before requesting review and note any suites intentionally skipped.

## Security & Configuration Tips
Never commit secrets; rely on environment variables loaded through `provide.foundation.config`. Gate optional dependencies via extras in `pyproject.toml` and guard optional imports with `ModuleNotFoundError` handling. Validate file and path inputs using helpers under `src/provide/foundation/file` to preserve hardening guarantees.
