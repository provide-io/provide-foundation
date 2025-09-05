# Context

::: provide.foundation.context

## Overview

The Context module provides unified configuration and state management for CLI applications and services. It combines configuration from multiple sources (files, environment variables, programmatic updates) into a single, type-safe, and validated context object.

## Key Features

- **Multi-source Configuration**: Load from files, environment variables, or code
- **Type Safety**: Full type annotations and validation using attrs
- **Multiple Formats**: Support for TOML, JSON, and YAML configuration files
- **Environment Integration**: Automatic environment variable parsing
- **Immutable Options**: Optional freezing to prevent modifications
- **Logging Integration**: Built-in logger integration with context binding

## Quick Start

```python
from provide.foundation import Context

# Create with defaults
ctx = Context()

# Create from environment variables
ctx = Context.from_env()

# Create with specific values
ctx = Context(
    log_level="DEBUG",
    profile="development",
    debug=True
)

# Load from configuration file
ctx.load_config("config.toml")

# Use the integrated logger
ctx.logger.info("Application started", profile=ctx.profile)
```

## API Reference

### Context Class

#### `Context(**kwargs)`

Main context class for unified configuration management.

**Parameters:**
- `log_level` (str): Logging level (default: "INFO")
- `profile` (str): Application profile (default: "default") 
- `debug` (bool): Debug mode flag (default: False)
- `json_output` (bool): JSON output format (default: False)
- `config_file` (Path, optional): Path to configuration file
- `log_file` (Path, optional): Path to log file
- `log_format` (str): Log format style (default: "key_value")
- `no_color` (bool): Disable colored output (default: False)
- `no_emoji` (bool): Disable emoji in output (default: False)

**Example:**
```python
from provide.foundation import Context
from pathlib import Path

ctx = Context(
    log_level="DEBUG",
    profile="production",
    config_file=Path("config/production.toml"),
    log_file=Path("logs/app.log"),
    debug=False
)
```

### Class Methods

#### `Context.from_env(prefix="PROVIDE")`

Create Context from environment variables.

**Parameters:**
- `prefix` (str): Environment variable prefix (default: "PROVIDE")

**Returns:**
- `Context`: New Context instance with values from environment

**Environment Variables:**
- `{PREFIX}_LOG_LEVEL`: Logging level
- `{PREFIX}_PROFILE`: Application profile
- `{PREFIX}_DEBUG`: Debug mode (true/false)
- `{PREFIX}_JSON_OUTPUT`: JSON output format (true/false)
- `{PREFIX}_CONFIG_FILE`: Path to config file
- `{PREFIX}_LOG_FILE`: Path to log file
- `{PREFIX}_LOG_FORMAT`: Log format style
- `{PREFIX}_NO_COLOR`: Disable colors (true/false)
- `{PREFIX}_NO_EMOJI`: Disable emoji (true/false)

**Example:**
```bash
# Set environment variables
export PROVIDE_LOG_LEVEL=DEBUG
export PROVIDE_PROFILE=development
export PROVIDE_DEBUG=true
export PROVIDE_CONFIG_FILE=config/dev.toml
```

```python
from provide.foundation import Context

# Load from environment
ctx = Context.from_env()
print(f"Profile: {ctx.profile}")  # development
print(f"Debug: {ctx.debug}")      # True
```

#### `Context.from_dict(data)`

Create Context from dictionary.

**Parameters:**
- `data` (dict[str, Any]): Dictionary with context values

**Returns:**
- `Context`: New Context instance

**Example:**
```python
from provide.foundation import Context

config_data = {
    "log_level": "WARNING",
    "profile": "production",
    "debug": False,
    "config_file": "config/prod.toml"
}

ctx = Context.from_dict(config_data)
```

### Instance Methods

#### `update_from_env(prefix="PROVIDE")`

Update existing context from environment variables.

**Parameters:**
- `prefix` (str): Environment variable prefix (default: "PROVIDE")

**Raises:**
- `RuntimeError`: If context is frozen

**Example:**
```python
from provide.foundation import Context

ctx = Context(profile="default")

# Update from environment
ctx.update_from_env()
```

#### `load_config(path)`

Load configuration from file.

**Parameters:**
- `path` (str | Path): Path to configuration file

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `ImportError`: If required parser library is missing
- `ValueError`: If file format is unsupported
- `RuntimeError`: If context is frozen

**Supported Formats:**
- **TOML** (.toml, .tml): Requires `tomli` or `tomllib`
- **JSON** (.json): Built-in support
- **YAML** (.yaml, .yml): Requires `PyYAML`

