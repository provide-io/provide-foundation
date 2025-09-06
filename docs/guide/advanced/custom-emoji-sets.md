# Custom Emoji Sets

Create domain-specific logging emoji sets for visual log parsing in specialized contexts.

## Creating Domain-Specific Emoji Sets

```python
from provide.foundation.logger.emoji.types import EmojiSetConfig, EmojiSet
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

class KubernetesEmojiSet(EmojiSetConfig):
    """Emoji set for Kubernetes operations."""
    
    domain = "k8s"
    
    def get_emoji(self, action: str, status: str) -> str:
        """Get emoji for Kubernetes operations."""
        if action.startswith("deploy"):
            return "🚀" if status == "success" else "💥"
        elif action.startswith("scale"):
            return "📏" if status == "success" else "⚠️"
        elif action.startswith("rollback"):
            return "⏪" if status == "success" else "🔄"
        elif action.startswith("pod"):
            return "📦" if status == "running" else "⏹️"
        elif action.startswith("service"):
            return "🔗" if status == "ready" else "🔌"
        else:
            return "⚙️"  # Default for unknown k8s operations

# Register and use the custom emoji set
k8s_emoji_set = KubernetesEmojiSet()

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="key_value",
        custom_emoji_sets=[k8s_emoji_set]
    )
)
setup_telemetry(config)

# Usage with domain-specific logger
from provide.foundation import get_logger
k8s_log = get_logger("k8s")

k8s_log.info("deploy_started", application="web-app", namespace="production")
k8s_log.info("deploy_success", application="web-app", replicas=3, namespace="production")
k8s_log.error("pod_failed", pod="web-app-abc123", reason="ImagePullBackOff")
```

## Multi-Domain Emoji Sets

```python
class WebEmojiSet(EmojiSetConfig):
    """Emoji set for web operations."""
    
    domain = "web"
    
    def get_emoji(self, action: str, status: str) -> str:
        if action.startswith("request"):
            if status.startswith("2"):  # 2xx status codes
                return "✅"
            elif status.startswith("4"):  # 4xx status codes
                return "❌"
            elif status.startswith("5"):  # 5xx status codes
                return "💥"
            else:
                return "🌐"
        elif action.startswith("cache"):
            return "⚡" if status == "hit" else "💾"
        elif action.startswith("auth"):
            return "🔐" if status == "success" else "🚫"
        else:
            return "🌐"

class DatabaseEmojiSet(EmojiSetConfig):
    """Emoji set for database operations."""
    
    domain = "db"
    
    def get_emoji(self, action: str, status: str) -> str:
        if action.startswith("query"):
            return "🔍" if status == "success" else "❗"
        elif action.startswith("connection"):
            return "🔗" if status == "connected" else "🔌"
        elif action.startswith("migration"):
            return "🔄" if status == "success" else "⚠️"
        elif action.startswith("backup"):
            return "💾" if status == "success" else "❌"
        else:
            return "🗄️"

# Use multiple emoji sets
config = TelemetryConfig(
    logging=LoggingConfig(
        custom_emoji_sets=[
            WebEmojiSet(),
            DatabaseEmojiSet(),
            KubernetesEmojiSet()
        ]
    )
)
setup_telemetry(config)

# Use with different domain loggers
web_log = get_logger("web")
db_log = get_logger("db")
k8s_log = get_logger("k8s")

web_log.info("request_completed", method="GET", status="200", path="/api/users")
db_log.debug("query_executed", table="users", duration_ms=45)
k8s_log.info("pod_ready", pod="api-server-xyz789", node="worker-1")
```