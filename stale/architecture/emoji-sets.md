# Emoji Set Architecture

Technical implementation details of provide.foundation's emoji mapping system.

## System Overview

```mermaid
graph TB
    A[Application Code] --> B[Emoji Set API]
    B --> C[Field Definitions]
    B --> D[Emoji Sets]
    B --> E[Validation Rules]
    C --> F[Logger Processor Chain]
    D --> F
    E --> F
    F --> G[Structured Output]
    G --> H[Console/File/Network]
```

## Core Components

### 1. EmojiSetConfig Class

The base class that defines an emoji set configuration:

```python
@attrs.define(frozen=True, kw_only=True)
class EmojiSetConfig:
    """Defines an emoji set configuration."""
    
    name: str                                    # e.g., "http", "llm", "database"
    description: str                             # Human-readable description
    emoji_sets: list[CustomDasEmojiSet]        # Domain-specific emoji mappings
    field_definitions: list[FieldToEmojiMapping]  # Field specifications
    priority: int = 50                          # Processing priority (higher = first)
```

### 2. Field Definitions

Each field mapping in an emoji set is precisely defined:

```python
@attrs.define(frozen=True, kw_only=True)
class FieldToEmojiMapping:
    """Defines a field-to-emoji mapping with metadata."""
    
    log_key: str                    # e.g., "http.method", "llm.provider"
    description: str = ""            # Field documentation
    value_type: str = "string"       # Expected type: string|integer|float|boolean
    emoji_set_name: str | None = None  # Links to emoji set for mapping
    default_emoji_override_key: str | None = None  # Fallback emoji key
    required: bool = False           # Whether field is mandatory
    validation_regex: str | None = None  # Optional validation pattern
```

### 3. Emoji Mapping System

Dynamic emoji assignment based on field values:

```python
@attrs.define(frozen=True, kw_only=True)
class CustomDasEmojiSet:
    """Emoji set for domain-action-status mapping."""
    
    name: str                        # Unique identifier
    emojis: dict[str, str]          # Value -> Emoji mapping
    default_emoji_key: str = "default"  # Fallback key
    
    def get_emoji(self, key: str) -> str:
        """Get emoji with fallback to default."""
        return self.emojis.get(key, self.emojis.get(self.default_emoji_key, ""))
```

## Built-in Emoji Set Specifications

### HTTP Emoji Set Architecture

```python
HTTP_EMOJI_SET = EmojiSetConfig(
    name="http",
    priority=80,  # High priority for web apps
    emoji_sets=[
        # Method-specific emojis
        CustomDasEmojiSet(
            name="http_method",
            emojis={
                "get": "📥",     # Receiving data
                "post": "📤",    # Sending data
                "put": "📝⬆️",   # Updating
                "delete": "🗑️",  # Removing
                "patch": "🩹",   # Partial update
            }
        ),
        # Status class emojis
        CustomDasEmojiSet(
            name="http_status_class",
            emojis={
                "2xx": "✅",     # Success
                "3xx": "↪️",     # Redirect
                "4xx": "⚠️",     # Client error
                "5xx": "🔥",     # Server error
            }
        )
    ]
)
```

### LLM Emoji Set Architecture

```python
LLM_EMOJI_SET = EmojiSetConfig(
    name="llm",
    priority=100,  # Highest priority for AI-focused apps
    emoji_sets=[
        # Provider-specific branding
        CustomDasEmojiSet(
            name="llm_provider",
            emojis={
                "openai": "🤖",
                "anthropic": "📚",
                "google": "🇬",
                "meta": "🦙",
            }
        ),
        # Task visualization
        CustomDasEmojiSet(
            name="llm_task",
            emojis={
                "generation": "✍️",
                "embedding": "🔗",
                "chat": "💬",
                "tool_use": "🛠️",
            }
        )
    ]
)
```

## Processing Pipeline

### 1. Emoji Set Registration

Layers are registered at initialization:

```python
BUILTIN_EMOJI_SETS: dict[str, EmojiSetConfig] = {
    "llm": LLM_EMOJI_SET,
    "database": DATABASE_EMOJI_SET,
    "http": HTTP_EMOJI_SET,
    "task_queue": TASK_QUEUE_EMOJI_SET,
}

# Sorted by priority for processing order
ACTIVE_LAYERS = sorted(
    BUILTIN_EMOJI_SETS.values(),
    key=lambda x: x.priority,
    reverse=True
)
```

### 2. Field Processing

When a log event occurs:

