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

