#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for SchemaField validation and edge cases."""

from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config.schema import (
    SchemaField,
)
from provide.foundation.errors import ConfigValidationError


class TestSchemaFieldComprehensive(FoundationTestCase):
    """Comprehensive tests for SchemaField validation."""

    def test_validate_required_field_missing(self) -> None:
        """Test validation fails for missing required field."""
        field_obj = SchemaField(name="test_field", required=True)

        with pytest.raises(ConfigValidationError, match="Field is required"):
            field_obj.validate(None)

    def test_validate_required_field_present(self) -> None:
        """Test validation passes for present required field."""
        field_obj = SchemaField(name="test_field", required=True, field_type=str)

        # Should not raise
        field_obj.validate("test_value")

    def test_validate_optional_field_none(self) -> None:
        """Test validation passes for None optional field."""
        field_obj = SchemaField(name="optional_field", required=False)

        # Should not raise
        field_obj.validate(None)

    def test_validate_type_mismatch(self) -> None:
        """Test validation fails for type mismatch."""
        field_obj = SchemaField(name="test_field", field_type=int)

        with pytest.raises(ConfigValidationError, match="Expected type int, got str"):
            field_obj.validate("not_an_int")

    def test_validate_type_correct(self) -> None:
        """Test validation passes for correct type."""
        field_obj = SchemaField(name="test_field", field_type=int)

        # Should not raise
        field_obj.validate(42)

    def test_validate_choices_invalid(self) -> None:
        """Test validation fails for invalid choice."""
        field_obj = SchemaField(name="test_field", choices=["option1", "option2"])

        with pytest.raises(ConfigValidationError, match="Value must be one of"):
            field_obj.validate("invalid_option")

    def test_validate_choices_valid(self) -> None:
        """Test validation passes for valid choice."""
        field_obj = SchemaField(name="test_field", choices=["option1", "option2"])

        # Should not raise
        field_obj.validate("option1")

    def test_validate_min_value_fail(self) -> None:
        """Test validation fails for value below minimum."""
        field_obj = SchemaField(name="test_field", min_value=10)

        with pytest.raises(ConfigValidationError, match="Value must be >= 10"):
            field_obj.validate(5)

    def test_validate_min_value_pass(self) -> None:
        """Test validation passes for value at or above minimum."""
        field_obj = SchemaField(name="test_field", min_value=10)

        # Should not raise
        field_obj.validate(10)
        field_obj.validate(15)

    def test_validate_max_value_fail(self) -> None:
        """Test validation fails for value above maximum."""
        field_obj = SchemaField(name="test_field", max_value=100)

        with pytest.raises(ConfigValidationError, match="Value must be <= 100"):
            field_obj.validate(150)

    def test_validate_max_value_pass(self) -> None:
        """Test validation passes for value at or below maximum."""
        field_obj = SchemaField(name="test_field", max_value=100)

        # Should not raise
        field_obj.validate(100)
        field_obj.validate(50)

    def test_validate_pattern_fail(self) -> None:
        """Test validation fails for pattern mismatch."""
        field_obj = SchemaField(name="test_field", pattern=r"^\d{3}-\d{4}$")

        with pytest.raises(ConfigValidationError, match="Value does not match pattern"):
            field_obj.validate("invalid-format")

    def test_validate_pattern_pass(self) -> None:
        """Test validation passes for pattern match."""
        field_obj = SchemaField(name="test_field", pattern=r"^\d{3}-\d{4}$")

        # Should not raise
        field_obj.validate("123-4567")

    def test_validate_pattern_non_string(self) -> None:
        """Test pattern validation skipped for non-string values."""
        field_obj = SchemaField(name="test_field", pattern=r"^\d+$")

        # Should not raise since 42 is not a string
        field_obj.validate(42)

    def test_validate_sync_validator_pass(self) -> None:
        """Test validation with passing sync validator."""

        def validator(value):
            return value > 0

        field_obj = SchemaField(name="test_field", validator=validator)

        # Should not raise
        field_obj.validate(5)

    def test_validate_sync_validator_fail(self) -> None:
        """Test validation with failing sync validator."""

        def validator(value):
            return value > 0

        field_obj = SchemaField(name="test_field", validator=validator)

        with pytest.raises(ConfigValidationError, match="Custom validation failed"):
            field_obj.validate(-5)

    def test_validate_sync_validator_pass_2(self) -> None:
        """Test validation with passing sync validator (additional test)."""

        def sync_validator(value):
            return value > 0

        field_obj = SchemaField(name="test_field", validator=sync_validator)

        # Should not raise
        field_obj.validate(5)

    def test_validate_sync_validator_fail_2(self) -> None:
        """Test validation with failing sync validator (additional test)."""

        def sync_validator(value):
            return value > 0

        field_obj = SchemaField(name="test_field", validator=sync_validator)

        with pytest.raises(ConfigValidationError, match="Custom validation failed"):
            field_obj.validate(-5)

    def test_validate_validator_raises_config_error(self) -> None:
        """Test validator that raises ConfigValidationError directly."""

        def validator(value) -> bool:
            if value < 0:
                raise ConfigValidationError(
                    "Must be positive",
                    field="test_field",
                    value=value,
                )
            return True

        field_obj = SchemaField(name="test_field", validator=validator)

        with pytest.raises(ConfigValidationError, match="Must be positive"):
            field_obj.validate(-1)

    def test_validate_validator_raises_generic_error(self) -> None:
        """Test validator that raises generic exception."""

        def validator(value) -> Never:
            raise ValueError("Generic error")

        field_obj = SchemaField(name="test_field", validator=validator)

        with pytest.raises(
            ConfigValidationError,
            match="Validation error: Generic error",
        ):
            field_obj.validate(5)

    def test_validate_lambda_validator(self) -> None:
        """Test validation with lambda validator."""

        def lambda_validator(x):
            return x > 0

        field_obj = SchemaField(name="test_field", validator=lambda_validator)

        # Should not raise
        field_obj.validate(5)

    def test_validate_all_constraints_combined(self) -> None:
        """Test validation with all constraints combined."""

        def custom_validator(value):
            return len(value) > 5

        field_obj = SchemaField(
            name="complex_field",
            field_type=str,
            required=True,
            choices=[
                "valid_option",
                "another_valid_option",
                "short",
                "UPPER_CASE",
            ],  # Add values to test different constraints
            pattern=r"^[a-z_]+$",
            validator=custom_validator,
        )

        # Should not raise
        field_obj.validate("valid_option")

        # Test failure cases
        with pytest.raises(ConfigValidationError, match="Field is required"):
            field_obj.validate(None)

        with pytest.raises(ConfigValidationError, match="Expected type str"):
            field_obj.validate(42)

        with pytest.raises(ConfigValidationError, match="Value must be one of"):
            field_obj.validate("invalid_choice")

        with pytest.raises(ConfigValidationError, match="Value does not match pattern"):
            field_obj.validate(
                "UPPER_CASE",
            )  # In choices, but fails pattern (uppercase)

        with pytest.raises(ConfigValidationError, match="Custom validation failed"):
            field_obj.validate(
                "short",
            )  # In choices, matches pattern, but fails custom validator (len <= 5)


