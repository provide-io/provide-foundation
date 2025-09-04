# Configuration Loaders API

Configuration loading classes that support multiple formats, sources, and loading strategies with async I/O.

## Overview

Configuration loaders provide the interface for loading configuration data from various sources:

- **File formats**: JSON, YAML, TOML, INI, ENV
- **Multiple sources**: Files, environment variables, dictionaries
- **Loading strategies**: Single source, multi-source merging, chained fallback
- **Async I/O**: Non-blocking file operations with aiofiles

## Base Classes

### ConfigLoader

Abstract base class for all configuration loaders.

```python
class ConfigLoader(ABC):
    """Abstract base class for configuration loaders."""
    
    @abstractmethod
    async def load(self, config_class: type[T]) -> T:
        """Load configuration and return instance of config_class."""
        
    @abstractmethod
    def exists(self) -> bool:
        """Check if the configuration source exists."""
```

All loaders implement these methods to provide consistent interface for the ConfigManager.

## File-based Loaders

### FileConfigLoader

Load configuration from files with automatic format detection.

```python
class FileConfigLoader(ConfigLoader):
    """Load configuration from files."""
    
    def __init__(
        self,
        path: str | Path,
        format: ConfigFormat | None = None,
        encoding: str = "utf-8",
    ) -> None:
        """
        Initialize file configuration loader.
        
        Args:
            path: Path to configuration file
            format: File format (auto-detected if None)
            encoding: File encoding
        """
```

#### Supported Formats

- **JSON** (`.json`) - Standard JSON format
- **YAML** (`.yaml`, `.yml`) - YAML format using PyYAML
- **TOML** (`.toml`) - TOML format using tomllib/tomli
- **INI** (`.ini`, `.cfg`) - INI format using configparser
- **ENV** (`.env`) - Environment file format

#### Methods

##### load(config_class)

Load configuration from file.

```python
async def load(self, config_class: type[T]) -> T:
    """
    Load configuration from file.
    
    Returns:
        Configuration instance with source=ConfigSource.FILE
    """
```

##### exists()

Check if configuration file exists.

```python
def exists(self) -> bool:
    """Check if configuration file exists."""
```

#### Usage Examples

```python
from provide.foundation.config.loader import FileConfigLoader

# JSON configuration
loader = FileConfigLoader("config.json")
config = await loader.load(AppConfig)

# YAML with explicit format
loader = FileConfigLoader("settings.yaml", format=ConfigFormat.YAML)
config = await loader.load(AppConfig)

# Auto-detection based on extension
loader = FileConfigLoader("app.toml")  # Automatically detects TOML format
config = await loader.load(AppConfig)
```

#### File Format Examples

**JSON** (`config.json`):
```json
{
    "name": "myapp",
    "debug": true,
    "database": {
        "host": "localhost",
        "port": 5432
    }
}
```

**YAML** (`config.yaml`):
```yaml
name: myapp
debug: true
database:
  host: localhost
  port: 5432
```

**TOML** (`config.toml`):
```toml
name = "myapp"
debug = true

[database]
host = "localhost"
port = 5432
```

**ENV** (`config.env`):
```env
NAME=myapp
DEBUG=true
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### Environment-based Loaders

### EnvConfigLoader

Load configuration from environment variables.

```python
class EnvConfigLoader(ConfigLoader):
    """Load configuration from environment variables."""
    
    def __init__(
        self, 
        prefix: str = "", 
        delimiter: str = "_", 
        case_sensitive: bool = False
    ) -> None:
        """
        Initialize environment configuration loader.
        
        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive
        """
```

#### Methods

##### load(config_class)

Load configuration from environment variables.

```python
async def load(self, config_class: type[T]) -> T:
    """
    Load configuration from environment variables.
    
    Note: config_class must inherit from EnvConfig
    """
```

##### exists()

Check if any relevant environment variables exist.

```python
def exists(self) -> bool:
    """Check if any relevant environment variables exist."""
```

#### Usage Example

```python
# Environment variables:
# MYAPP_DATABASE_HOST=postgres.example.com
# MYAPP_DATABASE_PORT=5432
# MYAPP_DEBUG=true

loader = EnvConfigLoader(prefix="MYAPP")
config = await loader.load(DatabaseConfig)  # Must inherit from EnvConfig
```

## Composite Loaders

### DictConfigLoader

Load configuration from a dictionary (useful for testing and runtime configuration).

```python
class DictConfigLoader(ConfigLoader):
    """Load configuration from a dictionary."""
    
    def __init__(
        self, 
        data: ConfigDict, 
        source: ConfigSource = ConfigSource.RUNTIME
    ) -> None:
        """
        Initialize dictionary configuration loader.
        
        Args:
            data: Configuration data
            source: Source of the configuration
        """
```

#### Usage Example

```python
config_data = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}

loader = DictConfigLoader(config_data, source=ConfigSource.RUNTIME)
config = await loader.load(AppConfig)
```

### MultiSourceLoader

Load and merge configuration from multiple sources with precedence.

```python
class MultiSourceLoader(ConfigLoader):
    """Load configuration from multiple sources with precedence."""
    
    def __init__(self, *loaders: ConfigLoader) -> None:
        """
        Initialize multi-source configuration loader.
        
        Args:
            *loaders: Configuration loaders in order of precedence 
                     (later overrides earlier)
        """
