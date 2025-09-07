# Runtime Updates

Dynamic configuration changes during runtime without application restarts.

## Basic Runtime Updates

### Update Log Level

```python
import asyncio
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.config import get_config, set_config

async def update_log_level_example():
    """Example of updating log level at runtime."""
    
    # Initial configuration
    config = TelemetryConfig(
        service_name="runtime-config-demo",
        logging=LoggingConfig(default_level="INFO")
    )
    setup_telemetry(config)
    
    logger = get_logger("runtime_demo")
    
    # Test initial level
    logger.debug("This debug message won't appear initially")
    logger.info("Initial info message appears")
    
    # Update log level at runtime
    config.logging.default_level = "DEBUG"
    
    # The change takes effect immediately for new log messages
    logger.debug("This debug message now appears!")
    logger.info("Info messages still work")

# Run the example
asyncio.run(update_log_level_example())
```

### Toggle Features

```python
import asyncio
from attrs import define
from provide.foundation.config import BaseConfig, ConfigManager, field

@define
class FeatureFlags(BaseConfig):
    """Feature flag configuration."""
    
    enable_new_ui: bool = field(default=False, description="Enable new UI")
    enable_analytics: bool = field(default=True, description="Enable analytics")
    enable_caching: bool = field(default=True, description="Enable caching")
    max_retries: int = field(default=3, description="Maximum retry attempts")
    timeout_seconds: float = field(default=30.0, description="Request timeout")

async def runtime_feature_toggle_example():
    """Example of toggling features at runtime."""
    
    # Create configuration manager
    manager = ConfigManager()
    
    # Register feature flags
    features = FeatureFlags()
    await manager.register("features", config=features)
    
    print(f"Initial new UI: {features.enable_new_ui}")
    print(f"Initial analytics: {features.enable_analytics}")
    
    # Simulate runtime feature toggle
    await manager.update("features", {
        "enable_new_ui": True,
        "max_retries": 5,
        "timeout_seconds": 45.0
    })
    
    # Get updated configuration
    updated_features = await manager.get("features")
    print(f"Updated new UI: {updated_features.enable_new_ui}")
    print(f"Updated max retries: {updated_features.max_retries}")
    print(f"Updated timeout: {updated_features.timeout_seconds}")
    
    # Features can be checked in application logic
    if updated_features.enable_new_ui:
        print("Rendering new UI")
    else:
        print("Rendering legacy UI")

# Usage
asyncio.run(runtime_feature_toggle_example())
```

## Configuration Sources

### Update from Dictionary

```python
import asyncio
from attrs import define
from provide.foundation.config import BaseConfig, ConfigManager, field
from provide.foundation.config.types import ConfigSource

@define  
class DatabaseConfig(BaseConfig):
    """Database configuration with runtime updates."""
    
    host: str = field(default="localhost", description="Database host")
    port: int = field(default=5432, description="Database port") 
    database: str = field(default="myapp", description="Database name")
    pool_size: int = field(default=10, description="Connection pool size")
    timeout: float = field(default=30.0, description="Connection timeout")

async def runtime_config_updates():
    """Example of updating configuration from various sources."""
    
    manager = ConfigManager()
    
    # Initial configuration
    db_config = DatabaseConfig()
    await manager.register("database", config=db_config)
    
    print("Initial configuration:")
    print(f"  Host: {db_config.host}")
    print(f"  Pool size: {db_config.pool_size}")
    
    # Update from runtime dictionary (highest precedence)
    runtime_updates = {
        "host": "prod-db.example.com",
        "pool_size": 20,
        "timeout": 45.0
    }
    
    await manager.update("database", runtime_updates, source=ConfigSource.RUNTIME)
    
    # Get updated config
    updated_config = await manager.get("database")
    print("\nAfter runtime update:")
    print(f"  Host: {updated_config.host}")
    print(f"  Pool size: {updated_config.pool_size}")
    print(f"  Timeout: {updated_config.timeout}")
    
    # Show source tracking
    print(f"  Host source: {updated_config.get_source('host')}")
    print(f"  Pool size source: {updated_config.get_source('pool_size')}")

asyncio.run(runtime_config_updates())
```

