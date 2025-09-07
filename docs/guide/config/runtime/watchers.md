# Configuration Watchers

File and environment variable watching for automatic configuration updates.

## File Watching

### Basic File Watcher

```python
import asyncio
import json
from pathlib import Path
from typing import Callable, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from attrs import define
from provide.foundation.config import BaseConfig, ConfigManager, field

@define
class WatchedConfig(BaseConfig):
    """Configuration that can be watched for changes."""
    
    api_key: str = field(default="default-key", description="API key")
    timeout: int = field(default=30, description="Request timeout")
    enabled: bool = field(default=True, description="Feature enabled")
    endpoints: list[str] = field(factory=list, description="API endpoints")

class ConfigFileWatcher(FileSystemEventHandler):
    """File system event handler for configuration files."""
    
    def __init__(self, file_path: Path, reload_callback: Callable):
        """
        Initialize file watcher.
        
        Args:
            file_path: Path to configuration file to watch
            reload_callback: Function to call when file changes
        """
        self.file_path = file_path
        self.reload_callback = reload_callback
        
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and Path(event.src_path) == self.file_path:
            print(f"Configuration file changed: {self.file_path}")
            asyncio.create_task(self.reload_callback())
    
    def on_moved(self, event):
        """Handle file move events (editor saves often do atomic moves)."""
        if not event.is_directory and Path(event.dest_path) == self.file_path:
            print(f"Configuration file moved/updated: {self.file_path}")
            asyncio.create_task(self.reload_callback())

async def file_watching_example():
    """Example of watching configuration files for changes."""
    
    # Create configuration file
    config_file = Path("/tmp/watched_config.json")
    initial_config = {
        "api_key": "initial-key",
        "timeout": 30,
        "enabled": True,
        "endpoints": ["http://api.example.com"]
    }
    
    config_file.write_text(json.dumps(initial_config, indent=2))
    
    # Setup configuration manager
    manager = ConfigManager()
    config = WatchedConfig.from_dict(initial_config)
    await manager.register("watched", config=config)
    
    async def reload_config():
        """Reload configuration from file."""
        try:
            # Small delay to ensure file write is complete
            await asyncio.sleep(0.1)
            
            if config_file.exists():
                new_data = json.loads(config_file.read_text())
                
                # Get current config for comparison
                current_config = await manager.get("watched")
                
                # Update configuration
                await manager.update("watched", new_data)
                updated_config = await manager.get("watched")
                
                # Show changes
                differences = current_config.diff(updated_config)
                if differences:
                    print("Configuration updated:")
                    for field, (old_val, new_val) in differences.items():
                        print(f"  {field}: {old_val} -> {new_val}")
                else:
                    print("No configuration changes detected")
                    
        except Exception as e:
            print(f"Error reloading configuration: {e}")
    
    # Setup file watcher
    event_handler = ConfigFileWatcher(config_file, reload_config)
    observer = Observer()
    observer.schedule(event_handler, str(config_file.parent), recursive=False)
    observer.start()
    
    try:
        print(f"Watching configuration file: {config_file}")
        print("Initial configuration:")
        initial = await manager.get("watched")
        print(f"  API Key: {initial.api_key}")
        print(f"  Timeout: {initial.timeout}")
        print(f"  Enabled: {initial.enabled}")
        
        # Simulate file changes
        print("\nSimulating configuration changes...")
        
        # First change
        await asyncio.sleep(1)
        updated_config = {
            "api_key": "updated-key-123",
            "timeout": 60,
            "enabled": True,
            "endpoints": ["http://api.example.com", "http://backup.example.com"]
        }
        config_file.write_text(json.dumps(updated_config, indent=2))
        
        # Second change  
        await asyncio.sleep(2)
        final_config = {
            "api_key": "final-key-456",
            "timeout": 45,
            "enabled": False,
            "endpoints": ["http://new-api.example.com"]
        }
        config_file.write_text(json.dumps(final_config, indent=2))
        
        # Wait for file events to be processed
        await asyncio.sleep(1)
        
    finally:
        observer.stop()
        observer.join()
        
        # Cleanup
        if config_file.exists():
            config_file.unlink()

# Run example
asyncio.run(file_watching_example())
```

