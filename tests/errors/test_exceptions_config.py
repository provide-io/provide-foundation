#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for configuration error classes."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.errors.config import ConfigurationError, ValidationError


class TestConfigurationError(FoundationTestCase):
    """Test ConfigurationError class."""

    def test_basic_creation(self) -> None:
        """Test basic ConfigurationError."""
        error = ConfigurationError("Config invalid")
        assert error.message == "Config invalid"
        assert error.code == "CONFIG_ERROR"

    def test_with_config_key(self) -> None:
        """Test with config_key parameter."""
        error = ConfigurationError("Invalid value", config_key="timeout")
        assert error.context["config.key"] == "timeout"

    def test_with_config_source(self) -> None:
        """Test with config_source parameter."""
        error = ConfigurationError("Parse error", config_source="/etc/app.conf")
        assert error.context["config.source"] == "/etc/app.conf"

    def test_with_all_parameters(self) -> None:
        """Test with all specific parameters."""
        error = ConfigurationError(
            "Config error",
            config_key="database.url",
            config_source="environment",
            extra_param="value",
        )
        assert error.context["config.key"] == "database.url"
        assert error.context["config.source"] == "environment"
        assert error.context["extra_param"] == "value"


class TestValidationError(FoundationTestCase):
    """Test ValidationError class."""

    def test_basic_creation(self) -> None:
        """Test basic ValidationError."""
        error = ValidationError("Invalid input")
        assert error.message == "Invalid input"
        assert error.code == "VALIDATION_ERROR"

    def test_with_field(self) -> None:
        """Test with field parameter."""
        error = ValidationError("Required field", field="email")
        assert error.context["validation.field"] == "email"

    def test_with_value(self) -> None:
        """Test with value parameter."""
        error = ValidationError("Invalid format", value="not-an-email")
        assert error.context["validation.value"] == "not-an-email"

    def test_with_rule(self) -> None:
        """Test with rule parameter."""
        error = ValidationError("Failed validation", rule="email_format")
        assert error.context["validation.rule"] == "email_format"

    def test_with_all_parameters(self) -> None:
        """Test with all validation parameters."""
        error = ValidationError(
            "Validation failed",
            field="age",
            value=-1,
            rule="positive_integer",
            max_value=120,
        )
        assert error.context["validation.field"] == "age"
        assert error.context["validation.value"] == "-1"
        assert error.context["validation.rule"] == "positive_integer"
        assert error.context["max_value"] == 120

    def test_value_conversion_to_string(self) -> None:
        """Test that value is converted to string."""
        error = ValidationError("Invalid", value={"complex": "object"})
        assert error.context["validation.value"] == "{'complex': 'object'}"


# 🧱🏗️🔚
