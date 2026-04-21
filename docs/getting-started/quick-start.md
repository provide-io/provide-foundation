# Quick Start

Get started with provide.foundation in under 5 minutes. This guide shows you the basics of structured logging and beautiful console output.

## 1. Installation

First, install the library:

```bash
uv add provide-foundation[all]
```

Verify the installation:
```bash
python -c "from provide.foundation import logger; logger.info('Installation successful!')"
```

## 2. Your First Log Messages

The easiest way to start is importing the global `logger` instance. Create a Python file named `app.py`:

```python
# app.py
from provide.foundation import logger

def main():
    """A simple function to demonstrate basic logging."""
    # The logger auto-initializes on first use with sensible defaults.
    # No setup required!

    logger.info("Application starting up")

    # Logging with structured context (key-value pairs)
    logger.info(
        "user_logged_in",
        user_id="usr_12345",
        source="google_oauth",
        ip_address="192.168.1.101",
    )

    logger.warning("Disk space is running low", free_space_gb=5, emoji="⚠️")

    # Logging an error with automatic exception info
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception(
            "critical_calculation_failed",
            details="Attempted to divide by zero",
            user_id="usr_12345",
        )

    logger.info("Application shutting down")

if __name__ == "__main__":
    main()
```

*This code is based on `examples/telemetry/01_basic_logging.py`.*

## 3. Running the Example

Execute the script:

```bash
python app.py
```

## 4. Understanding the Output

You'll see beautifully formatted output in your console:

```
INFO Application starting up
INFO user_logged_in user_id=usr_12345 source=google_oauth ip_address=192.168.1.101
⚠️ WARN Disk space is running low free_space_gb=5
❌ ERROR critical_calculation_failed details='Attempted to divide by zero' user_id=usr_12345
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
INFO Application shutting down
```

### Key Features You're Seeing:

1. **Emoji & Level Prefixes**: Visual markers (`⚠️`, `❌`) provide immediate context
2. **Event Name**: First argument (`"user_logged_in"`) identifies the event
3. **Structured Context**: Keyword arguments formatted as `key=value` pairs
4. **Exception Information**: Full traceback automatically captured with `logger.exception()`

## 5. Adding User-Facing Output

Foundation separates system logs from user output:

```python
from provide.foundation import logger, pout, perr

def process_file(filename: str):
    """Process a file and show progress to the user."""

    # Log for operators/debugging (goes to logs)
    logger.info("file_processing_started", filename=filename)

    # Show to user (goes to stdout)
    pout(f"Processing {filename}...", color="cyan")

    try:
        # ... do the work ...
        logger.info("file_processing_completed", filename=filename)
        pout(f"✅ Successfully processed {filename}", color="green")

    except Exception as e:
        logger.error("file_processing_failed", filename=filename, error=str(e))
        perr(f"❌ Failed to process {filename}: {e}", color="red")
```

### Output Separation:
- **`logger.*`**: System logs for debugging and monitoring
- **`pout()`**: Success messages for users (stdout)
- **`perr()`**: Error messages for users (stderr)

## 6. Configuration (Optional)

Foundation works with zero configuration, but you can customize it when needed.

### When to Initialize Explicitly

**Auto-initialization (default) - Use for:**
- ✅ Simple scripts and utilities
- ✅ Development and experimentation
- ✅ When default configuration is sufficient
- ✅ Quick prototypes

**Explicit initialization - Use for:**
- ✅ Production applications
- ✅ Custom configuration requirements
- ✅ Integration with web frameworks (FastAPI, Flask, Django)
- ✅ Multiple services with different configurations
- ✅ When you need control over service name, log format, or telemetry

### Explicit Configuration Example

```python
from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

# Initialize with custom configuration
config = TelemetryConfig(
    service_name="my-app",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json",  # Use JSON for production
    ),
)

hub = get_hub()
hub.initialize_foundation(config)

# Now use the logger normally
from provide.foundation import logger
logger.info("app_started", version="1.0.0")
```

## What You've Learned

✅ **Zero-configuration logging** - Just import and use
✅ **Structured logging** - Key-value pairs for machine-readable logs
✅ **Exception handling** - Automatic traceback capture
✅ **Output separation** - Logs vs user-facing messages
✅ **Optional configuration** - Customize when needed

## Next Steps

### Build a Complete Application
Continue to [First Application](first-app.md) to build a full CLI task manager (15 minutes).

### Explore Specific Features

- **[Basic Logging Guide](../how-to-guides/logging/basic-logging.md)** - Learn more logging patterns
- **[Exception Logging](../how-to-guides/logging/exception-logging.md)** - Handle errors effectively
- **[CLI Commands](../how-to-guides/cli/commands.md)** - Build command-line tools

### See More Examples

Browse the [Examples](examples.md) section for:
- Configuration management
- Async logging
- HTTP client usage
- Distributed tracing
- Production patterns

---

**Questions?** Check the [How-To Guides](../how-to-guides/logging/basic-logging.md) or [API Reference](../reference/index.md).
