# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`provide.foundation` is a Python telemetry library built on `structlog` that provides beautiful, performant structured logging with emoji-enhanced visual parsing and semantic Domain-Action-Status patterns.

## Development Environment Setup

**IMPORTANT**: Use `source env.sh` to set up the environment. This script provisions a virtual environment in `workenv/` (NOT `.venv`). The environment setup handles:
- Python 3.11+ requirement
- UV package manager for dependency management
- Platform-specific virtual environments (e.g., `workenv/provide-foundation_darwin_arm64`)

## Common Development Commands

```bash
# Environment setup (always use this instead of manual venv creation)
source env.sh

# Run tests
pytest                           # Run all tests
pytest -n auto                   # Run tests in parallel
pytest -n auto -vvv             # Verbose parallel test run
pytest tests/test_specific.py   # Run specific test file
pytest -k "test_name"           # Run tests matching pattern

# Code quality checks
ruff check .                    # Run linter
ruff format .                   # Format code
mypy src/                       # Type checking

# Build and distribution
uv build                        # Build package
uv publish                      # Publish to PyPI
```

## Architecture & Code Structure

### Core Components

1. **Logger System** (`src/provide/foundation/logger/`)
   - `base.py`: FoundationLogger class and global logger instance
   - `config.py`: TelemetryConfig and LoggingConfig data classes
   - `processors.py`: Log processing pipeline
   - `emoji_matrix.py`: Emoji mapping system for visual log parsing
   - `env.py`: Environment variable configuration parsing

2. **Configuration System** (`src/provide/foundation/config/`)
   - Async-first configuration loading system
   - Environment variable support
   - YAML/JSON file loading capabilities

3. **Emoji Sets** (`src/provide/foundation/logger/emoji/sets.py`)
   - Extensible domain-specific logging emoji sets (LLM, HTTP, Database)
   - Custom emoji mapping per domain
   - Falls back to classic Domain-Action-Status pattern

### Key Design Patterns

1. **Lazy Initialization**: Logger uses lazy setup to avoid import-time side effects
2. **Immutable Configuration**: Uses `attrs` with frozen dataclasses
3. **Modern Python Typing**: Uses Python 3.11+ type hints (no Dict/List/Optional)
4. **Emoji System**: Visual log parsing through contextual emoji prefixes

### Important Implementation Notes

1. **TelemetryConfig.from_env()** issue: The codebase expects this as a class method but it's currently a standalone function in `logger/env.py`. This causes test failures.

2. **Global Logger Instance**: The `logger` object in `logger/base.py` is the primary interface for logging throughout applications.

3. **Thread Safety**: All logging operations are thread-safe and async-compatible.

4. **Performance**: Benchmarked at >14,000 msg/sec with emoji processing enabled.

## Testing Strategy

- Comprehensive test coverage including unit, integration, and property-based tests
- Tests use `pytest` with async support via `pytest-asyncio`
- Parallel test execution with `pytest-xdist`
- Coverage tracking with `pytest-cov`

## Common Issues & Solutions

1. **ModuleNotFoundError for dependencies**: Run `source env.sh` to ensure proper environment setup
2. **Test failures related to from_env**: The `TelemetryConfig.from_env()` method needs to be properly exposed as a class method
3. **Import errors**: Ensure PYTHONPATH includes both `src/` and project root

## Development Guidelines

- Always use modern Python 3.11+ type hints (e.g., `list[str]` not `List[str]`)
- Maintain immutability in configuration objects
- Follow existing emoji naming conventions in emoji sets
- Preserve thread safety in all logging operations
- Use `attrs` for data classes consistently
- no migration, backward compatibility, or any of that kind of logic will be used. you must treat this as a prerelease in which i can do anything with .
- only use foundation.logger - never structlog directly
- only use absolute imports. never relative imports.
- use async in pytests where appropriate.
- no legacy implementation is needed. any refactoring will *replace* the logic. no migration. and the tests must the same as before. no migration.
- no. more. backward compatibility. implement it the way i want in the target state
- There should be *NO* inline defaults. EVER. Defaults should come from configuration modules or environment variables, not inline in field definitions.
- no backward compatibility.
- i do not need backward compatibility, migration logic, or transition comments and logic unless specifically asked.
- do not write functions to "go around tests" unless i ask.

## Output Guidelines for CLI and Logging

**IMPORTANT**: Use the correct output method for the context:

- **CLI User-Facing Output**: Use `pout()` for standard output and `perr()` for error messages
  - These are in `provide.foundation.console.output`
  - Never use `print()` directly in CLI commands
  - Example: `pout("✅ Operation successful")` or `perr("❌ Operation failed")`

- **Application Logging**: Use `logger` strictly for internal logging/debugging
  - Import with: `from provide.foundation import logger`
  - Example: `logger.debug("Internal state changed", state=new_state)`

- **Low-Level Infrastructure**: Only use `print()` to stderr where using Foundation logger would create circular dependencies
  - Example: In `streams/file.py` where the logger itself depends on these components
- it is okay to use future annotation for unquoted types.