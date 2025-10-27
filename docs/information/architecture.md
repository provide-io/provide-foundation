# Architecture

provide.foundation is intentionally designed as a **foundation layer**, not a full-stack framework. This page explains the key architectural decisions and design philosophy.

## Design Philosophy

### Foundation Layer, Not Framework

provide.foundation provides core infrastructure components (logging, CLI, configuration) but deliberately does NOT include:

- Web frameworks (use FastAPI, Flask, Django)
- Database layers or ORMs
- Authentication systems
- Template engines
- Message queues

**Rationale:** By focusing on foundational concerns, the library remains lightweight, composable, and easy to integrate with your existing stack.

## Key Architectural Decisions

### 1. Tool Stack Philosophy

**Decision:** Built on proven, opinionated tools:
- `structlog` for structured logging
- `attrs` for data classes
- `click` for CLI parsing
- OpenTelemetry for observability (optional)

**Trade-off:**
- ✅ Cohesive, well-tested stack with consistent patterns
- ✅ Less decision fatigue for teams
- ❌ Less flexibility if you prefer alternatives (Pydantic, loguru, etc.)

**When this matters:** If your project is standardized on different tools (e.g., Pydantic-only shops), integration adds complexity.

### 2. Threading Model

**Decision:** Registry uses `threading.RLock` for thread-safety, not `asyncio.Lock`.

**Rationale:**
- Simpler implementation for initialization-time use cases
- Most registry access is read-heavy (command lookup)
- Negligible contention in typical CLI and service startup scenarios

**Impact:**
- **Negligible:** CLI applications, initialization-time registration
- **Low:** Read-heavy workloads, service startup
- **Consider alternatives:** High-throughput async services (>10k req/sec) with runtime registration in hot paths

**When this matters:** If you're building an async-heavy web service with dynamic component registration on every request, evaluate whether the threading lock impacts your specific workload.

### 3. Global State Pattern

**Decision:** Singletons for ergonomic APIs:
```python
from provide.foundation import logger, get_hub

logger.info("event")           # Global logger instance
hub = get_hub()                # Singleton hub instance
```

**Rationale:**
- Simpler API for common use cases
- Reduces boilerplate in application code
- Matches patterns from standard library (`logging.getLogger()`)

**Trade-off:**
- ✅ More ergonomic, less verbose code
- ❌ Can complicate testing without proper isolation

**Mitigation:** Use `provide-testkit`'s `reset_foundation_setup_for_testing()` for clean test state.

### 4. Lazy Initialization

**Decision:** Components initialize on first use, not at import time.

**Example:**
```python
from provide.foundation import logger

# No setup needed - logger initializes on first use
logger.info("app_started")
```

**Benefits:**
- Zero-configuration default behavior
- No import-time side effects
- Faster imports for code inspection tools
- Simpler for beginners

### 5. Structured Over Free-Form

**Decision:** Prefer structured data (key-value logging) over free-form strings.

**Example:**
```python
# Encouraged: Structured
logger.info("user_login", user_id="123", source="oauth")

# Discouraged: String formatting
logger.info(f"User 123 logged in via oauth")
```

**Benefits:**
- Logs are machine-parseable for analysis
- Easier filtering and aggregation in log systems
- Better performance (no string formatting)

## Component Architecture

### The Hub System

The Hub is the central registry for application components, commands, and resources.

**Key Concepts:**

1. **Multi-Dimensional Registry:** Components organized by dimension (service, resource, command, etc.)
2. **Lifecycle Management:** Support for context managers and initialization/cleanup
3. **Command Discovery:** Automatic CLI generation from registered commands
4. **Dependency Injection:** Pattern for accessing shared components

**Example:**
```python
from provide.foundation import get_hub
from provide.foundation.hub import register_command

@register_command("init")
def init_command(name: str):
    """Initialize a new project."""
    # Command implementation

hub = get_hub()
cli = hub.create_cli(name="my-tool")
cli()  # Runs the CLI with all registered commands
```

### Logging Architecture

Foundation's logging is built on `structlog` with custom processors and enrichment.

