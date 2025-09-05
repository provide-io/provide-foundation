"""
Configuration field validators.

Provides validation functions for common configuration field patterns
including RPC plugin-specific validators.
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


def validate_transport_list(instance, attribute, value):
    """
    Validate transport list for RPC plugin.
    
    Valid combinations: ["unix"], ["tcp"], ["unix", "tcp"], ["tcp", "unix"]
    """
    valid_transports = {"unix", "tcp"}
    valid_combinations = [
        ["unix"], 
        ["tcp"], 
        ["unix", "tcp"], 
        ["tcp", "unix"]
    ]
    
    if not isinstance(value, list):
        raise ValidationError(
            f"Transport list must be a list, got {type(value).__name__}"
        )
    
    # Check individual transports are valid
    for transport in value:
        if transport not in valid_transports:
            raise ValidationError(
                f"Invalid transport '{transport}'. Must be one of: {valid_transports}"
            )
    
    # Check combination is valid
    if value not in valid_combinations:
        raise ValidationError(
            f"Invalid transport combination {value}. "
            f"Must be one of: {valid_combinations}"
        )


def validate_protocol_version(instance, attribute, value):
    """
    Validate protocol version for RPC plugin.
    
    Must be an integer between 1 and 7 (inclusive).
    """
    if not isinstance(value, int):
        raise ValidationError(
            f"Protocol version must be an integer, got {type(value).__name__}"
        )
    
    if not (1 <= value <= 7):
        raise ValidationError(
            f"Protocol version must be between 1 and 7, got {value}"
        )


def validate_protocol_version_list(instance, attribute, value):
    """
    Validate protocol version list for RPC plugin.
    
    Each version must be an integer between 1 and 7 (inclusive).
    """
    if not isinstance(value, list):
        raise ValidationError(
            f"Protocol version list must be a list, got {type(value).__name__}"
        )
    
    for version in value:
        if not isinstance(version, int):
            raise ValidationError(
                f"Protocol version must be an integer, got {type(version).__name__} for {version}"
            )
        
        if not (1 <= version <= 7):
            raise ValidationError(
                f"Protocol version must be between 1 and 7, got {version}"
            )


def validate_timeout(min_value: float = 0.0, max_value: float = 3600.0) -> Callable[[Any, Any, Any], None]:
    """
    Create a validator for timeout values.
    
    Args:
        min_value: Minimum allowed timeout value
        max_value: Maximum allowed timeout value
    
    Returns:
        Validator function
    """
    def validator(instance, attribute, value):
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Timeout must be a number, got {type(value).__name__}"
            )
        
        if not (min_value <= value <= max_value):
            raise ValidationError(
                f"Timeout must be between {min_value} and {max_value}, got {value}"
            )
    return validator


def validate_rate_limit(instance, attribute, value):
    """
    Validate rate limit value.
    
    Must be a positive number.
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Rate limit must be a number, got {type(value).__name__}"
        )
    
    if value <= 0:
        raise ValidationError(
            f"Rate limit must be positive, got {value}"
        )


def validate_log_level(instance, attribute, value):
    """
    Validate logging level.
    
    Must be one of the standard logging levels.
    """
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if value not in valid_levels:
        raise ValidationError(
            f"Invalid log level '{value}'. Must be one of: {valid_levels}"
        )


def validate_retry_count(instance, attribute, value):
    """
    Validate retry count value.
    
    Must be a non-negative integer.
    """
    if not isinstance(value, int):
        raise ValidationError(
            f"Retry count must be an integer, got {type(value).__name__}"
        )
    
    if value < 0:
        raise ValidationError(
            f"Retry count must be non-negative, got {value}"
        )


def validate_backoff_time(instance, attribute, value):
    """
    Validate backoff time value.
    
    Must be a positive number.
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Backoff time must be a number, got {type(value).__name__}"
        )
    
    if value <= 0:
        raise ValidationError(
            f"Backoff time must be positive, got {value}"
        )