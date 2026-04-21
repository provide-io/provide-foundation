# 🧱🏗️ Provide Foundation

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-package_manager-FF6B35.svg)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml/badge.svg)](https://github.com/provide-io/provide-foundation/actions)

**A comprehensive Python foundation library for modern applications**

provide.foundation offers structured logging, CLI utilities, configuration management, error handling, and essential application building blocks. Built with modern Python practices, it provides the core infrastructure that production applications need.

## ✨ Key Features

- 📝 **Structured Logging** - Beautiful, performant logging with emoji-enhanced visual parsing
- 🛡️ **Error Handling** - Comprehensive error handling with retry logic and error boundaries
- ⚙️ **Configuration Management** - Flexible configuration with environment variables and files
- 🔧 **CLI Framework** - Build command-line interfaces with automatic help generation
- 🔐 **Cryptographic Utilities** - Modern algorithms and secure defaults
- 📁 **File Operations** - Atomic file operations with format support and safety guarantees
- 🔄 **Resilience Patterns** - Retry, circuit breaker, and bulkhead decorators
- ⚡ **Async Support** - High-level utilities for managing asynchronous tasks

## Quick Start

> **Note**: provide-foundation is in pre-release (v0.x.x). APIs and features may change before 1.0 release.

1. Install: `uv add provide-foundation`
2. Read the [Quick Start guide](https://github.com/provide-io/provide-foundation/blob/main/docs/getting-started/quick-start.md).
3. Explore runnable examples in [examples/README.md](https://github.com/provide-io/provide-foundation/blob/main/examples/README.md).

## Documentation
- [Documentation index](https://github.com/provide-io/provide-foundation/blob/main/docs/index.md)
- [Getting started](https://github.com/provide-io/provide-foundation/blob/main/docs/getting-started/index.md)
- [Reference](https://github.com/provide-io/provide-foundation/blob/main/docs/reference/index.md)

## Development

### Quick Start

```bash
# Set up environment
uv sync

# Run common tasks
we run test       # Run tests
we run lint       # Check code
we run format     # Format code
we tasks          # See all available commands
```

See [CLAUDE.md](https://github.com/provide-io/provide-foundation/blob/main/CLAUDE.md) for detailed development instructions and architecture information.

## Contributing
See [CONTRIBUTING.md](https://github.com/provide-io/provide-foundation/blob/main/CONTRIBUTING.md) for contribution guidelines.

## License
See [LICENSE](https://github.com/provide-io/provide-foundation/blob/main/LICENSE) for license details.

## Quality Standards

**provide.foundation** focuses on code quality, testing, and reliability:

- **Test Coverage** is tracked and enforced in CI.
- **Security Checks** include path traversal and symlink validation tests.
- **Performance Benchmarks** cover logging, transport, and archive operations.
- **Type Checking** is enforced with `mypy`.
- **Linting and Formatting** are enforced with `ruff`.

---

### Optional Dependencies

provide.foundation has optional feature sets that require additional dependencies:

| Feature | Install Command | Required For |
|---------|----------------|--------------|
| **Basic logging** | `uv add provide-foundation` | Core logging functionality |
| **CLI framework** | `uv add provide-foundation[cli]` | Command-line interface features |
| **Cryptography** | `uv add provide-foundation[crypto]` | Hash functions, digital signatures, certificates |
| **HTTP Transport** | `uv add provide-foundation[transport]` | HTTP client utilities and transport features |
| **OpenTelemetry** | `uv add provide-foundation[opentelemetry]` | Distributed tracing and metrics |
| **All features** | `uv add provide-foundation[all]` | Everything above |

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
- Ultra-low latency systems (<100μs requirements) - e.g., HFT systems, real-time gaming servers where Foundation's lock-based registry adds unwanted overhead
- Full-stack framework needs (use Django, Rails) - Foundation provides logging/config but not ORM, templating, or routing
- Tool stack incompatibility - e.g., if your team standardized on Pydantic models (Foundation uses attrs) or loguru (Foundation uses structlog)

### Key Design Decisions

**Tool Stack Philosophy**: Built on proven tools (attrs, structlog, click) with strong opinions for consistency. Trade-off: less flexibility, but cohesive and well-tested stack.

**Threading Model**: Registry uses `threading.RLock` (not `asyncio.Lock`). Negligible impact for typical use cases (CLI apps, initialization-time registration, read-heavy workloads). For high-throughput async web services (>10k req/sec) with runtime registration in hot paths, consider async-native alternatives.

**Global State Pattern**: Singletons (`get_hub()`, `logger`) for ergonomic APIs. Mitigation: `provide-testkit` provides `reset_foundation_setup_for_testing()` for clean test state.

**Intentional Scope**: Provides logging, configuration, CLI patterns. Does NOT provide web frameworks, databases, auth, or templates. Integrate with FastAPI/Flask/Django for web applications.

<p align="center">
  Built by <a href="https://provide.io">provide.io</a>
</p>

Copyright (c) provide.io LLC.