### Environment Variable Updates

```python
import os
import asyncio
from attrs import define
from provide.foundation.config import RuntimeConfig, env_field

@define
class RuntimeAppConfig(RuntimeConfig):
    """Configuration that can be updated from environment variables."""
    
    debug_mode: bool = env_field(
        default=False, 
        env_var="DEBUG_MODE",
        description="Enable debug mode"
    )
    log_level: str = env_field(
        default="INFO",
        env_var="LOG_LEVEL", 
        description="Logging level"
    )
    feature_flag_new_ui: bool = env_field(
        default=False,
        env_var="FEATURE_NEW_UI",
        description="Enable new UI feature"
    )

async def environment_runtime_updates():
    """Example of runtime updates from environment variables."""
    
    # Initial configuration from environment
    config = RuntimeAppConfig.from_env()
    
    print("Initial configuration:")
    print(f"  Debug mode: {config.debug_mode}")
    print(f"  Log level: {config.log_level}")
    print(f"  New UI: {config.feature_flag_new_ui}")
    
    # Simulate environment changes (in real app, these would come from outside)
    os.environ["DEBUG_MODE"] = "true"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["FEATURE_NEW_UI"] = "true"
    
    # Reload configuration from environment
    updated_config = RuntimeAppConfig.from_env()
    
    print("\nAfter environment update:")
    print(f"  Debug mode: {updated_config.debug_mode}")
    print(f"  Log level: {updated_config.log_level}")
    print(f"  New UI: {updated_config.feature_flag_new_ui}")
    
    # In a real application, you would typically:
    # 1. Set up environment variable monitoring
    # 2. Reload configuration when changes are detected
    # 3. Apply changes to running services

asyncio.run(environment_runtime_updates())
```

## Configuration Validation

### Runtime Validation

```python
import asyncio
from attrs import define
from provide.foundation.config import BaseConfig, ConfigManager, field

@define
class APIConfig(BaseConfig):
    """API configuration with validation."""
    
    rate_limit: int = field(default=100, description="Requests per minute")
    timeout: float = field(default=30.0, description="Request timeout") 
    max_connections: int = field(default=50, description="Max concurrent connections")
    retry_attempts: int = field(default=3, description="Retry attempts")
    
    async def validate(self):
        """Custom validation logic."""
        if self.rate_limit <= 0:
            raise ValueError("Rate limit must be positive")
        
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
            
        if self.max_connections <= 0:
            raise ValueError("Max connections must be positive")
            
        if self.retry_attempts < 0:
            raise ValueError("Retry attempts cannot be negative")
        
        # Business logic validation
        if self.rate_limit > 1000 and self.max_connections < 100:
            raise ValueError("High rate limit requires more connections")

async def runtime_validation_example():
    """Example of runtime configuration validation."""
    
    manager = ConfigManager()
    
    # Register valid configuration
    config = APIConfig()
    await config.validate()  # Initial validation
    await manager.register("api", config=config)
    
    print("Initial valid configuration registered")
    
    # Try invalid update
    try:
        await manager.update("api", {"rate_limit": -10})  # Invalid
    except Exception as e:
        print(f"Validation prevented invalid update: {e}")
    
    # Try valid update
    await manager.update("api", {
        "rate_limit": 200,
        "max_connections": 100
    })
    
    updated_config = await manager.get("api")
    print(f"Valid update applied - rate limit: {updated_config.rate_limit}")

asyncio.run(runtime_validation_example())
```

## Configuration Diffing

### Track Configuration Changes