1. **Field Extraction**: Extract Contextual fields from event dict
2. **Emoji Set Matching**: Find appropriate layer based on field keys
3. **Emoji Resolution**: Map field values to emojis
4. **Validation**: Ensure field types and constraints
5. **Enrichment**: Add layer metadata

```python
def process_contextual_fields(event_dict: dict[str, Any]) -> dict[str, Any]:
    """Process event through emoji sets."""
    
    # Find matching emoji set
    layer = find_matching_layer(event_dict)
    if not layer:
        return event_dict
    
    # Apply field definitions
    for field_def in layer.field_definitions:
        if field_def.log_key in event_dict:
            # Validate type
            validate_field_type(event_dict[field_def.log_key], field_def.value_type)
            
            # Apply emoji if configured
            if field_def.emoji_set_name:
                emoji = resolve_emoji(
                    event_dict[field_def.log_key],
                    layer.get_emoji_set(field_def.emoji_set_name)
                )
                event_dict["_emoji"] = emoji
    
    return event_dict
```

### 3. Emoji Prefix Addition

The final processor adds emojis to the message:

```python
def add_emoji_prefix(event_dict: dict[str, Any]) -> str:
    """Add emoji prefix to log message."""
    
    emoji = event_dict.pop("_emoji", "")
    message = event_dict.get("event", "")
    
    if emoji:
        return f"{emoji} {message}"
    return message
```

## Performance Optimizations

### 1. Lazy Emoji Set Loading

Layers are only loaded when first used:

```python
class LazyLayerRegistry:
    def __init__(self):
        self._layers: dict[str, EmojiSetConfig] | None = None
    
    @property
    def layers(self) -> dict[str, EmojiSetConfig]:
        if self._layers is None:
            self._layers = self._load_layers()
        return self._layers
```

### 2. Emoji Caching

Emoji lookups are cached for performance:

```python
@lru_cache(maxsize=1024)
def get_emoji_for_value(
    value: str,
    emoji_set_name: str,
    emoji_set_name: str
) -> str:
    """Cached emoji lookup."""
    layer = BUILTIN_EMOJI_SETS[layer_name]
    emoji_set = layer.get_emoji_set(emoji_set_name)
    return emoji_set.get_emoji(value)
```

### 3. Field Key Indexing

Fields are indexed by prefix for fast matching:

```python
FIELD_PREFIX_INDEX = {
    "http.": HTTP_EMOJI_SET,
    "db.": DATABASE_EMOJI_SET,
    "llm.": LLM_EMOJI_SET,
    "task.": TASK_QUEUE_EMOJI_SET,
}

def find_emoji_set_for_event(event_dict: dict[str, Any]) -> EmojiSetConfig | None:
    """Fast layer lookup using prefix index."""
    for key in event_dict:
        for prefix, layer in FIELD_PREFIX_INDEX.items():
            if key.startswith(prefix):
                return layer
    return None
```

## Extensibility

### Custom Emoji Set Registration

Applications can register custom layers:

```python
from provide.foundation.emoji_sets import register_emoji_set

@register_emoji_set
class PaymentLayer(EmojiSetConfig):
    name = "payment"
    priority = 75
    # ... configuration ...

# Or programmatically
register_emoji_set(PAYMENT_LAYER)
```

### Layer Composition

Layers can be composed for complex scenarios:

```python
# Combine HTTP + LLM for AI API calls
class AIAPILayer(CompositeEmojiSetConfig):
    layers = [HTTP_EMOJI_SET, LLM_EMOJI_SET]
    
    def process(self, event_dict):
        # Apply both HTTP and LLM mappings
        event_dict = HTTP_EMOJI_SET.process(event_dict)
        event_dict = LLM_EMOJI_SET.process(event_dict)
        return event_dict
```

## Configuration & Control

### Runtime Configuration

```python
# Global configuration
TelemetryConfig(
    enable_emoji_sets=True,
    enabled_layers=["http", "llm"],  # Selective enabling
    emoji_set_timeout_ms=10,    # Processing timeout
)

# Per-logger configuration
logger = get_logger(
    emoji_sets_enabled=False  # Disable for performance-critical paths
)
```

### Performance Monitoring

```python
# Track layer processing time
LAYER_METRICS = {
    "http": {"count": 0, "total_ms": 0},
    "llm": {"count": 0, "total_ms": 0},
}

def track_layer_performance(emoji_set_name: str, duration_ms: float):
    LAYER_METRICS[layer_name]["count"] += 1
    LAYER_METRICS[layer_name]["total_ms"] += duration_ms
```

