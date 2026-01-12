# AGENTS.md

This file provides guidance for AI assistants when working with code in this repository.

## Project Overview

`provide.foundation` is a comprehensive Python foundation library for building robust applications. It provides structured logging, CLI framework, configuration management, cryptography, file operations, resilience patterns, and essential application building blocks. Built on proven libraries like `structlog`, `click`, and `attrs`, it offers beautiful, performant structured logging with emoji-enhanced visual parsing and semantic Domain-Action-Status patterns.

## Development Environment Setup

**IMPORTANT**: Use standard Python virtual environment setup with UV. The environment setup handles:
- Python 3.11+ requirement
- UV package manager for dependency management

## Common Development Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest                      # Run all tests
uv run pytest -n auto              # Run tests in parallel
uv run pytest -n auto -vvv         # Verbose parallel test run
uv run pytest tests/test_specific.py   # Run specific test file
uv run pytest -k "test_name"       # Run tests matching pattern

# Code quality checks
uv run ruff check .                # Run linter
uv run ruff format .               # Format code
uv run mypy src/                   # Type checking

# Build and distribution
uv build                           # Build package
uv publish                         # Publish to PyPI
```

## Environment Variables

The library provides two distinct APIs for working with environment variables, each serving different purposes:

### Direct Environment Variable Access (`utils/environment`)

Use for simple, one-off environment variable access with automatic type coercion:

```python
from provide.foundation.utils.environment import get_bool, get_int, get_str, get_list

# Simple direct access
debug = get_bool("DEBUG", default=False)
port = get_int("PORT", default=8080)
api_key = get_str("API_KEY", required=True)
allowed_hosts = get_list("ALLOWED_HOSTS", default=["localhost"])
```

**When to use**:
- Scripts and utilities
- Simple configuration needs
- One-off environment variable reads
- Quick prototyping

**Available functions**:
- `get_bool(name, default=None, required=False)` - Parse boolean values ("true", "1", "yes")
- `get_int(name, default=None, required=False)` - Parse integers
- `get_float(name, default=None, required=False)` - Parse floating point numbers
- `get_str(name, default=None, required=False)` - Get string values
- `get_list(name, default=None, separator=",", required=False)` - Parse comma-separated lists
- `get_tuple(name, default=None, separator=",", required=False)` - Parse comma-separated tuples
- `get_set(name, default=None, separator=",", required=False)` - Parse comma-separated sets (duplicates removed)
- `get_dict(name, default=None, required=False)` - Parse key=value pairs
- `get_path(name, default=None, required=False)` - Get filesystem paths
- `require(name)` - Require an environment variable (raises if missing)

### Structured Configuration Classes (`config/env`)

Use for building structured, validated configuration objects with file-based secret support:

```python
from provide.foundation.config import RuntimeConfig, env_field
from attrs import define

@define
class DatabaseConfig(RuntimeConfig):
    host: str = env_field(env_var="DB_HOST", default="localhost")
    port: int = env_field(env_var="DB_PORT", default=5432)
    # Supports file:// prefix for reading secrets from files
    password: str = env_field(env_var="DB_PASSWORD")  # Can be "file:///secrets/db_pass"
    ssl_enabled: bool = env_field(env_var="DB_SSL", default=False)

# Load from environment
config = DatabaseConfig.from_env()
```

**When to use**:
- Application-wide configuration
- Configuration classes with validation
- Secret management (supports `file://` prefix for reading from secret files)
- Complex configuration with multiple related values
- Type safety and IDE autocomplete

**Features**:
- Type validation through attrs
- Support for `file://` prefix to read secrets from files
- Automatic parsing based on field types
- Integration with RuntimeConfig for environment variable loading

### Examples

**Simple script**:
```python
from provide.foundation.utils.environment import get_int, get_bool

workers = get_int("WORKERS", default=4)
debug = get_bool("DEBUG", default=False)
```

**Application configuration**:
```python
from provide.foundation.config import RuntimeConfig, env_field
from attrs import define

@define
class AppConfig(RuntimeConfig):
    api_key: str = env_field(env_var="API_KEY")  # Required
    timeout: int = env_field(env_var="TIMEOUT", default=30)
    retry_enabled: bool = env_field(env_var="RETRY", default=True)

config = AppConfig.from_env()
```

## Architecture & Code Structure

### Core Components

1. **Logger System** (`src/provide/foundation/logger/`)
   - `base.py`: FoundationLogger class and global logger instance
   - `config/`: TelemetryConfig and LoggingConfig data classes
   - `processors/`: Log processing pipeline
   - `setup/`: Logger initialization and coordination
   - Event sets in `src/provide/foundation/eventsets/`: Emoji mapping system for visual log parsing

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

1. **Unified Initialization**: The Hub provides `initialize_foundation()` as the single entry point for library setup, replacing all deprecated `setup_*` functions.

