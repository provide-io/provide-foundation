# Repository Guidelines

## Project Structure & Module Organization
The package lives under `src/provide/foundation/`, organized by capability (for example `logger/`, `config/`, `cli/`, and `transport/`). Tests mirror runtime modules inside `tests/`, with dedicated integration and chaos suites, while runnable examples sit in `examples/`. Documentation sources live in `docs/` (MkDocs) and automation helpers in `scripts/`. Keep generated coverage artifacts in `htmlcov/` out of review.

## Build, Test, and Development Commands
Set up the environment with `uv venv` and `uv sync`, then activate `.venv`. Run `make lint` for `ruff format` plus lint fixes, `make typecheck` for mypy, and `make test` for the default pytest matrix (skips slow and integration markers). Use `make coverage` when you need HTML reports under `htmlcov/`. Targeted invocations include `uv run python -m pytest tests/logger/test_structlog.py` or `uv run ruff check src/provide/foundation/logger`.

## Coding Style & Naming Conventions
Python 3.11+ features are expected; prefer `attrs` dataclasses and async-first patterns. Follow `ruff` defaults: four-space indentation, double quotes, max line length 111, and absolute imports. Maintain comprehensive type hints and avoid `Any` except behind typed helpers. Module names stay lowercase with underscores, classes are PascalCase, pytest fixtures lowercase. Document public APIs with focused docstrings.

## Testing Guidelines
Pytest drives validation with configuration pinned in `pyproject.toml`. Name files `test_*.py` or `*_test.py`, functions `test_*`, and mark integration work with `@pytest.mark.integration`. Default `make test` excludes `integration`, `slow`, `benchmark`, and `time_sensitive`; include them via `pytest -m "integration or slow"`. Use `provide-testkit` helpers such as `reset_foundation_setup_for_testing` to isolate global state. Keep coverage at or above the current 83% baseline and extend benchmarks or chaos tests when touching performance-critical code.

## Commit & Pull Request Guidelines
Adopt Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`) with concise summaries and optional scope (`feat(logger): …`). One logical change per commit keeps the automated release tooling happy. PRs should link to issues, outline behavior changes, and mention new tests or docs updates; attach CLI output or screenshots when user-facing behavior shifts. Confirm `make lint typecheck test` passes before requesting review and call out any skipped suites in the PR description.

## Security & Configuration Tips
Avoid committing secrets; rely on environment variables loaded by `provide.foundation.config`. When adding new integrations, gate optional dependencies behind extras in `pyproject.toml` and guard imports with `ModuleNotFoundError` handling. Validate file and path input through existing helpers under `src/provide/foundation/file` to preserve hardening guarantees.