**Example:**
```python
from provide.foundation import Context

ctx = Context()

# Load TOML configuration
ctx.load_config("config.toml")

# Load JSON configuration  
ctx.load_config("config.json")

# Load YAML configuration
ctx.load_config("config.yaml")
```

**Example config.toml:**
```toml
log_level = "DEBUG"
profile = "development"
debug = true
json_output = false
log_format = "json"
no_color = false
no_emoji = false

# Optional file paths
config_file = "config/app.toml"
log_file = "logs/app.log"
```

#### `save_config(path)`

Save configuration to file.

**Parameters:**
- `path` (str | Path): Path to save configuration file

**Raises:**
- `ImportError`: If required writer library is missing
- `ValueError`: If file format is unsupported

**Example:**
```python
from provide.foundation import Context

ctx = Context(
    log_level="INFO",
    profile="production",
    debug=False
)

# Save as TOML
ctx.save_config("config/production.toml")

# Save as JSON
ctx.save_config("config/production.json")

# Save as YAML
ctx.save_config("config/production.yaml")
```

#### `to_dict()`

Convert context to dictionary.

**Returns:**
- `dict[str, Any]`: Dictionary representation of context

**Example:**
```python
from provide.foundation import Context

ctx = Context(log_level="DEBUG", profile="dev")
data = ctx.to_dict()
print(data)
# {
#     'log_level': 'DEBUG',
#     'profile': 'dev',
#     'debug': False,
#     'json_output': False,
#     'config_file': None,
#     'log_file': None,
#     'log_format': 'key_value',
#     'no_color': False,
#     'no_emoji': False
# }
```

#### `merge(other, override_defaults=False)`

Merge with another context.

**Parameters:**
- `other` (Context): Context to merge with (takes precedence)
- `override_defaults` (bool): Whether to override default values (default: False)

**Returns:**
- `Context`: New merged Context instance

**Example:**
```python
from provide.foundation import Context

base_ctx = Context(profile="base", log_level="INFO")
env_ctx = Context(log_level="DEBUG", debug=True)

# Merge contexts (env_ctx takes precedence)
merged = base_ctx.merge(env_ctx)
print(f"Profile: {merged.profile}")    # base
print(f"Log Level: {merged.log_level}") # DEBUG
print(f"Debug: {merged.debug}")         # True
```

#### `freeze()`

Freeze context to prevent further modifications.

**Example:**
```python
from provide.foundation import Context

ctx = Context(profile="production")
ctx.freeze()

# This will raise RuntimeError
try:
    ctx.load_config("config.toml")
except RuntimeError as e:
    print(f"Error: {e}")  # Context is frozen and cannot be modified
```

#### `copy()`

Create a deep copy of the context.

**Returns:**
- `Context`: New Context instance (deep copy)

**Example:**
```python
from provide.foundation import Context

original = Context(profile="original")
copy = original.copy()

# Modify copy without affecting original
copy.profile = "modified"
print(f"Original: {original.profile}")  # original
print(f"Copy: {copy.profile}")          # modified
```

### Properties

#### `logger`

Get integrated logger with context binding.

**Returns:**
- Logger instance bound with context values

**Example:**
```python
from provide.foundation import Context

ctx = Context(profile="myapp", log_level="DEBUG")

# Logger automatically includes context
ctx.logger.info("Application started")
# Output includes profile=myapp in structured log
```

## Configuration Sources Priority

Context values are resolved in the following priority order (highest to lowest):

1. **Programmatic values** - Direct parameter assignment
2. **Environment variables** - From `update_from_env()` or `from_env()`
3. **Configuration files** - From `load_config()`
4. **Default values** - Built-in defaults

**Example:**
```python
from provide.foundation import Context
import os

# Set environment
os.environ["PROVIDE_LOG_LEVEL"] = "WARNING"

# Create with defaults
ctx = Context(log_level="INFO")  # INFO from constructor
ctx.update_from_env()            # Overridden to WARNING from env
ctx.load_config("config.toml")   # May be overridden by config file

# Programmatic override (highest priority)
ctx.log_level = "ERROR"          # Final value: ERROR
```

## Environment Variable Reference

