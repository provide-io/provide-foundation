#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from attrs import define, field, fields, validators

from provide.foundation.config import defaults
from provide.foundation.config.base import ConfigSource, field as config_field
from provide.foundation.config.converters import parse_bool_strict
from provide.foundation.config.defaults import path_converter
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.errors.config import ConfigurationError
from provide.foundation.errors.runtime import StateError
from provide.foundation.file.formats import read_json, read_toml, read_yaml, write_json, write_toml, write_yaml
from provide.foundation.logger import get_logger

"""Unified context for configuration and CLI state management."""

VALID_LOG_LEVELS = {"TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@define(slots=True, repr=False)
class CLIContext(RuntimeConfig):
    """Runtime context for CLI execution and state management.

    Manages CLI-specific settings, output formatting, and runtime state
    during command execution. Supports loading from files, environment variables,
    and programmatic updates during CLI command execution.
    """

    log_level: str = config_field(
        default=defaults.DEFAULT_CONTEXT_LOG_LEVEL,
        env_var="PROVIDE_LOG_LEVEL",
        converter=str.upper,
        validator=validators.in_(VALID_LOG_LEVELS),
        description="Logging level for CLI output",
    )
    profile: str = config_field(
        default=defaults.DEFAULT_CONTEXT_PROFILE,
        env_var="PROVIDE_PROFILE",
        description="Configuration profile to use",
    )
    debug: bool = config_field(
        default=defaults.DEFAULT_CONTEXT_DEBUG,
        env_var="PROVIDE_DEBUG",
        converter=parse_bool_strict,
        description="Enable debug mode",
    )
    json_output: bool = config_field(
        default=defaults.DEFAULT_CONTEXT_JSON_OUTPUT,
        env_var="PROVIDE_JSON_OUTPUT",
        converter=parse_bool_strict,
        description="Output in JSON format",
    )
    config_file: Path | None = config_field(  # noqa: RUF009
        default=defaults.DEFAULT_CONTEXT_CONFIG_FILE,
        env_var="PROVIDE_CONFIG_FILE",
        converter=path_converter,
        description="Path to configuration file",
    )
    log_file: Path | None = config_field(  # noqa: RUF009
        default=defaults.DEFAULT_CONTEXT_LOG_FILE,
        env_var="PROVIDE_LOG_FILE",
        converter=path_converter,
        description="Path to log file",
    )
    log_format: str = config_field(
        default=defaults.DEFAULT_CONTEXT_LOG_FORMAT,
        env_var="PROVIDE_LOG_FORMAT",
        description="Log output format (key_value or json)",
    )
    no_color: bool = config_field(
        default=defaults.DEFAULT_CONTEXT_NO_COLOR,
        env_var="NO_COLOR",
        converter=parse_bool_strict,
        description="Disable colored output",
    )
    no_emoji: bool = config_field(
        default=defaults.DEFAULT_CONTEXT_NO_EMOJI,
        env_var="PROVIDE_NO_EMOJI",
        converter=parse_bool_strict,
        description="Disable emoji in output",
    )

    # Private fields - using Factory for mutable defaults
    _logger: Any = field(init=False, factory=lambda: None, repr=False)
    _frozen: bool = field(init=False, default=False, repr=False)

    def __attrs_post_init__(self) -> None:
        """Post-initialization hook."""
        # Validation is handled by attrs validators

    def update_from_env(self, prefix: str = "PROVIDE") -> None:
        """Update context from environment variables.

        Args:
            prefix: Environment variable prefix (default: PROVIDE)

        """
        if self._frozen:
            raise StateError(
                "Context is frozen and cannot be modified",
                code="CONTEXT_FROZEN",
                context_type=type(self).__name__,
            )

        # Create default instance and environment instance
        default_ctx = self.__class__()  # All defaults
        env_ctx = self.from_env(prefix=prefix)  # Environment + defaults

        # Only update fields where environment differs from default
        for attr in fields(self.__class__):
            if not attr.name.startswith("_"):  # Skip private fields
                default_value = getattr(default_ctx, attr.name)
                env_value = getattr(env_ctx, attr.name)

                # If environment value differs from default, it came from env
                if env_value != default_value:
                    setattr(self, attr.name, env_value)

    def to_dict(self, include_sensitive: bool = True) -> dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "log_level": self.log_level,
            "profile": self.profile,
            "debug": self.debug,
            "json_output": self.json_output,
            "config_file": str(self.config_file) if self.config_file else None,
            "log_file": str(self.log_file) if self.log_file else None,
            "log_format": self.log_format,
            "no_color": self.no_color,
            "no_emoji": self.no_emoji,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: ConfigSource = ConfigSource.RUNTIME) -> CLIContext:
        """Create context from dictionary.

        Args:
            data: Dictionary with context values
            source: Source of the configuration data

        Returns:
            New CLIContext instance

        """
        kwargs = {}

        if "log_level" in data:
            kwargs["log_level"] = data["log_level"]
        if "profile" in data:
            kwargs["profile"] = data["profile"]
        if "debug" in data:
            kwargs["debug"] = data["debug"]
        if "json_output" in data:
            kwargs["json_output"] = data["json_output"]
        if data.get("config_file"):
            kwargs["config_file"] = Path(data["config_file"])
        if data.get("log_file"):
            kwargs["log_file"] = Path(data["log_file"])
        if "log_format" in data:
            kwargs["log_format"] = data["log_format"]
        if "no_color" in data:
            kwargs["no_color"] = data["no_color"]
        if "no_emoji" in data:
            kwargs["no_emoji"] = data["no_emoji"]

        return cls(**kwargs)

    def _load_config_data(self, path: Path) -> dict[str, Any]:
        """Load configuration data from file based on extension."""
        if path.suffix in (".toml", ".tml"):
            return read_toml(path)
        elif path.suffix == ".json":
            return read_json(path)
        elif path.suffix in (".yaml", ".yml"):
            return read_yaml(path)
        else:
            raise ConfigurationError(
                f"Unsupported config format: {path.suffix}",
                code="UNSUPPORTED_CONFIG_FORMAT",
                path=str(path),
                suffix=path.suffix,
            )

    def _update_from_config_data(self, data: dict[str, Any]) -> None:
        """Update context fields from configuration data."""
        # Simple field mappings
        field_mappings = {
            "log_level": "log_level",
            "profile": "profile",
            "debug": "debug",
            "json_output": "json_output",
            "log_format": "log_format",
            "no_color": "no_color",
            "no_emoji": "no_emoji",
        }

        for data_key, attr_name in field_mappings.items():
            if data_key in data:
                setattr(self, attr_name, data[data_key])

        # Path fields that need conversion
        if data.get("config_file"):
            self.config_file = Path(data["config_file"])
        if data.get("log_file"):
            self.log_file = Path(data["log_file"])

    def load_config(self, path: str | Path) -> None:
        """Load configuration from file.

        Supports TOML, JSON, and YAML formats based on file extension.

        Args:
            path: Path to configuration file

        """
        # CLIContext is not frozen, so we can modify it
        path = Path(path)
        data = self._load_config_data(path)
        self._update_from_config_data(data)
        self._validate()

    def save_config(self, path: str | Path) -> None:
        """Save configuration to file.

        Format is determined by file extension.

        Args:
            path: Path to save configuration

        """
        path = Path(path)
        data = self.to_dict()

        # Remove None values for cleaner output
        data = {k: v for k, v in data.items() if v is not None}

        if path.suffix in (".toml", ".tml"):
            write_toml(path, data)
        elif path.suffix == ".json":
            write_json(path, data, indent=2)
        elif path.suffix in (".yaml", ".yml"):
            write_yaml(path, data, default_flow_style=False)
        elif not path.suffix:
            raise ConfigurationError(
                f"Unsupported config format: no file extension for {path}",
                code="MISSING_FILE_EXTENSION",
                path=str(path),
            )
        else:
            raise ConfigurationError(
                f"Unsupported config format: {path.suffix}",
                code="UNSUPPORTED_CONFIG_FORMAT",
                path=str(path),
                suffix=path.suffix,
            )

    def _merge_with_override(self, merged_data: dict[str, Any], other_data: dict[str, Any]) -> None:
        """Merge data with override_defaults=True strategy."""
        for key, value in other_data.items():
            if value is not None:
                merged_data[key] = value

    def _get_field_defaults(self) -> dict[str, Any]:
        """Get default values for all fields."""
        defaults = {}
        for f in fields(CLIContext):
            if not f.name.startswith("_"):  # Skip private fields
                # Check if default is a Factory using hasattr
                if hasattr(f.default, "factory") and f.default is not None:
                    defaults[f.name] = f.default.factory()
                elif f.default is not None:
                    defaults[f.name] = f.default
        return defaults

    def _merge_without_override(self, merged_data: dict[str, Any], other_data: dict[str, Any]) -> None:
        """Merge data with override_defaults=False strategy."""
        defaults = self._get_field_defaults()

        for key, value in other_data.items():
            if value is not None:
                # Check if this is different from the default
                if key in defaults and value == defaults[key]:
                    # Skip default values
                    continue
                merged_data[key] = value

    def merge(self, other: CLIContext, override_defaults: bool = False) -> CLIContext:
        """Merge with another context, with other taking precedence.

        Args:
            other: CLIContext to merge with
            override_defaults: If False, only override if other's value differs from its class default

        Returns:
            New merged CLIContext instance

        """
        merged_data = self.to_dict()
        other_data = other.to_dict()

        if override_defaults:
            self._merge_with_override(merged_data, other_data)
        else:
            self._merge_without_override(merged_data, other_data)

        return CLIContext.from_dict(merged_data)

    def freeze(self) -> None:
        """Freeze context to prevent further modifications."""
        # Note: With attrs, we can't dynamically freeze an instance
        # This is kept for API compatibility but does nothing
        self._frozen = True

    def copy(self) -> CLIContext:
        """Create a deep copy of the context."""
        return copy.deepcopy(self)

    @property
    def logger(self) -> Any:
        """Get or create a logger for this context."""
        if self._logger is None:
            self._logger = get_logger("context").bind(
                log_level=self.log_level,
                profile=self.profile,
            )
        return self._logger

    def _validate(self) -> None:
        """Validate context values. For attrs compatibility."""
        # Validation is handled by attrs validators automatically


# 🧱🏗️🔚
