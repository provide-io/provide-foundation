# provide/foundation/testmode/orchestration.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# orchestration.py
#
from typing import Any

"""Foundation Test Reset Orchestration.

This module provides the complete reset orchestration for Foundation's
internal state. It knows the proper reset order and handles Foundation-specific
concerns like OpenTelemetry providers and environment variables.

This is Foundation-internal knowledge that should be owned by Foundation,
not by external testing frameworks.
"""

# Global flags to prevent recursive resets
_reset_in_progress = False
_reset_for_testing_in_progress = False
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


def x__reset_otel_once_flag__mutmut_orig(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_1(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(None, "_done"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_2(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, None):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_3(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr("_done"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_4(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(
        once_obj,
    ):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_5(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "XX_doneXX"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_6(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_DONE"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_7(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = None
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_8(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = True
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_9(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(None, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_10(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(once_obj, None):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_11(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr("_lock"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_12(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(
        once_obj,
    ):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_13(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(once_obj, "XX_lockXX"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_14(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(once_obj, "_LOCK"):
        with once_obj._lock:
            once_obj._done = False


def x__reset_otel_once_flag__mutmut_15(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = None


def x__reset_otel_once_flag__mutmut_16(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = True


x__reset_otel_once_flag__mutmut_mutants: ClassVar[MutantDict] = {
    "x__reset_otel_once_flag__mutmut_1": x__reset_otel_once_flag__mutmut_1,
    "x__reset_otel_once_flag__mutmut_2": x__reset_otel_once_flag__mutmut_2,
    "x__reset_otel_once_flag__mutmut_3": x__reset_otel_once_flag__mutmut_3,
    "x__reset_otel_once_flag__mutmut_4": x__reset_otel_once_flag__mutmut_4,
    "x__reset_otel_once_flag__mutmut_5": x__reset_otel_once_flag__mutmut_5,
    "x__reset_otel_once_flag__mutmut_6": x__reset_otel_once_flag__mutmut_6,
    "x__reset_otel_once_flag__mutmut_7": x__reset_otel_once_flag__mutmut_7,
    "x__reset_otel_once_flag__mutmut_8": x__reset_otel_once_flag__mutmut_8,
    "x__reset_otel_once_flag__mutmut_9": x__reset_otel_once_flag__mutmut_9,
    "x__reset_otel_once_flag__mutmut_10": x__reset_otel_once_flag__mutmut_10,
    "x__reset_otel_once_flag__mutmut_11": x__reset_otel_once_flag__mutmut_11,
    "x__reset_otel_once_flag__mutmut_12": x__reset_otel_once_flag__mutmut_12,
    "x__reset_otel_once_flag__mutmut_13": x__reset_otel_once_flag__mutmut_13,
    "x__reset_otel_once_flag__mutmut_14": x__reset_otel_once_flag__mutmut_14,
    "x__reset_otel_once_flag__mutmut_15": x__reset_otel_once_flag__mutmut_15,
    "x__reset_otel_once_flag__mutmut_16": x__reset_otel_once_flag__mutmut_16,
}


def _reset_otel_once_flag(*args, **kwargs):
    result = _mutmut_trampoline(
        x__reset_otel_once_flag__mutmut_orig, x__reset_otel_once_flag__mutmut_mutants, args, kwargs
    )
    return result


_reset_otel_once_flag.__signature__ = _mutmut_signature(x__reset_otel_once_flag__mutmut_orig)
x__reset_otel_once_flag__mutmut_orig.__name__ = "x__reset_otel_once_flag"


def x__reset_tracer_provider__mutmut_orig() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, "_TRACER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_tracer_provider__mutmut_1() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(None, "_TRACER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_tracer_provider__mutmut_2() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, None):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_tracer_provider__mutmut_3() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr("_TRACER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_tracer_provider__mutmut_4() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(
            otel_trace,
        ):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_tracer_provider__mutmut_5() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, "XX_TRACER_PROVIDER_SET_ONCEXX"):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_tracer_provider__mutmut_6() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, "_tracer_provider_set_once"):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_tracer_provider__mutmut_7() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, "_TRACER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(None)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_tracer_provider__mutmut_8() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, "_TRACER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(None)
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


x__reset_tracer_provider__mutmut_mutants: ClassVar[MutantDict] = {
    "x__reset_tracer_provider__mutmut_1": x__reset_tracer_provider__mutmut_1,
    "x__reset_tracer_provider__mutmut_2": x__reset_tracer_provider__mutmut_2,
    "x__reset_tracer_provider__mutmut_3": x__reset_tracer_provider__mutmut_3,
    "x__reset_tracer_provider__mutmut_4": x__reset_tracer_provider__mutmut_4,
    "x__reset_tracer_provider__mutmut_5": x__reset_tracer_provider__mutmut_5,
    "x__reset_tracer_provider__mutmut_6": x__reset_tracer_provider__mutmut_6,
    "x__reset_tracer_provider__mutmut_7": x__reset_tracer_provider__mutmut_7,
    "x__reset_tracer_provider__mutmut_8": x__reset_tracer_provider__mutmut_8,
}


def _reset_tracer_provider(*args, **kwargs):
    result = _mutmut_trampoline(
        x__reset_tracer_provider__mutmut_orig, x__reset_tracer_provider__mutmut_mutants, args, kwargs
    )
    return result


_reset_tracer_provider.__signature__ = _mutmut_signature(x__reset_tracer_provider__mutmut_orig)
x__reset_tracer_provider__mutmut_orig.__name__ = "x__reset_tracer_provider"


def x__reset_meter_provider__mutmut_orig() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, "_METER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_meter_provider__mutmut_1() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(None, "_METER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_meter_provider__mutmut_2() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, None):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_meter_provider__mutmut_3() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr("_METER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_meter_provider__mutmut_4() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(
            otel_metrics_internal,
        ):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_meter_provider__mutmut_5() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, "XX_METER_PROVIDER_SET_ONCEXX"):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_meter_provider__mutmut_6() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, "_meter_provider_set_once"):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_meter_provider__mutmut_7() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, "_METER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(None)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def x__reset_meter_provider__mutmut_8() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, "_METER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(None)
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


x__reset_meter_provider__mutmut_mutants: ClassVar[MutantDict] = {
    "x__reset_meter_provider__mutmut_1": x__reset_meter_provider__mutmut_1,
    "x__reset_meter_provider__mutmut_2": x__reset_meter_provider__mutmut_2,
    "x__reset_meter_provider__mutmut_3": x__reset_meter_provider__mutmut_3,
    "x__reset_meter_provider__mutmut_4": x__reset_meter_provider__mutmut_4,
    "x__reset_meter_provider__mutmut_5": x__reset_meter_provider__mutmut_5,
    "x__reset_meter_provider__mutmut_6": x__reset_meter_provider__mutmut_6,
    "x__reset_meter_provider__mutmut_7": x__reset_meter_provider__mutmut_7,
    "x__reset_meter_provider__mutmut_8": x__reset_meter_provider__mutmut_8,
}


def _reset_meter_provider(*args, **kwargs):
    result = _mutmut_trampoline(
        x__reset_meter_provider__mutmut_orig, x__reset_meter_provider__mutmut_mutants, args, kwargs
    )
    return result


_reset_meter_provider.__signature__ = _mutmut_signature(x__reset_meter_provider__mutmut_orig)
x__reset_meter_provider__mutmut_orig.__name__ = "x__reset_meter_provider"


def _reset_opentelemetry_providers() -> None:
    """Reset OpenTelemetry providers to uninitialized state.

    This prevents "Overriding of current TracerProvider/MeterProvider" warnings
    and stream closure issues by properly resetting the global providers.
    """
    _reset_tracer_provider()
    _reset_meter_provider()


def x__reset_foundation_environment_variables__mutmut_orig() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_1() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = None

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_2() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "XXPROVIDE_LOG_LEVELXX": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_3() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "provide_log_level": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_4() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "XXDEBUGXX",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_5() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "debug",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_6() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "XXFOUNDATION_SUPPRESS_TESTING_WARNINGSXX": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_7() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "foundation_suppress_testing_warnings": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_8() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "XXtrueXX",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_9() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "TRUE",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_10() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = None

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_11() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "XXPROVIDE_PROFILEXX",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_12() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "provide_profile",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_13() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "XXPROVIDE_DEBUGXX",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_14() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "provide_debug",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_15() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "XXPROVIDE_JSON_OUTPUTXX",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_16() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "provide_json_output",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_17() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_18() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = None

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def x__reset_foundation_environment_variables__mutmut_19() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var not in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


x__reset_foundation_environment_variables__mutmut_mutants: ClassVar[MutantDict] = {
    "x__reset_foundation_environment_variables__mutmut_1": x__reset_foundation_environment_variables__mutmut_1,
    "x__reset_foundation_environment_variables__mutmut_2": x__reset_foundation_environment_variables__mutmut_2,
    "x__reset_foundation_environment_variables__mutmut_3": x__reset_foundation_environment_variables__mutmut_3,
    "x__reset_foundation_environment_variables__mutmut_4": x__reset_foundation_environment_variables__mutmut_4,
    "x__reset_foundation_environment_variables__mutmut_5": x__reset_foundation_environment_variables__mutmut_5,
    "x__reset_foundation_environment_variables__mutmut_6": x__reset_foundation_environment_variables__mutmut_6,
    "x__reset_foundation_environment_variables__mutmut_7": x__reset_foundation_environment_variables__mutmut_7,
    "x__reset_foundation_environment_variables__mutmut_8": x__reset_foundation_environment_variables__mutmut_8,
    "x__reset_foundation_environment_variables__mutmut_9": x__reset_foundation_environment_variables__mutmut_9,
    "x__reset_foundation_environment_variables__mutmut_10": x__reset_foundation_environment_variables__mutmut_10,
    "x__reset_foundation_environment_variables__mutmut_11": x__reset_foundation_environment_variables__mutmut_11,
    "x__reset_foundation_environment_variables__mutmut_12": x__reset_foundation_environment_variables__mutmut_12,
    "x__reset_foundation_environment_variables__mutmut_13": x__reset_foundation_environment_variables__mutmut_13,
    "x__reset_foundation_environment_variables__mutmut_14": x__reset_foundation_environment_variables__mutmut_14,
    "x__reset_foundation_environment_variables__mutmut_15": x__reset_foundation_environment_variables__mutmut_15,
    "x__reset_foundation_environment_variables__mutmut_16": x__reset_foundation_environment_variables__mutmut_16,
    "x__reset_foundation_environment_variables__mutmut_17": x__reset_foundation_environment_variables__mutmut_17,
    "x__reset_foundation_environment_variables__mutmut_18": x__reset_foundation_environment_variables__mutmut_18,
    "x__reset_foundation_environment_variables__mutmut_19": x__reset_foundation_environment_variables__mutmut_19,
}


def _reset_foundation_environment_variables(*args, **kwargs):
    result = _mutmut_trampoline(
        x__reset_foundation_environment_variables__mutmut_orig,
        x__reset_foundation_environment_variables__mutmut_mutants,
        args,
        kwargs,
    )
    return result


_reset_foundation_environment_variables.__signature__ = _mutmut_signature(
    x__reset_foundation_environment_variables__mutmut_orig
)
x__reset_foundation_environment_variables__mutmut_orig.__name__ = "x__reset_foundation_environment_variables"


def x_reset_foundation_state__mutmut_orig() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_1() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = None
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_2() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = False
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_3() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(None)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_4() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_5() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(None)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_6() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_7() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_8() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get(None):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_9() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("XXPYTEST_XDIST_WORKERXX"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_10() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("pytest_xdist_worker"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_11() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = None
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_12() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = True
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_13() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(None)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_14() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_15() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(None)
        except ImportError:
            pass


def x_reset_foundation_state__mutmut_16() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass


x_reset_foundation_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_foundation_state__mutmut_1": x_reset_foundation_state__mutmut_1,
    "x_reset_foundation_state__mutmut_2": x_reset_foundation_state__mutmut_2,
    "x_reset_foundation_state__mutmut_3": x_reset_foundation_state__mutmut_3,
    "x_reset_foundation_state__mutmut_4": x_reset_foundation_state__mutmut_4,
    "x_reset_foundation_state__mutmut_5": x_reset_foundation_state__mutmut_5,
    "x_reset_foundation_state__mutmut_6": x_reset_foundation_state__mutmut_6,
    "x_reset_foundation_state__mutmut_7": x_reset_foundation_state__mutmut_7,
    "x_reset_foundation_state__mutmut_8": x_reset_foundation_state__mutmut_8,
    "x_reset_foundation_state__mutmut_9": x_reset_foundation_state__mutmut_9,
    "x_reset_foundation_state__mutmut_10": x_reset_foundation_state__mutmut_10,
    "x_reset_foundation_state__mutmut_11": x_reset_foundation_state__mutmut_11,
    "x_reset_foundation_state__mutmut_12": x_reset_foundation_state__mutmut_12,
    "x_reset_foundation_state__mutmut_13": x_reset_foundation_state__mutmut_13,
    "x_reset_foundation_state__mutmut_14": x_reset_foundation_state__mutmut_14,
    "x_reset_foundation_state__mutmut_15": x_reset_foundation_state__mutmut_15,
    "x_reset_foundation_state__mutmut_16": x_reset_foundation_state__mutmut_16,
}


def reset_foundation_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_foundation_state__mutmut_orig, x_reset_foundation_state__mutmut_mutants, args, kwargs
    )
    return result


reset_foundation_state.__signature__ = _mutmut_signature(x_reset_foundation_state__mutmut_orig)
x_reset_foundation_state__mutmut_orig.__name__ = "x_reset_foundation_state"


def x_reset_foundation_for_testing__mutmut_orig() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_1() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = None
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_2() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = False
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_3() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = ""
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_4() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = None
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_5() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_6() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = None
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_7() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update(None)
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_8() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"XXdoneXX": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_9() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"DONE": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_10() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": True, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_11() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "XXerrorXX": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_12() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "ERROR": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_13() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "XXin_progressXX": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_14() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "IN_PROGRESS": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_15() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": True})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_16() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(None)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


def x_reset_foundation_for_testing__mutmut_17() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = None


def x_reset_foundation_for_testing__mutmut_18() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = True


x_reset_foundation_for_testing__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_foundation_for_testing__mutmut_1": x_reset_foundation_for_testing__mutmut_1,
    "x_reset_foundation_for_testing__mutmut_2": x_reset_foundation_for_testing__mutmut_2,
    "x_reset_foundation_for_testing__mutmut_3": x_reset_foundation_for_testing__mutmut_3,
    "x_reset_foundation_for_testing__mutmut_4": x_reset_foundation_for_testing__mutmut_4,
    "x_reset_foundation_for_testing__mutmut_5": x_reset_foundation_for_testing__mutmut_5,
    "x_reset_foundation_for_testing__mutmut_6": x_reset_foundation_for_testing__mutmut_6,
    "x_reset_foundation_for_testing__mutmut_7": x_reset_foundation_for_testing__mutmut_7,
    "x_reset_foundation_for_testing__mutmut_8": x_reset_foundation_for_testing__mutmut_8,
    "x_reset_foundation_for_testing__mutmut_9": x_reset_foundation_for_testing__mutmut_9,
    "x_reset_foundation_for_testing__mutmut_10": x_reset_foundation_for_testing__mutmut_10,
    "x_reset_foundation_for_testing__mutmut_11": x_reset_foundation_for_testing__mutmut_11,
    "x_reset_foundation_for_testing__mutmut_12": x_reset_foundation_for_testing__mutmut_12,
    "x_reset_foundation_for_testing__mutmut_13": x_reset_foundation_for_testing__mutmut_13,
    "x_reset_foundation_for_testing__mutmut_14": x_reset_foundation_for_testing__mutmut_14,
    "x_reset_foundation_for_testing__mutmut_15": x_reset_foundation_for_testing__mutmut_15,
    "x_reset_foundation_for_testing__mutmut_16": x_reset_foundation_for_testing__mutmut_16,
    "x_reset_foundation_for_testing__mutmut_17": x_reset_foundation_for_testing__mutmut_17,
    "x_reset_foundation_for_testing__mutmut_18": x_reset_foundation_for_testing__mutmut_18,
}


def reset_foundation_for_testing(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_foundation_for_testing__mutmut_orig,
        x_reset_foundation_for_testing__mutmut_mutants,
        args,
        kwargs,
    )
    return result


reset_foundation_for_testing.__signature__ = _mutmut_signature(x_reset_foundation_for_testing__mutmut_orig)
x_reset_foundation_for_testing__mutmut_orig.__name__ = "x_reset_foundation_for_testing"


# <3 🧱🤝🧪🪄