2. **Global Logger Instance**: The `logger` object in `logger/base.py` is the primary interface for logging throughout applications.

3. **Thread Safety**: All logging operations are thread-safe and async-compatible.

4. **Performance**: Benchmarked at >14,000 msg/sec with emoji processing enabled.

## Testing Strategy

### Core Testing Requirements

**CRITICAL**: When testing provide-foundation or any application that uses it, `provide-testkit` MUST be available and used. This is non-negotiable.

- **provide-testkit dependency**: Required in dev dependencies (already configured)
- **Foundation reset**: ALWAYS use `reset_foundation_setup_for_testing()` in test fixtures
- **Log stream control**: Use `set_log_stream_for_testing()` for capturing Foundation logs
- **Context detection**: Testkit automatically detects testing environments
- **Security scanning**: Use `SecurityFixture` or `SecurityScanner` for automated security analysis

### Standard Testing Pattern

```python
import pytest
from provide.testkit import (
    reset_foundation_setup_for_testing,
    set_log_stream_for_testing,
)

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state before each test."""
    reset_foundation_setup_for_testing()
```

### Security Testing

Use testkit's built-in security scanning tools to validate code security:

```python
from pathlib import Path
from provide.testkit.quality.security import SecurityScanner

def test_security_scan():
    """Run security scan on codebase."""
    scanner = SecurityScanner()
    result = scanner.analyze(Path("src/"))

    # Check for high-severity issues
    assert result.metadata.get("severity", {}).get("high", 0) == 0

    # Generate report
    report = scanner.report(result, format="terminal")
    print(report)
```

Or use as a pytest fixture:

```python
from provide.testkit.quality.security import SecurityFixture

@pytest.fixture
def security_scanner():
    """Security scanning fixture."""
    fixture = SecurityFixture()
    fixture.setup()
    yield fixture
    fixture.teardown()

def test_no_hardcoded_secrets(security_scanner):
    """Ensure no hardcoded secrets in source."""
    results = security_scanner.scan(Path("src/"))
    # Assert no S105, S106 violations
    assert "S105" not in str(results)
```

### FoundationTestCase Setup Pattern

**IMPORTANT**: When inheriting from FoundationTestCase, use `setup_method` and `teardown_method`, not `setUp`/`tearDown`:

```python
from provide.testkit import FoundationTestCase

class TestSomething(FoundationTestCase):
    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()  # Always call parent setup
        # Your custom setup code here
        self.manager = ConfigManager()

    def teardown_method(self) -> None:
        """Clean up after test."""
        # Your cleanup code here
        super().teardown_method()  # Always call parent teardown
```

This pattern ensures compatibility with FoundationTestCase's internal state management and maintains consistency with the pytest convention used throughout the codebase.

### Testing Infrastructure

- Comprehensive test coverage including unit, integration, and property-based tests
- Tests use `pytest` with async support via `pytest-asyncio`
- Parallel test execution with `pytest-xdist`
- Coverage tracking with `pytest-cov`
- **Foundation-specific fixtures**: All provided by provide-testkit

### Development Requirement

If `provide-testkit` is not available in the environment, **PAUSE DEVELOPMENT** and install it:
```bash
uv add provide-testkit --group dev
```

## Common Issues & Solutions

1. **ModuleNotFoundError for dependencies**: Ensure virtual environment is activated with `source .venv/bin/activate` and dependencies are installed with `uv sync`
2. **Hub Initialization**: Use `get_hub().initialize_foundation()` for proper library setup instead of deprecated setup functions
3. **Import errors**: Ensure PYTHONPATH includes both `src/` and project root
4. **Asyncio debug messages**: The logger automatically suppresses asyncio DEBUG messages (e.g., "Using selector: KqueueSelector") via module-level configuration. Override with `PROVIDE_LOG_MODULE_LEVELS="asyncio:DEBUG"` if needed.

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

## Third-Party Module Log Control

The logging system provides fine-grained control over third-party module logging via module-level configuration:

### Default Suppressions

- **asyncio**: Set to INFO level to suppress debug messages like "Using selector: KqueueSelector"

### Environment Variable Override

Control module-specific log levels via `PROVIDE_LOG_MODULE_LEVELS`:

```bash
# Allow asyncio debug messages
export PROVIDE_LOG_MODULE_LEVELS="asyncio:DEBUG"

# Multiple modules (suppress urllib3 info, allow asyncio debug)
export PROVIDE_LOG_MODULE_LEVELS="urllib3:WARNING,asyncio:DEBUG"

# Suppress multiple third-party modules
export PROVIDE_LOG_MODULE_LEVELS="asyncio:WARNING,urllib3:ERROR,requests:WARNING"
```

- it is okay to use future annotation for unquoted types.
- it is okay to use __future__ annotatrion for unquoted types
- It is okay to use `from __future__ import annotations`. Especially to support unquoted types.