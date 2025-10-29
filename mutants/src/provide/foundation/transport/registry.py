# provide/foundation/transport/registry.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.hub import get_component_registry
from provide.foundation.hub.components import ComponentCategory
from provide.foundation.logger import get_logger
from provide.foundation.transport.base import Transport
from provide.foundation.transport.errors import TransportNotFoundError
from provide.foundation.transport.types import TransportType

"""Transport registration and discovery using Foundation Hub."""

log = get_logger(__name__)
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


def x_register_transport__mutmut_orig(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_1(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = None

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_2(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is not None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_3(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = None

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_4(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=None,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_5(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=None,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_6(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=None,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_7(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata=None,
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_8(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=None,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_9(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_10(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_11(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_12(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_13(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_14(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "XXtransport_typeXX": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_15(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "TRANSPORT_TYPE": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_16(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "XXschemesXX": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_17(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "SCHEMES": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_18(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "XXclass_nameXX": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_19(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "CLASS_NAME": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def x_register_transport__mutmut_20(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=False,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


x_register_transport__mutmut_mutants: ClassVar[MutantDict] = {
    "x_register_transport__mutmut_1": x_register_transport__mutmut_1,
    "x_register_transport__mutmut_2": x_register_transport__mutmut_2,
    "x_register_transport__mutmut_3": x_register_transport__mutmut_3,
    "x_register_transport__mutmut_4": x_register_transport__mutmut_4,
    "x_register_transport__mutmut_5": x_register_transport__mutmut_5,
    "x_register_transport__mutmut_6": x_register_transport__mutmut_6,
    "x_register_transport__mutmut_7": x_register_transport__mutmut_7,
    "x_register_transport__mutmut_8": x_register_transport__mutmut_8,
    "x_register_transport__mutmut_9": x_register_transport__mutmut_9,
    "x_register_transport__mutmut_10": x_register_transport__mutmut_10,
    "x_register_transport__mutmut_11": x_register_transport__mutmut_11,
    "x_register_transport__mutmut_12": x_register_transport__mutmut_12,
    "x_register_transport__mutmut_13": x_register_transport__mutmut_13,
    "x_register_transport__mutmut_14": x_register_transport__mutmut_14,
    "x_register_transport__mutmut_15": x_register_transport__mutmut_15,
    "x_register_transport__mutmut_16": x_register_transport__mutmut_16,
    "x_register_transport__mutmut_17": x_register_transport__mutmut_17,
    "x_register_transport__mutmut_18": x_register_transport__mutmut_18,
    "x_register_transport__mutmut_19": x_register_transport__mutmut_19,
    "x_register_transport__mutmut_20": x_register_transport__mutmut_20,
}


def register_transport(*args, **kwargs):
    result = _mutmut_trampoline(
        x_register_transport__mutmut_orig, x_register_transport__mutmut_mutants, args, kwargs
    )
    return result


register_transport.__signature__ = _mutmut_signature(x_register_transport__mutmut_orig)
x_register_transport__mutmut_orig.__name__ = "x_register_transport"


def x_get_transport_for_scheme__mutmut_orig(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_1(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = None

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_2(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension != ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_3(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = None
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_4(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get(None, [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_5(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", None)
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_6(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get([])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_7(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get(
                "schemes",
            )
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_8(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("XXschemesXX", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_9(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("SCHEMES", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_10(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.upper() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_11(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() not in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_12(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(None)
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_13(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        None,
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_14(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=None,
    )


def x_get_transport_for_scheme__mutmut_15(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        scheme=scheme,
    )


def x_get_transport_for_scheme__mutmut_16(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
    )


x_get_transport_for_scheme__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_transport_for_scheme__mutmut_1": x_get_transport_for_scheme__mutmut_1,
    "x_get_transport_for_scheme__mutmut_2": x_get_transport_for_scheme__mutmut_2,
    "x_get_transport_for_scheme__mutmut_3": x_get_transport_for_scheme__mutmut_3,
    "x_get_transport_for_scheme__mutmut_4": x_get_transport_for_scheme__mutmut_4,
    "x_get_transport_for_scheme__mutmut_5": x_get_transport_for_scheme__mutmut_5,
    "x_get_transport_for_scheme__mutmut_6": x_get_transport_for_scheme__mutmut_6,
    "x_get_transport_for_scheme__mutmut_7": x_get_transport_for_scheme__mutmut_7,
    "x_get_transport_for_scheme__mutmut_8": x_get_transport_for_scheme__mutmut_8,
    "x_get_transport_for_scheme__mutmut_9": x_get_transport_for_scheme__mutmut_9,
    "x_get_transport_for_scheme__mutmut_10": x_get_transport_for_scheme__mutmut_10,
    "x_get_transport_for_scheme__mutmut_11": x_get_transport_for_scheme__mutmut_11,
    "x_get_transport_for_scheme__mutmut_12": x_get_transport_for_scheme__mutmut_12,
    "x_get_transport_for_scheme__mutmut_13": x_get_transport_for_scheme__mutmut_13,
    "x_get_transport_for_scheme__mutmut_14": x_get_transport_for_scheme__mutmut_14,
    "x_get_transport_for_scheme__mutmut_15": x_get_transport_for_scheme__mutmut_15,
    "x_get_transport_for_scheme__mutmut_16": x_get_transport_for_scheme__mutmut_16,
}


def get_transport_for_scheme(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_transport_for_scheme__mutmut_orig, x_get_transport_for_scheme__mutmut_mutants, args, kwargs
    )
    return result


get_transport_for_scheme.__signature__ = _mutmut_signature(x_get_transport_for_scheme__mutmut_orig)
x_get_transport_for_scheme__mutmut_orig.__name__ = "x_get_transport_for_scheme"


def x_get_transport__mutmut_orig(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = uri.split("://")[0].lower()
    transport_class = get_transport_for_scheme(scheme)
    return transport_class()


def x_get_transport__mutmut_1(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = None
    transport_class = get_transport_for_scheme(scheme)
    return transport_class()


def x_get_transport__mutmut_2(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = uri.split("://")[0].upper()
    transport_class = get_transport_for_scheme(scheme)
    return transport_class()


def x_get_transport__mutmut_3(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = uri.split(None)[0].lower()
    transport_class = get_transport_for_scheme(scheme)
    return transport_class()


def x_get_transport__mutmut_4(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = uri.split("XX://XX")[0].lower()
    transport_class = get_transport_for_scheme(scheme)
    return transport_class()


def x_get_transport__mutmut_5(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = uri.split("://")[1].lower()
    transport_class = get_transport_for_scheme(scheme)
    return transport_class()


def x_get_transport__mutmut_6(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = uri.split("://")[0].lower()
    transport_class = None
    return transport_class()


def x_get_transport__mutmut_7(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = uri.split("://")[0].lower()
    transport_class = get_transport_for_scheme(None)
    return transport_class()


x_get_transport__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_transport__mutmut_1": x_get_transport__mutmut_1,
    "x_get_transport__mutmut_2": x_get_transport__mutmut_2,
    "x_get_transport__mutmut_3": x_get_transport__mutmut_3,
    "x_get_transport__mutmut_4": x_get_transport__mutmut_4,
    "x_get_transport__mutmut_5": x_get_transport__mutmut_5,
    "x_get_transport__mutmut_6": x_get_transport__mutmut_6,
    "x_get_transport__mutmut_7": x_get_transport__mutmut_7,
}


def get_transport(*args, **kwargs):
    result = _mutmut_trampoline(x_get_transport__mutmut_orig, x_get_transport__mutmut_mutants, args, kwargs)
    return result


get_transport.__signature__ = _mutmut_signature(x_get_transport__mutmut_orig)
x_get_transport__mutmut_orig.__name__ = "x_get_transport"


def x_list_registered_transports__mutmut_orig() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_1() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = None
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_2() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = None

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_3() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension != ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_4() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = None

    return transports


def x_list_registered_transports__mutmut_5() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "XXclassXX": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_6() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "CLASS": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_7() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "XXschemesXX": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_8() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "SCHEMES": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_9() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get(None, []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_10() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", None),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_11() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get([]),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_12() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get(
                    "schemes",
                ),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_13() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("XXschemesXX", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_14() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("SCHEMES", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_15() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "XXtransport_typeXX": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_16() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "TRANSPORT_TYPE": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_17() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get(None),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_18() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("XXtransport_typeXX"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_19() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("TRANSPORT_TYPE"),
                "metadata": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_20() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "XXmetadataXX": entry.metadata,
            }

    return transports


def x_list_registered_transports__mutmut_21() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "METADATA": entry.metadata,
            }

    return transports


x_list_registered_transports__mutmut_mutants: ClassVar[MutantDict] = {
    "x_list_registered_transports__mutmut_1": x_list_registered_transports__mutmut_1,
    "x_list_registered_transports__mutmut_2": x_list_registered_transports__mutmut_2,
    "x_list_registered_transports__mutmut_3": x_list_registered_transports__mutmut_3,
    "x_list_registered_transports__mutmut_4": x_list_registered_transports__mutmut_4,
    "x_list_registered_transports__mutmut_5": x_list_registered_transports__mutmut_5,
    "x_list_registered_transports__mutmut_6": x_list_registered_transports__mutmut_6,
    "x_list_registered_transports__mutmut_7": x_list_registered_transports__mutmut_7,
    "x_list_registered_transports__mutmut_8": x_list_registered_transports__mutmut_8,
    "x_list_registered_transports__mutmut_9": x_list_registered_transports__mutmut_9,
    "x_list_registered_transports__mutmut_10": x_list_registered_transports__mutmut_10,
    "x_list_registered_transports__mutmut_11": x_list_registered_transports__mutmut_11,
    "x_list_registered_transports__mutmut_12": x_list_registered_transports__mutmut_12,
    "x_list_registered_transports__mutmut_13": x_list_registered_transports__mutmut_13,
    "x_list_registered_transports__mutmut_14": x_list_registered_transports__mutmut_14,
    "x_list_registered_transports__mutmut_15": x_list_registered_transports__mutmut_15,
    "x_list_registered_transports__mutmut_16": x_list_registered_transports__mutmut_16,
    "x_list_registered_transports__mutmut_17": x_list_registered_transports__mutmut_17,
    "x_list_registered_transports__mutmut_18": x_list_registered_transports__mutmut_18,
    "x_list_registered_transports__mutmut_19": x_list_registered_transports__mutmut_19,
    "x_list_registered_transports__mutmut_20": x_list_registered_transports__mutmut_20,
    "x_list_registered_transports__mutmut_21": x_list_registered_transports__mutmut_21,
}


def list_registered_transports(*args, **kwargs):
    result = _mutmut_trampoline(
        x_list_registered_transports__mutmut_orig, x_list_registered_transports__mutmut_mutants, args, kwargs
    )
    return result


list_registered_transports.__signature__ = _mutmut_signature(x_list_registered_transports__mutmut_orig)
x_list_registered_transports__mutmut_orig.__name__ = "x_list_registered_transports"


def x_get_transport_info__mutmut_orig(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_1(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = None

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_2(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension != ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_3(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name != scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_4(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "XXnameXX": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_5(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "NAME": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_6(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "XXclassXX": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_7(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "CLASS": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_8(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "XXschemesXX": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_9(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "SCHEMES": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_10(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get(None, []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_11(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", None),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_12(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get([]),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_13(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get(
                        "schemes",
                    ),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_14(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("XXschemesXX", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_15(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("SCHEMES", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_16(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "XXtransport_typeXX": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_17(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "TRANSPORT_TYPE": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_18(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get(None),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_19(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("XXtransport_typeXX"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_20(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("TRANSPORT_TYPE"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_21(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "XXmetadataXX": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_22(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "METADATA": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_23(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = None
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_24(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get(None, [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_25(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", None)
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_26(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get([])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_27(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get(
                "schemes",
            )
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_28(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("XXschemesXX", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_29(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("SCHEMES", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_30(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.upper() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_31(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() not in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_32(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "XXnameXX": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_33(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "NAME": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_34(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "XXclassXX": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_35(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "CLASS": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_36(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "XXschemesXX": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_37(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "SCHEMES": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_38(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "XXtransport_typeXX": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_39(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "TRANSPORT_TYPE": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_40(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get(None),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_41(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("XXtransport_typeXX"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_42(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("TRANSPORT_TYPE"),
                    "metadata": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_43(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "XXmetadataXX": entry.metadata,
                }

    return None


def x_get_transport_info__mutmut_44(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "METADATA": entry.metadata,
                }

    return None


x_get_transport_info__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_transport_info__mutmut_1": x_get_transport_info__mutmut_1,
    "x_get_transport_info__mutmut_2": x_get_transport_info__mutmut_2,
    "x_get_transport_info__mutmut_3": x_get_transport_info__mutmut_3,
    "x_get_transport_info__mutmut_4": x_get_transport_info__mutmut_4,
    "x_get_transport_info__mutmut_5": x_get_transport_info__mutmut_5,
    "x_get_transport_info__mutmut_6": x_get_transport_info__mutmut_6,
    "x_get_transport_info__mutmut_7": x_get_transport_info__mutmut_7,
    "x_get_transport_info__mutmut_8": x_get_transport_info__mutmut_8,
    "x_get_transport_info__mutmut_9": x_get_transport_info__mutmut_9,
    "x_get_transport_info__mutmut_10": x_get_transport_info__mutmut_10,
    "x_get_transport_info__mutmut_11": x_get_transport_info__mutmut_11,
    "x_get_transport_info__mutmut_12": x_get_transport_info__mutmut_12,
    "x_get_transport_info__mutmut_13": x_get_transport_info__mutmut_13,
    "x_get_transport_info__mutmut_14": x_get_transport_info__mutmut_14,
    "x_get_transport_info__mutmut_15": x_get_transport_info__mutmut_15,
    "x_get_transport_info__mutmut_16": x_get_transport_info__mutmut_16,
    "x_get_transport_info__mutmut_17": x_get_transport_info__mutmut_17,
    "x_get_transport_info__mutmut_18": x_get_transport_info__mutmut_18,
    "x_get_transport_info__mutmut_19": x_get_transport_info__mutmut_19,
    "x_get_transport_info__mutmut_20": x_get_transport_info__mutmut_20,
    "x_get_transport_info__mutmut_21": x_get_transport_info__mutmut_21,
    "x_get_transport_info__mutmut_22": x_get_transport_info__mutmut_22,
    "x_get_transport_info__mutmut_23": x_get_transport_info__mutmut_23,
    "x_get_transport_info__mutmut_24": x_get_transport_info__mutmut_24,
    "x_get_transport_info__mutmut_25": x_get_transport_info__mutmut_25,
    "x_get_transport_info__mutmut_26": x_get_transport_info__mutmut_26,
    "x_get_transport_info__mutmut_27": x_get_transport_info__mutmut_27,
    "x_get_transport_info__mutmut_28": x_get_transport_info__mutmut_28,
    "x_get_transport_info__mutmut_29": x_get_transport_info__mutmut_29,
    "x_get_transport_info__mutmut_30": x_get_transport_info__mutmut_30,
    "x_get_transport_info__mutmut_31": x_get_transport_info__mutmut_31,
    "x_get_transport_info__mutmut_32": x_get_transport_info__mutmut_32,
    "x_get_transport_info__mutmut_33": x_get_transport_info__mutmut_33,
    "x_get_transport_info__mutmut_34": x_get_transport_info__mutmut_34,
    "x_get_transport_info__mutmut_35": x_get_transport_info__mutmut_35,
    "x_get_transport_info__mutmut_36": x_get_transport_info__mutmut_36,
    "x_get_transport_info__mutmut_37": x_get_transport_info__mutmut_37,
    "x_get_transport_info__mutmut_38": x_get_transport_info__mutmut_38,
    "x_get_transport_info__mutmut_39": x_get_transport_info__mutmut_39,
    "x_get_transport_info__mutmut_40": x_get_transport_info__mutmut_40,
    "x_get_transport_info__mutmut_41": x_get_transport_info__mutmut_41,
    "x_get_transport_info__mutmut_42": x_get_transport_info__mutmut_42,
    "x_get_transport_info__mutmut_43": x_get_transport_info__mutmut_43,
    "x_get_transport_info__mutmut_44": x_get_transport_info__mutmut_44,
}


def get_transport_info(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_transport_info__mutmut_orig, x_get_transport_info__mutmut_mutants, args, kwargs
    )
    return result


get_transport_info.__signature__ = _mutmut_signature(x_get_transport_info__mutmut_orig)
x_get_transport_info__mutmut_orig.__name__ = "x_get_transport_info"


__all__ = [
    "get_transport",
    "get_transport_for_scheme",
    "get_transport_info",
    "list_registered_transports",
    "register_transport",
]


# <3 🧱🤝🚚🪄
