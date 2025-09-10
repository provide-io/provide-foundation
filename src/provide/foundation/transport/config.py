"""
Transport configuration with Foundation config integration.
"""

from attrs import define

from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.base import field
from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_float_with_validation,
    validate_non_negative,
    validate_positive,
)
from provide.foundation.config.loader import RuntimeConfigLoader
from provide.foundation.config.manager import register_config
from provide.foundation.logger import get_logger

log = get_logger(__name__)


@define(slots=True, repr=False)
class TransportConfig(RuntimeConfig):
    """Base configuration for all transports."""
    
    timeout: float = field(
        default=30.0,
        env_var="PROVIDE_TRANSPORT_TIMEOUT",
        converter=lambda x: parse_float_with_validation(x, min_val=0.0) if x else 30.0,
        validator=validate_positive,
        description="Request timeout in seconds",
    )
    max_retries: int = field(
        default=3,
        env_var="PROVIDE_TRANSPORT_MAX_RETRIES",
        converter=int,
        validator=validate_non_negative,
        description="Maximum number of retry attempts",
    )
    retry_backoff_factor: float = field(
        default=0.5,
        env_var="PROVIDE_TRANSPORT_RETRY_BACKOFF_FACTOR",
        converter=lambda x: parse_float_with_validation(x, min_val=0.0) if x else 0.5,
        validator=validate_non_negative,
        description="Backoff multiplier for retries",
    )
    verify_ssl: bool = field(
        default=True,
        env_var="PROVIDE_TRANSPORT_VERIFY_SSL",
        converter=parse_bool_extended,
        description="Whether to verify SSL certificates",
    )
    


@define(slots=True, repr=False)
class HTTPConfig(TransportConfig):
    """HTTP-specific configuration."""
    
    pool_connections: int = field(
        default=10,
        env_var="PROVIDE_HTTP_POOL_CONNECTIONS",
        converter=int,
        validator=validate_positive,
        description="Number of connection pools to cache",
    )
    pool_maxsize: int = field(
        default=100,
        env_var="PROVIDE_HTTP_POOL_MAXSIZE",
        converter=int,
        validator=validate_positive,
        description="Maximum number of connections per pool",
    )
    follow_redirects: bool = field(
        default=True,
        env_var="PROVIDE_HTTP_FOLLOW_REDIRECTS",
        converter=parse_bool_extended,
        description="Whether to automatically follow redirects",
    )
    http2: bool = field(
        default=False,
        env_var="PROVIDE_HTTP_USE_HTTP2",
        converter=parse_bool_extended,
        description="Enable HTTP/2 support",
    )
    max_redirects: int = field(
        default=5,
        env_var="PROVIDE_HTTP_MAX_REDIRECTS",
        converter=int,
        validator=validate_non_negative,
        description="Maximum number of redirects to follow",
    )
    


async def register_transport_configs() -> None:
    """Register transport configurations with the global ConfigManager."""
    try:
        # Register TransportConfig
        await register_config(
            name="transport",
            config=None,  # Will be loaded on demand
            loader=RuntimeConfigLoader(prefix="PROVIDE_TRANSPORT"),
            defaults={
                "timeout": 30.0,
                "max_retries": 3,
                "retry_backoff_factor": 0.5,
                "verify_ssl": True,
            }
        )
        
        # Register HTTPConfig  
        await register_config(
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
            }
        )
        
        log.trace("Successfully registered transport configurations with ConfigManager")
        
    except Exception as e:
        log.warning("Failed to register transport configurations", error=str(e))


__all__ = [
    "TransportConfig",
    "HTTPConfig",
    "register_transport_configs",
]