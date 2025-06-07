<div align="center">

# 🐍📡 `pyvider.telemetry`

**Beautiful, performant, structured logging for Python.**

Modern structured logging built on `structlog` with emoji-enhanced visual parsing and semantic Domain-Action-Status patterns.

[![Awesome: uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![PyPI Version](https://img.shields.io/pypi/v/pyvider-telemetry?style=flat-square)](https://pypi.org/project/pyvider-telemetry/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyvider-telemetry?style=flat-square)](https://pypi.org/project/pyvider-telemetry/)
[![Downloads](https://static.pepy.tech/badge/pyvider-telemetry/month)](https://pepy.tech/project/pyvider-telemetry)

[![CI](https://github.com/provide-io/pyvider-telemetry/actions/workflows/ci.yml/badge.svg)](https://github.com/provide-io/pyvider-telemetry/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/provide-io/pyvider-telemetry/branch/main/graph/badge.svg)](https://codecov.io/gh/provide-io/pyvider-telemetry)
[![Type Checked](https://img.shields.io/badge/type--checked-mypy-blue?style=flat-square)](https://mypy.readthedocs.io/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)

<!-- Dependencies & Performance -->
[![Powered by Structlog](https://img.shields.io/badge/powered%20by-structlog-lightgrey.svg?style=flat-square)](https://www.structlog.org/)
[![Built with attrs](https://img.shields.io/badge/built%20with-attrs-orange.svg?style=flat-square)](https://www.attrs.org/)
[![Performance](https://img.shields.io/badge/performance-%3E1k%20msg%2Fs-brightgreen?style=flat-square)](README.md#performance)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache-blue.svg?style=flat-square)](https://opensource.org/license/apache-2-0)

---

**Make your logs beautiful and meaningful!** `pyvider.telemetry` transforms your application logging with visual emoji prefixes, semantic Domain-Action-Status patterns, and high-performance structured output. Perfect for development debugging, production monitoring, and everything in between.

</div>

## 🤔 Why `pyvider.telemetry`?

* **🎨 Visual Log Parsing:** Emoji prefixes based on logger names and semantic context make logs instantly scannable
* **📊 Semantic Structure:** Domain-Action-Status (DAS) pattern brings meaning to your log events
* **⚡ High Performance:** Benchmarked >14,000 msg/sec (see details below)
* **🔧 Zero Configuration:** Works beautifully out of the box, configurable via environment variables or code
* **🎯 Developer Experience:** Thread-safe, async-ready, with comprehensive type hints for Python 3.13+

## ✨ Features

* **🎨 Emoji-Enhanced Logging:**
  * **Logger Name Prefixes:** `🔑 User authentication successful` (auth module)
  * **Domain-Action-Status:** `[🔑][➡️][✅] Login completed` (auth-login-success)
  * **Custom TRACE Level:** Ultra-verbose debugging with `👣` visual markers

* **📈 Production Ready:**
  * **High Performance:** >14,000 messages/second throughput (average ~40,000 msg/sec)
  * **Thread Safe:** Concurrent logging from multiple threads
  * **Async Support:** Native async/await compatibility
  * **Memory Efficient:** Optimized emoji caching and processor chains

* **⚙️ Flexible Configuration:**
  * **Multiple Formats:** JSON for production, key-value for development
  * **Module-Level Filtering:** Different log levels per component
  * **Environment Variables:** Zero-code configuration options
  * **Service Identification:** Automatic service name injection

* **🏗️ Modern Python:**
  * **Python 3.13+ Exclusive:** Latest language features and typing
  * **Built with `attrs`:** Immutable, validated configuration objects
  * **Structlog Foundation:** Industry-standard structured logging

## 🚀 Installation

Requires Python 3.13 or later.

```bash
pip install pyvider-telemetry
```

## 💡 Quick Start

### Basic Usage

```python
from pyvider.telemetry import setup_telemetry, logger

# Initialize with sensible defaults
setup_telemetry()

# Start logging immediately
logger.info("Application started", version="1.0.0")
logger.debug("Debug information", component="auth")
logger.error("Something went wrong", error_code="E123")

# Create component-specific loggers
auth_logger = logger.get_logger("auth.service")
auth_logger.info("User login attempt", user_id=12345)
# Output: 🔑 User login attempt user_id=12345
```

### Semantic Domain-Action-Status Logging

```python
# Use domain, action, status for semantic meaning
logger.info("User authentication",
           domain="auth", action="login", status="success",
           user_id=12345, ip="192.168.1.100")
# Output: [🔑][➡️][✅] User authentication user_id=12345 ip=192.168.1.100

logger.error("Database connection failed",
            domain="database", action="connect", status="error",
            host="db.example.com", timeout_ms=5000)
# Output: [🗄️][🔗][🔥] Database connection failed host=db.example.com timeout_ms=5000
```

### Custom Configuration

```python
from pyvider.telemetry import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    service_name="my-microservice",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json",           # JSON for production
        module_levels={
            "auth": "DEBUG",                # Verbose auth logging
            "database": "ERROR",            # Only DB errors
            "external.api": "WARNING",      # Minimal third-party noise
        }
    )
)

setup_telemetry(config)
```

### Environment Variable Configuration

```bash
export PYVIDER_SERVICE_NAME="my-service"
export PYVIDER_LOG_LEVEL="INFO"
export PYVIDER_LOG_CONSOLE_FORMATTER="json"
export PYVIDER_LOG_MODULE_LEVELS="auth:DEBUG,db:ERROR"
```

```python
from pyvider.telemetry import setup_telemetry, TelemetryConfig

# Automatically loads from environment
setup_telemetry(TelemetryConfig.from_env())
```

### Exception Logging

```python
try:
    risky_operation()
except Exception:
    logger.exception("Operation failed",
                    operation="user_registration",
                    user_id=123)
    # Automatically includes full traceback
```

### Ultra-Verbose TRACE Logging

```python
from pyvider.telemetry import setup_telemetry, logger, TelemetryConfig, LoggingConfig

# Enable TRACE level for deep debugging
config = TelemetryConfig(
    logging=LoggingConfig(default_level="TRACE")
)
setup_telemetry(config)

logger.trace("Entering function", function="authenticate_user")
logger.trace("Token validation details",
            token_type="bearer", expires_in=3600)
```

## 📊 Performance

`pyvider.telemetry` is designed for high-throughput production environments:

| Scenario | Performance | Notes |
|----------|-------------|-------|
| **Basic Logging** | ~40,000 msg/sec | Key-value format with emojis |
| **JSON Output** | ~38,900 msg/sec | Structured production format |
| **Multithreaded** | ~39,800 msg/sec | Concurrent logging |
| **Level Filtering** | ~68,100 msg/sec | Efficiently filters by level |
| **Large Payloads** | ~14,200 msg/sec | Logging with larger event data |
| **Async Logging** | ~43,400 msg/sec | Logging from async code |

**Overall Average Throughput:** ~40,800 msg/sec
**Peak Throughput:** ~68,100 msg/sec

Run benchmarks yourself:
```bash
python scripts/benchmark_performance.py

python scripts/extreme_performance.py
```

## 🎨 Emoji Reference

### Domain Emojis (Primary)
- `🔑` auth, `🗄️` database, `🌐` network, `⚙️` system
- `🛎️` server, `🙋` client, `🔐` security, `📄` file

### Action Emojis (Secondary)
- `➡️` login, `🔗` connect, `📤` send, `📥` receive
- `🔍` query, `📝` write, `🗑️` delete, `⚙️` process

### Status Emojis (Tertiary)
- `✅` success, `❌` failure, `🔥` error, `⚠️` warning
- `⏳` attempt, `🔁` retry, `🏁` complete, `⏱️` timeout

See full matrix: `PYVIDER_SHOW_EMOJI_MATRIX=true python -c "from pyvider.telemetry.logger.emoji_matrix import show_emoji_matrix; show_emoji_matrix()"`

## 🔧 Advanced Usage

### Async Applications

```python
import asyncio
from pyvider.telemetry import setup_telemetry, logger, shutdown_pyvider_telemetry

async def main():
    setup_telemetry()

    # Your async application code
    logger.info("Async app started")

    # Graceful shutdown
    await shutdown_pyvider_telemetry()

asyncio.run(main())
```

### Production Configuration

```python
production_config = TelemetryConfig(
    service_name="production-service",
    logging=LoggingConfig(
        default_level="INFO",               # Don't spam with DEBUG
        console_formatter="json",           # Machine-readable
        module_levels={
            "security": "DEBUG",            # Always verbose for security
            "performance": "WARNING",       # Only perf issues
            "third_party": "ERROR",         # Minimal external noise
        }
    )
)
```

## 📚 Documentation

For comprehensive API documentation, configuration options, and advanced usage patterns, see:

**[📖 Complete API Reference](docs/api-reference.md)**

## 📜 License

This project is licensed under the **Apache 2.0 License**. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

`pyvider.telemetry` builds upon these excellent open-source libraries:

- [`structlog`](https://www.structlog.org/) - The foundation for structured logging
- [`attrs`](https://www.attrs.org/) - Powerful data classes and configuration management

## 🤖 Development Transparency

**AI-Assisted Development Notice**: This project was developed with significant AI assistance for code generation and implementation. While AI tools performed much of the heavy lifting for writing code, documentation, and tests, all architectural decisions, design patterns, functionality requirements, and final verification were made by human developers.

**Human Oversight Includes**:
- Architectural design and module structure decisions
- API design and interface specifications  
- Feature requirements and acceptance criteria
- Code review and functionality verification
- Performance requirements and benchmarking validation
- Testing strategy and coverage requirements
- Release readiness assessment

**AI Assistance Includes**:
- Code implementation based on human specifications
- Documentation generation and formatting
- Test case generation and implementation
- Example script creation
- Boilerplate and repetitive code generation

This approach allows us to leverage AI capabilities for productivity while maintaining human control over critical technical decisions and quality assurance.
