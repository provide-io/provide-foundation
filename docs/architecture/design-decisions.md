# Architecture & Design Decisions

This document explains the **intentional design choices** in provide.foundation. Understanding these decisions helps teams evaluate whether the library aligns with their requirements.

---

## Design Philosophy

provide.foundation is designed as a **foundation layer**, not a full-stack framework. It provides:

- ✅ **Core infrastructure**: Logging, configuration, CLI, error handling
- ✅ **Building blocks**: Components that work together or independently
- ✅ **Strong opinions**: Curated tool stack with known characteristics
- ❌ **Not a full framework**: No ORM, web server, or database layer

**Key principle**: Provide excellent foundations that integrate with your choice of web framework, database, and business logic.

---

## Threading Model

### Current Implementation

The Registry uses `threading.RLock` for thread safety, not `asyncio.Lock`.

**Why this choice:**
- Works seamlessly in both sync and async contexts
- Zero dependencies on event loop
- Simpler implementation and debugging
- Thread-safe across all execution models

### When This Matters

The threading lock **matters** in:

```python
# ❌ Problematic: High-frequency runtime registration in async hot-path
async def handle_request(request):
    # This happens 10,000+ times per second
    hub = get_hub()
    plugin = hub.get_component(f"plugin_{request.type}")  # Registry lookup in hot path
    return await plugin.process(request)
```

**Impact**: Potential lock contention blocking the event loop in ultra-high-throughput async applications.

### When This Doesn't Matter

The threading lock is **negligible** in:

```python
# ✅ Typical usage: Initialization-time registration
def main():
    hub = get_hub()
    hub.initialize_foundation()  # One-time setup

    # Register components once
    hub.add_component(DatabasePool, name="db")
    hub.add_component(CacheManager, name="cache")

    # Now use them (no registry lookups in hot path)
    db = hub.get_component("db")
    run_application(db)
```

**Characteristics**:
- CLI applications (single-threaded, infrequent access)
- Initialization-time registration (happens once)
- Read-heavy workloads (registry lookups have minimal contention)
- Most web applications (component lookup outside request hot-path)

### Future Consideration

For async-native, ultra-high-throughput applications (>10k req/sec with runtime component registration), an `AsyncRegistry` with `asyncio.Lock` could be provided. Currently, this is **not needed** in the provide-io ecosystem.

**Recommendation**: Profile first. Lock contention shows up clearly in async profilers.

---

## Tool Stack Philosophy

### Chosen Stack

provide.foundation is built on a curated set of well-established libraries:

| Tool | Purpose | Why Chosen |
|------|---------|-----------|
| **attrs** | Data classes | Immutability, slots, validation, excellent performance |
| **structlog** | Logging | Structured, composable, mature, extensible |
| **click** | CLI framework | Battle-tested, extensive ecosystem, excellent UX |

### The Trade-off

**Benefit**: A cohesive, well-tested stack with predictable behavior and known performance characteristics.

**Cost**: Strong coupling to these specific tools. Integration with alternatives (Pydantic, loguru, Typer) requires adapter layers.

### Why Strong Opinions?

```python
# With strong opinions - works immediately
from provide.foundation import logger
logger.info("It just works")

# Without opinions - choose your own adventure
# (requires configuration, integration, debugging incompatibilities)
```

**Philosophy**: 80% of users benefit from opinionated defaults. The 20% needing alternatives can use integration patterns or adapter layers.

---

## Global State Pattern

### Current Implementation

Singleton instances for shared infrastructure:

```python
# Global instances
hub = get_hub()
logger = get_logger()
command_registry = get_command_registry()
```

### Why Global State?

**1. Ergonomic API**
```python
# With globals
from provide.foundation import logger
logger.info("Clean and simple")

# Without globals
from provide.foundation import create_logger_from_context
logger = create_logger_from_context(get_current_context())
logger.info("Verbose and repetitive")
```

**2. Shared Infrastructure**
- Logging configuration applies globally
- Component registry accessible from anywhere
- Reduced boilerplate in application code

### The Mitigation

**Problem**: Global state complicates testing.

**Solution**: `provide-testkit` with complete reset capabilities:

```python
import pytest
from provide.testkit import reset_foundation_setup_for_testing

@pytest.fixture(autouse=True)
def reset_foundation():
    """Clean state between tests."""
    reset_foundation_setup_for_testing()
```

**Result**: Tests are isolated despite global state.

### Best Practice

Use dependency injection in **your application layer**:

```python
# Application code - use DI for business logic
class UserService:
    def __init__(self, db_pool, cache, logger):
        self.db = db_pool
        self.cache = cache
        self.log = logger

    async def get_user(self, user_id):
        self.log.info("Fetching user", user_id=user_id)
        return await self.db.fetchone("SELECT * FROM users WHERE id = $1", user_id)

# Foundation layer - global for infrastructure
from provide.foundation import logger
logger.info("Application started")  # Infrastructure logging
```

**Separation**: Global state for infrastructure, DI for business logic.

---

## Intentional Scope Boundaries

### What's Included

| Component | Status | Why |
|-----------|--------|-----|
| Structured Logging | ✅ | Core infrastructure need |
| Configuration | ✅ | Essential for all applications |
| CLI Framework | ✅ | Common pattern, well-defined scope |
| HTTP Client | ✅ | Outbound transport is foundational |
| Error Handling | ✅ | Critical infrastructure concern |
| Crypto Utils | ✅ | Security primitives needed everywhere |

