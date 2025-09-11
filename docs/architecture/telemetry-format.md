# Telemetry Format Specification

The structured logging format specification for Foundation Telemetry messages.

## Overview

Foundation implements a consistent structured logging format that ensures compatibility across different output modes, processors, and integrations. This specification defines the canonical message structure, field conventions, and serialization requirements.

## Message Structure

### Core Message Format

Every Foundation log message follows this canonical structure:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456Z",
  "level": "INFO", 
  "logger": "provide.foundation.app",
  "event": "operation_completed",
  "service_name": "payment-api",
  "context": {
    "request_id": "req-abc123",
    "user_id": "usr-456",
    "trace_id": "trace-xyz789"
  },
  "metadata": {
    "duration_ms": 142.5,
    "status_code": 200,
    "records_processed": 1000
  }
}
```

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `timestamp` | `string` | ISO 8601 UTC timestamp with microseconds | `"2024-01-15T10:30:45.123456Z"` |
| `level` | `string` | Log level name in uppercase | `"INFO"`, `"ERROR"`, `"DEBUG"` |
| `logger` | `string` | Logger name/hierarchy | `"provide.foundation.app"` |
| `event` | `string` | Structured event name | `"user_login_completed"` |

### Optional Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `service_name` | `string` | Service identifier | `null` |
| `context` | `object` | Correlation and request context | `{}` |
| `metadata` | `object` | Event-specific data | `{}` |
| `error` | `object` | Error information (when applicable) | `null` |
| `emoji` | `string` | Visual emoji prefix | `null` |

## Field Specifications

### Timestamp Format

**Standard**: ISO 8601 with microsecond precision in UTC timezone

```
YYYY-MM-DDTHH:MM:SS.ssssssZ
```

**Examples**:
```json
{
  "timestamp": "2024-01-15T10:30:45.123456Z",  // Full precision
  "timestamp": "2024-01-15T10:30:45.000000Z",  // No sub-second data
  "timestamp": "2024-01-15T10:30:45.100000Z"   // Millisecond precision
}
```

**Generation**: Timestamps are generated at log emission time using `time.time()` converted to UTC.

### Log Levels

**Standard Levels** (aligned with Python logging):

| Level | Numeric | Usage |
|-------|---------|--------|
| `CRITICAL` | 50 | System failures requiring immediate attention |
| `ERROR` | 40 | Error conditions that prevent normal operation |
| `WARNING` | 30 | Warning conditions that should be noted |
| `INFO` | 20 | Informational messages for normal operations |
| `DEBUG` | 10 | Detailed diagnostic information |
| `TRACE` | 5 | Ultra-verbose debugging information |

**Format**: Always uppercase string values in JSON output.

### Logger Names

**Hierarchy**: Dot-separated hierarchical names following Python module conventions.

```json
{
  "logger": "provide.foundation",           // Root logger
  "logger": "provide.foundation.app",       // Application logger  
  "logger": "provide.foundation.db",        // Database operations
  "logger": "provide.foundation.auth.jwt"   // JWT authentication
}
```

**Naming Conventions**:
- Use dot-separated hierarchy
- Lowercase with underscores for multi-word components
- Match module/component structure when possible

### Event Names

**Pattern**: Domain-Action-Status format for semantic clarity.

```json
{
  "event": "user_authentication_completed",    // Success case
  "event": "database_connection_established",  // System event
  "event": "payment_processing_failed",        // Error case
  "event": "cache_invalidation_started"        // Process start
}
```

**Naming Rules**:
- Use lowercase with underscores
- Follow `domain_action_status` pattern when applicable
- Be descriptive but concise
- Use consistent vocabulary across similar events

### Context Object

**Purpose**: Correlation identifiers and request-scoped data.

```json
{
  "context": {
    "request_id": "req-abc123",       // Request correlation
    "user_id": "usr-456",             // User context
    "session_id": "sess-789",         // Session context
    "trace_id": "trace-xyz789",       // Distributed tracing
    "span_id": "span-def456",         // Tracing span
    "tenant_id": "tenant-org1"        // Multi-tenancy
  }
}
```

**Common Context Fields**:
- `request_id` - Unique request identifier
- `user_id` - User identifier 
- `session_id` - Session identifier
- `trace_id` - Distributed trace ID
- `span_id` - Trace span ID
- `tenant_id` - Multi-tenant identifier
- `correlation_id` - Custom correlation ID

### Metadata Object

**Purpose**: Event-specific data and measurements.

```json
{
  "metadata": {
    "duration_ms": 142.5,            // Timing data
    "status_code": 200,              // Response status
    "records_processed": 1000,       // Counts
    "file_size_bytes": 2048576,      // Measurements
    "retry_count": 2,                // State information
    "endpoint": "/api/users",        // Request details
    "method": "GET"                  // HTTP method
  }
}
```

**Data Types**:
- Numbers: Use appropriate precision (int vs float)
- Strings: UTF-8 encoded
- Booleans: Use `true`/`false`
- Arrays: Homogeneous types preferred
- Objects: Nested structures allowed but keep shallow

### Error Object

**Format**: Structured error information for exceptions.

```json
{
  "error": {
    "type": "ValueError",            // Exception class name
    "message": "Invalid input provided",  // Exception message
    "code": "E1001",                // Application error code
    "stack_trace": "Traceback...",  // Full traceback (optional)
    "context": {                    // Error context
      "input_value": "invalid",
      "expected_format": "email"
    }
  }
}
```

**Error Context**: Additional context specific to the error condition.

## Output Formats

### JSON Format (Production)

**Usage**: Production logging, structured analysis, log aggregation.

```json
{"timestamp": "2024-01-15T10:30:45.123456Z", "level": "INFO", "logger": "app", "event": "user_login", "service_name": "auth-api", "context": {"request_id": "req-123", "user_id": "usr-456"}, "metadata": {"method": "oauth", "duration_ms": 245}}
```

**Characteristics**:
- Single-line JSON objects
- All fields present (nulls for empty optional fields)
- UTF-8 encoding
- No pretty-printing for performance

### Key-Value Format (Development)

**Usage**: Development, debugging, human-readable output.

```
2024-01-15 10:30:45.123 [INFO] 🔐 user_login request_id=req-123 user_id=usr-456 method=oauth duration_ms=245
```

**Characteristics**:
- Human-readable timestamps
- Emoji prefixes for visual parsing
- Key=value pairs for structured data
- Color coding (when terminal supports it)

### Compact Format (CI/CD)

**Usage**: Continuous integration, automated processing.

```
[INFO] user_login request_id=req-123 method=oauth duration_ms=245
```

**Characteristics**:
- Minimal formatting overhead
- Essential information only
- No emojis or colors
- Fixed-width log levels

### Plain Format (Debugging)

**Usage**: Raw debugging, minimal overhead.

```
user_login request_id=req-123 user_id=usr-456 method=oauth duration_ms=245
```

**Characteristics**:
- No timestamps or levels
- Raw key-value output
- Minimal processing overhead
- Suitable for debugging tools

## Serialization Rules

### JSON Serialization

1. **UTF-8 Encoding**: All strings must be valid UTF-8
2. **Number Precision**: Preserve original precision, avoid unnecessary decimals
3. **Null Handling**: Include optional fields as `null` when not present
4. **Array Ordering**: Maintain insertion order for arrays
5. **Object Ordering**: Use consistent field ordering

### Special Value Handling

```json
{
  "metadata": {
    "count": 0,                    // Zero values included
    "rate": null,                  // Explicit null for missing values
    "active": true,                // Boolean values
    "tags": [],                    // Empty arrays included
    "nested": {},                  // Empty objects included
    "decimal": 3.14159265359,      // Full precision preserved
    "large_number": 9007199254740991  // JavaScript-safe integers
  }
}
```

### Character Escaping

Standard JSON escape sequences:
- `\"` - Quotation mark
- `\\` - Backslash  
- `\/` - Forward slash (optional)
- `\b` - Backspace
- `\f` - Form feed
- `\n` - Newline
- `\r` - Carriage return
- `\t` - Tab
- `\uXXXX` - Unicode escape

