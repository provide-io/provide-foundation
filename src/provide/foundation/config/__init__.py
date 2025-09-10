"""
Foundation Configuration System.

A comprehensive, extensible configuration framework for the provide.io ecosystem.
Supports multiple configuration sources with precedence, validation, and type safety.
"""

from provide.foundation.config.base import (
    BaseConfig,
    field,
)
from provide.foundation.config.env import (
    RuntimeConfig,
    env_field,
    get_env,
    get_env_async,
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

# Import sync wrappers for convenience
from provide.foundation.config.sync import (
    SyncConfigManager,
    load_config,
    load_config_from_env,
    load_config_from_file,
    validate_config,
)
from provide.foundation.config.types import (
    ConfigDict,
    ConfigSource,
    ConfigValue,
)
from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_comma_list,
    parse_console_formatter,
    parse_float_with_validation,
    parse_headers,
    parse_json_dict,
    parse_json_list,
    parse_log_level,
    parse_module_levels,
    parse_rate_limits,
    parse_sample_rate,
    validate_log_level,
    validate_non_negative,
    validate_overflow_policy,
    validate_port,
    validate_positive,
    validate_sample_rate,
)
from provide.foundation.config.validators import (
    validate_choice,
    validate_range,
)
from provide.foundation.errors.config import (
    ConfigurationError as ConfigError,
    ValidationError as ConfigValidationError,
)
from provide.foundation.utils.parsing import (
    parse_bool,
    parse_dict,
    parse_list,
)

__all__ = [
    # Base
    "BaseConfig",
    # Types
    "ConfigDict",
    "ConfigError",
    # Loader
    "ConfigLoader",
    # Manager
    "ConfigManager",
    # Schema
    "ConfigSchema",
    "ConfigSource",
    "ConfigValidationError",
    "ConfigValue",
    "DictConfigLoader",
    # Environment
    "RuntimeConfig",
    "FileConfigLoader",
    "MultiSourceLoader",
    "SchemaField",
    "SyncConfigManager",
    "env_field",
    "field",
    "get_config",
    "get_env",
    "get_env_async",
    # Sync wrappers
    "load_config",
    "load_config_from_env",
    "load_config_from_file",
    "parse_bool",
    "parse_dict",
    "parse_list",
    "set_config",
    # Converters
    "parse_bool_extended",
    "parse_comma_list",
    "parse_console_formatter",
    "parse_float_with_validation",
    "parse_headers",
    "parse_json_dict",
    "parse_json_list",
    "parse_log_level",
    "parse_module_levels",
    "parse_rate_limits",
    "parse_sample_rate",
    # Validators
    "validate_choice",
    "validate_config",
    "validate_log_level",
    "validate_non_negative",
    "validate_overflow_policy",
    "validate_port",
    "validate_positive",
    "validate_range",
    "validate_sample_rate",
    "validate_schema",
]
