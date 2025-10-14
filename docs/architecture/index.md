# provide.foundation Specification

This section documents the technical specifications, protocols, and enhancement proposals for provide.foundation.

## Design Philosophy & Trade-offs

Understanding provide.foundation's architectural decisions helps teams evaluate fit:

### [Design Decisions](design-decisions.md)
**Intentional design choices** behind provide.foundation's architecture:
- Threading model and async considerations
- Tool stack philosophy (attrs, structlog, click)
- Global state patterns and singletons
- Intentional scope boundaries

### [Limitations & Trade-offs](limitations.md)
**Honest assessment** of current limitations and mitigations:
- Async context considerations
- CLI adapter ecosystem
- Configuration source extensibility
- Performance characteristics

### [When to Use](../guide/when-to-use.md)
**Decision guide** for evaluating provide.foundation:
- ✅ Excellent fit: CLI apps, microservices, data pipelines
- ✅ Good fit: Web APIs, task processors, libraries
- ⚠️ Consider alternatives: Ultra-low latency, full-stack needs

---

## Core Specifications

### [Telemetry Format](telemetry-format.md)
Detailed specification of the structured logging format, including:
- Message structure
- Field conventions
- Timestamp formats
- Context propagation

### [Event Enrichment System](event-enrichment.md)
The visual parsing and metadata enhancement system:
- Domain-to-emoji mappings
- Event metadata enrichment
- Custom enrichment configuration
- Event set interface specification

### [Performance](performance.md)
Performance specifications and benchmarks:
- Throughput requirements (>14,000 msg/sec)
- Latency targets
- Memory usage guidelines
- Optimization strategies

## Implementation Status

### Stable Features
- ✅ **Structured Logging**: Full implementation with emoji support
- ✅ **Configuration System**: Environment variables, file loading, validation
- ✅ **CLI Framework**: Command registration, nested commands, JSON output
- ✅ **File Operations**: Atomic writes, format support, locking
- ✅ **Cryptographic Utils**: Hashing, checksums, signatures, certificates
- ✅ **Distributed Tracing**: Lightweight span-based tracing
- ✅ **Error Handling**: Rich context, decorators, boundaries
- ✅ **OpenTelemetry Bridge**: Full OTEL compatibility layer

### Experimental Features
- None currently

### Deprecated Features
- None currently

## Technical Standards

### Message Format

All log messages follow this structure:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456Z",
  "level": "INFO",
  "logger": "provide.foundation",
  "message": "operation_completed",
  "context": {
    "request_id": "abc-123",
    "user_id": "user-456"
  },
  "metadata": {
    "duration_ms": 142,
    "status": "success"
  }
}
```

### Event Set Interface

```python
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from attrs import define, field

from provide.foundation.config.defaults import DEFAULT_EVENT_KEY

@define(frozen=True, slots=True)
class EventMapping:
    name: str
    visual_markers: dict[str, str] = field(factory=dict)
    metadata_fields: dict[str, dict[str, Any]] = field(factory=dict)
    transformations: dict[str, Callable[[Any], Any]] = field(factory=dict)
    default_key: str = field(default=DEFAULT_EVENT_KEY)


@define(frozen=True, slots=True)
class FieldMapping:
    log_key: str
    description: str | None = field(default=None)
    value_type: str | None = field(default=None)
    event_set_name: str | None = field(default=None)
    default_override_key: str | None = field(default=None)
    default_value: Any | None = field(default=None)


@define(frozen=True, slots=True)
class EventSet:
    name: str
    description: str | None = field(default=None)
    mappings: list[EventMapping] = field(factory=list)
    field_mappings: list[FieldMapping] = field(factory=list)
    priority: int = field(default=0, converter=int)
```

### Performance Requirements

| Metric | Requirement | Current |
|--------|------------|---------|
| Throughput | >10,000 msg/sec | 14,000 msg/sec |
| Latency (p50) | <100μs | 71μs |
| Latency (p99) | <1ms | 890μs |
| Memory per logger | <1MB | 640KB |
| Thread safety | Required | ✅ |
| Async support | Required | ✅ |

## Compatibility Matrix

| provide.foundation | Python | structlog | attrs |
|-------------------|---------|-----------|--------|
| 1.0.x | ≥3.11 | ≥23.0 | ≥23.0 |
| 0.9.x | ≥3.10 | ≥22.0 | ≥22.0 |
| 0.8.x | ≥3.9 | ≥21.0 | ≥21.0 |

## API Stability

### Stable APIs
- `provide.foundation.logger`
- `provide.foundation.cli`
- `provide.foundation.config`
- `provide.foundation.platform`
- `provide.foundation.tracer` - Distributed tracing functionality

### Deprecated APIs
- None currently

## Contributing to Specifications

To propose changes to specifications:

1. Open an issue for discussion
2. Draft an FEP following the template
3. Submit a pull request
4. Participate in review process

See [Contributing Guide](../development/contributing.md) for details.