All environment variables use the specified prefix (default: "PROVIDE"):

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `{PREFIX}_LOG_LEVEL` | str | Logging level | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `{PREFIX}_PROFILE` | str | Application profile | `development`, `staging`, `production` |
| `{PREFIX}_DEBUG` | bool | Debug mode flag | `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off` |
| `{PREFIX}_JSON_OUTPUT` | bool | JSON output format | `true`, `false` |
| `{PREFIX}_CONFIG_FILE` | str | Config file path | `/path/to/config.toml` |
| `{PREFIX}_LOG_FILE` | str | Log file path | `/path/to/app.log` |
| `{PREFIX}_LOG_FORMAT` | str | Log format style | `key_value`, `json`, `console` |
| `{PREFIX}_NO_COLOR` | bool | Disable colored output | `true`, `false` |
| `{PREFIX}_NO_EMOJI` | bool | Disable emoji | `true`, `false` |

## Type Validation

The Context class automatically validates field types and values:

```python
from provide.foundation import Context

# Valid log levels
ctx = Context(log_level="DEBUG")    # ✅ Valid
ctx = Context(log_level="INFO")     # ✅ Valid
ctx = Context(log_level="ERROR")    # ✅ Valid

# Invalid log level raises ValueError
try:
    ctx = Context(log_level="INVALID")  # ❌ Raises ValueError
except ValueError as e:
    print(f"Validation error: {e}")

# Boolean conversion
ctx = Context(debug="true")    # ✅ Converted to True
ctx = Context(debug="1")       # ✅ Converted to True  
ctx = Context(debug="false")   # ✅ Converted to False
ctx = Context(debug="0")       # ✅ Converted to False
```

## Complete Examples

### CLI Application Context Management

```python
from provide.foundation import Context
from pathlib import Path
import sys

class AppContext:
    def __init__(self, config_dir: Path = Path("config")):
        self.config_dir = config_dir
        self.context = Context()
        
    def initialize(self, profile: str = None):
        """Initialize context from multiple sources."""
        
        # 1. Load base configuration
        base_config = self.config_dir / "base.toml"
        if base_config.exists():
            self.context.load_config(base_config)
            
        # 2. Load profile-specific configuration
        if profile:
            profile_config = self.config_dir / f"{profile}.toml"
            if profile_config.exists():
                profile_ctx = Context()
                profile_ctx.load_config(profile_config)
                self.context = self.context.merge(profile_ctx)
                
        # 3. Override with environment variables
        self.context.update_from_env()
        
        # 4. Set final profile
        if profile:
            self.context.profile = profile
            
        # 5. Setup logging based on context
        self._setup_logging()
        
        return self.context
        
    def _setup_logging(self):
        """Configure logging based on context."""
        from provide.foundation import setup_logging
        
        setup_logging(
            level=self.context.log_level,
            format=self.context.log_format,
            file=self.context.log_file,
            console=not self.context.json_output
        )

# Usage
app_ctx = AppContext()
ctx = app_ctx.initialize(profile="development")

# Log with context
ctx.logger.info("Application initialized", 
                profile=ctx.profile,
                debug_mode=ctx.debug)
```

### Configuration File Management

```python
from provide.foundation import Context
from pathlib import Path

def create_default_configs():
    """Create default configuration files for different environments."""
    
    configs = {
        "development": Context(
            log_level="DEBUG",
            profile="development",
            debug=True,
            json_output=False,
            log_format="console"
        ),
        "staging": Context(
            log_level="INFO", 
            profile="staging",
            debug=False,
            json_output=True,
            log_format="json"
        ),
        "production": Context(
            log_level="WARNING",
            profile="production", 
            debug=False,
            json_output=True,
            log_format="json",
            no_color=True
        )
    }
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    for env_name, ctx in configs.items():
        config_path = config_dir / f"{env_name}.toml"
        ctx.save_config(config_path)
        print(f"Created {config_path}")

def load_runtime_config():
    """Load configuration at runtime with fallbacks."""
    
    # Try multiple configuration sources
    sources = [
        Path("config/local.toml"),      # Local overrides
        Path("config/production.toml"),  # Environment config
        Path("config/base.toml")         # Base configuration
    ]
    
    ctx = Context()  # Start with defaults
    
    for config_path in sources:
        if config_path.exists():
            ctx.load_config(config_path)
            print(f"Loaded config from {config_path}")
            break
    else:
        print("No configuration file found, using defaults")
    
    # Always check environment variables
    ctx.update_from_env()
    
    return ctx

# Create default configurations
create_default_configs()

# Load runtime configuration
runtime_ctx = load_runtime_config()
```

### Context Merging Strategies

