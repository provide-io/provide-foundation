# provide/foundation/logger/custom_processors.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# custom_processors.py
#
import logging as stdlib_logging
from typing import Any, Protocol

import structlog

from provide.foundation.logger.constants import DEFAULT_FALLBACK_NUMERIC
from provide.foundation.logger.levels import get_numeric_level, normalize_level
from provide.foundation.logger.types import TRACE_LEVEL_NAME, TRACE_LEVEL_NUM, LogLevelStr

"""Foundation Telemetry Custom Structlog Processors.
Includes processors for log level normalization, level-based filtering,
and logger name emoji prefixes. The semantic field emoji prefix processor
is now created as a closure in config.py.
"""

_NUMERIC_TO_LEVEL_NAME_CUSTOM: dict[int, str] = {
    stdlib_logging.CRITICAL: "critical",
    stdlib_logging.ERROR: "error",
    stdlib_logging.WARNING: "warning",
    stdlib_logging.INFO: "info",
    stdlib_logging.DEBUG: "debug",
    TRACE_LEVEL_NUM: TRACE_LEVEL_NAME.lower(),
}
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


class StructlogProcessor(Protocol):
    def __call__(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict: ...  # pragma: no cover


def x_add_log_level_custom__mutmut_orig(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_1(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = None
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_2(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop(None, None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_3(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop(None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_4(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop(
        "_foundation_level_hint",
    )
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_5(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("XX_foundation_level_hintXX", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_6(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_FOUNDATION_LEVEL_HINT", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_7(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_8(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = None
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_9(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["XXlevelXX"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_10(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["LEVEL"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_11(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.upper()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_12(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "XXlevelXX" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_13(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "LEVEL" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_14(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_15(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_16(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_17(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_18(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
    return event_dict


def x_add_log_level_custom__mutmut_19(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "XXexceptionXX":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_20(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "EXCEPTION":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_21(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = None
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_22(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["XXlevelXX"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_23(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["LEVEL"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_24(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "XXerrorXX"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_25(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "ERROR"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_26(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "XXwarnXX":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_27(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "WARN":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_28(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = None
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_29(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["XXlevelXX"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_30(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["LEVEL"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_31(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "XXwarningXX"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_32(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "WARNING"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_33(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "XXmsgXX":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_34(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "MSG":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_35(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = None
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_36(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["XXlevelXX"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_37(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["LEVEL"] = "info"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_38(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "XXinfoXX"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_39(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "INFO"
            case _:
                event_dict["level"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_40(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = None
    return event_dict


def x_add_log_level_custom__mutmut_41(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["XXlevelXX"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_42(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["LEVEL"] = method_name.lower()
    return event_dict


def x_add_log_level_custom__mutmut_43(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.upper()
    return event_dict


x_add_log_level_custom__mutmut_mutants: ClassVar[MutantDict] = {
    "x_add_log_level_custom__mutmut_1": x_add_log_level_custom__mutmut_1,
    "x_add_log_level_custom__mutmut_2": x_add_log_level_custom__mutmut_2,
    "x_add_log_level_custom__mutmut_3": x_add_log_level_custom__mutmut_3,
    "x_add_log_level_custom__mutmut_4": x_add_log_level_custom__mutmut_4,
    "x_add_log_level_custom__mutmut_5": x_add_log_level_custom__mutmut_5,
    "x_add_log_level_custom__mutmut_6": x_add_log_level_custom__mutmut_6,
    "x_add_log_level_custom__mutmut_7": x_add_log_level_custom__mutmut_7,
    "x_add_log_level_custom__mutmut_8": x_add_log_level_custom__mutmut_8,
    "x_add_log_level_custom__mutmut_9": x_add_log_level_custom__mutmut_9,
    "x_add_log_level_custom__mutmut_10": x_add_log_level_custom__mutmut_10,
    "x_add_log_level_custom__mutmut_11": x_add_log_level_custom__mutmut_11,
    "x_add_log_level_custom__mutmut_12": x_add_log_level_custom__mutmut_12,
    "x_add_log_level_custom__mutmut_13": x_add_log_level_custom__mutmut_13,
    "x_add_log_level_custom__mutmut_14": x_add_log_level_custom__mutmut_14,
    "x_add_log_level_custom__mutmut_15": x_add_log_level_custom__mutmut_15,
    "x_add_log_level_custom__mutmut_16": x_add_log_level_custom__mutmut_16,
    "x_add_log_level_custom__mutmut_17": x_add_log_level_custom__mutmut_17,
    "x_add_log_level_custom__mutmut_18": x_add_log_level_custom__mutmut_18,
    "x_add_log_level_custom__mutmut_19": x_add_log_level_custom__mutmut_19,
    "x_add_log_level_custom__mutmut_20": x_add_log_level_custom__mutmut_20,
    "x_add_log_level_custom__mutmut_21": x_add_log_level_custom__mutmut_21,
    "x_add_log_level_custom__mutmut_22": x_add_log_level_custom__mutmut_22,
    "x_add_log_level_custom__mutmut_23": x_add_log_level_custom__mutmut_23,
    "x_add_log_level_custom__mutmut_24": x_add_log_level_custom__mutmut_24,
    "x_add_log_level_custom__mutmut_25": x_add_log_level_custom__mutmut_25,
    "x_add_log_level_custom__mutmut_26": x_add_log_level_custom__mutmut_26,
    "x_add_log_level_custom__mutmut_27": x_add_log_level_custom__mutmut_27,
    "x_add_log_level_custom__mutmut_28": x_add_log_level_custom__mutmut_28,
    "x_add_log_level_custom__mutmut_29": x_add_log_level_custom__mutmut_29,
    "x_add_log_level_custom__mutmut_30": x_add_log_level_custom__mutmut_30,
    "x_add_log_level_custom__mutmut_31": x_add_log_level_custom__mutmut_31,
    "x_add_log_level_custom__mutmut_32": x_add_log_level_custom__mutmut_32,
    "x_add_log_level_custom__mutmut_33": x_add_log_level_custom__mutmut_33,
    "x_add_log_level_custom__mutmut_34": x_add_log_level_custom__mutmut_34,
    "x_add_log_level_custom__mutmut_35": x_add_log_level_custom__mutmut_35,
    "x_add_log_level_custom__mutmut_36": x_add_log_level_custom__mutmut_36,
    "x_add_log_level_custom__mutmut_37": x_add_log_level_custom__mutmut_37,
    "x_add_log_level_custom__mutmut_38": x_add_log_level_custom__mutmut_38,
    "x_add_log_level_custom__mutmut_39": x_add_log_level_custom__mutmut_39,
    "x_add_log_level_custom__mutmut_40": x_add_log_level_custom__mutmut_40,
    "x_add_log_level_custom__mutmut_41": x_add_log_level_custom__mutmut_41,
    "x_add_log_level_custom__mutmut_42": x_add_log_level_custom__mutmut_42,
    "x_add_log_level_custom__mutmut_43": x_add_log_level_custom__mutmut_43,
}


def add_log_level_custom(*args, **kwargs):
    result = _mutmut_trampoline(
        x_add_log_level_custom__mutmut_orig, x_add_log_level_custom__mutmut_mutants, args, kwargs
    )
    return result


add_log_level_custom.__signature__ = _mutmut_signature(x_add_log_level_custom__mutmut_orig)
x_add_log_level_custom__mutmut_orig.__name__ = "x_add_log_level_custom"


class _LevelFilter:
    def xǁ_LevelFilterǁ__init____mutmut_orig(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), key=len, reverse=True)

    def xǁ_LevelFilterǁ__init____mutmut_1(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = None
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), key=len, reverse=True)

    def xǁ_LevelFilterǁ__init____mutmut_2(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = None
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), key=len, reverse=True)

    def xǁ_LevelFilterǁ__init____mutmut_3(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = None
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), key=len, reverse=True)

    def xǁ_LevelFilterǁ__init____mutmut_4(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = None

    def xǁ_LevelFilterǁ__init____mutmut_5(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(None, key=len, reverse=True)

    def xǁ_LevelFilterǁ__init____mutmut_6(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), key=None, reverse=True)

    def xǁ_LevelFilterǁ__init____mutmut_7(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), key=len, reverse=None)

    def xǁ_LevelFilterǁ__init____mutmut_8(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(key=len, reverse=True)

    def xǁ_LevelFilterǁ__init____mutmut_9(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), reverse=True)

    def xǁ_LevelFilterǁ__init____mutmut_10(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(
            self.module_numeric_levels.keys(),
            key=len,
        )

    def xǁ_LevelFilterǁ__init____mutmut_11(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), key=len, reverse=False)

    xǁ_LevelFilterǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁ_LevelFilterǁ__init____mutmut_1": xǁ_LevelFilterǁ__init____mutmut_1,
        "xǁ_LevelFilterǁ__init____mutmut_2": xǁ_LevelFilterǁ__init____mutmut_2,
        "xǁ_LevelFilterǁ__init____mutmut_3": xǁ_LevelFilterǁ__init____mutmut_3,
        "xǁ_LevelFilterǁ__init____mutmut_4": xǁ_LevelFilterǁ__init____mutmut_4,
        "xǁ_LevelFilterǁ__init____mutmut_5": xǁ_LevelFilterǁ__init____mutmut_5,
        "xǁ_LevelFilterǁ__init____mutmut_6": xǁ_LevelFilterǁ__init____mutmut_6,
        "xǁ_LevelFilterǁ__init____mutmut_7": xǁ_LevelFilterǁ__init____mutmut_7,
        "xǁ_LevelFilterǁ__init____mutmut_8": xǁ_LevelFilterǁ__init____mutmut_8,
        "xǁ_LevelFilterǁ__init____mutmut_9": xǁ_LevelFilterǁ__init____mutmut_9,
        "xǁ_LevelFilterǁ__init____mutmut_10": xǁ_LevelFilterǁ__init____mutmut_10,
        "xǁ_LevelFilterǁ__init____mutmut_11": xǁ_LevelFilterǁ__init____mutmut_11,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁ_LevelFilterǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁ_LevelFilterǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁ_LevelFilterǁ__init____mutmut_orig)
    xǁ_LevelFilterǁ__init____mutmut_orig.__name__ = "xǁ_LevelFilterǁ__init__"

    def xǁ_LevelFilterǁ__call____mutmut_orig(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_1(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = None
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_2(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get(None, "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_3(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", None)
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_4(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_5(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get(
            "logger_name",
        )
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_6(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("XXlogger_nameXX", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_7(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("LOGGER_NAME", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_8(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "XXunnamed_filter_targetXX")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_9(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "UNNAMED_FILTER_TARGET")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_10(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = None

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_11(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(None)

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_12(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get(None, "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_13(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", None))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_14(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_15(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(
            event_dict.get(
                "level",
            )
        )

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_16(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("XXlevelXX", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_17(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("LEVEL", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_18(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "XXinfoXX"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_19(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "INFO"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_20(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = None
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_21(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(None)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_22(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = None
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_23(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            None,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_24(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=None,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_25(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_26(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_27(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = None
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_28(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(None):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_29(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = None
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_30(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                return
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    def xǁ_LevelFilterǁ__call____mutmut_31(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level <= threshold_num_level:
            raise structlog.DropEvent
        return event_dict

    xǁ_LevelFilterǁ__call____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁ_LevelFilterǁ__call____mutmut_1": xǁ_LevelFilterǁ__call____mutmut_1,
        "xǁ_LevelFilterǁ__call____mutmut_2": xǁ_LevelFilterǁ__call____mutmut_2,
        "xǁ_LevelFilterǁ__call____mutmut_3": xǁ_LevelFilterǁ__call____mutmut_3,
        "xǁ_LevelFilterǁ__call____mutmut_4": xǁ_LevelFilterǁ__call____mutmut_4,
        "xǁ_LevelFilterǁ__call____mutmut_5": xǁ_LevelFilterǁ__call____mutmut_5,
        "xǁ_LevelFilterǁ__call____mutmut_6": xǁ_LevelFilterǁ__call____mutmut_6,
        "xǁ_LevelFilterǁ__call____mutmut_7": xǁ_LevelFilterǁ__call____mutmut_7,
        "xǁ_LevelFilterǁ__call____mutmut_8": xǁ_LevelFilterǁ__call____mutmut_8,
        "xǁ_LevelFilterǁ__call____mutmut_9": xǁ_LevelFilterǁ__call____mutmut_9,
        "xǁ_LevelFilterǁ__call____mutmut_10": xǁ_LevelFilterǁ__call____mutmut_10,
        "xǁ_LevelFilterǁ__call____mutmut_11": xǁ_LevelFilterǁ__call____mutmut_11,
        "xǁ_LevelFilterǁ__call____mutmut_12": xǁ_LevelFilterǁ__call____mutmut_12,
        "xǁ_LevelFilterǁ__call____mutmut_13": xǁ_LevelFilterǁ__call____mutmut_13,
        "xǁ_LevelFilterǁ__call____mutmut_14": xǁ_LevelFilterǁ__call____mutmut_14,
        "xǁ_LevelFilterǁ__call____mutmut_15": xǁ_LevelFilterǁ__call____mutmut_15,
        "xǁ_LevelFilterǁ__call____mutmut_16": xǁ_LevelFilterǁ__call____mutmut_16,
        "xǁ_LevelFilterǁ__call____mutmut_17": xǁ_LevelFilterǁ__call____mutmut_17,
        "xǁ_LevelFilterǁ__call____mutmut_18": xǁ_LevelFilterǁ__call____mutmut_18,
        "xǁ_LevelFilterǁ__call____mutmut_19": xǁ_LevelFilterǁ__call____mutmut_19,
        "xǁ_LevelFilterǁ__call____mutmut_20": xǁ_LevelFilterǁ__call____mutmut_20,
        "xǁ_LevelFilterǁ__call____mutmut_21": xǁ_LevelFilterǁ__call____mutmut_21,
        "xǁ_LevelFilterǁ__call____mutmut_22": xǁ_LevelFilterǁ__call____mutmut_22,
        "xǁ_LevelFilterǁ__call____mutmut_23": xǁ_LevelFilterǁ__call____mutmut_23,
        "xǁ_LevelFilterǁ__call____mutmut_24": xǁ_LevelFilterǁ__call____mutmut_24,
        "xǁ_LevelFilterǁ__call____mutmut_25": xǁ_LevelFilterǁ__call____mutmut_25,
        "xǁ_LevelFilterǁ__call____mutmut_26": xǁ_LevelFilterǁ__call____mutmut_26,
        "xǁ_LevelFilterǁ__call____mutmut_27": xǁ_LevelFilterǁ__call____mutmut_27,
        "xǁ_LevelFilterǁ__call____mutmut_28": xǁ_LevelFilterǁ__call____mutmut_28,
        "xǁ_LevelFilterǁ__call____mutmut_29": xǁ_LevelFilterǁ__call____mutmut_29,
        "xǁ_LevelFilterǁ__call____mutmut_30": xǁ_LevelFilterǁ__call____mutmut_30,
        "xǁ_LevelFilterǁ__call____mutmut_31": xǁ_LevelFilterǁ__call____mutmut_31,
    }

    def __call__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁ_LevelFilterǁ__call____mutmut_orig"),
            object.__getattribute__(self, "xǁ_LevelFilterǁ__call____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __call__.__signature__ = _mutmut_signature(xǁ_LevelFilterǁ__call____mutmut_orig)
    xǁ_LevelFilterǁ__call____mutmut_orig.__name__ = "xǁ_LevelFilterǁ__call__"


def x_filter_by_level_custom__mutmut_orig(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int],
) -> _LevelFilter:
    return _LevelFilter(default_level_str, module_levels, level_to_numeric_map)


def x_filter_by_level_custom__mutmut_1(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int],
) -> _LevelFilter:
    return _LevelFilter(None, module_levels, level_to_numeric_map)


def x_filter_by_level_custom__mutmut_2(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int],
) -> _LevelFilter:
    return _LevelFilter(default_level_str, None, level_to_numeric_map)


def x_filter_by_level_custom__mutmut_3(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int],
) -> _LevelFilter:
    return _LevelFilter(default_level_str, module_levels, None)


def x_filter_by_level_custom__mutmut_4(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int],
) -> _LevelFilter:
    return _LevelFilter(module_levels, level_to_numeric_map)


def x_filter_by_level_custom__mutmut_5(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int],
) -> _LevelFilter:
    return _LevelFilter(default_level_str, level_to_numeric_map)


def x_filter_by_level_custom__mutmut_6(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int],
) -> _LevelFilter:
    return _LevelFilter(
        default_level_str,
        module_levels,
    )


x_filter_by_level_custom__mutmut_mutants: ClassVar[MutantDict] = {
    "x_filter_by_level_custom__mutmut_1": x_filter_by_level_custom__mutmut_1,
    "x_filter_by_level_custom__mutmut_2": x_filter_by_level_custom__mutmut_2,
    "x_filter_by_level_custom__mutmut_3": x_filter_by_level_custom__mutmut_3,
    "x_filter_by_level_custom__mutmut_4": x_filter_by_level_custom__mutmut_4,
    "x_filter_by_level_custom__mutmut_5": x_filter_by_level_custom__mutmut_5,
    "x_filter_by_level_custom__mutmut_6": x_filter_by_level_custom__mutmut_6,
}


def filter_by_level_custom(*args, **kwargs):
    result = _mutmut_trampoline(
        x_filter_by_level_custom__mutmut_orig, x_filter_by_level_custom__mutmut_mutants, args, kwargs
    )
    return result


filter_by_level_custom.__signature__ = _mutmut_signature(x_filter_by_level_custom__mutmut_orig)
x_filter_by_level_custom__mutmut_orig.__name__ = "x_filter_by_level_custom"


_LOGGER_NAME_EMOJI_PREFIXES: dict[str, str] = {
    "provide.foundation.core.test": "⚙️",
    "provide.foundation.core_setup": "🛠️",
    "provide.foundation.emoji_matrix_display": "💡",
    "provide.foundation": "⚙️",
    "provide.foundation.logger": "📝",
    "provide.foundation.logger.config": "🔩",
    "pyvider.dynamic_call_trace": "👣",
    "pyvider.dynamic_call": "🗣️",
    "pyvider.default": "📦",
    "formatter.test": "🎨",
    "service.alpha": "🇦",
    "service.beta": "🇧",
    "service.beta.child": "👶",
    "service.gamma.trace_enabled": "🇬",
    "service.delta": "🇩",
    "das.test": "🃏",
    "json.exc.test": "💥",
    "service.name.test": "📛",
    "simple": "📄",
    "test.basic": "🧪",
    "unknown": "❓",
    "test": "🧪",
    "default": "🔹",
    "emoji.test": "🎭",
}
_SORTED_LOGGER_NAME_EMOJI_KEYWORDS: list[str] = sorted(
    _LOGGER_NAME_EMOJI_PREFIXES.keys(),
    key=len,
    reverse=True,
)
_EMOJI_LOOKUP_CACHE: dict[str, str] = {}
_EMOJI_CACHE_SIZE_LIMIT: int = 1000


def x__compute_emoji_for_logger_name__mutmut_orig(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", "🔹")


def x__compute_emoji_for_logger_name__mutmut_1(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword != "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", "🔹")


def x__compute_emoji_for_logger_name__mutmut_2(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "XXdefaultXX":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", "🔹")


def x__compute_emoji_for_logger_name__mutmut_3(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "DEFAULT":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", "🔹")


def x__compute_emoji_for_logger_name__mutmut_4(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            break
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", "🔹")


def x__compute_emoji_for_logger_name__mutmut_5(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(None):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", "🔹")


def x__compute_emoji_for_logger_name__mutmut_6(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get(None, "🔹")


def x__compute_emoji_for_logger_name__mutmut_7(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", None)


def x__compute_emoji_for_logger_name__mutmut_8(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("🔹")


def x__compute_emoji_for_logger_name__mutmut_9(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get(
        "default",
    )


def x__compute_emoji_for_logger_name__mutmut_10(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("XXdefaultXX", "🔹")


def x__compute_emoji_for_logger_name__mutmut_11(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("DEFAULT", "🔹")


def x__compute_emoji_for_logger_name__mutmut_12(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", "XX🔹XX")


x__compute_emoji_for_logger_name__mutmut_mutants: ClassVar[MutantDict] = {
    "x__compute_emoji_for_logger_name__mutmut_1": x__compute_emoji_for_logger_name__mutmut_1,
    "x__compute_emoji_for_logger_name__mutmut_2": x__compute_emoji_for_logger_name__mutmut_2,
    "x__compute_emoji_for_logger_name__mutmut_3": x__compute_emoji_for_logger_name__mutmut_3,
    "x__compute_emoji_for_logger_name__mutmut_4": x__compute_emoji_for_logger_name__mutmut_4,
    "x__compute_emoji_for_logger_name__mutmut_5": x__compute_emoji_for_logger_name__mutmut_5,
    "x__compute_emoji_for_logger_name__mutmut_6": x__compute_emoji_for_logger_name__mutmut_6,
    "x__compute_emoji_for_logger_name__mutmut_7": x__compute_emoji_for_logger_name__mutmut_7,
    "x__compute_emoji_for_logger_name__mutmut_8": x__compute_emoji_for_logger_name__mutmut_8,
    "x__compute_emoji_for_logger_name__mutmut_9": x__compute_emoji_for_logger_name__mutmut_9,
    "x__compute_emoji_for_logger_name__mutmut_10": x__compute_emoji_for_logger_name__mutmut_10,
    "x__compute_emoji_for_logger_name__mutmut_11": x__compute_emoji_for_logger_name__mutmut_11,
    "x__compute_emoji_for_logger_name__mutmut_12": x__compute_emoji_for_logger_name__mutmut_12,
}


def _compute_emoji_for_logger_name(*args, **kwargs):
    result = _mutmut_trampoline(
        x__compute_emoji_for_logger_name__mutmut_orig,
        x__compute_emoji_for_logger_name__mutmut_mutants,
        args,
        kwargs,
    )
    return result


_compute_emoji_for_logger_name.__signature__ = _mutmut_signature(x__compute_emoji_for_logger_name__mutmut_orig)
x__compute_emoji_for_logger_name__mutmut_orig.__name__ = "x__compute_emoji_for_logger_name"


def x_add_logger_name_emoji_prefix__mutmut_orig(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_1(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = None
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_2(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get(None, "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_3(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", None)
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_4(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_5(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get(
        "logger_name",
    )
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_6(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("XXlogger_nameXX", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_7(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("LOGGER_NAME", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_8(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "XXdefaultXX")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_9(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "DEFAULT")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_10(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name not in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_11(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = None
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_12(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = None
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_13(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(None)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_14(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) <= _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_15(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = None
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_16(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = None
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_17(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get(None)
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_18(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("XXeventXX")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_19(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("EVENT")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_20(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_21(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = None
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_22(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["XXeventXX"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_23(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["EVENT"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_24(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = None
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_25(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["XXeventXX"] = chosen_emoji
    return event_dict


def x_add_logger_name_emoji_prefix__mutmut_26(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["EVENT"] = chosen_emoji
    return event_dict


x_add_logger_name_emoji_prefix__mutmut_mutants: ClassVar[MutantDict] = {
    "x_add_logger_name_emoji_prefix__mutmut_1": x_add_logger_name_emoji_prefix__mutmut_1,
    "x_add_logger_name_emoji_prefix__mutmut_2": x_add_logger_name_emoji_prefix__mutmut_2,
    "x_add_logger_name_emoji_prefix__mutmut_3": x_add_logger_name_emoji_prefix__mutmut_3,
    "x_add_logger_name_emoji_prefix__mutmut_4": x_add_logger_name_emoji_prefix__mutmut_4,
    "x_add_logger_name_emoji_prefix__mutmut_5": x_add_logger_name_emoji_prefix__mutmut_5,
    "x_add_logger_name_emoji_prefix__mutmut_6": x_add_logger_name_emoji_prefix__mutmut_6,
    "x_add_logger_name_emoji_prefix__mutmut_7": x_add_logger_name_emoji_prefix__mutmut_7,
    "x_add_logger_name_emoji_prefix__mutmut_8": x_add_logger_name_emoji_prefix__mutmut_8,
    "x_add_logger_name_emoji_prefix__mutmut_9": x_add_logger_name_emoji_prefix__mutmut_9,
    "x_add_logger_name_emoji_prefix__mutmut_10": x_add_logger_name_emoji_prefix__mutmut_10,
    "x_add_logger_name_emoji_prefix__mutmut_11": x_add_logger_name_emoji_prefix__mutmut_11,
    "x_add_logger_name_emoji_prefix__mutmut_12": x_add_logger_name_emoji_prefix__mutmut_12,
    "x_add_logger_name_emoji_prefix__mutmut_13": x_add_logger_name_emoji_prefix__mutmut_13,
    "x_add_logger_name_emoji_prefix__mutmut_14": x_add_logger_name_emoji_prefix__mutmut_14,
    "x_add_logger_name_emoji_prefix__mutmut_15": x_add_logger_name_emoji_prefix__mutmut_15,
    "x_add_logger_name_emoji_prefix__mutmut_16": x_add_logger_name_emoji_prefix__mutmut_16,
    "x_add_logger_name_emoji_prefix__mutmut_17": x_add_logger_name_emoji_prefix__mutmut_17,
    "x_add_logger_name_emoji_prefix__mutmut_18": x_add_logger_name_emoji_prefix__mutmut_18,
    "x_add_logger_name_emoji_prefix__mutmut_19": x_add_logger_name_emoji_prefix__mutmut_19,
    "x_add_logger_name_emoji_prefix__mutmut_20": x_add_logger_name_emoji_prefix__mutmut_20,
    "x_add_logger_name_emoji_prefix__mutmut_21": x_add_logger_name_emoji_prefix__mutmut_21,
    "x_add_logger_name_emoji_prefix__mutmut_22": x_add_logger_name_emoji_prefix__mutmut_22,
    "x_add_logger_name_emoji_prefix__mutmut_23": x_add_logger_name_emoji_prefix__mutmut_23,
    "x_add_logger_name_emoji_prefix__mutmut_24": x_add_logger_name_emoji_prefix__mutmut_24,
    "x_add_logger_name_emoji_prefix__mutmut_25": x_add_logger_name_emoji_prefix__mutmut_25,
    "x_add_logger_name_emoji_prefix__mutmut_26": x_add_logger_name_emoji_prefix__mutmut_26,
}


def add_logger_name_emoji_prefix(*args, **kwargs):
    result = _mutmut_trampoline(
        x_add_logger_name_emoji_prefix__mutmut_orig,
        x_add_logger_name_emoji_prefix__mutmut_mutants,
        args,
        kwargs,
    )
    return result


add_logger_name_emoji_prefix.__signature__ = _mutmut_signature(x_add_logger_name_emoji_prefix__mutmut_orig)
x_add_logger_name_emoji_prefix__mutmut_orig.__name__ = "x_add_logger_name_emoji_prefix"


def x_get_emoji_cache_stats__mutmut_orig() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_1() -> dict[str, Any]:  # pragma: no cover
    return {
        "XXcache_sizeXX": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_2() -> dict[str, Any]:  # pragma: no cover
    return {
        "CACHE_SIZE": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_3() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "XXcache_limitXX": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_4() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "CACHE_LIMIT": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_5() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "XXcache_utilizationXX": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_6() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "CACHE_UTILIZATION": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_7() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT / 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_8() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) * _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_9() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 101
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_10() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT >= 0
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_11() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 1
        else 0,
    }


def x_get_emoji_cache_stats__mutmut_12() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 1,
    }


x_get_emoji_cache_stats__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_emoji_cache_stats__mutmut_1": x_get_emoji_cache_stats__mutmut_1,
    "x_get_emoji_cache_stats__mutmut_2": x_get_emoji_cache_stats__mutmut_2,
    "x_get_emoji_cache_stats__mutmut_3": x_get_emoji_cache_stats__mutmut_3,
    "x_get_emoji_cache_stats__mutmut_4": x_get_emoji_cache_stats__mutmut_4,
    "x_get_emoji_cache_stats__mutmut_5": x_get_emoji_cache_stats__mutmut_5,
    "x_get_emoji_cache_stats__mutmut_6": x_get_emoji_cache_stats__mutmut_6,
    "x_get_emoji_cache_stats__mutmut_7": x_get_emoji_cache_stats__mutmut_7,
    "x_get_emoji_cache_stats__mutmut_8": x_get_emoji_cache_stats__mutmut_8,
    "x_get_emoji_cache_stats__mutmut_9": x_get_emoji_cache_stats__mutmut_9,
    "x_get_emoji_cache_stats__mutmut_10": x_get_emoji_cache_stats__mutmut_10,
    "x_get_emoji_cache_stats__mutmut_11": x_get_emoji_cache_stats__mutmut_11,
    "x_get_emoji_cache_stats__mutmut_12": x_get_emoji_cache_stats__mutmut_12,
}


def get_emoji_cache_stats(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_emoji_cache_stats__mutmut_orig, x_get_emoji_cache_stats__mutmut_mutants, args, kwargs
    )
    return result


get_emoji_cache_stats.__signature__ = _mutmut_signature(x_get_emoji_cache_stats__mutmut_orig)
x_get_emoji_cache_stats__mutmut_orig.__name__ = "x_get_emoji_cache_stats"


def clear_emoji_cache() -> None:  # pragma: no cover
    global _EMOJI_LOOKUP_CACHE
    _EMOJI_LOOKUP_CACHE.clear()


# <3 🧱🤝📝🪄
