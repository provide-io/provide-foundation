# provide/foundation/logger/setup/processors.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# processors.py
#
from typing import Any, TextIO, cast

import structlog

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.logger.processors import (
    _build_core_processors_list,
    _build_formatter_processors_list,
)

"""Processor chain building for Foundation Telemetry.
Handles the assembly of structlog processor chains including emoji processing.
"""
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


def x_build_complete_processor_chain__mutmut_orig(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("list[Any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_1(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = None
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("list[Any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_2(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(None)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("list[Any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_3(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = None
    return cast("list[Any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_4(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(None, log_stream)
    return cast("list[Any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_5(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, None)
    return cast("list[Any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_6(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(log_stream)
    return cast("list[Any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_7(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, )
    return cast("list[Any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_8(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast(None, core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_9(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("list[Any]", None)


def x_build_complete_processor_chain__mutmut_10(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast(core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_11(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("list[Any]", )


def x_build_complete_processor_chain__mutmut_12(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("XXlist[Any]XX", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_13(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("list[any]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_14(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("LIST[ANY]", core_processors + formatter_processors)


def x_build_complete_processor_chain__mutmut_15(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("list[Any]", core_processors - formatter_processors)

x_build_complete_processor_chain__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_complete_processor_chain__mutmut_1': x_build_complete_processor_chain__mutmut_1, 
    'x_build_complete_processor_chain__mutmut_2': x_build_complete_processor_chain__mutmut_2, 
    'x_build_complete_processor_chain__mutmut_3': x_build_complete_processor_chain__mutmut_3, 
    'x_build_complete_processor_chain__mutmut_4': x_build_complete_processor_chain__mutmut_4, 
    'x_build_complete_processor_chain__mutmut_5': x_build_complete_processor_chain__mutmut_5, 
    'x_build_complete_processor_chain__mutmut_6': x_build_complete_processor_chain__mutmut_6, 
    'x_build_complete_processor_chain__mutmut_7': x_build_complete_processor_chain__mutmut_7, 
    'x_build_complete_processor_chain__mutmut_8': x_build_complete_processor_chain__mutmut_8, 
    'x_build_complete_processor_chain__mutmut_9': x_build_complete_processor_chain__mutmut_9, 
    'x_build_complete_processor_chain__mutmut_10': x_build_complete_processor_chain__mutmut_10, 
    'x_build_complete_processor_chain__mutmut_11': x_build_complete_processor_chain__mutmut_11, 
    'x_build_complete_processor_chain__mutmut_12': x_build_complete_processor_chain__mutmut_12, 
    'x_build_complete_processor_chain__mutmut_13': x_build_complete_processor_chain__mutmut_13, 
    'x_build_complete_processor_chain__mutmut_14': x_build_complete_processor_chain__mutmut_14, 
    'x_build_complete_processor_chain__mutmut_15': x_build_complete_processor_chain__mutmut_15
}

def build_complete_processor_chain(*args, **kwargs):
    result = _mutmut_trampoline(x_build_complete_processor_chain__mutmut_orig, x_build_complete_processor_chain__mutmut_mutants, args, kwargs)
    return result 

build_complete_processor_chain.__signature__ = _mutmut_signature(x_build_complete_processor_chain__mutmut_orig)
x_build_complete_processor_chain__mutmut_orig.__name__ = 'x_build_complete_processor_chain'


def x_apply_structlog_configuration__mutmut_orig(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_1(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = None
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_2(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = None

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_3(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_4(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=None,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_5(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=None,
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_6(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=None,
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_7(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=None,
    )


def x_apply_structlog_configuration__mutmut_8(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_9(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_10(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_11(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        )


def x_apply_structlog_configuration__mutmut_12(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=None),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_13(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast(None, structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_14(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", None),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_15(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast(structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_16(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", ),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_17(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("XXtype[structlog.types.BindableLogger]XX", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_18(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.bindablelogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def x_apply_structlog_configuration__mutmut_19(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("TYPE[STRUCTLOG.TYPES.BINDABLELOGGER]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )

x_apply_structlog_configuration__mutmut_mutants : ClassVar[MutantDict] = {
'x_apply_structlog_configuration__mutmut_1': x_apply_structlog_configuration__mutmut_1, 
    'x_apply_structlog_configuration__mutmut_2': x_apply_structlog_configuration__mutmut_2, 
    'x_apply_structlog_configuration__mutmut_3': x_apply_structlog_configuration__mutmut_3, 
    'x_apply_structlog_configuration__mutmut_4': x_apply_structlog_configuration__mutmut_4, 
    'x_apply_structlog_configuration__mutmut_5': x_apply_structlog_configuration__mutmut_5, 
    'x_apply_structlog_configuration__mutmut_6': x_apply_structlog_configuration__mutmut_6, 
    'x_apply_structlog_configuration__mutmut_7': x_apply_structlog_configuration__mutmut_7, 
    'x_apply_structlog_configuration__mutmut_8': x_apply_structlog_configuration__mutmut_8, 
    'x_apply_structlog_configuration__mutmut_9': x_apply_structlog_configuration__mutmut_9, 
    'x_apply_structlog_configuration__mutmut_10': x_apply_structlog_configuration__mutmut_10, 
    'x_apply_structlog_configuration__mutmut_11': x_apply_structlog_configuration__mutmut_11, 
    'x_apply_structlog_configuration__mutmut_12': x_apply_structlog_configuration__mutmut_12, 
    'x_apply_structlog_configuration__mutmut_13': x_apply_structlog_configuration__mutmut_13, 
    'x_apply_structlog_configuration__mutmut_14': x_apply_structlog_configuration__mutmut_14, 
    'x_apply_structlog_configuration__mutmut_15': x_apply_structlog_configuration__mutmut_15, 
    'x_apply_structlog_configuration__mutmut_16': x_apply_structlog_configuration__mutmut_16, 
    'x_apply_structlog_configuration__mutmut_17': x_apply_structlog_configuration__mutmut_17, 
    'x_apply_structlog_configuration__mutmut_18': x_apply_structlog_configuration__mutmut_18, 
    'x_apply_structlog_configuration__mutmut_19': x_apply_structlog_configuration__mutmut_19
}

def apply_structlog_configuration(*args, **kwargs):
    result = _mutmut_trampoline(x_apply_structlog_configuration__mutmut_orig, x_apply_structlog_configuration__mutmut_mutants, args, kwargs)
    return result 

apply_structlog_configuration.__signature__ = _mutmut_signature(x_apply_structlog_configuration__mutmut_orig)
x_apply_structlog_configuration__mutmut_orig.__name__ = 'x_apply_structlog_configuration'


def x_configure_structlog_output__mutmut_orig(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(config, log_stream)
    apply_structlog_configuration(processors, log_stream)


def x_configure_structlog_output__mutmut_1(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = None
    apply_structlog_configuration(processors, log_stream)


def x_configure_structlog_output__mutmut_2(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(None, log_stream)
    apply_structlog_configuration(processors, log_stream)


def x_configure_structlog_output__mutmut_3(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(config, None)
    apply_structlog_configuration(processors, log_stream)


def x_configure_structlog_output__mutmut_4(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(log_stream)
    apply_structlog_configuration(processors, log_stream)


def x_configure_structlog_output__mutmut_5(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(config, )
    apply_structlog_configuration(processors, log_stream)


def x_configure_structlog_output__mutmut_6(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(config, log_stream)
    apply_structlog_configuration(None, log_stream)


def x_configure_structlog_output__mutmut_7(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(config, log_stream)
    apply_structlog_configuration(processors, None)


def x_configure_structlog_output__mutmut_8(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(config, log_stream)
    apply_structlog_configuration(log_stream)


def x_configure_structlog_output__mutmut_9(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(config, log_stream)
    apply_structlog_configuration(processors, )

x_configure_structlog_output__mutmut_mutants : ClassVar[MutantDict] = {
'x_configure_structlog_output__mutmut_1': x_configure_structlog_output__mutmut_1, 
    'x_configure_structlog_output__mutmut_2': x_configure_structlog_output__mutmut_2, 
    'x_configure_structlog_output__mutmut_3': x_configure_structlog_output__mutmut_3, 
    'x_configure_structlog_output__mutmut_4': x_configure_structlog_output__mutmut_4, 
    'x_configure_structlog_output__mutmut_5': x_configure_structlog_output__mutmut_5, 
    'x_configure_structlog_output__mutmut_6': x_configure_structlog_output__mutmut_6, 
    'x_configure_structlog_output__mutmut_7': x_configure_structlog_output__mutmut_7, 
    'x_configure_structlog_output__mutmut_8': x_configure_structlog_output__mutmut_8, 
    'x_configure_structlog_output__mutmut_9': x_configure_structlog_output__mutmut_9
}

def configure_structlog_output(*args, **kwargs):
    result = _mutmut_trampoline(x_configure_structlog_output__mutmut_orig, x_configure_structlog_output__mutmut_mutants, args, kwargs)
    return result 

configure_structlog_output.__signature__ = _mutmut_signature(x_configure_structlog_output__mutmut_orig)
x_configure_structlog_output__mutmut_orig.__name__ = 'x_configure_structlog_output'


def x_handle_globally_disabled_setup__mutmut_orig() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def x_handle_globally_disabled_setup__mutmut_1() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        processors=None,
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def x_handle_globally_disabled_setup__mutmut_2() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        processors=[],
        logger_factory=None,
        cache_logger_on_first_use=True,
    )


def x_handle_globally_disabled_setup__mutmut_3() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=None,
    )


def x_handle_globally_disabled_setup__mutmut_4() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def x_handle_globally_disabled_setup__mutmut_5() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        processors=[],
        cache_logger_on_first_use=True,
    )


def x_handle_globally_disabled_setup__mutmut_6() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        )


def x_handle_globally_disabled_setup__mutmut_7() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=False,
    )

x_handle_globally_disabled_setup__mutmut_mutants : ClassVar[MutantDict] = {
'x_handle_globally_disabled_setup__mutmut_1': x_handle_globally_disabled_setup__mutmut_1, 
    'x_handle_globally_disabled_setup__mutmut_2': x_handle_globally_disabled_setup__mutmut_2, 
    'x_handle_globally_disabled_setup__mutmut_3': x_handle_globally_disabled_setup__mutmut_3, 
    'x_handle_globally_disabled_setup__mutmut_4': x_handle_globally_disabled_setup__mutmut_4, 
    'x_handle_globally_disabled_setup__mutmut_5': x_handle_globally_disabled_setup__mutmut_5, 
    'x_handle_globally_disabled_setup__mutmut_6': x_handle_globally_disabled_setup__mutmut_6, 
    'x_handle_globally_disabled_setup__mutmut_7': x_handle_globally_disabled_setup__mutmut_7
}

def handle_globally_disabled_setup(*args, **kwargs):
    result = _mutmut_trampoline(x_handle_globally_disabled_setup__mutmut_orig, x_handle_globally_disabled_setup__mutmut_mutants, args, kwargs)
    return result 

handle_globally_disabled_setup.__signature__ = _mutmut_signature(x_handle_globally_disabled_setup__mutmut_orig)
x_handle_globally_disabled_setup__mutmut_orig.__name__ = 'x_handle_globally_disabled_setup'


# <3 🧱🤝📝🪄
