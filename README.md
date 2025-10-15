# provide.foundation

**A Comprehensive Python Foundation Library for Modern Applications**

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

<p align="center">
  Built by <a href="https://provide.io">provide.io</a>
</p>
