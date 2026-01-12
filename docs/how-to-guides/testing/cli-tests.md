# Testing CLI Commands

Learn how to test CLI applications built with Foundation using Click's testing utilities and provide-testkit.

## Overview

Testing CLI applications requires special tools to simulate command execution, capture output, and verify behavior. Foundation provides comprehensive testing support for CLI commands through integration with Click's test runner and provide-testkit.

**What you'll learn:**
- Basic CLI command testing
- Testing with arguments and options
- Capturing and verifying output
- Testing interactive prompts
- Error handling and exit codes
- Testing file I/O operations
- Mocking dependencies

## Prerequisites

Install testing dependencies:
```bash
uv add provide-testkit
uv add pytest
```

## Basic CLI Testing

### Simple Command Test

Test a basic CLI command:

```python
import pytest
from click.testing import CliRunner
from provide.testkit import reset_foundation_setup_for_testing

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state before each test."""
    reset_foundation_setup_for_testing()

def test_hello_command():
    """Test basic hello command."""
    from myapp.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["hello"])

    assert result.exit_code == 0
    assert "Hello, World!" in result.output
```

### Test with Arguments

Test commands that accept arguments:

```python
def test_greet_with_name():
    """Test greeting with name argument."""
    runner = CliRunner()
    result = runner.invoke(cli, ["greet", "Alice"])

    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output

def test_greet_multiple_names():
    """Test greeting multiple names."""
    runner = CliRunner()
    result = runner.invoke(cli, ["greet", "Alice", "Bob", "Charlie"])

    assert result.exit_code == 0
    assert "Alice" in result.output
    assert "Bob" in result.output
    assert "Charlie" in result.output
```

### Test with Options

Test commands with flags and options:

```python
def test_greet_with_options():
    """Test command with options."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        "greet",
        "Alice",
        "--greeting", "Hi",
        "--uppercase"
    ])

    assert result.exit_code == 0
    assert "HI, ALICE!" in result.output

def test_short_flags():
    """Test short flag options."""
    runner = CliRunner()
    result = runner.invoke(cli, ["process", "-v", "-f", "input.txt"])

    assert result.exit_code == 0
    # Verify verbose output appears
    assert "Processing" in result.output
```

## Testing Output

### Capture Standard Output

Verify command output:

```python
def test_list_command_output():
    """Test list command produces correct output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list", "--format", "table"])

    # Check exit code
    assert result.exit_code == 0

    # Verify output contains expected content
    assert "ID" in result.output
    assert "Name" in result.output
    assert "Status" in result.output

    # Verify output format
    lines = result.output.split("\n")
    assert len(lines) >= 2  # Header + at least one row
```

### Capture Standard Error

Test error messages:

```python
from provide.testkit import set_log_stream_for_testing
from io import StringIO

def test_error_messages():
    """Test error output goes to stderr."""
    # Capture logs
    log_stream = StringIO()
    set_log_stream_for_testing(log_stream)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["invalid-command"])

    assert result.exit_code != 0
    assert "Error" in result.stderr

    # Check logs
    logs = log_stream.getvalue()
    assert "invalid-command" in logs
```

### Test JSON Output

Verify structured output:

```python
import json

def test_json_output():
    """Test command with JSON output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["export", "--format", "json"])

    assert result.exit_code == 0

    # Parse and verify JSON
    data = json.loads(result.output)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]
```

## Testing File Operations

### Test with Temporary Files

Use Click's file isolation:

```python
def test_process_file():
    """Test file processing command."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Create test input file
        with open("input.txt", "w") as f:
            f.write("test data\n")

        # Run command
        result = runner.invoke(cli, ["process", "input.txt"])

        assert result.exit_code == 0

        # Verify output file was created
        assert Path("output.txt").exists()

        # Verify output content
        output = Path("output.txt").read_text()
        assert "PROCESSED: test data" in output
```

### Test File Reading

Test commands that read files:

```python
def test_analyze_file():
    """Test file analysis command."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Create test file with known content
        test_data = "line1\nline2\nline3\n"
        Path("data.txt").write_text(test_data)

        result = runner.invoke(cli, ["analyze", "data.txt"])

        assert result.exit_code == 0
        assert "3 lines" in result.output
        assert "17 bytes" in result.output
```

### Test File Writing

Verify file output:

```python
def test_export_to_file():
    """Test exporting data to file."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            "export",
            "--output", "export.csv",
            "--format", "csv"
        ])

        assert result.exit_code == 0

        # Verify file created
        export_file = Path("export.csv")
        assert export_file.exists()

        # Verify CSV content
        import csv
        with open(export_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) > 0
            assert "id" in rows[0]
```

## Testing Interactive Prompts

### Test Input Prompts

Simulate user input:

