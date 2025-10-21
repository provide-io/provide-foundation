# provide/foundation/parsers/structured.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

"""Complex data structure parsers for structured configuration values.

Handles parsing of structured data like dictionaries with specific formats
(headers, module levels, rate limits) from string configuration values.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.types import LogLevelStr
else:
    LogLevelStr = str
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


def x_parse_log_level__mutmut_orig(value: str) -> LogLevelStr:
    """Import parse_log_level from telemetry module to avoid circular imports."""
    from provide.foundation.parsers.telemetry import parse_log_level as _parse_log_level

    return _parse_log_level(value)


def x_parse_log_level__mutmut_1(value: str) -> LogLevelStr:
    """Import parse_log_level from telemetry module to avoid circular imports."""
    from provide.foundation.parsers.telemetry import parse_log_level as _parse_log_level

    return _parse_log_level(None)

x_parse_log_level__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_log_level__mutmut_1': x_parse_log_level__mutmut_1
}

def parse_log_level(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_log_level__mutmut_orig, x_parse_log_level__mutmut_mutants, args, kwargs)
    return result 

parse_log_level.__signature__ = _mutmut_signature(x_parse_log_level__mutmut_orig)
x_parse_log_level__mutmut_orig.__name__ = 'x_parse_log_level'


def x_parse_module_levels__mutmut_orig(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_1(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = None
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_2(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = None
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_3(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(None)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_4(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                break
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_5(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value and not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_6(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_7(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_8(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = None
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_9(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(None):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_10(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split("XX,XX"):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_11(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = None
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_12(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_13(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            break

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_14(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "XX:XX" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_15(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_16(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            break

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_17(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = None
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_18(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(None, 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_19(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", None)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_20(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_21(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", )
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_22(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.rsplit(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_23(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split("XX:XX", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_24(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 2)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_25(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = None
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_26(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = None

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_27(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = None
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_28(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(None)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def x_parse_module_levels__mutmut_29(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                break

    return result

x_parse_module_levels__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_module_levels__mutmut_1': x_parse_module_levels__mutmut_1, 
    'x_parse_module_levels__mutmut_2': x_parse_module_levels__mutmut_2, 
    'x_parse_module_levels__mutmut_3': x_parse_module_levels__mutmut_3, 
    'x_parse_module_levels__mutmut_4': x_parse_module_levels__mutmut_4, 
    'x_parse_module_levels__mutmut_5': x_parse_module_levels__mutmut_5, 
    'x_parse_module_levels__mutmut_6': x_parse_module_levels__mutmut_6, 
    'x_parse_module_levels__mutmut_7': x_parse_module_levels__mutmut_7, 
    'x_parse_module_levels__mutmut_8': x_parse_module_levels__mutmut_8, 
    'x_parse_module_levels__mutmut_9': x_parse_module_levels__mutmut_9, 
    'x_parse_module_levels__mutmut_10': x_parse_module_levels__mutmut_10, 
    'x_parse_module_levels__mutmut_11': x_parse_module_levels__mutmut_11, 
    'x_parse_module_levels__mutmut_12': x_parse_module_levels__mutmut_12, 
    'x_parse_module_levels__mutmut_13': x_parse_module_levels__mutmut_13, 
    'x_parse_module_levels__mutmut_14': x_parse_module_levels__mutmut_14, 
    'x_parse_module_levels__mutmut_15': x_parse_module_levels__mutmut_15, 
    'x_parse_module_levels__mutmut_16': x_parse_module_levels__mutmut_16, 
    'x_parse_module_levels__mutmut_17': x_parse_module_levels__mutmut_17, 
    'x_parse_module_levels__mutmut_18': x_parse_module_levels__mutmut_18, 
    'x_parse_module_levels__mutmut_19': x_parse_module_levels__mutmut_19, 
    'x_parse_module_levels__mutmut_20': x_parse_module_levels__mutmut_20, 
    'x_parse_module_levels__mutmut_21': x_parse_module_levels__mutmut_21, 
    'x_parse_module_levels__mutmut_22': x_parse_module_levels__mutmut_22, 
    'x_parse_module_levels__mutmut_23': x_parse_module_levels__mutmut_23, 
    'x_parse_module_levels__mutmut_24': x_parse_module_levels__mutmut_24, 
    'x_parse_module_levels__mutmut_25': x_parse_module_levels__mutmut_25, 
    'x_parse_module_levels__mutmut_26': x_parse_module_levels__mutmut_26, 
    'x_parse_module_levels__mutmut_27': x_parse_module_levels__mutmut_27, 
    'x_parse_module_levels__mutmut_28': x_parse_module_levels__mutmut_28, 
    'x_parse_module_levels__mutmut_29': x_parse_module_levels__mutmut_29
}

def parse_module_levels(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_module_levels__mutmut_orig, x_parse_module_levels__mutmut_mutants, args, kwargs)
    return result 

parse_module_levels.__signature__ = _mutmut_signature(x_parse_module_levels__mutmut_orig)
x_parse_module_levels__mutmut_orig.__name__ = 'x_parse_module_levels'


def x_parse_rate_limits__mutmut_orig(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_1(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value and not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_2(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_3(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_4(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = None
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_5(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(None):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_6(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split("XX,XX"):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_7(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = None
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_8(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_9(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            break

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_10(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = None
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_11(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(None)
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_12(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split("XX:XX")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_13(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) == 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_14(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 4:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_15(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            break

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_16(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = None
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_17(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = None

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_18(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_19(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            break

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_20(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = None
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_21(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(None)
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_22(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = None
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_23(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(None)
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_24(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = None
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def x_parse_rate_limits__mutmut_25(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            break

    return result

x_parse_rate_limits__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_rate_limits__mutmut_1': x_parse_rate_limits__mutmut_1, 
    'x_parse_rate_limits__mutmut_2': x_parse_rate_limits__mutmut_2, 
    'x_parse_rate_limits__mutmut_3': x_parse_rate_limits__mutmut_3, 
    'x_parse_rate_limits__mutmut_4': x_parse_rate_limits__mutmut_4, 
    'x_parse_rate_limits__mutmut_5': x_parse_rate_limits__mutmut_5, 
    'x_parse_rate_limits__mutmut_6': x_parse_rate_limits__mutmut_6, 
    'x_parse_rate_limits__mutmut_7': x_parse_rate_limits__mutmut_7, 
    'x_parse_rate_limits__mutmut_8': x_parse_rate_limits__mutmut_8, 
    'x_parse_rate_limits__mutmut_9': x_parse_rate_limits__mutmut_9, 
    'x_parse_rate_limits__mutmut_10': x_parse_rate_limits__mutmut_10, 
    'x_parse_rate_limits__mutmut_11': x_parse_rate_limits__mutmut_11, 
    'x_parse_rate_limits__mutmut_12': x_parse_rate_limits__mutmut_12, 
    'x_parse_rate_limits__mutmut_13': x_parse_rate_limits__mutmut_13, 
    'x_parse_rate_limits__mutmut_14': x_parse_rate_limits__mutmut_14, 
    'x_parse_rate_limits__mutmut_15': x_parse_rate_limits__mutmut_15, 
    'x_parse_rate_limits__mutmut_16': x_parse_rate_limits__mutmut_16, 
    'x_parse_rate_limits__mutmut_17': x_parse_rate_limits__mutmut_17, 
    'x_parse_rate_limits__mutmut_18': x_parse_rate_limits__mutmut_18, 
    'x_parse_rate_limits__mutmut_19': x_parse_rate_limits__mutmut_19, 
    'x_parse_rate_limits__mutmut_20': x_parse_rate_limits__mutmut_20, 
    'x_parse_rate_limits__mutmut_21': x_parse_rate_limits__mutmut_21, 
    'x_parse_rate_limits__mutmut_22': x_parse_rate_limits__mutmut_22, 
    'x_parse_rate_limits__mutmut_23': x_parse_rate_limits__mutmut_23, 
    'x_parse_rate_limits__mutmut_24': x_parse_rate_limits__mutmut_24, 
    'x_parse_rate_limits__mutmut_25': x_parse_rate_limits__mutmut_25
}

def parse_rate_limits(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_rate_limits__mutmut_orig, x_parse_rate_limits__mutmut_mutants, args, kwargs)
    return result 

parse_rate_limits.__signature__ = _mutmut_signature(x_parse_rate_limits__mutmut_orig)
x_parse_rate_limits__mutmut_orig.__name__ = 'x_parse_rate_limits'


def x_parse_headers__mutmut_orig(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_1(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value and not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_2(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_3(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_4(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = None
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_5(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(None):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_6(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split("XX,XX"):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_7(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = None
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_8(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_9(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            break

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_10(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "XX=XX" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_11(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_12(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            break

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_13(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = None
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_14(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split(None, 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_15(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", None)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_16(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split(1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_17(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", )
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_18(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.rsplit("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_19(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("XX=XX", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_20(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 2)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_21(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = None
        val = val.strip()

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_22(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = None

        if key:
            result[key] = val

    return result


def x_parse_headers__mutmut_23(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = None

    return result

x_parse_headers__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_headers__mutmut_1': x_parse_headers__mutmut_1, 
    'x_parse_headers__mutmut_2': x_parse_headers__mutmut_2, 
    'x_parse_headers__mutmut_3': x_parse_headers__mutmut_3, 
    'x_parse_headers__mutmut_4': x_parse_headers__mutmut_4, 
    'x_parse_headers__mutmut_5': x_parse_headers__mutmut_5, 
    'x_parse_headers__mutmut_6': x_parse_headers__mutmut_6, 
    'x_parse_headers__mutmut_7': x_parse_headers__mutmut_7, 
    'x_parse_headers__mutmut_8': x_parse_headers__mutmut_8, 
    'x_parse_headers__mutmut_9': x_parse_headers__mutmut_9, 
    'x_parse_headers__mutmut_10': x_parse_headers__mutmut_10, 
    'x_parse_headers__mutmut_11': x_parse_headers__mutmut_11, 
    'x_parse_headers__mutmut_12': x_parse_headers__mutmut_12, 
    'x_parse_headers__mutmut_13': x_parse_headers__mutmut_13, 
    'x_parse_headers__mutmut_14': x_parse_headers__mutmut_14, 
    'x_parse_headers__mutmut_15': x_parse_headers__mutmut_15, 
    'x_parse_headers__mutmut_16': x_parse_headers__mutmut_16, 
    'x_parse_headers__mutmut_17': x_parse_headers__mutmut_17, 
    'x_parse_headers__mutmut_18': x_parse_headers__mutmut_18, 
    'x_parse_headers__mutmut_19': x_parse_headers__mutmut_19, 
    'x_parse_headers__mutmut_20': x_parse_headers__mutmut_20, 
    'x_parse_headers__mutmut_21': x_parse_headers__mutmut_21, 
    'x_parse_headers__mutmut_22': x_parse_headers__mutmut_22, 
    'x_parse_headers__mutmut_23': x_parse_headers__mutmut_23
}

def parse_headers(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_headers__mutmut_orig, x_parse_headers__mutmut_mutants, args, kwargs)
    return result 

parse_headers.__signature__ = _mutmut_signature(x_parse_headers__mutmut_orig)
x_parse_headers__mutmut_orig.__name__ = 'x_parse_headers'


__all__ = [
    "parse_headers",
    "parse_module_levels",
    "parse_rate_limits",
]


# <3 🧱🤝🧩🪄