### Multi-File Configuration Watching

```python
import asyncio
import json
import yaml
from pathlib import Path
from typing import Dict, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MultiFileConfigWatcher(FileSystemEventHandler):
    """Watch multiple configuration files simultaneously."""
    
    def __init__(self):
        self.watched_files: Dict[Path, str] = {}  # file_path -> config_name
        self.reload_callbacks: Dict[str, Callable] = {}
        self.debounce_delays: Dict[Path, float] = {}
        self._pending_reloads: Set[str] = set()
    
    def add_file(self, file_path: Path, config_name: str, reload_callback: Callable, debounce_delay: float = 0.5):
        """Add a file to watch."""
        self.watched_files[file_path] = config_name
        self.reload_callbacks[config_name] = reload_callback
        self.debounce_delays[file_path] = debounce_delay
    
    def on_modified(self, event):
        """Handle file modification with debouncing."""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if file_path in self.watched_files:
            config_name = self.watched_files[file_path]
            
            # Debounce rapid file changes
            if config_name not in self._pending_reloads:
                self._pending_reloads.add(config_name)
                delay = self.debounce_delays[file_path]
                asyncio.create_task(self._debounced_reload(config_name, delay))
    
    async def _debounced_reload(self, config_name: str, delay: float):
        """Reload configuration after debounce delay."""
        await asyncio.sleep(delay)
        
        try:
            if config_name in self.reload_callbacks:
                await self.reload_callbacks[config_name]()
        finally:
            self._pending_reloads.discard(config_name)

async def multi_file_watching_example():
    """Example of watching multiple configuration files."""
    
    # Create multiple config files
    config_dir = Path("/tmp/multi_config")
    config_dir.mkdir(exist_ok=True)
    
    # Main app config (JSON)
    app_config_file = config_dir / "app.json"
    app_config_file.write_text(json.dumps({
        "name": "MyApp",
        "version": "1.0.0",
        "debug": False
    }, indent=2))
    
    # Database config (YAML)
    db_config_file = config_dir / "database.yml"
    db_config_file.write_text(yaml.dump({
        "host": "localhost",
        "port": 5432,
        "database": "myapp"
    }))
    
    # Feature flags (JSON)
    features_file = config_dir / "features.json"
    features_file.write_text(json.dumps({
        "new_ui": False,
        "analytics": True,
        "caching": True
    }, indent=2))
    
    # Configuration storage
    configs = {
        "app": {},
        "database": {}, 
        "features": {}
    }
    
    # Reload callbacks
    async def reload_app_config():
        """Reload application configuration."""
        try:
            data = json.loads(app_config_file.read_text())
            old_config = configs["app"]
            configs["app"] = data
            
            print("App configuration reloaded:")
            for key, value in data.items():
                old_value = old_config.get(key, "N/A")
                if old_value != value:
                    print(f"  {key}: {old_value} -> {value}")
                    
        except Exception as e:
            print(f"Error reloading app config: {e}")
    
    async def reload_db_config():
        """Reload database configuration."""
        try:
            data = yaml.safe_load(db_config_file.read_text())
            old_config = configs["database"]
            configs["database"] = data
            
            print("Database configuration reloaded:")
            for key, value in data.items():
                old_value = old_config.get(key, "N/A")
                if old_value != value:
                    print(f"  {key}: {old_value} -> {value}")
                    
        except Exception as e:
            print(f"Error reloading database config: {e}")
    
    async def reload_features_config():
        """Reload feature flags."""
        try:
            data = json.loads(features_file.read_text())
            old_config = configs["features"]
            configs["features"] = data
            
            print("Feature flags reloaded:")
            for key, value in data.items():
                old_value = old_config.get(key, "N/A")
                if old_value != value:
                    print(f"  {key}: {old_value} -> {value}")
                    
        except Exception as e:
            print(f"Error reloading features config: {e}")
    
    # Setup multi-file watcher
    watcher = MultiFileConfigWatcher()
    watcher.add_file(app_config_file, "app", reload_app_config, debounce_delay=0.3)
    watcher.add_file(db_config_file, "database", reload_db_config, debounce_delay=0.5)
    watcher.add_file(features_file, "features", reload_features_config, debounce_delay=0.2)
    
    # Start watching
    observer = Observer()
    observer.schedule(watcher, str(config_dir), recursive=True)
    observer.start()
    
    try:
        print(f"Watching configuration directory: {config_dir}")
        
        # Load initial configs
        await reload_app_config()
        await reload_db_config() 
        await reload_features_config()
        
        print("\nSimulating configuration changes...")
        
        # Simulate changes to different files
        await asyncio.sleep(1)
        
        # Update app config
        app_config_file.write_text(json.dumps({
            "name": "MyApp",
            "version": "1.1.0",
            "debug": True
        }, indent=2))
        
        await asyncio.sleep(1)
        
        # Update features
        features_file.write_text(json.dumps({
            "new_ui": True,
            "analytics": True,
            "caching": False,
            "beta_features": True
        }, indent=2))
        
        await asyncio.sleep(1)
        
        # Update database config
        db_config_file.write_text(yaml.dump({
            "host": "prod-db.example.com",
            "port": 5432,
            "database": "myapp_prod",
            "ssl": True
        }))
        
        # Wait for all changes to be processed
        await asyncio.sleep(2)
        
    finally:
        observer.stop()
        observer.join()
        
        # Cleanup
        import shutil
        if config_dir.exists():
            shutil.rmtree(config_dir)

# Run example
asyncio.run(multi_file_watching_example())
```

