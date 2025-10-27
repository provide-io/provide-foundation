# Testing CLI Commands

Learn how to test CLI applications built with Foundation.

## Overview

Test CLI commands using Click's testing utilities and Foundation's testkit.

## Basic CLI Test

```python
from click.testing import CliRunner
from provide.testkit import reset_foundation_setup_for_testing

def test_cli_command():
    """Test a CLI command."""
    reset_foundation_setup_for_testing()

    from your_app import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["command", "--option", "value"])

    assert result.exit_code == 0
    assert "Expected output" in result.output
```

## Testing with Arguments

```python
def test_with_arguments():
    runner = CliRunner()
    result = runner.invoke(cli, ["greet", "Alice", "--greeting", "Hi"])

    assert result.exit_code == 0
    assert "Hi, Alice" in result.output
```

## Testing Error Cases

```python
def test_invalid_input():
    runner = CliRunner()
    result = runner.invoke(cli, ["process", "--count", "invalid"])

    assert result.exit_code != 0
    assert "Invalid value" in result.output
```

## Next Steps

- **[Unit Testing](unit-tests.md)** - General unit tests
- **[API Reference: CLI](../../reference/provide/foundation/cli/index.md)**
