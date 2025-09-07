# Advanced Filtering

Sophisticated filtering techniques for controlling log output in complex applications.

## Level-Based Filtering

### Module-Specific Levels

```python
from provide.foundation import setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

def setup_granular_logging():
    """Configure different log levels for different modules."""
    
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            
            # Fine-grained control per module
            module_levels={
                # Core application - verbose logging
                "myapp.core": "DEBUG",
                "myapp.services": "DEBUG",
                
                # Database - moderate logging
                "myapp.database": "INFO",
                "myapp.database.connection": "WARNING",
                
                # External libraries - minimal logging
                "requests": "WARNING",
                "urllib3": "ERROR",
                "boto3": "ERROR",
                "botocore": "ERROR",
                
                # Development utilities - trace everything
                "myapp.dev": "TRACE",
                "myapp.debugging": "TRACE",
                
                # Security - log everything
                "myapp.auth": "DEBUG",
                "myapp.security": "DEBUG",
                
                # Performance-critical paths - minimal logging
                "myapp.hotpath": "WARNING",
                "myapp.highfrequency": "ERROR",
            }
        )
    )
    
    setup_telemetry(config)
    
    # Test the configuration
    from provide.foundation import get_logger
    
    # These loggers will have different effective levels
    core_logger = get_logger("myapp.core.engine")
    db_logger = get_logger("myapp.database.queries")  
    external_logger = get_logger("requests.adapters")
    dev_logger = get_logger("myapp.dev.profiler")
    
    # Demonstrate different filtering
    core_logger.debug("Core debug message")  # Will appear
    db_logger.debug("Database debug message")  # Will NOT appear (INFO level)
    external_logger.warning("External warning")  # Will appear  
    dev_logger.trace("Development trace")  # Will appear
    
    print("Granular logging configuration applied")

setup_granular_logging()
```

### Dynamic Level Adjustment

```python
import asyncio
from typing import Any
from provide.foundation import get_logger
from provide.foundation.logger.custom_processors import StructlogProcessor

class DynamicLevelFilter:
    """Filter that adjusts log levels based on runtime conditions."""
    
    def __init__(self):
        self.base_levels = {
            "DEBUG": 10,
            "INFO": 20, 
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50
        }
        self.boost_conditions: dict[str, int] = {}
        self.suppress_conditions: dict[str, int] = {}
    
    def add_boost_condition(self, condition_name: str, level_boost: int):
        """Add condition that increases logging verbosity."""
        self.boost_conditions[condition_name] = level_boost
    
    def add_suppress_condition(self, condition_name: str, level_penalty: int):
        """Add condition that decreases logging verbosity."""
        self.suppress_conditions[condition_name] = level_penalty
    
    def __call__(
        self, 
        logger: Any, 
        method_name: str, 
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Apply dynamic level filtering."""
        
        # Get base level
        level_str = str(event_dict.get("level", "INFO")).upper()
        base_level = self.base_levels.get(level_str, 20)
        
        # Calculate adjustments
        level_adjustment = 0
        
        # Check boost conditions
        for condition, boost in self.boost_conditions.items():
            if self._check_condition(condition, event_dict):
                level_adjustment -= boost  # Lower number = more verbose
        
        # Check suppress conditions  
        for condition, penalty in self.suppress_conditions.items():
            if self._check_condition(condition, event_dict):
                level_adjustment += penalty  # Higher number = less verbose
        
        # Apply adjustment
        adjusted_level = base_level + level_adjustment
        
        # Determine if message should be filtered
        threshold = self._get_current_threshold(event_dict)
        
        if adjusted_level < threshold:
            raise structlog.DropEvent
        
        # Add adjustment info for debugging
        if level_adjustment != 0:
            event_dict["_level_adjusted"] = level_adjustment
        
        return event_dict
    
    def _check_condition(self, condition: str, event_dict: dict) -> bool:
        """Check if a condition applies to this log event."""
        
        if condition == "error_burst":
            # More verbose logging when errors are frequent
            return self._is_error_burst_active()
        
        elif condition == "high_load":
            # Less verbose logging under high load
            return self._is_system_under_load()
        
        elif condition == "debug_session":
            # More verbose for debug sessions
            return event_dict.get("debug_session") is True
        
        elif condition == "production_hours":
            # Less verbose during production hours
            return self._is_production_hours()
        
        return False
    
    def _get_current_threshold(self, event_dict: dict) -> int:
        """Get current logging threshold for this event."""
        logger_name = event_dict.get("logger_name", "")
        
        # Different thresholds for different modules
        if logger_name.startswith("myapp.critical"):
            return 10  # Very verbose for critical components
        elif logger_name.startswith("myapp.background"):
            return 30  # Less verbose for background tasks
        else:
            return 20  # Default INFO level
    
    def _is_error_burst_active(self) -> bool:
        """Check if we're currently experiencing an error burst."""
        # Implementation would check error rate metrics
        return False
    
    def _is_system_under_load(self) -> bool:
        """Check if system is under high load."""
        import psutil
        return psutil.cpu_percent() > 80 or psutil.virtual_memory().percent > 85
    
    def _is_production_hours(self) -> bool:
        """Check if it's during production peak hours."""
        import datetime
        now = datetime.datetime.now()
        return 9 <= now.hour <= 17  # 9 AM to 5 PM

# Usage example
async def demonstrate_dynamic_filtering():
    """Shows dynamic level filtering in action."""
    
    filter_processor = DynamicLevelFilter()
    
    # Configure conditions
    filter_processor.add_boost_condition("error_burst", 10)  # More verbose during errors
    filter_processor.add_boost_condition("debug_session", 15)  # Even more verbose in debug
    filter_processor.add_suppress_condition("high_load", 10)  # Less verbose under load
    filter_processor.add_suppress_condition("production_hours", 5)  # Slightly less verbose in prod hours
    
    # Test events
    test_events = [
        {"level": "debug", "logger_name": "myapp.core", "event": "Debug message"},
        {"level": "debug", "logger_name": "myapp.critical", "event": "Critical debug"},
        {"level": "info", "logger_name": "myapp.background", "event": "Background task", "debug_session": True},
        {"level": "warning", "logger_name": "myapp.service", "event": "Service warning"},
    ]
    
    for event in test_events:
        try:
            processed = filter_processor(None, "info", event.copy())
            adjustment = processed.get("_level_adjusted", 0)
            print(f"Passed: {event['event']} (adjustment: {adjustment:+d})")
        except structlog.DropEvent:
            print(f"Filtered: {event['event']}")

asyncio.run(demonstrate_dynamic_filtering())
```

