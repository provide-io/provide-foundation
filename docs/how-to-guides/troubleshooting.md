# Troubleshooting Guide

Common issues and solutions when using provide.foundation.

## Table of Contents

- [Import Errors](#import-errors)
- [Logging Issues](#logging-issues)
- [Configuration Problems](#configuration-problems)
- [Performance Issues](#performance-issues)
- [CLI Problems](#cli-problems)
- [Environment Variable Issues](#environment-variable-issues)
- [Testing Issues](#testing-issues)
- [Integration Problems](#integration-problems)

## Import Errors

### ModuleNotFoundError: No module named 'provide.foundation'

**Symptoms:**
```python
ImportError: No module named 'provide.foundation'
```

**Solutions:**

1. **Install the package:**
   ```bash
   uv add provide-foundation
   ```

2. **Check virtual environment:**
   ```bash
   which python  # Should point to your venv
   uv run python -c "import importlib.metadata as m; print(m.version('provide-foundation'))"
   ```

3. **Verify Python version:**
   ```bash
   python --version  # Must be 3.11 or higher
   ```

---

### ImportError: cannot import name 'X' from 'provide.foundation'

**Symptoms:**
```python
ImportError: cannot import name 'pout' from 'provide.foundation'
```

**Solutions:**

1. **Check if you need an optional dependency:**
   ```bash
   # CLI features require [cli] extra
   uv add provide-foundation[cli]

   # Crypto features require [crypto] extra
   uv add provide-foundation[crypto]

   # Or install everything
   uv add provide-foundation[all]
   ```

2. **Verify import path:**
   ```python
   # ✅ Correct
   from provide.foundation import logger, pout, perr

   # ❌ Wrong
   from provide import foundation  # Don't do this
   ```

---

### ModuleNotFoundError: No module named 'click'

**Symptoms:**
```python
ModuleNotFoundError: No module named 'click'
```

**Solution:**

Install CLI extras:
```bash
uv add provide-foundation[cli]
```

---

## Logging Issues

### Logs Not Appearing

**Symptoms:**
- No log output to console
- Expected logs missing

**Solutions:**

1. **Check log level:**
   ```bash
   # Set log level to see more logs
   export PROVIDE_LOG_LEVEL=DEBUG
   python your_script.py
   ```

2. **Verify logger is being used:**
   ```python
   from provide.foundation import logger

   # ✅ Correct
   logger.info("This will log")

   # ❌ Wrong - using print instead
   print("This won't go to logs")
   ```

3. **Check if logs are going to the right stream:**
   ```python
   # Logs go to stderr by default
   python your_script.py 2>&1 | less
   ```

---

### Logs Missing Context Fields

**Symptoms:**
```
Expected: {"event": "user_login", "user_id": "123"}
Got: {"event": "user_login"}
```

**Solutions:**

1. **Use keyword arguments:**
   ```python
   # ✅ Correct
   logger.info("user_login", user_id="123")

   # ❌ Wrong - missing context
   logger.info("user_login 123")
   ```

2. **Check field naming:**
   ```python
   # Field names must be valid Python identifiers
   logger.info("event", valid_field="value")
   logger.info("event", **{"valid-field": "value"})  # Use ** for non-identifier names
   ```

---

### JSON Logs Not Formatted

**Symptoms:**
- Logs appear as plain text instead of JSON
- Log aggregation tools can't parse logs

**Solution:**

Enable JSON format:
```bash
export PROVIDE_LOG_FORMAT=json
python your_script.py
```

Output:
```json
{"event": "user_login", "level": "info", "timestamp": "2025-10-24T10:00:00Z"}
```

---

###  Emojis Not Showing in Logs

**Symptoms:**
- Emojis appear as `?` or boxes
- No emoji prefixes on log messages

**Solutions:**

1. **Check terminal encoding:**
   ```bash
   # Set UTF-8 encoding
   export LANG=en_US.UTF-8
   export LC_ALL=en_US.UTF-8
   ```

2. **Use console format (not JSON):**
   ```bash
   export PROVIDE_LOG_FORMAT=console
   ```

3. **Disable emojis if needed:**
   ```bash
   export PROVIDE_DISABLE_EMOJIS=true
   ```

---

### Third-Party Library Logs Too Verbose

**Symptoms:**
```
DEBUG:urllib3:Starting new HTTPS connection
DEBUG:asyncio:Using selector: KqueueSelector
```

**Solution:**

Control module log levels:
```bash
# Suppress urllib3 and asyncio debug logs
export PROVIDE_LOG_MODULE_LEVELS="urllib3:WARNING,asyncio:WARNING"
```

Or programmatically:
```python
from provide.foundation.logger import set_module_log_level

set_module_log_level("urllib3", "WARNING")
set_module_log_level("asyncio", "WARNING")
```

---

## Configuration Problems

### Environment Variables Not Loading

**Symptoms:**
- Environment variables set but not being read
- Config shows default values instead of env values

**Solutions:**

1. **Verify variable names:**
   ```bash
   # Foundation looks for PROVIDE_* prefix
   export PROVIDE_LOG_LEVEL=DEBUG  # ✅ Correct
   export LOG_LEVEL=DEBUG  # ❌ Wrong prefix
   ```

2. **Check variable is exported:**
   ```bash
   # ✅ Export variable
   export PROVIDE_LOG_LEVEL=DEBUG

   # ❌ Just setting doesn't export
   PROVIDE_LOG_LEVEL=DEBUG
   ```

3. **Verify in environment:**
   ```bash
   env | grep PROVIDE
   ```

---

### BaseConfig.from_env() Not Working

**Symptoms:**
```python
config = MyConfig.from_env()  # Values are None or defaults
```

**Solutions:**

1. **Use env_field() decorator:**
   ```python
   from provide.foundation.config import BaseConfig, env_field
   from attrs import define

   @define
   class MyConfig(BaseConfig):
       # ✅ Correct
       api_key: str = env_field(env_var="API_KEY")

       # ❌ Wrong - missing env_field
       db_host: str = "localhost"  # Won't load from env
   ```

2. **Check environment variable is set:**
   ```bash
   export API_KEY="my-secret-key"
   ```

---

### File-Based Secrets Not Loading

**Symptoms:**
```python
config.password = "file:///run/secrets/password"  # Should be file contents
```

**Solutions:**

1. **Verify file exists:**
   ```bash
   ls -la /run/secrets/password
   cat /run/secrets/password
   ```

2. **Check file permissions:**
   ```bash
   chmod 400 /run/secrets/password  # Read-only for owner
   ```

3. **Use correct file:// syntax:**
   ```bash
   # ✅ Correct
   export DB_PASSWORD="file:///run/secrets/db_password"

   # ❌ Wrong - missing file:// prefix
   export DB_PASSWORD="/run/secrets/db_password"
   ```

---

## Performance Issues

### Slow Logging Performance

**Symptoms:**
- Application slows down significantly with logging
- High CPU usage

**Solutions:**

1. **Reduce log level:**
   ```bash
   # Only log INFO and above in production
   export PROVIDE_LOG_LEVEL=INFO
   ```

2. **Avoid logging in tight loops:**
   ```python
   # ❌ Bad: Logs in loop
   for item in million_items:
       logger.debug("Processing", item=item)  # Too much!

   # ✅ Good: Log summary
   logger.info("Processing batch", count=len(million_items))
   for item in million_items:
       process(item)
   logger.info("Batch completed")
   ```

3. **Use sampling for high-frequency events:**
   ```python
   import random

   for i, item in enumerate(items):
       # Only log 1% of items
       if random.random() < 0.01:
           logger.debug("Processing sample", item=item, position=i)
   ```

---

### High Memory Usage

**Symptoms:**
- Memory grows over time
- Out of memory errors

**Solutions:**

1. **Check for log buffering:**
   ```python
   # Flush logs regularly
   import sys
   sys.stderr.flush()
   ```

2. **Avoid storing large objects in log context:**
   ```python
   # ❌ Bad: Logs entire large object
   logger.info("Processing", data=large_dataframe)

   # ✅ Good: Log summary
   logger.info("Processing", row_count=len(large_dataframe))
   ```

3. **Clear log handlers if dynamically creating loggers:**
   ```python
   import logging

   # Clear handlers to prevent accumulation
   logger_obj = logging.getLogger("my_logger")
   logger_obj.handlers.clear()
   ```

---

## CLI Problems

### Commands Not Discovered

**Symptoms:**
```bash
$ mycli mycommand
Error: No such command 'mycommand'
```

**Solutions:**

1. **Verify @register_command decorator:**
   ```python
   from provide.foundation.hub import register_command

   # ✅ Correct
   @register_command("mycommand")
   def my_command():
       pass

   # ❌ Wrong - missing decorator
   def my_command():
       pass
   ```

2. **Ensure module is imported:**
   ```python
   # In your main file
   import my_commands  # Must import to register

   hub = get_hub()
   cli = hub.create_cli()
   cli()
   ```

3. **Check command name:**
   ```python
   # Command name must be lowercase, use hyphens
   @register_command("process-data")  # ✅ Good
   @register_command("processData")   # ❌ Not idiomatic
   ```

---

### CLI Help Text Not Showing

**Symptoms:**
- `--help` shows empty or generic help
- Command descriptions missing

**Solution:**

Add docstrings:
```python
@register_command("process")
def process_data(input_file: str):
    """Process data from input file.

    Args:
        input_file: Path to the input data file
    """
    pass
```

---

## Environment Variable Issues

### Boolean Variables Not Parsing

**Symptoms:**
```python
debug = get_bool("DEBUG")  # Returns None even when DEBUG=false
```

**Solutions:**

1. **Use accepted boolean values:**
   ```bash
   # ✅ Truthy values
   export DEBUG=true
   export DEBUG=1
   export DEBUG=yes
   export DEBUG=on

   # ✅ Falsy values
   export DEBUG=false
   export DEBUG=0
   export DEBUG=no
   export DEBUG=off
   export DEBUG=""  # Empty string is false

   # ❌ Wrong
   export DEBUG=False  # Case-sensitive, should be lowercase
   ```

2. **Check for required vs optional:**
   ```python
   # Returns None if not set
   debug = get_bool("DEBUG")

   # Raises error if not set
   debug = get_bool("DEBUG", required=True)

   # Uses default if not set
   debug = get_bool("DEBUG", default=False)
   ```

---

### List Variables Not Parsing

**Symptoms:**
```python
hosts = get_list("HOSTS")  # Expected list, got string
```

**Solutions:**

1. **Use comma separation:**
   ```bash
   # ✅ Correct
   export HOSTS="host1,host2,host3"

   # ❌ Wrong - spaces without commas
   export HOSTS="host1 host2 host3"
   ```

2. **Custom separator:**
   ```python
   # For colon-separated values
   paths = get_list("PATH", separator=":")
   ```

---

## Testing Issues

### Tests Failing Due to Shared State

**Symptoms:**
- Tests pass individually but fail when run together
- Random test failures

**Solutions:**

1. **Use provide-testkit:**
   ```bash
   uv add provide-testkit
   ```

2. **Reset Foundation state:**
   ```python
   import pytest
   from provide.testkit import reset_foundation_setup_for_testing

   @pytest.fixture(autouse=True)
   def reset_foundation():
       """Reset Foundation state before each test."""
       reset_foundation_setup_for_testing()
   ```

3. **Isolate test configuration:**
   ```python
   def test_with_custom_config():
       """Test with isolated configuration."""
       reset_foundation_setup_for_testing()

       # Set test-specific config
       from provide.foundation import get_hub
       hub = get_hub()
       hub.initialize_foundation(test_config)

       # Run test
       assert something()
   ```

---

### Log Output Polluting Test Output

**Symptoms:**
- Test output cluttered with log messages
- Hard to read test results

**Solutions:**

1. **Capture logs in tests:**
   ```python
   from provide.testkit import set_log_stream_for_testing
   from io import StringIO

   def test_with_captured_logs():
       log_stream = StringIO()
       set_log_stream_for_testing(log_stream)

       # Run code that logs
       my_function()

       # Check logs
       logs = log_stream.getvalue()
       assert "expected_message" in logs
   ```

2. **Suppress logs in tests:**
   ```bash
   # Run tests with minimal logging
   PROVIDE_LOG_LEVEL=ERROR pytest
   ```

---

## Integration Problems

### FastAPI/Flask Integration Issues

**Symptoms:**
- Request context not preserved in logs
- Logs from different requests mixed together

**Solution:**

Use correlation IDs:
```python
from fastapi import FastAPI, Request
from provide.foundation import logger
import uuid

app = FastAPI()

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    """Add correlation ID to each request."""
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())

    # Add to all logs in this request
    with logger.bind(correlation_id=correlation_id):
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response
```

---

### Celery Integration Issues

**Symptoms:**
- Logs from different Celery tasks mixed together
- Can't track which logs belong to which task

**Solution:**

Bind task context:
```python
from celery import Task
from provide.foundation import logger

class FoundationTask(Task):
    """Celery task with Foundation logging."""

    def __call__(self, *args, **kwargs):
        with logger.bind(task_id=self.request.id, task_name=self.name):
            return super().__call__(*args, **kwargs)

@celery.task(base=FoundationTask)
def my_task(user_id):
    logger.info("Processing task", user_id=user_id)
    # All logs will include task_id and task_name
```

---

## Getting More Help

### Enable Debug Logging

Get maximum visibility:
```bash
export PROVIDE_LOG_LEVEL=DEBUG
export PROVIDE_LOG_FORMAT=console
python your_script.py
```

### Check Versions

Verify you're using compatible versions:
```bash
uv run python -c "import importlib.metadata as m; print(m.version('provide-foundation'))"
python --version
```

### Reproduce in Minimal Example

Create a minimal reproduction:
```python
from provide.foundation import logger

logger.info("Testing basic logging")
# Add minimal code to reproduce your issue
```

### Report Issues

If you've found a bug:

1. **Check existing issues:** [GitHub Issues](https://github.com/provide-io/provide-foundation/issues)
2. **Create a new issue** with:
   - Python version
   - Foundation version
   - Minimal reproduction code
   - Expected vs actual behavior
   - Full error traceback

---

## Common Error Messages

### RuntimeError: Foundation not initialized

**Message:**
```
RuntimeError: Foundation not initialized. Call get_hub().initialize_foundation() first.
```

**Solution:**
```python
from provide.foundation import get_hub

# Initialize before using Foundation features
hub = get_hub()
hub.initialize_foundation()

# Now you can use Foundation
from provide.foundation import logger
logger.info("Ready to go")
```

---

### AttributeError: module 'provide.foundation' has no attribute 'X'

**Message:**
```
AttributeError: module 'provide.foundation' has no attribute 'CircuitBreaker'
```

**Solution:**

Import from the correct submodule:
```python
# ✅ Correct
from provide.foundation.resilience import CircuitBreaker

# ❌ Wrong
from provide.foundation import CircuitBreaker
```

---

### CircuitBreakerOpen: Circuit breaker is open

**Message:**
```
CircuitBreakerOpen: Circuit breaker 'api_service' is open
```

**Solution:**

This is expected behavior when a circuit breaker trips. Options:

1. **Implement fallback:**
   ```python
   try:
       result = call_api()
   except CircuitBreakerOpen:
       result = get_cached_result()
   ```

2. **Wait for circuit to close:**
   - Circuit automatically resets after timeout period
   - Check `circuit.state` to monitor recovery

3. **Adjust thresholds:**
   ```python
   # Make circuit less sensitive
   @circuit_breaker(
       failure_threshold=10,  # More failures before opening
       timeout=30,  # Shorter recovery time
   )
   def call_api():
       pass
   ```

---

## Still Having Issues?

1. **Review the documentation:** [foundry.provide.io](https://foundry.provide.io/provide-foundation/)
2. **Check examples:** Look at `examples/` in the repository
3. **Ask for help:** Open a [GitHub Discussion](https://github.com/provide-io/provide-foundation/discussions)
4. **Report bugs:** Create an [Issue](https://github.com/provide-io/provide-foundation/issues)

---

**Tip**: When troubleshooting, start with `PROVIDE_LOG_LEVEL=DEBUG` to see what's happening internally. Most issues become clear with debug logging enabled.