```python
import asyncio
from attrs import define
from provide.foundation.config import BaseConfig, ConfigManager, field

@define
class MonitoringConfig(BaseConfig):
    """Configuration with change tracking."""
    
    enabled: bool = field(default=True, description="Enable monitoring")
    interval_seconds: int = field(default=60, description="Check interval")
    alert_threshold: float = field(default=0.95, description="Alert threshold")
    notification_email: str = field(
        default="admin@example.com", 
        description="Notification email"
    )

async def configuration_diffing_example():
    """Example of tracking configuration changes."""
    
    manager = ConfigManager()
    
    # Initial configuration
    original_config = MonitoringConfig()
    await manager.register("monitoring", config=original_config)
    
    print("Original configuration:")
    print(f"  Enabled: {original_config.enabled}")
    print(f"  Interval: {original_config.interval_seconds}")
    print(f"  Threshold: {original_config.alert_threshold}")
    
    # Make updates
    await manager.update("monitoring", {
        "interval_seconds": 30,
        "alert_threshold": 0.90,
        "notification_email": "ops@example.com"
    })
    
    # Get updated configuration
    updated_config = await manager.get("monitoring")
    
    # Calculate and display differences
    differences = original_config.diff(updated_config)
    
    print("\nConfiguration changes:")
    for field_name, (old_value, new_value) in differences.items():
        print(f"  {field_name}: {old_value} -> {new_value}")
    
    # Clone for further modifications
    cloned_config = updated_config.clone()
    cloned_config.enabled = False
    
    print(f"\nCloned config enabled: {cloned_config.enabled}")
    print(f"Original updated config enabled: {updated_config.enabled}")

asyncio.run(configuration_diffing_example())
```

## Atomic Updates

### Transaction-Like Updates

```python
import asyncio
from attrs import define
from provide.foundation.config import BaseConfig, ConfigManager, field
from provide.foundation.config.types import ConfigSource

@define
class ServiceConfig(BaseConfig):
    """Service configuration requiring atomic updates."""
    
    worker_count: int = field(default=4, description="Number of workers")
    memory_limit_mb: int = field(default=512, description="Memory limit MB")
    cpu_limit_percent: int = field(default=80, description="CPU limit percent")
    
    async def validate(self):
        """Ensure configuration consistency."""
        # Business rule: more workers need more memory
        min_memory_per_worker = 128
        required_memory = self.worker_count * min_memory_per_worker
        
        if self.memory_limit_mb < required_memory:
            raise ValueError(
                f"Memory limit {self.memory_limit_mb}MB insufficient for "
                f"{self.worker_count} workers (need {required_memory}MB)"
            )

class AtomicConfigManager(ConfigManager):
    """Configuration manager with atomic update support."""
    
    async def atomic_update(self, name: str, updates: dict):
        """Perform atomic configuration update with rollback on failure."""
        
        # Get current configuration
        current_config = await self.get(name)
        if not current_config:
            raise ValueError(f"Configuration not found: {name}")
        
        # Create backup
        backup_config = current_config.clone()
        
        try:
            # Apply updates
            await self.update(name, updates)
            
            # Get updated config and validate
            updated_config = await self.get(name)
            await updated_config.validate()
            
            print(f"Atomic update successful for {name}")
            return updated_config
            
        except Exception as e:
            # Rollback on any failure
            await self.set(name, backup_config)
            print(f"Atomic update failed for {name}, rolled back: {e}")
            raise

async def atomic_updates_example():
    """Example of atomic configuration updates."""
    
    manager = AtomicConfigManager()
    
    # Initial configuration
    config = ServiceConfig()
    await manager.register("service", config=config)
    
    print("Initial configuration:")
    print(f"  Workers: {config.worker_count}")  
    print(f"  Memory: {config.memory_limit_mb}MB")
    
    # Valid atomic update
    try:
        await manager.atomic_update("service", {
            "worker_count": 8,
            "memory_limit_mb": 1024  # Sufficient for 8 workers
        })
        
        updated_config = await manager.get("service")
        print(f"\nValid update - Workers: {updated_config.worker_count}")
        
    except Exception as e:
        print(f"Update failed: {e}")
    
    # Invalid atomic update (should rollback)
    try:
        await manager.atomic_update("service", {
            "worker_count": 16,
            "memory_limit_mb": 256  # Insufficient for 16 workers
        })
    except Exception as e:
        print(f"\nInvalid update prevented: {e}")
        
        # Verify rollback
        current_config = await manager.get("service")
        print(f"After rollback - Workers: {current_config.worker_count}")

asyncio.run(atomic_updates_example())
```

