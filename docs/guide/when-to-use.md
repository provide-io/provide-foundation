# When to Use provide.foundation

This guide helps teams evaluate whether provide.foundation is a good fit for their project.

---

## Executive Summary

**Use provide.foundation when you want:**
- 🎯 Beautiful, structured logging with emoji-enhanced visual parsing
- 🛠️ Framework-agnostic CLI tooling with consistent patterns
- ⚙️ Type-safe configuration management across multiple sources
- 🧩 Composable telemetry for observability pipelines

**Consider alternatives when you need:**
- Ultra-low latency requirements (<100μs)
- Pure async-native, high-throughput web frameworks
- Full-stack framework (Django, Rails, etc.)
- Tool stack incompatibility (Pydantic-only, loguru-only projects)

---

## ✅ Excellent Fit

### CLI Applications & Developer Tools

provide.foundation **excels** in command-line applications:

```python
from provide.foundation.hub import Hub

hub = Hub()
hub.initialize_foundation()

# Framework-agnostic CLI with beautiful logging
cli = hub.create_cli()
cli()
```

**Why it's a great fit:**
- Emoji-enhanced logs make output scannable in terminal UIs
- Domain-Action-Status patterns provide consistent structure
- Hub pattern enables plugin architectures
- No async complexity for typical CLI workflows

**Examples:**
- DevOps tooling (deployment scripts, infrastructure automation)
- Code generators and scaffolding tools
- Data migration utilities
- Build and CI/CD tools

### Microservices with Structured Logging

For microservices prioritizing observability:

```python
from provide.foundation import logger, get_hub

hub = get_hub()
hub.initialize_foundation(
    telemetry_config={
        "log_level": "INFO",
        "format": "json",  # For log aggregation
    }
)

# Structured logging with semantic context
logger.info("user.created", user_id=user.id, cohort="premium")
logger.bind(request_id=req_id).info("api.request", method="POST")
```

**Why it's a great fit:**
- JSON output integrates with ELK, Loki, DataDog
- Structured logs enable powerful querying
- Emoji mode for local dev, JSON for production
- Low overhead (>14k msg/sec throughput)

**Examples:**
- REST APIs (FastAPI + foundation)
- gRPC services
- Message queue workers (Celery, RQ)
- Background job processors

### Data Processing Pipelines

For ETL and data transformation workflows:

```python
from provide.foundation import logger

# Rich contextual logging for data pipelines
logger.info("pipeline.started", source="s3://bucket", rows=1_000_000)
logger.info("transform.applied", operation="dedupe", rows_removed=1234)
logger.warn("validation.failed", invalid_rows=56, error_rate=0.0056)
```

**Why it's a great fit:**
- Domain-specific emoji sets (DATA, ETL, ML)
- Structured context tracking across pipeline stages
- Performance profiling built-in
- Thread-safe for parallel processing

**Examples:**
- Apache Airflow tasks
- Spark/Pandas transformations
- ML training pipelines
- Data validation frameworks

---

## ✅ Good Fit (With Awareness)

### Web APIs (FastAPI, Flask, Django)

provide.foundation works well for **logging and configuration**, but does not provide web framework features:

```python
from fastapi import FastAPI
from provide.foundation import logger, get_hub

app = FastAPI()
hub = get_hub()
hub.initialize_foundation()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    logger.info("user.fetch", user_id=user_id)
    # Use foundation for logging, FastAPI for HTTP
    return {"id": user_id}
```

**What to know:**
- ✅ Use foundation for: Structured logging, configuration management
- ❌ Foundation does NOT provide: HTTP servers, routing, request handling
- ⚠️ Registry lock: Negligible impact unless runtime registration in hot path (>10k req/sec)


### Task Processors & Background Workers

For Celery, RQ, or custom worker pools:

```python
from celery import Celery
from provide.foundation import logger

app = Celery("tasks")

@app.task
def process_order(order_id: int):
    logger.info("order.processing", order_id=order_id)
    # Foundation provides structured logging
    # Celery handles task distribution
```

**What to know:**
- ✅ Foundation provides: Context-aware logging, configuration
- ❌ Foundation does NOT provide: Task queues, distributed scheduling
- ⚠️ Thread safety: RLock works fine for worker processes

### Library Development

For libraries needing structured logging without forcing structlog on users:

```python
from provide.foundation import logger

def my_library_function(data: dict):
    # Library uses foundation internally
    logger.debug("lib.processing", keys=len(data))
    return process(data)
```

**What to know:**
- ✅ Foundation provides: No-op logging when not initialized, lazy setup
- ❌ Consideration: Adds dependency on provide.foundation
- 💡 Alternative: Consider using standard library `logging` for public libraries

---

## ⚠️ Consider Alternatives

### Ultra-Low Latency Systems

**Don't use foundation if:**
- Sub-100μs latency requirements
- High-frequency trading systems
- Real-time audio/video processing
- Kernel-space or embedded systems

