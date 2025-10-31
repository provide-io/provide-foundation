#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Configuration-related exceptions."""


class ConfigurationError(FoundationError):
    """Raised when configuration is invalid or cannot be loaded.

    Args:
        message: Error message describing the configuration issue.
        config_key: Optional configuration key that caused the error.
        config_source: Optional source of the configuration (file, env, etc.).
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise ConfigurationError("Missing required config")
        >>> raise ConfigurationError("Invalid timeout", config_key="timeout")

    """

    def __init__(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault("context", {})["config.key"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "CONFIG_ERROR"


class ValidationError(FoundationError):
    """Raised when data validation fails.

    Args:
        message: Validation error message.
        field: Optional field name that failed validation.
        value: Optional invalid value.
        rule: Optional validation rule that failed.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise ValidationError("Invalid email format")
        >>> raise ValidationError("Value out of range", field="age", value=-1)

    """

    def __init__(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault("context", {})["validation.field"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "VALIDATION_ERROR"


class ConfigValidationError(ValidationError):
    """Raised when configuration validation fails.

    This is a specialized validation error for configuration-specific validation failures.

    Args:
        message: Validation error message.
        config_class: Optional name of the config class.
        **kwargs: Additional context passed to ValidationError.

    Examples:
        >>> raise ConfigValidationError("Invalid database configuration")
        >>> raise ConfigValidationError("Port must be positive", field="port", value=-1)

    """

    def __init__(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", {})["config.class"] = config_class
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "CONFIG_VALIDATION_ERROR"


# 🧱🏗️🔚
