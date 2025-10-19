# provide/foundation/config/env.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
import os
from typing import Any, ClassVar, Self, TypeVar

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

    _pending_registration: ClassVar[list[type[RuntimeConfig]]] = []
    _registration_complete: ClassVar[bool] = False

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Queue config class for Hub registration.

        This method is called automatically when a subclass is defined.
        It queues the class for later registration with the Hub to avoid
        import order issues.

        Args:
            **kwargs: Keyword arguments passed to super().__init_subclass__

        """
        super().__init_subclass__(**kwargs)
        # Queue for registration instead of immediate registration
        # to avoid circular import issues with Hub
        if not cls._registration_complete:
            RuntimeConfig._pending_registration.append(cls)

    @classmethod
    def register_all_configs(cls) -> None:
        """Register all pending config schemas with the Hub.

        This should be called after the Hub is initialized to register
        all discovered RuntimeConfig subclasses with the CONFIG_SCHEMA dimension.

        """
        if cls._registration_complete:
            return

        from provide.foundation.hub import get_hub
        from provide.foundation.hub.categories import ComponentCategory

        hub = get_hub()

        for config_cls in cls._pending_registration:
            # Extract category from module path
            # e.g., "provide.foundation.logger.config.logging" -> "logger"
            module_parts = config_cls.__module__.split(".")
            category = "core"
            if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
                category = module_parts[2]

            # Check if class has any env_var fields
            has_env_vars = False
            try:
                for attr in fields(config_cls):
                    if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                        has_env_vars = True
                        break
            except Exception:
                # If we can't inspect fields, assume it might have env vars
                has_env_vars = True

            hub._component_registry.register(
                name=config_cls.__name__,
                value=config_cls,
                dimension=ComponentCategory.CONFIG_SCHEMA.value,
                metadata={
                    "module": config_cls.__module__,
                    "category": category,
                    "has_env_vars": has_env_vars,
                    "doc": config_cls.__doc__ or "",
                },
            )

        cls._pending_registration.clear()
        cls._registration_complete = True

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


# <3 🧱🤝⚙️🪄
