#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def read_json(
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


def write_json(
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


def read_yaml(
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


def write_yaml(
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


def read_toml(
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


def write_toml(
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


__all__ = [
    "read_json",
    "read_toml",
    "read_yaml",
    "write_json",
    "write_toml",
    "write_yaml",
]

# 🧱🏗️🔚