```python
from provide.foundation import Context

def demonstrate_merging():
    """Show different context merging strategies."""
    
    # Base application context
    base = Context(
        profile="myapp",
        log_level="INFO",
        debug=False
    )
    
    # Environment-specific overrides
    env_overrides = Context(
        log_level="DEBUG",  # Override log level
        debug=True          # Override debug flag
        # profile not set - will use base value
    )
    
    # User-specific preferences  
    user_prefs = Context(
        log_format="json",  # User prefers JSON
        no_color=True       # User prefers no color
    )
    
    # Strategy 1: Simple merge (all non-None values)
    merged1 = base.merge(env_overrides, override_defaults=True)
    print("Strategy 1 - Override all:")
    print(f"  Profile: {merged1.profile}")      # myapp (from base)
    print(f"  Log Level: {merged1.log_level}")  # DEBUG (from env)
    print(f"  Debug: {merged1.debug}")          # True (from env)
    
    # Strategy 2: Smart merge (only non-default values)
    merged2 = base.merge(env_overrides, override_defaults=False)
    print("Strategy 2 - Override non-defaults only:")
    print(f"  Profile: {merged2.profile}")      # myapp (from base)
    print(f"  Log Level: {merged2.log_level}")  # DEBUG (from env)
    print(f"  Debug: {merged2.debug}")          # True (from env)
    
    # Strategy 3: Chain merging
    final = base.merge(env_overrides).merge(user_prefs)
    print("Strategy 3 - Chain merge:")
    print(f"  Profile: {final.profile}")        # myapp (from base)
    print(f"  Log Level: {final.log_level}")    # DEBUG (from env)
    print(f"  Log Format: {final.log_format}")  # json (from user)
    print(f"  No Color: {final.no_color}")      # True (from user)

demonstrate_merging()
```

## Best Practices

### 1. Use Consistent Configuration Patterns

```python
# Good: Consistent initialization pattern
def init_app_context(profile: str = "default") -> Context:
    ctx = Context()
    
    # Load in order of precedence
    if Path("config/base.toml").exists():
        ctx.load_config("config/base.toml")
        
    if Path(f"config/{profile}.toml").exists():  
        profile_ctx = Context()
        profile_ctx.load_config(f"config/{profile}.toml")
        ctx = ctx.merge(profile_ctx)
        
    ctx.update_from_env()
    ctx.profile = profile
    
    return ctx
```

### 2. Validate Configuration Early

```python
# Good: Validate critical settings
def validate_context(ctx: Context) -> None:
    if ctx.profile == "production" and ctx.debug:
        raise ValueError("Debug mode should not be enabled in production")
        
    if ctx.log_file and not ctx.log_file.parent.exists():
        raise ValueError(f"Log directory does not exist: {ctx.log_file.parent}")
```

### 3. Use Type-Safe Configuration

```python
# Good: Leverage type safety
def configure_database(ctx: Context) -> dict:
    config = {
        "debug": ctx.debug,
        "log_queries": ctx.log_level == "DEBUG",
        "connection_timeout": 30 if ctx.profile == "production" else 5
    }
    return config
```

### 4. Handle Missing Dependencies Gracefully

```python
# Good: Graceful fallback for optional formats
def load_config_safe(ctx: Context, path: str) -> bool:
    try:
        ctx.load_config(path)
        return True
    except ImportError as e:
        print(f"Warning: Could not load {path}: {e}")
        return False
    except FileNotFoundError:
        print(f"Config file not found: {path}")
        return False
```

## Thread Safety

The Context class is thread-safe for read operations but not for write operations:

- ✅ **Safe**: Reading context values from multiple threads
- ✅ **Safe**: Creating new Context instances
- ❌ **Unsafe**: Modifying context from multiple threads
- ✅ **Safe**: Using frozen contexts from multiple threads

For multi-threaded applications, either:
1. Create context once and freeze it
2. Use separate context instances per thread
3. Add external synchronization for modifications

## Error Handling

Context operations can raise several types of errors:

- `ValueError`: Invalid field values or configuration
- `FileNotFoundError`: Missing configuration files
- `ImportError`: Missing optional dependencies (TOML/YAML)
- `RuntimeError`: Operations on frozen contexts
- `json.JSONDecodeError`: Invalid JSON configuration
- `yaml.YAMLError`: Invalid YAML configuration

## See Also

- [Logger Module](../logger/index.md) - For logging integration
- [Config Module](../config/index.md) - For advanced configuration management
- [CLI Guide](../../guide/cli/index.md) - Using Context with CLI applications
- [Configuration Guide](../../guide/config/index.md) - Configuration best practices