**Pipeline:**
```
Log Event → Event Enrichment → Sanitization → Formatting → Output
```

**Key Components:**

1. **Event Enrichment:** Adds emojis, context, and metadata based on event sets
2. **Sanitization:** Removes sensitive data (PII, credentials)
3. **OTLP Processor:** Optional OpenTelemetry integration for distributed tracing
4. **Formatters:** Key-value, JSON, or custom formatting

**Performance:** >14,000 messages/second with full enrichment pipeline.

### Configuration System

Two-tier configuration approach:

1. **Simple utilities** (`utils/environment.py`): One-off environment variable access
2. **Structured classes** (`config/env.py`): Type-safe configuration objects with validation

**Design Rationale:** Provides both quick utilities for scripts AND robust configuration for applications.

## Performance Characteristics

### Logging Performance

Benchmarked at >14,000 msg/sec with emoji processing enabled.

**Optimization Strategies:**
- Lazy evaluation of structured data
- Efficient processor pipeline
- Minimal string formatting in hot path
- Optional sampling for high-volume logs

### Memory Usage

- **Minimal state:** Hub and registry are lightweight
- **No message queuing:** Logs written directly (no in-memory buffer)
- **Lazy initialization:** Components created only when needed

### Startup Time

- **Fast imports:** No heavy initialization at import time
- **Lazy setup:** Logger and hub initialize on first use
- **Minimal dependencies:** Core package has few required dependencies

## Security Considerations

### Input Validation

- **Path traversal protection:** File operations validate paths
- **Symlink attack prevention:** Safe extraction from archives
- **SQL injection protection:** Parameterized queries in examples

### Sensitive Data

- **Automatic sanitization:** PII and credentials removed from logs
- **Secret file support:** Read secrets from files with `file://` prefix
- **No logging of secrets:** Configuration system avoids logging sensitive values

### Cryptographic Operations

- **Modern algorithms:** Ed25519, RSA with secure key sizes
- **Secure defaults:** Strong hash functions (SHA-256, BLAKE2b)
- **Certificate validation:** X.509 certificate chain validation

## Testing Philosophy

### Test Coverage Goals

- **>80% overall coverage** for production readiness
- **100% for critical modules:** Logging, configuration, CLI
- **Security tests:** Path traversal, symlink attacks, input sanitization

### Testing Utilities

`provide-testkit` provides essential testing utilities:

- `reset_foundation_setup_for_testing()`: Clean state between tests
- `set_log_stream_for_testing()`: Capture log output
- `FoundationTestCase`: Base class with automatic cleanup

**Pattern:**
```python
import pytest
from provide.testkit import reset_foundation_setup_for_testing

@pytest.fixture(autouse=True)
def reset_foundation():
    reset_foundation_setup_for_testing()
```

## Extensibility Points

### Custom Event Sets

Add domain-specific emoji mappings:

```python
from provide.foundation.eventsets import EventSet, EventMapping

my_events = EventSet(
    name="custom",
    mappings={
        "domain": "finance",
        "action": "transaction",
        "status": "completed",
    },
    emoji="💰",
)
```

### Custom Processors

Add custom log processors:

```python
def my_processor(logger, method_name, event_dict):
    event_dict["custom_field"] = "value"
    return event_dict

# Add to logging configuration
config = LoggingConfig(
    processors=[my_processor]
)
```

### Custom Commands

Register commands for the CLI:

```python
from provide.foundation.hub import register_command

@register_command("my-command", category="custom")
def my_command(arg: str):
    """My custom command."""
    # Implementation
```

## Future Considerations

### Async Registry (Under Consideration)

Potential future enhancement: `asyncio.Lock` option for high-concurrency async services.

**Status:** Not currently planned, but open to discussion based on real-world use cases.

### Plugin System (Planned)

Extensible plugin system for third-party integrations.

**Status:** Design phase, feedback welcome.

---

**See Also:**
- [Features](features.md) for complete component list
- [Use Cases](use-cases.md) for when to use Foundation
- [Dependency Injection](../explanation/dependency-injection.md) for Hub patterns
