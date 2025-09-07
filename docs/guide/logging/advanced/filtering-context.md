# Contextual Filtering

Advanced filtering using context information and metadata.

### User-Based Filtering

```python
from typing import Any, Optional
from provide.foundation.logger.custom_processors import StructlogProcessor

class UserContextFilter:
    """Filter logs based on user context and permissions."""
    
    def __init__(self):
        self.user_levels: dict[str, str] = {}
        self.group_levels: dict[str, str] = {}
        self.sensitive_operations: set[str] = set()
    
    def set_user_level(self, user_id: str, level: str):
        """Set logging level for specific user."""
        self.user_levels[user_id] = level.upper()
    
    def set_group_level(self, group: str, level: str):
        """Set logging level for user group."""
        self.group_levels[group] = level.upper()
    
    def add_sensitive_operation(self, operation: str):
        """Mark operation as sensitive (requires elevated logging)."""
        self.sensitive_operations.add(operation.lower())
    
    def __call__(
        self, 
        logger: Any, 
        method_name: str, 
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Apply user context filtering."""
        
        user_id = event_dict.get("user_id")
        user_group = event_dict.get("user_group") 
        operation = event_dict.get("operation", "").lower()
        level = event_dict.get("level", "INFO").upper()
        
        # Check if operation is sensitive
        is_sensitive = any(sens_op in operation for sens_op in self.sensitive_operations)
        
        # Determine required level for this user
        required_level = self._get_required_level(user_id, user_group, is_sensitive)
        
        # Convert levels to numeric for comparison
        level_values = {"TRACE": 5, "DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
        
        current_level_value = level_values.get(level, 20)
        required_level_value = level_values.get(required_level, 20)
        
        # Filter if current level is below required
        if current_level_value < required_level_value:
            raise structlog.DropEvent
        
        # Add context info
        event_dict["_user_context"] = {
            "user_id": user_id,
            "user_group": user_group,
            "required_level": required_level,
            "is_sensitive": is_sensitive
        }
        
        return event_dict
    
    def _get_required_level(self, user_id: Optional[str], user_group: Optional[str], is_sensitive: bool) -> str:
        """Determine required logging level for user context."""
        
        # Sensitive operations always require INFO or higher
        if is_sensitive:
            base_level = "INFO"
        else:
            base_level = "DEBUG"
        
        # Check user-specific level
        if user_id and user_id in self.user_levels:
            return self.user_levels[user_id]
        
        # Check group-specific level
        if user_group and user_group in self.group_levels:
            return self.group_levels[user_group]
        
        return base_level

def demonstrate_user_filtering():
    """Shows user context filtering."""
    
    filter_processor = UserContextFilter()
    
    # Configure user/group levels
    filter_processor.set_user_level("admin-123", "DEBUG")    # Admin sees everything
    filter_processor.set_user_level("user-456", "WARNING")  # Regular user sees less
    filter_processor.set_group_level("developers", "TRACE") # Developers see everything
    filter_processor.set_group_level("support", "INFO")     # Support sees normal ops
    
    # Configure sensitive operations
    filter_processor.add_sensitive_operation("payment")
    filter_processor.add_sensitive_operation("password")
    filter_processor.add_sensitive_operation("auth")
    
    # Test events
    test_events = [
        {"level": "debug", "user_id": "admin-123", "operation": "user_lookup", "event": "User data accessed"},
        {"level": "debug", "user_id": "user-456", "operation": "user_lookup", "event": "User data accessed"},
        {"level": "info", "user_id": "user-456", "operation": "payment_process", "event": "Payment processed"},
        {"level": "debug", "user_group": "developers", "operation": "debug_trace", "event": "Debug trace"},
        {"level": "warning", "user_group": "support", "operation": "auth_failure", "event": "Auth failed"},
        {"level": "debug", "user_group": "support", "operation": "auth_check", "event": "Auth check"},
    ]
    
    print("User context filtering results:")
    for event in test_events:
        try:
            processed = filter_processor(None, "info", event.copy())
            context = processed.get("_user_context", {})
            user = context.get("user_id") or f"group:{context.get('user_group')}"
            required = context.get("required_level")
            sensitive = " (SENSITIVE)" if context.get("is_sensitive") else ""
            
            print(f"✓ {user} [{required}]: {event['event']}{sensitive}")
            
        except structlog.DropEvent:
            user = event.get("user_id") or f"group:{event.get('user_group')}"
            print(f"✗ {user}: {event['event']} (filtered)")

demonstrate_user_filtering()
```

### Environment-Based Filtering

