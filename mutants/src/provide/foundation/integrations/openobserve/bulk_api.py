# provide/foundation/integrations/openobserve/bulk_api.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""OpenObserve bulk API (non-OTLP fallback).

Provides functions for sending logs via OpenObserve's proprietary bulk ingestion API.
This is used as a fallback when OTLP is unavailable or when the circuit breaker is open.
"""

from __future__ import annotations

import time
from typing import Any

from provide.foundation.hub import get_hub
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.logger import get_logger
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.otlp.helpers import add_trace_context_to_attributes
from provide.foundation.serialization import json_dumps
from provide.foundation.utils.async_helpers import run_async

log = get_logger(__name__)
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


def x_build_log_entry__mutmut_orig(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_1(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = None

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_2(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "XX_timestampXX": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_3(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_TIMESTAMP": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_4(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(None),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_5(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() / 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_6(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1000001),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_7(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "XXlevelXX": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_8(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "LEVEL": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_9(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.lower(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_10(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "XXmessageXX": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_11(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "MESSAGE": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_12(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "XXserviceXX": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_13(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "SERVICE": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_14(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name and "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_15(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name and config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_16(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "XXfoundationXX",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_17(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "FOUNDATION",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_18(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(None)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def x_build_log_entry__mutmut_19(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(None)
    return log_entry

x_build_log_entry__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_log_entry__mutmut_1': x_build_log_entry__mutmut_1, 
    'x_build_log_entry__mutmut_2': x_build_log_entry__mutmut_2, 
    'x_build_log_entry__mutmut_3': x_build_log_entry__mutmut_3, 
    'x_build_log_entry__mutmut_4': x_build_log_entry__mutmut_4, 
    'x_build_log_entry__mutmut_5': x_build_log_entry__mutmut_5, 
    'x_build_log_entry__mutmut_6': x_build_log_entry__mutmut_6, 
    'x_build_log_entry__mutmut_7': x_build_log_entry__mutmut_7, 
    'x_build_log_entry__mutmut_8': x_build_log_entry__mutmut_8, 
    'x_build_log_entry__mutmut_9': x_build_log_entry__mutmut_9, 
    'x_build_log_entry__mutmut_10': x_build_log_entry__mutmut_10, 
    'x_build_log_entry__mutmut_11': x_build_log_entry__mutmut_11, 
    'x_build_log_entry__mutmut_12': x_build_log_entry__mutmut_12, 
    'x_build_log_entry__mutmut_13': x_build_log_entry__mutmut_13, 
    'x_build_log_entry__mutmut_14': x_build_log_entry__mutmut_14, 
    'x_build_log_entry__mutmut_15': x_build_log_entry__mutmut_15, 
    'x_build_log_entry__mutmut_16': x_build_log_entry__mutmut_16, 
    'x_build_log_entry__mutmut_17': x_build_log_entry__mutmut_17, 
    'x_build_log_entry__mutmut_18': x_build_log_entry__mutmut_18, 
    'x_build_log_entry__mutmut_19': x_build_log_entry__mutmut_19
}

def build_log_entry(*args, **kwargs):
    result = _mutmut_trampoline(x_build_log_entry__mutmut_orig, x_build_log_entry__mutmut_mutants, args, kwargs)
    return result 

build_log_entry.__signature__ = _mutmut_signature(x_build_log_entry__mutmut_orig)
x_build_log_entry__mutmut_orig.__name__ = 'x_build_log_entry'


def x_build_bulk_url__mutmut_orig(client: OpenObserveClient) -> str:
    """Build the bulk API URL for the client.

    Args:
        client: OpenObserve client instance

    Returns:
        Bulk API URL

    Examples:
        >>> client = OpenObserveClient(
        ...     url="https://api.openobserve.ai",
        ...     username="admin",
        ...     password="secret",
        ...     organization="my-org",
        ... )
        >>> build_bulk_url(client)
        'https://api.openobserve.ai/api/my-org/_bulk'
    """
    if f"/api/{client.organization}" in client.url:
        return f"{client.url}/_bulk"
    return f"{client.url}/api/{client.organization}/_bulk"


def x_build_bulk_url__mutmut_1(client: OpenObserveClient) -> str:
    """Build the bulk API URL for the client.

    Args:
        client: OpenObserve client instance

    Returns:
        Bulk API URL

    Examples:
        >>> client = OpenObserveClient(
        ...     url="https://api.openobserve.ai",
        ...     username="admin",
        ...     password="secret",
        ...     organization="my-org",
        ... )
        >>> build_bulk_url(client)
        'https://api.openobserve.ai/api/my-org/_bulk'
    """
    if f"/api/{client.organization}" not in client.url:
        return f"{client.url}/_bulk"
    return f"{client.url}/api/{client.organization}/_bulk"

x_build_bulk_url__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_bulk_url__mutmut_1': x_build_bulk_url__mutmut_1
}

def build_bulk_url(*args, **kwargs):
    result = _mutmut_trampoline(x_build_bulk_url__mutmut_orig, x_build_bulk_url__mutmut_mutants, args, kwargs)
    return result 

build_bulk_url.__signature__ = _mutmut_signature(x_build_bulk_url__mutmut_orig)
x_build_bulk_url__mutmut_orig.__name__ = 'x_build_bulk_url'


def x_build_bulk_request__mutmut_orig(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_1(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = None
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_2(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(None, level, service_name, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_3(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, None, service_name, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_4(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, None, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_5(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, None, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_6(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, None)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_7(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(level, service_name, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_8(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, service_name, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_9(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_10(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_11(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, )
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_12(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = None
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_13(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps(None)
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_14(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps({"XXindexXX": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_15(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps({"INDEX": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_16(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps({"index": {"XX_indexXX": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_17(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps({"index": {"_INDEX": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_18(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = None
    return f"{index_line}\n{data_line}\n"


def x_build_bulk_request__mutmut_19(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(None)
    return f"{index_line}\n{data_line}\n"

x_build_bulk_request__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_bulk_request__mutmut_1': x_build_bulk_request__mutmut_1, 
    'x_build_bulk_request__mutmut_2': x_build_bulk_request__mutmut_2, 
    'x_build_bulk_request__mutmut_3': x_build_bulk_request__mutmut_3, 
    'x_build_bulk_request__mutmut_4': x_build_bulk_request__mutmut_4, 
    'x_build_bulk_request__mutmut_5': x_build_bulk_request__mutmut_5, 
    'x_build_bulk_request__mutmut_6': x_build_bulk_request__mutmut_6, 
    'x_build_bulk_request__mutmut_7': x_build_bulk_request__mutmut_7, 
    'x_build_bulk_request__mutmut_8': x_build_bulk_request__mutmut_8, 
    'x_build_bulk_request__mutmut_9': x_build_bulk_request__mutmut_9, 
    'x_build_bulk_request__mutmut_10': x_build_bulk_request__mutmut_10, 
    'x_build_bulk_request__mutmut_11': x_build_bulk_request__mutmut_11, 
    'x_build_bulk_request__mutmut_12': x_build_bulk_request__mutmut_12, 
    'x_build_bulk_request__mutmut_13': x_build_bulk_request__mutmut_13, 
    'x_build_bulk_request__mutmut_14': x_build_bulk_request__mutmut_14, 
    'x_build_bulk_request__mutmut_15': x_build_bulk_request__mutmut_15, 
    'x_build_bulk_request__mutmut_16': x_build_bulk_request__mutmut_16, 
    'x_build_bulk_request__mutmut_17': x_build_bulk_request__mutmut_17, 
    'x_build_bulk_request__mutmut_18': x_build_bulk_request__mutmut_18, 
    'x_build_bulk_request__mutmut_19': x_build_bulk_request__mutmut_19
}

def build_bulk_request(*args, **kwargs):
    result = _mutmut_trampoline(x_build_bulk_request__mutmut_orig, x_build_bulk_request__mutmut_mutants, args, kwargs)
    return result 

build_bulk_request.__signature__ = _mutmut_signature(x_build_bulk_request__mutmut_orig)
x_build_bulk_request__mutmut_orig.__name__ = 'x_build_bulk_request'


def x_send_log_bulk__mutmut_orig(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_1(
    message: str,
    level: str = "XXINFOXX",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_2(
    message: str,
    level: str = "info",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_3(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is not None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_4(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = None

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_5(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = None
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_6(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = None
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_7(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is not None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_8(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = None

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_9(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = None

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_10(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = None
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_11(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream and "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_12(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "XXdefaultXX"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_13(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "DEFAULT"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_14(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = None

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_15(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(None, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_16(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, None, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_17(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, None, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_18(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, None, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_19(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, None, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_20(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, None)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_21(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_22(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_23(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_24(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_25(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_26(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, )

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_27(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = None

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_28(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(None)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_29(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = None

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_30(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=None,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_31(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method=None,
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_32(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=None,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_33(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers=None,
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_34(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_35(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_36(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_37(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_38(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="XXPOSTXX",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_39(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="post",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_40(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"XXContent-TypeXX": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_41(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"content-type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_42(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"CONTENT-TYPE": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_43(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "XXapplication/x-ndjsonXX"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_44(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "APPLICATION/X-NDJSON"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_45(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(None)
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_46(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:51]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_47(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return False
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_48(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(None)
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_49(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return True

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_50(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(None)

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def x_send_log_bulk__mutmut_51(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(None)
        return False


def x_send_log_bulk__mutmut_52(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return True

x_send_log_bulk__mutmut_mutants : ClassVar[MutantDict] = {
'x_send_log_bulk__mutmut_1': x_send_log_bulk__mutmut_1, 
    'x_send_log_bulk__mutmut_2': x_send_log_bulk__mutmut_2, 
    'x_send_log_bulk__mutmut_3': x_send_log_bulk__mutmut_3, 
    'x_send_log_bulk__mutmut_4': x_send_log_bulk__mutmut_4, 
    'x_send_log_bulk__mutmut_5': x_send_log_bulk__mutmut_5, 
    'x_send_log_bulk__mutmut_6': x_send_log_bulk__mutmut_6, 
    'x_send_log_bulk__mutmut_7': x_send_log_bulk__mutmut_7, 
    'x_send_log_bulk__mutmut_8': x_send_log_bulk__mutmut_8, 
    'x_send_log_bulk__mutmut_9': x_send_log_bulk__mutmut_9, 
    'x_send_log_bulk__mutmut_10': x_send_log_bulk__mutmut_10, 
    'x_send_log_bulk__mutmut_11': x_send_log_bulk__mutmut_11, 
    'x_send_log_bulk__mutmut_12': x_send_log_bulk__mutmut_12, 
    'x_send_log_bulk__mutmut_13': x_send_log_bulk__mutmut_13, 
    'x_send_log_bulk__mutmut_14': x_send_log_bulk__mutmut_14, 
    'x_send_log_bulk__mutmut_15': x_send_log_bulk__mutmut_15, 
    'x_send_log_bulk__mutmut_16': x_send_log_bulk__mutmut_16, 
    'x_send_log_bulk__mutmut_17': x_send_log_bulk__mutmut_17, 
    'x_send_log_bulk__mutmut_18': x_send_log_bulk__mutmut_18, 
    'x_send_log_bulk__mutmut_19': x_send_log_bulk__mutmut_19, 
    'x_send_log_bulk__mutmut_20': x_send_log_bulk__mutmut_20, 
    'x_send_log_bulk__mutmut_21': x_send_log_bulk__mutmut_21, 
    'x_send_log_bulk__mutmut_22': x_send_log_bulk__mutmut_22, 
    'x_send_log_bulk__mutmut_23': x_send_log_bulk__mutmut_23, 
    'x_send_log_bulk__mutmut_24': x_send_log_bulk__mutmut_24, 
    'x_send_log_bulk__mutmut_25': x_send_log_bulk__mutmut_25, 
    'x_send_log_bulk__mutmut_26': x_send_log_bulk__mutmut_26, 
    'x_send_log_bulk__mutmut_27': x_send_log_bulk__mutmut_27, 
    'x_send_log_bulk__mutmut_28': x_send_log_bulk__mutmut_28, 
    'x_send_log_bulk__mutmut_29': x_send_log_bulk__mutmut_29, 
    'x_send_log_bulk__mutmut_30': x_send_log_bulk__mutmut_30, 
    'x_send_log_bulk__mutmut_31': x_send_log_bulk__mutmut_31, 
    'x_send_log_bulk__mutmut_32': x_send_log_bulk__mutmut_32, 
    'x_send_log_bulk__mutmut_33': x_send_log_bulk__mutmut_33, 
    'x_send_log_bulk__mutmut_34': x_send_log_bulk__mutmut_34, 
    'x_send_log_bulk__mutmut_35': x_send_log_bulk__mutmut_35, 
    'x_send_log_bulk__mutmut_36': x_send_log_bulk__mutmut_36, 
    'x_send_log_bulk__mutmut_37': x_send_log_bulk__mutmut_37, 
    'x_send_log_bulk__mutmut_38': x_send_log_bulk__mutmut_38, 
    'x_send_log_bulk__mutmut_39': x_send_log_bulk__mutmut_39, 
    'x_send_log_bulk__mutmut_40': x_send_log_bulk__mutmut_40, 
    'x_send_log_bulk__mutmut_41': x_send_log_bulk__mutmut_41, 
    'x_send_log_bulk__mutmut_42': x_send_log_bulk__mutmut_42, 
    'x_send_log_bulk__mutmut_43': x_send_log_bulk__mutmut_43, 
    'x_send_log_bulk__mutmut_44': x_send_log_bulk__mutmut_44, 
    'x_send_log_bulk__mutmut_45': x_send_log_bulk__mutmut_45, 
    'x_send_log_bulk__mutmut_46': x_send_log_bulk__mutmut_46, 
    'x_send_log_bulk__mutmut_47': x_send_log_bulk__mutmut_47, 
    'x_send_log_bulk__mutmut_48': x_send_log_bulk__mutmut_48, 
    'x_send_log_bulk__mutmut_49': x_send_log_bulk__mutmut_49, 
    'x_send_log_bulk__mutmut_50': x_send_log_bulk__mutmut_50, 
    'x_send_log_bulk__mutmut_51': x_send_log_bulk__mutmut_51, 
    'x_send_log_bulk__mutmut_52': x_send_log_bulk__mutmut_52
}

def send_log_bulk(*args, **kwargs):
    result = _mutmut_trampoline(x_send_log_bulk__mutmut_orig, x_send_log_bulk__mutmut_mutants, args, kwargs)
    return result 

send_log_bulk.__signature__ = _mutmut_signature(x_send_log_bulk__mutmut_orig)
x_send_log_bulk__mutmut_orig.__name__ = 'x_send_log_bulk'


__all__ = [
    "build_bulk_request",
    "build_bulk_url",
    "build_log_entry",
    "send_log_bulk",
]


# <3 🧱🤝🔌🪄
