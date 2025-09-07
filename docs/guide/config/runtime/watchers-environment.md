# Environment Variable Monitoring

Track environment variable changes with configurable polling for dynamic configuration updates.

## Environment Change Detection

```python
import asyncio
import os
from typing import Dict, Set, Callable, Optional
from attrs import define
from provide.foundation.config import RuntimeConfig, env_field

@define
class WatchedEnvConfig(RuntimeConfig):
    """Configuration loaded from environment variables."""
    
    api_url: str = env_field(
        default="http://localhost:8080",
        env_var="API_URL",
        description="API endpoint URL"
    )
    max_workers: int = env_field(
        default=4,
        env_var="MAX_WORKERS", 
        parser=int,
        description="Maximum worker threads"
    )
    debug_enabled: bool = env_field(
        default=False,
        env_var="DEBUG_ENABLED",
        parser=lambda x: x.lower() in ('true', '1', 'yes', 'on'),
        description="Enable debug mode"
    )
    log_level: str = env_field(
        default="INFO",
        env_var="LOG_LEVEL",
        description="Logging level"
    )

class EnvironmentWatcher:
    """Monitor environment variables for changes."""
    
    def __init__(self, poll_interval: float = 5.0):
        self.poll_interval = poll_interval
        self.watched_vars: Dict[str, str] = {}  # var_name -> current_value
        self.callbacks: Dict[str, list[Callable]] = {}  # var_name -> callbacks
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    def watch_var(self, var_name: str, callback: Callable):
        """Watch an environment variable for changes."""
        current_value = os.getenv(var_name, "")
        self.watched_vars[var_name] = current_value
        
        if var_name not in self.callbacks:
            self.callbacks[var_name] = []
        self.callbacks[var_name].append(callback)
    
    def watch_vars(self, var_names: list[str], callback: Callable):
        """Watch multiple environment variables with single callback."""
        for var_name in var_names:
            self.watch_var(var_name, callback)
    
    async def start(self):
        """Start watching for environment variable changes."""
        if self._running:
            return
            
        self._running = True
        self._task = asyncio.create_task(self._watch_loop())
        print(f"Started environment watcher (poll interval: {self.poll_interval}s)")
    
    async def stop(self):
        """Stop watching for changes."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        print("Stopped environment watcher")
    
    async def _watch_loop(self):
        """Main watching loop."""
        while self._running:
            try:
                changes = self._check_for_changes()
                
                if changes:
                    print(f"Environment changes detected: {list(changes.keys())}")
                    await self._notify_callbacks(changes)
                
                await asyncio.sleep(self.poll_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Environment watcher error: {e}")
                await asyncio.sleep(self.poll_interval)
    
    def _check_for_changes(self) -> Dict[str, tuple[str, str]]:
        """Check for environment variable changes."""
        changes = {}
        
        for var_name, old_value in self.watched_vars.items():
            current_value = os.getenv(var_name, "")
            
            if current_value != old_value:
                changes[var_name] = (old_value, current_value)
                self.watched_vars[var_name] = current_value
        
        return changes
    
    async def _notify_callbacks(self, changes: Dict[str, tuple[str, str]]):
        """Notify callbacks of environment changes."""
        notified_callbacks = set()
        
        for var_name, (old_value, new_value) in changes.items():
            if var_name in self.callbacks:
                for callback in self.callbacks[var_name]:
                    if callback not in notified_callbacks:
                        try:
                            await callback(changes)
                            notified_callbacks.add(callback)
                        except Exception as e:
                            print(f"Callback error for {var_name}: {e}")

async def environment_watching_example():
    """Example of watching environment variables."""
    
    # Initial environment setup
    os.environ["API_URL"] = "http://localhost:8080"
    os.environ["MAX_WORKERS"] = "4"
    os.environ["DEBUG_ENABLED"] = "false"
    os.environ["LOG_LEVEL"] = "INFO"
    
    # Load initial configuration
    config = WatchedEnvConfig.from_env()
    
    print("Initial configuration:")
    print(f"  API URL: {config.api_url}")
    print(f"  Max workers: {config.max_workers}")
    print(f"  Debug: {config.debug_enabled}")
    print(f"  Log level: {config.log_level}")
    
    async def on_config_change(changes: Dict[str, tuple[str, str]]):
        """Handle configuration changes."""
        print("\nEnvironment configuration changed:")
        
        # Reload configuration from environment
        new_config = WatchedEnvConfig.from_env()
        
        for var_name, (old_value, new_value) in changes.items():
            print(f"  {var_name}: {old_value} -> {new_value}")
        
        # Show configuration impact
        print("Updated configuration:")
        print(f"  API URL: {new_config.api_url}")
        print(f"  Max workers: {new_config.max_workers}")
        print(f"  Debug: {new_config.debug_enabled}")
        print(f"  Log level: {new_config.log_level}")
        
        # Here you would typically apply the new configuration
        # to your application components
    
    # Setup environment watcher
    watcher = EnvironmentWatcher(poll_interval=1.0)  # Fast polling for demo
    watcher.watch_vars([
        "API_URL", "MAX_WORKERS", "DEBUG_ENABLED", "LOG_LEVEL"
    ], on_config_change)
    
    await watcher.start()
    
    try:
        # Simulate environment changes
        print("\nSimulating environment variable changes...")
        
        await asyncio.sleep(2)
        os.environ["DEBUG_ENABLED"] = "true"
        os.environ["LOG_LEVEL"] = "DEBUG"
        
        await asyncio.sleep(3)
        os.environ["API_URL"] = "http://api.production.com"
        os.environ["MAX_WORKERS"] = "8"
        
        await asyncio.sleep(3)
        os.environ["LOG_LEVEL"] = "ERROR"
        
        # Wait for final changes to be detected
        await asyncio.sleep(2)
        
    finally:
        await watcher.stop()

# Run example
asyncio.run(environment_watching_example())
```

