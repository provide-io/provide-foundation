# provide/foundation/integrations/openobserve/otlp_helpers.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

"""Helper functions for OTLP integration.

This module contains helper functions extracted from otlp.py to keep
file sizes manageable and improve code organization.
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


def x_configure_otlp_exporter__mutmut_orig(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_1(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = None
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_2(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = None
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_3(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["XXorganizationXX"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_4(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["ORGANIZATION"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_5(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = None

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_6(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["XXstream-nameXX"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_7(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["STREAM-NAME"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_8(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = None
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_9(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace(None, "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_10(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", None)
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_11(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_12(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", )
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_13(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("XX/v1/tracesXX", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_14(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/V1/TRACES", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_15(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "XX/v1/logsXX")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_16(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/V1/LOGS")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def x_configure_otlp_exporter__mutmut_17(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = None

    return logs_endpoint, headers

x_configure_otlp_exporter__mutmut_mutants : ClassVar[MutantDict] = {
'x_configure_otlp_exporter__mutmut_1': x_configure_otlp_exporter__mutmut_1, 
    'x_configure_otlp_exporter__mutmut_2': x_configure_otlp_exporter__mutmut_2, 
    'x_configure_otlp_exporter__mutmut_3': x_configure_otlp_exporter__mutmut_3, 
    'x_configure_otlp_exporter__mutmut_4': x_configure_otlp_exporter__mutmut_4, 
    'x_configure_otlp_exporter__mutmut_5': x_configure_otlp_exporter__mutmut_5, 
    'x_configure_otlp_exporter__mutmut_6': x_configure_otlp_exporter__mutmut_6, 
    'x_configure_otlp_exporter__mutmut_7': x_configure_otlp_exporter__mutmut_7, 
    'x_configure_otlp_exporter__mutmut_8': x_configure_otlp_exporter__mutmut_8, 
    'x_configure_otlp_exporter__mutmut_9': x_configure_otlp_exporter__mutmut_9, 
    'x_configure_otlp_exporter__mutmut_10': x_configure_otlp_exporter__mutmut_10, 
    'x_configure_otlp_exporter__mutmut_11': x_configure_otlp_exporter__mutmut_11, 
    'x_configure_otlp_exporter__mutmut_12': x_configure_otlp_exporter__mutmut_12, 
    'x_configure_otlp_exporter__mutmut_13': x_configure_otlp_exporter__mutmut_13, 
    'x_configure_otlp_exporter__mutmut_14': x_configure_otlp_exporter__mutmut_14, 
    'x_configure_otlp_exporter__mutmut_15': x_configure_otlp_exporter__mutmut_15, 
    'x_configure_otlp_exporter__mutmut_16': x_configure_otlp_exporter__mutmut_16, 
    'x_configure_otlp_exporter__mutmut_17': x_configure_otlp_exporter__mutmut_17
}

def configure_otlp_exporter(*args, **kwargs):
    result = _mutmut_trampoline(x_configure_otlp_exporter__mutmut_orig, x_configure_otlp_exporter__mutmut_mutants, args, kwargs)
    return result 

configure_otlp_exporter.__signature__ = _mutmut_signature(x_configure_otlp_exporter__mutmut_orig)
x_configure_otlp_exporter__mutmut_orig.__name__ = 'x_configure_otlp_exporter'


def x_create_otlp_resource__mutmut_orig(
    service_name: str,
    service_version: str | None,
    resource_class: Any,
    resource_attrs_class: Any,
) -> Any:
    """Create OTLP resource with service information.

    Args:
        service_name: Service name
        service_version: Optional service version
        resource_class: Resource class from OpenTelemetry
        resource_attrs_class: ResourceAttributes class from OpenTelemetry

    Returns:
        Resource instance
    """
    resource_attrs = {
        resource_attrs_class.SERVICE_NAME: service_name,
    }
    if service_version:
        resource_attrs[resource_attrs_class.SERVICE_VERSION] = service_version

    return resource_class.create(resource_attrs)


def x_create_otlp_resource__mutmut_1(
    service_name: str,
    service_version: str | None,
    resource_class: Any,
    resource_attrs_class: Any,
) -> Any:
    """Create OTLP resource with service information.

    Args:
        service_name: Service name
        service_version: Optional service version
        resource_class: Resource class from OpenTelemetry
        resource_attrs_class: ResourceAttributes class from OpenTelemetry

    Returns:
        Resource instance
    """
    resource_attrs = None
    if service_version:
        resource_attrs[resource_attrs_class.SERVICE_VERSION] = service_version

    return resource_class.create(resource_attrs)


def x_create_otlp_resource__mutmut_2(
    service_name: str,
    service_version: str | None,
    resource_class: Any,
    resource_attrs_class: Any,
) -> Any:
    """Create OTLP resource with service information.

    Args:
        service_name: Service name
        service_version: Optional service version
        resource_class: Resource class from OpenTelemetry
        resource_attrs_class: ResourceAttributes class from OpenTelemetry

    Returns:
        Resource instance
    """
    resource_attrs = {
        resource_attrs_class.SERVICE_NAME: service_name,
    }
    if service_version:
        resource_attrs[resource_attrs_class.SERVICE_VERSION] = None

    return resource_class.create(resource_attrs)


def x_create_otlp_resource__mutmut_3(
    service_name: str,
    service_version: str | None,
    resource_class: Any,
    resource_attrs_class: Any,
) -> Any:
    """Create OTLP resource with service information.

    Args:
        service_name: Service name
        service_version: Optional service version
        resource_class: Resource class from OpenTelemetry
        resource_attrs_class: ResourceAttributes class from OpenTelemetry

    Returns:
        Resource instance
    """
    resource_attrs = {
        resource_attrs_class.SERVICE_NAME: service_name,
    }
    if service_version:
        resource_attrs[resource_attrs_class.SERVICE_VERSION] = service_version

    return resource_class.create(None)

x_create_otlp_resource__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_otlp_resource__mutmut_1': x_create_otlp_resource__mutmut_1, 
    'x_create_otlp_resource__mutmut_2': x_create_otlp_resource__mutmut_2, 
    'x_create_otlp_resource__mutmut_3': x_create_otlp_resource__mutmut_3
}

def create_otlp_resource(*args, **kwargs):
    result = _mutmut_trampoline(x_create_otlp_resource__mutmut_orig, x_create_otlp_resource__mutmut_mutants, args, kwargs)
    return result 

create_otlp_resource.__signature__ = _mutmut_signature(x_create_otlp_resource__mutmut_orig)
x_create_otlp_resource__mutmut_orig.__name__ = 'x_create_otlp_resource'


def x_add_trace_attributes__mutmut_orig(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["trace_id"] = f"{span_context.trace_id:032x}"
        attributes["span_id"] = f"{span_context.span_id:016x}"


def x_add_trace_attributes__mutmut_1(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = None
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["trace_id"] = f"{span_context.trace_id:032x}"
        attributes["span_id"] = f"{span_context.span_id:016x}"


def x_add_trace_attributes__mutmut_2(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span or current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["trace_id"] = f"{span_context.trace_id:032x}"
        attributes["span_id"] = f"{span_context.span_id:016x}"


def x_add_trace_attributes__mutmut_3(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = None
        attributes["trace_id"] = f"{span_context.trace_id:032x}"
        attributes["span_id"] = f"{span_context.span_id:016x}"


def x_add_trace_attributes__mutmut_4(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["trace_id"] = None
        attributes["span_id"] = f"{span_context.span_id:016x}"


def x_add_trace_attributes__mutmut_5(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["XXtrace_idXX"] = f"{span_context.trace_id:032x}"
        attributes["span_id"] = f"{span_context.span_id:016x}"


def x_add_trace_attributes__mutmut_6(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["TRACE_ID"] = f"{span_context.trace_id:032x}"
        attributes["span_id"] = f"{span_context.span_id:016x}"


def x_add_trace_attributes__mutmut_7(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["trace_id"] = f"{span_context.trace_id:032x}"
        attributes["span_id"] = None


def x_add_trace_attributes__mutmut_8(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["trace_id"] = f"{span_context.trace_id:032x}"
        attributes["XXspan_idXX"] = f"{span_context.span_id:016x}"


def x_add_trace_attributes__mutmut_9(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["trace_id"] = f"{span_context.trace_id:032x}"
        attributes["SPAN_ID"] = f"{span_context.span_id:016x}"

x_add_trace_attributes__mutmut_mutants : ClassVar[MutantDict] = {
'x_add_trace_attributes__mutmut_1': x_add_trace_attributes__mutmut_1, 
    'x_add_trace_attributes__mutmut_2': x_add_trace_attributes__mutmut_2, 
    'x_add_trace_attributes__mutmut_3': x_add_trace_attributes__mutmut_3, 
    'x_add_trace_attributes__mutmut_4': x_add_trace_attributes__mutmut_4, 
    'x_add_trace_attributes__mutmut_5': x_add_trace_attributes__mutmut_5, 
    'x_add_trace_attributes__mutmut_6': x_add_trace_attributes__mutmut_6, 
    'x_add_trace_attributes__mutmut_7': x_add_trace_attributes__mutmut_7, 
    'x_add_trace_attributes__mutmut_8': x_add_trace_attributes__mutmut_8, 
    'x_add_trace_attributes__mutmut_9': x_add_trace_attributes__mutmut_9
}

def add_trace_attributes(*args, **kwargs):
    result = _mutmut_trampoline(x_add_trace_attributes__mutmut_orig, x_add_trace_attributes__mutmut_mutants, args, kwargs)
    return result 

add_trace_attributes.__signature__ = _mutmut_signature(x_add_trace_attributes__mutmut_orig)
x_add_trace_attributes__mutmut_orig.__name__ = 'x_add_trace_attributes'


def x_map_level_to_severity__mutmut_orig(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_1(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = None
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_2(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "XXTRACEXX": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_3(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "trace": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_4(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 2,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_5(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "XXDEBUGXX": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_6(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "debug": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_7(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 6,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_8(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "XXINFOXX": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_9(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "info": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_10(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 10,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_11(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "XXWARNXX": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_12(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "warn": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_13(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 14,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_14(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "XXWARNINGXX": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_15(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "warning": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_16(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 14,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_17(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "XXERRORXX": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_18(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "error": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_19(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 18,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_20(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "XXFATALXX": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_21(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "fatal": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_22(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 22,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_23(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "XXCRITICALXX": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_24(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "critical": 21,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_25(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 22,
    }
    return severity_map.get(level.upper(), 9)


def x_map_level_to_severity__mutmut_26(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(None, 9)


def x_map_level_to_severity__mutmut_27(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), None)


def x_map_level_to_severity__mutmut_28(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(9)


def x_map_level_to_severity__mutmut_29(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), )


def x_map_level_to_severity__mutmut_30(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.lower(), 9)


def x_map_level_to_severity__mutmut_31(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 10)

x_map_level_to_severity__mutmut_mutants : ClassVar[MutantDict] = {
'x_map_level_to_severity__mutmut_1': x_map_level_to_severity__mutmut_1, 
    'x_map_level_to_severity__mutmut_2': x_map_level_to_severity__mutmut_2, 
    'x_map_level_to_severity__mutmut_3': x_map_level_to_severity__mutmut_3, 
    'x_map_level_to_severity__mutmut_4': x_map_level_to_severity__mutmut_4, 
    'x_map_level_to_severity__mutmut_5': x_map_level_to_severity__mutmut_5, 
    'x_map_level_to_severity__mutmut_6': x_map_level_to_severity__mutmut_6, 
    'x_map_level_to_severity__mutmut_7': x_map_level_to_severity__mutmut_7, 
    'x_map_level_to_severity__mutmut_8': x_map_level_to_severity__mutmut_8, 
    'x_map_level_to_severity__mutmut_9': x_map_level_to_severity__mutmut_9, 
    'x_map_level_to_severity__mutmut_10': x_map_level_to_severity__mutmut_10, 
    'x_map_level_to_severity__mutmut_11': x_map_level_to_severity__mutmut_11, 
    'x_map_level_to_severity__mutmut_12': x_map_level_to_severity__mutmut_12, 
    'x_map_level_to_severity__mutmut_13': x_map_level_to_severity__mutmut_13, 
    'x_map_level_to_severity__mutmut_14': x_map_level_to_severity__mutmut_14, 
    'x_map_level_to_severity__mutmut_15': x_map_level_to_severity__mutmut_15, 
    'x_map_level_to_severity__mutmut_16': x_map_level_to_severity__mutmut_16, 
    'x_map_level_to_severity__mutmut_17': x_map_level_to_severity__mutmut_17, 
    'x_map_level_to_severity__mutmut_18': x_map_level_to_severity__mutmut_18, 
    'x_map_level_to_severity__mutmut_19': x_map_level_to_severity__mutmut_19, 
    'x_map_level_to_severity__mutmut_20': x_map_level_to_severity__mutmut_20, 
    'x_map_level_to_severity__mutmut_21': x_map_level_to_severity__mutmut_21, 
    'x_map_level_to_severity__mutmut_22': x_map_level_to_severity__mutmut_22, 
    'x_map_level_to_severity__mutmut_23': x_map_level_to_severity__mutmut_23, 
    'x_map_level_to_severity__mutmut_24': x_map_level_to_severity__mutmut_24, 
    'x_map_level_to_severity__mutmut_25': x_map_level_to_severity__mutmut_25, 
    'x_map_level_to_severity__mutmut_26': x_map_level_to_severity__mutmut_26, 
    'x_map_level_to_severity__mutmut_27': x_map_level_to_severity__mutmut_27, 
    'x_map_level_to_severity__mutmut_28': x_map_level_to_severity__mutmut_28, 
    'x_map_level_to_severity__mutmut_29': x_map_level_to_severity__mutmut_29, 
    'x_map_level_to_severity__mutmut_30': x_map_level_to_severity__mutmut_30, 
    'x_map_level_to_severity__mutmut_31': x_map_level_to_severity__mutmut_31
}

def map_level_to_severity(*args, **kwargs):
    result = _mutmut_trampoline(x_map_level_to_severity__mutmut_orig, x_map_level_to_severity__mutmut_mutants, args, kwargs)
    return result 

map_level_to_severity.__signature__ = _mutmut_signature(x_map_level_to_severity__mutmut_orig)
x_map_level_to_severity__mutmut_orig.__name__ = 'x_map_level_to_severity'


def x_add_trace_context_to_log_entry__mutmut_orig(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_1(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = None
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_2(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span or current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_3(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = None
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_4(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = None
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_5(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["XXtrace_idXX"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_6(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["TRACE_ID"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_7(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = None
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_8(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["XXspan_idXX"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_9(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["SPAN_ID"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_10(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = None
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_11(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = None
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_12(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["XXtrace_idXX"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_13(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["TRACE_ID"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_14(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = None
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_15(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["XXspan_idXX"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_16(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["SPAN_ID"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_17(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = None
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_18(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["XXtrace_idXX"] = trace_id
    except ImportError:
        pass


def x_add_trace_context_to_log_entry__mutmut_19(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["TRACE_ID"] = trace_id
    except ImportError:
        pass

x_add_trace_context_to_log_entry__mutmut_mutants : ClassVar[MutantDict] = {
'x_add_trace_context_to_log_entry__mutmut_1': x_add_trace_context_to_log_entry__mutmut_1, 
    'x_add_trace_context_to_log_entry__mutmut_2': x_add_trace_context_to_log_entry__mutmut_2, 
    'x_add_trace_context_to_log_entry__mutmut_3': x_add_trace_context_to_log_entry__mutmut_3, 
    'x_add_trace_context_to_log_entry__mutmut_4': x_add_trace_context_to_log_entry__mutmut_4, 
    'x_add_trace_context_to_log_entry__mutmut_5': x_add_trace_context_to_log_entry__mutmut_5, 
    'x_add_trace_context_to_log_entry__mutmut_6': x_add_trace_context_to_log_entry__mutmut_6, 
    'x_add_trace_context_to_log_entry__mutmut_7': x_add_trace_context_to_log_entry__mutmut_7, 
    'x_add_trace_context_to_log_entry__mutmut_8': x_add_trace_context_to_log_entry__mutmut_8, 
    'x_add_trace_context_to_log_entry__mutmut_9': x_add_trace_context_to_log_entry__mutmut_9, 
    'x_add_trace_context_to_log_entry__mutmut_10': x_add_trace_context_to_log_entry__mutmut_10, 
    'x_add_trace_context_to_log_entry__mutmut_11': x_add_trace_context_to_log_entry__mutmut_11, 
    'x_add_trace_context_to_log_entry__mutmut_12': x_add_trace_context_to_log_entry__mutmut_12, 
    'x_add_trace_context_to_log_entry__mutmut_13': x_add_trace_context_to_log_entry__mutmut_13, 
    'x_add_trace_context_to_log_entry__mutmut_14': x_add_trace_context_to_log_entry__mutmut_14, 
    'x_add_trace_context_to_log_entry__mutmut_15': x_add_trace_context_to_log_entry__mutmut_15, 
    'x_add_trace_context_to_log_entry__mutmut_16': x_add_trace_context_to_log_entry__mutmut_16, 
    'x_add_trace_context_to_log_entry__mutmut_17': x_add_trace_context_to_log_entry__mutmut_17, 
    'x_add_trace_context_to_log_entry__mutmut_18': x_add_trace_context_to_log_entry__mutmut_18, 
    'x_add_trace_context_to_log_entry__mutmut_19': x_add_trace_context_to_log_entry__mutmut_19
}

def add_trace_context_to_log_entry(*args, **kwargs):
    result = _mutmut_trampoline(x_add_trace_context_to_log_entry__mutmut_orig, x_add_trace_context_to_log_entry__mutmut_mutants, args, kwargs)
    return result 

add_trace_context_to_log_entry.__signature__ = _mutmut_signature(x_add_trace_context_to_log_entry__mutmut_orig)
x_add_trace_context_to_log_entry__mutmut_orig.__name__ = 'x_add_trace_context_to_log_entry'


def x_build_log_entry__mutmut_orig(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_1(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = None

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_2(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "XX_timestampXX": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_3(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_TIMESTAMP": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_4(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(None),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_5(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() / 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_6(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1000001),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_7(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "XXlevelXX": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_8(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "LEVEL": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_9(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.lower(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_10(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "XXmessageXX": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_11(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "MESSAGE": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_12(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "XXserviceXX": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_13(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "SERVICE": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_14(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name and "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_15(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service and config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_16(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "XXfoundationXX",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_17(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "FOUNDATION",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_18(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(None)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def x_build_log_entry__mutmut_19(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(None)
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


def x_build_bulk_url__mutmut_orig(client: Any) -> str:
    """Build the bulk API URL for the client.

    Args:
        client: OpenObserve client instance

    Returns:
        Bulk API URL
    """
    if f"/api/{client.organization}" in client.url:
        return f"{client.url}/_bulk"
    return f"{client.url}/api/{client.organization}/_bulk"


def x_build_bulk_url__mutmut_1(client: Any) -> str:
    """Build the bulk API URL for the client.

    Args:
        client: OpenObserve client instance

    Returns:
        Bulk API URL
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


__all__ = [
    "add_trace_attributes",
    "add_trace_context_to_log_entry",
    "build_bulk_url",
    "build_log_entry",
    "configure_otlp_exporter",
    "create_otlp_resource",
    "map_level_to_severity",
]


# <3 🧱🤝🔌🪄
