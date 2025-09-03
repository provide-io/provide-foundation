# API Reference

Complete API documentation for provide.foundation.

## Quick Navigation

<div class="feature-grid">
  <div class="feature-card">
    <h3>🎯 Core APIs</h3>
    <p>Fundamental logging and configuration</p>
    <ul>
      <li><a href="core/logger/">Logger</a></li>
      <li><a href="core/config/">Configuration</a></li>
      <li><a href="core/telemetry/">Telemetry</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🌐 Semantic Layers</h3>
    <p>Domain-specific logging interfaces</p>
    <ul>
      <li><a href="semantic/http/">HTTP Layer</a></li>
      <li><a href="semantic/database/">Database Layer</a></li>
      <li><a href="semantic/llm/">LLM Layer</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🖥️ CLI Framework</h3>
    <p>Command-line interface tools</p>
    <ul>
      <li><a href="cli/decorators/">Decorators</a></li>
      <li><a href="cli/registry/">Registry</a></li>
      <li><a href="cli/helpers/">Helpers</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🔧 Utilities</h3>
    <p>System and helper utilities</p>
    <ul>
      <li><a href="utils/platform/">Platform</a></li>
      <li><a href="utils/process/">Process</a></li>
      <li><a href="utils/console/">Console</a></li>
    </ul>
  </div>
</div>

## Primary Interfaces

### Logger

The main logging interface:

```python
from provide.foundation import logger, plog

# Direct logger usage
logger.info("event_occurred", user_id=123, action="login")

# Convenience alias
plog.debug("debug_info", details={"key": "value"})
```

**Key Methods:**
- `debug()`, `info()`, `warning()`, `error()`, `critical()`
- `bind()` - Add context to all subsequent logs
- `unbind()` - Remove context
- `exception()` - Log with exception info

### Configuration

Type-safe configuration management:

```python
from provide.foundation.config import TelemetryConfig

config = TelemetryConfig.from_env()
config = TelemetryConfig(
    level="DEBUG",
    format="json",
    enable_emoji=True
)
```

### CLI Framework

Build command-line interfaces:

```python
from provide.foundation.cli import register_command, run_cli

@register_command("hello")
def hello(name: str = "World"):
    """Say hello."""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    run_cli()
```

### Console Output

Standardized output functions:

```python
from provide.foundation import pout, perr

pout("✅ Success message")  # stdout
perr("❌ Error message")    # stderr
```

## Module Organization

```
provide.foundation/
├── __init__.py           # Main exports
├── logger/               # Logging system
│   ├── base.py          # Core logger
│   ├── config.py        # Configuration
│   ├── processors.py    # Log processors
│   └── emoji_matrix.py  # Emoji mappings
├── cli/                  # CLI framework
│   ├── decorators.py    # Command decorators
│   ├── registry.py      # Command registry
│   └── runner.py        # CLI runner
├── config/               # Configuration
│   ├── base.py          # Base config
│   ├── env.py           # Environment parsing
│   └── loaders.py       # File loaders
├── platform/             # Platform utilities
│   ├── detect.py        # OS detection
│   └── info.py          # System info
├── process/              # Process execution
│   ├── run.py           # Command runner
│   └── output.py        # Output capture
├── console/              # Console output
│   └── output.py        # pout/perr functions
├── errors/               # Error handling
│   ├── base.py          # Base exceptions
│   └── handlers.py      # Error handlers
├── registry/             # Registry pattern
│   └── base.py          # Object registry
└── semantic_layers.py    # Semantic layers
```

## Type Annotations

All APIs are fully type-annotated:

```python
from typing import Any
from provide.foundation import logger

def process_data(data: dict[str, Any]) -> None:
    logger.info("processing_data", size=len(data))
```

## Thread Safety

All core APIs are thread-safe:

```python
import threading
from provide.foundation import logger

def worker(n: int) -> None:
    logger.info("worker_started", worker_id=n)

threads = [
    threading.Thread(target=worker, args=(i,))
    for i in range(10)
]
```

## Async Support

Full async/await support:

```python
import asyncio
from provide.foundation import logger

async def async_task():
    async with logger.bind(task="async"):
        await logger.ainfo("async_operation")
```

## Extension Points

### Custom Processors

```python
from provide.foundation.logger import add_processor

def custom_processor(logger, method_name, event_dict):
    event_dict["custom_field"] = "value"
    return event_dict

add_processor(custom_processor)
```

### Custom Semantic Layers

```python
from provide.foundation.semantic_layers import SemanticLayer

class CustomLayer(SemanticLayer):
    domain = "custom"
    
    def get_emoji(self, action: str, status: str) -> str:
        return "🔧"
```

## Performance Characteristics

| Operation | Time | Throughput |
|-----------|------|------------|
| Simple log | 71μs | 14,000/sec |
| With context | 85μs | 11,700/sec |
| JSON format | 62μs | 16,100/sec |
| With emoji | 78μs | 12,800/sec |

## Version Compatibility

| provide.foundation | Python | API Stability |
|-------------------|---------|---------------|
| 1.0+ | 3.11+ | Stable |
| 0.9 | 3.10+ | Beta |
| 0.8 | 3.9+ | Alpha |

## See Also

- [User Guide](../guide/index.md) - Learn concepts and patterns
- [Cookbook](../cookbook/index.md) - Practical recipes
- [Specification](../spec/index.md) - Technical specifications