## Configuration Health Monitoring

```python
import asyncio
import os
from typing import Dict, Any, Optional
from attrs import define
from provide.foundation.config import BaseConfig, field
from provide.foundation.health import HealthCheck

@define  
class MonitoredConfig(BaseConfig):
    """Configuration with health monitoring."""
    
    service_url: str = field(description="Service endpoint URL")
    timeout_seconds: int = field(description="Request timeout")
    retry_count: int = field(description="Number of retries")
    feature_flags: dict[str, bool] = field(factory=dict, description="Feature toggles")

class ConfigHealthMonitor:
    """Monitor configuration health and validity."""
    
    def __init__(self, config: MonitoredConfig):
        self.config = config
        self.health_checks = []
        self.last_check_time = 0
        self.health_status = {"healthy": True, "issues": []}
    
    def add_health_check(self, name: str, check_func: Callable):
        """Add a configuration health check."""
        self.health_checks.append((name, check_func))
    
    async def check_health(self) -> Dict[str, Any]:
        """Run all health checks on current configuration."""
        issues = []
        
        for check_name, check_func in self.health_checks:
            try:
                result = await check_func(self.config)
                if not result.get("healthy", True):
                    issues.extend(result.get("issues", [f"{check_name} failed"]))
            except Exception as e:
                issues.append(f"{check_name} error: {str(e)}")
        
        self.health_status = {
            "healthy": len(issues) == 0,
            "issues": issues,
            "check_count": len(self.health_checks),
            "timestamp": asyncio.get_event_loop().time()
        }
        
        return self.health_status

async def config_health_check_example():
    """Example of configuration health monitoring."""
    
    # Setup configuration
    config = MonitoredConfig(
        service_url="http://api.example.com",
        timeout_seconds=30,
        retry_count=3,
        feature_flags={"new_feature": True, "legacy_mode": False}
    )
    
    # Create health monitor
    monitor = ConfigHealthMonitor(config)
    
    # Define health checks
    async def check_service_url(config: MonitoredConfig) -> Dict[str, Any]:
        """Check if service URL is reachable."""
        import aiohttp
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(config.service_url) as response:
                    if response.status < 400:
                        return {"healthy": True}
                    else:
                        return {"healthy": False, "issues": [f"Service returned {response.status}"]}
        except Exception as e:
            return {"healthy": False, "issues": [f"Service unreachable: {str(e)}"]}
    
    async def check_timeout_range(config: MonitoredConfig) -> Dict[str, Any]:
        """Check if timeout is within reasonable range."""
        if 1 <= config.timeout_seconds <= 300:
            return {"healthy": True}
        else:
            return {"healthy": False, "issues": [f"Timeout {config.timeout_seconds}s outside range 1-300"]}
    
    async def check_retry_count(config: MonitoredConfig) -> Dict[str, Any]:
        """Check if retry count is reasonable."""
        if 0 <= config.retry_count <= 10:
            return {"healthy": True}
        else:
            return {"healthy": False, "issues": [f"Retry count {config.retry_count} outside range 0-10"]}
    
    # Add health checks
    monitor.add_health_check("service_connectivity", check_service_url)
    monitor.add_health_check("timeout_validation", check_timeout_range)
    monitor.add_health_check("retry_validation", check_retry_count)
    
    # Initial health check
    print("Running initial configuration health check...")
    health_status = await monitor.check_health()
    
    print(f"Configuration healthy: {health_status['healthy']}")
    if health_status['issues']:
        print("Issues found:")
        for issue in health_status['issues']:
            print(f"  - {issue}")
    
    # Simulate configuration change that causes health issues
    print("\nSimulating problematic configuration change...")
    config.timeout_seconds = 500  # Outside valid range
    config.retry_count = 15       # Too many retries
    
    health_status = await monitor.check_health()
    print(f"Configuration healthy: {health_status['healthy']}")
    if health_status['issues']:
        print("Issues found:")
        for issue in health_status['issues']:
            print(f"  - {issue}")

# Run example
asyncio.run(config_health_check_example())
```

## Next Steps

- [Multi-Source Sync](watchers-sync.md) - Synchronize multiple configuration sources
- [File Watching](watchers-files.md) - Monitor configuration files for changes  
- [Remote Configuration](remote.md) - Remote config sources and synchronization