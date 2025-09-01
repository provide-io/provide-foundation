# 🚀 Getting Started

## ⚡ Quick Start Guide

This guide will walk you through the absolute basics of using `provide.foundation`. You'll see how to import the global logger and log different kinds of messages.

### Your First Log Messages

The easiest way to start is to import the global `logger` instance and call its methods. Create a Python file named `app.py` with the following content:

```python
# app.py
from provide.foundation import logger

def main():
    """A simple function to demonstrate basic logging."""
    logger.info("Application starting up")

    # Logging with structured context
    logger.info(
        "User logged in",
        user_id="usr_12345",
        source="google_oauth",
        ip_address="192.168.1.101",
    )

    logger.warning("Disk space is running low", free_space_gb=5)

    # Logging an error with exception info
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception(
            "An expected error occurred during a critical calculation",
            error_details="Attempted to divide by zero",
            user_id="usr_12345",
        )

    logger.info("Application shutting down")

if __name__ == "__main__":
    main()

```

### Running the Example

Execute the script from your terminal:

```bash
python app.py
```

### Understanding the Output

You will see the following output in your console, beautifully formatted and instantly scannable:

```
[▶️] Application starting up
[▶️] User logged in user_id=usr_12345 source=google_oauth ip_address=192.168.1.101
[⚠️] Disk space is running low free_space_gb=5
[🔥] An expected error occurred during a critical calculation error_details='Attempted to divide by zero' user_id=usr_12345 exc_info=... # Traceback follows
[▶️] Application shutting down
```

Let's break down what you're seeing:

1.  **Emoji Prefixes**: Each message is prefixed with an emoji (`▶️`, `⚠️`, `🔥`). This is part of the **Domain-Action-Status** pattern, which provides immediate visual context about the log's meaning. `▶️` for informational events, `⚠️` for warnings, and `🔥` for errors.

2.  **Log Message**: The main, human-readable message for the event.

3.  **Structured Context**: The keyword arguments you passed to the logger methods are automatically formatted as `key=value` pairs. This is the core of **structured logging**.

4.  **Exception Information**: When you use `logger.exception()`, the full exception traceback is automatically captured and included with the log message, which is invaluable for debugging.

---

Congratulations! You've successfully used `provide.foundation` to produce structured, human-readable logs.

Next, dive into the [**Core Concepts**](../core-concepts/structured-logging.md) to understand the principles that make this library so powerful.
