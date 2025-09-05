# Examples Gallery

Quick, copy-paste examples for common provide.foundation use cases.

## Logging Examples

### Basic Structured Logging

```python
from provide.foundation import logger

# Simple logging with context
logger.info("user_login", 
            user_id="user-123",
            ip="192.168.1.1",
            success=True)

# With error context
try:
    process_data()
except Exception as e:
    logger.exception("processing_failed",
                    error=str(e),
                    data_size=1024)
```

### Contextual Logging

```python
from provide.foundation import logger

# Bind context for all subsequent logs
with logger.bind(request_id="req-456", user_id="user-123"):
    logger.info("request_started")
    process_request()
    logger.info("request_completed")
    # All logs include request_id and user_id
```

### Async Logging

```python
import asyncio
from provide.foundation import logger

async def async_operation():
    async with logger.bind(operation="async_task"):
        logger.info("task_started")
        await asyncio.sleep(1)
        logger.info("task_completed")

asyncio.run(async_operation())
```

## CLI Examples

### Simple Command

```python
from provide.foundation.cli import register_command, run_cli

@register_command("greet")
def greet(name: str = "World", excited: bool = False):
    """Greet someone."""
    greeting = f"Hello, {name}{'!' if excited else '.'}"
    print(greeting)

if __name__ == "__main__":
    run_cli()
```

### Nested Commands

```python
from provide.foundation.cli import register_command, run_cli

@register_command("db.migrate")
def migrate():
    """Run database migrations."""
    print("Running migrations...")

@register_command("db.seed")
def seed(count: int = 10):
    """Seed the database."""
    print(f"Seeding {count} records...")

@register_command("db.reset")
def reset():
    """Reset the database."""
    print("Resetting database...")

# Usage: ./app.py db.migrate
```

### Command with JSON Output

```python
import json
from provide.foundation.cli import register_command

@register_command("info")
def info(format: str = "text"):
    """Show system information."""
    data = {
        "version": "1.0.0",
        "status": "healthy",
        "uptime": 3600
    }
    
    if format == "json":
        print(json.dumps(data, indent=2))
    else:
        for key, value in data.items():
            print(f"{key}: {value}")
```

## Configuration Examples

### Environment Variables

```python
import os
from provide.foundation.config import TelemetryConfig

# Set environment variables
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"
os.environ["PROVIDE_LOG_FORMAT"] = "json"

# Load configuration
config = TelemetryConfig.from_env()
print(f"Log level: {config.level}")
print(f"Format: {config.format}")
```

### Configuration File

```python
from provide.foundation.config import Config

# config.yaml:
# database:
#   host: localhost
#   port: 5432
#   name: myapp

config = Config.from_file("config.yaml")
db_host = config.get("database.host")
db_port = config.get("database.port", 5432)
```

### Runtime Configuration

```python
from provide.foundation.logger import setup_logging

# Change configuration at runtime
setup_logging(
    level="DEBUG",
    format="json",
    processors=["timestamp", "level", "message"]
)
```

## Semantic Layer Examples

### HTTP Request Logging

```python
from provide.foundation.emoji_sets import HTTPLayer
import time

http = HTTPLayer()

# Log request lifecycle
start = time.time()
http.request_started(method="GET", path="/api/users")

# Simulate processing
time.sleep(0.1)

# Log completion
duration_ms = (time.time() - start) * 1000
http.request_completed(status=200, duration_ms=duration_ms)
```

### Database Query Logging

```python
from provide.foundation.emoji_sets import DatabaseLayer

db = DatabaseLayer()

# Log query execution
db.query_started(query="SELECT * FROM users", database="main")
# ... execute query ...
db.query_completed(rows_affected=42, duration_ms=15.3)

# Log transaction
db.transaction_started()
# ... perform operations ...
db.transaction_committed()
```

### Custom Emoji Set

