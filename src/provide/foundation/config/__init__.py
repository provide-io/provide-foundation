"""
Foundation Configuration System.

A comprehensive, extensible configuration framework for the provide.io ecosystem.
Supports multiple configuration sources with precedence, validation, and type safety.
"""

from provide.foundation.config.base import (
    BaseConfig,
    ConfigError,
    ConfigValidationError,
    field,
)
from provide.foundation.config.env import (
    EnvConfig,
    env_field,
    get_env,
    get_env_async,
    parse_bool,
    parse_dict,
    parse_list,
)
from provide.foundation.config.loader import (
    ConfigLoader,
    DictConfigLoader,
    FileConfigLoader,
    MultiSourceLoader,
)
from provide.foundation.config.manager import (
    ConfigManager,
    get_config,
    set_config,
)
from provide.foundation.config.schema import (
    ConfigSchema,
    SchemaField,
    validate_schema,
)
from provide.foundation.config.types import (
    ConfigDict,
    ConfigSource,
    ConfigValue,
)

# Import sync wrappers for convenience
from provide.foundation.config.sync import (
    load_config,
    load_config_from_env,
    load_config_from_file,
    validate_config,
    SyncConfigManager,
)

__all__ = [
    # Base
    "BaseConfig",
    "ConfigError",
    "ConfigValidationError",
    "field",
    # Environment
    "EnvConfig",
    "env_field",
    "get_env",
    "get_env_async",
    "parse_bool",
    "parse_dict",
    "parse_list",
    # Loader
    "ConfigLoader",
    "DictConfigLoader",
    "FileConfigLoader",
    "MultiSourceLoader",
    # Manager
    "ConfigManager",
    "get_config",
    "set_config",
    # Schema
    "ConfigSchema",
    "SchemaField",
    "validate_schema",
    # Types
    "ConfigDict",
    "ConfigSource",
    "ConfigValue",
    # Sync wrappers
    "load_config",
    "load_config_from_env",
    "load_config_from_file",
    "validate_config",
    "SyncConfigManager",
]