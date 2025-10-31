#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
import os
from typing import Any, Self, TypeVar

from attrs import fields

from provide.foundation.config.base import BaseConfig, field
from provide.foundation.config.types import ConfigSource

"""Environment variable configuration utilities."""


T = TypeVar("T")


def get_env(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

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
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def env_field(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

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
    """Configuration that can be loaded from environment variables."""

    @classmethod
    def from_env(
        cls,
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False,
    ) -> Self:
        """Load configuration from environment variables synchronously.

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

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Get value from environment
            raw_value = os.environ.get(env_var)

            if raw_value is not None:
                value = raw_value
                # Check if it's a file-based secret
                if value.startswith("file://"):
                    # Read synchronously
                    file_path = value[7:]
                    from provide.foundation.file.safe import safe_read_text

                    try:
                        value = safe_read_text(file_path, default="").strip()
                        if not value:
                            raise ValueError(f"Secret file is empty: {file_path}")
                    except Exception as e:
                        raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

                # Apply parser if specified
                parser = attr.metadata.get("env_parser")

                if parser:
                    try:
                        value = parser(value)
                    except Exception as e:
                        raise ValueError(f"Failed to parse {env_var}: {e}") from e
                else:
                    # Try to infer parser from type
                    from provide.foundation.parsers import auto_parse

                    value = auto_parse(attr, value)

                data[attr.name] = value

        return cls.from_dict(data, source=ConfigSource.ENV)

    def to_env_dict(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

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

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

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


# 🧱🏗️🔚
