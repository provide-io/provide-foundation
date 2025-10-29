# provide/foundation/transport/config.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from attrs import define

from provide.foundation.config.base import field
from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_float_with_validation,
    validate_non_negative,
    validate_positive,
)
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.loader import RuntimeConfigLoader
from provide.foundation.config.manager import register_config
from provide.foundation.logger import get_logger
from provide.foundation.transport import defaults

"""Transport configuration with Foundation config integration."""

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


@define(slots=True, repr=False)
class TransportConfig(RuntimeConfig):
    """Base configuration for all transports."""

    timeout: float = field(
        default=defaults.DEFAULT_TRANSPORT_TIMEOUT,
        env_var="PROVIDE_TRANSPORT_TIMEOUT",
        converter=lambda x: parse_float_with_validation(x, min_val=0.0)
        if x
        else defaults.DEFAULT_TRANSPORT_TIMEOUT,
        validator=validate_positive,
        description="Request timeout in seconds",
    )
    max_retries: int = field(
        default=defaults.DEFAULT_TRANSPORT_MAX_RETRIES,
        env_var="PROVIDE_TRANSPORT_MAX_RETRIES",
        converter=int,
        validator=validate_non_negative,
        description="Maximum number of retry attempts",
    )
    retry_backoff_factor: float = field(
        default=defaults.DEFAULT_TRANSPORT_RETRY_BACKOFF_FACTOR,
        env_var="PROVIDE_TRANSPORT_RETRY_BACKOFF_FACTOR",
        converter=lambda x: parse_float_with_validation(x, min_val=0.0)
        if x
        else defaults.DEFAULT_TRANSPORT_RETRY_BACKOFF_FACTOR,
        validator=validate_non_negative,
        description="Backoff multiplier for retries",
    )
    verify_ssl: bool = field(
        default=defaults.DEFAULT_TRANSPORT_VERIFY_SSL,
        env_var="PROVIDE_TRANSPORT_VERIFY_SSL",
        converter=parse_bool_extended,
        description="Whether to verify SSL certificates",
    )


@define(slots=True, repr=False)
class HTTPConfig(TransportConfig):
    """HTTP-specific configuration."""

    pool_connections: int = field(
        default=defaults.DEFAULT_HTTP_POOL_CONNECTIONS,
        env_var="PROVIDE_HTTP_POOL_CONNECTIONS",
        converter=int,
        validator=validate_positive,
        description="Number of connection pools to cache",
    )
    pool_maxsize: int = field(
        default=defaults.DEFAULT_HTTP_POOL_MAXSIZE,
        env_var="PROVIDE_HTTP_POOL_MAXSIZE",
        converter=int,
        validator=validate_positive,
        description="Maximum number of connections per pool",
    )
    follow_redirects: bool = field(
        default=defaults.DEFAULT_HTTP_FOLLOW_REDIRECTS,
        env_var="PROVIDE_HTTP_FOLLOW_REDIRECTS",
        converter=parse_bool_extended,
        description="Whether to automatically follow redirects",
    )
    http2: bool = field(
        default=defaults.DEFAULT_HTTP_USE_HTTP2,
        env_var="PROVIDE_HTTP_USE_HTTP2",
        converter=parse_bool_extended,
        description="Enable HTTP/2 support",
    )
    max_redirects: int = field(
        default=defaults.DEFAULT_HTTP_MAX_REDIRECTS,
        env_var="PROVIDE_HTTP_MAX_REDIRECTS",
        converter=int,
        validator=validate_non_negative,
        description="Maximum number of redirects to follow",
    )


def x_register_transport_configs__mutmut_orig() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_1() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name=None,
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_2() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=None,
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_3() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults=None,
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_4() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_5() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_6() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_7() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_8() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="XXtransportXX",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_9() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="TRANSPORT",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_10() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix=None),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_11() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="XXPROVIDE_TRANSPORTXX"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_12() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="provide_transport"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_13() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "XXtimeoutXX": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_14() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "TIMEOUT": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_15() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 31.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_16() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "XXmax_retriesXX": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_17() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "MAX_RETRIES": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_18() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 4,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_19() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "XXretry_backoff_factorXX": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_20() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "RETRY_BACKOFF_FACTOR": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_21() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 1.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_22() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "XXverify_sslXX": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_23() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "VERIFY_SSL": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_24() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": False,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_25() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name=None,
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_26() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=None,
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_27() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults=None,
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_28() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_29() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_30() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_31() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_32() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="XXtransport.httpXX",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_33() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="TRANSPORT.HTTP",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_34() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix=None),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_35() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="XXPROVIDE_HTTPXX"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_36() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="provide_http"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_37() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "XXtimeoutXX": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_38() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "TIMEOUT": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_39() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 31.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_40() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "XXmax_retriesXX": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_41() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "MAX_RETRIES": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_42() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 4,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_43() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "XXretry_backoff_factorXX": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_44() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "RETRY_BACKOFF_FACTOR": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_45() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 1.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_46() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "XXverify_sslXX": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_47() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "VERIFY_SSL": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_48() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": False,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_49() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "XXpool_connectionsXX": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_50() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "POOL_CONNECTIONS": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_51() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 11,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_52() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "XXpool_maxsizeXX": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_53() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "POOL_MAXSIZE": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_54() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 101,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_55() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "XXfollow_redirectsXX": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_56() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "FOLLOW_REDIRECTS": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_57() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": False,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_58() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "XXhttp2XX": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_59() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "HTTP2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_60() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": True,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_61() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "XXmax_redirectsXX": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_62() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "MAX_REDIRECTS": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_63() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 6,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_64() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace(None)

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_65() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("XXSuccessfully registered transport configurations with ConfigManagerXX")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_66() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("successfully registered transport configurations with configmanager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_67() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("SUCCESSFULLY REGISTERED TRANSPORT CONFIGURATIONS WITH CONFIGMANAGER")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_68() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning(None, error=str(e))


def x_register_transport_configs__mutmut_69() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=None)


