# Custom Emoji Sets

Guide for creating custom domain-specific emoji sets to enhance your logging with visual context.

## Overview

Custom emoji sets allow you to create domain-specific visual enhancements for your logging. By implementing the `EmojiSetConfig` base class, you can define custom emoji mappings for your specific use cases and technologies.

## Creating Custom Emoji Sets

### Basic Custom Emoji Set

```python
from provide.foundation.logger.emoji.types import EmojiSetConfig

class KubernetesEmojiSet(EmojiSetConfig):
    """Custom emoji set for Kubernetes operations."""
    
    # Define the domain this emoji set handles
    domain = "k8s"
    
    def get_emoji(self, action: str, status: str) -> str:
        """
        Return appropriate emoji based on action and status.
        
        Args:
            action: The operation being performed (e.g., "deploy", "scale", "rollback")
            status: The outcome or state (e.g., "success", "failed", "pending")
            
        Returns:
            Emoji string for the given action and status combination
        """
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
        elif action.startswith("ingress"):
            return "🌐" if status == "ready" else "🚧"
        else:
            return "⚙️"  # Default for unknown operations
```

### Advanced Custom Emoji Set

```python
class CloudInfraEmojiSet(EmojiSetConfig):
    """Advanced emoji set for cloud infrastructure operations."""
    
    domain = "cloud"
    
    # Define emoji mappings as class attributes for better organization
    COMPUTE_EMOJIS = {
        "vm": {"start": "🟢", "stop": "🔴", "restart": "🔄"},
        "container": {"deploy": "🚀", "scale": "📈", "terminate": "💀"},
        "function": {"invoke": "⚡", "deploy": "📦", "error": "❌"},
    }
    
    STORAGE_EMOJIS = {
        "bucket": {"create": "🪣", "delete": "🗑️", "upload": "⬆️", "download": "⬇️"},
        "database": {"backup": "💾", "restore": "♻️", "migrate": "🔄"},
    }
    
    NETWORK_EMOJIS = {
        "lb": {"healthy": "⚖️", "unhealthy": "⚠️"},
        "cdn": {"hit": "⚡", "miss": "🐌", "purge": "🧹"},
        "dns": {"resolve": "🔍", "update": "📝"},
    }
    
    def get_emoji(self, action: str, status: str) -> str:
        """Get emoji with fallback hierarchy."""
        
        # Parse action to extract resource type and operation
        parts = action.split("_")
        if len(parts) >= 2:
            resource_type, operation = parts[0], parts[1]
        else:
            resource_type, operation = action, status
        
        # Look up in specific emoji mappings
        for emoji_group in [self.COMPUTE_EMOJIS, self.STORAGE_EMOJIS, self.NETWORK_EMOJIS]:
            if resource_type in emoji_group:
                resource_emojis = emoji_group[resource_type]
                if operation in resource_emojis:
                    return resource_emojis[operation]
                elif status in resource_emojis:
                    return resource_emojis[status]
        
        # Fallback to general status emojis
        status_emojis = {
            "success": "✅",
            "error": "❌", 
            "warning": "⚠️",
            "pending": "⏳",
            "running": "🏃",
            "stopped": "⏹️"
        }
        
        return status_emojis.get(status, "☁️")  # Cloud default
```

## Registering Custom Emoji Sets

### Single Custom Set

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

# Create emoji set instance
k8s_emoji_set = KubernetesEmojiSet()

# Configure with custom emoji set
config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        das_emoji_prefix_enabled=True,
        custom_emoji_sets=[k8s_emoji_set]
    )
)

setup_telemetry(config)
```

### Multiple Custom Sets

```python
# Create multiple emoji set instances
k8s_set = KubernetesEmojiSet()
cloud_set = CloudInfraEmojiSet() 
monitoring_set = MonitoringEmojiSet()