## Content-Based Filtering

### Field-Based Filters

```python
import re
from typing import Any, Pattern
from provide.foundation.logger.custom_processors import StructlogProcessor

class FieldBasedFilter:
    """Filter log events based on field content."""
    
    def __init__(self):
        self.include_patterns: dict[str, Pattern] = {}
        self.exclude_patterns: dict[str, Pattern] = {}
        self.required_fields: set[str] = set()
        self.forbidden_fields: set[str] = set()
    
    def include_field_pattern(self, field: str, pattern: str):
        """Include events where field matches pattern."""
        self.include_patterns[field] = re.compile(pattern, re.IGNORECASE)
    
    def exclude_field_pattern(self, field: str, pattern: str):
        """Exclude events where field matches pattern."""
        self.exclude_patterns[field] = re.compile(pattern, re.IGNORECASE)
    
    def require_fields(self, *fields: str):
        """Require specific fields to be present."""
        self.required_fields.update(fields)
    
    def forbid_fields(self, *fields: str):
        """Forbid specific fields (drop if present)."""
        self.forbidden_fields.update(fields)
    
    def __call__(
        self, 
        logger: Any, 
        method_name: str, 
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Apply field-based filtering."""
        
        # Check required fields
        for field in self.required_fields:
            if field not in event_dict:
                raise structlog.DropEvent
        
        # Check forbidden fields
        for field in self.forbidden_fields:
            if field in event_dict:
                raise structlog.DropEvent
        
        # Check include patterns
        if self.include_patterns:
            include_match = False
            for field, pattern in self.include_patterns.items():
                value = event_dict.get(field, "")
                if pattern.search(str(value)):
                    include_match = True
                    break
            
            if not include_match:
                raise structlog.DropEvent
        
        # Check exclude patterns
        for field, pattern in self.exclude_patterns.items():
            value = event_dict.get(field, "")
            if pattern.search(str(value)):
                raise structlog.DropEvent
        
        return event_dict

def demonstrate_field_filtering():
    """Shows field-based filtering capabilities."""
    
    filter_processor = FieldBasedFilter()
    
    # Configure filters
    filter_processor.include_field_pattern("user_type", r"^(admin|premium)$")  # Only admin/premium users
    filter_processor.exclude_field_pattern("event", r"heartbeat|ping")  # No heartbeat messages
    filter_processor.require_fields("request_id", "user_id")  # Must have tracking IDs
    filter_processor.forbid_fields("password", "secret")  # Never allow sensitive fields
    
    # Test events
    test_events = [
        {"event": "User login", "user_type": "admin", "request_id": "req-123", "user_id": "u-456"},
        {"event": "Heartbeat check", "user_type": "admin", "request_id": "req-124", "user_id": "u-456"},
        {"event": "Data access", "user_type": "standard", "request_id": "req-125", "user_id": "u-789"},
        {"event": "Payment processed", "user_type": "premium", "request_id": "req-126", "user_id": "u-101"},
        {"event": "Login attempt", "user_type": "admin", "password": "secret123", "request_id": "req-127", "user_id": "u-456"},
        {"event": "System error", "user_type": "admin"},  # Missing required fields
    ]
    
    print("Field-based filtering results:")
    for event in test_events:
        try:
            processed = filter_processor(None, "info", event.copy())
            print(f"✓ Passed: {event['event']}")
        except structlog.DropEvent:
            print(f"✗ Filtered: {event['event']}")

demonstrate_field_filtering()
```

