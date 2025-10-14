# provide.foundation

**A Comprehensive Python Foundation Library for Modern Applications**

<p align="center">
    <a href="https://pypi.org/project/provide-foundation/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/provide-foundation.svg">
    </a>
    <a href="https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml">
        <img alt="CI Status" src="https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/provide-io/provide-foundation">
        <img src="https://codecov.io/gh/provide-io/provide-foundation/branch/main/graph/badge.svg"/>
    </a>
    <img alt="Test Coverage" src="https://img.shields.io/badge/coverage-83.65%25-brightgreen.svg">
    <img alt="Test Count" src="https://img.shields.io/badge/tests-1000+-blue.svg">
    <img alt="Type Checking" src="https://img.shields.io/badge/typing-mypy-informational.svg">
    <a href="https://github.com/provide-io/provide-foundation/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/provide-io/provide-foundation.svg">
    </a>
</p>

---

**provide.foundation** is a comprehensive foundation library for Python applications, offering structured logging, CLI utilities, configuration management, error handling, and essential application building blocks. Built with modern Python practices, it provides the core infrastructure that production applications need.

## Quality Standards

**provide.foundation** maintains high standards for code quality, testing, and reliability:

- **83.65% Test Coverage** with 1000+ comprehensive tests
- **46 modules with 100% coverage** including core components
- **Comprehensive Security Testing** with path traversal, symlink validation, and input sanitization
- **Performance Benchmarked** logging, transport, and archive operations
- **Type-Safe Codebase** with comprehensive type annotations
- **Automated Quality Checks** with ruff, mypy, and bandit

---

## Getting Started

> **Important:** This project uses `uv` for Python environment and package management.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/provide-io/provide-foundation.git
cd provide-foundation

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync
```

### Installing as a Package

```bash
# Install from PyPI
uv add provide-foundation

# Or install from source
uv add git+https://github.com/provide-io/provide-foundation.git

# Or using pip (if you prefer)
pip install provide-foundation
```

### Optional Dependencies

provide.foundation has optional feature sets that require additional dependencies:

| Feature | Install Command | Required For |
|---------|----------------|--------------|
| **Basic logging** | `pip install provide-foundation` | Core logging functionality |
| **CLI framework** | `pip install provide-foundation[cli]` | Command-line interface features |
| **Cryptography** | `pip install provide-foundation[crypto]` | Hash functions, digital signatures, certificates |
| **HTTP Transport** | `pip install provide-foundation[transport]` | HTTP client utilities and transport features |
| **OpenTelemetry** | `pip install provide-foundation[opentelemetry]` | Distributed tracing and metrics |
| **All features** | `pip install provide-foundation[all]` | Everything above |

> **Quick Start Tip**: For immediate use with just logging, install the base package. Add extras as needed.

---

## What's Included

**provide.foundation** offers a comprehensive toolkit for building robust applications:

### Core Components

- **Structured Logging** - Beautiful, performant logging built on `structlog` with event-enriched structured logging and zero configuration required
- **Metrics** - Lightweight and extensible metrics collection with optional OpenTelemetry integration
- **CLI Framework** - Build command-line interfaces with automatic help generation and component registration (requires `[cli]` extra)
- **Configuration Management** - Flexible configuration system supporting environment variables, files, and runtime updates
- **Error Handling** - Comprehensive error handling with retry logic and error boundaries
- **Resilience Patterns** - Suite of decorators for building reliable applications (retry, circuit breaker, bulkhead)
- **Concurrency Utilities** - High-level utilities for managing asynchronous tasks and thread-safe operations
- **Cryptographic Utilities** - Comprehensive cryptographic operations with modern algorithms and secure defaults (requires `[crypto]` extra)
- **File Operations** - Atomic file operations with format support and safety guarantees
- **Archive Operations** - Create and extract archives with support for TAR, ZIP, GZIP, and BZIP2 formats
- **Serialization** - Safe and consistent JSON serialization and deserialization
- **Console I/O** - Enhanced console input/output with color support, JSON mode, and interactive prompts
- **Formatting Utilities** - Collection of helpers for formatting text, numbers, and data structures
- **Platform Utilities** - Cross-platform detection and system information gathering
- **Process Execution** - Safe subprocess execution with streaming and async support
- **Hub and Registry** - Central system for managing application components, commands, and resources

> **See the [examples/](examples/) directory and [documentation](https://provide-io.github.io/provide-foundation/) for comprehensive usage examples and tutorials.**

---

## Configuration

### Environment Variables

All configuration can be controlled through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PROVIDE_SERVICE_NAME` | Service identifier in logs | `None` |
| `PROVIDE_LOG_LEVEL` | Minimum log level | `WARNING` |
| `PROVIDE_LOG_CONSOLE_FORMATTER` | Output format (`key_value` or `json`) | `key_value` |
| `PROVIDE_LOG_OMIT_TIMESTAMP` | Remove timestamps from console | `false` |
| `PROVIDE_LOG_FILE` | Log to file path | `None` |
| `PROVIDE_LOG_MODULE_LEVELS` | Per-module log levels (format: module1:LEVEL,module2:LEVEL) | `""` |
| `PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED` | Enable emoji prefixes based on logger names | `true` |
| `PROVIDE_LOG_DAS_EMOJI_ENABLED` | Enable Domain-Action-Status emoji prefixes | `true` |
| `PROVIDE_TELEMETRY_DISABLED` | Globally disable telemetry | `false` |
| `PROVIDE_SERVICE_VERSION` | Service version for telemetry | `None` |
| `FOUNDATION_LOG_LEVEL` | Log level for Foundation internal setup messages | `WARNING` |
| `OTEL_SERVICE_NAME` | OpenTelemetry service name (takes precedence over PROVIDE_SERVICE_NAME) | `None` |
| `OTEL_TRACING_ENABLED` | Enable OpenTelemetry tracing | `true` |
| `OTEL_METRICS_ENABLED` | Enable OpenTelemetry metrics | `true` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint for traces and metrics | `None` |
| `OTEL_EXPORTER_OTLP_HEADERS` | Headers for OTLP requests (key1=value1,key2=value2) | `""` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (grpc, http/protobuf) | `http/protobuf` |
| `OTEL_TRACE_SAMPLE_RATE` | Sampling rate for traces (0.0 to 1.0) | `1.0` |

