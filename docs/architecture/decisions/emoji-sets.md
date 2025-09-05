# Design Decision: Semantic Layers

**Status**: Implemented  
**Created**: 2024-01-15  
**Authors**: provide.io Team

## Summary

This document explains why we built emoji sets and how they enhance the provide.io ecosystem's logging capabilities.

## Context

provide.foundation is an opinionated foundation library for the provide.io ecosystem. We needed domain-specific logging that provides the architecture and protocol for emoji sets in provide.foundation. Emoji sets provide domain-specific logging interfaces that enhance structured logging with contextual understanding and visual parsing through emojis.

## Motivation

Traditional logging lacks domain context. When logging HTTP requests, database queries, or LLM interactions, developers must manually structure their logs with appropriate context and visual indicators. Emoji sets solve this by providing:

1. **Domain-specific interfaces** that understand the context
2. **Automatic emoji mapping** for visual parsing
3. **Standardized field names** across applications
4. **Performance optimizations** for specific domains

## Specification

### Base Protocol

All emoji sets must implement this interface:

```python
from abc import ABC, abstractmethod
from typing import Any

class EmojiSetConfig(ABC):
    """Base emoji set protocol."""
    
    @property
    @abstractmethod
    def domain(self) -> str:
        """Return the domain identifier (e.g., 'http', 'database', 'llm')."""
        pass
    
    @abstractmethod
    def get_emoji(self, action: str, status: str) -> str:
        """Get emoji for domain-action-status combination."""
        pass
    
    @abstractmethod
    def format_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Format event with domain-specific fields."""
        pass
```

### Domain-Action-Status Pattern

Events follow the Domain-Action-Status (DAS) pattern:

```
{domain}_{action}_{status}
```

Examples:
- `http_request_started`
- `database_query_completed`
- `llm_generation_failed`

### Emoji Mapping

Each domain defines emoji mappings:

```python
EMOJI_MATRIX = {
    "http": {
        "request": {"started": "🌐", "completed": "✅", "failed": "❌"},
        "response": {"2xx": "✅", "4xx": "⚠️", "5xx": "🔥"}
    },
    "database": {
        "query": {"started": "🔍", "completed": "✅", "failed": "❌"},
        "transaction": {"started": "🔄", "committed": "✅", "rolled_back": "↩️"}
    }
}
```

### Standard Domains

#### HTTP Layer

```python
class HTTPLayer(EmojiSetConfig):
    domain = "http"
    
    def request_started(self, method: str, path: str, **kwargs):
        self.logger.info("http_request_started",
                        method=method,
                        path=path,
                        **kwargs)
    
    def request_completed(self, status: int, duration_ms: float, **kwargs):
        self.logger.info("http_request_completed",
                        status_code=status,
                        duration_ms=duration_ms,
                        **kwargs)
```

#### Database Layer

```python
class DatabaseLayer(EmojiSetConfig):
    domain = "database"
    
    def query_executed(self, query: str, duration_ms: float, **kwargs):
        self.logger.info("database_query_executed",
                        query=self._sanitize(query),
                        duration_ms=duration_ms,
                        **kwargs)
```

#### LLM Layer

```python
class LLMLayer(EmojiSetConfig):
    domain = "llm"
    
    def generation_started(self, model: str, prompt_tokens: int, **kwargs):
        self.logger.info("llm_generation_started",
                        model=model,
                        prompt_tokens=prompt_tokens,
                        **kwargs)
```

## Implementation

### Registry System

```python
from provide.foundation.registry import Registry

semantic_registry = Registry[EmojiSetConfig]()

# Register layers
semantic_registry.register("http", HTTPLayer)
semantic_registry.register("database", DatabaseLayer)
semantic_registry.register("llm", LLMLayer)
```

### Auto-discovery

Layers can be auto-discovered using entry points:

```toml
[project.entry_points."provide.foundation.semantic_layers"]
custom = "myapp.layers:CustomLayer"
```

### Performance Considerations

1. **Lazy Loading**: Layers are loaded on first use
2. **Caching**: Emoji mappings are cached after first lookup
3. **Batching**: Support for batched event processing
4. **Zero-cost Abstraction**: No overhead when not used

## Usage Examples

### Basic Usage

```python
from provide.foundation.emoji_sets import http_layer

# Automatic emoji and formatting
http_layer.request_started(method="GET", path="/api/users")
# Output: 🌐 http_request_started method=GET path=/api/users

http_layer.request_completed(status=200, duration_ms=42)
# Output: ✅ http_request_completed status_code=200 duration_ms=42
```

### Custom Layer

```python
from provide.foundation.emoji_sets import EmojiSetConfig, register_layer

@register_layer("payment")
class PaymentLayer(EmojiSetConfig):
    domain = "payment"
    
    EMOJI_MATRIX = {
        "charge": {"started": "💳", "completed": "✅", "failed": "❌"},
        "refund": {"started": "↩️", "completed": "✅", "failed": "❌"}
    }
    
    def charge_card(self, amount: float, currency: str, **kwargs):
        self.logger.info("payment_charge_started",
                        amount=amount,
                        currency=currency,
                        **kwargs)
```

### Context Integration

```python
from provide.foundation import logger
from provide.foundation.emoji_sets import http_layer

with logger.bind(request_id="abc-123"):
    http_layer.request_started(method="POST", path="/api/orders")
    # Includes request_id in all logs within context
```

## Impact

This design introduces new functionality without breaking existing APIs. The traditional logger interface remains unchanged, ensuring backward compatibility across the provide.io ecosystem.

## Security Considerations

1. **Sanitization**: Layers must sanitize sensitive data (e.g., SQL queries, API keys)
2. **PII Protection**: Personal information must be excluded or redacted
3. **Rate Limiting**: Layers should implement rate limiting for high-frequency events

## Performance Impact

Benchmarks show minimal overhead:
- **Without emoji sets**: 14,000 msg/sec
- **With emoji sets**: 13,500 msg/sec (3.5% overhead)
- **With emoji mapping**: 13,200 msg/sec (5.7% overhead)

## References

- [Structured Logging Best Practices](https://www.structlog.org/en/stable/why.html)
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/)
- [Emoji Unicode Standard](https://unicode.org/emoji/charts/full-emoji-list.html)

## Copyright

This document is placed in the public domain.