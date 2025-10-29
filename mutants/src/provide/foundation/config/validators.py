# provide/foundation/config/validators.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from provide.foundation.parsers.errors import (
    _VALID_LOG_LEVEL_TUPLE,
    _VALID_OVERFLOW_POLICY_TUPLE,
    _format_invalid_value_error,
    _format_validation_error,
)

"""Validation functions for configuration field values.

These validators are used with the attrs `validator` parameter to validate
field values after conversion. They provide consistent error messages and
follow attrs validator conventions.
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_validate_log_level__mutmut_orig(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )


def x_validate_log_level__mutmut_1(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )


def x_validate_log_level__mutmut_2(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            None,
        )


def x_validate_log_level__mutmut_3(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                None,
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )


def x_validate_log_level__mutmut_4(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                None,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )


def x_validate_log_level__mutmut_5(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=None,
            ),
        )


def x_validate_log_level__mutmut_6(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )


def x_validate_log_level__mutmut_7(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )


def x_validate_log_level__mutmut_8(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
            ),
        )


def x_validate_log_level__mutmut_9(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=list(None),
            ),
        )


x_validate_log_level__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_log_level__mutmut_1": x_validate_log_level__mutmut_1,
    "x_validate_log_level__mutmut_2": x_validate_log_level__mutmut_2,
    "x_validate_log_level__mutmut_3": x_validate_log_level__mutmut_3,
    "x_validate_log_level__mutmut_4": x_validate_log_level__mutmut_4,
    "x_validate_log_level__mutmut_5": x_validate_log_level__mutmut_5,
    "x_validate_log_level__mutmut_6": x_validate_log_level__mutmut_6,
    "x_validate_log_level__mutmut_7": x_validate_log_level__mutmut_7,
    "x_validate_log_level__mutmut_8": x_validate_log_level__mutmut_8,
    "x_validate_log_level__mutmut_9": x_validate_log_level__mutmut_9,
}


def validate_log_level(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_log_level__mutmut_orig, x_validate_log_level__mutmut_mutants, args, kwargs
    )
    return result


validate_log_level.__signature__ = _mutmut_signature(x_validate_log_level__mutmut_orig)
x_validate_log_level__mutmut_orig.__name__ = "x_validate_log_level"


def x_validate_sample_rate__mutmut_orig(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_1(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_2(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_3(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 < value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_4(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value < 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_5(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 2.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_6(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            None,
        )


def x_validate_sample_rate__mutmut_7(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(None, value, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_8(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, None, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_9(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, None),
        )


def x_validate_sample_rate__mutmut_10(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(value, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_11(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, "must be between 0.0 and 1.0"),
        )


def x_validate_sample_rate__mutmut_12(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(
                attribute.name,
                value,
            ),
        )


def x_validate_sample_rate__mutmut_13(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "XXmust be between 0.0 and 1.0XX"),
        )


def x_validate_sample_rate__mutmut_14(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "MUST BE BETWEEN 0.0 AND 1.0"),
        )


x_validate_sample_rate__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_sample_rate__mutmut_1": x_validate_sample_rate__mutmut_1,
    "x_validate_sample_rate__mutmut_2": x_validate_sample_rate__mutmut_2,
    "x_validate_sample_rate__mutmut_3": x_validate_sample_rate__mutmut_3,
    "x_validate_sample_rate__mutmut_4": x_validate_sample_rate__mutmut_4,
    "x_validate_sample_rate__mutmut_5": x_validate_sample_rate__mutmut_5,
    "x_validate_sample_rate__mutmut_6": x_validate_sample_rate__mutmut_6,
    "x_validate_sample_rate__mutmut_7": x_validate_sample_rate__mutmut_7,
    "x_validate_sample_rate__mutmut_8": x_validate_sample_rate__mutmut_8,
    "x_validate_sample_rate__mutmut_9": x_validate_sample_rate__mutmut_9,
    "x_validate_sample_rate__mutmut_10": x_validate_sample_rate__mutmut_10,
    "x_validate_sample_rate__mutmut_11": x_validate_sample_rate__mutmut_11,
    "x_validate_sample_rate__mutmut_12": x_validate_sample_rate__mutmut_12,
    "x_validate_sample_rate__mutmut_13": x_validate_sample_rate__mutmut_13,
    "x_validate_sample_rate__mutmut_14": x_validate_sample_rate__mutmut_14,
}


def validate_sample_rate(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_sample_rate__mutmut_orig, x_validate_sample_rate__mutmut_mutants, args, kwargs
    )
    return result


validate_sample_rate.__signature__ = _mutmut_signature(x_validate_sample_rate__mutmut_orig)
x_validate_sample_rate__mutmut_orig.__name__ = "x_validate_sample_rate"


def x_validate_port__mutmut_orig(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_1(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_2(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 2 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_3(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 < value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_4(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value < 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_5(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65536:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_6(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            None,
        )


def x_validate_port__mutmut_7(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(None, value, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_8(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, None, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_9(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, None),
        )


def x_validate_port__mutmut_10(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(value, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_11(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, "must be between 1 and 65535"),
        )


def x_validate_port__mutmut_12(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(
                attribute.name,
                value,
            ),
        )


def x_validate_port__mutmut_13(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "XXmust be between 1 and 65535XX"),
        )


def x_validate_port__mutmut_14(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "MUST BE BETWEEN 1 AND 65535"),
        )


x_validate_port__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_port__mutmut_1": x_validate_port__mutmut_1,
    "x_validate_port__mutmut_2": x_validate_port__mutmut_2,
    "x_validate_port__mutmut_3": x_validate_port__mutmut_3,
    "x_validate_port__mutmut_4": x_validate_port__mutmut_4,
    "x_validate_port__mutmut_5": x_validate_port__mutmut_5,
    "x_validate_port__mutmut_6": x_validate_port__mutmut_6,
    "x_validate_port__mutmut_7": x_validate_port__mutmut_7,
    "x_validate_port__mutmut_8": x_validate_port__mutmut_8,
    "x_validate_port__mutmut_9": x_validate_port__mutmut_9,
    "x_validate_port__mutmut_10": x_validate_port__mutmut_10,
    "x_validate_port__mutmut_11": x_validate_port__mutmut_11,
    "x_validate_port__mutmut_12": x_validate_port__mutmut_12,
    "x_validate_port__mutmut_13": x_validate_port__mutmut_13,
    "x_validate_port__mutmut_14": x_validate_port__mutmut_14,
}


def validate_port(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_port__mutmut_orig, x_validate_port__mutmut_mutants, args, kwargs)
    return result


validate_port.__signature__ = _mutmut_signature(x_validate_port__mutmut_orig)
x_validate_port__mutmut_orig.__name__ = "x_validate_port"


def x_validate_positive__mutmut_orig(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be positive"),
        )


def x_validate_positive__mutmut_1(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be positive"),
        )


def x_validate_positive__mutmut_2(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            None,
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be positive"),
        )


def x_validate_positive__mutmut_3(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(None).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be positive"),
        )


def x_validate_positive__mutmut_4(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be positive"),
        )


def x_validate_positive__mutmut_5(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 1:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be positive"),
        )


def x_validate_positive__mutmut_6(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            None,
        )


def x_validate_positive__mutmut_7(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(None, value, "must be positive"),
        )


def x_validate_positive__mutmut_8(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, None, "must be positive"),
        )


def x_validate_positive__mutmut_9(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, None),
        )


def x_validate_positive__mutmut_10(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(value, "must be positive"),
        )


def x_validate_positive__mutmut_11(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, "must be positive"),
        )


def x_validate_positive__mutmut_12(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(
                attribute.name,
                value,
            ),
        )


def x_validate_positive__mutmut_13(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "XXmust be positiveXX"),
        )


def x_validate_positive__mutmut_14(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "MUST BE POSITIVE"),
        )


x_validate_positive__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_positive__mutmut_1": x_validate_positive__mutmut_1,
    "x_validate_positive__mutmut_2": x_validate_positive__mutmut_2,
    "x_validate_positive__mutmut_3": x_validate_positive__mutmut_3,
    "x_validate_positive__mutmut_4": x_validate_positive__mutmut_4,
    "x_validate_positive__mutmut_5": x_validate_positive__mutmut_5,
    "x_validate_positive__mutmut_6": x_validate_positive__mutmut_6,
    "x_validate_positive__mutmut_7": x_validate_positive__mutmut_7,
    "x_validate_positive__mutmut_8": x_validate_positive__mutmut_8,
    "x_validate_positive__mutmut_9": x_validate_positive__mutmut_9,
    "x_validate_positive__mutmut_10": x_validate_positive__mutmut_10,
    "x_validate_positive__mutmut_11": x_validate_positive__mutmut_11,
    "x_validate_positive__mutmut_12": x_validate_positive__mutmut_12,
    "x_validate_positive__mutmut_13": x_validate_positive__mutmut_13,
    "x_validate_positive__mutmut_14": x_validate_positive__mutmut_14,
}


def validate_positive(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_positive__mutmut_orig, x_validate_positive__mutmut_mutants, args, kwargs
    )
    return result


validate_positive.__signature__ = _mutmut_signature(x_validate_positive__mutmut_orig)
x_validate_positive__mutmut_orig.__name__ = "x_validate_positive"


def x_validate_non_negative__mutmut_orig(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_1(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_2(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            None,
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_3(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(None).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_4(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_5(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 1:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_6(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            None,
        )


def x_validate_non_negative__mutmut_7(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(None, value, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_8(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, None, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_9(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, None),
        )


def x_validate_non_negative__mutmut_10(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(value, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_11(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, "must be non-negative"),
        )


def x_validate_non_negative__mutmut_12(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(
                attribute.name,
                value,
            ),
        )


def x_validate_non_negative__mutmut_13(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "XXmust be non-negativeXX"),
        )


def x_validate_non_negative__mutmut_14(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "MUST BE NON-NEGATIVE"),
        )


x_validate_non_negative__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_non_negative__mutmut_1": x_validate_non_negative__mutmut_1,
    "x_validate_non_negative__mutmut_2": x_validate_non_negative__mutmut_2,
    "x_validate_non_negative__mutmut_3": x_validate_non_negative__mutmut_3,
    "x_validate_non_negative__mutmut_4": x_validate_non_negative__mutmut_4,
    "x_validate_non_negative__mutmut_5": x_validate_non_negative__mutmut_5,
    "x_validate_non_negative__mutmut_6": x_validate_non_negative__mutmut_6,
    "x_validate_non_negative__mutmut_7": x_validate_non_negative__mutmut_7,
    "x_validate_non_negative__mutmut_8": x_validate_non_negative__mutmut_8,
    "x_validate_non_negative__mutmut_9": x_validate_non_negative__mutmut_9,
    "x_validate_non_negative__mutmut_10": x_validate_non_negative__mutmut_10,
    "x_validate_non_negative__mutmut_11": x_validate_non_negative__mutmut_11,
    "x_validate_non_negative__mutmut_12": x_validate_non_negative__mutmut_12,
    "x_validate_non_negative__mutmut_13": x_validate_non_negative__mutmut_13,
    "x_validate_non_negative__mutmut_14": x_validate_non_negative__mutmut_14,
}


def validate_non_negative(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_non_negative__mutmut_orig, x_validate_non_negative__mutmut_mutants, args, kwargs
    )
    return result


validate_non_negative.__signature__ = _mutmut_signature(x_validate_non_negative__mutmut_orig)
x_validate_non_negative__mutmut_orig.__name__ = "x_validate_non_negative"


def x_validate_overflow_policy__mutmut_orig(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=list(_VALID_OVERFLOW_POLICY_TUPLE),
            ),
        )


def x_validate_overflow_policy__mutmut_1(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=list(_VALID_OVERFLOW_POLICY_TUPLE),
            ),
        )


def x_validate_overflow_policy__mutmut_2(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            None,
        )


def x_validate_overflow_policy__mutmut_3(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                None,
                value,
                valid_options=list(_VALID_OVERFLOW_POLICY_TUPLE),
            ),
        )


def x_validate_overflow_policy__mutmut_4(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                None,
                valid_options=list(_VALID_OVERFLOW_POLICY_TUPLE),
            ),
        )


def x_validate_overflow_policy__mutmut_5(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=None,
            ),
        )


def x_validate_overflow_policy__mutmut_6(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                value,
                valid_options=list(_VALID_OVERFLOW_POLICY_TUPLE),
            ),
        )


def x_validate_overflow_policy__mutmut_7(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                valid_options=list(_VALID_OVERFLOW_POLICY_TUPLE),
            ),
        )


def x_validate_overflow_policy__mutmut_8(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
            ),
        )


def x_validate_overflow_policy__mutmut_9(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=list(None),
            ),
        )


x_validate_overflow_policy__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_overflow_policy__mutmut_1": x_validate_overflow_policy__mutmut_1,
    "x_validate_overflow_policy__mutmut_2": x_validate_overflow_policy__mutmut_2,
    "x_validate_overflow_policy__mutmut_3": x_validate_overflow_policy__mutmut_3,
    "x_validate_overflow_policy__mutmut_4": x_validate_overflow_policy__mutmut_4,
    "x_validate_overflow_policy__mutmut_5": x_validate_overflow_policy__mutmut_5,
    "x_validate_overflow_policy__mutmut_6": x_validate_overflow_policy__mutmut_6,
    "x_validate_overflow_policy__mutmut_7": x_validate_overflow_policy__mutmut_7,
    "x_validate_overflow_policy__mutmut_8": x_validate_overflow_policy__mutmut_8,
    "x_validate_overflow_policy__mutmut_9": x_validate_overflow_policy__mutmut_9,
}


def validate_overflow_policy(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_overflow_policy__mutmut_orig, x_validate_overflow_policy__mutmut_mutants, args, kwargs
    )
    return result


validate_overflow_policy.__signature__ = _mutmut_signature(x_validate_overflow_policy__mutmut_orig)
x_validate_overflow_policy__mutmut_orig.__name__ = "x_validate_overflow_policy"


def x_validate_choice__mutmut_orig(choices: list[Any]) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is one of the given choices.

    Args:
        choices: List of valid choices

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        if value not in choices:
            # Import ValidationError locally to avoid circular imports
            from provide.foundation.errors.config import ValidationError

            raise ValidationError(
                f"Invalid value '{value}' for {attribute.name}. Must be one of: {choices!r}",
            )

    return validator


def x_validate_choice__mutmut_1(choices: list[Any]) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is one of the given choices.

    Args:
        choices: List of valid choices

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        if value in choices:
            # Import ValidationError locally to avoid circular imports
            from provide.foundation.errors.config import ValidationError

            raise ValidationError(
                f"Invalid value '{value}' for {attribute.name}. Must be one of: {choices!r}",
            )

    return validator


def x_validate_choice__mutmut_2(choices: list[Any]) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is one of the given choices.

    Args:
        choices: List of valid choices

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        if value not in choices:
            # Import ValidationError locally to avoid circular imports
            from provide.foundation.errors.config import ValidationError

            raise ValidationError(
                None,
            )

    return validator


x_validate_choice__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_choice__mutmut_1": x_validate_choice__mutmut_1,
    "x_validate_choice__mutmut_2": x_validate_choice__mutmut_2,
}


def validate_choice(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_choice__mutmut_orig, x_validate_choice__mutmut_mutants, args, kwargs
    )
    return result


validate_choice.__signature__ = _mutmut_signature(x_validate_choice__mutmut_orig)
x_validate_choice__mutmut_orig.__name__ = "x_validate_choice"


def x_validate_range__mutmut_orig(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Value must be a number, got {type(value).__name__}",
            )

        if not (min_val <= value <= max_val):
            raise ValidationError(
                f"Value must be between {min_val} and {max_val}, got {value}",
            )

    return validator


def x_validate_range__mutmut_1(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if isinstance(value, (int, float)):
            raise ValidationError(
                f"Value must be a number, got {type(value).__name__}",
            )

        if not (min_val <= value <= max_val):
            raise ValidationError(
                f"Value must be between {min_val} and {max_val}, got {value}",
            )

    return validator


def x_validate_range__mutmut_2(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                None,
            )

        if not (min_val <= value <= max_val):
            raise ValidationError(
                f"Value must be between {min_val} and {max_val}, got {value}",
            )

    return validator


def x_validate_range__mutmut_3(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Value must be a number, got {type(None).__name__}",
            )

        if not (min_val <= value <= max_val):
            raise ValidationError(
                f"Value must be between {min_val} and {max_val}, got {value}",
            )

    return validator


def x_validate_range__mutmut_4(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Value must be a number, got {type(value).__name__}",
            )

        if min_val <= value <= max_val:
            raise ValidationError(
                f"Value must be between {min_val} and {max_val}, got {value}",
            )

    return validator


def x_validate_range__mutmut_5(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Value must be a number, got {type(value).__name__}",
            )

        if not (min_val < value <= max_val):
            raise ValidationError(
                f"Value must be between {min_val} and {max_val}, got {value}",
            )

    return validator


def x_validate_range__mutmut_6(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Value must be a number, got {type(value).__name__}",
            )

        if not (min_val <= value < max_val):
            raise ValidationError(
                f"Value must be between {min_val} and {max_val}, got {value}",
            )

    return validator


def x_validate_range__mutmut_7(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Value must be a number, got {type(value).__name__}",
            )

        if not (min_val <= value <= max_val):
            raise ValidationError(
                None,
            )

    return validator


x_validate_range__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_range__mutmut_1": x_validate_range__mutmut_1,
    "x_validate_range__mutmut_2": x_validate_range__mutmut_2,
    "x_validate_range__mutmut_3": x_validate_range__mutmut_3,
    "x_validate_range__mutmut_4": x_validate_range__mutmut_4,
    "x_validate_range__mutmut_5": x_validate_range__mutmut_5,
    "x_validate_range__mutmut_6": x_validate_range__mutmut_6,
    "x_validate_range__mutmut_7": x_validate_range__mutmut_7,
}


def validate_range(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_range__mutmut_orig, x_validate_range__mutmut_mutants, args, kwargs)
    return result


validate_range.__signature__ = _mutmut_signature(x_validate_range__mutmut_orig)
x_validate_range__mutmut_orig.__name__ = "x_validate_range"


__all__ = [
    "validate_choice",
    "validate_log_level",
    "validate_non_negative",
    "validate_overflow_policy",
    "validate_port",
    "validate_positive",
    "validate_range",
    "validate_sample_rate",
]


# <3 🧱🤝⚙️🪄
