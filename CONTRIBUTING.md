# Contributing to provide.foundation

We welcome contributions to provide.foundation! This guide will help you get started with development, testing, and submitting contributions.

## Prerequisites

> **Important:** This project uses `uv` for Python environment and package management.

### Install UV

Visit [UV Documentation](https://github.com/astral-sh/uv) for more information.

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Update UV to latest version
uv self update
```

## Quick Start

### Development Setup

```bash
# Clone the repository
git clone https://github.com/provide-io/provide-foundation.git
cd provide-foundation

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
uv sync
```

### Development Workflow

```bash
# Run tests
pytest                          # All tests
pytest -n auto                 # Parallel tests
pytest tests/test_specific.py  # Specific test file
pytest -k "test_name"         # Tests matching pattern

# Code quality
ruff check .                   # Linting
ruff format .                  # Code formatting
mypy src/                      # Type checking

# Run examples
python examples/01_quick_start.py
```

## Development Guidelines

### Code Style

- **Modern Python**: Use Python 3.11+ features (`dict`, `list`, `set` - not `Dict`, `List`, `Optional`)
- **Type Hints**: Full type annotations required
- **Imports**: Always use absolute imports, never relative
- **Testing**: Use async tests where appropriate
- **No Legacy Code**: Implement target state directly, no backward compatibility

### Architecture Principles

1. **Immutable Configuration**: Use `attrs` frozen dataclasses
2. **Lazy Initialization**: Avoid import-time side effects
3. **Thread Safety**: All operations must be thread-safe
4. **Optional Dependencies**: Core functionality must work without extras
5. **Modern Standards**: Follow current Python best practices

### Dependencies

The project uses optional dependency groups:

- **Core**: `structlog`, `attrs`, `aiofiles`, `tomli_w`
- **CLI**: `click` (for command-line features)
- **Crypto**: `cryptography` (for cryptographic operations)
- **OpenTelemetry**: OTEL packages (for tracing/metrics)
- **Development**: `pytest`, `mypy`, `ruff`, etc.

## Testing

### Running Tests

```bash
# Basic test run
pytest

# With coverage
pytest --cov=provide.foundation --cov-report=term-missing

# Parallel execution
pytest -n auto

# Verbose output
pytest -vvv
```

### Writing Tests

- Use `pytest` with `pytest-asyncio` for async tests
- Mock external dependencies appropriately
- Test both success and error conditions
- Include property-based tests where applicable

Example:
```python
import pytest
from provide.foundation import logger

@pytest.mark.asyncio
async def test_async_logging():
    """Test async logging functionality."""
    # Test implementation
    pass
```

## Submitting Changes

### Before Submitting

1. **Tests Pass**: Ensure all tests pass locally
2. **Code Quality**: Run linting and type checking
3. **Documentation**: Update docs for any API changes
4. **Examples**: Add/update examples if adding features

### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch from `main`
3. **Implement** your changes following the guidelines
4. **Test** thoroughly with various scenarios
5. **Submit** a pull request with clear description

### Commit Message Format

Use clear, concise commit messages:
```
feat: add new emoji set for database operations
fix: handle missing OpenTelemetry dependencies gracefully
docs: update quick start guide for new users
test: add coverage for config loading edge cases
```

## Project Structure

```
provide-foundation/
├── src/provide/foundation/     # Main package code
│   ├── logger/                 # Logging system
│   ├── config/                 # Configuration management
│   ├── cli/                    # Command-line interface
│   ├── crypto/                 # Cryptographic utilities
│   └── ...
├── tests/                      # Test suite
├── examples/                   # Usage examples
├── docs/                       # Documentation
└── workenv/                    # Platform-specific virtual environments
    └── provide-foundation_<platform>/  # e.g., provide-foundation_darwin_arm64
```

## Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Documentation**: Check `docs/` for comprehensive guides

## License

By contributing, you agree that your contributions will be licensed under the same Apache 2.0 License that covers the project.
