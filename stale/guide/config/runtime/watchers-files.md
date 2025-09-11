# File Watching

Monitor configuration files for changes and reload automatically when they are modified.

## Basic File Watcher

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

## Multi-File Configuration Watching

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

## Next Steps

- [Environment Monitoring](watchers-environment.md) - Watch environment variables for changes
- [Multi-Source Sync](watchers-sync.md) - Synchronize multiple configuration sources
- [Configuration Loading](../files-loading.md) - Basic configuration loading patterns