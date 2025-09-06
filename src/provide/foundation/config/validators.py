"""
Configuration field validators.

Provides common validation functions for configuration fields.
Domain-specific validators should be implemented in their respective packages.
"""

from collections.abc import Callable
from typing import Any

from provide.foundation.errors.config import ValidationError


def validate_choice(choices: list[Any]) -> Callable[[Any, Any, Any], None]:
    """
    Create a validator that ensures the value is one of the allowed choices.

    Args:
        choices: List of allowed values

    Returns:
        Validator function
    """

    def validator(instance, attribute, value):
        if value not in choices:
            raise ValidationError(
                f"Invalid value '{value}' for {attribute.name}. "
                f"Must be one of: {choices}"
            )

    return validator


def validate_range(
    min_value: float, max_value: float
) -> Callable[[Any, Any, Any], None]:
    """
    Create a validator that ensures the value is within a numeric range.

    Args:
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)

    Returns:
        Validator function
    """

    def validator(instance, attribute, value):
        if not isinstance(value, (int, float)):
            raise ValidationError(f"Value must be a number, got {type(value).__name__}")

        if not (min_value <= value <= max_value):
            raise ValidationError(
                f"Value must be between {min_value} and {max_value}, got {value}"
            )

    return validator


def validate_positive(instance, attribute, value):
    """
    Validate that a numeric value is positive.
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(f"Value must be a number, got {type(value).__name__}")

    if value <= 0:
        raise ValidationError(f"Value must be positive, got {value}")


def validate_non_negative(instance, attribute, value):
    """
    Validate that a numeric value is non-negative.
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(f"Value must be a number, got {type(value).__name__}")

    if value < 0:
        raise ValidationError(f"Value must be non-negative, got {value}")
