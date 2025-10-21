# provide/foundation/logger/defaults.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.logger.config.logging import LoggingConfig

"""Logger defaults for Foundation configuration."""

# =================================
# Logging Defaults
# =================================
DEFAULT_LOG_LEVEL = "WARNING"
DEFAULT_CONSOLE_FORMATTER = "key_value"
DEFAULT_LOGGER_NAME_EMOJI_ENABLED = True
DEFAULT_DAS_EMOJI_ENABLED = True
DEFAULT_OMIT_TIMESTAMP = False
DEFAULT_FOUNDATION_SETUP_LOG_LEVEL = "WARNING"
DEFAULT_FOUNDATION_LOG_OUTPUT = "stderr"

# =================================
# Rate Limiting Defaults
# =================================
DEFAULT_RATE_LIMIT_ENABLED = False
DEFAULT_RATE_LIMIT_EMIT_WARNINGS = True
DEFAULT_RATE_LIMIT_GLOBAL = 5.0
DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY = 1000
DEFAULT_RATE_LIMIT_OVERFLOW_POLICY = "drop_oldest"

# =================================
# Sanitization Defaults
# =================================
DEFAULT_SANITIZATION_ENABLED = True
DEFAULT_SANITIZATION_MASK_PATTERNS = True
DEFAULT_SANITIZATION_SANITIZE_DICTS = True

# =================================
# Logger System Defaults
# =================================
DEFAULT_FALLBACK_LOG_LEVEL = "INFO"
DEFAULT_FALLBACK_LOG_LEVEL_NUMERIC = 20
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

# =================================
# Factory Functions for Mutable Defaults
# =================================


def x_default_module_levels__mutmut_orig() -> dict[str, str]:
    """Factory for module log levels dictionary."""
    return {
        "asyncio": "INFO",  # Suppress asyncio DEBUG messages (e.g., selector events)
    }

# =================================
# Factory Functions for Mutable Defaults
# =================================


def x_default_module_levels__mutmut_1() -> dict[str, str]:
    """Factory for module log levels dictionary."""
    return {
        "XXasyncioXX": "INFO",  # Suppress asyncio DEBUG messages (e.g., selector events)
    }

# =================================
# Factory Functions for Mutable Defaults
# =================================


def x_default_module_levels__mutmut_2() -> dict[str, str]:
    """Factory for module log levels dictionary."""
    return {
        "ASYNCIO": "INFO",  # Suppress asyncio DEBUG messages (e.g., selector events)
    }

# =================================
# Factory Functions for Mutable Defaults
# =================================


def x_default_module_levels__mutmut_3() -> dict[str, str]:
    """Factory for module log levels dictionary."""
    return {
        "asyncio": "XXINFOXX",  # Suppress asyncio DEBUG messages (e.g., selector events)
    }

# =================================
# Factory Functions for Mutable Defaults
# =================================


def x_default_module_levels__mutmut_4() -> dict[str, str]:
    """Factory for module log levels dictionary."""
    return {
        "asyncio": "info",  # Suppress asyncio DEBUG messages (e.g., selector events)
    }

x_default_module_levels__mutmut_mutants : ClassVar[MutantDict] = {
'x_default_module_levels__mutmut_1': x_default_module_levels__mutmut_1, 
    'x_default_module_levels__mutmut_2': x_default_module_levels__mutmut_2, 
    'x_default_module_levels__mutmut_3': x_default_module_levels__mutmut_3, 
    'x_default_module_levels__mutmut_4': x_default_module_levels__mutmut_4
}

def default_module_levels(*args, **kwargs):
    result = _mutmut_trampoline(x_default_module_levels__mutmut_orig, x_default_module_levels__mutmut_mutants, args, kwargs)
    return result 

default_module_levels.__signature__ = _mutmut_signature(x_default_module_levels__mutmut_orig)
x_default_module_levels__mutmut_orig.__name__ = 'x_default_module_levels'


def default_rate_limits() -> dict[str, tuple[float, float]]:
    """Factory for per-logger rate limits dictionary."""
    return {}


def default_logging_config() -> LoggingConfig:
    """Factory for LoggingConfig instance."""
    from provide.foundation.logger.config.logging import LoggingConfig

    return LoggingConfig.from_env()


__all__ = [
    "DEFAULT_CONSOLE_FORMATTER",
    "DEFAULT_DAS_EMOJI_ENABLED",
    "DEFAULT_FALLBACK_LOG_LEVEL",
    "DEFAULT_FALLBACK_LOG_LEVEL_NUMERIC",
    "DEFAULT_FOUNDATION_LOG_OUTPUT",
    "DEFAULT_FOUNDATION_SETUP_LOG_LEVEL",
    "DEFAULT_LOGGER_NAME_EMOJI_ENABLED",
    "DEFAULT_LOG_LEVEL",
    "DEFAULT_OMIT_TIMESTAMP",
    "DEFAULT_RATE_LIMIT_EMIT_WARNINGS",
    "DEFAULT_RATE_LIMIT_ENABLED",
    "DEFAULT_RATE_LIMIT_GLOBAL",
    "DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY",
    "DEFAULT_RATE_LIMIT_OVERFLOW_POLICY",
    "DEFAULT_SANITIZATION_ENABLED",
    "DEFAULT_SANITIZATION_MASK_PATTERNS",
    "DEFAULT_SANITIZATION_SANITIZE_DICTS",
    "default_logging_config",
    "default_module_levels",
    "default_rate_limits",
]


# <3 🧱🤝📝🪄