def x_register_transport_configs__mutmut_70() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning(error=str(e))


def x_register_transport_configs__mutmut_71() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning(
            "Failed to register transport configurations",
        )


def x_register_transport_configs__mutmut_72() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("XXFailed to register transport configurationsXX", error=str(e))


def x_register_transport_configs__mutmut_73() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("failed to register transport configurations", error=str(e))


def x_register_transport_configs__mutmut_74() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("FAILED TO REGISTER TRANSPORT CONFIGURATIONS", error=str(e))


def x_register_transport_configs__mutmut_75() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            },
        )

        # Register HTTPConfig
        register_config(
            name="transport.http",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_HTTP"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
                "pool_connections": 10,
                "pool_maxsize": 100,
                "follow_redirects": True,
                "http2": False,
                "max_redirects": 5,
            },
        )

        log.trace("Successfully registered transport configurations with ConfigManager")

    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(None))


x_register_transport_configs__mutmut_mutants: ClassVar[MutantDict] = {
    "x_register_transport_configs__mutmut_1": x_register_transport_configs__mutmut_1,
    "x_register_transport_configs__mutmut_2": x_register_transport_configs__mutmut_2,
    "x_register_transport_configs__mutmut_3": x_register_transport_configs__mutmut_3,
    "x_register_transport_configs__mutmut_4": x_register_transport_configs__mutmut_4,
    "x_register_transport_configs__mutmut_5": x_register_transport_configs__mutmut_5,
    "x_register_transport_configs__mutmut_6": x_register_transport_configs__mutmut_6,
    "x_register_transport_configs__mutmut_7": x_register_transport_configs__mutmut_7,
    "x_register_transport_configs__mutmut_8": x_register_transport_configs__mutmut_8,
    "x_register_transport_configs__mutmut_9": x_register_transport_configs__mutmut_9,
    "x_register_transport_configs__mutmut_10": x_register_transport_configs__mutmut_10,
    "x_register_transport_configs__mutmut_11": x_register_transport_configs__mutmut_11,
    "x_register_transport_configs__mutmut_12": x_register_transport_configs__mutmut_12,
    "x_register_transport_configs__mutmut_13": x_register_transport_configs__mutmut_13,
    "x_register_transport_configs__mutmut_14": x_register_transport_configs__mutmut_14,
    "x_register_transport_configs__mutmut_15": x_register_transport_configs__mutmut_15,
    "x_register_transport_configs__mutmut_16": x_register_transport_configs__mutmut_16,
    "x_register_transport_configs__mutmut_17": x_register_transport_configs__mutmut_17,
    "x_register_transport_configs__mutmut_18": x_register_transport_configs__mutmut_18,
    "x_register_transport_configs__mutmut_19": x_register_transport_configs__mutmut_19,
    "x_register_transport_configs__mutmut_20": x_register_transport_configs__mutmut_20,
    "x_register_transport_configs__mutmut_21": x_register_transport_configs__mutmut_21,
    "x_register_transport_configs__mutmut_22": x_register_transport_configs__mutmut_22,
    "x_register_transport_configs__mutmut_23": x_register_transport_configs__mutmut_23,
    "x_register_transport_configs__mutmut_24": x_register_transport_configs__mutmut_24,
    "x_register_transport_configs__mutmut_25": x_register_transport_configs__mutmut_25,
    "x_register_transport_configs__mutmut_26": x_register_transport_configs__mutmut_26,
    "x_register_transport_configs__mutmut_27": x_register_transport_configs__mutmut_27,
    "x_register_transport_configs__mutmut_28": x_register_transport_configs__mutmut_28,
    "x_register_transport_configs__mutmut_29": x_register_transport_configs__mutmut_29,
    "x_register_transport_configs__mutmut_30": x_register_transport_configs__mutmut_30,
    "x_register_transport_configs__mutmut_31": x_register_transport_configs__mutmut_31,
    "x_register_transport_configs__mutmut_32": x_register_transport_configs__mutmut_32,
    "x_register_transport_configs__mutmut_33": x_register_transport_configs__mutmut_33,
    "x_register_transport_configs__mutmut_34": x_register_transport_configs__mutmut_34,
    "x_register_transport_configs__mutmut_35": x_register_transport_configs__mutmut_35,
    "x_register_transport_configs__mutmut_36": x_register_transport_configs__mutmut_36,
    "x_register_transport_configs__mutmut_37": x_register_transport_configs__mutmut_37,
    "x_register_transport_configs__mutmut_38": x_register_transport_configs__mutmut_38,
    "x_register_transport_configs__mutmut_39": x_register_transport_configs__mutmut_39,
    "x_register_transport_configs__mutmut_40": x_register_transport_configs__mutmut_40,
    "x_register_transport_configs__mutmut_41": x_register_transport_configs__mutmut_41,
    "x_register_transport_configs__mutmut_42": x_register_transport_configs__mutmut_42,
    "x_register_transport_configs__mutmut_43": x_register_transport_configs__mutmut_43,
    "x_register_transport_configs__mutmut_44": x_register_transport_configs__mutmut_44,
    "x_register_transport_configs__mutmut_45": x_register_transport_configs__mutmut_45,
    "x_register_transport_configs__mutmut_46": x_register_transport_configs__mutmut_46,
    "x_register_transport_configs__mutmut_47": x_register_transport_configs__mutmut_47,
    "x_register_transport_configs__mutmut_48": x_register_transport_configs__mutmut_48,
    "x_register_transport_configs__mutmut_49": x_register_transport_configs__mutmut_49,
    "x_register_transport_configs__mutmut_50": x_register_transport_configs__mutmut_50,
    "x_register_transport_configs__mutmut_51": x_register_transport_configs__mutmut_51,
    "x_register_transport_configs__mutmut_52": x_register_transport_configs__mutmut_52,
    "x_register_transport_configs__mutmut_53": x_register_transport_configs__mutmut_53,
    "x_register_transport_configs__mutmut_54": x_register_transport_configs__mutmut_54,
    "x_register_transport_configs__mutmut_55": x_register_transport_configs__mutmut_55,
    "x_register_transport_configs__mutmut_56": x_register_transport_configs__mutmut_56,
    "x_register_transport_configs__mutmut_57": x_register_transport_configs__mutmut_57,
    "x_register_transport_configs__mutmut_58": x_register_transport_configs__mutmut_58,
    "x_register_transport_configs__mutmut_59": x_register_transport_configs__mutmut_59,
    "x_register_transport_configs__mutmut_60": x_register_transport_configs__mutmut_60,
    "x_register_transport_configs__mutmut_61": x_register_transport_configs__mutmut_61,
    "x_register_transport_configs__mutmut_62": x_register_transport_configs__mutmut_62,
    "x_register_transport_configs__mutmut_63": x_register_transport_configs__mutmut_63,
    "x_register_transport_configs__mutmut_64": x_register_transport_configs__mutmut_64,
    "x_register_transport_configs__mutmut_65": x_register_transport_configs__mutmut_65,
    "x_register_transport_configs__mutmut_66": x_register_transport_configs__mutmut_66,
    "x_register_transport_configs__mutmut_67": x_register_transport_configs__mutmut_67,
    "x_register_transport_configs__mutmut_68": x_register_transport_configs__mutmut_68,
    "x_register_transport_configs__mutmut_69": x_register_transport_configs__mutmut_69,
    "x_register_transport_configs__mutmut_70": x_register_transport_configs__mutmut_70,
    "x_register_transport_configs__mutmut_71": x_register_transport_configs__mutmut_71,
    "x_register_transport_configs__mutmut_72": x_register_transport_configs__mutmut_72,
    "x_register_transport_configs__mutmut_73": x_register_transport_configs__mutmut_73,
    "x_register_transport_configs__mutmut_74": x_register_transport_configs__mutmut_74,
    "x_register_transport_configs__mutmut_75": x_register_transport_configs__mutmut_75,
}


def register_transport_configs(*args, **kwargs):
    result = _mutmut_trampoline(
        x_register_transport_configs__mutmut_orig, x_register_transport_configs__mutmut_mutants, args, kwargs
    )
    return result


register_transport_configs.__signature__ = _mutmut_signature(x_register_transport_configs__mutmut_orig)
x_register_transport_configs__mutmut_orig.__name__ = "x_register_transport_configs"


__all__ = [
    "HTTPConfig",
    "TransportConfig",
    "register_transport_configs",
]


# <3 🧱🤝🚚🪄
