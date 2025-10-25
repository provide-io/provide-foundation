# API Reference

Complete API documentation for `provide.foundation` — auto-generated from source code docstrings and type hints.

## 🚀 Quick Access

Most commonly used functions and classes:

### Essential Functions

```python
from provide.foundation import logger, pout, perr, get_hub
from provide.foundation.hub import register_command
from provide.foundation.resilience import retry
```

| Import | Purpose | Documentation |
|--------|---------|---------------|
| `logger` | Global logger instance for structured logging | [logger docs](provide/foundation/logger/index.md) |
| `pout()` | User-facing output to stdout (with colors) | [console docs](provide/foundation/console/index.md) |
| `perr()` | User-facing errors to stderr (with colors) | [console docs](provide/foundation/console/index.md) |
| `get_hub()` | Access the central component registry | [hub docs](provide/foundation/hub/index.md) |
| `@register_command` | Register CLI commands | [CLI docs](provide/foundation/cli/index.md) |
| `@retry` | Retry decorator with exponential backoff | [resilience docs](provide/foundation/resilience/index.md) |

### Configuration Classes

```python
from provide.foundation.config import BaseConfig, env_field
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
```

| Class | Purpose | Documentation |
|-------|---------|---------------|
| `BaseConfig` | Base class for configuration objects | [config docs](provide/foundation/config/index.md) |
| `TelemetryConfig` | Configure logging and telemetry | [logger config docs](provide/foundation/logger/config/index.md) |
| `LoggingConfig` | Detailed logging configuration | [logger config docs](provide/foundation/logger/config/index.md) |

### Utilities

```python
from provide.foundation.utils.environment import get_bool, get_int, get_str
from provide.foundation.file import atomic_write
from provide.foundation.serialization import provide_dumps, provide_loads
from provide.foundation.eventsets.display import show_event_matrix
from provide.foundation import shutdown_foundation
```

| Function | Purpose | Documentation |
|----------|---------|---------------|
| `get_bool()`, `get_int()`, `get_str()` | Environment variable helpers | [environment docs](provide/foundation/utils/environment/index.md) |
| `atomic_write()` | Safe atomic file writes | [file docs](provide/foundation/file/index.md) |
| `provide_dumps()`, `provide_loads()` | JSON serialization | [serialization docs](provide/foundation/serialization/index.md) |
| `show_event_matrix()` | Display event set emoji matrix | [eventsets docs](provide/foundation/eventsets/index.md) |
| `shutdown_foundation()` | Graceful shutdown and cleanup | [setup docs](provide/foundation/setup/index.md) |

### Advanced Features

```python
from provide.foundation.hub import injectable
from provide.foundation.hub.container import Container, create_container
from provide.foundation.eventsets.types import EventSet, EventMapping
```

| Feature | Purpose | Documentation |
|---------|---------|---------------|
| `@injectable` | Mark classes for dependency injection | [hub docs](provide/foundation/hub/index.md) |
| `Container` | Dependency injection container | [container docs](provide/foundation/hub/container/index.md) |
| `EventSet` | Define custom event sets with emojis | [eventsets docs](provide/foundation/eventsets/index.md) |
| `EventMapping` | Map events to emoji representations | [eventsets docs](provide/foundation/eventsets/index.md) |

---

## Quick Navigation

### Core Components

- **[logger](provide/foundation/logger/index.md)** - Structured logging system with emoji-enhanced output
- **[hub](provide/foundation/hub/index.md)** - Central component registry and dependency injection
- **[config](provide/foundation/config/index.md)** - Configuration management with environment variable support
- **[errors](provide/foundation/errors/index.md)** - Error handling and custom exception types

### CLI & Console

- **[cli](provide/foundation/cli/index.md)** - Command-line interface framework
- **[console](provide/foundation/console/index.md)** - Console I/O with colors and formatting

### Resilience & Observability

- **[resilience](provide/foundation/resilience/index.md)** - Retry patterns, circuit breakers, and failure handling
- **[metrics](provide/foundation/metrics/index.md)** - Metrics collection and OpenTelemetry integration
- **[tracer](provide/foundation/tracer/index.md)** - Distributed tracing support

### Data & Files

- **[file](provide/foundation/file/index.md)** - Atomic file operations and change detection
- **[archive](provide/foundation/archive/index.md)** - Archive creation and extraction (tar, zip, gzip)
- **[serialization](provide/foundation/serialization/index.md)** - JSON serialization with type safety

### Security & Crypto

- **[crypto](provide/foundation/crypto/index.md)** - Cryptographic operations (keys, signatures, certificates)
- **[security](provide/foundation/security/index.md)** - Security utilities and path validation

### Utilities

- **[utils](provide/foundation/utils/index.md)** - General utilities (async, caching, formatting, timing)
- **[process](provide/foundation/process/index.md)** - Safe subprocess execution
- **[platform](provide/foundation/platform/index.md)** - Platform detection and system information
- **[transport](provide/foundation/transport/index.md)** - HTTP client utilities
- **[parsers](provide/foundation/parsers/index.md)** - Data parsing utilities

## Browse All Modules

For a complete hierarchical view of all modules, classes, and functions:

**[📑 Full Module Index](SUMMARY/)** - Complete navigation tree

## Module Count

This reference documents **36 foundation modules** with **352 API pages**.

---

**Tip:** Use your browser's search (Ctrl+F / Cmd+F) within individual module pages to quickly find specific functions or classes.
