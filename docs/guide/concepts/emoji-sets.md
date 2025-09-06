# Emoji Sets

Domain-specific telemetry interfaces with visual emoji mapping - a unique approach to structured logging in the provide.io ecosystem.

## What Are Emoji Sets in provide.foundation?

provide.foundation's emoji sets are **domain-specific emoji mappings** that provide:
- 🎯 **Structured logging** with consistent field naming
- 🌐 **Domain context** for technologies like HTTP, databases, and LLMs
- 👀 **Visual parsing** through intelligent emoji mapping
- ⚡ **High performance** with minimal overhead (<5%)

## Understanding Emoji Sets

Emoji sets in provide.foundation are passive configuration objects that map field values to emojis:

### What We're NOT

| Type | Used In | Purpose | Not Us Because |
|------|---------|---------|----------------|
| **BI Semantic Layer** | Data warehouses (Cube, dbt) | Business-friendly data abstraction | We're about logging, not data warehousing |
| **Generic Semantic Logging** | Observability tools | Structured logging with types | We add domain-specific interfaces + visual parsing |
| **OpenTelemetry Semantic Conventions** | Distributed tracing | Standardized attribute names | We're opinionated for provide.io, not a standard |

### What We ARE

**Domain-Specific Emoji Mapping Configurations** - Think of them as passive data structures that define how field values map to emojis during log formatting:

```python
# How emoji sets actually work - just use regular logging with semantic field names
logger.info("http_request", 
    **{"http.method": "GET", "http.status_code": 200, "http.target": "/api/users"})
# The emoji processor automatically adds emojis based on field names
# Output: 📥 ✅ http_request status_code=200 target=/api/users
```

## Built-in Emoji Sets

provide.foundation includes pre-configured layers for common domains:

### 1. HTTP Layer 🌐
For web requests and responses:
```python
# Just log with the semantic field names - emojis are added automatically
logger.info("http_request",
    **{"http.method": "POST",      # → 📤 (added by processor)
       "http.status_code": 201,     # → ✅ (added by processor)
       "http.target": "/api/orders"}
)
```

### 2. Database Layer 🗄️
For database operations:
```python
# Log with semantic field names - emojis are mapped automatically
logger.info("db_operation",
    **{"db.system": "postgres",     # → 🐘 (added by processor)
       "db.operation": "insert",     # → ➕ (added by processor)
       "db.rows_affected": 42}
)
```

### 3. LLM Layer 🤖
For AI/ML model interactions:
```python
# Log with semantic field names for automatic emoji mapping
logger.info("llm_operation",
    **{"llm.provider": "anthropic", # → 📚 (added by processor)
       "llm.task": "generation",     # → ✍️ (added by processor)
       "llm.input.tokens": 150,
       "llm.output.tokens": 500}
)
```

### 4. Task Queue Layer 📨
For async job processing:
```python
# Log with semantic field names for automatic emoji mapping
logger.info("task_completed",
    **{"task.system": "celery",     # → 🥕 (added by processor)
       "task.status": "success",     # → ✅ (added by processor)
       "duration_ms": 1234}
)
```

## The Emoji System

Each emoji set includes intelligent emoji mapping that provides instant visual context:

### Domain → Action → Status Pattern

```python
# The emoji tells the story at a glance:
🤖 llm_generation_started      # AI starting generation
✍️ llm_generation_progress      # Generation in progress  
✅ llm_generation_completed     # Successfully completed
🔥 llm_generation_failed        # Failed with error
```

### Visual Parsing Benefits

1. **Faster log scanning** - Emojis are processed faster than text
2. **Pattern recognition** - Errors (🔥) stand out from success (✅)
3. **Domain clarity** - Instantly know if it's HTTP (🌐), DB (🗄️), or LLM (🤖)
4. **Reduced cognitive load** - Less mental parsing needed

## Performance Characteristics

Emoji sets add minimal overhead:

| Operation | Without Layers | With Layers | Overhead |
|-----------|---------------|-------------|----------|
| Simple log | 71μs | 74μs | +4.2% |
| With context | 85μs | 89μs | +4.7% |
| Emoji mapping | - | +3μs | - |
| Field validation | - | +2μs | - |

## Creating Custom Emoji Sets

Extend the system with your own domain-specific emoji mappings:

