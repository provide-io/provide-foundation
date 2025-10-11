# Limitations & Trade-offs

This document provides an honest assessment of provide.foundation's current limitations. Understanding these helps teams make informed decisions and plan appropriate mitigations.

---

## Async Context Considerations

### The Limitation

The Registry uses `threading.RLock`, which **can** block the event loop in specific scenarios.

**Affected operations:**
- `registry.get()` - Component lookup
- `registry.register()` - Component registration
- `registry.list_dimension()` - Listing components

### When This Is a Problem

**Scenario**: High-frequency registry access in async request hot-paths

```python
# ❌ Problematic pattern
async def handle_request(request):
    # This runs 10,000+ times per second
    hub = get_hub()

    # Registry lookup in hot-path with threading lock
    handler = hub.get_component(f"handler_{request.type}")

    return await handler.process(request)
```

**Symptoms**:
- Event loop blocking
- Reduced throughput under load
- Increased P99 latency

### How to Detect

Profile with async-aware tools:

```python
import cProfile
import pstats

# Profile your async application
cProfile.run('asyncio.run(main())', 'profile.stats')

# Analyze
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative')
p.print_stats('registry')  # Look for registry bottlenecks
```

**Look for**: `threading.RLock.acquire` appearing in hot-path traces

### Workarounds

**1. Cache component references** (Recommended)
```python
# ✅ Resolve components once at startup
class RequestHandler:
    def __init__(self, hub):
        # One-time registry lookup
        self.handlers = {
            "type_a": hub.get_component("handler_a"),
            "type_b": hub.get_component("handler_b"),
        }

    async def handle(self, request):
        # No registry lookup in hot-path
        handler = self.handlers[request.type]
        return await handler.process(request)
```

**2. Dependency injection**
```python
# ✅ Pass components explicitly
async def create_app():
    hub = get_hub()

    # Resolve dependencies at startup
    db = hub.get_component("database")
    cache = hub.get_component("cache")

    # Inject into application
    app = FastAPI()
    app.state.db = db
    app.state.cache = cache

    return app
```

**3. Local registries for hot-path** (Advanced)
```python
# ✅ Create request-scoped registry without global lock
class RequestContext:
    def __init__(self):
        self._local_components = {}  # No locking needed

    def get_component(self, name):
        return self._local_components[name]
```

### Future Solution

An `AsyncRegistry` with `asyncio.Lock` could be provided for async-native applications. This is **not currently needed** in the provide-io ecosystem.

**Tracking**: Consider opening an issue if you encounter this limitation in production.

---

## CLI Adapter Ecosystem

### The Limitation

**Included**: `ClickAdapter` only

**Not Included**: Typer, argparse, Cement, Fire, etc.

### Why This Matters

If your team prefers a different CLI framework:

```python
# ❌ Not available out-of-the-box
from provide.foundation.cli import TyperAdapter  # Does not exist

# ✅ Current solution: Use click or create adapter
from provide.foundation.cli import ClickAdapter
```

### Creating Custom Adapters

The protocol-based design allows custom adapters:

```python
from provide.foundation.cli.base import CLIAdapter
import typer

class TyperAdapter(CLIAdapter):
    """Adapter for Typer framework."""

    def create_command(self, func, **kwargs):
        """Convert foundation command to Typer command."""
        return typer.Typer.command(func, **kwargs)

    def create_group(self, name, **kwargs):
        """Create Typer command group."""
        return typer.Typer(name=name, **kwargs)
```

### Request Community Adapter

If you create an adapter that would benefit others:

1. Open a PR to add it to `provide.foundation.cli.adapters`
2. Or publish as separate package: `provide-cli-typer`

**Current status**: Community contributions welcome.

---

## Configuration Sources

### The Limitation

**Built-in**:
- ✅ File-based (YAML, JSON, TOML, .env)
- ✅ Environment variables
- ✅ Runtime dictionaries

**Not Built-in**:
- ❌ HashiCorp Vault
- ❌ AWS Secrets Manager
- ❌ Azure Key Vault
- ❌ Google Secret Manager
- ❌ Kubernetes ConfigMaps/Secrets
- ❌ Consul KV

### Why This Matters

Modern cloud-native applications often use cloud secret managers:

```python
# ❌ Not available out-of-the-box
from provide.foundation.config import VaultConfigLoader  # Does not exist

# ✅ Current solution: Implement custom loader
from provide.foundation.config.loader import ConfigLoader
```

