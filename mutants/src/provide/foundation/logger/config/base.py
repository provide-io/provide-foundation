# provide/foundation/logger/config/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# base.py
#
import os
import sys
from typing import Any

"""Base configuration utilities for Foundation logger."""
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


def x_get_config_logger__mutmut_orig() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_1() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = None
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_2() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").upper()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_3() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv(None, "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_4() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", None).lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_5() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_6() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv(
            "FOUNDATION_LOG_OUTPUT",
        ).lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_7() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("XXFOUNDATION_LOG_OUTPUTXX", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_8() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("foundation_log_output", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_9() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "XXstderrXX").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_10() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "STDERR").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_11() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = None
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_12() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(None)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_13() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = None

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_14() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = None
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_15() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=None,
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_16() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=None,
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_17() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=None,
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_18() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=None,
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_19() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_20() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_21() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_22() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_23() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get(None, [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_24() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", None),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_25() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get([structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_26() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get(
                "processors",
            ),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_27() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("XXprocessorsXX", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_28() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("PROCESSORS", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_29() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=None),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_30() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get(None, structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_31() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", None),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_32() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get(structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_33() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get(
                "wrapper_class",
            ),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_34() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("XXwrapper_classXX", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_35() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("WRAPPER_CLASS", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_36() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get(None, True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_37() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", None),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_38() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get(True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_39() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get(
                "cache_logger_on_first_use",
            ),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_40() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("XXcache_logger_on_first_useXX", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_41() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("CACHE_LOGGER_ON_FIRST_USE", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_42() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", False),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_43() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=None,
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_44() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=None,
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_45() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=None,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_46() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=None,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_47() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_48() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_49() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_50() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_51() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=None),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_52() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=False,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


def x_get_config_logger__mutmut_53() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name=None)


def x_get_config_logger__mutmut_54() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="XXprovide.foundation.logger.configXX")


def x_get_config_logger__mutmut_55() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="PROVIDE.FOUNDATION.LOGGER.CONFIG")


x_get_config_logger__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_config_logger__mutmut_1": x_get_config_logger__mutmut_1,
    "x_get_config_logger__mutmut_2": x_get_config_logger__mutmut_2,
    "x_get_config_logger__mutmut_3": x_get_config_logger__mutmut_3,
    "x_get_config_logger__mutmut_4": x_get_config_logger__mutmut_4,
    "x_get_config_logger__mutmut_5": x_get_config_logger__mutmut_5,
    "x_get_config_logger__mutmut_6": x_get_config_logger__mutmut_6,
    "x_get_config_logger__mutmut_7": x_get_config_logger__mutmut_7,
    "x_get_config_logger__mutmut_8": x_get_config_logger__mutmut_8,
    "x_get_config_logger__mutmut_9": x_get_config_logger__mutmut_9,
    "x_get_config_logger__mutmut_10": x_get_config_logger__mutmut_10,
    "x_get_config_logger__mutmut_11": x_get_config_logger__mutmut_11,
    "x_get_config_logger__mutmut_12": x_get_config_logger__mutmut_12,
    "x_get_config_logger__mutmut_13": x_get_config_logger__mutmut_13,
    "x_get_config_logger__mutmut_14": x_get_config_logger__mutmut_14,
    "x_get_config_logger__mutmut_15": x_get_config_logger__mutmut_15,
    "x_get_config_logger__mutmut_16": x_get_config_logger__mutmut_16,
    "x_get_config_logger__mutmut_17": x_get_config_logger__mutmut_17,
    "x_get_config_logger__mutmut_18": x_get_config_logger__mutmut_18,
    "x_get_config_logger__mutmut_19": x_get_config_logger__mutmut_19,
    "x_get_config_logger__mutmut_20": x_get_config_logger__mutmut_20,
    "x_get_config_logger__mutmut_21": x_get_config_logger__mutmut_21,
    "x_get_config_logger__mutmut_22": x_get_config_logger__mutmut_22,
    "x_get_config_logger__mutmut_23": x_get_config_logger__mutmut_23,
    "x_get_config_logger__mutmut_24": x_get_config_logger__mutmut_24,
    "x_get_config_logger__mutmut_25": x_get_config_logger__mutmut_25,
    "x_get_config_logger__mutmut_26": x_get_config_logger__mutmut_26,
    "x_get_config_logger__mutmut_27": x_get_config_logger__mutmut_27,
    "x_get_config_logger__mutmut_28": x_get_config_logger__mutmut_28,
    "x_get_config_logger__mutmut_29": x_get_config_logger__mutmut_29,
    "x_get_config_logger__mutmut_30": x_get_config_logger__mutmut_30,
    "x_get_config_logger__mutmut_31": x_get_config_logger__mutmut_31,
    "x_get_config_logger__mutmut_32": x_get_config_logger__mutmut_32,
    "x_get_config_logger__mutmut_33": x_get_config_logger__mutmut_33,
    "x_get_config_logger__mutmut_34": x_get_config_logger__mutmut_34,
    "x_get_config_logger__mutmut_35": x_get_config_logger__mutmut_35,
    "x_get_config_logger__mutmut_36": x_get_config_logger__mutmut_36,
    "x_get_config_logger__mutmut_37": x_get_config_logger__mutmut_37,
    "x_get_config_logger__mutmut_38": x_get_config_logger__mutmut_38,
    "x_get_config_logger__mutmut_39": x_get_config_logger__mutmut_39,
    "x_get_config_logger__mutmut_40": x_get_config_logger__mutmut_40,
    "x_get_config_logger__mutmut_41": x_get_config_logger__mutmut_41,
    "x_get_config_logger__mutmut_42": x_get_config_logger__mutmut_42,
    "x_get_config_logger__mutmut_43": x_get_config_logger__mutmut_43,
    "x_get_config_logger__mutmut_44": x_get_config_logger__mutmut_44,
    "x_get_config_logger__mutmut_45": x_get_config_logger__mutmut_45,
    "x_get_config_logger__mutmut_46": x_get_config_logger__mutmut_46,
    "x_get_config_logger__mutmut_47": x_get_config_logger__mutmut_47,
    "x_get_config_logger__mutmut_48": x_get_config_logger__mutmut_48,
    "x_get_config_logger__mutmut_49": x_get_config_logger__mutmut_49,
    "x_get_config_logger__mutmut_50": x_get_config_logger__mutmut_50,
    "x_get_config_logger__mutmut_51": x_get_config_logger__mutmut_51,
    "x_get_config_logger__mutmut_52": x_get_config_logger__mutmut_52,
    "x_get_config_logger__mutmut_53": x_get_config_logger__mutmut_53,
    "x_get_config_logger__mutmut_54": x_get_config_logger__mutmut_54,
    "x_get_config_logger__mutmut_55": x_get_config_logger__mutmut_55,
}


def get_config_logger(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_config_logger__mutmut_orig, x_get_config_logger__mutmut_mutants, args, kwargs
    )
    return result


get_config_logger.__signature__ = _mutmut_signature(x_get_config_logger__mutmut_orig)
x_get_config_logger__mutmut_orig.__name__ = "x_get_config_logger"


# <3 🧱🤝📝🪄
