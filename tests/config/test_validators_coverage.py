#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests for config validators to improve code coverage."""

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock
import pytest

from provide.foundation.config.validators import (
    validate_choice,
    validate_non_negative,
    validate_positive,
    validate_range,
)
from provide.foundation.errors.config import ValidationError


class TestValidatorsCoverage(FoundationTestCase):
    """Test config validators for improved coverage."""

    def test_validate_choice_valid_value(self) -> None:
        """Test validate_choice with valid value."""
        choices = ["a", "b", "c"]
        validator = validate_choice(choices)

        # Mock attrs-style arguments
        instance = Mock()
        attribute = Mock()
        attribute.name = "test_field"

        # Should not raise for valid choice
        validator(instance, attribute, "a")
        validator(instance, attribute, "b")
        validator(instance, attribute, "c")

    def test_validate_choice_invalid_value(self) -> None:
        """Test validate_choice with invalid value raises ValidationError."""
        choices = ["a", "b", "c"]
        validator = validate_choice(choices)

        instance = Mock()
        attribute = Mock()
        attribute.name = "test_field"

        with pytest.raises(ValidationError) as exc_info:
            validator(instance, attribute, "invalid")

        assert "Invalid value 'invalid' for test_field" in str(exc_info.value)
        assert "Must be one of: ['a', 'b', 'c']" in str(exc_info.value)

    def test_validate_choice_with_mixed_types(self) -> None:
        """Test validate_choice with mixed data types."""
        choices = [1, "string", True, None]
        validator = validate_choice(choices)

        instance = Mock()
        attribute = Mock()
        attribute.name = "mixed_field"

        # All these should be valid
        validator(instance, attribute, 1)
        validator(instance, attribute, "string")
        validator(instance, attribute, True)
        validator(instance, attribute, None)

        # This should fail
        with pytest.raises(ValidationError):
            validator(instance, attribute, "not_in_choices")

    def test_validate_range_valid_values(self) -> None:
        """Test validate_range with valid values."""
        validator = validate_range(0.0, 10.0)

        instance = Mock()
        attribute = Mock()
        attribute.name = "range_field"

        # Test boundary values and middle values
        validator(instance, attribute, 0.0)  # min boundary
        validator(instance, attribute, 10.0)  # max boundary
        validator(instance, attribute, 5.0)  # middle value
        validator(instance, attribute, 0)  # integer min
        validator(instance, attribute, 10)  # integer max

    def test_validate_range_invalid_type(self) -> None:
        """Test validate_range with non-numeric type."""
        validator = validate_range(0.0, 10.0)

        instance = Mock()
        attribute = Mock()
        attribute.name = "range_field"

        with pytest.raises(ValidationError) as exc_info:
            validator(instance, attribute, "not_a_number")

        assert "Value must be a number, got str" in str(exc_info.value)

    def test_validate_range_out_of_bounds(self) -> None:
        """Test validate_range with out-of-bounds values."""
        validator = validate_range(1.0, 5.0)

        instance = Mock()
        attribute = Mock()
        attribute.name = "range_field"

        # Test below minimum
        with pytest.raises(ValidationError) as exc_info:
            validator(instance, attribute, 0.5)
        assert "Value must be between 1.0 and 5.0, got 0.5" in str(exc_info.value)

        # Test above maximum
        with pytest.raises(ValidationError) as exc_info:
            validator(instance, attribute, 5.5)
        assert "Value must be between 1.0 and 5.0, got 5.5" in str(exc_info.value)

    def test_validate_range_negative_range(self) -> None:
        """Test validate_range with negative values."""
        validator = validate_range(-10.0, -1.0)

        instance = Mock()
        attribute = Mock()
        attribute.name = "negative_range"

        # Valid negative values
        validator(instance, attribute, -5.0)
        validator(instance, attribute, -1.0)
        validator(instance, attribute, -10.0)

        # Invalid values
        with pytest.raises(ValidationError):
            validator(instance, attribute, 0)

    def test_validate_positive_valid_values(self) -> None:
        """Test validate_positive with valid positive values."""
        instance = Mock()
        attribute = Mock()
        attribute.name = "positive_field"

        # Valid positive values
        validate_positive(instance, attribute, 1)
        validate_positive(instance, attribute, 1.5)
        validate_positive(instance, attribute, 0.001)
        validate_positive(instance, attribute, 1000)

    def test_validate_positive_invalid_type(self) -> None:
        """Test validate_positive with non-numeric type."""
        instance = Mock()
        attribute = Mock()
        attribute.name = "positive_field"

        with pytest.raises(ValidationError) as exc_info:
            validate_positive(instance, attribute, "not_a_number")

        assert "Value must be a number, got str" in str(exc_info.value)

    def test_validate_positive_zero_and_negative(self) -> None:
        """Test validate_positive with zero and negative values."""
        instance = Mock()
        attribute = Mock()
        attribute.name = "positive_field"

        # Zero should fail
        with pytest.raises(ValidationError) as exc_info:
            validate_positive(instance, attribute, 0)
        assert "Value 0 for positive_field must be positive" in str(exc_info.value)

        # Negative should fail
        with pytest.raises(ValidationError) as exc_info:
            validate_positive(instance, attribute, -1)
        assert "Value -1 for positive_field must be positive" in str(exc_info.value)

    def test_validate_non_negative_valid_values(self) -> None:
        """Test validate_non_negative with valid non-negative values."""
        instance = Mock()
        attribute = Mock()
        attribute.name = "non_negative_field"

        # Valid non-negative values
        validate_non_negative(instance, attribute, 0)  # zero is valid
        validate_non_negative(instance, attribute, 0.0)
        validate_non_negative(instance, attribute, 1)
        validate_non_negative(instance, attribute, 1.5)
        validate_non_negative(instance, attribute, 1000)

    def test_validate_non_negative_invalid_type(self) -> None:
        """Test validate_non_negative with non-numeric type."""
        instance = Mock()
        attribute = Mock()
        attribute.name = "non_negative_field"

        with pytest.raises(ValidationError) as exc_info:
            validate_non_negative(instance, attribute, "not_a_number")

        assert "Value must be a number, got str" in str(exc_info.value)

    def test_validate_non_negative_negative_values(self) -> None:
        """Test validate_non_negative with negative values."""
        instance = Mock()
        attribute = Mock()
        attribute.name = "non_negative_field"

        # Negative values should fail
        with pytest.raises(ValidationError) as exc_info:
            validate_non_negative(instance, attribute, -1)
        assert "Value -1 for non_negative_field must be non-negative" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            validate_non_negative(instance, attribute, -0.5)
        assert "Value -0.5 for non_negative_field must be non-negative" in str(exc_info.value)

    def test_validators_with_different_numeric_types(self) -> None:
        """Test validators work with different numeric types."""
        instance = Mock()
        attribute = Mock()
        attribute.name = "numeric_field"

        # Test with different numeric types
        validate_positive(instance, attribute, 5)
        validate_positive(instance, attribute, 5.0)

        validate_non_negative(instance, attribute, 0)
        validate_non_negative(instance, attribute, 0.0)

        range_validator = validate_range(0, 10)
        range_validator(instance, attribute, 5)
        range_validator(instance, attribute, 5.5)


# 🧱🏗️🔚
