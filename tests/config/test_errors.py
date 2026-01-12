#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for config.errors module."""

from provide.testkit import FoundationTestCase

from provide.foundation.config.errors import (
    ConfigError,
    ParseError,
    ValidationError,
    format_invalid_value_error,
    format_validation_error,
)


class TestConfigError(FoundationTestCase):
    """Test base ConfigError class."""

    def test_config_error_inherits_from_foundation_error(self) -> None:
        """Test ConfigError inherits from FoundationError."""
        from provide.foundation.errors.base import FoundationError

        error = ConfigError("test message")
        assert isinstance(error, FoundationError)

    def test_config_error_default_code(self) -> None:
        """Test ConfigError default error code."""
        error = ConfigError("test message")
        assert error._default_code() == "CONFIG_ERROR"

    def test_config_error_with_message(self) -> None:
        """Test ConfigError with custom message."""
        message = "Custom configuration error"
        error = ConfigError(message)
        assert str(error) == message

    def test_config_error_with_kwargs(self) -> None:
        """Test ConfigError accepts additional context."""
        error = ConfigError("test", field="test_field", value=123)
        # Base error should store kwargs in context
        assert error.message == "test"


class TestParseError(FoundationTestCase):
    """Test ParseError class."""

    def test_parse_error_inherits_from_config_error(self) -> None:
        """Test ParseError inherits from ConfigError."""
        error = ParseError("test", value="invalid")
        assert isinstance(error, ConfigError)

    def test_parse_error_default_code(self) -> None:
        """Test ParseError default error code."""
        error = ParseError("test", value="invalid")
        assert error._default_code() == "PARSE_ERROR"

    def test_parse_error_with_value(self) -> None:
        """Test ParseError with value parameter."""
        error = ParseError("Invalid value", value="bad_value")
        assert error.message == "Invalid value"

    def test_parse_error_with_field_name(self) -> None:
        """Test ParseError with field_name parameter."""
        error = ParseError(
            "Invalid field",
            value="bad_value",
            field_name="test_field",
        )
        assert error.message == "Invalid field"

    def test_parse_error_with_expected_type(self) -> None:
        """Test ParseError with expected_type parameter."""
        error = ParseError(
            "Type error",
            value="not_a_bool",
            expected_type="boolean",
        )
        assert error.message == "Type error"

    def test_parse_error_with_valid_options(self) -> None:
        """Test ParseError with valid_options parameter."""
        error = ParseError(
            "Invalid option",
            value="INVALID",
            valid_options=["DEBUG", "INFO", "ERROR"],
        )
        assert error.message == "Invalid option"

    def test_parse_error_with_all_parameters(self) -> None:
        """Test ParseError with all parameters."""
        error = ParseError(
            "Complete parse error",
            value="bad_value",
            field_name="test_field",
            expected_type="string",
            valid_options=["option1", "option2"],
            extra_context="additional info",
        )
        assert error.message == "Complete parse error"


class TestValidationError(FoundationTestCase):
    """Test ValidationError class."""

    def test_validation_error_inherits_from_config_error(self) -> None:
        """Test ValidationError inherits from ConfigError."""
        error = ValidationError("test", value=123, field_name="port")
        assert isinstance(error, ConfigError)

    def test_validation_error_default_code(self) -> None:
        """Test ValidationError default error code."""
        error = ValidationError("test", value=123, field_name="port")
        assert error._default_code() == "VALIDATION_ERROR"

    def test_validation_error_required_parameters(self) -> None:
        """Test ValidationError requires value and field_name."""
        error = ValidationError("Range error", value=0, field_name="port")
        assert error.message == "Range error"

    def test_validation_error_with_constraint(self) -> None:
        """Test ValidationError with constraint parameter."""
        error = ValidationError(
            "Constraint violation",
            value=0,
            field_name="port",
            constraint="must be between 1 and 65535",
        )
        assert error.message == "Constraint violation"

    def test_validation_error_with_all_parameters(self) -> None:
        """Test ValidationError with all parameters."""
        error = ValidationError(
            "Complete validation error",
            value=-1,
            field_name="timeout",
            constraint="must be positive",
            extra_info="negative values not allowed",
        )
        assert error.message == "Complete validation error"