## Hot Reloading

### Application Integration

```python
import asyncio
import signal
from typing import Callable, Dict, Any
from attrs import define
from provide.foundation.config import BaseConfig, ConfigManager, field

@define
class AppConfig(BaseConfig):
    """Application configuration."""
    
    server_port: int = field(default=8000, description="Server port")
    debug_mode: bool = field(default=False, description="Debug mode")  
    worker_count: int = field(default=4, description="Worker processes")
    log_level: str = field(default="INFO", description="Log level")

class HotReloadConfigManager(ConfigManager):
    """Configuration manager with hot reload support."""
    
    def __init__(self):
        super().__init__()
        self._reload_callbacks: Dict[str, list[Callable]] = {}
    
    def on_config_reload(self, config_name: str, callback: Callable):
        """Register callback for configuration reloads."""
        if config_name not in self._reload_callbacks:
            self._reload_callbacks[config_name] = []
        self._reload_callbacks[config_name].append(callback)
    
    async def hot_reload(self, config_name: str, new_config_data: Dict[str, Any]):
        """Perform hot reload of configuration."""
        print(f"Hot reloading configuration: {config_name}")
        
        # Get current configuration
        current_config = await self.get(config_name)
        if not current_config:
            raise ValueError(f"Configuration not found: {config_name}")
        
        # Calculate differences
        old_values = current_config.to_dict()
        
        # Apply updates
        await self.update(config_name, new_config_data)
        new_config = await self.get(config_name)
        
        # Calculate what changed
        differences = current_config.diff(new_config)
        
        if differences:
            print(f"Configuration changes detected:")
            for field, (old_val, new_val) in differences.items():
                print(f"  {field}: {old_val} -> {new_val}")
            
            # Notify callbacks
            if config_name in self._reload_callbacks:
                for callback in self._reload_callbacks[config_name]:
                    try:
                        await callback(new_config, differences)
                    except Exception as e:
                        print(f"Reload callback error: {e}")
        
        return new_config

# Application components that respond to config changes
class WebServer:
    """Mock web server that responds to configuration changes."""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.running = False
    
    async def start(self):
        """Start the web server."""
        self.running = True
        print(f"Web server started on port {self.config.server_port}")
    
    async def on_config_reload(self, new_config: AppConfig, changes: dict):
        """Handle configuration reload."""
        if "server_port" in changes:
            old_port, new_port = changes["server_port"]
            print(f"Restarting server: port {old_port} -> {new_port}")
            await self.restart(new_config)
        
        if "debug_mode" in changes:
            old_debug, new_debug = changes["debug_mode"]
            print(f"Debug mode changed: {old_debug} -> {new_debug}")
            self.config = new_config
    
    async def restart(self, new_config: AppConfig):
        """Restart server with new configuration."""
        print("Stopping server...")
        self.running = False
        self.config = new_config
        await self.start()

async def hot_reload_example():
    """Example of hot reloading configuration."""
    
    manager = HotReloadConfigManager()
    
    # Initial configuration
    config = AppConfig()
    await manager.register("app", config=config)
    
    # Create application components
    web_server = WebServer(config)
    await web_server.start()
    
    # Register for reload notifications
    manager.on_config_reload("app", web_server.on_config_reload)
    
    # Simulate configuration changes
    print("\nSimulating configuration reload...")
    await manager.hot_reload("app", {
        "server_port": 8080,
        "debug_mode": True,
        "log_level": "DEBUG"
    })
    
    # Simulate another change
    print("\nSimulating another reload...")
    await manager.hot_reload("app", {
        "worker_count": 8,
        "debug_mode": False
    })

asyncio.run(hot_reload_example())
```