config = TelemetryConfig(
    logging=LoggingConfig(
        das_emoji_prefix_enabled=True,
        custom_emoji_sets=[k8s_set, cloud_set, monitoring_set],
        # Can also include built-in sets
        enabled_emoji_sets=["http", "database"]
    )
)

setup_telemetry(config)
```

## Usage Patterns

### Domain-Specific Loggers

```python
from provide.foundation import get_logger

# Create loggers that match your emoji set domains
k8s_log = get_logger("k8s")
cloud_log = get_logger("cloud")

# Logging will automatically use appropriate emojis
k8s_log.info("deploy_success", application="web-app", replicas=3)
# Output: 🚀 deploy_success application=web-app replicas=3

cloud_log.info("vm_start", instance_id="i-1234567", region="us-west-2")
# Output: 🟢 vm_start instance_id=i-1234567 region=us-west-2

k8s_log.error("pod_failed", pod="web-app-abc123", reason="ImagePullBackOff")
# Output: ⏹️ pod_failed pod=web-app-abc123 reason=ImagePullBackOff
```

### Action and Status Combinations

```python
# The emoji system looks at both action and status
k8s_log.info("deploy_success", app="api")  # 🚀 (deploy + success)
k8s_log.error("deploy_failed", app="api")   # 💥 (deploy + failed)
k8s_log.info("scale_success", replicas=5)   # 📏 (scale + success)
k8s_log.warning("scale_warning", replicas=0) # ⚠️ (scale + warning)
```

## Advanced Patterns

### Hierarchical Emoji Selection

```python
class SmartEmojiSet(EmojiSetConfig):
    """Emoji set with hierarchical fallback logic."""
    
    domain = "smart"
    
    def get_emoji(self, action: str, status: str) -> str:
        # Priority 1: Exact action + status match
        exact_key = f"{action}_{status}"
        if exact_key in self.EXACT_MAPPINGS:
            return self.EXACT_MAPPINGS[exact_key]
        
        # Priority 2: Action-based match
        if action in self.ACTION_MAPPINGS:
            action_emojis = self.ACTION_MAPPINGS[action]
            if status in action_emojis:
                return action_emojis[status]
        
        # Priority 3: Status-based fallback
        if status in self.STATUS_FALLBACKS:
            return self.STATUS_FALLBACKS[status]
        
        # Priority 4: Default domain emoji
        return self.DEFAULT_EMOJI
    
    EXACT_MAPPINGS = {
        "database_query_success": "🔍✅",
        "api_request_timeout": "🌐⏱️",
        "cache_hit_success": "⚡✨"
    }
    
    ACTION_MAPPINGS = {
        "deploy": {"success": "🚀", "failed": "💥", "pending": "🔄"},
        "backup": {"success": "💾✅", "failed": "💾❌", "running": "💾⏳"}
    }
    
    STATUS_FALLBACKS = {
        "success": "✅", "failed": "❌", "warning": "⚠️",
        "pending": "⏳", "running": "🏃", "stopped": "⏹️"
    }
    
    DEFAULT_EMOJI = "🤖"
```

### Context-Aware Emoji Selection

```python
class ContextAwareEmojiSet(EmojiSetConfig):
    """Emoji set that considers additional context."""
    
    domain = "context"
    
    def get_emoji(self, action: str, status: str, context: dict = None) -> str:
        """Enhanced get_emoji with context support."""
        context = context or {}
        
        # Consider environment context
        if context.get("environment") == "production":
            if status == "error":
                return "🚨"  # More urgent in production
            elif status == "success":
                return "🟢"  # Green for production success
        
        # Consider criticality context
        if context.get("critical", False):
            return "🔥" if status == "error" else "⭐"
        
        # Consider user impact context
        user_impact = context.get("user_impact", "low")
        if user_impact == "high" and status == "error":
            return "💔"  # High user impact error
        
        # Fallback to standard emoji logic
        return self._standard_emoji_logic(action, status)
    
    def _standard_emoji_logic(self, action: str, status: str) -> str:
        # Standard emoji selection logic
        return "📍"