class TestFormatInvalidValueError(FoundationTestCase):
    """Test format_invalid_value_error function."""

    def test_format_with_field_and_value_only(self) -> None:
        """Test basic format with just field name and value."""
        result = format_invalid_value_error("log_level", "INVALID")
        assert result == "Invalid log_level 'INVALID'."

    def test_format_with_valid_options(self) -> None:
        """Test format with valid options list."""
        result = format_invalid_value_error(
            "log_level",
            "INVALID",
            valid_options=["DEBUG", "INFO", "ERROR"],
        )
        assert result == "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO, ERROR"

    def test_format_with_expected_type(self) -> None:
        """Test format with expected type."""
        result = format_invalid_value_error(
            "sample_rate",
            "abc",
            expected_type="float",
        )
        assert result == "Invalid sample_rate 'abc'. Expected: float"

    def test_format_with_additional_info(self) -> None:
        """Test format with additional info."""
        result = format_invalid_value_error(
            "config_file",
            "missing.yaml",
            additional_info="File does not exist",
        )
        assert result == "Invalid config_file 'missing.yaml'. File does not exist"

    def test_format_prefers_valid_options_over_expected_type(self) -> None:
        """Test that valid_options takes precedence over expected_type."""
        result = format_invalid_value_error(
            "level",
            "INVALID",
            expected_type="string",
            valid_options=["DEBUG", "INFO"],
        )
        assert result == "Invalid level 'INVALID'. Valid options: DEBUG, INFO"

    def test_format_with_all_parameters(self) -> None:
        """Test format with all parameters."""
        result = format_invalid_value_error(
            "port",
            "abc",
            expected_type="integer",  # Should be ignored
            valid_options=["80", "443", "8080"],
            additional_info="For HTTP services",
        )
        assert result == "Invalid port 'abc'. Valid options: 80, 443, 8080 For HTTP services"

    def test_format_with_numeric_value(self) -> None:
        """Test format with numeric value."""
        result = format_invalid_value_error("port", 0, expected_type="positive integer")
        assert result == "Invalid port '0'. Expected: positive integer"

    def test_format_with_none_value(self) -> None:
        """Test format with None value."""
        result = format_invalid_value_error("config", None, expected_type="dict")
        assert result == "Invalid config 'None'. Expected: dict"


class TestFormatValidationError(FoundationTestCase):
    """Test format_validation_error function."""

    def test_format_basic_validation_error(self) -> None:
        """Test basic validation error format."""
        result = format_validation_error("port", 0, "must be positive")
        assert result == "Value 0 for port must be positive"

    def test_format_with_additional_info(self) -> None:
        """Test validation error with additional info."""
        result = format_validation_error(
            "sample_rate",
            1.5,
            "must be between 0.0 and 1.0",
            additional_info="received from environment variable",
        )
        assert (
            result
            == "Value 1.5 for sample_rate must be between 0.0 and 1.0(received from environment variable)"
        )

    def test_format_with_string_value(self) -> None:
        """Test validation error with string value."""
        result = format_validation_error(
            "hostname",
            "",
            "cannot be empty",
        )
        assert result == "Value  for hostname cannot be empty"

    def test_format_with_complex_constraint(self) -> None:
        """Test validation error with complex constraint description."""
        result = format_validation_error(
            "timeout",
            -5,
            "must be between 1 and 300 seconds",
        )
        assert result == "Value -5 for timeout must be between 1 and 300 seconds"

    def test_format_with_none_value(self) -> None:
        """Test validation error with None value."""
        result = format_validation_error("required_field", None, "is required")
        assert result == "Value None for required_field is required"

    def test_format_with_boolean_value(self) -> None:
        """Test validation error with boolean value."""
        result = format_validation_error("debug_mode", True, "must be configured explicitly")
        assert result == "Value True for debug_mode must be configured explicitly"


class TestErrorIntegration(FoundationTestCase):
    """Test integration between error classes and formatters."""

    def test_parse_error_with_formatted_message(self) -> None:
        """Test ParseError using formatted message."""
        formatted_msg = format_invalid_value_error(
            "log_level",
            "INVALID",
            valid_options=["DEBUG", "INFO", "ERROR"],
        )

        error = ParseError(
            formatted_msg,
            value="INVALID",
            field_name="log_level",
            valid_options=["DEBUG", "INFO", "ERROR"],
        )

        assert str(error) == "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO, ERROR"
        assert error._default_code() == "PARSE_ERROR"

    def test_validation_error_with_formatted_message(self) -> None:
        """Test ValidationError using formatted message."""
        formatted_msg = format_validation_error(
            "port",
            0,
            "must be between 1 and 65535",
        )

        error = ValidationError(
            formatted_msg,
            value=0,
            field_name="port",
            constraint="must be between 1 and 65535",
        )

        assert str(error) == "Value 0 for port must be between 1 and 65535"
        assert error._default_code() == "VALIDATION_ERROR"

    def test_error_chaining(self) -> None:
        """Test error chaining with cause."""
        original_error = ValueError("Invalid integer")

        parse_error = ParseError(
            "Failed to parse port number",
            value="abc",
            field_name="port",
            expected_type="integer",
        )

        # Test that we can chain errors
        try:
            raise parse_error from original_error
        except ParseError as e:
            assert e.__cause__ == original_error
            assert isinstance(e, ConfigError)


# 🧱🏗️🔚
