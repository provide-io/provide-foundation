# provide/foundation/logger/otlp/resource.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""OpenTelemetry Resource creation and service attribute management.

Provides functions for building OTLP Resource instances with standard service
attributes according to the OpenTelemetry specification.

Reference: https://opentelemetry.io/docs/specs/otel/resource/semantic_conventions/
"""

from __future__ import annotations

from typing import Any
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


def x_build_resource_attributes__mutmut_orig(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_1(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = None

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_2(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "XXservice.nameXX": service_name,
    }

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_3(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "SERVICE.NAME": service_name,
    }

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_4(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["service.version"] = None

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_5(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["XXservice.versionXX"] = service_version

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_6(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["SERVICE.VERSION"] = service_version

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_7(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["deployment.environment"] = None

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_8(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["XXdeployment.environmentXX"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_9(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["DEPLOYMENT.ENVIRONMENT"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def x_build_resource_attributes__mutmut_10(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(None)

    return attrs

x_build_resource_attributes__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_resource_attributes__mutmut_1': x_build_resource_attributes__mutmut_1, 
    'x_build_resource_attributes__mutmut_2': x_build_resource_attributes__mutmut_2, 
    'x_build_resource_attributes__mutmut_3': x_build_resource_attributes__mutmut_3, 
    'x_build_resource_attributes__mutmut_4': x_build_resource_attributes__mutmut_4, 
    'x_build_resource_attributes__mutmut_5': x_build_resource_attributes__mutmut_5, 
    'x_build_resource_attributes__mutmut_6': x_build_resource_attributes__mutmut_6, 
    'x_build_resource_attributes__mutmut_7': x_build_resource_attributes__mutmut_7, 
    'x_build_resource_attributes__mutmut_8': x_build_resource_attributes__mutmut_8, 
    'x_build_resource_attributes__mutmut_9': x_build_resource_attributes__mutmut_9, 
    'x_build_resource_attributes__mutmut_10': x_build_resource_attributes__mutmut_10
}

def build_resource_attributes(*args, **kwargs):
    result = _mutmut_trampoline(x_build_resource_attributes__mutmut_orig, x_build_resource_attributes__mutmut_mutants, args, kwargs)
    return result 

build_resource_attributes.__signature__ = _mutmut_signature(x_build_resource_attributes__mutmut_orig)
x_build_resource_attributes__mutmut_orig.__name__ = 'x_build_resource_attributes'


def x_create_otlp_resource__mutmut_orig(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        service_version=service_version,
        environment=environment,
        additional_attrs=additional_attrs,
    )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_1(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = None

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_2(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=None,
        service_version=service_version,
        environment=environment,
        additional_attrs=additional_attrs,
    )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_3(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        service_version=None,
        environment=environment,
        additional_attrs=additional_attrs,
    )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_4(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        service_version=service_version,
        environment=None,
        additional_attrs=additional_attrs,
    )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_5(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        service_version=service_version,
        environment=environment,
        additional_attrs=None,
    )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_6(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_version=service_version,
        environment=environment,
        additional_attrs=additional_attrs,
    )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_7(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        environment=environment,
        additional_attrs=additional_attrs,
    )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_8(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        service_version=service_version,
        additional_attrs=additional_attrs,
    )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_9(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        service_version=service_version,
        environment=environment,
        )

    return Resource.create(attrs)


def x_create_otlp_resource__mutmut_10(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        service_version=service_version,
        environment=environment,
        additional_attrs=additional_attrs,
    )

    return Resource.create(None)

x_create_otlp_resource__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_otlp_resource__mutmut_1': x_create_otlp_resource__mutmut_1, 
    'x_create_otlp_resource__mutmut_2': x_create_otlp_resource__mutmut_2, 
    'x_create_otlp_resource__mutmut_3': x_create_otlp_resource__mutmut_3, 
    'x_create_otlp_resource__mutmut_4': x_create_otlp_resource__mutmut_4, 
    'x_create_otlp_resource__mutmut_5': x_create_otlp_resource__mutmut_5, 
    'x_create_otlp_resource__mutmut_6': x_create_otlp_resource__mutmut_6, 
    'x_create_otlp_resource__mutmut_7': x_create_otlp_resource__mutmut_7, 
    'x_create_otlp_resource__mutmut_8': x_create_otlp_resource__mutmut_8, 
    'x_create_otlp_resource__mutmut_9': x_create_otlp_resource__mutmut_9, 
    'x_create_otlp_resource__mutmut_10': x_create_otlp_resource__mutmut_10
}

def create_otlp_resource(*args, **kwargs):
    result = _mutmut_trampoline(x_create_otlp_resource__mutmut_orig, x_create_otlp_resource__mutmut_mutants, args, kwargs)
    return result 

create_otlp_resource.__signature__ = _mutmut_signature(x_create_otlp_resource__mutmut_orig)
x_create_otlp_resource__mutmut_orig.__name__ = 'x_create_otlp_resource'


__all__ = [
    "build_resource_attributes",
    "create_otlp_resource",
]


# <3 🧱🤝📝🪄