### Implementing Custom Loaders

The `ConfigLoader` protocol makes this straightforward:

**HashiCorp Vault Example:**
```python
import hvac
from provide.foundation.config.loader import ConfigLoader

class VaultConfigLoader(ConfigLoader):
    def __init__(self, vault_url: str, token: str, secret_path: str):
        self.client = hvac.Client(url=vault_url, token=token)
        self.secret_path = secret_path

    def exists(self) -> bool:
        try:
            self.client.secrets.kv.v2.read_secret_version(path=self.secret_path)
            return True
        except:
            return False

    def load(self, config_class):
        response = self.client.secrets.kv.v2.read_secret_version(
            path=self.secret_path
        )
        secrets = response['data']['data']
        return config_class.from_dict(secrets)

# Usage
vault_loader = VaultConfigLoader(
    vault_url="https://vault.example.com",
    token=os.environ["VAULT_TOKEN"],
    secret_path="secret/myapp/config"
)

config = vault_loader.load(DatabaseConfig)
```

**AWS Secrets Manager Example:**
```python
import boto3
import json
from provide.foundation.config.loader import ConfigLoader

class AWSSecretsLoader(ConfigLoader):
    def __init__(self, secret_name: str, region: str = "us-east-1"):
        self.client = boto3.client('secretsmanager', region_name=region)
        self.secret_name = secret_name

    def exists(self) -> bool:
        try:
            self.client.describe_secret(SecretId=self.secret_name)
            return True
        except:
            return False

    def load(self, config_class):
        response = self.client.get_secret_value(SecretId=self.secret_name)
        secrets = json.loads(response['SecretString'])
        return config_class.from_dict(secrets)

# Usage
aws_loader = AWSSecretsLoader(secret_name="myapp/production/config")
config = aws_loader.load(AppConfig)
```

**Azure Key Vault Example:**
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from provide.foundation.config.loader import ConfigLoader

class AzureKeyVaultLoader(ConfigLoader):
    def __init__(self, vault_url: str):
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=credential)
        self.vault_url = vault_url

    def exists(self) -> bool:
        try:
            # Check if vault is accessible
            list(self.client.list_properties_of_secrets(max_page_size=1))
            return True
        except:
            return False

    def load(self, config_class):
        secrets = {}
        for secret in self.client.list_properties_of_secrets():
            retrieved_secret = self.client.get_secret(secret.name)
            secrets[secret.name] = retrieved_secret.value

        return config_class.from_dict(secrets)

# Usage
azure_loader = AzureKeyVaultLoader(
    vault_url="https://mykeyvault.vault.azure.net/"
)
config = azure_loader.load(AppConfig)
```

### Multi-Source Loading

Combine multiple loaders with precedence:

```python
from provide.foundation.config.loader import MultiSourceLoader

loader = MultiSourceLoader(
    FileConfigLoader("config.yaml"),           # Base config
    VaultConfigLoader(...),                    # Secrets from Vault
    RuntimeConfigLoader(prefix="MYAPP_"),      # Env overrides
)

config = loader.load(AppConfig)  # Merged with precedence
```

**Pattern**: File → Cloud Secrets → Environment (highest precedence)

### Request Built-In Support

If cloud secret manager support would benefit the community:

1. Open an issue describing your use case
2. Contribute an implementation as a PR
3. Or publish as separate package: `provide-config-vault`

**Current status**: Implementations expected from users (examples provided).

---

## Performance Characteristics

### The Limitation

Abstraction layers add overhead:

| Operation | Overhead | Impact |
|-----------|----------|--------|
| Log message processing | ~10-50μs | Processor chain execution |
| Decorator wrapping | ~5-20μs | Function call overhead |
| Registry lookup | ~1-5μs | Dictionary + lock |
| HTTP middleware | ~50-200μs | Request/response processing |

### When This Matters

**Ultra-low latency systems** (<100μs requirements):

```python
# ❌ Every microsecond counts
async def high_frequency_trading():
    start = time.perf_counter()

    logger.debug("Trade executed", price=100.50)  # ~15μs overhead

    elapsed = time.perf_counter() - start
    # Target: <10μs total, Actual: 15μs (logging alone)
```

**High-throughput logging** (>100k msg/sec):

```python
# ❌ Processor chain becomes bottleneck
for i in range(1_000_000):
    logger.info("Event", id=i)  # 100k/sec → 10μs per log → CPU bound
