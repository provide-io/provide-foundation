# Content-Based Filtering

Filtering logs based on message content and field values.

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

