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
    parse_bool,
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
    "parse_bool",
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
]