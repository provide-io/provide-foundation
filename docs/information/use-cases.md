# Use Cases

provide.foundation is designed as a foundation layer for building production-focused Python applications. This page explains when to use it and what kinds of applications it's best suited for.

## When to Use provide.foundation

### Excellent Fit

These application types are ideally suited for provide.foundation:

#### CLI Applications and Developer Tools
Perfect for command-line tools that need structured logging, configuration management, and beautiful console output.

**Why it fits:**
- Declarative CLI framework with `@register_command`
- Rich console output with colors and formatting
- Zero-configuration logging that just works
- Component registry for managing resources

**Examples:**
- Development tools (code generators, project scaffolders)
- DevOps utilities (deployment scripts, infrastructure tools)
- Data processing command-line tools
- Build and automation tools

**See:** [CLI Application Tutorial](../getting-started/first-app.md)

#### Microservices with Structured Logging
Services that need production-focused logging and observability.

**Why it fits:**
- Structured logging ready for log aggregation
- OpenTelemetry integration for distributed tracing
- Metrics collection and reporting
- Environment-based configuration

**Examples:**
- REST API backend services (with FastAPI/Flask)
- gRPC services
- Message queue consumers
- Background job processors

#### Data Processing Pipelines
Batch and streaming data processing applications.

**Why it fits:**
- Resilience patterns (retry, circuit breaker)
- Progress tracking and logging
- File operations with safety guarantees
- Archive and serialization utilities

**Examples:**
- ETL pipelines
- Data transformation jobs
- Log processing systems
- Report generators

#### Background Task Processors
Long-running workers that process async tasks.

**Why it fits:**
- Structured logging for debugging
- Error handling with automatic retries
- Metrics and health monitoring
- Clean shutdown handling

**Examples:**
- Celery workers
- RQ job processors
- Scheduled task runners
- Email/notification senders

### Good Fit (With Awareness)

These use cases work well but require understanding of the architecture:

#### Web APIs
Use for logging, configuration, and resilience - NOT as a web framework.

**Integration Pattern:**
```python
# Use FastAPI/Flask for HTTP, Foundation for logging
from fastapi import FastAPI
from provide.foundation import logger, get_hub
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

app = FastAPI()

# Initialize Foundation
config = TelemetryConfig(
    service_name="my-api",
    logging=LoggingConfig(default_level="INFO")
)
get_hub().initialize_foundation(config)

@app.get("/users")
async def get_users():
    logger.info("users_fetch_started")
    # ... your logic ...
    logger.info("users_fetch_completed", count=len(users))
    return users
```

#### Task Queue Systems
Great for worker logging, less ideal if using async-heavy task queues.

**Consideration:** Registry uses threading locks, not async locks. For ultra-high-throughput async workers (>10k tasks/sec), consider this trade-off.

#### Libraries Needing Structured Logging
Libraries can use Foundation's logging, but should allow users to configure it.

**Pattern:**
```python
# In your library
from provide.foundation import logger

def process_data(data):
    logger.debug("library_processing", data_size=len(data))
    # ... processing ...
```

### Consider Alternatives

These scenarios might be better served by other tools:

#### Ultra-Low Latency Systems
If you need <100μs latencies, Foundation's structured logging overhead may be too high.

**Alternative:** Use Python's standard `logging` module with minimal formatting, or consider lower-level languages.

#### Full-Stack Framework Needs
If you need batteries-included web framework with ORM, auth, and templates.

**Alternative:** Use Django or Rails instead. Foundation is explicitly NOT a full-stack framework.

#### Tool Stack Incompatibility
If your project is standardized on Pydantic-only or loguru-only stacks.

**Trade-off:** Foundation uses attrs and structlog for consistency. Mixing tool stacks adds complexity.

## Real-World Application Examples

### Example 1: Developer CLI Tool

A CLI tool for managing cloud infrastructure:

```python
from provide.foundation import logger, pout, get_hub
from provide.foundation.hub import register_command
from provide.foundation.resilience import retry

@register_command("deploy")
def deploy(environment: str, version: str):
    """Deploy application to cloud environment."""
    logger.info("deployment_started", env=environment, version=version)
    pout(f"🚀 Deploying version {version} to {environment}...")

    deploy_to_cloud(environment, version)

    logger.info("deployment_completed", env=environment)
    pout("✅ Deployment successful!", color="green")

if __name__ == "__main__":
    cli = get_hub().create_cli(name="cloud-deploy")
    cli()
```

### Example 2: Microservice with FastAPI

An API service with structured logging:

```python
from fastapi import FastAPI
from provide.foundation import logger, get_hub
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Initialize Foundation
get_hub().initialize_foundation(
    TelemetryConfig(
        service_name="user-api",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",  # JSON for production
        ),
    )
)

app = FastAPI()

@app.get("/health")
async def health():
    logger.debug("health_check")
    return {"status": "healthy"}
```

### Example 3: Data Pipeline

A data processing pipeline with resilience:

```python
from provide.foundation import logger
from provide.foundation.resilience import retry
from provide.foundation.errors import NetworkError

@retry(max_attempts=3, exceptions=(NetworkError,))
def fetch_data_from_api(endpoint: str):
    """Fetch data with automatic retry on network errors."""
    logger.info("api_fetch_started", endpoint=endpoint)

    try:
        data = call_api(endpoint)
        logger.info("api_fetch_completed", records=len(data))
        return data
    except Exception as e:
        logger.error("api_fetch_failed", endpoint=endpoint, error=str(e))
        raise NetworkError(f"Failed to fetch from {endpoint}")

def process_pipeline():
    data = fetch_data_from_api("/v1/users")
    # ... process data ...
    logger.info("pipeline_completed", records_processed=len(data))
```

## Architecture Considerations

### Threading vs Async
Foundation's registry uses threading locks (`threading.RLock`), not async locks.

**Impact:**
- **Negligible** for CLI apps, initialization-time registration
- **Low** for read-heavy workloads (command lookup)
- **Consider** for high-throughput async services with runtime registration in hot paths

### Global State Pattern
Foundation uses singleton patterns (`get_hub()`, `logger`) for ergonomic APIs.

**Mitigation:** Use `provide-testkit`'s `reset_foundation_setup_for_testing()` for clean test isolation.

### Intentional Scope
Foundation provides logging, CLI, configuration. It does NOT provide:
- Web frameworks (use FastAPI/Flask/Django)
- Databases or ORMs (use SQLAlchemy/Django ORM)
- Authentication systems (use libraries specific to your framework)
- Template engines (use Jinja2/etc.)

---

**Next Steps:**
- Review [Features](features.md) for complete capabilities
- Check [Architecture](../explanation/architecture.md) for design decisions
- Start building with [Quick Start](../getting-started/quick-start.md)
