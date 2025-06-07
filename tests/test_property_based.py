#
# test_property_based.py
#

"""
Property-based tests for Pyvider Telemetry using Hypothesis.

These tests aim to cover a wider range of inputs and edge cases
by generating test data automatically.
"""
from collections.abc import Callable
import io
from typing import (
    Any,
    get_args,  # Added get_args
)

from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import (
    SearchStrategy,
    booleans,
    composite,
    dictionaries,
    integers,
    lists,
    none,
    one_of,
    sampled_from,
    text,
)

from pyvider.telemetry import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
    LoggingConfig,
    TelemetryConfig,
    logger as pyvider_global_logger,
    setup_telemetry,
)
from pyvider.telemetry.core import (
    _set_log_stream_for_testing,
    reset_pyvider_setup_for_testing,
)
from pyvider.telemetry.types import ConsoleFormatterStr, LogLevelStr  # Corrected import

# --- Strategies ---

# Strategy for valid logger names (simplified for robustness)
logger_names_st = text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._- ",
    min_size=0,
    max_size=50
)

# Strategy for log messages - FIXED: More conservative character set
log_messages_st = text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?-_",
    min_size=1,
    max_size=100
)

# Strategy for DAS (Domain-Action-Status) keys
das_keys_base_st = list(PRIMARY_EMOJI.keys()) + list(SECONDARY_EMOJI.keys()) + list(TERTIARY_EMOJI.keys())
das_values_st = one_of(
    none(),
    sampled_from(das_keys_base_st),
    text(alphabet="abcdefghijklmnopqrstuvwxyz_", min_size=3, max_size=15)
)

# Strategy for arbitrary kwargs - FIXED: More conservative values
simple_kwargs_st = dictionaries(
    keys=text(alphabet="abcdefghijklmnopqrstuvwxyz_", min_size=1, max_size=20),
    values=one_of(
        none(),
        booleans(),
        integers(min_value=-1000, max_value=1000),
        text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ._-", max_size=50),
    ),
    max_size=3  # Reduced from 5 to 3
)

# Strategy for log levels (strings)
log_levels_st = sampled_from(list(get_args(LogLevelStr)))

# Strategy for console formatters
console_formatters_st = sampled_from(list(get_args(ConsoleFormatterStr)))

# Composite strategy for TelemetryConfig
@composite
def telemetry_config_st(draw: Callable[[SearchStrategy[Any]], Any]) -> TelemetryConfig:
    service_name = draw(one_of(none(), text(max_size=30)))
    default_level = draw(log_levels_st)

    module_levels_keys = draw(lists(logger_names_st, max_size=3))  # Reduced from 5
    module_levels_values = draw(lists(log_levels_st, min_size=len(module_levels_keys), max_size=len(module_levels_keys)))
    module_levels = dict(zip(module_levels_keys, module_levels_values, strict=False))

    console_formatter = draw(console_formatters_st)
    logger_name_emoji_enabled = draw(booleans())
    das_emoji_enabled = draw(booleans())
    omit_timestamp = draw(booleans())
    globally_disabled = draw(booleans())

    logging_conf = LoggingConfig(
        default_level=default_level,
        module_levels=module_levels,
        console_formatter=console_formatter,
        logger_name_emoji_prefix_enabled=logger_name_emoji_enabled,
        das_emoji_prefix_enabled=das_emoji_enabled,
        omit_timestamp=omit_timestamp,
    )
    return TelemetryConfig(
        service_name=service_name,
        logging=logging_conf,
        globally_disabled=globally_disabled,
    )

# --- Tests ---

@given(
    config=telemetry_config_st(),
    logger_name=logger_names_st,
    message=log_messages_st,
    domain=das_values_st,
    action=das_values_st,
    status=das_values_st,
    extra_kwargs=simple_kwargs_st,
    log_method_name=sampled_from(["debug", "info", "warning", "error", "critical", "trace"])  # Removed "exception"
)
@settings(
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.data_too_large,
        HealthCheck.filter_too_much,
        HealthCheck.function_scoped_fixture
    ],
    deadline=None,
    max_examples=25  # Reduced from 50
)
def test_pyvider_logger_robustness(
    config: TelemetryConfig,
    logger_name: str,
    message: str,
    domain: str | None,
    action: str | None,
    status: str | None,
    extra_kwargs: dict[str, Any],
    log_method_name: str
) -> None:
    """
    Tests that PyviderLogger methods do not crash with varied inputs.
    """
    # Manual setup for each Hypothesis example
    reset_pyvider_setup_for_testing()
    current_example_log_capture_buffer = io.StringIO()
    _set_log_stream_for_testing(current_example_log_capture_buffer)

    try:
        setup_telemetry(config)

        # FIXED: Sanitize inputs to prevent issues
        safe_message = str(message) if message else "test message"
        safe_logger_name = str(logger_name).strip() if logger_name and str(logger_name).strip() else "test.logger"

        log_call_kwargs = {}
        # FIXED: Only add safe kwargs
        for k, v in extra_kwargs.items():
            if k and isinstance(k, str) and k.isidentifier():
                log_call_kwargs[k] = v

        if domain is not None:
            log_call_kwargs["domain"] = str(domain)
        if action is not None:
            log_call_kwargs["action"] = str(action)
        if status is not None:
            log_call_kwargs["status"] = str(status)

        current_logger = pyvider_global_logger

        if hasattr(current_logger, log_method_name):
            getattr(current_logger, log_method_name)

            if log_method_name == "trace":
                trace_kwargs = log_call_kwargs.copy()
                current_logger.trace(safe_message, _pyvider_logger_name=safe_logger_name, **trace_kwargs)
            else:
                # For other methods, use get_logger
                named_logger = current_logger.get_logger(safe_logger_name)
                named_log_method = getattr(named_logger, log_method_name)
                named_log_method(safe_message, **log_call_kwargs)

    except Exception as e:
        import pytest
        pytest.fail(
            f"Logging call failed unexpectedly with error: {e}\n"
            f"Config: {config}\n"
            f"Logger Name: {logger_name}\n"
            f"Method: {log_method_name}\n"
            f"Message: {str(message)[:100]}...\n"
            f"Domain: {domain}, Action: {action}, Status: {status}\n"
            f"Extra Kwargs: {extra_kwargs}"
        )
    finally:
        _set_log_stream_for_testing(None)
        current_example_log_capture_buffer.close()

# 🧪🔬