```python
def test_interactive_input():
    """Test command with interactive prompts."""
    runner = CliRunner()

    # Simulate user typing "Alice" when prompted
    result = runner.invoke(cli, ["greet"], input="Alice\n")

    assert result.exit_code == 0
    assert "What is your name?" in result.output
    assert "Hello, Alice!" in result.output

def test_multiple_prompts():
    """Test multiple interactive prompts."""
    runner = CliRunner()

    # Simulate multiple inputs
    result = runner.invoke(cli, ["configure"], input="myapp\nproduction\ny\n")

    assert result.exit_code == 0
    assert "App name: myapp" in result.output
    assert "Environment: production" in result.output
```

### Test Confirmation Prompts

Test yes/no confirmations:

```python
def test_confirmation_yes():
    """Test accepting confirmation."""
    runner = CliRunner()

    result = runner.invoke(cli, ["delete", "item-123"], input="y\n")

    assert result.exit_code == 0
    assert "Deleted item-123" in result.output

def test_confirmation_no():
    """Test declining confirmation."""
    runner = CliRunner()

    result = runner.invoke(cli, ["delete", "item-123"], input="n\n")

    assert result.exit_code == 0
    assert "Cancelled" in result.output
    assert "Deleted" not in result.output
```

### Test Password Input

Test secure password prompts:

```python
def test_password_prompt():
    """Test password input (hidden)."""
    runner = CliRunner()

    result = runner.invoke(cli, ["login"], input="alice\nsecret123\n")

    assert result.exit_code == 0
    assert "Username:" in result.output
    assert "Password:" in result.output
    # Password should not appear in output
    assert "secret123" not in result.output
    assert "Logged in as alice" in result.output
```

## Testing Error Handling

### Test Invalid Arguments

Verify error handling for bad input:

```python
def test_invalid_argument_type():
    """Test invalid argument type."""
    runner = CliRunner()

    # Pass string where integer expected
    result = runner.invoke(cli, ["process", "--count", "invalid"])

    assert result.exit_code != 0
    assert "Invalid value for '--count'" in result.output

def test_missing_required_argument():
    """Test missing required argument."""
    runner = CliRunner()

    result = runner.invoke(cli, ["greet"])

    assert result.exit_code != 0
    assert "Missing argument" in result.output
```

### Test File Not Found

Test file error handling:

```python
def test_file_not_found():
    """Test handling of missing file."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["process", "nonexistent.txt"])

        assert result.exit_code != 0
        assert "File not found" in result.output or "does not exist" in result.output
```

### Test Validation Errors

Test custom validation:

```python
def test_email_validation():
    """Test email format validation."""
    runner = CliRunner()

    # Invalid email
    result = runner.invoke(cli, ["register", "--email", "invalid-email"])

    assert result.exit_code != 0
    assert "Invalid email" in result.output

    # Valid email
    result = runner.invoke(cli, ["register", "--email", "user@example.com"])

    assert result.exit_code == 0
```

## Testing Exit Codes

### Verify Success

Test successful execution:

```python
def test_success_exit_code():
    """Test successful command returns 0."""
    runner = CliRunner()

    result = runner.invoke(cli, ["status"])

    assert result.exit_code == 0

def test_all_commands_success():
    """Test all commands can succeed."""
    runner = CliRunner()

    commands = ["status", "version", "help"]

    for cmd in commands:
        result = runner.invoke(cli, [cmd])
        assert result.exit_code == 0, f"Command '{cmd}' failed"
```

### Verify Failure Exit Codes

Test different error conditions:

```python
def test_error_exit_codes():
    """Test appropriate exit codes for errors."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # File not found
        result = runner.invoke(cli, ["process", "missing.txt"])
        assert result.exit_code == 1

        # Invalid input
        result = runner.invoke(cli, ["convert", "--format", "invalid"])
        assert result.exit_code == 2

        # Permission denied (simulated)
        Path("readonly.txt").touch()
        Path("readonly.txt").chmod(0o444)
        result = runner.invoke(cli, ["delete", "readonly.txt"])
        assert result.exit_code != 0
```

## Mocking and Fixtures

### Mock External Dependencies

Mock API calls and external services:

```python
from unittest.mock import patch, MagicMock

def test_api_command_with_mock():
    """Test command that calls external API."""
    runner = CliRunner()

    with patch('myapp.api.client.get_users') as mock_get_users:
        # Setup mock response
        mock_get_users.return_value = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]

        result = runner.invoke(cli, ["list-users"])

        assert result.exit_code == 0
        assert "Alice" in result.output
        assert "Bob" in result.output

        # Verify API was called
        mock_get_users.assert_called_once()
```

### Use Pytest Fixtures

Share test setup:

```python
import pytest
from click.testing import CliRunner

@pytest.fixture
def cli_runner():
    """Provide CLI runner."""
    return CliRunner()

@pytest.fixture
def sample_data_file(cli_runner):
    """Create sample data file."""
    with cli_runner.isolated_filesystem():
        data = "id,name,status\n1,Alice,active\n2,Bob,inactive\n"
        Path("data.csv").write_text(data)
        yield "data.csv"

def test_with_fixture(cli_runner, sample_data_file):
    """Test using fixtures."""
    result = cli_runner.invoke(cli, ["import", sample_data_file])

    assert result.exit_code == 0
    assert "2 records imported" in result.output
```

