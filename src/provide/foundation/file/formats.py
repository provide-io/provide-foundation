"""Format-specific file operations for JSON, YAML, TOML."""

import json
from pathlib import Path
from typing import Any

from provide.foundation.file.atomic import atomic_write_text
from provide.foundation.file.safe import safe_read_text
from provide.foundation.logger import get_logger

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
        return json.loads(content)
    except json.JSONDecodeError as e:
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
        content = json.dumps(
            data, indent=indent, sort_keys=sort_keys, ensure_ascii=False
        )

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
        import yaml
    except ImportError:
        log.warning("PyYAML not installed, returning default")
        return default

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing YAML file, returning default", path=str(path))
        return default

    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as e:
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
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required for YAML operations")

    path = Path(path)

    try:
        content = yaml.dump(
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
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            log.warning("tomllib/tomli not available, returning default")
            return default if default is not None else {}

    content = safe_read_text(path, default="", encoding=encoding)

    if not content:
        log.debug("Empty or missing TOML file, returning default", path=str(path))
        return default if default is not None else {}

    try:
        return tomllib.loads(content)
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
        import tomli_w
    except ImportError:
        raise ImportError("tomli-w is required for TOML write operations")

    path = Path(path)

    try:
        content = tomli_w.dumps(data)

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