## Context Propagation

### Thread Safety

Context data is stored using `contextvars` for thread-safe and async-safe propagation:

```python
from contextvars import ContextVar

request_context: ContextVar[dict] = ContextVar('request_context', default={})
```

### Automatic Propagation

Context is automatically included in all log messages within the same execution context:

```python
# Set context once
logger.bind(request_id="req-123", user_id="usr-456")

# All subsequent logs include context
logger.info("processing_started")  # Includes request_id and user_id
logger.info("processing_completed")  # Includes request_id and user_id
```

### Cross-Service Propagation

For distributed systems, context can be serialized for HTTP headers:

```json
{
  "X-Request-ID": "req-123",
  "X-User-ID": "usr-456", 
  "X-Trace-ID": "trace-xyz789"
}
```

## Validation Rules

### Message Validation

1. **Required Fields**: `timestamp`, `level`, `logger`, `event` must be present
2. **Field Types**: All fields must match specified types
3. **Timestamp Format**: Must be valid ISO 8601 UTC timestamp
4. **Log Level**: Must be one of the standard levels
5. **Event Name**: Must be non-empty string, recommend underscore format

### Size Limitations

- **Maximum Message Size**: 64KB (configurable)
- **Maximum Field Count**: 1000 fields per message
- **Maximum Nesting Depth**: 10 levels for nested objects
- **Maximum Array Length**: 10,000 elements

### Content Restrictions

- **No Sensitive Data**: Passwords, tokens, API keys prohibited
- **UTF-8 Only**: All strings must be valid UTF-8
- **Finite Numbers**: No `Infinity` or `NaN` values
- **Safe Characters**: Control characters escaped

## Compatibility

### Structlog Compatibility

Foundation messages are compatible with structlog processors:

```python
import structlog

# Foundation message can be processed by structlog
structlog.get_logger().info("test", foundation_context={"key": "value"})
```

### Standard Library Compatibility

Foundation extends Python's standard logging:

```python
import logging

# Foundation loggers are Python loggers
foundation_logger = get_logger("app")
assert isinstance(foundation_logger, logging.Logger)
```

### JSON Schema

Complete JSON Schema available for validation:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["timestamp", "level", "logger", "event"],
  "properties": {
    "timestamp": {"type": "string", "format": "date-time"},
    "level": {"type": "string", "enum": ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]},
    "logger": {"type": "string", "minLength": 1},
    "event": {"type": "string", "minLength": 1}
  }
}
```

## Implementation Notes

### Performance Considerations

- Field ordering optimized for common access patterns
- Lazy serialization until output format determined  
- Context propagation uses copy-on-write semantics
- String formatting deferred until emission

### Backwards Compatibility

- New optional fields may be added in minor versions
- Required field structure is stable across major versions
- Output format selection maintains compatibility
- Processors can filter or transform messages as needed

## See Also

- [Event Enrichment](../guide/concepts/event-enrichment.md) - Visual parsing and metadata enhancement
- [Performance Architecture](performance.md) - Throughput and latency specifications