## Environment Variable Watching

### Environment Change Detection

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

## Configuration Synchronization

### Multi-Source Synchronization

```python
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, Optional
from attrs import define
from provide.foundation.config import BaseConfig, ConfigManager, field

@define
class SyncedConfig(BaseConfig):
    """Configuration that synchronizes across multiple sources."""
    
    feature_enabled: bool = field(default=False, description="Feature enabled")
    rate_limit: int = field(default=100, description="Rate limit")  
    timeout_ms: int = field(default=5000, description="Timeout milliseconds")
    api_version: str = field(default="v1", description="API version")

class MultiSourceConfigSync:
    """Synchronize configuration across file, environment, and remote sources."""
    
    def __init__(self, config_name: str, manager: ConfigManager):
        self.config_name = config_name
        self.manager = manager
        self.sources = {}  # source_name -> source_handler
        self.last_sync_time = 0
        
    def add_file_source(self, file_path: Path, priority: int = 10):
        """Add file as configuration source."""
        self.sources[f"file:{file_path}"] = {
            "type": "file",
            "path": file_path,
            "priority": priority,
            "loader": self._load_from_file
        }
    
    def add_env_source(self, env_prefix: str, priority: int = 20):
        """Add environment variables as configuration source."""
        self.sources[f"env:{env_prefix}"] = {
            "type": "env",
            "prefix": env_prefix,
            "priority": priority,
            "loader": self._load_from_env
        }
    
    async def _load_from_file(self, source_info: dict) -> Dict[str, Any]:
        """Load configuration from file."""
        file_path = source_info["path"]
        if not file_path.exists():
            return {}
        
        try:
            content = file_path.read_text()
            return json.loads(content)
        except Exception as e:
            print(f"Error loading from file {file_path}: {e}")
            return {}
    
    async def _load_from_env(self, source_info: dict) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        import os
        prefix = source_info["prefix"]
        config = {}
        
        env_mappings = {
            f"{prefix}_FEATURE_ENABLED": ("feature_enabled", lambda x: x.lower() == 'true'),
            f"{prefix}_RATE_LIMIT": ("rate_limit", int),
            f"{prefix}_TIMEOUT_MS": ("timeout_ms", int),
            f"{prefix}_API_VERSION": ("api_version", str),
        }
        
        for env_var, (config_key, parser) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    config[config_key] = parser(value)
                except Exception as e:
                    print(f"Error parsing {env_var}={value}: {e}")
        
        return config
    
    async def sync_configuration(self) -> Optional[SyncedConfig]:
        """Synchronize configuration from all sources."""
        print(f"Synchronizing configuration from {len(self.sources)} sources")
        
        # Load from all sources
        source_data = []
        for source_name, source_info in self.sources.items():
            data = await source_info["loader"](source_info)
            if data:
                source_data.append((source_info["priority"], source_name, data))
        
        # Sort by priority (lower number = higher priority)
        source_data.sort(key=lambda x: x[0])
        
        # Merge configuration with priority order
        merged_config = {}
        source_tracking = {}
        
        for priority, source_name, data in source_data:
            for key, value in data.items():
                if key not in merged_config:  # First source wins for each key
                    merged_config[key] = value
                    source_tracking[key] = source_name
        
        if merged_config:
            print("Configuration sources:")
            for key, source in source_tracking.items():
                print(f"  {key}: {source}")
            
            # Update configuration
            await self.manager.update(self.config_name, merged_config)
            updated_config = await self.manager.get(self.config_name)
            
            self.last_sync_time = asyncio.get_event_loop().time()
            return updated_config
        
        return None

async def multi_source_sync_example():
    """Example of multi-source configuration synchronization."""
    
    # Setup temporary files and environment
    config_dir = Path("/tmp/config_sync")
    config_dir.mkdir(exist_ok=True)
    
    # Primary config file (low priority)
    primary_config = config_dir / "config.json"
    primary_config.write_text(json.dumps({
        "feature_enabled": false,
        "rate_limit": 100,
        "timeout_ms": 5000,
        "api_version": "v1"
    }, indent=2))
    
    # Override config file (medium priority) 
    override_config = config_dir / "overrides.json"
    override_config.write_text(json.dumps({
        "rate_limit": 200,
        "timeout_ms": 10000
    }, indent=2))
    
    # Environment variables (high priority)
    import os
    os.environ["MYAPP_FEATURE_ENABLED"] = "true"
    os.environ["MYAPP_API_VERSION"] = "v2"
    
    # Setup configuration manager
    manager = ConfigManager()
    initial_config = SyncedConfig()
    await manager.register("synced", config=initial_config)
    
    # Setup multi-source sync
    sync = MultiSourceConfigSync("synced", manager)
    sync.add_file_source(primary_config, priority=30)      # Lowest priority
    sync.add_file_source(override_config, priority=20)     # Medium priority  
    sync.add_env_source("MYAPP", priority=10)             # Highest priority
    
    # Initial synchronization
    print("Performing initial synchronization...")
    synced_config = await sync.sync_configuration()
    
    if synced_config:
        print("\nFinal synchronized configuration:")
        print(f"  Feature enabled: {synced_config.feature_enabled}")  # From env (high priority)
        print(f"  Rate limit: {synced_config.rate_limit}")           # From override file (medium)
        print(f"  Timeout: {synced_config.timeout_ms}")              # From override file (medium)
        print(f"  API version: {synced_config.api_version}")         # From env (high priority)
    
    # Simulate configuration changes
    print("\nSimulating configuration source changes...")
    
    # Change override file
    override_config.write_text(json.dumps({
        "rate_limit": 500,
        "timeout_ms": 15000,
        "feature_enabled": false  # This won't override env var due to lower priority
    }, indent=2))
    
    # Re-sync
    updated_config = await sync.sync_configuration()
    
    if updated_config:
        print("\nAfter file update:")
        print(f"  Feature enabled: {updated_config.feature_enabled}")  # Still from env
        print(f"  Rate limit: {updated_config.rate_limit}")           # Updated from file
        print(f"  Timeout: {updated_config.timeout_ms}")              # Updated from file
        print(f"  API version: {updated_config.api_version}")         # Still from env
    
    # Cleanup
    import shutil
    if config_dir.exists():
        shutil.rmtree(config_dir)

# Run example
asyncio.run(multi_source_sync_example())
```