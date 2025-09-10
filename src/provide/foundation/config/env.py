"""
Environment variable configuration utilities.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import os
from typing import Any, TypeVar

try:
    import aiofiles
except ImportError:
    aiofiles = None
from attrs import fields

from provide.foundation.config.base import BaseConfig, field
from provide.foundation.config.types import ConfigSource

T = TypeVar("T")


async def get_env_async(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """
    Get environment variable value with optional file-based secret support (async).

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found
    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets asynchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        try:
            async with aiofiles.open(file_path) as f:
                value = await f.read()
                value = value.strip()
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}")

    return value


def get_env(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """
    Get environment variable value with optional file-based secret support (sync).

    This is a compatibility function that uses sync I/O.
    Prefer get_env_async for new code.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found
    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        try:
            with open(file_path) as f:
                value = f.read().strip()
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}")

    return value


def env_field(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs,
) -> Any:
    """
    Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor
    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


class RuntimeConfig(BaseConfig):
    """
    Configuration that can be loaded from environment variables.
    All methods are async to support async secret fetching and validation.
    """

    @classmethod
    def from_env(
        cls: type[T],
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False,
    ) -> T:
        """
        Load configuration from environment variables synchronously.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        Returns:
            Configuration instance
        """
        data = {}

        for attr in fields(cls):
            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                # Build from prefix and field name
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper() if not case_sensitive else attr.name

                if field_prefix:
                    env_var = f"{field_prefix}{delimiter}{field_name}"
                else:
                    env_var = field_name

            # Get value from environment
            raw_value = os.environ.get(env_var)

            if raw_value is not None:
                value = raw_value
                # Check if it's a file-based secret
                if value.startswith("file://"):
                    # Read synchronously
                    file_path = value[7:]
                    try:
                        with open(file_path) as f:
                            value = f.read().strip()
                    except Exception as e:
                        raise ValueError(
                            f"Failed to read secret from file '{file_path}': {e}"
                        )

                # Apply parser if specified
                parser = attr.metadata.get("env_parser")

                if parser:
                    try:
                        value = parser(value)
                    except Exception as e:
                        raise ValueError(f"Failed to parse {env_var}: {e}")
                else:
                    # Try to infer parser from type
                    from provide.foundation.utils.parsing import auto_parse
                    value = auto_parse(attr, value)

                data[attr.name] = value

        return cls.from_dict(data, source=ConfigSource.ENV)

    @classmethod
    async def from_env_async(
        cls: type[T],
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False,
        use_async_secrets: bool = True,
    ) -> T:
        """
        Load configuration from environment variables asynchronously.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive
            use_async_secrets: Whether to use async I/O for file-based secrets

        Returns:
            Configuration instance
        """
        data = {}

        # Collect all async operations
        async_tasks = {}
        sync_values = {}

        for attr in fields(cls):
            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                # Build from prefix and field name
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper() if not case_sensitive else attr.name

                if field_prefix:
                    env_var = f"{field_prefix}{delimiter}{field_name}"
                else:
                    env_var = field_name

            # Get value from environment
            raw_value = os.environ.get(env_var)

            if raw_value is not None:
                # Check if it's a file-based secret
                if use_async_secrets and raw_value.startswith("file://"):
                    # Schedule async read
                    async_tasks[attr.name] = cls._read_secret_async(raw_value[7:])
                else:
                    # Store for sync processing
                    sync_values[attr.name] = (attr, raw_value)

        # Execute all async reads in parallel
        if async_tasks:
            async_results = await asyncio.gather(*async_tasks.values())
            for field_name, value in zip(
                async_tasks.keys(), async_results, strict=False
            ):
                # Find the attribute
                attr = next(a for a in fields(cls) if a.name == field_name)
                sync_values[field_name] = (attr, value)

        # Process all values
        for field_name, (attr, value) in sync_values.items():
            # Apply parser if specified
            parser = attr.metadata.get("env_parser")

            if parser:
                try:
                    value = parser(value)
                except Exception as e:
                    raise ValueError(f"Failed to parse {env_var}: {e}")
            else:
                # Try to infer parser from type
                from provide.foundation.utils.parsing import auto_parse
                value = auto_parse(attr, value)

            data[field_name] = value

        return cls.from_dict(data, source=ConfigSource.ENV)

    @staticmethod
    async def _read_secret_async(file_path: str) -> str:
        """Read secret from file asynchronously."""
        try:
            if aiofiles:
                async with aiofiles.open(file_path) as f:
                    content = await f.read()
                    return content.strip()
            else:
                # Fallback to synchronous read
                with open(file_path) as f:
                    content = f.read()
                    return content.strip()
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}")


    def to_env_dict(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """
        Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables
        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                if field_prefix:
                    env_var = f"{field_prefix}{delimiter}{field_name}"
                else:
                    env_var = field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict
