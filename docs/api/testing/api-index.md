# Testing API Reference

Comprehensive testing utilities for Foundation applications including fixtures, mocks, and testing helpers.

## Overview

The testing module provides Foundation's complete testing infrastructure with:

- **[Stream Testing](api-streams.md)** - Stream redirection and output capture utilities
- **[Logger Management](api-logger.md)** - Logger state management and isolation
- **[CLI Testing](api-cli.md)** - Command-line interface testing tools
- **[Crypto Fixtures](api-crypto.md)** - Certificate and key testing data
- **[Context Detection](api-context.md)** - Testing environment detection

## Key Features

### Stream Capture
- Automatic log output capture with pytest fixtures
- Custom stream redirection for testing scenarios
- Thread-safe stream management

### Logger Isolation
- Complete logger state reset between tests
- Configuration isolation and cleanup
- Lazy setup state management

### CLI Testing
- Isolated command-line test environments
- Mock context objects for testing
- Temporary configuration file management

### Crypto Testing
- Comprehensive certificate fixtures for TLS testing
- Valid and invalid PEM content for error scenarios
- File-based fixtures with various formatting edge cases

## Quick Start

```python
import pytest
from provide.foundation.testing import (
    captured_stderr_for_foundation,
    reset_foundation_setup_for_testing,
    set_log_stream_for_testing,
    isolated_cli_runner
)

# Capture log output
def test_with_captured_logs(captured_stderr_for_foundation):
    logger.info("test_message", key="value")
    output = captured_stderr_for_foundation.getvalue()
    assert "test_message" in output

# Reset logger state
def test_logger_isolation():
    reset_foundation_setup_for_testing()
    # Logger is in clean state

# CLI testing
def test_cli_command():
    with isolated_cli_runner() as runner:
        result = runner.invoke(cli, ["command", "--option"])
        assert result.exit_code == 0
```

## Quick Reference

| Component | Purpose | Complexity |
|-----------|---------|------------|
| [Stream Testing](api-streams.md) | Log output capture | Basic |
| [Logger Management](api-logger.md) | State isolation | Intermediate |
| [CLI Testing](api-cli.md) | Command testing | Intermediate |
| [Crypto Fixtures](api-crypto.md) | Certificate testing | Advanced |
| [Context Detection](api-context.md) | Environment detection | Basic |

## Related Documentation

- [Logger API](../logger/api-index.md) - Foundation logging system
- [Streams API](../streams/api-index.md) - Stream management and redirection
- [Errors API](../errors/api-index.md) - Error handling and testing
- [CLI Guide](../../guide/cli/index.md) - Command-line interface development
- [Testing Guide](../../guide/testing.md) - Comprehensive testing practices