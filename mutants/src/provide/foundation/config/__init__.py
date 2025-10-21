# provide/foundation/config/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.config.base import (
    BaseConfig,
    field,
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
from provide.foundation.config.env import (
    RuntimeConfig,
    env_field,
    get_env,
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
    load_config,
    register_config,
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
from provide.foundation.config.validators import (
    validate_choice,
    validate_range,
)
from provide.foundation.errors.config import (
    ConfigurationError as ConfigError,
    ValidationError as ConfigValidationError,
)
from provide.foundation.parsers import (
    parse_bool,
    parse_dict,
    parse_list,
)

"""Foundation Configuration System.

A comprehensive, extensible configuration framework for the provide.io ecosystem.
Supports multiple configuration sources with precedence, validation, and type safety.
"""

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
    "FileConfigLoader",
    "MultiSourceLoader",
    # Environment
    "RuntimeConfig",
    "SchemaField",
    "env_field",
    "field",
    "get_config",
    "get_env",
    # Config loading
    "load_config",
    "parse_bool",
    # Converters
    "parse_bool_extended",
    "parse_comma_list",
    "parse_console_formatter",
    "parse_dict",
    "parse_float_with_validation",
    "parse_headers",
    "parse_json_dict",
    "parse_json_list",
    "parse_list",
    "parse_log_level",
    "parse_module_levels",
    "parse_rate_limits",
    "parse_sample_rate",
    "register_config",
    "set_config",
    # Validators
    "validate_choice",
    "validate_log_level",
    "validate_non_negative",
    "validate_overflow_policy",
    "validate_port",
    "validate_positive",
    "validate_range",
    "validate_sample_rate",
    "validate_schema",
]
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


# <3 🧱🤝⚙️🪄