```

## Testing Custom Emoji Sets

### Unit Testing

```python
import pytest
from your_app.emoji_sets import KubernetesEmojiSet

def test_kubernetes_emoji_set():
    emoji_set = KubernetesEmojiSet()
    
    # Test deploy operations
    assert emoji_set.get_emoji("deploy_started", "success") == "🚀"
    assert emoji_set.get_emoji("deploy_failed", "error") == "💥"
    
    # Test scale operations  
    assert emoji_set.get_emoji("scale_up", "success") == "📏"
    assert emoji_set.get_emoji("scale_down", "warning") == "⚠️"
    
    # Test pod operations
    assert emoji_set.get_emoji("pod_created", "running") == "📦"
    assert emoji_set.get_emoji("pod_terminated", "stopped") == "⏹️"
    
    # Test fallback
    assert emoji_set.get_emoji("unknown_action", "unknown_status") == "⚙️"
```

### Integration Testing

```python
def test_emoji_set_integration():
    """Test custom emoji set with actual logging."""
    import structlog.testing
    from provide.foundation import get_logger, setup_telemetry
    from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
    
    # Setup with custom emoji set
    config = TelemetryConfig(
        logging=LoggingConfig(
            custom_emoji_sets=[KubernetesEmojiSet()]
        )
    )
    setup_telemetry(config)
    
    # Test logging with emoji
    log = get_logger("k8s")
    
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        log.info("deploy_success", application="test-app")
    
    # Verify emoji appears in log output
    assert len(cap_logs.entries) == 1
    # Note: Exact emoji verification depends on your formatter configuration
```

## Best Practices

### 1. Clear Domain Separation

```python
# Good: Clear domain boundaries
class DatabaseEmojiSet(EmojiSetConfig):
    domain = "database"  # Handles database operations only
    
class CacheEmojiSet(EmojiSetConfig):
    domain = "cache"     # Handles cache operations only

# Avoid: Overlapping domains
class DataEmojiSet(EmojiSetConfig):
    domain = "data"      # Too broad - what about databases vs cache vs files?
```

### 2. Consistent Naming Conventions

```python
class WellNamedEmojiSet(EmojiSetConfig):
    def get_emoji(self, action: str, status: str) -> str:
        # Use consistent action naming: resource_operation
        if action == "pod_create" and status == "success":
            return "📦✅"
        elif action == "service_deploy" and status == "failed":
            return "🔗❌"
        # ...
```

### 3. Comprehensive Fallbacks

```python
class RobustEmojiSet(EmojiSetConfig):
    def get_emoji(self, action: str, status: str) -> str:
        try:
            # Attempt specific emoji lookup
            return self._get_specific_emoji(action, status)
        except KeyError:
            # Fallback to status-based emoji
            return self._get_status_emoji(status)
        except Exception:
            # Ultimate fallback
            return "📍"  # Generic marker
```

### 4. Documentation and Examples

```python
class DocumentedEmojiSet(EmojiSetConfig):
    """
    Emoji set for monitoring and observability operations.
    
    Supported Actions:
    - alert_*: Alert management (🚨 critical, ⚠️ warning, ℹ️ info)
    - metric_*: Metric collection (📊 success, 📉 failure)
    - trace_*: Distributed tracing (🔍 started, ✅ completed)
    
    Example Usage:
        log.info("alert_triggered", severity="critical", service="api")
        log.debug("metric_collected", name="response_time", value=150)
    """
    
    domain = "monitoring"
    
    def get_emoji(self, action: str, status: str) -> str:
        # Implementation with clear logic...
        pass
```

## Related Documentation

- [api-Emoji Base Types](api-base.md) - Core emoji set interfaces
- [api-Built-in Emoji Sets](api-index.md) - Available built-in emoji sets
- [Advanced Usage Guide](../../guide/advanced-usage.md) - Advanced emoji patterns
- [Testing Guide](../../guide/testing.md) - Testing emoji functionality