# API Reference

Complete API documentation for provide.foundation.

## Quick Navigation

<div class="feature-grid">
  <div class="feature-card">
    <h3>🎯 Core APIs</h3>
    <p>Fundamental logging and configuration</p>
    <ul>
      <li><a href="logger/index/">Logger System</a></li>
      <li><a href="config/index/">Configuration</a></li>
      <li><a href="context/index/">Context Management</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>📁 File & Data</h3>
    <p>Safe file operations and data handling</p>
    <ul>
      <li><a href="file/index/">File Operations</a></li>
      <li><a href="crypto/index/">Cryptographic Utils</a></li>
      <li><a href="utils/index/">Environment & Utils</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🖥️ Console & CLI</h3>
    <p>User interaction and command-line tools</p>
    <ul>
      <li><a href="utils/console/">Console I/O</a></li>
      <li><a href="cli/decorators/">CLI Decorators</a></li>
      <li><a href="hub/index/">Command Hub</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🌐 Semantic & Advanced</h3>
    <p>Domain-specific and advanced features</p>
    <ul>
      <li><a href="semantic/http/">HTTP Layer</a></li>
      <li><a href="semantic/database/">Database Layer</a></li>
      <li><a href="semantic/llm/">LLM Layer</a></li>
    </ul>
  </div>
</div>

## Primary Interfaces

### Logger

The main logging interface with structured, emoji-enhanced output:

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

### Console I/O

Standardized input/output functions with JSON mode support:

```python
from provide.foundation import pout, perr, pin

# Output with styling
pout("✅ Success message", color="green", bold=True)
perr("❌ Error message", color="red")

# Interactive input with type conversion
name = pin("Enter name: ")
age = pin("Enter age: ", type=int, default=0)
password = pin("Password: ", password=True)
```

### Configuration and Context

Unified configuration management from multiple sources:

```python
from provide.foundation import Context

# Environment-based configuration
ctx = Context.from_env()

# Programmatic configuration
ctx = Context(
    log_level="DEBUG",
    profile="development",
    debug=True,
    json_output=False
)

# Load from files (TOML, JSON, YAML)
ctx.load_config("config.toml")
```

### File Operations

Safe, atomic file operations with format support:

```python
from provide.foundation.file import atomic_write_text, read_json, write_json

# Atomic operations prevent corruption
atomic_write_text("config.txt", "new content", backup=True)

# Format-specific operations
data = read_json("config.json", default={})
write_json("output.json", {"key": "value"})
```

### Cryptographic Utilities

Secure hashing and checksum verification:

```python
from provide.foundation.crypto import hash_file, verify_file, calculate_checksums

# Hash files securely
digest = hash_file("document.pdf", algorithm="sha256")

# Verify integrity
is_valid = verify_file("document.pdf", expected_hash)

# Batch checksum calculation
checksums = calculate_checksums(["file1.txt", "file2.txt"])
```

### Environment and Utilities

Type-safe environment parsing and formatting utilities:

```python
from provide.foundation.utils import get_int, get_bool, format_size, timed_block

# Environment parsing with defaults
port = get_int("PORT", 8000)
debug = get_bool("DEBUG", False)

# Human-readable formatting
print(format_size(1536))  # "1.5 KB"

# Performance timing with logging
with timed_block(logger, "data_processing") as ctx:
    # Your code here
    ctx["records_processed"] = 1000
```

## Module Organization

```
provide.foundation/
├── __init__.py              # Main exports and primary interface
├── logger/                  # Structured logging system
│   ├── base.py             # Core FoundationLogger
│   ├── config.py           # TelemetryConfig, LoggingConfig
│   ├── processors.py       # Log processing pipeline
│   └── emoji_matrix.py     # Visual emoji mappings
├── console/                 # Standardized I/O functions
│   ├── input.py            # pin(), pin_stream(), async variants
│   └── output.py           # pout(), perr() functions
├── context.py               # Unified Context class for configuration
├── config/                  # Advanced configuration system
│   ├── base.py             # Base configuration classes
│   ├── env.py              # Environment variable parsing
│   ├── loader.py           # File loading (YAML, JSON, TOML)
│   └── manager.py          # Configuration management
├── file/                    # Safe file operations
│   ├── atomic.py           # Atomic write operations
│   ├── formats.py          # JSON, YAML, TOML support
│   ├── safe.py             # Safe read/write operations
│   ├── lock.py             # File locking
│   └── utils.py            # File utilities
├── crypto/                  # Cryptographic utilities
│   ├── hashing.py          # File and data hashing
│   ├── checksums.py        # Checksum verification
│   ├── algorithms.py       # Algorithm management
│   └── utils.py            # Crypto utilities
├── utils/                   # Common utilities
│   ├── env.py              # Environment variable parsing
│   ├── formatting.py       # String and number formatting
│   ├── parsing.py          # Data type parsing
│   └── timing.py           # Performance timing
├── errors/                  # Comprehensive error handling
│   ├── base.py             # Base exceptions
│   ├── handlers.py         # Error handlers
│   └── decorators.py       # Error handling decorators
├── platform/                # Platform detection
│   └── detection.py        # OS and environment detection
├── process/                 # Process execution
│   ├── runner.py           # Subprocess execution
│   └── async_runner.py     # Async process execution
├── cli/                     # CLI framework components
│   ├── decorators.py       # Command decorators
│   └── testing.py          # CLI testing utilities
├── hub/                     # Command hub system
│   ├── manager.py          # Hub management
│   ├── registry.py         # Command registry
│   └── components.py       # Hub components
├── registry.py              # General registry pattern
└── emoji_sets.py       # Domain-specific logging layers
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

### Custom Emoji Sets

```python
from provide.foundation.emoji_sets import EmojiSetConfig

class CustomLayer(EmojiSetConfig):
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