## Thread Safety

All emoji set operations are thread-safe:

```python
# Immutable configuration
@attrs.define(frozen=True)  # Frozen = immutable
class EmojiSetConfig:
    ...

# Thread-local storage for context
THREAD_LOCAL = threading.local()

def with_contextual_context(**kwargs):
    """Thread-safe context manager."""
    THREAD_LOCAL.contextual_context = kwargs
    try:
        yield
    finally:
        THREAD_LOCAL.contextual_context = None
```

## Integration Points

### With Structlog Processors

Emoji sets integrate seamlessly with structlog's processor chain:

```python
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        emoji_set_processor,  # Our emoji set
        add_emoji_prefix,          # Emoji addition
        structlog.processors.JSONRenderer(),
    ]
)
```

### With OpenTelemetry

Emoji sets are designed to **extend and enhance OpenTelemetry**, not replace it:

```python
from opentelemetry import trace, metrics
from provide.foundation.otel import ContextualOTELProcessor

# Emoji sets automatically enrich OTEL spans
tracer = trace.get_tracer(__name__)

class ContextualOTELProcessor:
    """Bridges emoji sets with OpenTelemetry."""
    
    def process_span(self, span: Span, event_dict: dict[str, Any]):
        """Enrich OTEL span with emoji set data."""
        
        # Direct OTEL attribute mapping (already compatible!)
        for key, value in event_dict.items():
            if key.startswith(("http.", "db.", "rpc.", "messaging.")):
                span.set_attribute(key, value)
        
        # Add provide.io-specific attributes
        if "_emoji_set" in event_dict:
            span.set_attribute("provide.emoji_set", event_dict["_emoji_set"])
        
        # Visual parsing in span events (not attributes)
        if "_emoji" in event_dict:
            span.add_event(f"{event_dict['_emoji']} {event_dict.get('event', '')}")
        
        return span

# Automatic OTEL integration
@with_otel_span("http.request")
def handle_request(request):
    # Emoji sets enhance the OTEL span
    logger.info("http_request_started",
        **{
            "http.method": request.method,        # OTEL standard
            "http.url": request.url,              # OTEL standard
            "http.route": request.route,          # OTEL standard
            "provide.request_id": request.id,     # provide.io addition
        }
    )
    # Creates OTEL span with all attributes + visual logging
```

### Distributed Tracing Integration

```python
from provide.foundation.otel import setup_tracing

# Configure OTEL with emoji set enhancement
setup_tracing(
    endpoint="otel-collector:4317",
    service_name="my-service",
    emoji_sets_enabled=True,  # Enable emoji enrichment
    visual_span_events=True,        # Add emoji events to spans
)

# Automatic trace context propagation
with tracer.start_as_current_span("process_order") as span:
    logger.info("order_processing",
        order_id="123",
        # Emoji set adds emoji + validates fields
        # OTEL span gets all attributes
    )
```

## Design Decisions

### Why Extend OpenTelemetry?

1. **Standards compliance**: OTEL is the industry standard for observability
2. **Visual enhancement**: We add developer-friendly emoji on top of OTEL
3. **Ecosystem integration**: provide.io services need both OTEL and visual logging
4. **Progressive enhancement**: Start with our logging, seamlessly add OTEL when needed

### Architecture Benefits

1. **No lock-in**: Can export to any OTEL-compatible backend
2. **Best of both worlds**: Visual local development + standard production observability
3. **Gradual adoption**: Use emoji sets alone, or with full OTEL
4. **Forward compatible**: As OTEL evolves, we evolve with it

### Why Domain-Specific?

1. **Context awareness**: HTTP logs differ from database logs
2. **Field validation**: Each domain has specific requirements
3. **Visual distinction**: Different emoji sets per domain
4. **Future extensibility**: Easy to add new domains

### Why Emoji Mapping?

1. **Visual scanning**: 10x faster pattern recognition
2. **Error detection**: 🔥 stands out immediately
3. **Domain identification**: 🤖 = AI, 🌐 = Web, 🗄️ = Database
4. **Developer experience**: More engaging and memorable logs

## Next Steps

- 📖 [Advanced Logging Guide](../guide/logging/advanced.md) for customization
- 🔧 [API Reference](../api/emoji_sets/api-index.md) for complete documentation
- 📚 [Usage Examples](../getting-started/examples.md) for practical patterns
- 🎨 [Emoji System Details](emoji-system.md) for implementation details