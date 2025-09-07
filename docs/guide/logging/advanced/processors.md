# Custom Processors

Creating and configuring custom log processors for advanced logging functionality.

## Understanding Processors

Processors transform log records as they pass through the logging pipeline. Each processor receives an event dictionary and can modify, filter, or enhance it.

### Processor Interface

```python
from typing import Any
import structlog
from provide.foundation.logger.custom_processors import StructlogProcessor

def example_processor(
    logger: Any, 
    method_name: str, 
    event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """
    Basic processor interface.
    
    Args:
        logger: The logger instance
        method_name: The logging method called (info, debug, etc.)
        event_dict: The event data dictionary
        
    Returns:
        Modified event dictionary
    """
    # Process the event_dict
    event_dict["processed"] = True
    return event_dict
```

## Built-in Processors

### Log Level Processing

```python
from provide.foundation.logger.custom_processors import add_log_level_custom

def demonstrate_log_level_processor():
    """Shows how log level normalization works."""
    
    # Example event dictionaries before processing
    test_events = [
        {"event": "Test message"},  # Uses method_name
        {"event": "Test message", "_foundation_level_hint": "ERROR"},  # Uses hint
        {"event": "Test message", "level": "custom"},  # Preserves existing
    ]
    
    # Process each event
    for i, event_dict in enumerate(test_events):
        method_names = ["info", "debug", "warning"]
        processed = add_log_level_custom(
            None, method_names[i % 3], event_dict.copy()
        )
        print(f"Event {i + 1}: {processed}")

# Example output:
# Event 1: {'event': 'Test message', 'level': 'info'}
# Event 2: {'event': 'Test message', 'level': 'error'}  
# Event 3: {'event': 'Test message', 'level': 'custom'}

demonstrate_log_level_processor()
```

### Level Filtering

```python
from provide.foundation.logger.custom_processors import filter_by_level_custom
from provide.foundation.types import LogLevelStr

# Create level filter
level_filter = filter_by_level_custom(
    default_level_str="INFO",
    module_levels={
        "myapp.database": "DEBUG",
        "myapp.auth": "WARNING", 
        "external.library": "ERROR"
    },
    level_to_numeric_map={
        "CRITICAL": 50,
        "ERROR": 40, 
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
        "TRACE": 5
    }
)

def demonstrate_level_filtering():
    """Shows how level-based filtering works."""
    
    test_events = [
        {"logger_name": "myapp.database", "level": "debug", "event": "DB query"},
        {"logger_name": "myapp.auth", "level": "info", "event": "Auth check"},  # Filtered
        {"logger_name": "external.library", "level": "warning", "event": "Lib warning"},  # Filtered
        {"logger_name": "myapp.main", "level": "info", "event": "App started"},
    ]
    
    for event_dict in test_events:
        try:
            processed = level_filter(None, "info", event_dict)
            print(f"Passed: {processed}")
        except structlog.DropEvent:
            print(f"Filtered: {event_dict}")

demonstrate_level_filtering()
```

### Logger Name Emoji Prefixes

```python
from provide.foundation.logger.custom_processors import add_logger_name_emoji_prefix

def demonstrate_emoji_prefixes():
    """Shows emoji prefix assignment based on logger names."""
    
    test_events = [
        {"logger_name": "provide.foundation.core", "event": "Core message"},
        {"logger_name": "myapp.database.connection", "event": "DB connection"},
        {"logger_name": "external.requests", "event": "HTTP request"},
        {"logger_name": "unknown.module", "event": "Unknown module"},
    ]
    
    for event_dict in test_events:
        processed = add_logger_name_emoji_prefix(None, "info", event_dict.copy())
        print(f"Original: {event_dict['logger_name']}")
        print(f"With emoji: {processed['event']}")
        print()

demonstrate_emoji_prefixes()
```

## Custom Processor Creation

### Basic Custom Processor

```python
from typing import Any
import structlog

def create_request_id_processor() -> StructlogProcessor:
    """Creates a processor that adds request ID to log events."""
    
    def request_id_processor(
        logger: Any,
        method_name: str, 
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        # Get request ID from context (implementation depends on framework)
        request_id = get_current_request_id()  # Your implementation
        
        if request_id:
            event_dict["request_id"] = request_id
            
        return event_dict
    
    return request_id_processor

def get_current_request_id() -> str | None:
    """Get current request ID from context."""
    # Example implementation - replace with your context system
    import contextvars
    
    # Define context variable
    if not hasattr(get_current_request_id, '_request_id_var'):
        get_current_request_id._request_id_var = contextvars.ContextVar('request_id')
    
    try:
        return get_current_request_id._request_id_var.get()
    except LookupError:
        return None

# Usage example
def example_with_request_processor():
    from provide.foundation import get_logger, setup_telemetry
    from provide.foundation.logger.config import TelemetryConfig
    
    # This would be integrated into the processor pipeline
    # For demonstration only - actual integration requires setup modification
    
    logger = get_logger(__name__)
    
    # Set request context
    if hasattr(get_current_request_id, '_request_id_var'):
        get_current_request_id._request_id_var.set("req-12345")
    
    logger.info("Processing request", action="start")
    logger.info("Request completed", action="finish", status="success")
```

