# Welcome to the Provide Foundation

**The Provide Foundation** is a comprehensive Python library that provides structured logging, CLI framework, configuration management, and system utilities for building robust applications.

Built on industry-standard libraries like `structlog`, `click`, and `attrs`, provide.foundation offers a batteries-included development experience with beautiful console output, powerful error handling, and cross-platform system utilities.

## Key Features

### Structured Logging
- Beautiful, event-enriched structured logging
- High-performance logging (>14,000 msg/sec)
- Event sets for log enrichment
- Thread-safe and async-compatible

### CLI Framework
- Decorator-based command registration
- Nested commands with dot notation
- Automatic help generation
- JSON output mode support

### Configuration Management
- Environment variable support
- Multi-source configuration loading
- Type-safe with attrs classes
- YAML, JSON, and TOML support

### System Utilities
- **Platform Detection**: OS and architecture detection
- **Process Execution**: Safe subprocess handling with async support
- **File Operations**: Atomic operations with format support
- **Console I/O**: Standardized input/output with color support
- **Registry Pattern**: Thread-safe component management

### Cryptographic Operations
- **Hash Functions**: SHA-256, SHA-512, Blake2b with file/stream support
- **Digital Signatures**: Ed25519, ECDSA, RSA with verification
- **Certificates**: X.509 certificate creation and management
- **Key Generation**: Secure key generation for multiple algorithms

### Error Handling
- Rich error context with metadata
- Retry decorators
- Error boundaries for graceful degradation
- Structured error logging

## Quick Start

```python
from provide.foundation import logger, pout, perr
from provide.foundation.hub import register_command
from provide.foundation import platform, process
from provide.foundation.crypto import hash_file

# Structured logging with event enrichment
logger.info("Starting application", version="1.0.0")

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
logger.info("System info", **info.to_dict())

# Process execution
result = process.run_command(["git", "status"])
if result.returncode == 0:
    pout("Repository is clean")

# Cryptographic operations
file_hash = hash_file("document.pdf")
logger.info("File verified", hash=file_hash.hex_digest)
```

## 📚 Documentation Structure

### [Getting Started](getting-started/installation.md)
- Installation guide
- Quick start tutorial
- Basic configuration

### [Core Concepts](guide/concepts/index.md)
- Structured logging principles
- Event enrichment system
- Configuration architecture

### [API Reference](api/api-index.md)
Complete API documentation for all modules:
- Logger and telemetry
- CLI framework  
- Configuration system
- Cryptographic utilities
- File operations
- Platform utilities
- Process execution
- Console I/O
- Hub and registry
- Error handling
- Context management

### [User Guide](guide/index.md)
Practical guides for common tasks:
- Configuration management
- Logging patterns
- CLI development
- System utilities

### [Examples](getting-started/examples.md)
Practical examples and code snippets

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
- **Stable API**: Contextual versioning

### For DevOps Teams
- **Observable**: Structured logs for analysis
- **Configurable**: Environment-based configuration
- **Cross-Platform**: Works on Linux, macOS, Windows
- **Production Ready**: Thread-safe, battle-tested


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

We welcome contributions! See our [Contributing Guide](development/contributing.md) for details.

## 📄 License

Apache 2.0 - See LICENSE file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/provide-io/provide-foundation)
- [PyPI Package](https://pypi.org/project/provide-foundation/)
- [Issue Tracker](https://github.com/provide-io/provide-foundation/issues)

---

Ready to get started? Head to the [Installation Guide](getting-started/installation.md) →