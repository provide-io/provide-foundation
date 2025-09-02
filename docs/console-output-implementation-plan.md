# Console Output Standardization Implementation Plan

## Executive Summary

### Problem Statement
The current codebase uses multiple inconsistent methods for console output:
- Direct `click.echo()` and `click.secho()` calls
- `provide.foundation.cli` utils (`echo_error`, `echo_info`, etc.)
- `wrknv.wenv.visual` print functions using Rich
- Raw `print()` statements
- Mixed stdout/stderr usage without clear patterns

This inconsistency leads to:
- Difficult testing (hard to mock/capture output)
- Inconsistent user experience
- No centralized control over output formatting
- Poor JSON output support
- Incorrect stream usage (e.g., errors to stdout)

### Proposed Solution
Implement three standardized console output functions:
- **`pout()`** - Program output to stdout
- **`perr()`** - Errors/warnings/info to stderr  
- **`plog()`** - Structured logging via foundation.logger

### Key Benefits
- **Consistency**: Single source of truth for all console output
- **Testability**: Easy to mock and capture output in tests
- **Flexibility**: JSON mode, color support, emoji prefixes
- **Correctness**: Proper stdout/stderr separation
- **Maintainability**: Centralized control over output behavior

## Current State Analysis

### Existing Output Methods

1. **provide.foundation.cli.utils**
   - `echo_error()` - Red text with ✗ prefix to stderr
   - `echo_success()` - Green text with ✓ prefix to stdout
   - `echo_warning()` - Yellow text with ⚠ prefix to stderr
   - `echo_info()` - Plain text with ℹ prefix to stdout
   - `echo_json()` - JSON output with proper serialization
   - Usage: 187 occurrences across 8 command files

2. **wrknv.wenv.visual**
   - `print_error()` - Using Rich console with theme
   - `print_success()` - Rich formatted output
   - `print_warning()` - Rich formatted output
   - `print_info()` - Rich formatted output
   - Duplicate functionality with different implementation

3. **Direct Usage**
   - `click.echo()` - Scattered throughout codebase
   - `click.secho()` - For colored output
   - `print()` - In various utility functions
   - `sys.stdout.write()` - Low-level output

### Pain Points
- No consistent way to switch between normal and JSON output
- Testing requires mocking multiple different functions
- Stream selection (stdout vs stderr) is inconsistent
- No centralized emoji/symbol management
- Rich vs Click formatting conflicts

## Proposed Architecture

### Module Structure
```
provide/foundation/
├── console.py          # New console output module
├── cli/
│   └── utils.py       # Updated to use console.py
└── context.py         # Extended with console settings
```

### Core Design Principles

1. **Stream Separation**
   - stdout: Program results, data output, normal messages
   - stderr: Errors, warnings, debug info, progress updates
   - Follows Unix philosophy for proper piping/redirection

2. **Context Awareness**
   - Automatically detect JSON mode from Context
   - Respect color settings from environment
   - Support quiet/verbose modes

3. **Layered Architecture**
   - console.py wraps click.echo for portability
   - cli.utils becomes thin wrappers around console
   - Commands use high-level functions only

## API Design

### Core Functions

#### `pout(message, **kwargs)`
```python
def pout(
    message: Any,
    json_key: str | None = None,
    color: str | None = None,
    bold: bool = False,
    nl: bool = True,
    ctx: Context | None = None
) -> None:
    """
    Output to stdout for program results.
    
    Args:
        message: Content to output (will be stringified)
        json_key: Key for JSON output mode (e.g., "result")
        color: Optional color name for styling
        bold: Whether to bold the text
        nl: Whether to add newline
        ctx: Optional context (auto-detected if not provided)
    
    Example:
        pout("Processing complete")  # Normal output
        pout(data, json_key="data")  # JSON-aware output
        pout("Success!", color="green", bold=True)
    """
```

#### `perr(message, level="error", **kwargs)`
```python
def perr(
    message: Any,
    level: Literal["error", "warning", "info", "debug"] = "error",
    json_key: str | None = None,
    prefix: bool = True,
    emoji: str | None = None,
    ctx: Context | None = None
) -> None:
    """
    Output to stderr for errors, warnings, and status.
    
    Args:
        message: Content to output
        level: Message level (determines color and default emoji)
        json_key: Key for JSON output mode
        prefix: Whether to add emoji prefix
        emoji: Custom emoji (overrides default for level)
        ctx: Optional context
    
    Example:
        perr("File not found")  # Error with ❌
        perr("Deprecated", level="warning")  # Warning with ⚠️
        perr("Loading...", level="info", emoji="⏳")
    """
```