class TestSchemaFieldEdgeCases(FoundationTestCase):
    """Test edge cases and corner cases for SchemaField."""

    def test_validate_none_with_type_check(self) -> None:
        """Test that None values skip type checking."""
        field_obj = SchemaField(name="test", field_type=int, required=False)

        # Should not raise even though None is not an int
        field_obj.validate(None)

    def test_validate_comparison_operators_edge_cases(self) -> None:
        """Test min/max validation with various types."""
        # String comparison
        field_obj = SchemaField(name="test", field_type=str, min_value="b", max_value="y")

        field_obj.validate("m")  # Should pass

        with pytest.raises(ConfigValidationError):
            field_obj.validate("a")  # Below min

        with pytest.raises(ConfigValidationError):
            field_obj.validate("z")  # Above max

    def test_validate_sync_validator_simple(self) -> None:
        """Test simple sync validator functionality."""

        def sync_validator(value) -> bool:
            return True

        field_obj = SchemaField(name="test", validator=sync_validator)

        # Should handle validator properly
        field_obj.validate(42)

    def test_validate_complex_nested_validation(self) -> None:
        """Test validation with complex nested constraints."""

        def complex_validator(value):
            # Multi-step validation
            if not isinstance(value, str):
                return False
            if len(value) < 3:
                return False
            return value.isalnum()

        field_obj = SchemaField(
            name="complex",
            field_type=str,
            required=True,
            min_value="aaa",  # Alphabetically
            max_value="zzz",
            pattern=r"^[a-z0-9]+$",
            validator=complex_validator,
        )

        field_obj.validate("abc123")  # Should pass all validations

        # Test each validation constraint
        with pytest.raises(ConfigValidationError, match="Field is required"):
            field_obj.validate(None)

        with pytest.raises(ConfigValidationError, match="Expected type str"):
            field_obj.validate(123)

        with pytest.raises(ConfigValidationError, match="Value must be >= aaa"):
            field_obj.validate("aa")  # Below min alphabetically


# 🧱🏗️🔚
