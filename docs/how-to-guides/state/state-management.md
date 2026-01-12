# How to Use State Management

Foundation provides thread-safe, immutable state management utilities for building robust applications with predictable state transitions.

## Overview

The state module provides:

- **ImmutableState**: Thread-safe immutable state containers
- **StateMachine**: Finite state machine implementation
- **StateManager**: Centralized state management
- **ConfigManager**: Configuration versioning with change tracking
- **VersionedConfig**: Configuration with audit trails

## ImmutableState

Create thread-safe, immutable state containers:

```python
from provide.foundation.state import ImmutableState

# Create initial state
state = ImmutableState(
    user_id="user_123",
    status="active",
    count=0
)

# Read values
print(state.user_id)  # "user_123"
print(state.count)    # 0

# Create new state with updates (original unchanged)
new_state = state.update(count=1, status="processing")

print(state.count)      # 0 (unchanged)
print(new_state.count)  # 1 (new state)
```

**Key features:**
- Thread-safe access
- Immutable by design
- Type-safe attribute access
- Efficient copy-on-write semantics

### Use Cases

**1. Request Context:**
```python
from provide.foundation.state import ImmutableState

def handle_request(request_id: str):
    # Create immutable request context
    context = ImmutableState(
        request_id=request_id,
        user_id=None,
        authenticated=False
    )

    # Authenticate user (creates new state)
    context = context.update(
        user_id="user_123",
        authenticated=True
    )

    # Process with guaranteed immutability
    process_request(context)
```

**2. Transaction State:**
```python
from provide.foundation.state import ImmutableState

def process_transaction(transaction_id: str):
    state = ImmutableState(
        transaction_id=transaction_id,
        status="pending",
        amount=0,
        timestamp=None
    )

    try:
        state = state.update(status="processing")
        result = execute_transaction()
        state = state.update(
            status="completed",
            amount=result.amount,
            timestamp=result.timestamp
        )
        return state

    except Exception as e:
        state = state.update(status="failed", error=str(e))
        raise
```

## StateMachine

Implement finite state machines with explicit transitions:

```python
from provide.foundation.state import StateMachine

# Define states and allowed transitions
machine = StateMachine(
    initial_state="draft",
    transitions={
        "draft": ["review", "archived"],
        "review": ["approved", "rejected", "draft"],
        "approved": ["published", "archived"],
        "rejected": ["draft", "archived"],
        "published": ["archived"],
        "archived": []  # Terminal state
    }
)

# Check current state
print(machine.current_state)  # "draft"

# Transition to new state
machine.transition("review")
print(machine.current_state)  # "review"

# Invalid transitions raise errors
try:
    machine.transition("published")  # Not allowed from "review"
except ValueError as e:
    print(f"Invalid transition: {e}")

# Check if transition is valid
if machine.can_transition("approved"):
    machine.transition("approved")
```

### Document Workflow Example

```python
from provide.foundation.state import StateMachine
from provide.foundation import logger

class Document:
    def __init__(self, doc_id: str):
        self.doc_id = doc_id
        self.machine = StateMachine(
            initial_state="draft",
            transitions={
                "draft": ["submitted"],
                "submitted": ["reviewing"],
                "reviewing": ["approved", "rejected"],
                "approved": ["published"],
                "rejected": ["draft"],
                "published": []
            }
        )

    def submit(self):
        """Submit document for review."""
        if self.machine.can_transition("submitted"):
            self.machine.transition("submitted")
            logger.info("document_submitted", doc_id=self.doc_id)
        else:
            raise ValueError("Cannot submit from current state")

    def review(self):
        """Start review process."""
        self.machine.transition("reviewing")
        logger.info("document_review_started", doc_id=self.doc_id)

    def approve(self):
        """Approve document."""
        self.machine.transition("approved")
        logger.info("document_approved", doc_id=self.doc_id)

    def publish(self):
        """Publish approved document."""
        self.machine.transition("published")
        logger.info("document_published", doc_id=self.doc_id)

# Usage
doc = Document("doc_001")
doc.submit()
doc.review()
doc.approve()
doc.publish()
```

## StateManager

Centralized state management with observers:

```python
from provide.foundation.state import StateManager

# Create manager with initial state
manager = StateManager(initial_state={
    "connection_count": 0,
    "status": "idle"
})

# Register state change observers
def on_state_change(old_state, new_state):
    print(f"State changed: {old_state} -> {new_state}")

manager.add_observer(on_state_change)

# Update state
manager.update_state({"connection_count": 1, "status": "active"})

# Get current state
current = manager.get_state()
print(current["connection_count"])  # 1
```

### Application State Example

