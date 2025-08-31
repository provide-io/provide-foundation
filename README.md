<div align="center">

# 🐍📡 `provide.foundation`

**Beautiful, performant, structured logging for Python.**

Modern structured logging built on `structlog` with emoji-enhanced visual parsing and semantic Domain-Action-Status patterns.

[![Awesome: uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![PyPI Version](https://img.shields.io/pypi/v/provide-foundation?style=flat-square)](https://pypi.org/project/provide-foundation/)
[![Python Versions](https://img.shields.io/pypi/pyversions/provide-foundation?style=flat-square)](https://pypi.org/project/provide-foundation/)
[![Downloads](https://static.pepy.tech/badge/provide-foundation/month)](https://pepy.tech/project/provide-foundation)

[![CI](https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml/badge.svg)](https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/provide-io/provide-foundation/branch/main/graph/badge.svg)](https://codecov.io/gh/provide-io/provide-foundation)
[![Type Checked](https://img.shields.io/badge/type--checked-mypy-blue?style=flat-square)](https://mypy.readthedocs.io/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)

<!-- Dependencies & Performance -->
[![Powered by Structlog](https://img.shields.io/badge/powered%20by-structlog-lightgrey.svg?style=flat-square)](https://www.structlog.org/)
[![Built with attrs](https://img.shields.io/badge/built%20with-attrs-orange.svg?style=flat-square)](https://www.attrs.org/)
[![Performance](https://img.shields.io/badge/performance-%3E1k%20msg%2Fs-brightgreen?style=flat-square)](README.md#performance)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache-blue.svg?style=flat-square)](https://opensource.org/license/apache-2-0)

---

**Make your logs beautiful and meaningful!** `provide.foundation` transforms your application logging with visual emoji prefixes, semantic Domain-Action-Status patterns, and high-performance structured output. Perfect for development debugging, production monitoring, and everything in between.

</div>

## 🤔 Why `provide.foundation`?

* **🎨 Visual Log Parsing:** Emoji prefixes based on logger names and semantic context make logs instantly scannable
* **📊 Semantic Structure:** **(New!)** Extensible Semantic Layers for domains like LLMs, HTTP, and Databases, with a fallback to the classic Domain-Action-Status (DAS) pattern.
* **⚡ High Performance:** Benchmarked >14,000 msg/sec (see details below)
* **🔧 Zero Configuration:** Works beautifully out of the box, configurable via environment variables or code
* **🎯 Developer Experience:** Thread-safe, async-ready, with comprehensive type hints for Python 3.13+

## ✨ Features

* **🎨 Emoji-Enhanced Logging:**
  * **Logger Name Prefixes:** `🔑 User authentication successful` (auth module)
  * **(New!) Semantic Layer Prefixes:** `[🤖][✍️][👍] LLM response generated` (llm-generation-success)
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
pip install provide-foundation
```

## 💡 Quick Start

### Basic Usage

```python
from provide.foundation import setup_telemetry, logger

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

### 🏗️ Semantic Logging with Layers

Go beyond the basic DAS pattern with extensible, schema-driven logging. Semantic Layers allow you to define structured logging conventions for specific domains (like LLMs, HTTP, or Databases) and automatically get rich, contextual emoji prefixes.

**Example: Using the built-in `llm` layer**

First, enable the layer in your configuration:
```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

# Enable the 'llm' semantic layer
config = TelemetryConfig(
    logging=LoggingConfig(enabled_semantic_layers=["llm"])
)
setup_telemetry(config)
```

Now, log events using the layer's defined keys (like `llm.provider`, `llm.task`, `llm.outcome`):
```python
from provide.foundation import logger

# Log a successful LLM generation task
logger.info(
    "LLM response generated",
    **{
        "llm.provider": "openai",
        "llm.task": "generation",
        "llm.outcome": "success",
        "llm.model": "gpt-4o",
        "duration_ms": 1230,
        "llm.output.tokens": 250,
    }
)
# Output: [🤖][✍️][👍] LLM response generated duration_ms=1230 llm.output.tokens=250

# Log a rate-limiting event from another provider
logger.warning(
    "LLM call failed",
    **{
        "llm.provider": "anthropic",
        "llm.task": "chat",
        "llm.outcome": "rate_limit",
        "llm.model": "claude-3-opus",
    }
)
# Output: [📚][💬][⏳] LLM call failed
```
- **How it works:** The `llm` layer maps the `llm.provider` key to provider emojis (🤖 for openai, 📚 for anthropic), `llm.task` to task emojis (✍️ for generation), and `llm.outcome` to outcome emojis (👍 for success).
- **Extensible:** You can define your own custom layers and emoji sets for your application's specific domains!
- **Legacy DAS:** The original `domain`, `action`, `status` keys still work as a fallback if no semantic layers are active.

### Custom Configuration

```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    service_name="my-microservice",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json",           # JSON for production
        # Enable built-in layers for HTTP and Database logging
        enabled_semantic_layers=["http", "database"],
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
# New: Enable semantic layers via environment
export PYVIDER_LOG_ENABLED_SEMANTIC_LAYERS="llm,http"
```

```python
from provide.foundation import setup_telemetry, TelemetryConfig

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
from provide.foundation import setup_telemetry, logger, TelemetryConfig, LoggingConfig

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

`provide.foundation` is designed for high-throughput production environments:

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

The emoji system is now driven by **Semantic Layers**. The active layers determine which log keys produce emoji prefixes.

### Viewing the Active Emoji Contract

To see the complete emoji mappings for your **current configuration** (including any custom layers), run the following command. This is the best way to see which emojis are active.

```bash
# This will print the full emoji matrix for your active configuration
export PYVIDER_SHOW_EMOJI_MATRIX=true
python -c "from provide.foundation.logger.emoji_matrix import show_emoji_matrix; show_emoji_matrix()"
```

### Built-in Layer Emojis (Examples)

- **`llm` Layer:**
  - **Provider:** `llm.provider` -> `🤖` (openai), `📚` (anthropic), `🦙` (meta)
  - **Task:** `llm.task` -> `✍️` (generation), `💬` (chat), `🛠️` (tool_use)
  - **Outcome:** `llm.outcome` -> `👍` (success), `🔥` (error), `⏳` (rate_limit)

- **`http` Layer:**
  - **Method:** `http.method` -> `📥` (get), `📤` (post), `🗑️` (delete)
  - **Status Class:** `http.status_class` -> `✅` (2xx), `⚠️CLIENT` (4xx), `🔥SERVER` (5xx)

### Legacy DAS Emojis (Fallback)

These emojis are used when no semantic layers are active and you use the `domain`, `action`, and `status` keys.

- **Domain Emojis (Primary):** `🔑` auth, `🗄️` database, `🌐` network, `⚙️` system
- **Action Emojis (Secondary):** `➡️` login, `🔗` connect, `📤` send, `🔍` query
- **Status Emojis (Tertiary):** `✅` success, `🔥` error, `⚠️` warning, `⏳` attempt


## 🔧 Advanced Usage

### Async Applications

```python
import asyncio
from provide.foundation import setup_telemetry, logger, shutdown_foundation_telemetry

async def main():
    setup_telemetry()

    # Your async application code
    logger.info("Async app started")

    # Graceful shutdown
    await shutdown_foundation_telemetry()

asyncio.run(main())
```

<!-- NEW SECTION -->
### Timing Code Blocks

Easily log the duration and outcome of any code block using the `timed_block` context manager. It automatically handles success and failure cases.

```python
import time
from provide.foundation import logger, timed_block

# Successful operation
with timed_block(logger, "Data processing task", task_id="abc-123"):
    time.sleep(0.05)  # Simulate work
# Output: Data processing task task_id=abc-123 outcome=success duration_ms=50

# Failing operation
try:
    with timed_block(logger, "Database query", table="users"):
        raise ValueError("Connection refused")
except ValueError:
    pass # Exception is re-raised and caught here
# Output: Database query table=users outcome=error error.message='Connection refused' error.type=ValueError duration_ms=...
```
<!-- END NEW SECTION -->

### Production Configuration

```python
production_config = TelemetryConfig(
    service_name="production-service",
    logging=LoggingConfig(
        default_level="INFO",               # Don't spam with DEBUG
        console_formatter="json",           # Machine-readable
        enabled_semantic_layers=["http"],   # Enable HTTP layer for request logging
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

`provide.foundation` builds upon these excellent open-source libraries:

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

