# Emoji Sets API

Domain-specific emoji enhancements for structured logging with visual context cues.

## Overview

The Emoji Sets system provides domain-specific visual enhancements to structured logging through contextual emoji prefixes. Different domains (HTTP, Database, LLM, etc.) can have specialized emoji mappings that provide immediate visual context for log entries.

## Available Emoji Sets

- [Base Types](base.md) - Core types and interfaces
- [HTTP Layer](http.md) - Web request and API logging
- [Database Layer](database.md) - Database operations and queries
- [LLM Layer](llm.md) - AI/ML model interactions
- [Task Queue Layer](task_queue.md) - Asynchronous task processing
- [Custom Layers](custom.md) - Creating custom emoji sets

## Quick Start

### Using Built-in Emoji Sets

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry
from provide.foundation import get_logger

# Enable emoji sets in configuration
config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        das_emoji_prefix_enabled=True,
        enabled_emoji_sets=["http", "database", "llm"]
    )
)
setup_telemetry(config)

# Use domain-specific loggers
http_log = get_logger("http")
db_log = get_logger("database") 
llm_log = get_logger("llm")

# Logs will automatically include contextual emojis
http_log.info("request_completed", method="GET", status=200, path="/api/users")
db_log.debug("query_executed", table="users", duration_ms=45)
llm_log.info("model_invoked", model="gpt-4", tokens=150)
```

### Creating Custom Emoji Sets

```python
from provide.foundation.logger.emoji.types import EmojiSetConfig

class KubernetesEmojiSet(EmojiSetConfig):
    """Custom emoji set for Kubernetes operations."""
    
    domain = "k8s"
    
    def get_emoji(self, action: str, status: str) -> str:
        if action.startswith("deploy"):
            return "🚀" if status == "success" else "💥"
        elif action.startswith("scale"):
            return "📏" if status == "success" else "⚠️"
        elif action.startswith("pod"):
            return "📦" if status == "running" else "⏹️"
        else:
            return "⚙️"

# Register custom emoji set
config = TelemetryConfig(
    logging=LoggingConfig(
        custom_emoji_sets=[KubernetesEmojiSet()]
    )
)
setup_telemetry(config)

# Use with custom logger
k8s_log = get_logger("k8s")
k8s_log.info("deploy_success", application="web-app", replicas=3)
```

## Emoji Set Architecture

### Domain-Action-Status Pattern

The emoji system follows a Domain-Action-Status (DAS) pattern where:

- **Domain**: The technology or context area (http, database, llm, k8s)
- **Action**: The operation being performed (request, query, inference, deploy)  
- **Status**: The outcome or state (success, error, pending, completed)

### Visual Enhancement Benefits

- **Rapid Log Scanning**: Emojis provide immediate visual context
- **Domain Recognition**: Quickly identify log sources and types
- **Status Indication**: Visual cues for success/failure states
- **Reduced Cognitive Load**: Less text parsing needed for log analysis

## Configuration Options

### Global Emoji Settings

```python
from provide.foundation.logger.config import LoggingConfig

config = LoggingConfig(
    # Enable/disable emoji prefixes globally
    das_emoji_prefix_enabled=True,
    
    # Enable logger name emoji prefixes  
    logger_name_emoji_prefix_enabled=True,
    
    # Specify which emoji sets to load
    enabled_emoji_sets=["http", "database", "llm"],
    
    # Add custom emoji sets
    custom_emoji_sets=[CustomEmojiSet()],
    
    # Legacy user-defined sets (deprecated)
    user_defined_emoji_sets=[]
)
```

### Per-Logger Configuration

```python
# Different loggers can use different emoji contexts
web_log = get_logger("web.api")      # Uses HTTP emoji set
db_log = get_logger("database.orm")  # Uses Database emoji set
ml_log = get_logger("ml.inference")  # Uses LLM emoji set
```

## Integration Examples

### FastAPI Web Service

```python
from provide.foundation import get_logger

# HTTP-specific logging with emoji context
api_log = get_logger("api")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    api_log.info("request_started", method="GET", path=f"/users/{user_id}")
    
    try:
        user = await user_service.get_user(user_id)
        api_log.info("request_success", user_id=user_id, status=200)
        return user
    except UserNotFound:
        api_log.warning("request_not_found", user_id=user_id, status=404)
        raise HTTPException(404, "User not found")
```

### Database Operations

```python
from provide.foundation import get_logger

# Database-specific logging
db_log = get_logger("database")

class UserRepository:
    async def find_by_id(self, user_id: int):
        db_log.debug("query_started", operation="SELECT", table="users")
        
        try:
            result = await self.db.fetch_one(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            db_log.info("query_success", table="users", rows_affected=1)
            return result
        except Exception as e:
            db_log.error("query_failed", table="users", error=str(e))
            raise
```

## API Reference

::: provide.foundation.logger.emoji.sets

## Related Documentation

- [Emoji System Concepts](../../guide/concepts/emoji-system.md) - Design and architecture
- [Advanced Usage](../../guide/advanced-usage.md) - Custom emoji set development
- [Logger Configuration](../logger/config.md) - Configuration options
- [Testing Guide](../../guide/testing.md) - Testing emoji output