```

#### Features

- **Source precedence**: Later loaders override earlier ones
- **Source tracking**: Each field tracks its source
- **Partial loading**: Works even if some sources are unavailable

#### Usage Example

```python
# Load with precedence: base config < environment < local overrides
loader = MultiSourceLoader(
    FileConfigLoader("config/base.yaml"),     # Base configuration
    EnvConfigLoader(prefix="APP"),            # Environment overrides  
    FileConfigLoader("config/local.yaml"),   # Local development overrides
)

config = await loader.load(AppConfig)

# Check source of specific fields
print(f"Debug source: {config.get_source('debug')}")  # Might be ConfigSource.FILE
print(f"Port source: {config.get_source('port')}")    # Might be ConfigSource.ENV
```

### ChainedLoader

Try multiple loaders until one succeeds (fallback pattern).

```python
class ChainedLoader(ConfigLoader):
    """Try multiple loaders until one succeeds."""
    
    def __init__(self, *loaders: ConfigLoader) -> None:
        """
        Initialize chained configuration loader.
        
        Args:
            *loaders: Configuration loaders to try in order
        """
```

#### Usage Example

```python
# Try loading from different locations
loader = ChainedLoader(
    FileConfigLoader("config/production.yaml"),  # Try production config first
    FileConfigLoader("config/default.yaml"),    # Fall back to default
    DictConfigLoader({"debug": True}),          # Final fallback
)

config = await loader.load(AppConfig)
```

## Advanced Usage Patterns

### Configuration Environments

```python
import os

def create_loader_for_environment() -> ConfigLoader:
    """Create loader based on deployment environment."""
    env = os.getenv("ENVIRONMENT", "development")
    
    base_loaders = [
        FileConfigLoader("config/base.yaml"),
        EnvConfigLoader(prefix="APP"),
    ]
    
    if env == "production":
        return MultiSourceLoader(
            *base_loaders,
            FileConfigLoader("config/production.yaml"),
        )
    elif env == "testing":
        return MultiSourceLoader(
            *base_loaders,
            DictConfigLoader({"debug": True, "database_url": "sqlite:///:memory:"}),
        )
    else:  # development
        return MultiSourceLoader(
            *base_loaders,
            FileConfigLoader("config/development.yaml"),
        )

# Usage
loader = create_loader_for_environment()
config = await loader.load(AppConfig)
```

### Hot Configuration Reloading

```python
import asyncio
from pathlib import Path

class WatchingFileLoader(FileConfigLoader):
    """File loader that supports change detection."""
    
    def __init__(self, path: str | Path, **kwargs):
        super().__init__(path, **kwargs)
        self._last_modified = None
        
    def has_changed(self) -> bool:
        """Check if file has been modified."""
        if not self.exists():
            return False
            
        current_modified = self.path.stat().st_mtime
        if self._last_modified is None:
            self._last_modified = current_modified
            return True
            
        if current_modified > self._last_modified:
            self._last_modified = current_modified
            return True
            
        return False

# Usage with ConfigManager
async def setup_hot_reload():
    loader = WatchingFileLoader("config.yaml")
    
    # Initial load
    config = await manager.load("app", AppConfig, loader=loader)
    
    # Watch for changes
    while True:
        await asyncio.sleep(5)  # Check every 5 seconds
        if loader.has_changed():
            print("Configuration file changed, reloading...")
            config = await manager.reload("app")
```

### Custom Loader Implementation

```python
class DatabaseConfigLoader(ConfigLoader):
    """Load configuration from database."""
    
    def __init__(self, connection_string: str, table: str = "config"):
        self.connection_string = connection_string
        self.table = table
        
    def exists(self) -> bool:
        # Check if database table exists
        # Implementation depends on your database library
        return True
        
    async def load(self, config_class: type[T]) -> T:
        # Connect to database and load configuration
        async with get_db_connection(self.connection_string) as conn:
            query = f"SELECT key, value FROM {self.table}"
            rows = await conn.fetch(query)
            
            data = {row['key']: row['value'] for row in rows}
            return config_class.from_dict(data, source=ConfigSource.RUNTIME)

# Usage
loader = DatabaseConfigLoader("postgresql://user:pass@localhost/config")
config = await loader.load(AppConfig)
```

## Error Handling

Loaders raise specific exceptions for different failure modes:

```python
from provide.foundation.errors.config import ConfigurationError
from provide.foundation.errors.resources import NotFoundError

try:
    config = await loader.load(AppConfig)
except NotFoundError as e:
    print(f"Configuration source not found: {e.message}")
except ConfigurationError as e:
    print(f"Configuration loading failed: {e.message}")
    print(f"Error code: {e.code}")
```

## Performance Considerations

- **Async I/O**: Use aiofiles for non-blocking file operations
- **Parallel loading**: MultiSourceLoader loads sources in parallel where possible
- **Caching**: Implement caching in custom loaders for frequently accessed sources
- **Format selection**: JSON is fastest, YAML is most readable, TOML is most structured

## Related Documentation

- [Configuration Manager API](manager.md) - Using loaders with ConfigManager
- [Environment Config API](env.md) - Environment variable loading
- [Configuration Base API](base.md) - BaseConfig and field definitions
- [Configuration Files Guide](/guide/config/files/) - File format details and locations