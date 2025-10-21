# provide/foundation/logger/processors/main.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# processors.py
#
from typing import Any, TextIO, cast

import structlog

from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
from provide.foundation.logger.constants import LEVEL_TO_NUMERIC
from provide.foundation.logger.custom_processors import (
    StructlogProcessor,
    add_log_level_custom,
    add_logger_name_emoji_prefix,
    filter_by_level_custom,
)
from provide.foundation.logger.processors.trace import inject_trace_context
from provide.foundation.serialization import json_dumps

"""Structlog processors for Foundation Telemetry."""

# Module-level flags to prevent event enrichment re-initialization during resets
# These persist across structlog.reset_defaults() calls
_event_enrichment_initialized = False
_reset_in_progress = False
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__config_create_service_name_processor__mutmut_orig(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast("StructlogProcessor", processor)


def x__config_create_service_name_processor__mutmut_1(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast("StructlogProcessor", processor)


def x__config_create_service_name_processor__mutmut_2(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = None
        return event_dict

    return cast("StructlogProcessor", processor)


def x__config_create_service_name_processor__mutmut_3(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["XXservice_nameXX"] = service_name
        return event_dict

    return cast("StructlogProcessor", processor)


def x__config_create_service_name_processor__mutmut_4(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["SERVICE_NAME"] = service_name
        return event_dict

    return cast("StructlogProcessor", processor)


def x__config_create_service_name_processor__mutmut_5(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast(None, processor)


def x__config_create_service_name_processor__mutmut_6(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast("StructlogProcessor", None)


def x__config_create_service_name_processor__mutmut_7(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast(processor)


def x__config_create_service_name_processor__mutmut_8(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast("StructlogProcessor", )


def x__config_create_service_name_processor__mutmut_9(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast("XXStructlogProcessorXX", processor)


def x__config_create_service_name_processor__mutmut_10(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast("structlogprocessor", processor)


def x__config_create_service_name_processor__mutmut_11(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast("STRUCTLOGPROCESSOR", processor)

x__config_create_service_name_processor__mutmut_mutants : ClassVar[MutantDict] = {
'x__config_create_service_name_processor__mutmut_1': x__config_create_service_name_processor__mutmut_1, 
    'x__config_create_service_name_processor__mutmut_2': x__config_create_service_name_processor__mutmut_2, 
    'x__config_create_service_name_processor__mutmut_3': x__config_create_service_name_processor__mutmut_3, 
    'x__config_create_service_name_processor__mutmut_4': x__config_create_service_name_processor__mutmut_4, 
    'x__config_create_service_name_processor__mutmut_5': x__config_create_service_name_processor__mutmut_5, 
    'x__config_create_service_name_processor__mutmut_6': x__config_create_service_name_processor__mutmut_6, 
    'x__config_create_service_name_processor__mutmut_7': x__config_create_service_name_processor__mutmut_7, 
    'x__config_create_service_name_processor__mutmut_8': x__config_create_service_name_processor__mutmut_8, 
    'x__config_create_service_name_processor__mutmut_9': x__config_create_service_name_processor__mutmut_9, 
    'x__config_create_service_name_processor__mutmut_10': x__config_create_service_name_processor__mutmut_10, 
    'x__config_create_service_name_processor__mutmut_11': x__config_create_service_name_processor__mutmut_11
}

def _config_create_service_name_processor(*args, **kwargs):
    result = _mutmut_trampoline(x__config_create_service_name_processor__mutmut_orig, x__config_create_service_name_processor__mutmut_mutants, args, kwargs)
    return result 

_config_create_service_name_processor.__signature__ = _mutmut_signature(x__config_create_service_name_processor__mutmut_orig)
x__config_create_service_name_processor__mutmut_orig.__name__ = 'x__config_create_service_name_processor'


def x__config_create_timestamp_processors__mutmut_orig(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_1(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = None
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_2(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt=None, utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_3(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=None),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_4(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_5(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", ),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_6(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="XX%Y-%m-%d %H:%M:%S.%fXX", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_7(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%y-%m-%d %h:%m:%s.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_8(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%M-%D %H:%M:%S.%F", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_9(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=True),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_10(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop(None, None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_11(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop(None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_12(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", )
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_13(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("XXtimestampXX", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_14(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("TIMESTAMP", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_15(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(None)
    return processors


def x__config_create_timestamp_processors__mutmut_16(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast(None, pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_17(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", None))
    return processors


def x__config_create_timestamp_processors__mutmut_18(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast(pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_19(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", ))
    return processors


def x__config_create_timestamp_processors__mutmut_20(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("XXStructlogProcessorXX", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_21(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("structlogprocessor", pop_timestamp_processor))
    return processors


def x__config_create_timestamp_processors__mutmut_22(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("STRUCTLOGPROCESSOR", pop_timestamp_processor))
    return processors

x__config_create_timestamp_processors__mutmut_mutants : ClassVar[MutantDict] = {
'x__config_create_timestamp_processors__mutmut_1': x__config_create_timestamp_processors__mutmut_1, 
    'x__config_create_timestamp_processors__mutmut_2': x__config_create_timestamp_processors__mutmut_2, 
    'x__config_create_timestamp_processors__mutmut_3': x__config_create_timestamp_processors__mutmut_3, 
    'x__config_create_timestamp_processors__mutmut_4': x__config_create_timestamp_processors__mutmut_4, 
    'x__config_create_timestamp_processors__mutmut_5': x__config_create_timestamp_processors__mutmut_5, 
    'x__config_create_timestamp_processors__mutmut_6': x__config_create_timestamp_processors__mutmut_6, 
    'x__config_create_timestamp_processors__mutmut_7': x__config_create_timestamp_processors__mutmut_7, 
    'x__config_create_timestamp_processors__mutmut_8': x__config_create_timestamp_processors__mutmut_8, 
    'x__config_create_timestamp_processors__mutmut_9': x__config_create_timestamp_processors__mutmut_9, 
    'x__config_create_timestamp_processors__mutmut_10': x__config_create_timestamp_processors__mutmut_10, 
    'x__config_create_timestamp_processors__mutmut_11': x__config_create_timestamp_processors__mutmut_11, 
    'x__config_create_timestamp_processors__mutmut_12': x__config_create_timestamp_processors__mutmut_12, 
    'x__config_create_timestamp_processors__mutmut_13': x__config_create_timestamp_processors__mutmut_13, 
    'x__config_create_timestamp_processors__mutmut_14': x__config_create_timestamp_processors__mutmut_14, 
    'x__config_create_timestamp_processors__mutmut_15': x__config_create_timestamp_processors__mutmut_15, 
    'x__config_create_timestamp_processors__mutmut_16': x__config_create_timestamp_processors__mutmut_16, 
    'x__config_create_timestamp_processors__mutmut_17': x__config_create_timestamp_processors__mutmut_17, 
    'x__config_create_timestamp_processors__mutmut_18': x__config_create_timestamp_processors__mutmut_18, 
    'x__config_create_timestamp_processors__mutmut_19': x__config_create_timestamp_processors__mutmut_19, 
    'x__config_create_timestamp_processors__mutmut_20': x__config_create_timestamp_processors__mutmut_20, 
    'x__config_create_timestamp_processors__mutmut_21': x__config_create_timestamp_processors__mutmut_21, 
    'x__config_create_timestamp_processors__mutmut_22': x__config_create_timestamp_processors__mutmut_22
}

def _config_create_timestamp_processors(*args, **kwargs):
    result = _mutmut_trampoline(x__config_create_timestamp_processors__mutmut_orig, x__config_create_timestamp_processors__mutmut_mutants, args, kwargs)
    return result 

_config_create_timestamp_processors.__signature__ = _mutmut_signature(x__config_create_timestamp_processors__mutmut_orig)
x__config_create_timestamp_processors__mutmut_orig.__name__ = 'x__config_create_timestamp_processors'


def x__config_create_event_enrichment_processors__mutmut_orig(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_1(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = None
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_2(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(None)
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_3(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast(None, add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_4(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", None))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_5(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast(add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_6(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", ))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_7(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("XXStructlogProcessorXX", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_8(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("structlogprocessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_9(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("STRUCTLOGPROCESSOR", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_10(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_11(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = None
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_12(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace(None)
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_13(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("XXInitializing event enrichment processorXX")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_14(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_15(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("INITIALIZING EVENT ENRICHMENT PROCESSOR")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_16(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = None
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_17(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = False
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_18(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace(None)

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_19(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("XXEvent enrichment processor initializedXX")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_20(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_21(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("EVENT ENRICHMENT PROCESSOR INITIALIZED")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_22(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = None
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_23(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(None)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_24(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(None)
    return processors


def x__config_create_event_enrichment_processors__mutmut_25(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast(None, add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_26(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", None))
    return processors


def x__config_create_event_enrichment_processors__mutmut_27(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast(add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_28(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", ))
    return processors


def x__config_create_event_enrichment_processors__mutmut_29(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("XXStructlogProcessorXX", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_30(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("structlogprocessor", add_event_enrichment_processor))
    return processors


def x__config_create_event_enrichment_processors__mutmut_31(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("STRUCTLOGPROCESSOR", add_event_enrichment_processor))
    return processors

x__config_create_event_enrichment_processors__mutmut_mutants : ClassVar[MutantDict] = {
'x__config_create_event_enrichment_processors__mutmut_1': x__config_create_event_enrichment_processors__mutmut_1, 
    'x__config_create_event_enrichment_processors__mutmut_2': x__config_create_event_enrichment_processors__mutmut_2, 
    'x__config_create_event_enrichment_processors__mutmut_3': x__config_create_event_enrichment_processors__mutmut_3, 
    'x__config_create_event_enrichment_processors__mutmut_4': x__config_create_event_enrichment_processors__mutmut_4, 
    'x__config_create_event_enrichment_processors__mutmut_5': x__config_create_event_enrichment_processors__mutmut_5, 
    'x__config_create_event_enrichment_processors__mutmut_6': x__config_create_event_enrichment_processors__mutmut_6, 
    'x__config_create_event_enrichment_processors__mutmut_7': x__config_create_event_enrichment_processors__mutmut_7, 
    'x__config_create_event_enrichment_processors__mutmut_8': x__config_create_event_enrichment_processors__mutmut_8, 
    'x__config_create_event_enrichment_processors__mutmut_9': x__config_create_event_enrichment_processors__mutmut_9, 
    'x__config_create_event_enrichment_processors__mutmut_10': x__config_create_event_enrichment_processors__mutmut_10, 
    'x__config_create_event_enrichment_processors__mutmut_11': x__config_create_event_enrichment_processors__mutmut_11, 
    'x__config_create_event_enrichment_processors__mutmut_12': x__config_create_event_enrichment_processors__mutmut_12, 
    'x__config_create_event_enrichment_processors__mutmut_13': x__config_create_event_enrichment_processors__mutmut_13, 
    'x__config_create_event_enrichment_processors__mutmut_14': x__config_create_event_enrichment_processors__mutmut_14, 
    'x__config_create_event_enrichment_processors__mutmut_15': x__config_create_event_enrichment_processors__mutmut_15, 
    'x__config_create_event_enrichment_processors__mutmut_16': x__config_create_event_enrichment_processors__mutmut_16, 
    'x__config_create_event_enrichment_processors__mutmut_17': x__config_create_event_enrichment_processors__mutmut_17, 
    'x__config_create_event_enrichment_processors__mutmut_18': x__config_create_event_enrichment_processors__mutmut_18, 
    'x__config_create_event_enrichment_processors__mutmut_19': x__config_create_event_enrichment_processors__mutmut_19, 
    'x__config_create_event_enrichment_processors__mutmut_20': x__config_create_event_enrichment_processors__mutmut_20, 
    'x__config_create_event_enrichment_processors__mutmut_21': x__config_create_event_enrichment_processors__mutmut_21, 
    'x__config_create_event_enrichment_processors__mutmut_22': x__config_create_event_enrichment_processors__mutmut_22, 
    'x__config_create_event_enrichment_processors__mutmut_23': x__config_create_event_enrichment_processors__mutmut_23, 
    'x__config_create_event_enrichment_processors__mutmut_24': x__config_create_event_enrichment_processors__mutmut_24, 
    'x__config_create_event_enrichment_processors__mutmut_25': x__config_create_event_enrichment_processors__mutmut_25, 
    'x__config_create_event_enrichment_processors__mutmut_26': x__config_create_event_enrichment_processors__mutmut_26, 
    'x__config_create_event_enrichment_processors__mutmut_27': x__config_create_event_enrichment_processors__mutmut_27, 
    'x__config_create_event_enrichment_processors__mutmut_28': x__config_create_event_enrichment_processors__mutmut_28, 
    'x__config_create_event_enrichment_processors__mutmut_29': x__config_create_event_enrichment_processors__mutmut_29, 
    'x__config_create_event_enrichment_processors__mutmut_30': x__config_create_event_enrichment_processors__mutmut_30, 
    'x__config_create_event_enrichment_processors__mutmut_31': x__config_create_event_enrichment_processors__mutmut_31
}

def _config_create_event_enrichment_processors(*args, **kwargs):
    result = _mutmut_trampoline(x__config_create_event_enrichment_processors__mutmut_orig, x__config_create_event_enrichment_processors__mutmut_mutants, args, kwargs)
    return result 

_config_create_event_enrichment_processors.__signature__ = _mutmut_signature(x__config_create_event_enrichment_processors__mutmut_orig)
x__config_create_event_enrichment_processors__mutmut_orig.__name__ = 'x__config_create_event_enrichment_processors'


def x_set_reset_in_progress__mutmut_orig(in_progress: bool) -> None:
    """Set whether a reset is currently in progress.

    This prevents event enrichment from triggering during resets.
    """
    global _reset_in_progress
    _reset_in_progress = in_progress


def x_set_reset_in_progress__mutmut_1(in_progress: bool) -> None:
    """Set whether a reset is currently in progress.

    This prevents event enrichment from triggering during resets.
    """
    global _reset_in_progress
    _reset_in_progress = None

x_set_reset_in_progress__mutmut_mutants : ClassVar[MutantDict] = {
'x_set_reset_in_progress__mutmut_1': x_set_reset_in_progress__mutmut_1
}

def set_reset_in_progress(*args, **kwargs):
    result = _mutmut_trampoline(x_set_reset_in_progress__mutmut_orig, x_set_reset_in_progress__mutmut_mutants, args, kwargs)
    return result 

set_reset_in_progress.__signature__ = _mutmut_signature(x_set_reset_in_progress__mutmut_orig)
x_set_reset_in_progress__mutmut_orig.__name__ = 'x_set_reset_in_progress'


def x_reset_event_enrichment_state__mutmut_orig() -> None:
    """Reset event enrichment initialization state for testing.

    This should only be called during test cleanup to allow re-initialization
    in the next test.
    """
    global _event_enrichment_initialized
    _event_enrichment_initialized = False


def x_reset_event_enrichment_state__mutmut_1() -> None:
    """Reset event enrichment initialization state for testing.

    This should only be called during test cleanup to allow re-initialization
    in the next test.
    """
    global _event_enrichment_initialized
    _event_enrichment_initialized = None


def x_reset_event_enrichment_state__mutmut_2() -> None:
    """Reset event enrichment initialization state for testing.

    This should only be called during test cleanup to allow re-initialization
    in the next test.
    """
    global _event_enrichment_initialized
    _event_enrichment_initialized = True

x_reset_event_enrichment_state__mutmut_mutants : ClassVar[MutantDict] = {
'x_reset_event_enrichment_state__mutmut_1': x_reset_event_enrichment_state__mutmut_1, 
    'x_reset_event_enrichment_state__mutmut_2': x_reset_event_enrichment_state__mutmut_2
}

def reset_event_enrichment_state(*args, **kwargs):
    result = _mutmut_trampoline(x_reset_event_enrichment_state__mutmut_orig, x_reset_event_enrichment_state__mutmut_mutants, args, kwargs)
    return result 

reset_event_enrichment_state.__signature__ = _mutmut_signature(x_reset_event_enrichment_state__mutmut_orig)
x_reset_event_enrichment_state__mutmut_orig.__name__ = 'x_reset_event_enrichment_state'


def x__build_core_processors_list__mutmut_orig(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_1(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = None
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_2(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = None

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_3(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast(None, add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_4(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", None),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_5(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast(add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_6(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", ),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_7(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("XXStructlogProcessorXX", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_8(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("structlogprocessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_9(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("STRUCTLOGPROCESSOR", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_10(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(None)
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_11(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(None))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_12(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_13(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(None)

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_14(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(None))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_15(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled or not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_16(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_17(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(None)

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_18(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast(None, inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_19(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", None))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_20(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast(inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_21(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", ))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_22(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("XXStructlogProcessorXX", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_23(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("structlogprocessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_24(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("STRUCTLOGPROCESSOR", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_25(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = None
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_26(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=None,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_27(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=None,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_28(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=None,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_29(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_30(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_31(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_32(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(None)

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_33(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast(None, sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_34(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", None))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_35(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast(sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_36(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", ))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_37(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("XXStructlogProcessorXX", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_38(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("structlogprocessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_39(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("STRUCTLOGPROCESSOR", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_40(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(None)

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_41(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(None))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_42(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = None
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_43(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(None)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_44(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_45(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(None)

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_46(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast(None, otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_47(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", None))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_48(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast(otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_49(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", ))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_50(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("XXStructlogProcessorXX", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_51(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("structlogprocessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_52(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("STRUCTLOGPROCESSOR", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_53(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        None
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_54(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            None,
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_55(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            None,
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_56(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_57(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_58(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "XXStructlogProcessorXX",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_59(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "structlogprocessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_60(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "STRUCTLOGPROCESSOR",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_61(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=None,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_62(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=None,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_63(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=None,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_64(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_65(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_66(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_67(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        None
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_68(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = None
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_69(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=None,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_70(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=None,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_71(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=None,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_72(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=None,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_73(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=None,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_74(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=None,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_75(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=None,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_76(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=None,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_77(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_78(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_79(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_80(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_81(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_82(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_83(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_84(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_85(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(None)

    return processors


def x__build_core_processors_list__mutmut_86(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast(None, rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_87(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", None))

    return processors


def x__build_core_processors_list__mutmut_88(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast(rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_89(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", ))

    return processors


def x__build_core_processors_list__mutmut_90(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("XXStructlogProcessorXX", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_91(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("structlogprocessor", rate_limiter_processor))

    return processors


def x__build_core_processors_list__mutmut_92(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("STRUCTLOGPROCESSOR", rate_limiter_processor))

    return processors

x__build_core_processors_list__mutmut_mutants : ClassVar[MutantDict] = {
'x__build_core_processors_list__mutmut_1': x__build_core_processors_list__mutmut_1, 
    'x__build_core_processors_list__mutmut_2': x__build_core_processors_list__mutmut_2, 
    'x__build_core_processors_list__mutmut_3': x__build_core_processors_list__mutmut_3, 
    'x__build_core_processors_list__mutmut_4': x__build_core_processors_list__mutmut_4, 
    'x__build_core_processors_list__mutmut_5': x__build_core_processors_list__mutmut_5, 
    'x__build_core_processors_list__mutmut_6': x__build_core_processors_list__mutmut_6, 
    'x__build_core_processors_list__mutmut_7': x__build_core_processors_list__mutmut_7, 
    'x__build_core_processors_list__mutmut_8': x__build_core_processors_list__mutmut_8, 
    'x__build_core_processors_list__mutmut_9': x__build_core_processors_list__mutmut_9, 
    'x__build_core_processors_list__mutmut_10': x__build_core_processors_list__mutmut_10, 
    'x__build_core_processors_list__mutmut_11': x__build_core_processors_list__mutmut_11, 
    'x__build_core_processors_list__mutmut_12': x__build_core_processors_list__mutmut_12, 
    'x__build_core_processors_list__mutmut_13': x__build_core_processors_list__mutmut_13, 
    'x__build_core_processors_list__mutmut_14': x__build_core_processors_list__mutmut_14, 
    'x__build_core_processors_list__mutmut_15': x__build_core_processors_list__mutmut_15, 
    'x__build_core_processors_list__mutmut_16': x__build_core_processors_list__mutmut_16, 
    'x__build_core_processors_list__mutmut_17': x__build_core_processors_list__mutmut_17, 
    'x__build_core_processors_list__mutmut_18': x__build_core_processors_list__mutmut_18, 
    'x__build_core_processors_list__mutmut_19': x__build_core_processors_list__mutmut_19, 
    'x__build_core_processors_list__mutmut_20': x__build_core_processors_list__mutmut_20, 
    'x__build_core_processors_list__mutmut_21': x__build_core_processors_list__mutmut_21, 
    'x__build_core_processors_list__mutmut_22': x__build_core_processors_list__mutmut_22, 
    'x__build_core_processors_list__mutmut_23': x__build_core_processors_list__mutmut_23, 
    'x__build_core_processors_list__mutmut_24': x__build_core_processors_list__mutmut_24, 
    'x__build_core_processors_list__mutmut_25': x__build_core_processors_list__mutmut_25, 
    'x__build_core_processors_list__mutmut_26': x__build_core_processors_list__mutmut_26, 
    'x__build_core_processors_list__mutmut_27': x__build_core_processors_list__mutmut_27, 
    'x__build_core_processors_list__mutmut_28': x__build_core_processors_list__mutmut_28, 
    'x__build_core_processors_list__mutmut_29': x__build_core_processors_list__mutmut_29, 
    'x__build_core_processors_list__mutmut_30': x__build_core_processors_list__mutmut_30, 
    'x__build_core_processors_list__mutmut_31': x__build_core_processors_list__mutmut_31, 
    'x__build_core_processors_list__mutmut_32': x__build_core_processors_list__mutmut_32, 
    'x__build_core_processors_list__mutmut_33': x__build_core_processors_list__mutmut_33, 
    'x__build_core_processors_list__mutmut_34': x__build_core_processors_list__mutmut_34, 
    'x__build_core_processors_list__mutmut_35': x__build_core_processors_list__mutmut_35, 
    'x__build_core_processors_list__mutmut_36': x__build_core_processors_list__mutmut_36, 
    'x__build_core_processors_list__mutmut_37': x__build_core_processors_list__mutmut_37, 
    'x__build_core_processors_list__mutmut_38': x__build_core_processors_list__mutmut_38, 
    'x__build_core_processors_list__mutmut_39': x__build_core_processors_list__mutmut_39, 
    'x__build_core_processors_list__mutmut_40': x__build_core_processors_list__mutmut_40, 
    'x__build_core_processors_list__mutmut_41': x__build_core_processors_list__mutmut_41, 
    'x__build_core_processors_list__mutmut_42': x__build_core_processors_list__mutmut_42, 
    'x__build_core_processors_list__mutmut_43': x__build_core_processors_list__mutmut_43, 
    'x__build_core_processors_list__mutmut_44': x__build_core_processors_list__mutmut_44, 
    'x__build_core_processors_list__mutmut_45': x__build_core_processors_list__mutmut_45, 
    'x__build_core_processors_list__mutmut_46': x__build_core_processors_list__mutmut_46, 
    'x__build_core_processors_list__mutmut_47': x__build_core_processors_list__mutmut_47, 
    'x__build_core_processors_list__mutmut_48': x__build_core_processors_list__mutmut_48, 
    'x__build_core_processors_list__mutmut_49': x__build_core_processors_list__mutmut_49, 
    'x__build_core_processors_list__mutmut_50': x__build_core_processors_list__mutmut_50, 
    'x__build_core_processors_list__mutmut_51': x__build_core_processors_list__mutmut_51, 
    'x__build_core_processors_list__mutmut_52': x__build_core_processors_list__mutmut_52, 
    'x__build_core_processors_list__mutmut_53': x__build_core_processors_list__mutmut_53, 
    'x__build_core_processors_list__mutmut_54': x__build_core_processors_list__mutmut_54, 
    'x__build_core_processors_list__mutmut_55': x__build_core_processors_list__mutmut_55, 
    'x__build_core_processors_list__mutmut_56': x__build_core_processors_list__mutmut_56, 
    'x__build_core_processors_list__mutmut_57': x__build_core_processors_list__mutmut_57, 
    'x__build_core_processors_list__mutmut_58': x__build_core_processors_list__mutmut_58, 
    'x__build_core_processors_list__mutmut_59': x__build_core_processors_list__mutmut_59, 
    'x__build_core_processors_list__mutmut_60': x__build_core_processors_list__mutmut_60, 
    'x__build_core_processors_list__mutmut_61': x__build_core_processors_list__mutmut_61, 
    'x__build_core_processors_list__mutmut_62': x__build_core_processors_list__mutmut_62, 
    'x__build_core_processors_list__mutmut_63': x__build_core_processors_list__mutmut_63, 
    'x__build_core_processors_list__mutmut_64': x__build_core_processors_list__mutmut_64, 
    'x__build_core_processors_list__mutmut_65': x__build_core_processors_list__mutmut_65, 
    'x__build_core_processors_list__mutmut_66': x__build_core_processors_list__mutmut_66, 
    'x__build_core_processors_list__mutmut_67': x__build_core_processors_list__mutmut_67, 
    'x__build_core_processors_list__mutmut_68': x__build_core_processors_list__mutmut_68, 
    'x__build_core_processors_list__mutmut_69': x__build_core_processors_list__mutmut_69, 
    'x__build_core_processors_list__mutmut_70': x__build_core_processors_list__mutmut_70, 
    'x__build_core_processors_list__mutmut_71': x__build_core_processors_list__mutmut_71, 
    'x__build_core_processors_list__mutmut_72': x__build_core_processors_list__mutmut_72, 
    'x__build_core_processors_list__mutmut_73': x__build_core_processors_list__mutmut_73, 
    'x__build_core_processors_list__mutmut_74': x__build_core_processors_list__mutmut_74, 
    'x__build_core_processors_list__mutmut_75': x__build_core_processors_list__mutmut_75, 
    'x__build_core_processors_list__mutmut_76': x__build_core_processors_list__mutmut_76, 
    'x__build_core_processors_list__mutmut_77': x__build_core_processors_list__mutmut_77, 
    'x__build_core_processors_list__mutmut_78': x__build_core_processors_list__mutmut_78, 
    'x__build_core_processors_list__mutmut_79': x__build_core_processors_list__mutmut_79, 
    'x__build_core_processors_list__mutmut_80': x__build_core_processors_list__mutmut_80, 
    'x__build_core_processors_list__mutmut_81': x__build_core_processors_list__mutmut_81, 
    'x__build_core_processors_list__mutmut_82': x__build_core_processors_list__mutmut_82, 
    'x__build_core_processors_list__mutmut_83': x__build_core_processors_list__mutmut_83, 
    'x__build_core_processors_list__mutmut_84': x__build_core_processors_list__mutmut_84, 
    'x__build_core_processors_list__mutmut_85': x__build_core_processors_list__mutmut_85, 
    'x__build_core_processors_list__mutmut_86': x__build_core_processors_list__mutmut_86, 
    'x__build_core_processors_list__mutmut_87': x__build_core_processors_list__mutmut_87, 
    'x__build_core_processors_list__mutmut_88': x__build_core_processors_list__mutmut_88, 
    'x__build_core_processors_list__mutmut_89': x__build_core_processors_list__mutmut_89, 
    'x__build_core_processors_list__mutmut_90': x__build_core_processors_list__mutmut_90, 
    'x__build_core_processors_list__mutmut_91': x__build_core_processors_list__mutmut_91, 
    'x__build_core_processors_list__mutmut_92': x__build_core_processors_list__mutmut_92
}

def _build_core_processors_list(*args, **kwargs):
    result = _mutmut_trampoline(x__build_core_processors_list__mutmut_orig, x__build_core_processors_list__mutmut_mutants, args, kwargs)
    return result 

_build_core_processors_list.__signature__ = _mutmut_signature(x__build_core_processors_list__mutmut_orig)
x__build_core_processors_list__mutmut_orig.__name__ = 'x__build_core_processors_list'


def x__config_create_json_formatter_processors__mutmut_orig() -> list[StructlogProcessor]:
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=json_dumps, sort_keys=False),
    ]


def x__config_create_json_formatter_processors__mutmut_1() -> list[StructlogProcessor]:
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=None, sort_keys=False),
    ]


def x__config_create_json_formatter_processors__mutmut_2() -> list[StructlogProcessor]:
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=json_dumps, sort_keys=None),
    ]


def x__config_create_json_formatter_processors__mutmut_3() -> list[StructlogProcessor]:
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(sort_keys=False),
    ]


def x__config_create_json_formatter_processors__mutmut_4() -> list[StructlogProcessor]:
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=json_dumps, ),
    ]


def x__config_create_json_formatter_processors__mutmut_5() -> list[StructlogProcessor]:
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=json_dumps, sort_keys=True),
    ]

x__config_create_json_formatter_processors__mutmut_mutants : ClassVar[MutantDict] = {
'x__config_create_json_formatter_processors__mutmut_1': x__config_create_json_formatter_processors__mutmut_1, 
    'x__config_create_json_formatter_processors__mutmut_2': x__config_create_json_formatter_processors__mutmut_2, 
    'x__config_create_json_formatter_processors__mutmut_3': x__config_create_json_formatter_processors__mutmut_3, 
    'x__config_create_json_formatter_processors__mutmut_4': x__config_create_json_formatter_processors__mutmut_4, 
    'x__config_create_json_formatter_processors__mutmut_5': x__config_create_json_formatter_processors__mutmut_5
}

def _config_create_json_formatter_processors(*args, **kwargs):
    result = _mutmut_trampoline(x__config_create_json_formatter_processors__mutmut_orig, x__config_create_json_formatter_processors__mutmut_mutants, args, kwargs)
    return result 

_config_create_json_formatter_processors.__signature__ = _mutmut_signature(x__config_create_json_formatter_processors__mutmut_orig)
x__config_create_json_formatter_processors__mutmut_orig.__name__ = 'x__config_create_json_formatter_processors'


def x__config_create_keyvalue_formatter_processors__mutmut_orig(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_1(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop(None, None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_2(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop(None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_3(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", )
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_4(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("XXlogger_nameXX", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_5(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("LOGGER_NAME", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_6(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = None
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_7(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") or output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_8(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(None, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_9(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, None) and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_10(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr("isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_11(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, ) and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_12(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "XXisattyXX") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_13(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "ISATTY") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_14(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast(None, pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_15(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", None),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_16(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast(pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_17(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", ),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_18(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("XXStructlogProcessorXX", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_19(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("structlogprocessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_20(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("STRUCTLOGPROCESSOR", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_21(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=None, exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_22(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=None),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_23(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(exception_formatter=structlog.dev.plain_traceback),
    ]


def x__config_create_keyvalue_formatter_processors__mutmut_24(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, ),
    ]

x__config_create_keyvalue_formatter_processors__mutmut_mutants : ClassVar[MutantDict] = {
'x__config_create_keyvalue_formatter_processors__mutmut_1': x__config_create_keyvalue_formatter_processors__mutmut_1, 
    'x__config_create_keyvalue_formatter_processors__mutmut_2': x__config_create_keyvalue_formatter_processors__mutmut_2, 
    'x__config_create_keyvalue_formatter_processors__mutmut_3': x__config_create_keyvalue_formatter_processors__mutmut_3, 
    'x__config_create_keyvalue_formatter_processors__mutmut_4': x__config_create_keyvalue_formatter_processors__mutmut_4, 
    'x__config_create_keyvalue_formatter_processors__mutmut_5': x__config_create_keyvalue_formatter_processors__mutmut_5, 
    'x__config_create_keyvalue_formatter_processors__mutmut_6': x__config_create_keyvalue_formatter_processors__mutmut_6, 
    'x__config_create_keyvalue_formatter_processors__mutmut_7': x__config_create_keyvalue_formatter_processors__mutmut_7, 
    'x__config_create_keyvalue_formatter_processors__mutmut_8': x__config_create_keyvalue_formatter_processors__mutmut_8, 
    'x__config_create_keyvalue_formatter_processors__mutmut_9': x__config_create_keyvalue_formatter_processors__mutmut_9, 
    'x__config_create_keyvalue_formatter_processors__mutmut_10': x__config_create_keyvalue_formatter_processors__mutmut_10, 
    'x__config_create_keyvalue_formatter_processors__mutmut_11': x__config_create_keyvalue_formatter_processors__mutmut_11, 
    'x__config_create_keyvalue_formatter_processors__mutmut_12': x__config_create_keyvalue_formatter_processors__mutmut_12, 
    'x__config_create_keyvalue_formatter_processors__mutmut_13': x__config_create_keyvalue_formatter_processors__mutmut_13, 
    'x__config_create_keyvalue_formatter_processors__mutmut_14': x__config_create_keyvalue_formatter_processors__mutmut_14, 
    'x__config_create_keyvalue_formatter_processors__mutmut_15': x__config_create_keyvalue_formatter_processors__mutmut_15, 
    'x__config_create_keyvalue_formatter_processors__mutmut_16': x__config_create_keyvalue_formatter_processors__mutmut_16, 
    'x__config_create_keyvalue_formatter_processors__mutmut_17': x__config_create_keyvalue_formatter_processors__mutmut_17, 
    'x__config_create_keyvalue_formatter_processors__mutmut_18': x__config_create_keyvalue_formatter_processors__mutmut_18, 
    'x__config_create_keyvalue_formatter_processors__mutmut_19': x__config_create_keyvalue_formatter_processors__mutmut_19, 
    'x__config_create_keyvalue_formatter_processors__mutmut_20': x__config_create_keyvalue_formatter_processors__mutmut_20, 
    'x__config_create_keyvalue_formatter_processors__mutmut_21': x__config_create_keyvalue_formatter_processors__mutmut_21, 
    'x__config_create_keyvalue_formatter_processors__mutmut_22': x__config_create_keyvalue_formatter_processors__mutmut_22, 
    'x__config_create_keyvalue_formatter_processors__mutmut_23': x__config_create_keyvalue_formatter_processors__mutmut_23, 
    'x__config_create_keyvalue_formatter_processors__mutmut_24': x__config_create_keyvalue_formatter_processors__mutmut_24
}

def _config_create_keyvalue_formatter_processors(*args, **kwargs):
    result = _mutmut_trampoline(x__config_create_keyvalue_formatter_processors__mutmut_orig, x__config_create_keyvalue_formatter_processors__mutmut_mutants, args, kwargs)
    return result 

_config_create_keyvalue_formatter_processors.__signature__ = _mutmut_signature(x__config_create_keyvalue_formatter_processors__mutmut_orig)
x__config_create_keyvalue_formatter_processors__mutmut_orig.__name__ = 'x__config_create_keyvalue_formatter_processors'


def x__build_formatter_processors_list__mutmut_orig(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_1(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_2(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_3(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_4(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "XXjsonXX":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_5(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "JSON":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_6(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "XXkey_valueXX":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_7(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "KEY_VALUE":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_8(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(None)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_9(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = None
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_10(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                None,
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


def x__build_formatter_processors_list__mutmut_11(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(None)

x__build_formatter_processors_list__mutmut_mutants : ClassVar[MutantDict] = {
'x__build_formatter_processors_list__mutmut_1': x__build_formatter_processors_list__mutmut_1, 
    'x__build_formatter_processors_list__mutmut_2': x__build_formatter_processors_list__mutmut_2, 
    'x__build_formatter_processors_list__mutmut_3': x__build_formatter_processors_list__mutmut_3, 
    'x__build_formatter_processors_list__mutmut_4': x__build_formatter_processors_list__mutmut_4, 
    'x__build_formatter_processors_list__mutmut_5': x__build_formatter_processors_list__mutmut_5, 
    'x__build_formatter_processors_list__mutmut_6': x__build_formatter_processors_list__mutmut_6, 
    'x__build_formatter_processors_list__mutmut_7': x__build_formatter_processors_list__mutmut_7, 
    'x__build_formatter_processors_list__mutmut_8': x__build_formatter_processors_list__mutmut_8, 
    'x__build_formatter_processors_list__mutmut_9': x__build_formatter_processors_list__mutmut_9, 
    'x__build_formatter_processors_list__mutmut_10': x__build_formatter_processors_list__mutmut_10, 
    'x__build_formatter_processors_list__mutmut_11': x__build_formatter_processors_list__mutmut_11
}

def _build_formatter_processors_list(*args, **kwargs):
    result = _mutmut_trampoline(x__build_formatter_processors_list__mutmut_orig, x__build_formatter_processors_list__mutmut_mutants, args, kwargs)
    return result 

_build_formatter_processors_list.__signature__ = _mutmut_signature(x__build_formatter_processors_list__mutmut_orig)
x__build_formatter_processors_list__mutmut_orig.__name__ = 'x__build_formatter_processors_list'


# <3 🧱🤝📝🪄