#### `plog(message, **fields)`
```python
def plog(
    message: str,
    level: str = "info",
    **fields: Any
) -> None:
    """
    Structured logging via foundation.logger.
    
    Args:
        message: Log message
        level: Log level (debug, info, warning, error, critical)
        **fields: Additional structured fields
    
    Example:
        plog("Starting process", pid=1234, user="admin")
        plog("Database error", level="error", code=500, query=sql)
    """
```

### Helper Functions

#### `with_json_mode(ctx: Context | None = None)`
```python
@contextmanager
def with_json_mode(enabled: bool = True):
    """Context manager to temporarily enable/disable JSON output."""
```

#### `capture_output()`
```python
@contextmanager
def capture_output():
    """Context manager to capture console output for testing."""
```

### Configuration Classes

#### Console Settings Extension to Context
```python
@define(slots=True, frozen=False)
class Context:
    # Existing fields...
    
    # Console output settings
    console_json: bool = field(default=False)
    console_color: bool = field(default=True)
    console_emoji: bool = field(default=True)
    console_quiet: bool = field(default=False)
    console_verbose: int = field(default=0)  # -v count
```

## Implementation Details

### Core Implementation

```python
# provide/foundation/console.py

import json
import sys
from typing import Any, Literal
import click
from provide.foundation.context import Context
from provide.foundation.logger import get_logger

# Emoji mappings
LEVEL_EMOJI = {
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "debug": "🔍",
    "success": "✅",
}

LEVEL_COLORS = {
    "error": "red",
    "warning": "yellow", 
    "info": "blue",
    "debug": "dim",
    "success": "green",
}

def _get_context() -> Context | None:
    """Get current context from Click or environment."""
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(ctx, "obj") and isinstance(ctx.obj, Context):
        return ctx.obj
    return None

def _should_use_json(ctx: Context | None = None) -> bool:
    """Determine if JSON output should be used."""
    if ctx is None:
        ctx = _get_context()
    return ctx.console_json if ctx else False

def _should_use_color(ctx: Context | None = None) -> bool:
    """Determine if color output should be used."""
    if ctx is None:
        ctx = _get_context()
    if ctx and not ctx.console_color:
        return False
    return sys.stdout.isatty() or sys.stderr.isatty()
```

### JSON Mode Handling

```python
def _output_json(data: Any, stream=sys.stdout) -> None:
    """Output data as JSON."""
    try:
        json_str = json.dumps(data, indent=2, default=str)
        click.echo(json_str, file=stream)
    except (TypeError, ValueError) as e:
        # Fallback to string representation
        click.echo(json.dumps({"error": f"JSON encoding failed: {e}", 
                              "data": str(data)}), file=stream)
```

### Stream Selection Logic

- **stdout**: Results, data, help text, success messages
- **stderr**: Errors, warnings, progress, debug info
- Respects Unix conventions for piping and redirection
- Can be overridden per-call if needed

## Migration Strategy

### Phase 1: Core Implementation (Week 1)
1. Create `provide/foundation/console.py`
2. Implement `pout()`, `perr()`, `plog()`
3. Add Context extensions for console settings
4. Write comprehensive unit tests

### Phase 2: Foundation Migration (Week 2)
1. Update `provide.foundation.cli.utils` to use console
2. Maintain backward compatibility with deprecation warnings
3. Update foundation tests

### Phase 3: Command Migration (Weeks 3-4)
1. Migrate wrknv commands file by file:
   - container.py (26 uses)
   - tools.py (14 uses)
   - config.py (26 uses)
   - setup.py (22 uses)
2. Test each migrated command
3. Update command tests

### Phase 4: Cleanup (Week 5)
1. Remove `wrknv.wenv.visual` print functions
2. Remove deprecated functions from cli.utils
3. Update all documentation
4. Final testing pass

### Phase 5: Release (Week 6)
1. Update changelog
2. Bump version
3. Release notes highlighting new console API
4. Migration guide for external users

## Testing Strategy

### Unit Tests
```python
def test_pout_normal_mode():
    """Test pout in normal text mode."""
    with capture_output() as (out, err):
        pout("Hello World")
    assert out.getvalue() == "Hello World\n"
    assert err.getvalue() == ""

def test_pout_json_mode():
    """Test pout in JSON mode."""
    ctx = Context(console_json=True)
    with capture_output() as (out, err):
        pout("Hello", json_key="message", ctx=ctx)
    data = json.loads(out.getvalue())
    assert data == {"message": "Hello"}

def test_perr_levels():
    """Test perr with different levels."""
    with capture_output() as (out, err):
        perr("Error", level="error")
        perr("Warning", level="warning")
    assert "❌ Error" in err.getvalue()
    assert "⚠️ Warning" in err.getvalue()
```