### What's Excluded (By Design)

| Component | Status | Rationale |
|-----------|--------|-----------|
| HTTP Server | ❌ | Use FastAPI/Flask/Django (see [integration patterns](../guide/advanced/integration-patterns.md)) |
| ORM / Database | ❌ | Business logic concern, not infrastructure |
| Message Queue | ❌ | Application-specific, many options exist |
| GraphQL / gRPC | ❌ | Protocol-specific, not foundational |

### Philosophy: Foundation, Not Framework

```
Django/Rails:        Full-stack framework (everything included)
FastAPI:             Web framework (web-specific stack)
provide.foundation:  Foundation layer (infrastructure for anything)
```

**provide.foundation sits below your framework of choice**, providing infrastructure that works with any application type.

### Integration is First-Class

While we don't provide a web server, we provide **excellent integration**:

- FastAPI middleware examples
- Django middleware examples
- Celery signal integration
- Custom adapter protocols

See: [Integration Patterns](../guide/advanced/integration-patterns.md)

---

## CLI Adapter Ecosystem

### Current State

**Included**: `ClickAdapter` (click framework)

**Not included**: Typer, argparse, Cement, etc.

### Why Only Click?

1. **Mature ecosystem**: Click is battle-tested in tools like Flask, pip, AWS CLI
2. **Excellent UX**: Help generation, parameter validation, composability
3. **Well-maintained**: Active development, security updates
4. **Known quantity**: Predictable behavior, extensive documentation

### Extensibility Built-In

The CLI system is **protocol-based**, allowing custom adapters:

```python
from provide.foundation.cli.base import CLIAdapter

class TyperAdapter(CLIAdapter):
    """Custom adapter for Typer framework."""

    def create_command(self, func, **kwargs):
        # Implement Typer command creation
        pass
```

**Current status**: Protocol defined, community adapters welcome.

**Future**: If demand emerges, official Typer/argparse adapters could be added.

---

## Configuration Sources

### Built-In Sources

1. **Environment variables**: `RuntimeConfigLoader`
2. **Files**: YAML, JSON, TOML, .env via `FileConfigLoader`
3. **Runtime**: In-memory dictionaries via `DictConfigLoader`

### Not Built-In (But Extensible)

Cloud secret managers require custom loaders:

- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager

### Why Not Included?

1. **Different deployment models**: Not all apps need cloud secrets
2. **Authentication complexity**: Each service has unique auth flows
3. **Dependency weight**: Avoid pulling in boto3/azure-sdk for all users
4. **Extensibility works**: Users can implement in ~50 lines

### Implementation Examples

Complete examples for Vault, AWS Secrets, and Azure are provided in [Integration Patterns](../guide/advanced/integration-patterns.md#custom-configuration-sources).

**Pattern**:
```python
from provide.foundation.config.loader import ConfigLoader

class VaultConfigLoader(ConfigLoader):
    def load(self, config_class):
        secrets = self.vault_client.read(self.secret_path)
        return config_class.from_dict(secrets)
```

---

## Performance Characteristics

### Where Overhead Exists

1. **Log Processing**: Each log passes through processor chain
2. **Decorators**: `@retry`, `@resilient` add wrapper layers
3. **Registry Lookups**: Dictionary search with lock acquisition

### When It Matters

**Ultra-low latency requirements** (<100μs):
```python
# Every microsecond counts
async def high_frequency_trading():
    # Logging overhead may be measurable
    logger.debug("Trade executed", price=100.50)  # ~10μs overhead
```

**High-throughput logging** (>100k msg/sec):
- Processor chains become bottleneck
- Consider: Async logging, sampling, batching

### When It Doesn't Matter

**Typical web applications** (99% of use cases):
- Request processing: milliseconds to seconds
- Logging overhead: microseconds
- **Ratio**: 0.001% - 0.1% of request time

### Measurement Tools

Built-in profiling:
```python
from provide.foundation.profiling import profile

with profile("database_query"):
    results = await db.query("SELECT ...")
# Logs: "database_query completed duration_ms=42.3"
```

**Recommendation**: Measure, don't guess. Premature optimization is the root of all evil.

---

## Summary

### Core Principles

1. **Strong opinions**: Curated stack for 80% use case
2. **Extensibility**: Protocols and examples for the other 20%
3. **Foundation layer**: Not a framework, works with any framework
4. **Transparency**: Trade-offs documented, not hidden

### Decision Framework

When evaluating provide.foundation:

1. ✅ **Align with tool choices?** (attrs, structlog, click)
2. ✅ **Foundation layer sufficient?** (not needing full-stack)
3. ✅ **Acceptable trade-offs?** (global state, thread locks, included CLI adapter)
4. ✅ **Integration path clear?** (web framework, database, cloud secrets)

If all ✅, provide.foundation is an excellent fit.

If some ❌, see [When to Use](../guide/when-to-use.md) for alternatives.

---

## Related Documentation

- [Limitations & Trade-offs](limitations.md) - Honest assessment of current limitations
- [Integration Patterns](../guide/advanced/integration-patterns.md) - FastAPI, Django, Vault examples
- [When to Use](../guide/when-to-use.md) - Decision guide for adoption
- [Performance Specifications](performance.md) - Benchmarks and optimization guidance