**Rate Limiting Configuration:**

| Variable | Description | Default |
|----------|-------------|---------|
| `PROVIDE_LOG_RATE_LIMIT_ENABLED` | Enable rate limiting for log output | `false` |
| `PROVIDE_LOG_RATE_LIMIT_GLOBAL` | Global rate limit (logs per second) | `None` |
| `PROVIDE_LOG_RATE_LIMIT_GLOBAL_CAPACITY` | Global rate limit burst capacity | `None` |
| `PROVIDE_LOG_RATE_LIMIT_PER_LOGGER` | Per-logger rate limits (format: logger1:rate:capacity,logger2:rate:capacity) | `""` |
| `PROVIDE_LOG_RATE_LIMIT_EMIT_WARNINGS` | Emit warnings when logs are rate limited | `true` |
| `PROVIDE_LOG_RATE_LIMIT_SUMMARY_INTERVAL` | Seconds between rate limit summary reports | `5.0` |
| `PROVIDE_LOG_RATE_LIMIT_MAX_QUEUE_SIZE` | Maximum number of logs to queue when rate limited | `1000` |
| `PROVIDE_LOG_RATE_LIMIT_MAX_MEMORY_MB` | Maximum memory (MB) for queued logs | `None` |
| `PROVIDE_LOG_RATE_LIMIT_OVERFLOW_POLICY` | Policy when queue is full: drop_oldest, drop_newest, or block | `drop_oldest` |

### Configuration Files

Support for YAML, JSON, TOML, and .env files:

```yaml
# config.yaml
service_name: my-app
environment: production

logging:
  level: INFO
  formatter: json
  file: /var/log/myapp.log

database:
  host: db.example.com
  port: 5432
  pool_size: 20
```

---

## OpenTelemetry Integration

provide.foundation includes built-in OpenTelemetry support for distributed tracing and metrics collection. The library supports standard OTLP-compatible backends including Jaeger, Honeycomb, Lightstep, and New Relic.

Configure via environment variables or programmatically. See the [documentation](https://provide-io.github.io/provide-foundation/) and [examples/tracing/](examples/tracing/) for detailed setup and usage patterns.

---

## Architecture & Design Philosophy

provide.foundation is intentionally designed as a **foundation layer**, not a full-stack framework. Understanding our architectural decisions helps teams evaluate whether the library aligns with their requirements.

### When to Use provide.foundation

**Excellent fit:**
- CLI applications and developer tools
- Microservices with structured logging needs
- Data processing pipelines
- Background task processors

**Good fit (with awareness):**
- Web APIs (use for logging, not HTTP server)
- Task processors (Celery, RQ)
- Libraries needing structured logging

**Consider alternatives:**
- Ultra-low latency systems (<100μs requirements)
- Full-stack framework needs (use Django, Rails)
- Tool stack incompatibility (Pydantic-only, loguru-only projects)

### Key Design Decisions

**Tool Stack Philosophy**: Built on proven tools (attrs, structlog, click) with strong opinions for consistency. Trade-off: less flexibility, but cohesive and well-tested stack.

**Threading Model**: Registry uses `threading.RLock` (not `asyncio.Lock`). Negligible impact for typical use cases (CLI apps, initialization-time registration, read-heavy workloads). For high-throughput async web services (>10k req/sec) with runtime registration in hot paths, consider async-native alternatives.

**Global State Pattern**: Singletons (`get_hub()`, `logger`) for ergonomic APIs. Mitigation: `provide-testkit` provides `reset_foundation_setup_for_testing()` for clean test state.

**Intentional Scope**: Provides logging, configuration, CLI patterns. Does NOT provide web frameworks, databases, auth, or templates. Integrate with FastAPI/Flask/Django for web applications.

## Documentation

For comprehensive documentation, tutorials, and API reference:

- **[Documentation](https://provide-io.github.io/provide-foundation/)** - Full documentation site
- **[Examples](examples/)** - Working code examples for all features
- **[Tutorials](https://provide-io.github.io/provide-foundation/tutorials/01-quick-start/)** - Step-by-step guides
- **[How-To Guides](https://provide-io.github.io/provide-foundation/how-to-guides/logging/basic-logging/)** - Task-focused recipes
- **[API Reference](https://provide-io.github.io/provide-foundation/reference/)** - Complete API documentation

---

<p align="center">
  Built by <a href="https://provide.io">provide.io</a>
</p>