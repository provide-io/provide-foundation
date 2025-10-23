# Custom Log Processors

Learn how to create custom log processors to transform or enrich log events.

## Overview

Processors are functions that transform log events before they're written. Use them to add context, filter sensitive data, or format output.

## Creating a Simple Processor

```python
from provide.foundation import get_hub
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

def add_hostname_processor(logger, method_name, event_dict):
    """Add hostname to every log event."""
    import socket
    event_dict["hostname"] = socket.gethostname()
    return event_dict

# Register the processor
hub = get_hub()
hub.initialize_foundation(
    TelemetryConfig(
        service_name="my-app",
        logging=LoggingConfig(
            processors=[add_hostname_processor]
        )
    )
)
```

## Filtering Sensitive Data

```python
def sanitize_secrets(logger, method_name, event_dict):
    """Remove sensitive data from logs."""
    sensitive_keys = {"password", "api_key", "token", "secret"}

    for key in list(event_dict.keys()):
        if any(s in key.lower() for s in sensitive_keys):
            event_dict[key] = "***REDACTED***"

    return event_dict
```

## Conditional Processing

```python
def production_only_processor(logger, method_name, event_dict):
    """Only process in production environment."""
    import os

    if os.getenv("ENVIRONMENT") != "production":
        return event_dict

    # Add production-specific context
    event_dict["environment"] = "production"
    event_dict["region"] = os.getenv("AWS_REGION", "unknown")

    return event_dict
```

## Processor Order

Processors run in the order they're defined:

```python
processors = [
    add_hostname_processor,      # Runs first
    sanitize_secrets,             # Runs second
    production_only_processor,    # Runs third
]
```

## Next Steps

- **[Structured Events](structured-events.md)** - Learn event patterns
- **[API Reference: Processors](../../reference/provide/foundation/logger/processors/index.md)** - Complete processor API

---

**See also:** [examples/telemetry/](https://github.com/provide-io/provide-foundation/tree/main/examples/telemetry)
