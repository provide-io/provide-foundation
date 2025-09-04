# Welcome to provide.foundation

**`provide.foundation`** is a comprehensive Python foundation library that provides structured logging, CLI framework, configuration management, and system utilities for building robust applications.

Built on industry-standard libraries like `structlog`, `click`, and `attrs`, provide.foundation offers a batteries-included development experience with beautiful console output, powerful error handling, and cross-platform system utilities.

## ✨ Key Features

### 🎯 Structured Logging
- Beautiful, emoji-enhanced visual parsing
- High-performance logging (>14,000 msg/sec)
- Semantic layers for domain-specific logging
- Thread-safe and async-compatible

### 🖥️ CLI Framework
- Decorator-based command registration
- Nested commands with dot notation
- Automatic help generation
- JSON output mode support

### ⚙️ Configuration Management
- Environment variable support
- Multi-source configuration loading
- Type-safe with attrs classes
- YAML, JSON, and TOML support

### 🔧 System Utilities
- **Platform Detection**: OS and architecture detection
- **Process Execution**: Safe subprocess handling with logging
- **Console Output**: Standardized stdout/stderr functions
- **Registry Pattern**: Thread-safe object storage

### 🛡️ Error Handling
- Rich error context with metadata
- Retry decorators
- Error boundaries for graceful degradation
- Structured error logging

## 🚀 Quick Start

```python
from provide.foundation import plog, pout, perr
from provide.foundation.cli import register_command
from provide.foundation import platform, process

# Structured logging with emojis
plog.info("Starting application", version="1.0.0")

# Console output
pout("✅ Configuration loaded")
perr("⚠️ Low memory warning")

# CLI commands
@register_command("deploy")
def deploy(environment: str = "staging"):
    """Deploy the application."""
    pout(f"Deploying to {environment}...")

# Platform detection
info = platform.get_system_info()
plog.info(f"Running on {info.platform}")

# Process execution
result = process.run_command(["git", "status"])
if result.returncode == 0:
    pout("Repository is clean")
```

## 📚 Documentation Structure

### [Getting Started](getting-started/installation.md)
- Installation guide
- Quick start tutorial
- Basic configuration

### [Core Concepts](core-concepts/structured-logging.md)
- Structured logging principles
- Semantic layers
- The emoji system
- Configuration architecture

### [API Reference](api-reference/logger.md)
Complete API documentation for all modules:
- Logger and telemetry
- CLI framework
- Configuration system
- Platform utilities
- Process execution
- Console output
- Registry pattern
- Error handling

### [Guides](guides/async-usage.md)
Practical guides for common tasks:
- Async usage patterns
- Exception logging
- Performance tuning
- Creating custom semantic layers

### [Tutorials](tutorials/fastapi-integration.md)
Step-by-step tutorials for integrations

## 🎯 Why provide.foundation?

### For Application Developers
- **Zero Configuration**: Works beautifully out of the box
- **Type Safe**: Full type hints and runtime validation
- **Fast**: Optimized for production workloads
- **Testable**: Built-in testing utilities

### For Library Authors
- **Extensible**: Plugin system via Registry
- **Composable**: Mix and match components
- **Well-Documented**: Comprehensive API docs
- **Stable API**: Semantic versioning

### For DevOps Teams
- **Observable**: Structured logs for analysis
- **Configurable**: Environment-based configuration
- **Cross-Platform**: Works on Linux, macOS, Windows
- **Production Ready**: Thread-safe, battle-tested

## 🔄 Migration from pyvider

If you're migrating from `pyvider.telemetry`:

```python
# Old (pyvider)
from provide.foundation import logger

# New (provide.foundation)
from provide.foundation import plog as logger

# Or use the logger directly
from provide.foundation import logger
```

The API is largely compatible, with improvements:
- Better performance
- More features
- Cleaner configuration
- Enhanced error handling

## 🚦 System Requirements

- Python 3.11 or higher
- No compiled dependencies
- Works on Linux, macOS, and Windows
- Optional: psutil for enhanced system info

## 📦 Installation

```bash
pip install provide-foundation

# With all optional dependencies
pip install provide-foundation[all]

# For development
pip install provide-foundation[dev]
```

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](about/contributing.md) for details.

## 📄 License

Apache 2.0 - See LICENSE file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/provide-io/provide-foundation)
- [PyPI Package](https://pypi.org/project/provide-foundation/)
- [Issue Tracker](https://github.com/provide-io/provide-foundation/issues)

---

Ready to get started? Head to the [Installation Guide](getting-started/installation.md) →