### Data Masking Processor

```python
import re
from typing import Any

def create_data_masking_processor() -> StructlogProcessor:
    """Creates processor that masks sensitive data in log events."""
    
    # Sensitive field patterns
    SENSITIVE_FIELDS = {
        "password", "passwd", "secret", "token", "key", 
        "auth", "authorization", "credential", "api_key"
    }
    
    # Patterns for sensitive data in strings
    SENSITIVE_PATTERNS = [
        (re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'), '****-****-****-****'),  # Credit cards
        (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '***@***.***'),  # Emails
        (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), '***-**-****'),  # SSN
    ]
    
    def mask_value(value: Any) -> Any:
        """Mask sensitive values."""
        if isinstance(value, str):
            # Apply pattern-based masking
            for pattern, replacement in SENSITIVE_PATTERNS:
                value = pattern.sub(replacement, value)
            return value
        elif isinstance(value, dict):
            return {k: mask_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [mask_value(item) for item in value]
        else:
            return value
    
    def masking_processor(
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Mask sensitive data in event dictionary."""
        
        # Mask sensitive fields by name
        for key in list(event_dict.keys()):
            if any(sensitive in key.lower() for sensitive in SENSITIVE_FIELDS):
                event_dict[key] = "[REDACTED]"
        
        # Mask sensitive patterns in string values
        for key, value in event_dict.items():
            if key not in SENSITIVE_FIELDS:  # Don't double-process
                event_dict[key] = mask_value(value)
        
        return event_dict
    
    return masking_processor

# Example usage
def demonstrate_data_masking():
    """Shows data masking in action."""
    
    processor = create_data_masking_processor()
    
    test_event = {
        "event": "User login attempt",
        "user_email": "john.doe@example.com",
        "password": "secret123",
        "api_key": "ak_1234567890abcdef",
        "user_data": {
            "credit_card": "4532-1234-5678-9012",
            "phone": "555-0123"
        },
        "message": "User john.doe@example.com logged in with card 4532-1234-5678-9012"
    }
    
    masked_event = processor(None, "info", test_event.copy())
    
    print("Original event:")
    for k, v in test_event.items():
        print(f"  {k}: {v}")
    
    print("\\nMasked event:")
    for k, v in masked_event.items():
        print(f"  {k}: {v}")

demonstrate_data_masking()
```

### Performance Monitoring Processor

```python
import time
from typing import Any
from collections import deque, defaultdict

class PerformanceProcessor:
    """Processor that tracks logging performance metrics."""
    
    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.message_times: deque = deque(maxlen=window_size)
        self.level_counts: defaultdict = defaultdict(int)
        self.logger_counts: defaultdict = defaultdict(int)
        self.start_time = time.time()
    
    def __call__(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Track performance metrics for each log message."""
        
        current_time = time.time()
        self.message_times.append(current_time)
        
        # Track level distribution
        level = event_dict.get("level", "unknown")
        self.level_counts[level] += 1
        
        # Track logger name distribution  
        logger_name = event_dict.get("logger_name", "unknown")
        self.logger_counts[logger_name] += 1
        
        # Add performance metadata to high-frequency debug events
        if level == "debug" and len(self.message_times) % 100 == 0:
            event_dict["_perf_stats"] = self.get_current_stats()
        
        return event_dict
    
    def get_current_stats(self) -> dict[str, Any]:
        """Get current performance statistics."""
        
        current_time = time.time()
        
        # Calculate message rate
        if len(self.message_times) >= 2:
            time_span = self.message_times[-1] - self.message_times[0]
            rate = len(self.message_times) / time_span if time_span > 0 else 0
        else:
            rate = 0
        
        # Total runtime stats
        total_runtime = current_time - self.start_time
        total_messages = sum(self.level_counts.values())
        
        return {
            "messages_per_second": round(rate, 2),
            "total_messages": total_messages,
            "runtime_seconds": round(total_runtime, 2),
            "avg_rate": round(total_messages / total_runtime, 2) if total_runtime > 0 else 0,
            "level_distribution": dict(self.level_counts),
            "top_loggers": dict(sorted(
                self.logger_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5])
        }

# Example usage
def demonstrate_performance_processor():
    """Shows performance monitoring processor."""
    
    perf_processor = PerformanceProcessor(window_size=50)
    
    # Simulate log events
    import random
    
    loggers = ["myapp.main", "myapp.db", "myapp.auth", "myapp.api"]
    levels = ["info", "debug", "warning", "error"]
    
    for i in range(200):
        event_dict = {
            "event": f"Test message {i}",
            "logger_name": random.choice(loggers),
            "level": random.choice(levels),
            "iteration": i
        }
        
        processed = perf_processor(None, "info", event_dict)
        
        # Print performance stats when available
        if "_perf_stats" in processed:
            print(f"\\nPerformance stats at message {i}:")
            stats = processed["_perf_stats"]
            print(f"  Rate: {stats['messages_per_second']} msg/sec")
            print(f"  Total: {stats['total_messages']} messages")
            print(f"  Levels: {stats['level_distribution']}")
            print(f"  Top loggers: {list(stats['top_loggers'].keys())[:3]}")

demonstrate_performance_processor()
```