**Why:**
- Processor chains add overhead (~1-5μs per log call)
- Registry lookups (even read-only) have cost
- Emoji rendering (even disabled) has minimal parsing cost

**Alternative:** Use bare `logging.Logger` or custom zero-allocation logging.

### Pure Async-Native, High-Throughput Web

**Consider alternatives if:**
- Async-only architecture (no sync code)
- >10k req/sec with runtime component registration
- Hot-path registry access in every request

**Why:**
- Registry uses `threading.RLock` (not `asyncio.Lock`)
- Potential for lock contention in extreme async scenarios

**Mitigation:** Use read-heavy patterns, initialize at startup, profile before optimizing.

### Pydantic-Only / Typer-Only Projects

**Foundation may not fit if:**
- Project mandates Pydantic for all data classes
- CLI must use Typer (not Click)
- Team has standardized on loguru

**Why:**
- Foundation uses `attrs` (not Pydantic)
- Built-in CLI adapter is Click (Typer adapter would need custom implementation)
- Foundation uses `structlog` (not loguru)

**Compatibility:**
- ✅ Foundation and Pydantic can coexist (but duplicated data validation)
- ❌ Foundation and loguru should not be mixed (conflicting logging systems)

### Full-Stack Framework Needs

**Use Django/Rails/Laravel if:**
- Need ORM, admin interface, auth system, templates
- Want "batteries included" full-stack solution
- Building traditional web applications

**Why:**
- Foundation is a **foundation layer**, not full-stack framework
- Provides: Logging, configuration, CLI patterns
- Does NOT provide: Web frameworks, databases, auth, templates

**Integration:** You can use foundation **within** Django for structured logging:
```python
# Django + Foundation for logging
from provide.foundation import logger

def my_view(request):
    logger.info("view.rendered", user_id=request.user.id)
    return render(request, "template.html")
```

---

## Decision Matrix

| Use Case | Fit Level | Notes |
|----------|-----------|-------|
| **CLI Applications** | ✅ Excellent | Primary use case, full feature set |
| **Microservices (logging)** | ✅ Excellent | JSON output, structured logs |
| **Data Pipelines** | ✅ Excellent | Rich context tracking |
| **FastAPI/Flask APIs** | ✅ Good | Use for logging, not HTTP |
| **Celery Workers** | ✅ Good | Structured task logging |
| **Library Development** | ✅ Good | Consider dependency impact |
| **High-throughput async web** | ⚠️ Profile first | Check registry lock contention |
| **Ultra-low latency (<100μs)** | ❌ No | Overhead too high |
| **Pydantic-only projects** | ⚠️ Mixed | attrs/Pydantic duplication |
| **Full-stack web framework** | ❌ No | Use Django/Rails instead |

---

## Questions to Ask

### 1. What problem am I solving?

- **Structured logging?** ✅ Foundation excels
- **Configuration management?** ✅ Foundation provides
- **Web framework?** ❌ Use FastAPI/Flask/Django
- **Database ORM?** ❌ Use SQLAlchemy/Django ORM

### 2. What are my performance requirements?

- **CLI or background tasks?** ✅ Overhead negligible
- **<10ms API latency target?** ✅ Foundation adds <1ms
- **<100μs latency target?** ❌ Too much overhead

### 3. What's my existing stack?

- **attrs + structlog + Click?** ✅ Perfect match
- **Pydantic + Typer + loguru?** ⚠️ Friction likely
- **Mixed stack?** ✅ Foundation can coexist

### 4. What's my scale?

- **Hundreds of requests/sec?** ✅ No problem
- **10k+ req/sec with hot-path registry?** ⚠️ Profile first
- **100k+ msg/sec logging?** ⚠️ Disable emoji, use JSON

---

## Next Steps

### ✅ If Foundation Fits

1. Read: [Quick Start Guide](../index.md)
2. Try: [Example Projects](../../examples/index.md)

### ⚠️ If You're Unsure

1. Read: [Design Decisions](../../architecture/design-decisions.md) - Understand the philosophy
2. Read: [Limitations](../../architecture/limitations.md) - Know the trade-offs
3. Prototype: Build a small proof-of-concept
4. Profile: Measure actual overhead in your use case

### ❌ If Foundation Doesn't Fit

**For ultra-low latency:**
- Standard library `logging` with custom handlers
- Zero-allocation logging (C extensions)

**For full-stack web:**
- Django (full-featured, batteries included)
- Ruby on Rails, Laravel

**For Pydantic-centric projects:**
- Build configuration with `pydantic-settings`
- Use `loguru` or `structlog` directly

---

## Summary

provide.foundation is designed for **CLI applications, microservices, and data pipelines** that value structured logging and composable telemetry. It's a **foundation layer**, not a full-stack framework.

**Use it when** you want beautiful, structured logs and framework-agnostic patterns.

**Consider alternatives when** you need ultra-low latency, full-stack features, or have incompatible tool requirements.

**Key insight:** Most teams overthink this. If you're building a CLI tool or need better logging, just try it. If you need Django's admin interface or <100μs latency, use the right tool for that job.
