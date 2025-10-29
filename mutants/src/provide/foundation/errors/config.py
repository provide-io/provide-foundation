# provide/foundation/errors/config.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Configuration-related exceptions."""
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

    def xǁConfigurationErrorǁ__init____mutmut_orig(
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

    def xǁConfigurationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault("context", {})["config.key"] = None
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault(None, {})["config.key"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault("context", None)["config.key"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault({})["config.key"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault(
                "context",
            )["config.key"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault("XXcontextXX", {})["config.key"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault("CONTEXT", {})["config.key"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault("context", {})["XXconfig.keyXX"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_key:
            kwargs.setdefault("context", {})["CONFIG.KEY"] = config_key
        if config_source:
            kwargs.setdefault("context", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_10(
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
            kwargs.setdefault("context", {})["config.source"] = None
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_11(
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
            kwargs.setdefault(None, {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_12(
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
            kwargs.setdefault("context", None)["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_13(
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
            kwargs.setdefault({})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_14(
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
            kwargs.setdefault(
                "context",
            )["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_15(
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
            kwargs.setdefault("XXcontextXX", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_16(
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
            kwargs.setdefault("CONTEXT", {})["config.source"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_17(
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
            kwargs.setdefault("context", {})["XXconfig.sourceXX"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_18(
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
            kwargs.setdefault("context", {})["CONFIG.SOURCE"] = config_source
        super().__init__(message, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_19(
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
        super().__init__(None, **kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_20(
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
        super().__init__(**kwargs)

    def xǁConfigurationErrorǁ__init____mutmut_21(
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
        super().__init__(
            message,
        )

    xǁConfigurationErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigurationErrorǁ__init____mutmut_1": xǁConfigurationErrorǁ__init____mutmut_1,
        "xǁConfigurationErrorǁ__init____mutmut_2": xǁConfigurationErrorǁ__init____mutmut_2,
        "xǁConfigurationErrorǁ__init____mutmut_3": xǁConfigurationErrorǁ__init____mutmut_3,
        "xǁConfigurationErrorǁ__init____mutmut_4": xǁConfigurationErrorǁ__init____mutmut_4,
        "xǁConfigurationErrorǁ__init____mutmut_5": xǁConfigurationErrorǁ__init____mutmut_5,
        "xǁConfigurationErrorǁ__init____mutmut_6": xǁConfigurationErrorǁ__init____mutmut_6,
        "xǁConfigurationErrorǁ__init____mutmut_7": xǁConfigurationErrorǁ__init____mutmut_7,
        "xǁConfigurationErrorǁ__init____mutmut_8": xǁConfigurationErrorǁ__init____mutmut_8,
        "xǁConfigurationErrorǁ__init____mutmut_9": xǁConfigurationErrorǁ__init____mutmut_9,
        "xǁConfigurationErrorǁ__init____mutmut_10": xǁConfigurationErrorǁ__init____mutmut_10,
        "xǁConfigurationErrorǁ__init____mutmut_11": xǁConfigurationErrorǁ__init____mutmut_11,
        "xǁConfigurationErrorǁ__init____mutmut_12": xǁConfigurationErrorǁ__init____mutmut_12,
        "xǁConfigurationErrorǁ__init____mutmut_13": xǁConfigurationErrorǁ__init____mutmut_13,
        "xǁConfigurationErrorǁ__init____mutmut_14": xǁConfigurationErrorǁ__init____mutmut_14,
        "xǁConfigurationErrorǁ__init____mutmut_15": xǁConfigurationErrorǁ__init____mutmut_15,
        "xǁConfigurationErrorǁ__init____mutmut_16": xǁConfigurationErrorǁ__init____mutmut_16,
        "xǁConfigurationErrorǁ__init____mutmut_17": xǁConfigurationErrorǁ__init____mutmut_17,
        "xǁConfigurationErrorǁ__init____mutmut_18": xǁConfigurationErrorǁ__init____mutmut_18,
        "xǁConfigurationErrorǁ__init____mutmut_19": xǁConfigurationErrorǁ__init____mutmut_19,
        "xǁConfigurationErrorǁ__init____mutmut_20": xǁConfigurationErrorǁ__init____mutmut_20,
        "xǁConfigurationErrorǁ__init____mutmut_21": xǁConfigurationErrorǁ__init____mutmut_21,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigurationErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁConfigurationErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁConfigurationErrorǁ__init____mutmut_orig)
    xǁConfigurationErrorǁ__init____mutmut_orig.__name__ = "xǁConfigurationErrorǁ__init__"

    def xǁConfigurationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "CONFIG_ERROR"

    def xǁConfigurationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXCONFIG_ERRORXX"

    def xǁConfigurationErrorǁ_default_code__mutmut_2(self) -> str:
        return "config_error"

    xǁConfigurationErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigurationErrorǁ_default_code__mutmut_1": xǁConfigurationErrorǁ_default_code__mutmut_1,
        "xǁConfigurationErrorǁ_default_code__mutmut_2": xǁConfigurationErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigurationErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigurationErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁConfigurationErrorǁ_default_code__mutmut_orig)
    xǁConfigurationErrorǁ_default_code__mutmut_orig.__name__ = "xǁConfigurationErrorǁ_default_code"


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

    def xǁValidationErrorǁ__init____mutmut_orig(
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

    def xǁValidationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault("context", {})["validation.field"] = None
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault(None, {})["validation.field"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault("context", None)["validation.field"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault({})["validation.field"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault(
                "context",
            )["validation.field"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault("XXcontextXX", {})["validation.field"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault("CONTEXT", {})["validation.field"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault("context", {})["XXvalidation.fieldXX"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any,
    ) -> None:
        if field:
            kwargs.setdefault("context", {})["VALIDATION.FIELD"] = field
        if value is not None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_10(
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
        if value is None:
            kwargs.setdefault("context", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_11(
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
            kwargs.setdefault("context", {})["validation.value"] = None
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_12(
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
            kwargs.setdefault(None, {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_13(
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
            kwargs.setdefault("context", None)["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_14(
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
            kwargs.setdefault({})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_15(
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
            kwargs.setdefault(
                "context",
            )["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_16(
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
            kwargs.setdefault("XXcontextXX", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_17(
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
            kwargs.setdefault("CONTEXT", {})["validation.value"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_18(
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
            kwargs.setdefault("context", {})["XXvalidation.valueXX"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_19(
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
            kwargs.setdefault("context", {})["VALIDATION.VALUE"] = str(value)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_20(
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
            kwargs.setdefault("context", {})["validation.value"] = str(None)
        if rule:
            kwargs.setdefault("context", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_21(
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
            kwargs.setdefault("context", {})["validation.rule"] = None
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_22(
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
            kwargs.setdefault(None, {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_23(
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
            kwargs.setdefault("context", None)["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_24(
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
            kwargs.setdefault({})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_25(
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
            kwargs.setdefault(
                "context",
            )["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_26(
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
            kwargs.setdefault("XXcontextXX", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_27(
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
            kwargs.setdefault("CONTEXT", {})["validation.rule"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_28(
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
            kwargs.setdefault("context", {})["XXvalidation.ruleXX"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_29(
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
            kwargs.setdefault("context", {})["VALIDATION.RULE"] = rule
        super().__init__(message, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_30(
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
        super().__init__(None, **kwargs)

    def xǁValidationErrorǁ__init____mutmut_31(
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
        super().__init__(**kwargs)

    def xǁValidationErrorǁ__init____mutmut_32(
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
        super().__init__(
            message,
        )

    xǁValidationErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁValidationErrorǁ__init____mutmut_1": xǁValidationErrorǁ__init____mutmut_1,
        "xǁValidationErrorǁ__init____mutmut_2": xǁValidationErrorǁ__init____mutmut_2,
        "xǁValidationErrorǁ__init____mutmut_3": xǁValidationErrorǁ__init____mutmut_3,
        "xǁValidationErrorǁ__init____mutmut_4": xǁValidationErrorǁ__init____mutmut_4,
        "xǁValidationErrorǁ__init____mutmut_5": xǁValidationErrorǁ__init____mutmut_5,
        "xǁValidationErrorǁ__init____mutmut_6": xǁValidationErrorǁ__init____mutmut_6,
        "xǁValidationErrorǁ__init____mutmut_7": xǁValidationErrorǁ__init____mutmut_7,
        "xǁValidationErrorǁ__init____mutmut_8": xǁValidationErrorǁ__init____mutmut_8,
        "xǁValidationErrorǁ__init____mutmut_9": xǁValidationErrorǁ__init____mutmut_9,
        "xǁValidationErrorǁ__init____mutmut_10": xǁValidationErrorǁ__init____mutmut_10,
        "xǁValidationErrorǁ__init____mutmut_11": xǁValidationErrorǁ__init____mutmut_11,
        "xǁValidationErrorǁ__init____mutmut_12": xǁValidationErrorǁ__init____mutmut_12,
        "xǁValidationErrorǁ__init____mutmut_13": xǁValidationErrorǁ__init____mutmut_13,
        "xǁValidationErrorǁ__init____mutmut_14": xǁValidationErrorǁ__init____mutmut_14,
        "xǁValidationErrorǁ__init____mutmut_15": xǁValidationErrorǁ__init____mutmut_15,
        "xǁValidationErrorǁ__init____mutmut_16": xǁValidationErrorǁ__init____mutmut_16,
        "xǁValidationErrorǁ__init____mutmut_17": xǁValidationErrorǁ__init____mutmut_17,
        "xǁValidationErrorǁ__init____mutmut_18": xǁValidationErrorǁ__init____mutmut_18,
        "xǁValidationErrorǁ__init____mutmut_19": xǁValidationErrorǁ__init____mutmut_19,
        "xǁValidationErrorǁ__init____mutmut_20": xǁValidationErrorǁ__init____mutmut_20,
        "xǁValidationErrorǁ__init____mutmut_21": xǁValidationErrorǁ__init____mutmut_21,
        "xǁValidationErrorǁ__init____mutmut_22": xǁValidationErrorǁ__init____mutmut_22,
        "xǁValidationErrorǁ__init____mutmut_23": xǁValidationErrorǁ__init____mutmut_23,
        "xǁValidationErrorǁ__init____mutmut_24": xǁValidationErrorǁ__init____mutmut_24,
        "xǁValidationErrorǁ__init____mutmut_25": xǁValidationErrorǁ__init____mutmut_25,
        "xǁValidationErrorǁ__init____mutmut_26": xǁValidationErrorǁ__init____mutmut_26,
        "xǁValidationErrorǁ__init____mutmut_27": xǁValidationErrorǁ__init____mutmut_27,
        "xǁValidationErrorǁ__init____mutmut_28": xǁValidationErrorǁ__init____mutmut_28,
        "xǁValidationErrorǁ__init____mutmut_29": xǁValidationErrorǁ__init____mutmut_29,
        "xǁValidationErrorǁ__init____mutmut_30": xǁValidationErrorǁ__init____mutmut_30,
        "xǁValidationErrorǁ__init____mutmut_31": xǁValidationErrorǁ__init____mutmut_31,
        "xǁValidationErrorǁ__init____mutmut_32": xǁValidationErrorǁ__init____mutmut_32,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁValidationErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁValidationErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁValidationErrorǁ__init____mutmut_orig)
    xǁValidationErrorǁ__init____mutmut_orig.__name__ = "xǁValidationErrorǁ__init__"

    def xǁValidationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "VALIDATION_ERROR"

    def xǁValidationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXVALIDATION_ERRORXX"

    def xǁValidationErrorǁ_default_code__mutmut_2(self) -> str:
        return "validation_error"

    xǁValidationErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁValidationErrorǁ_default_code__mutmut_1": xǁValidationErrorǁ_default_code__mutmut_1,
        "xǁValidationErrorǁ_default_code__mutmut_2": xǁValidationErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁValidationErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁValidationErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁValidationErrorǁ_default_code__mutmut_orig)
    xǁValidationErrorǁ_default_code__mutmut_orig.__name__ = "xǁValidationErrorǁ_default_code"


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

    def xǁConfigValidationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", {})["config.class"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", {})["config.class"] = None
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault(None, {})["config.class"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", None)["config.class"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault({})["config.class"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault(
                "context",
            )["config.class"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("XXcontextXX", {})["config.class"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("CONTEXT", {})["config.class"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", {})["XXconfig.classXX"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", {})["CONFIG.CLASS"] = config_class
        super().__init__(message, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", {})["config.class"] = config_class
        super().__init__(None, **kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", {})["config.class"] = config_class
        super().__init__(**kwargs)

    def xǁConfigValidationErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        config_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        if config_class:
            kwargs.setdefault("context", {})["config.class"] = config_class
        super().__init__(
            message,
        )

    xǁConfigValidationErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigValidationErrorǁ__init____mutmut_1": xǁConfigValidationErrorǁ__init____mutmut_1,
        "xǁConfigValidationErrorǁ__init____mutmut_2": xǁConfigValidationErrorǁ__init____mutmut_2,
        "xǁConfigValidationErrorǁ__init____mutmut_3": xǁConfigValidationErrorǁ__init____mutmut_3,
        "xǁConfigValidationErrorǁ__init____mutmut_4": xǁConfigValidationErrorǁ__init____mutmut_4,
        "xǁConfigValidationErrorǁ__init____mutmut_5": xǁConfigValidationErrorǁ__init____mutmut_5,
        "xǁConfigValidationErrorǁ__init____mutmut_6": xǁConfigValidationErrorǁ__init____mutmut_6,
        "xǁConfigValidationErrorǁ__init____mutmut_7": xǁConfigValidationErrorǁ__init____mutmut_7,
        "xǁConfigValidationErrorǁ__init____mutmut_8": xǁConfigValidationErrorǁ__init____mutmut_8,
        "xǁConfigValidationErrorǁ__init____mutmut_9": xǁConfigValidationErrorǁ__init____mutmut_9,
        "xǁConfigValidationErrorǁ__init____mutmut_10": xǁConfigValidationErrorǁ__init____mutmut_10,
        "xǁConfigValidationErrorǁ__init____mutmut_11": xǁConfigValidationErrorǁ__init____mutmut_11,
        "xǁConfigValidationErrorǁ__init____mutmut_12": xǁConfigValidationErrorǁ__init____mutmut_12,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigValidationErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁConfigValidationErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁConfigValidationErrorǁ__init____mutmut_orig)
    xǁConfigValidationErrorǁ__init____mutmut_orig.__name__ = "xǁConfigValidationErrorǁ__init__"

    def xǁConfigValidationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "CONFIG_VALIDATION_ERROR"

    def xǁConfigValidationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXCONFIG_VALIDATION_ERRORXX"

    def xǁConfigValidationErrorǁ_default_code__mutmut_2(self) -> str:
        return "config_validation_error"

    xǁConfigValidationErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigValidationErrorǁ_default_code__mutmut_1": xǁConfigValidationErrorǁ_default_code__mutmut_1,
        "xǁConfigValidationErrorǁ_default_code__mutmut_2": xǁConfigValidationErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigValidationErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigValidationErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁConfigValidationErrorǁ_default_code__mutmut_orig)
    xǁConfigValidationErrorǁ_default_code__mutmut_orig.__name__ = "xǁConfigValidationErrorǁ_default_code"


# <3 🧱🤝🐛🪄
