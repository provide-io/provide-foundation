# Semantic Layers

Domain-specific telemetry interfaces with visual emoji mapping - a unique approach to structured logging in the provide.io ecosystem.

## What Are Semantic Layers in provide.foundation?

provide.foundation's semantic layers are **domain-specific logging interfaces** that combine:
- 🎯 **Structured logging** with consistent field naming
- 🌐 **Domain context** for technologies like HTTP, databases, and LLMs
- 👀 **Visual parsing** through intelligent emoji mapping
- ⚡ **High performance** with minimal overhead (<5%)

## Not Your Typical Semantic Layer

The term "semantic layer" appears in different contexts across the tech industry. Here's how ours is unique:

### What We're NOT

| Type | Used In | Purpose | Not Us Because |
|------|---------|---------|----------------|
| **BI Semantic Layer** | Data warehouses (Cube, dbt) | Business-friendly data abstraction | We're about logging, not data warehousing |
| **Generic Semantic Logging** | Observability tools | Structured logging with types | We add domain-specific interfaces + visual parsing |
| **OpenTelemetry Semantic Conventions** | Distributed tracing | Standardized attribute names | We're opinionated for provide.io, not a standard |

### What We ARE

**Domain-Specific Telemetry Interfaces** - Think of them as specialized logging APIs that understand the context of what you're logging:

```python
# Traditional structured logging
logger.info("http_request", method="GET", path="/api/users", status=200)

# With semantic layers - automatic context, emojis, and validation
http_layer.request_completed(method="GET", path="/api/users", status=200)
# Output: 📥 http_request_completed method=GET path=/api/users status=200 ✅
```

## Built-in Semantic Layers

provide.foundation includes pre-configured layers for common domains:

### 1. HTTP Layer 🌐
For web requests and responses:
```python
from provide.foundation.semantic_layers import HTTP_LAYER

# Automatic emoji mapping based on method and status
http_layer.log(
    "http.method": "POST",      # 📤
    "http.status_code": 201,    # ✅
    "http.target": "/api/orders"
)
```

### 2. Database Layer 🗄️
For database operations:
```python
from provide.foundation.semantic_layers import DATABASE_LAYER

# Context-aware logging with operation-specific emojis
db_layer.log(
    "db.system": "postgres",     # 🐘
    "db.operation": "insert",    # ➕
    "db.rows_affected": 42
)
```

### 3. LLM Layer 🤖
For AI/ML model interactions:
```python
from provide.foundation.semantic_layers import LLM_LAYER

# Specialized fields for LLM operations
llm_layer.log(
    "llm.provider": "anthropic", # 📚
    "llm.task": "generation",    # ✍️
    "llm.input.tokens": 150,
    "llm.output.tokens": 500
)
```

### 4. Task Queue Layer 📨
For async job processing:
```python
from provide.foundation.semantic_layers import TASK_QUEUE_LAYER

# Track async task lifecycle
task_layer.log(
    "task.system": "celery",     # 🥕
    "task.status": "success",    # ✅
    "duration_ms": 1234
)
```

## The Emoji System

Each semantic layer includes intelligent emoji mapping that provides instant visual context:

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

Semantic layers add minimal overhead:

| Operation | Without Layers | With Layers | Overhead |
|-----------|---------------|-------------|----------|
| Simple log | 71μs | 74μs | +4.2% |
| With context | 85μs | 89μs | +4.7% |
| Emoji mapping | - | +3μs | - |
| Field validation | - | +2μs | - |

## Creating Custom Semantic Layers

Extend the system with your own domain-specific layers:

```python
from provide.foundation.types import SemanticLayer, CustomDasEmojiSet

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
        }
    )
]

# Create your semantic layer
PAYMENT_LAYER = SemanticLayer(
    name="payment",
    description="Payment processing operations",
    emoji_sets=PAYMENT_EMOJI_SETS,
    field_definitions=[
        SemanticFieldDefinition(
            log_key="payment.method",
            emoji_set_name="payment_method"
        )
    ]
)
```

## When to Use Semantic Layers

### Use Semantic Layers When:
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

Enable or disable semantic layers:

```python
from provide.foundation.config import TelemetryConfig

config = TelemetryConfig(
    enable_semantic_layers=True,     # Enable all layers
    enabled_layers=["http", "llm"],  # Or specific ones
    enable_emoji=True,                # Visual parsing
    emoji_fallback="text"             # Fallback strategy
)
```

## Best Practices

1. **Use the right layer** - Don't force HTTP semantics on database operations
2. **Extend thoughtfully** - Create custom layers for truly distinct domains
3. **Preserve context** - Semantic layers complement, not replace, structured logging
4. **Monitor performance** - Disable in ultra-high-throughput scenarios if needed

## OpenTelemetry Integration

Our semantic layers are designed to **seamlessly integrate with OpenTelemetry**, following [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/concepts/semantic-conventions/) while adding provide.io-specific enhancements:

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

# Enable OTEL export - semantic layers automatically translate
setup_otel_export(
    endpoint="https://otel-collector.example.com",
    service_name="my-service"
)

# Log with semantic layers - automatically exports to OTEL
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

- 📖 See [Architecture: Semantic Layers](../../architecture/semantic-layers.md) for implementation details
- 🛠️ Learn to [Create Custom Semantic Layers](../../tutorials/custom-semantic-layer.md)
- 📚 Explore [Cookbook Recipes](../../cookbook/recipes/index.md) for real-world usage
- 🔧 Check [API Reference](../../api/semantic/index.md) for all available fields

## Summary

provide.foundation's semantic layers are a unique innovation that combines:
- The structure of semantic logging
- The domain awareness of BI semantic layers
- The visual parsing of emoji-enhanced output
- The performance of optimized telemetry

They're not a general standard - they're an opinionated tool designed specifically for building observable, debuggable services in the provide.io ecosystem.