```python
import os
from typing import Any
from provide.foundation.logger.custom_processors import StructlogProcessor

class EnvironmentFilter:
    """Filter logs based on deployment environment."""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development").lower()
        
        # Define what's allowed in each environment
        self.environment_config = {
            "production": {
                "min_level": "INFO",
                "allowed_loggers": ["myapp.*"],
                "blocked_loggers": ["test.*", "debug.*", "dev.*"],
                "allowed_fields": ["event", "level", "timestamp", "logger_name", "service_name"],
                "blocked_fields": ["debug_info", "dev_notes", "internal_state"],
                "sensitive_scrubbing": True
            },
            "staging": {
                "min_level": "DEBUG", 
                "allowed_loggers": ["*"],
                "blocked_loggers": ["test.*"],
                "allowed_fields": "*",
                "blocked_fields": ["password", "secret", "token"],
                "sensitive_scrubbing": True
            },
            "development": {
                "min_level": "TRACE",
                "allowed_loggers": ["*"],
                "blocked_loggers": [],
                "allowed_fields": "*", 
                "blocked_fields": [],
                "sensitive_scrubbing": False
            },
            "testing": {
                "min_level": "DEBUG",
                "allowed_loggers": ["*"],
                "blocked_loggers": [],
                "allowed_fields": "*",
                "blocked_fields": [],
                "sensitive_scrubbing": False
            }
        }
    
    def __call__(
        self, 
        logger: Any, 
        method_name: str, 
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Apply environment-specific filtering."""
        
        config = self.environment_config.get(self.environment, self.environment_config["development"])
        
        # Check minimum level
        level = event_dict.get("level", "INFO").upper()
        if not self._level_allowed(level, config["min_level"]):
            raise structlog.DropEvent
        
        # Check logger name
        logger_name = event_dict.get("logger_name", "")
        if not self._logger_allowed(logger_name, config):
            raise structlog.DropEvent
        
        # Filter fields
        event_dict = self._filter_fields(event_dict, config)
        
        # Apply sensitive data scrubbing
        if config["sensitive_scrubbing"]:
            event_dict = self._scrub_sensitive_data(event_dict)
        
        # Add environment context
        event_dict["environment"] = self.environment
        
        return event_dict
    
    def _level_allowed(self, current_level: str, min_level: str) -> bool:
        """Check if log level meets minimum requirement."""
        
        levels = {"TRACE": 5, "DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
        
        current_value = levels.get(current_level, 20)
        min_value = levels.get(min_level, 20)
        
        return current_value >= min_value
    
    def _logger_allowed(self, logger_name: str, config: dict) -> bool:
        """Check if logger name is allowed in this environment."""
        
        import fnmatch
        
        # Check blocked loggers first
        for pattern in config["blocked_loggers"]:
            if fnmatch.fnmatch(logger_name, pattern):
                return False
        
        # Check allowed loggers
        if config["allowed_loggers"] == ["*"]:
            return True
        
        for pattern in config["allowed_loggers"]:
            if fnmatch.fnmatch(logger_name, pattern):
                return True
        
        return False
    
    def _filter_fields(self, event_dict: dict, config: dict) -> dict:
        """Filter event fields based on environment policy."""
        
        if config["allowed_fields"] == "*" and not config["blocked_fields"]:
            return event_dict
        
        filtered_dict = {}
        
        for key, value in event_dict.items():
            # Always keep essential fields
            if key in ["event", "level", "timestamp", "logger_name"]:
                filtered_dict[key] = value
                continue
            
            # Check blocked fields
            if key in config["blocked_fields"]:
                continue
            
            # Check allowed fields
            if config["allowed_fields"] == "*" or key in config["allowed_fields"]:
                filtered_dict[key] = value
        
        return filtered_dict
    
    def _scrub_sensitive_data(self, event_dict: dict) -> dict:
        """Scrub sensitive data from event dictionary."""
        
        import re
        
        sensitive_patterns = [
            (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '[EMAIL]'),
            (re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'), '[CARD]'),
            (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), '[SSN]'),
            (re.compile(r'(?i)(password|passwd|secret|token|key|auth)\s*[:=]\s*\S+'), r'\\1=[REDACTED]'),
        ]
        
        scrubbed_dict = {}
        
        for key, value in event_dict.items():
            if isinstance(value, str):
                scrubbed_value = value
                for pattern, replacement in sensitive_patterns:
                    scrubbed_value = pattern.sub(replacement, scrubbed_value)
                scrubbed_dict[key] = scrubbed_value
            else:
                scrubbed_dict[key] = value
        
        return scrubbed_dict

def demonstrate_environment_filtering():
    """Shows environment-based filtering for different deployment contexts."""
    
    # Test with different environment configurations
    environments = ["production", "staging", "development"]
    
    test_events = [
        {"level": "debug", "logger_name": "myapp.core", "event": "Core processing", "debug_info": {"state": "active"}},
        {"level": "info", "logger_name": "test.suite", "event": "Test completed"},
        {"level": "trace", "logger_name": "myapp.auth", "event": "Auth trace", "password": "secret123"},
        {"level": "error", "logger_name": "myapp.payment", "event": "Payment failed", "card": "4532-1234-5678-9012"},
        {"level": "warning", "logger_name": "debug.profiler", "event": "Performance warning"},
    ]
    
    for env in environments:
        print(f"\\n=== {env.upper()} ENVIRONMENT ===")
        
        # Set environment
        os.environ["ENVIRONMENT"] = env
        
        # Create filter for this environment
        env_filter = EnvironmentFilter()
        
        for event in test_events:
            try:
                processed = env_filter(None, "info", event.copy())
                fields_count = len([k for k in processed.keys() if not k.startswith('_')])
                print(f"✓ {event['logger_name']}: {processed.get('event', 'N/A')} ({fields_count} fields)")
                
                # Show field filtering
                if fields_count != len(event):
                    filtered_out = set(event.keys()) - set(processed.keys())
                    if filtered_out:
                        print(f"   Filtered fields: {', '.join(filtered_out)}")
                
            except structlog.DropEvent:
                print(f"✗ {event['logger_name']}: {event['event']} (dropped)")

demonstrate_environment_filtering()
```