```python
from provide.foundation.state import StateManager
from provide.foundation import logger

class ApplicationState:
    def __init__(self):
        self.manager = StateManager(initial_state={
            "initialized": False,
            "connections": 0,
            "errors": 0,
            "status": "starting"
        })

        # Log state changes
        self.manager.add_observer(self._log_state_change)

    def _log_state_change(self, old_state, new_state):
        """Log all state changes."""
        logger.info("app_state_changed", old=old_state, new=new_state)

    def mark_initialized(self):
        """Mark application as initialized."""
        self.manager.update_state({"initialized": True, "status": "ready"})

    def increment_connections(self):
        """Increment connection count."""
        current = self.manager.get_state()
        self.manager.update_state({
            "connections": current["connections"] + 1
        })

    def record_error(self):
        """Record an error."""
        current = self.manager.get_state()
        self.manager.update_state({
            "errors": current["errors"] + 1
        })

    def get_health(self) -> dict:
        """Get application health status."""
        state = self.manager.get_state()
        return {
            "status": state["status"],
            "initialized": state["initialized"],
            "connections": state["connections"],
            "errors": state["errors"]
        }
```

## ConfigManager

Manage configuration with versioning and change tracking:

```python
from provide.foundation.state import ConfigManager

# Create manager with initial config
config = ConfigManager(initial_config={
    "log_level": "INFO",
    "timeout": 30,
    "enabled_features": ["auth", "api"]
})

# Update configuration
config.update_config({
    "log_level": "DEBUG",
    "timeout": 60
})

# Get current config
current = config.get_config()
print(current["log_level"])  # "DEBUG"

# Get config version
version = config.get_version()
print(f"Config version: {version}")

# Get change history
history = config.get_history()
for change in history:
    print(f"Version {change.version}: {change.changes}")
```

### Runtime Configuration Updates

```python
from provide.foundation.state import ConfigManager
from provide.foundation import logger, get_hub

class DynamicConfig:
    def __init__(self):
        self.manager = ConfigManager(initial_config={
            "log_level": "INFO",
            "max_connections": 100,
            "cache_ttl": 300,
            "features": {
                "auth_enabled": True,
                "metrics_enabled": False
            }
        })

    def update_log_level(self, level: str):
        """Update log level at runtime."""
        self.manager.update_config({"log_level": level})

        # Apply to Foundation logger
        hub = get_hub()
        logger.info("log_level_changed", new_level=level)

    def enable_feature(self, feature: str):
        """Enable a feature flag."""
        config = self.manager.get_config()
        features = config["features"].copy()
        features[f"{feature}_enabled"] = True

        self.manager.update_config({"features": features})
        logger.info("feature_enabled", feature=feature)

    def rollback_to_version(self, version: int):
        """Rollback to previous configuration version."""
        history = self.manager.get_history()
        if version < len(history):
            old_config = history[version].config
            self.manager.update_config(old_config)
            logger.info("config_rolled_back", version=version)

# Usage
config = DynamicConfig()
config.update_log_level("DEBUG")
config.enable_feature("metrics")
```

## VersionedConfig

Track configuration changes with full audit trails:

```python
from provide.foundation.state import VersionedConfig

# Create versioned config
config = VersionedConfig(
    version=1,
    config={
        "database_url": "postgresql://localhost/mydb",
        "cache_enabled": True
    },
    metadata={"author": "admin", "reason": "Initial configuration"}
)

# Create new version
config_v2 = VersionedConfig(
    version=2,
    config={
        "database_url": "postgresql://prod-db/mydb",
        "cache_enabled": True,
        "read_replicas": 3
    },
    metadata={"author": "admin", "reason": "Production migration"}
)

# Compare versions
print(f"Version {config.version} -> Version {config_v2.version}")
print(f"Changes: {config_v2.metadata['reason']}")
```

## Best Practices

### ✅ DO: Use Immutable State for Concurrency

```python
# ✅ Good: Thread-safe immutable state
from provide.foundation.state import ImmutableState

shared_state = ImmutableState(count=0)

def increment():
    global shared_state
    shared_state = shared_state.update(count=shared_state.count + 1)

# ❌ Bad: Mutable shared state
shared_dict = {"count": 0}

def increment_bad():
    shared_dict["count"] += 1  # Race condition!
```

### ✅ DO: Use StateMachine for Complex Workflows

```python
# ✅ Good: Explicit state machine
from provide.foundation.state import StateMachine

order = StateMachine(
    initial_state="pending",
    transitions={
        "pending": ["processing"],
        "processing": ["shipped", "cancelled"],
        "shipped": ["delivered"],
        "cancelled": [],
        "delivered": []
    }
)

# ❌ Bad: Manual state tracking
order_status = "pending"
if order_status == "pending":
    order_status = "shipped"  # Skipped "processing"!
```

### ✅ DO: Track Configuration Changes

```python
# ✅ Good: Version configuration changes
from provide.foundation.state import ConfigManager

config = ConfigManager(initial_config={"timeout": 30})
config.update_config({"timeout": 60})

history = config.get_history()
# Can see who changed what and when

# ❌ Bad: Direct updates without tracking
global_config = {"timeout": 30}
global_config["timeout"] = 60  # No audit trail
```

## Next Steps

- **[Configuration](../configuration/env-variables.md)**: Environment-based configuration
- **[Architecture](../../explanation/architecture.md)**: Understanding Foundation's design
- **[Logging](../logging/basic-logging.md)**: Combine with structured logging

---

**Tip**: Use ImmutableState for thread-safe data, StateMachine for workflows, and ConfigManager for dynamic configuration.
