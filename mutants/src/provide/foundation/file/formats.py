# provide/foundation/file/formats.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path
from typing import Any

from provide.foundation.file.atomic import atomic_write_text
from provide.foundation.file.safe import safe_read_text
from provide.foundation.logger import get_logger
from provide.foundation.serialization import (
    json_dumps,
    json_loads,
    toml_dumps,
    toml_loads,
    yaml_dumps,
    yaml_loads,
)

"""Format-specific file operations for JSON, YAML, TOML."""

log = get_logger(__name__)
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


def x_read_json__mutmut_orig(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_1(
    path: Path | str,
    default: Any = None,
    encoding: str = "XXutf-8XX",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_2(
    path: Path | str,
    default: Any = None,
    encoding: str = "UTF-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_3(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = None

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_4(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(None, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_5(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default=None, encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_6(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=None)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_7(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_8(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_9(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", )

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_10(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="XXXX", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_11(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_12(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug(None, path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_13(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=None)
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_14(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug(path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_15(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", )
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_16(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("XXEmpty or missing JSON file, returning defaultXX", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_17(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("empty or missing json file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_18(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("EMPTY OR MISSING JSON FILE, RETURNING DEFAULT", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_19(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(None))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_20(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(None)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_21(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning(None, path=str(path), error=str(e))
        return default


def x_read_json__mutmut_22(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=None, error=str(e))
        return default


def x_read_json__mutmut_23(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=None)
        return default


def x_read_json__mutmut_24(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning(path=str(path), error=str(e))
        return default


def x_read_json__mutmut_25(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", error=str(e))
        return default


def x_read_json__mutmut_26(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), )
        return default


def x_read_json__mutmut_27(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("XXInvalid JSON fileXX", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_28(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("invalid json file", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_29(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("INVALID JSON FILE", path=str(path), error=str(e))
        return default


def x_read_json__mutmut_30(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(None), error=str(e))
        return default


def x_read_json__mutmut_31(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read JSON file with error handling.

    Args:
        path: JSON file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed JSON data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing JSON file, returning default", path=str(path))
        return default

    try:
        return json_loads(content)
    except Exception as e:
        log.warning("Invalid JSON file", path=str(path), error=str(None))
        return default

x_read_json__mutmut_mutants : ClassVar[MutantDict] = {
'x_read_json__mutmut_1': x_read_json__mutmut_1, 
    'x_read_json__mutmut_2': x_read_json__mutmut_2, 
    'x_read_json__mutmut_3': x_read_json__mutmut_3, 
    'x_read_json__mutmut_4': x_read_json__mutmut_4, 
    'x_read_json__mutmut_5': x_read_json__mutmut_5, 
    'x_read_json__mutmut_6': x_read_json__mutmut_6, 
    'x_read_json__mutmut_7': x_read_json__mutmut_7, 
    'x_read_json__mutmut_8': x_read_json__mutmut_8, 
    'x_read_json__mutmut_9': x_read_json__mutmut_9, 
    'x_read_json__mutmut_10': x_read_json__mutmut_10, 
    'x_read_json__mutmut_11': x_read_json__mutmut_11, 
    'x_read_json__mutmut_12': x_read_json__mutmut_12, 
    'x_read_json__mutmut_13': x_read_json__mutmut_13, 
    'x_read_json__mutmut_14': x_read_json__mutmut_14, 
    'x_read_json__mutmut_15': x_read_json__mutmut_15, 
    'x_read_json__mutmut_16': x_read_json__mutmut_16, 
    'x_read_json__mutmut_17': x_read_json__mutmut_17, 
    'x_read_json__mutmut_18': x_read_json__mutmut_18, 
    'x_read_json__mutmut_19': x_read_json__mutmut_19, 
    'x_read_json__mutmut_20': x_read_json__mutmut_20, 
    'x_read_json__mutmut_21': x_read_json__mutmut_21, 
    'x_read_json__mutmut_22': x_read_json__mutmut_22, 
    'x_read_json__mutmut_23': x_read_json__mutmut_23, 
    'x_read_json__mutmut_24': x_read_json__mutmut_24, 
    'x_read_json__mutmut_25': x_read_json__mutmut_25, 
    'x_read_json__mutmut_26': x_read_json__mutmut_26, 
    'x_read_json__mutmut_27': x_read_json__mutmut_27, 
    'x_read_json__mutmut_28': x_read_json__mutmut_28, 
    'x_read_json__mutmut_29': x_read_json__mutmut_29, 
    'x_read_json__mutmut_30': x_read_json__mutmut_30, 
    'x_read_json__mutmut_31': x_read_json__mutmut_31
}

def read_json(*args, **kwargs):
    result = _mutmut_trampoline(x_read_json__mutmut_orig, x_read_json__mutmut_mutants, args, kwargs)
    return result 

read_json.__signature__ = _mutmut_signature(x_read_json__mutmut_orig)
x_read_json__mutmut_orig.__name__ = 'x_read_json'


def x_write_json__mutmut_orig(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_1(
    path: Path | str,
    data: Any,
    indent: int = 3,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_2(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = True,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_3(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = False,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_4(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "XXutf-8XX",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_5(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "UTF-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_6(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = None

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_7(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(None)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_8(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = None

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_9(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(None, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_10(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=None, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_11(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=None, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_12(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=None)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_13(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_14(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_15(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_16(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_17(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=True)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_18(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(None, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_19(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, None, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_20(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=None)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_21(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_22(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_23(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_24(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=None, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_25(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=None)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_26(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_27(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, )
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_28(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=False, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_29(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=False)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_30(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(None, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_31(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=None)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_32(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_33(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, )

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_34(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug(None, path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_35(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=None, atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_36(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=None)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_37(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug(path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_38(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_39(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), )
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_40(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("XXWrote JSON fileXX", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_41(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("wrote json file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_42(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("WROTE JSON FILE", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_43(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(None), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_44(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error(None, path=str(path), error=str(e))
        raise


def x_write_json__mutmut_45(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=None, error=str(e))
        raise


def x_write_json__mutmut_46(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=None)
        raise


def x_write_json__mutmut_47(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error(path=str(path), error=str(e))
        raise


def x_write_json__mutmut_48(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", error=str(e))
        raise


def x_write_json__mutmut_49(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), )
        raise


def x_write_json__mutmut_50(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("XXFailed to write JSON fileXX", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_51(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("failed to write json file", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_52(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("FAILED TO WRITE JSON FILE", path=str(path), error=str(e))
        raise


def x_write_json__mutmut_53(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(None), error=str(e))
        raise


def x_write_json__mutmut_54(
    path: Path | str,
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write JSON file, optionally atomic.

    Args:
        path: JSON file path
        data: Data to serialize
        indent: Indentation level (None for compact)
        sort_keys: Whether to sort dictionary keys
        atomic: Use atomic write
        encoding: Text encoding

    """
    path = Path(path)

    try:
        content = json_dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote JSON file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write JSON file", path=str(path), error=str(None))
        raise

x_write_json__mutmut_mutants : ClassVar[MutantDict] = {
'x_write_json__mutmut_1': x_write_json__mutmut_1, 
    'x_write_json__mutmut_2': x_write_json__mutmut_2, 
    'x_write_json__mutmut_3': x_write_json__mutmut_3, 
    'x_write_json__mutmut_4': x_write_json__mutmut_4, 
    'x_write_json__mutmut_5': x_write_json__mutmut_5, 
    'x_write_json__mutmut_6': x_write_json__mutmut_6, 
    'x_write_json__mutmut_7': x_write_json__mutmut_7, 
    'x_write_json__mutmut_8': x_write_json__mutmut_8, 
    'x_write_json__mutmut_9': x_write_json__mutmut_9, 
    'x_write_json__mutmut_10': x_write_json__mutmut_10, 
    'x_write_json__mutmut_11': x_write_json__mutmut_11, 
    'x_write_json__mutmut_12': x_write_json__mutmut_12, 
    'x_write_json__mutmut_13': x_write_json__mutmut_13, 
    'x_write_json__mutmut_14': x_write_json__mutmut_14, 
    'x_write_json__mutmut_15': x_write_json__mutmut_15, 
    'x_write_json__mutmut_16': x_write_json__mutmut_16, 
    'x_write_json__mutmut_17': x_write_json__mutmut_17, 
    'x_write_json__mutmut_18': x_write_json__mutmut_18, 
    'x_write_json__mutmut_19': x_write_json__mutmut_19, 
    'x_write_json__mutmut_20': x_write_json__mutmut_20, 
    'x_write_json__mutmut_21': x_write_json__mutmut_21, 
    'x_write_json__mutmut_22': x_write_json__mutmut_22, 
    'x_write_json__mutmut_23': x_write_json__mutmut_23, 
    'x_write_json__mutmut_24': x_write_json__mutmut_24, 
    'x_write_json__mutmut_25': x_write_json__mutmut_25, 
    'x_write_json__mutmut_26': x_write_json__mutmut_26, 
    'x_write_json__mutmut_27': x_write_json__mutmut_27, 
    'x_write_json__mutmut_28': x_write_json__mutmut_28, 
    'x_write_json__mutmut_29': x_write_json__mutmut_29, 
    'x_write_json__mutmut_30': x_write_json__mutmut_30, 
    'x_write_json__mutmut_31': x_write_json__mutmut_31, 
    'x_write_json__mutmut_32': x_write_json__mutmut_32, 
    'x_write_json__mutmut_33': x_write_json__mutmut_33, 
    'x_write_json__mutmut_34': x_write_json__mutmut_34, 
    'x_write_json__mutmut_35': x_write_json__mutmut_35, 
    'x_write_json__mutmut_36': x_write_json__mutmut_36, 
    'x_write_json__mutmut_37': x_write_json__mutmut_37, 
    'x_write_json__mutmut_38': x_write_json__mutmut_38, 
    'x_write_json__mutmut_39': x_write_json__mutmut_39, 
    'x_write_json__mutmut_40': x_write_json__mutmut_40, 
    'x_write_json__mutmut_41': x_write_json__mutmut_41, 
    'x_write_json__mutmut_42': x_write_json__mutmut_42, 
    'x_write_json__mutmut_43': x_write_json__mutmut_43, 
    'x_write_json__mutmut_44': x_write_json__mutmut_44, 
    'x_write_json__mutmut_45': x_write_json__mutmut_45, 
    'x_write_json__mutmut_46': x_write_json__mutmut_46, 
    'x_write_json__mutmut_47': x_write_json__mutmut_47, 
    'x_write_json__mutmut_48': x_write_json__mutmut_48, 
    'x_write_json__mutmut_49': x_write_json__mutmut_49, 
    'x_write_json__mutmut_50': x_write_json__mutmut_50, 
    'x_write_json__mutmut_51': x_write_json__mutmut_51, 
    'x_write_json__mutmut_52': x_write_json__mutmut_52, 
    'x_write_json__mutmut_53': x_write_json__mutmut_53, 
    'x_write_json__mutmut_54': x_write_json__mutmut_54
}

def write_json(*args, **kwargs):
    result = _mutmut_trampoline(x_write_json__mutmut_orig, x_write_json__mutmut_mutants, args, kwargs)
    return result 

write_json.__signature__ = _mutmut_signature(x_write_json__mutmut_orig)
x_write_json__mutmut_orig.__name__ = 'x_write_json'


def x_read_yaml__mutmut_orig(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_1(
    path: Path | str,
    default: Any = None,
    encoding: str = "XXutf-8XX",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_2(
    path: Path | str,
    default: Any = None,
    encoding: str = "UTF-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_3(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning(None)
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_4(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("XXPyYAML not installed, returning defaultXX")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_5(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("pyyaml not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_6(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PYYAML NOT INSTALLED, RETURNING DEFAULT")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_7(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = None

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_8(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(None, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_9(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default=None, encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_10(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=None)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_11(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_12(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_13(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", )

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_14(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="XXXX", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_15(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_16(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug(None, path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_17(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=None)
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_18(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug(path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_19(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", )
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_20(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("XXEmpty or missing YAML file, returning defaultXX", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_21(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("empty or missing yaml file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_22(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("EMPTY OR MISSING YAML FILE, RETURNING DEFAULT", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_23(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(None))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_24(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(None)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_25(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning(None, path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_26(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=None, error=str(e))
        return default


def x_read_yaml__mutmut_27(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=None)
        return default


def x_read_yaml__mutmut_28(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning(path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_29(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", error=str(e))
        return default


def x_read_yaml__mutmut_30(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), )
        return default


def x_read_yaml__mutmut_31(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("XXInvalid YAML fileXX", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_32(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("invalid yaml file", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_33(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("INVALID YAML FILE", path=str(path), error=str(e))
        return default


def x_read_yaml__mutmut_34(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(None), error=str(e))
        return default


def x_read_yaml__mutmut_35(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> Any:
    """Read YAML file with error handling.

    Args:
        path: YAML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed YAML data or default value

    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml_loads(content)
    except Exception as e:
        log.warning("Invalid YAML file", path=str(path), error=str(None))
        return default

x_read_yaml__mutmut_mutants : ClassVar[MutantDict] = {
'x_read_yaml__mutmut_1': x_read_yaml__mutmut_1, 
    'x_read_yaml__mutmut_2': x_read_yaml__mutmut_2, 
    'x_read_yaml__mutmut_3': x_read_yaml__mutmut_3, 
    'x_read_yaml__mutmut_4': x_read_yaml__mutmut_4, 
    'x_read_yaml__mutmut_5': x_read_yaml__mutmut_5, 
    'x_read_yaml__mutmut_6': x_read_yaml__mutmut_6, 
    'x_read_yaml__mutmut_7': x_read_yaml__mutmut_7, 
    'x_read_yaml__mutmut_8': x_read_yaml__mutmut_8, 
    'x_read_yaml__mutmut_9': x_read_yaml__mutmut_9, 
    'x_read_yaml__mutmut_10': x_read_yaml__mutmut_10, 
    'x_read_yaml__mutmut_11': x_read_yaml__mutmut_11, 
    'x_read_yaml__mutmut_12': x_read_yaml__mutmut_12, 
    'x_read_yaml__mutmut_13': x_read_yaml__mutmut_13, 
    'x_read_yaml__mutmut_14': x_read_yaml__mutmut_14, 
    'x_read_yaml__mutmut_15': x_read_yaml__mutmut_15, 
    'x_read_yaml__mutmut_16': x_read_yaml__mutmut_16, 
    'x_read_yaml__mutmut_17': x_read_yaml__mutmut_17, 
    'x_read_yaml__mutmut_18': x_read_yaml__mutmut_18, 
    'x_read_yaml__mutmut_19': x_read_yaml__mutmut_19, 
    'x_read_yaml__mutmut_20': x_read_yaml__mutmut_20, 
    'x_read_yaml__mutmut_21': x_read_yaml__mutmut_21, 
    'x_read_yaml__mutmut_22': x_read_yaml__mutmut_22, 
    'x_read_yaml__mutmut_23': x_read_yaml__mutmut_23, 
    'x_read_yaml__mutmut_24': x_read_yaml__mutmut_24, 
    'x_read_yaml__mutmut_25': x_read_yaml__mutmut_25, 
    'x_read_yaml__mutmut_26': x_read_yaml__mutmut_26, 
    'x_read_yaml__mutmut_27': x_read_yaml__mutmut_27, 
    'x_read_yaml__mutmut_28': x_read_yaml__mutmut_28, 
    'x_read_yaml__mutmut_29': x_read_yaml__mutmut_29, 
    'x_read_yaml__mutmut_30': x_read_yaml__mutmut_30, 
    'x_read_yaml__mutmut_31': x_read_yaml__mutmut_31, 
    'x_read_yaml__mutmut_32': x_read_yaml__mutmut_32, 
    'x_read_yaml__mutmut_33': x_read_yaml__mutmut_33, 
    'x_read_yaml__mutmut_34': x_read_yaml__mutmut_34, 
    'x_read_yaml__mutmut_35': x_read_yaml__mutmut_35
}

def read_yaml(*args, **kwargs):
    result = _mutmut_trampoline(x_read_yaml__mutmut_orig, x_read_yaml__mutmut_mutants, args, kwargs)
    return result 

read_yaml.__signature__ = _mutmut_signature(x_read_yaml__mutmut_orig)
x_read_yaml__mutmut_orig.__name__ = 'x_read_yaml'


def x_write_yaml__mutmut_orig(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_1(
    path: Path | str,
    data: Any,
    atomic: bool = False,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_2(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "XXutf-8XX",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_3(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "UTF-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_4(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = True,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_5(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError(None) from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_6(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("XXPyYAML is required for YAML operationsXX") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_7(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("pyyaml is required for yaml operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_8(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PYYAML IS REQUIRED FOR YAML OPERATIONS") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_9(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = None

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_10(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(None)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_11(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = None

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_12(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            None,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_13(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=None,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_14(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=None,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_15(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=None,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_16(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_17(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_18(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_19(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_20(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=False,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_21(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=True,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_22(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(None, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_23(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, None, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_24(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=None)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_25(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_26(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_27(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_28(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=None, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_29(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=None)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_30(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_31(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, )
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_32(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=False, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_33(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=False)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_34(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(None, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_35(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=None)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_36(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_37(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, )

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_38(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug(None, path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_39(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=None, atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_40(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=None)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_41(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug(path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_42(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_43(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), )
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_44(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("XXWrote YAML fileXX", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_45(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("wrote yaml file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_46(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("WROTE YAML FILE", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_47(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(None), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_48(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error(None, path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_49(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=None, error=str(e))
        raise


def x_write_yaml__mutmut_50(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=None)
        raise


def x_write_yaml__mutmut_51(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error(path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_52(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", error=str(e))
        raise


def x_write_yaml__mutmut_53(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), )
        raise


def x_write_yaml__mutmut_54(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("XXFailed to write YAML fileXX", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_55(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("failed to write yaml file", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_56(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("FAILED TO WRITE YAML FILE", path=str(path), error=str(e))
        raise


def x_write_yaml__mutmut_57(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(None), error=str(e))
        raise


def x_write_yaml__mutmut_58(
    path: Path | str,
    data: Any,
    atomic: bool = True,
    encoding: str = "utf-8",
    default_flow_style: bool = False,
) -> None:
    """Write YAML file, optionally atomic.

    Args:
        path: YAML file path
        data: Data to serialize
        atomic: Use atomic write
        encoding: Text encoding
        default_flow_style: Use flow style (JSON-like) instead of block style

    """
    try:
        import yaml  # noqa: F401
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    path = Path(path)

    try:
        content = yaml_dumps(
            data,
            default_flow_style=default_flow_style,
            allow_unicode=True,
            sort_keys=False,
        )

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote YAML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write YAML file", path=str(path), error=str(None))
        raise

x_write_yaml__mutmut_mutants : ClassVar[MutantDict] = {
'x_write_yaml__mutmut_1': x_write_yaml__mutmut_1, 
    'x_write_yaml__mutmut_2': x_write_yaml__mutmut_2, 
    'x_write_yaml__mutmut_3': x_write_yaml__mutmut_3, 
    'x_write_yaml__mutmut_4': x_write_yaml__mutmut_4, 
    'x_write_yaml__mutmut_5': x_write_yaml__mutmut_5, 
    'x_write_yaml__mutmut_6': x_write_yaml__mutmut_6, 
    'x_write_yaml__mutmut_7': x_write_yaml__mutmut_7, 
    'x_write_yaml__mutmut_8': x_write_yaml__mutmut_8, 
    'x_write_yaml__mutmut_9': x_write_yaml__mutmut_9, 
    'x_write_yaml__mutmut_10': x_write_yaml__mutmut_10, 
    'x_write_yaml__mutmut_11': x_write_yaml__mutmut_11, 
    'x_write_yaml__mutmut_12': x_write_yaml__mutmut_12, 
    'x_write_yaml__mutmut_13': x_write_yaml__mutmut_13, 
    'x_write_yaml__mutmut_14': x_write_yaml__mutmut_14, 
    'x_write_yaml__mutmut_15': x_write_yaml__mutmut_15, 
    'x_write_yaml__mutmut_16': x_write_yaml__mutmut_16, 
    'x_write_yaml__mutmut_17': x_write_yaml__mutmut_17, 
    'x_write_yaml__mutmut_18': x_write_yaml__mutmut_18, 
    'x_write_yaml__mutmut_19': x_write_yaml__mutmut_19, 
    'x_write_yaml__mutmut_20': x_write_yaml__mutmut_20, 
    'x_write_yaml__mutmut_21': x_write_yaml__mutmut_21, 
    'x_write_yaml__mutmut_22': x_write_yaml__mutmut_22, 
    'x_write_yaml__mutmut_23': x_write_yaml__mutmut_23, 
    'x_write_yaml__mutmut_24': x_write_yaml__mutmut_24, 
    'x_write_yaml__mutmut_25': x_write_yaml__mutmut_25, 
    'x_write_yaml__mutmut_26': x_write_yaml__mutmut_26, 
    'x_write_yaml__mutmut_27': x_write_yaml__mutmut_27, 
    'x_write_yaml__mutmut_28': x_write_yaml__mutmut_28, 
    'x_write_yaml__mutmut_29': x_write_yaml__mutmut_29, 
    'x_write_yaml__mutmut_30': x_write_yaml__mutmut_30, 
    'x_write_yaml__mutmut_31': x_write_yaml__mutmut_31, 
    'x_write_yaml__mutmut_32': x_write_yaml__mutmut_32, 
    'x_write_yaml__mutmut_33': x_write_yaml__mutmut_33, 
    'x_write_yaml__mutmut_34': x_write_yaml__mutmut_34, 
    'x_write_yaml__mutmut_35': x_write_yaml__mutmut_35, 
    'x_write_yaml__mutmut_36': x_write_yaml__mutmut_36, 
    'x_write_yaml__mutmut_37': x_write_yaml__mutmut_37, 
    'x_write_yaml__mutmut_38': x_write_yaml__mutmut_38, 
    'x_write_yaml__mutmut_39': x_write_yaml__mutmut_39, 
    'x_write_yaml__mutmut_40': x_write_yaml__mutmut_40, 
    'x_write_yaml__mutmut_41': x_write_yaml__mutmut_41, 
    'x_write_yaml__mutmut_42': x_write_yaml__mutmut_42, 
    'x_write_yaml__mutmut_43': x_write_yaml__mutmut_43, 
    'x_write_yaml__mutmut_44': x_write_yaml__mutmut_44, 
    'x_write_yaml__mutmut_45': x_write_yaml__mutmut_45, 
    'x_write_yaml__mutmut_46': x_write_yaml__mutmut_46, 
    'x_write_yaml__mutmut_47': x_write_yaml__mutmut_47, 
    'x_write_yaml__mutmut_48': x_write_yaml__mutmut_48, 
    'x_write_yaml__mutmut_49': x_write_yaml__mutmut_49, 
    'x_write_yaml__mutmut_50': x_write_yaml__mutmut_50, 
    'x_write_yaml__mutmut_51': x_write_yaml__mutmut_51, 
    'x_write_yaml__mutmut_52': x_write_yaml__mutmut_52, 
    'x_write_yaml__mutmut_53': x_write_yaml__mutmut_53, 
    'x_write_yaml__mutmut_54': x_write_yaml__mutmut_54, 
    'x_write_yaml__mutmut_55': x_write_yaml__mutmut_55, 
    'x_write_yaml__mutmut_56': x_write_yaml__mutmut_56, 
    'x_write_yaml__mutmut_57': x_write_yaml__mutmut_57, 
    'x_write_yaml__mutmut_58': x_write_yaml__mutmut_58
}

def write_yaml(*args, **kwargs):
    result = _mutmut_trampoline(x_write_yaml__mutmut_orig, x_write_yaml__mutmut_mutants, args, kwargs)
    return result 

write_yaml.__signature__ = _mutmut_signature(x_write_yaml__mutmut_orig)
x_write_yaml__mutmut_orig.__name__ = 'x_write_yaml'


def x_read_toml__mutmut_orig(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_1(
    path: Path | str,
    default: Any = None,
    encoding: str = "XXutf-8XX",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_2(
    path: Path | str,
    default: Any = None,
    encoding: str = "UTF-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_3(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = None

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_4(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(None, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_5(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default=None, encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_6(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=None)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_7(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_8(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_9(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", )

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_10(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="XXXX", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_11(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_12(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug(None, path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_13(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=None)
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_14(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug(path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_15(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", )
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_16(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("XXEmpty or missing TOML file, returning defaultXX", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_17(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("empty or missing toml file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_18(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("EMPTY OR MISSING TOML FILE, RETURNING DEFAULT", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_19(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(None))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_20(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_21(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(None)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_22(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning(None, path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_23(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=None, error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_24(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=None)
        return default if default is not None else {}


def x_read_toml__mutmut_25(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning(path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_26(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_27(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), )
        return default if default is not None else {}


def x_read_toml__mutmut_28(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("XXInvalid TOML fileXX", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_29(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("invalid toml file", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_30(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("INVALID TOML FILE", path=str(path), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_31(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(None), error=str(e))
        return default if default is not None else {}


def x_read_toml__mutmut_32(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(None))
        return default if default is not None else {}


def x_read_toml__mutmut_33(
    path: Path | str,
    default: Any = None,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """Read TOML file with error handling.

    Args:
        path: TOML file path
        default: Default value if file doesn't exist or is invalid
        encoding: Text encoding

    Returns:
        Parsed TOML data or default value

    """
    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return toml_loads(content)
    except Exception as e:
        log.warning("Invalid TOML file", path=str(path), error=str(e))
        return default if default is None else {}

x_read_toml__mutmut_mutants : ClassVar[MutantDict] = {
'x_read_toml__mutmut_1': x_read_toml__mutmut_1, 
    'x_read_toml__mutmut_2': x_read_toml__mutmut_2, 
    'x_read_toml__mutmut_3': x_read_toml__mutmut_3, 
    'x_read_toml__mutmut_4': x_read_toml__mutmut_4, 
    'x_read_toml__mutmut_5': x_read_toml__mutmut_5, 
    'x_read_toml__mutmut_6': x_read_toml__mutmut_6, 
    'x_read_toml__mutmut_7': x_read_toml__mutmut_7, 
    'x_read_toml__mutmut_8': x_read_toml__mutmut_8, 
    'x_read_toml__mutmut_9': x_read_toml__mutmut_9, 
    'x_read_toml__mutmut_10': x_read_toml__mutmut_10, 
    'x_read_toml__mutmut_11': x_read_toml__mutmut_11, 
    'x_read_toml__mutmut_12': x_read_toml__mutmut_12, 
    'x_read_toml__mutmut_13': x_read_toml__mutmut_13, 
    'x_read_toml__mutmut_14': x_read_toml__mutmut_14, 
    'x_read_toml__mutmut_15': x_read_toml__mutmut_15, 
    'x_read_toml__mutmut_16': x_read_toml__mutmut_16, 
    'x_read_toml__mutmut_17': x_read_toml__mutmut_17, 
    'x_read_toml__mutmut_18': x_read_toml__mutmut_18, 
    'x_read_toml__mutmut_19': x_read_toml__mutmut_19, 
    'x_read_toml__mutmut_20': x_read_toml__mutmut_20, 
    'x_read_toml__mutmut_21': x_read_toml__mutmut_21, 
    'x_read_toml__mutmut_22': x_read_toml__mutmut_22, 
    'x_read_toml__mutmut_23': x_read_toml__mutmut_23, 
    'x_read_toml__mutmut_24': x_read_toml__mutmut_24, 
    'x_read_toml__mutmut_25': x_read_toml__mutmut_25, 
    'x_read_toml__mutmut_26': x_read_toml__mutmut_26, 
    'x_read_toml__mutmut_27': x_read_toml__mutmut_27, 
    'x_read_toml__mutmut_28': x_read_toml__mutmut_28, 
    'x_read_toml__mutmut_29': x_read_toml__mutmut_29, 
    'x_read_toml__mutmut_30': x_read_toml__mutmut_30, 
    'x_read_toml__mutmut_31': x_read_toml__mutmut_31, 
    'x_read_toml__mutmut_32': x_read_toml__mutmut_32, 
    'x_read_toml__mutmut_33': x_read_toml__mutmut_33
}

def read_toml(*args, **kwargs):
    result = _mutmut_trampoline(x_read_toml__mutmut_orig, x_read_toml__mutmut_mutants, args, kwargs)
    return result 

read_toml.__signature__ = _mutmut_signature(x_read_toml__mutmut_orig)
x_read_toml__mutmut_orig.__name__ = 'x_read_toml'


def x_write_toml__mutmut_orig(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_1(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = False,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_2(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "XXutf-8XX",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_3(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "UTF-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_4(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError(None) from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_5(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("XXtomli-w is required for TOML write operationsXX") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_6(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for toml write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_7(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("TOMLI-W IS REQUIRED FOR TOML WRITE OPERATIONS") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_8(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = None

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_9(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(None)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_10(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = None

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_11(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(None)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_12(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(None, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_13(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, None, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_14(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=None)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_15(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_16(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_17(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_18(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=None, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_19(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=None)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_20(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_21(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, )
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_22(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=False, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_23(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=False)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_24(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(None, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_25(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=None)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_26(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_27(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, )

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_28(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug(None, path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_29(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=None, atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_30(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=None)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_31(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug(path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_32(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_33(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), )
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_34(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("XXWrote TOML fileXX", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_35(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("wrote toml file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_36(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("WROTE TOML FILE", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_37(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(None), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_38(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error(None, path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_39(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=None, error=str(e))
        raise


def x_write_toml__mutmut_40(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=None)
        raise


def x_write_toml__mutmut_41(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error(path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_42(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", error=str(e))
        raise


def x_write_toml__mutmut_43(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), )
        raise


def x_write_toml__mutmut_44(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("XXFailed to write TOML fileXX", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_45(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("failed to write toml file", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_46(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("FAILED TO WRITE TOML FILE", path=str(path), error=str(e))
        raise


def x_write_toml__mutmut_47(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(None), error=str(e))
        raise


def x_write_toml__mutmut_48(
    path: Path | str,
    data: dict[str, Any],
    atomic: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write TOML file, optionally atomic.

    Args:
        path: TOML file path
        data: Data to serialize (must be a dictionary)
        atomic: Use atomic write
        encoding: Text encoding

    """
    try:
        import tomli_w  # noqa: F401
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    path = Path(path)

    try:
        content = toml_dumps(data)

        if atomic:
            atomic_write_text(path, content, encoding=encoding)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)

        log.debug("Wrote TOML file", path=str(path), atomic=atomic)
    except Exception as e:
        log.error("Failed to write TOML file", path=str(path), error=str(None))
        raise

x_write_toml__mutmut_mutants : ClassVar[MutantDict] = {
'x_write_toml__mutmut_1': x_write_toml__mutmut_1, 
    'x_write_toml__mutmut_2': x_write_toml__mutmut_2, 
    'x_write_toml__mutmut_3': x_write_toml__mutmut_3, 
    'x_write_toml__mutmut_4': x_write_toml__mutmut_4, 
    'x_write_toml__mutmut_5': x_write_toml__mutmut_5, 
    'x_write_toml__mutmut_6': x_write_toml__mutmut_6, 
    'x_write_toml__mutmut_7': x_write_toml__mutmut_7, 
    'x_write_toml__mutmut_8': x_write_toml__mutmut_8, 
    'x_write_toml__mutmut_9': x_write_toml__mutmut_9, 
    'x_write_toml__mutmut_10': x_write_toml__mutmut_10, 
    'x_write_toml__mutmut_11': x_write_toml__mutmut_11, 
    'x_write_toml__mutmut_12': x_write_toml__mutmut_12, 
    'x_write_toml__mutmut_13': x_write_toml__mutmut_13, 
    'x_write_toml__mutmut_14': x_write_toml__mutmut_14, 
    'x_write_toml__mutmut_15': x_write_toml__mutmut_15, 
    'x_write_toml__mutmut_16': x_write_toml__mutmut_16, 
    'x_write_toml__mutmut_17': x_write_toml__mutmut_17, 
    'x_write_toml__mutmut_18': x_write_toml__mutmut_18, 
    'x_write_toml__mutmut_19': x_write_toml__mutmut_19, 
    'x_write_toml__mutmut_20': x_write_toml__mutmut_20, 
    'x_write_toml__mutmut_21': x_write_toml__mutmut_21, 
    'x_write_toml__mutmut_22': x_write_toml__mutmut_22, 
    'x_write_toml__mutmut_23': x_write_toml__mutmut_23, 
    'x_write_toml__mutmut_24': x_write_toml__mutmut_24, 
    'x_write_toml__mutmut_25': x_write_toml__mutmut_25, 
    'x_write_toml__mutmut_26': x_write_toml__mutmut_26, 
    'x_write_toml__mutmut_27': x_write_toml__mutmut_27, 
    'x_write_toml__mutmut_28': x_write_toml__mutmut_28, 
    'x_write_toml__mutmut_29': x_write_toml__mutmut_29, 
    'x_write_toml__mutmut_30': x_write_toml__mutmut_30, 
    'x_write_toml__mutmut_31': x_write_toml__mutmut_31, 
    'x_write_toml__mutmut_32': x_write_toml__mutmut_32, 
    'x_write_toml__mutmut_33': x_write_toml__mutmut_33, 
    'x_write_toml__mutmut_34': x_write_toml__mutmut_34, 
    'x_write_toml__mutmut_35': x_write_toml__mutmut_35, 
    'x_write_toml__mutmut_36': x_write_toml__mutmut_36, 
    'x_write_toml__mutmut_37': x_write_toml__mutmut_37, 
    'x_write_toml__mutmut_38': x_write_toml__mutmut_38, 
    'x_write_toml__mutmut_39': x_write_toml__mutmut_39, 
    'x_write_toml__mutmut_40': x_write_toml__mutmut_40, 
    'x_write_toml__mutmut_41': x_write_toml__mutmut_41, 
    'x_write_toml__mutmut_42': x_write_toml__mutmut_42, 
    'x_write_toml__mutmut_43': x_write_toml__mutmut_43, 
    'x_write_toml__mutmut_44': x_write_toml__mutmut_44, 
    'x_write_toml__mutmut_45': x_write_toml__mutmut_45, 
    'x_write_toml__mutmut_46': x_write_toml__mutmut_46, 
    'x_write_toml__mutmut_47': x_write_toml__mutmut_47, 
    'x_write_toml__mutmut_48': x_write_toml__mutmut_48
}

def write_toml(*args, **kwargs):
    result = _mutmut_trampoline(x_write_toml__mutmut_orig, x_write_toml__mutmut_mutants, args, kwargs)
    return result 

write_toml.__signature__ = _mutmut_signature(x_write_toml__mutmut_orig)
x_write_toml__mutmut_orig.__name__ = 'x_write_toml'


__all__ = [
    "read_json",
    "read_toml",
    "read_yaml",
    "write_json",
    "write_toml",
    "write_yaml",
]


# <3 🧱🤝📄🪄
