# Tutorial: Quick Start

This tutorial will guide you through installing `provide.foundation` and writing your first application in under 5 minutes. You'll learn the basics of structured logging and see the beautiful console output.

## 1. Installation

First, install the library using `pip` or your favorite package manager.

```bash
pip install "provide-foundation[all]"
```
The `[all]` extra includes dependencies for all optional features, which is great for getting started.

To verify the installation, run:
```bash
python -c "from provide.foundation import logger; logger.info('Installation successful!')"
```
You should see a formatted log message, confirming that everything is working.

## 2. Your First Log Messages

The easiest way to start is to import the global `logger` instance. Create a Python file named `app.py`:

```python
# app.py
from provide.foundation import logger, setup_telemetry

def main():
    """A simple function to demonstrate basic logging."""
    # This single line configures the entire logging system with sensible defaults.
    setup_telemetry()

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

## 3. Running the Example

Execute the script from your terminal:

```bash
python app.py
```

## 4. Understanding the Output

You will see the following output in your console, beautifully formatted and instantly scannable:

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

Let's break down what you're seeing:

1.  **Emoji & Level Prefixes**: Each message is prefixed with a visual marker (`⚠️`, `❌`) and the log level. This provides immediate context about the log's severity and meaning.
2.  **Event Name**: The first argument to the logger (`"user_logged_in"`) is the primary event name.
3.  **Structured Context**: The keyword arguments are automatically formatted as `key=value` pairs. This is the core of **structured logging**, making your logs easy to parse for both humans and machines.
4.  **Exception Information**: When you use `logger.exception()`, the full exception traceback is automatically captured and included.

---

Congratulations! You've successfully used `provide.foundation` to produce structured, human-readable logs.

**Next Steps:**
- Build a more complete application in the **[First Application Tutorial](./02-first-application/)**.
