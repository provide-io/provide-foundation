# Multi-Source Configuration Synchronization

Synchronize configuration across multiple sources with priority handling and conflict resolution.

## Multi-Source Synchronization

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
        "feature_enabled": False,
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
        "feature_enabled": False  # This won't override env var due to lower priority
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

## Advanced Synchronization Patterns

```python
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from attrs import define
from provide.foundation.config import BaseConfig, field

@define
class AdvancedSyncConfig(BaseConfig):
    """Configuration with advanced synchronization features."""
    
    database_url: str = field(description="Database connection URL")
    cache_enabled: bool = field(default=True, description="Enable caching")
    worker_pool_size: int = field(default=4, description="Worker pool size")
    feature_toggles: dict[str, bool] = field(factory=dict, description="Feature flags")
    rate_limits: dict[str, int] = field(factory=dict, description="Rate limiting rules")

class AdvancedConfigSync:
    """Advanced configuration synchronization with conflict resolution."""
    
    def __init__(self, config_name: str):
        self.config_name = config_name
        self.sources: List[Dict[str, Any]] = []
        self.merge_strategies = {
            "override": self._merge_override,
            "merge_dict": self._merge_dict,
            "append_list": self._merge_append_list,
            "union_set": self._merge_union_set
        }
        self.field_strategies: Dict[str, str] = {}
    
    def add_source(self, name: str, loader_func: Callable, priority: int = 10, 
                   merge_strategy: str = "override"):
        """Add configuration source with custom merge strategy."""
        self.sources.append({
            "name": name,
            "loader": loader_func,
            "priority": priority,
            "merge_strategy": merge_strategy
        })
        # Sort by priority after adding
        self.sources.sort(key=lambda x: x["priority"])
    
    def set_field_strategy(self, field_name: str, strategy: str):
        """Set merge strategy for specific field."""
        self.field_strategies[field_name] = strategy
    
    async def sync_with_resolution(self) -> Optional[AdvancedSyncConfig]:
        """Synchronize configuration with advanced conflict resolution."""
        print(f"Syncing configuration from {len(self.sources)} sources...")
        
        # Load all source data
        source_configs = []
        for source in self.sources:
            try:
                data = await source["loader"]()
                if data:
                    source_configs.append({
                        "name": source["name"],
                        "data": data,
                        "priority": source["priority"],
                        "merge_strategy": source["merge_strategy"]
                    })
                    print(f"  Loaded from {source['name']}: {len(data)} keys")
            except Exception as e:
                print(f"  Failed to load from {source['name']}: {e}")
        
        if not source_configs:
            return None
        
        # Merge configurations
        merged = await self._merge_configurations(source_configs)
        
        # Create final configuration
        return AdvancedSyncConfig.from_dict(merged)
    
    async def _merge_configurations(self, source_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge configurations using various strategies."""
        final_config = {}
        source_tracking = {}
        
        # Get all unique keys across sources
        all_keys = set()
        for config in source_configs:
            all_keys.update(config["data"].keys())
        
        # Merge each key
        for key in all_keys:
            values_for_key = []
            
            # Collect values from all sources that have this key
            for config in source_configs:
                if key in config["data"]:
                    values_for_key.append({
                        "value": config["data"][key],
                        "source": config["name"],
                        "priority": config["priority"],
                        "strategy": self.field_strategies.get(key, config["merge_strategy"])
                    })
            
            if values_for_key:
                # Sort by priority and apply merge strategy
                values_for_key.sort(key=lambda x: x["priority"])
                final_value, source_used = await self._resolve_field_conflict(key, values_for_key)
                
                final_config[key] = final_value
                source_tracking[key] = source_used
        
        # Show resolution summary
        print("Configuration resolution:")
        for key, sources in source_tracking.items():
            print(f"  {key}: {sources}")
        
        return final_config
    
    async def _resolve_field_conflict(self, field_name: str, 
                                    values: List[Dict[str, Any]]) -> tuple[Any, str]:
        """Resolve conflicts for a specific field."""
        if len(values) == 1:
            return values[0]["value"], values[0]["source"]
        
        strategy = values[0]["strategy"]  # Use highest priority source's strategy
        
        if strategy in self.merge_strategies:
            return await self.merge_strategies[strategy](field_name, values)
        else:
            # Default to override (highest priority wins)
            return values[0]["value"], values[0]["source"]
    
    async def _merge_override(self, field_name: str, values: List[Dict[str, Any]]) -> tuple[Any, str]:
        """Override merge: highest priority wins."""
        return values[0]["value"], values[0]["source"]
    
    async def _merge_dict(self, field_name: str, values: List[Dict[str, Any]]) -> tuple[Any, str]:
        """Dictionary merge: combine all dict values."""
        merged_dict = {}
        sources_used = []
        
        # Merge in reverse priority order so high priority overwrites
        for value_info in reversed(values):
            if isinstance(value_info["value"], dict):
                merged_dict.update(value_info["value"])
                sources_used.append(value_info["source"])
        
        return merged_dict, "+".join(sources_used)
    
    async def _merge_append_list(self, field_name: str, values: List[Dict[str, Any]]) -> tuple[Any, str]:
        """List merge: append all list values."""
        merged_list = []
        sources_used = []
        
        for value_info in values:
            if isinstance(value_info["value"], list):
                merged_list.extend(value_info["value"])
                sources_used.append(value_info["source"])
        
        return merged_list, "+".join(sources_used)
    
    async def _merge_union_set(self, field_name: str, values: List[Dict[str, Any]]) -> tuple[Any, str]:
        """Set merge: union of all values."""
        merged_set = set()
        sources_used = []
        
        for value_info in values:
            if isinstance(value_info["value"], (list, set)):
                merged_set.update(value_info["value"])
                sources_used.append(value_info["source"])
        
        return list(merged_set), "+".join(sources_used)

async def advanced_sync_example():
    """Example of advanced configuration synchronization."""
    
    # Setup test data
    config_dir = Path("/tmp/advanced_sync")
    config_dir.mkdir(exist_ok=True)
    
    # Base config
    base_file = config_dir / "base.json"
    base_file.write_text(json.dumps({
        "database_url": "sqlite:///base.db",
        "cache_enabled": True,
        "worker_pool_size": 4,
        "feature_toggles": {
            "feature_a": False,
            "feature_b": True
        },
        "rate_limits": {
            "api": 100,
            "uploads": 10
        }
    }, indent=2))
    
    # Environment overrides
    env_file = config_dir / "env.json"
    env_file.write_text(json.dumps({
        "database_url": "postgres://prod-db:5432/myapp",
        "worker_pool_size": 8,
        "feature_toggles": {
            "feature_a": True,
            "feature_c": True
        },
        "rate_limits": {
            "api": 1000
        }
    }, indent=2))
    
    # Local overrides  
    local_file = config_dir / "local.json"
    local_file.write_text(json.dumps({
        "cache_enabled": False,
        "feature_toggles": {
            "debug_mode": True
        },
        "rate_limits": {
            "debug": 5
        }
    }, indent=2))
    
    # Source loaders
    async def load_base():
        return json.loads(base_file.read_text())
    
    async def load_env():
        return json.loads(env_file.read_text())
    
    async def load_local():
        return json.loads(local_file.read_text())
    
    # Setup advanced sync
    sync = AdvancedConfigSync("advanced")
    
    # Add sources with different priorities and merge strategies
    sync.add_source("base", load_base, priority=30, merge_strategy="override")
    sync.add_source("environment", load_env, priority=20, merge_strategy="override")
    sync.add_source("local", load_local, priority=10, merge_strategy="override")
    
    # Set field-specific merge strategies
    sync.set_field_strategy("feature_toggles", "merge_dict")  # Merge feature flags
    sync.set_field_strategy("rate_limits", "merge_dict")      # Merge rate limits
    
    # Perform synchronization
    final_config = await sync.sync_with_resolution()
    
    if final_config:
        print("\nFinal merged configuration:")
        print(f"  Database URL: {final_config.database_url}")
        print(f"  Cache enabled: {final_config.cache_enabled}")
        print(f"  Worker pool size: {final_config.worker_pool_size}")
        print(f"  Feature toggles: {final_config.feature_toggles}")
        print(f"  Rate limits: {final_config.rate_limits}")
    
    # Cleanup
    import shutil
    if config_dir.exists():
        shutil.rmtree(config_dir)

# Run example
asyncio.run(advanced_sync_example())
```

## Next Steps

- [Remote Configuration](remote.md) - Remote config sources and synchronization
- [File Watching](watchers-files.md) - Monitor configuration files for changes
- [Environment Monitoring](watchers-environment.md) - Track environment variable changes