## Processor Integration

### Adding Processors to Configuration

```python
from provide.foundation import setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

def setup_with_custom_processors():
    """Example of how custom processors would be integrated."""
    
    # Note: This shows the concept - actual integration requires
    # modifying the processor pipeline in the setup code
    
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json"
        )
    )
    
    setup_telemetry(config)
    
    # Custom processors would be added to the pipeline here
    # This is conceptual - actual implementation would modify
    # the _build_core_processors_list function
    
    print("Telemetry setup with custom processors")

# Custom processor pipeline concept
def create_custom_processor_pipeline():
    """Shows how to create a complete custom processor pipeline."""
    
    from provide.foundation.logger.custom_processors import (
        add_log_level_custom,
        filter_by_level_custom
    )
    
    processors = [
        # Context and core processing
        structlog.contextvars.merge_contextvars,
        add_log_level_custom,
        
        # Custom processors
        create_request_id_processor(),
        create_data_masking_processor(),
        PerformanceProcessor(),
        
        # Level filtering (after custom processing)
        filter_by_level_custom(
            default_level_str="INFO",
            module_levels={},
            level_to_numeric_map={
                "CRITICAL": 50, "ERROR": 40, "WARNING": 30, 
                "INFO": 20, "DEBUG": 10, "TRACE": 5
            }
        ),
        
        # Output formatting
        structlog.processors.JSONRenderer()
    ]
    
    return processors
```

### Conditional Processor Application

```python
import os
from typing import Any

def create_environment_aware_processor() -> StructlogProcessor:
    """Processor that behaves differently based on environment."""
    
    environment = os.getenv("ENVIRONMENT", "development")
    
    def environment_processor(
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        
        # Add environment context
        event_dict["environment"] = environment
        
        if environment == "production":
            # In production: mask sensitive data, add minimal debug info
            if "debug_info" in event_dict:
                event_dict.pop("debug_info")
                
        elif environment == "development":
            # In development: add extra debug context
            event_dict["dev_context"] = {
                "timestamp_ms": time.time() * 1000,
                "process_id": os.getpid()
            }
            
        elif environment == "testing":
            # In testing: add test metadata
            event_dict["test_run"] = True
            
        return event_dict
    
    return environment_processor

# Usage in different environments
def demonstrate_environment_processor():
    """Shows environment-aware processing."""
    
    processor = create_environment_aware_processor()
    
    test_event = {
        "event": "Application started",
        "debug_info": {"memory_usage": "128MB"},
        "user_count": 42
    }
    
    processed = processor(None, "info", test_event.copy())
    
    print("Environment-aware processing:")
    print(f"Environment: {processed.get('environment')}")
    print(f"Has debug_info: {'debug_info' in processed}")
    print(f"Has dev_context: {'dev_context' in processed}")
    print(f"Has test_run: {'test_run' in processed}")

demonstrate_environment_processor()
```

## Processor Best Practices

### Error Handling in Processors

```python
from typing import Any
import structlog

def create_resilient_processor() -> StructlogProcessor:
    """Creates a processor with proper error handling."""
    
    def resilient_processor(
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        try:
            # Your custom processing logic here
            result = complex_processing_operation(event_dict)
            event_dict["processed_result"] = result
            
        except Exception as e:
            # Log the error but don't break the pipeline
            event_dict["_processor_error"] = f"Processing failed: {str(e)}"
            
            # Optionally, use a fallback logger to report the issue
            # (Be careful not to create infinite loops)
            
        return event_dict
    
    return resilient_processor

def complex_processing_operation(event_dict: dict) -> str:
    """Simulate complex processing that might fail."""
    # This might raise exceptions
    if "invalid_field" in event_dict:
        raise ValueError("Invalid field detected")
    return "processed_successfully"
```

### Performance Considerations

```python
from functools import lru_cache
from typing import Any

def create_optimized_processor() -> StructlogProcessor:
    """Creates a performance-optimized processor."""
    
    # Pre-compute expensive operations
    STATIC_MAPPINGS = {
        "prod": "production",
        "dev": "development", 
        "stage": "staging"
    }
    
    @lru_cache(maxsize=128)
    def expensive_transformation(value: str) -> str:
        """Cached expensive operation."""
        # Simulate expensive computation
        return value.upper().replace("-", "_")
    
    def optimized_processor(
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        
        # Use static mappings when possible
        env = event_dict.get("env")
        if env in STATIC_MAPPINGS:
            event_dict["environment"] = STATIC_MAPPINGS[env]
        
        # Cache expensive transformations
        service = event_dict.get("service")
        if service:
            event_dict["service_normalized"] = expensive_transformation(service)
        
        # Avoid creating new objects when possible
        if "metadata" not in event_dict:
            event_dict["metadata"] = {}  # Reuse when possible
        
        return event_dict
    
    return optimized_processor
```