```

### Profiling Guidance

**1. Identify hot paths**
```python
import cProfile

cProfile.run('main()', 'profile.stats')

# Analyze
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative')
p.print_stats(20)  # Top 20 functions
```

**2. Measure logging overhead**
```python
import time

# With logging
start = time.perf_counter()
for _ in range(10000):
    logger.info("test", value=42)
with_logging = time.perf_counter() - start

# Without logging (commented out)
# ...measure...

overhead_pct = (with_logging - without_logging) / without_logging * 100
print(f"Logging overhead: {overhead_pct:.1f}%")
```

**3. Use built-in profiling**
```python
from provide.foundation.profiling import profile, get_metrics

with profile("critical_operation"):
    result = expensive_function()

metrics = get_metrics()
print(f"Duration: {metrics['critical_operation']['duration_ms']}ms")
```

### Optimization Strategies

**1. Selective logging** (Recommended)
```python
# ✅ Log less in hot paths
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Detailed state", expensive_to_compute=get_state())
```

**2. Async logging** (Advanced)
```python
# ✅ Non-blocking log queue
from provide.foundation.logger.config import LoggingConfig

config = LoggingConfig(
    async_mode=True,  # Queue logs, process in background
    queue_size=10000
)
```

**3. Sampling** (High-throughput)
```python
# ✅ Log 1% of requests
import random

if random.random() < 0.01:  # 1% sampling
    logger.info("Request processed", request_id=req_id)
```

**4. Conditional features**
```python
# ✅ Disable heavy features in production
config = LoggingConfig(
    emoji_enabled=False,  # Faster in production
    module_levels={"": "WARNING"}  # Reduce log volume
)
```

### Benchmarking Your Application

```python
# Establish baseline
from provide.foundation.profiling import benchmark

@benchmark(iterations=1000)
async def my_endpoint():
    # Your application logic
    pass

# Output: "Benchmark: avg=142μs, p50=130μs, p99=890μs"
```

**Target**: Logging should be <1% of total request time for most applications.

---

## Web Framework Integration

### The Limitation

**Not included**:
- HTTP server implementation
- Web framework (FastAPI/Flask/Django)
- ASGI/WSGI support

**Rationale**: provide.foundation is infrastructure, not a web framework.

### Integration Required

To use with web applications, you **must integrate** yourself:

```python
# ❌ Does not exist
from provide.foundation.web import create_app

# ✅ Integrate with your framework
from fastapi import FastAPI
from provide.foundation import setup_telemetry, logger

setup_telemetry()
app = FastAPI()

@app.get("/")
async def root():
    logger.info("Request received")
    return {"status": "ok"}
```

### Full Integration Examples

See [Integration Patterns](../guide/advanced/integration-patterns.md) for complete examples:

- FastAPI middleware for logging
- Django middleware integration
- Celery signal handlers
- Custom framework integration

**Effort**: ~50-100 lines for comprehensive integration.

---

## Summary

### Current Limitations

| Area | Limitation | Workaround | Future |
|------|-----------|------------|--------|
| **Async Registry** | Threading lock in async | Cache components, DI | Consider AsyncRegistry |
| **CLI Adapters** | Click only | Custom adapters (protocol) | Community contributions |
| **Config Sources** | No cloud secrets | Custom loaders (~50 lines) | Community packages |
| **Performance** | Abstraction overhead | Profiling, selective features | Optimization guides |
| **Web Server** | Not included | Use FastAPI/Flask/Django | Integration examples |

### Decision Framework

1. **Measure first**: Profile to confirm limitation affects you
2. **Use workarounds**: Most have simple solutions
3. **Contribute back**: Share useful adapters/loaders
4. **Consider alternatives**: If limitations are blockers

### Getting Help

- **Workaround questions**: Open a GitHub discussion
- **Performance profiling**: See [Performance Guide](performance.md)
- **Custom adapters**: See [Integration Patterns](../guide/advanced/integration-patterns.md)
- **Bug reports**: Open a GitHub issue

---

## Related Documentation

- [Design Decisions](design-decisions.md) - Why these trade-offs were made
- [When to Use](../guide/when-to-use.md) - Is provide.foundation right for you?
- [Integration Patterns](../guide/advanced/integration-patterns.md) - Framework integration examples
- [Performance](performance.md) - Benchmarks and optimization