```python
from provide.foundation.emoji_sets import EmojiSetConfig, register_layer

@register_layer("cache")
class CacheLayer(EmojiSetConfig):
    domain = "cache"
    
    def get(self, key: str, hit: bool, **kwargs):
        status = "hit" if hit else "miss"
        self.logger.info(f"cache_get_{status}", key=key, **kwargs)
    
    def set(self, key: str, ttl: int, **kwargs):
        self.logger.info("cache_set", key=key, ttl=ttl, **kwargs)

# Use it
cache = CacheLayer()
cache.get(key="user:123", hit=True)
cache.set(key="user:123", ttl=3600)
```

## Error Handling Examples

### Error Boundaries

```python
from provide.foundation.errors import with_error_boundary
from provide.foundation import logger

@with_error_boundary(fallback="default_value")
def risky_operation():
    """Operation that might fail."""
    if random.random() > 0.5:
        raise ValueError("Random failure")
    return "success"

result = risky_operation()  # Returns "default_value" on error
```

### Retry Logic

```python
from provide.foundation.errors import retry
from provide.foundation import logger

@retry(max_attempts=3, backoff=2.0)
def flaky_api_call():
    """API call that might fail."""
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
    return response.json()

data = flaky_api_call()  # Retries up to 3 times
```

## Platform Detection Examples

```python
from provide.foundation.platform import get_system_info

info = get_system_info()
print(f"OS: {info.platform}")  # "darwin", "linux", "windows"
print(f"Architecture: {info.arch}")  # "arm64", "x86_64"
print(f"Python: {info.python_version}")
print(f"Hostname: {info.hostname}")

# Conditional logic based on platform
if info.platform == "darwin":
    # macOS specific code
    pass
elif info.platform == "linux":
    # Linux specific code
    pass
```

## Process Execution Examples

```python
from provide.foundation.process import run_command

# Simple command
result = run_command(["ls", "-la"])
if result.returncode == 0:
    print(result.stdout)
else:
    print(f"Error: {result.stderr}")

# With timeout
result = run_command(["slow_command"], timeout=5.0)

# With environment variables
result = run_command(
    ["npm", "run", "build"],
    env={"NODE_ENV": "production"}
)
```

## Console Output Examples

```python
from provide.foundation import pout, perr

# Standard output with emoji
pout("✅ Operation successful")
pout("📊 Processing 1000 records...")
pout("🎉 All tests passed!")

# Error output
perr("❌ Connection failed")
perr("⚠️ Warning: Low memory")
perr("🔥 Critical error detected")

# Conditional output
if success:
    pout("✅ Task completed")
else:
    perr("❌ Task failed")
```

## Complete Application Template

```python
#!/usr/bin/env python3
"""
Application template using provide.foundation
"""

from provide.foundation import logger, pout, perr
from provide.foundation.cli import register_command, run_cli
from provide.foundation.config import Config
from provide.foundation.platform import get_system_info

# Initialize
logger.info("app_started", 
            platform=get_system_info().platform,
            version="1.0.0")

# Load config
config = Config.from_env()

@register_command("run")
def run_app(debug: bool = False):
    """Run the application."""
    if debug:
        logger.set_level("DEBUG")
    
    try:
        pout("🚀 Starting application...")
        logger.info("app_run_started", debug=debug)
        
        # Your application logic here
        
        pout("✅ Application completed successfully")
        logger.info("app_run_completed")
        return 0
        
    except Exception as e:
        perr(f"❌ Application failed: {e}")
        logger.exception("app_run_failed", error=str(e))
        return 1

if __name__ == "__main__":
    run_cli()
```

## Testing Examples

```python
import pytest
from provide.foundation import logger
from provide.foundation.cli import get_command

def test_logging():
    """Test structured logging."""
    with logger.capture() as logs:
        logger.info("test_event", value=42)
    
    assert len(logs) == 1
    assert logs[0]["event"] == "test_event"
    assert logs[0]["value"] == 42

def test_cli_command():
    """Test CLI command registration."""
    command = get_command("mycommand")
    assert command is not None
    result = command(arg1="value")
    assert result == 0
```

## Next Steps

- Explore the [User Guide](../guide/index.md) for in-depth coverage
- Check the [API Reference](../api/index.md) for complete documentation
- Browse the [Cookbook](../cookbook/index.md) for advanced patterns