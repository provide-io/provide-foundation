# 📚 API Reference

## Logger

This section provides a detailed reference for the core logging interface of `provide.foundation`.

The primary entry point for all logging is the global `logger` instance, which is an instance of `FoundationLogger`.

---

### The Global Logger Instance

::: provide.foundation.logger.base.logger

---

### `FoundationLogger` Class

::: provide.foundation.logger.base.FoundationLogger
    options:
      show_root_heading: false
      members:
        - get_logger
        - trace
        - debug
        - info
        - warning
        - error
        - exception
        - critical