### Rate-Based Filtering

```python
import time
from collections import defaultdict, deque
from typing import Any

class RateLimitingFilter:
    """Filter that limits log message frequency."""
    
    def __init__(self, default_rate_limit: float = 10.0, window_seconds: float = 60.0):
        self.default_rate_limit = default_rate_limit
        self.window_seconds = window_seconds
        
        # Track message timestamps per key
        self.message_timestamps: defaultdict = defaultdict(lambda: deque())
        
        # Per-pattern rate limits
        self.pattern_limits: dict[str, float] = {}
    
    def set_rate_limit(self, pattern: str, rate_limit: float):
        """Set specific rate limit for messages matching pattern."""
        self.pattern_limits[pattern] = rate_limit
    
    def __call__(
        self, 
        logger: Any, 
        method_name: str, 
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Apply rate limiting filter."""
        
        current_time = time.time()
        
        # Generate key for rate limiting
        rate_key = self._generate_rate_key(event_dict)
        
        # Get rate limit for this message type
        rate_limit = self._get_rate_limit(event_dict)
        
        # Clean old timestamps
        timestamps = self.message_timestamps[rate_key]
        cutoff_time = current_time - self.window_seconds
        
        while timestamps and timestamps[0] < cutoff_time:
            timestamps.popleft()
        
        # Check if we're over the rate limit
        if len(timestamps) >= rate_limit * self.window_seconds:
            # Add rate limiting info
            event_dict["_rate_limited"] = True
            event_dict["_rate_key"] = rate_key
            event_dict["_current_rate"] = len(timestamps) / self.window_seconds
            raise structlog.DropEvent
        
        # Record this message
        timestamps.append(current_time)
        
        # Add rate info for monitoring
        if len(timestamps) > rate_limit * self.window_seconds * 0.8:  # 80% of limit
            event_dict["_rate_warning"] = True
            event_dict["_current_rate"] = len(timestamps) / self.window_seconds
        
        return event_dict
    
    def _generate_rate_key(self, event_dict: dict) -> str:
        """Generate key for rate limiting grouping."""
        
        # Rate limit by logger + event type
        logger_name = event_dict.get("logger_name", "unknown")
        event_type = event_dict.get("event_type", event_dict.get("event", "unknown"))
        
        return f"{logger_name}:{event_type}"
    
    def _get_rate_limit(self, event_dict: dict) -> float:
        """Get applicable rate limit for this event."""
        
        event_text = str(event_dict.get("event", ""))
        
        # Check pattern-specific limits
        for pattern, limit in self.pattern_limits.items():
            if pattern in event_text.lower():
                return limit
        
        # Check level-based limits
        level = event_dict.get("level", "info").upper()
        if level == "ERROR":
            return self.default_rate_limit * 0.5  # Stricter for errors
        elif level == "DEBUG":
            return self.default_rate_limit * 2.0   # More lenient for debug
        
        return self.default_rate_limit

def demonstrate_rate_limiting():
    """Shows rate limiting filter in action."""
    
    filter_processor = RateLimitingFilter(
        default_rate_limit=2.0,  # 2 messages per second
        window_seconds=5.0       # Over 5 second window
    )
    
    # Configure specific limits
    filter_processor.set_rate_limit("database", 1.0)  # DB messages: 1/sec
    filter_processor.set_rate_limit("heartbeat", 0.2)  # Heartbeats: 1 per 5 sec
    
    # Simulate rapid messages
    test_events = [
        {"event": "Database query executed", "logger_name": "myapp.db", "level": "debug"},
        {"event": "Database connection opened", "logger_name": "myapp.db", "level": "info"},
        {"event": "Heartbeat check successful", "logger_name": "myapp.health", "level": "info"},
        {"event": "User login successful", "logger_name": "myapp.auth", "level": "info"},
        {"event": "Database query executed", "logger_name": "myapp.db", "level": "debug"},  # Duplicate
        {"event": "System error occurred", "logger_name": "myapp.core", "level": "error"},
    ]
    
    print("Rate limiting demonstration:")
    
    for i, event in enumerate(test_events):
        try:
            processed = filter_processor(None, "info", event.copy())
            rate_warning = processed.get("_rate_warning", False)
            current_rate = processed.get("_current_rate", 0)
            
            status = "⚠️ NEAR LIMIT" if rate_warning else "✓"
            print(f"{status} Message {i+1}: {event['event'][:30]}... (rate: {current_rate:.1f}/s)")
            
        except structlog.DropEvent:
            print(f"🚫 RATE LIMITED {i+1}: {event['event'][:30]}...")
        
        # Small delay between messages
        time.sleep(0.1)

demonstrate_rate_limiting()
```

## Contextual Filtering

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