### Parameterized Tests

Test multiple scenarios:

```python
@pytest.mark.parametrize("input_value,expected", [
    ("5", "Result: 25"),
    ("10", "Result: 100"),
    ("0", "Result: 0"),
])
def test_square_command(input_value, expected):
    """Test square command with various inputs."""
    runner = CliRunner()

    result = runner.invoke(cli, ["square", input_value])

    assert result.exit_code == 0
    assert expected in result.output

@pytest.mark.parametrize("format,extension", [
    ("json", ".json"),
    ("csv", ".csv"),
    ("xml", ".xml"),
])
def test_export_formats(format, extension):
    """Test different export formats."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["export", "--format", format])

        assert result.exit_code == 0

        # Find created file with correct extension
        files = list(Path(".").glob(f"*{extension}"))
        assert len(files) == 1
```

## Testing Async Commands

### Test Async CLI Commands

Test commands using async operations:

```python
import pytest

@pytest.mark.asyncio
async def test_async_command():
    """Test async CLI command."""
    reset_foundation_setup_for_testing()

    from myapp.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["fetch", "https://api.example.com/data"])

    assert result.exit_code == 0
    assert "Data fetched" in result.output
```

## Testing Command Groups

### Test Subcommands

Test commands organized in groups:

```python
def test_user_subcommands():
    """Test user management subcommands."""
    runner = CliRunner()

    # Test create
    result = runner.invoke(cli, ["user", "create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "User created" in result.output

    # Test list
    result = runner.invoke(cli, ["user", "list"])
    assert result.exit_code == 0
    assert "Alice" in result.output

    # Test delete
    result = runner.invoke(cli, ["user", "delete", "Alice"])
    assert result.exit_code == 0
    assert "User deleted" in result.output
```

### Test Help Output

Verify help text:

```python
def test_help_output():
    """Test help text is displayed."""
    runner = CliRunner()

    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output

def test_command_specific_help():
    """Test command-specific help."""
    runner = CliRunner()

    result = runner.invoke(cli, ["process", "--help"])

    assert result.exit_code == 0
    assert "Usage: cli process" in result.output
    assert "Process files" in result.output  # Command description
```

## Best Practices

### ✅ DO: Reset Foundation State

```python
# ✅ Good: Clean state for each test
@pytest.fixture(autouse=True)
def reset_foundation():
    reset_foundation_setup_for_testing()

def test_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["command"])
    assert result.exit_code == 0
```

### ✅ DO: Use Isolated Filesystem

```python
# ✅ Good: Isolate file operations
def test_file_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("test.txt").write_text("data")
        result = runner.invoke(cli, ["process", "test.txt"])
        assert result.exit_code == 0
```

### ✅ DO: Test Both Success and Failure

```python
# ✅ Good: Test happy and error paths
def test_valid_input():
    result = runner.invoke(cli, ["greet", "Alice"])
    assert result.exit_code == 0

def test_invalid_input():
    result = runner.invoke(cli, ["greet"])  # Missing name
    assert result.exit_code != 0
```

### ✅ DO: Verify Output Content

```python
# ✅ Good: Check actual output
def test_output_content():
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Total: 5 items" in result.output

# ❌ Bad: Only check exit code
def test_only_exit_code():
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0  # Could still have wrong output!
```

### ❌ DON'T: Forget to Test Edge Cases

```python
# ✅ Good: Test edge cases
def test_empty_list():
    result = runner.invoke(cli, ["list"])
    assert "No items found" in result.output

def test_special_characters():
    result = runner.invoke(cli, ["greet", "Alice & Bob"])
    assert result.exit_code == 0
```

## Integration Testing

### Test Full Workflows

Test complete user workflows:

```python
def test_full_workflow():
    """Test complete user workflow."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Step 1: Initialize
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert Path("config.yml").exists()

        # Step 2: Add data
        result = runner.invoke(cli, ["add", "--name", "Item1"])
        assert result.exit_code == 0

        # Step 3: List data
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "Item1" in result.output

        # Step 4: Export
        result = runner.invoke(cli, ["export", "--format", "json"])
        assert result.exit_code == 0
        assert Path("export.json").exists()
```

## Next Steps

### Related Guides
- **[Unit Testing](unit-tests.md)**: General unit testing with provide-testkit
- **[Building Commands](../cli/commands.md)**: Create CLI commands
- **[CLI Arguments](../cli/arguments.md)**: Advanced argument handling

### Examples
- See `examples/cli/` for CLI application examples
- See `tests/cli/` in the repository for more test patterns

### API Reference
- **[API Reference: CLI](../../reference/provide/foundation/cli/index.md)**: Complete CLI API documentation

---

**Tip**: Always use `CliRunner` in isolated filesystem mode for file operations to avoid test pollution. Use `reset_foundation_setup_for_testing()` to ensure clean state between tests.