```python
from provide.foundation.types import EmojiSetConfig, CustomDasEmojiSet, FieldToEmojiMapping

# Define emoji mappings for your domain
PAYMENT_EMOJI_SETS = [
    CustomDasEmojiSet(
        name="payment_method",
        emojis={
            "card": "💳",
            "bank": "🏦",
            "crypto": "₿",
            "paypal": "🅿️",
            "default": "💰"
        },
        default_emoji_key="default"
    )
]

# Create your emoji set configuration
PAYMENT_LAYER = EmojiSetConfig(
    name="payment",
    description="Payment processing operations",
    emoji_sets=PAYMENT_EMOJI_SETS,
    field_definitions=[
        FieldToEmojiMapping(
            log_key="payment.method",
            emoji_set_name="payment_method"
        )
    ]
)

# Register and use it
from provide.foundation import logger

# Log with your custom semantic fields
logger.info("payment_processed",
    **{"payment.method": "card",  # → 💳 (automatically mapped)
       "payment.amount": 99.99}
)
```

## When to Use Emoji Sets

### Use Emoji Sets When:
- ✅ Logging domain-specific operations (HTTP, DB, LLM)
- ✅ You want consistent field naming across services
- ✅ Visual log parsing would help (development, debugging)
- ✅ Building provide.io ecosystem services

### Use Traditional Logging When:
- ❌ Logging generic application events
- ❌ Performance is absolutely critical (<70μs requirement)
- ❌ Integrating with non-provide.io systems
- ❌ Simple debug statements

## Configuration

Enable or disable emoji sets:

```python
from provide.foundation.config import TelemetryConfig

config = TelemetryConfig(
    enable_emoji_sets=True,          # Enable all emoji sets
    enabled_layers=["http", "llm"],  # Or specific ones
    enable_emoji=True,                # Visual parsing
    emoji_fallback="text"             # Fallback strategy
)
```

## Best Practices

1. **Use the right layer** - Don't force HTTP semantics on database operations
2. **Extend thoughtfully** - Create custom layers for truly distinct domains
3. **Preserve context** - Emoji sets complement, not replace, structured logging
4. **Monitor performance** - Disable in ultra-high-throughput scenarios if needed

## OpenTelemetry Integration

Our emoji sets are designed to **seamlessly integrate with OpenTelemetry**, following [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/concepts/semantic-conventions/) while adding provide.io-specific enhancements:

### OTEL-Compatible Field Naming
```python
# Our fields match OTEL conventions
"http.method"        # OTEL standard
"http.status_code"   # OTEL standard
"db.system"          # OTEL standard
"db.operation"       # OTEL standard

# Plus our visual layer
"http.method" → "GET" → 📥  # Added emoji mapping
```

### Seamless OTEL Export
```python
from provide.foundation import logger
from provide.foundation.otel import setup_otel_export

# Enable OTEL export - emoji sets automatically translate
setup_otel_export(
    endpoint="https://otel-collector.example.com",
    service_name="my-service"
)

# Log with emoji sets - automatically exports to OTEL
logger.info("http_request",
    **{"http.method": "GET", "http.status_code": 200}
)
# → Sends OTEL span with proper attributes
# → Also shows: 📥 http_request method=GET status=200 ✅
```

### Extension, Not Replacement
- ✅ **OTEL fields work as-is**: Use standard OTEL attribute names
- ✅ **Visual enhancement**: Adds emoji layer without breaking OTEL
- ✅ **Automatic translation**: Bridges any naming differences
- ✅ **Full tracing support**: Spans, metrics, and logs all work together

The key enhancement: We add visual parsing and domain validation **on top of** OTEL standards, making them more developer-friendly for the provide.io ecosystem.

## Next Steps

- 📖 See [Architecture: Semantic Layers](../../architecture/emoji-sets.md) for implementation details
- 🛠️ See [Advanced Logging Guide](../logging/advanced.md) for customization
- 📚 Explore [Examples](../../getting-started/examples.md) for real-world usage
- 🔧 Check [API Reference](../../api/emoji_sets/index.md) for all available fields

## Summary

provide.foundation's emoji sets are a unique feature that provides:
- The structure of semantic logging
- The domain awareness of BI emoji sets
- The visual parsing of emoji-enhanced output
- The performance of optimized telemetry

They're not a general standard - they're an opinionated tool designed specifically for building observable, debuggable services in the provide.io ecosystem.