### Integration Tests
- Test with actual CLI commands
- Verify stream separation works correctly
- Test JSON mode end-to-end
- Test color output in TTY vs non-TTY

### Mocking Strategy
```python
@patch('provide.foundation.console.pout')
@patch('provide.foundation.console.perr')
def test_command_output(mock_perr, mock_pout):
    """Test command uses console functions correctly."""
    result = runner.invoke(cli, ['status'])
    mock_pout.assert_called_with("Status: OK")
    mock_perr.assert_not_called()
```

## Backwards Compatibility

### Deprecation Plan
1. Version 1.0: Add console.py, mark old functions as deprecated
2. Version 1.1: Show deprecation warnings
3. Version 2.0: Remove deprecated functions

### Compatibility Layer
```python
# provide/foundation/cli/utils.py
def echo_error(message: str, json_output: bool = False) -> None:
    """DEPRECATED: Use perr() instead."""
    import warnings
    warnings.warn(
        "echo_error is deprecated, use perr() instead",
        DeprecationWarning,
        stacklevel=2
    )
    perr(message, level="error", ctx=Context(console_json=json_output))
```

## Documentation Updates

### API Reference
- Add console.py to API docs
- Document all functions with examples
- Add migration guide section

### User Guide Updates
- Update CLI development guide
- Add console output best practices
- Update testing documentation

### Example Updates
```python
# Before
from provide.foundation.cli import echo_error, echo_success
echo_error("Failed to connect")
echo_success("Connected!")

# After  
from provide.foundation.console import perr, pout
perr("Failed to connect")
pout("Connected!", color="green")
```

## Success Metrics

### Quantitative
- 100% test coverage for console module
- Zero direct click.echo calls in command files
- All tests passing with new implementation
- <5ms overhead for console functions

### Qualitative
- Consistent output formatting across all commands
- Easier to test command output
- Clear separation of stdout/stderr
- Improved JSON mode support
- Better error messages with proper formatting

## Risk Mitigation

### Risks
1. **Breaking Changes**: Existing scripts may depend on output format
   - Mitigation: Careful deprecation, compatibility layer
   
2. **Performance**: Additional abstraction layer overhead
   - Mitigation: Benchmark and optimize hot paths
   
3. **Color/Emoji Support**: Terminal compatibility issues  
   - Mitigation: Auto-detection, disable flags, environment variables

4. **Testing Complexity**: Mock/capture complexity
   - Mitigation: Provide testing utilities, clear examples

## Timeline

| Week | Milestone | Deliverables |
|------|-----------|--------------|
| 1 | Core Implementation | console.py, unit tests |
| 2 | Foundation Integration | Updated cli.utils, tests |
| 3-4 | Command Migration | Migrated commands, tests |
| 5 | Cleanup & Testing | Removed old code, full test suite |
| 6 | Release Preparation | Docs, changelog, release |

## Appendix: Usage Examples

### Basic Usage
```python
from provide.foundation.console import pout, perr, plog

# Simple output
pout("Processing complete")

# Error with auto-formatting
perr("Connection failed", level="error")

# Structured logging
plog("Request received", method="GET", path="/api/users", status=200)
```

### JSON Mode
```python
# Automatically detected from context
ctx = Context(console_json=True)
pout("Done", json_key="status", ctx=ctx)
# Output: {"status": "Done"}

perr("Not found", level="error", json_key="error", ctx=ctx)  
# Output: {"error": "Not found", "level": "error"}
```

### Custom Formatting
```python
# Custom colors
pout("Success!", color="green", bold=True)

# Custom emoji
perr("Loading data", level="info", emoji="📊")

# No emoji prefix
perr("Plain message", prefix=False)
```

### Testing
```python
from provide.foundation.console import capture_output

def test_my_command():
    with capture_output() as (out, err):
        result = runner.invoke(cli, ['my-command'])
    
    assert "Expected output" in out.getvalue()
    assert err.getvalue() == ""
```

## Conclusion

This implementation plan provides a clear path to standardizing console output across the provide.foundation and wrknv codebases. By following Python best practices and Unix conventions, we'll create a more maintainable, testable, and user-friendly CLI experience.