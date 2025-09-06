"""
Transport configuration with environment variable support.
"""

import os
from typing import Any

from attrs import define, field

from provide.foundation.logger import get_logger
from provide.foundation.transport.errors import TransportConfigurationError

log = get_logger(__name__)


@define(frozen=True)
class TransportConfig:
    """Base configuration for all transports."""
    
    timeout: float = field()
    max_retries: int = field()
    retry_backoff_factor: float = field()
    verify_ssl: bool = field()
    
    @classmethod
    def from_env(cls) -> "TransportConfig":
        """Load configuration from environment variables."""
        try:
            timeout = float(os.environ.get("TRANSPORT_TIMEOUT", "30.0"))
            max_retries = int(os.environ.get("TRANSPORT_MAX_RETRIES", "3"))
            retry_backoff_factor = float(os.environ.get("TRANSPORT_RETRY_BACKOFF_FACTOR", "0.5"))
            verify_ssl = os.environ.get("TRANSPORT_VERIFY_SSL", "true").lower() == "true"
            
            config = cls(
                timeout=timeout,
                max_retries=max_retries,
                retry_backoff_factor=retry_backoff_factor,
                verify_ssl=verify_ssl,
            )
            
            log.trace("Loaded transport configuration", config=config)
            return config
            
        except (ValueError, TypeError) as e:
            raise TransportConfigurationError(
                f"Invalid transport configuration: {e}"
            ) from e


@define(frozen=True) 
class HTTPConfig(TransportConfig):
    """HTTP-specific configuration."""
    
    pool_connections: int = field()
    pool_maxsize: int = field() 
    follow_redirects: bool = field()
    http2: bool = field()
    max_redirects: int = field()
    
    @classmethod
    def from_env(cls) -> "HTTPConfig":
        """Load HTTP configuration from environment variables."""
        try:
            # Get base transport config
            base_config = TransportConfig.from_env()
            
            # HTTP-specific settings
            pool_connections = int(os.environ.get("HTTP_POOL_CONNECTIONS", "10"))
            pool_maxsize = int(os.environ.get("HTTP_POOL_MAXSIZE", "100"))
            follow_redirects = os.environ.get("HTTP_FOLLOW_REDIRECTS", "true").lower() == "true"
            http2 = os.environ.get("HTTP_USE_HTTP2", "false").lower() == "true"
            max_redirects = int(os.environ.get("HTTP_MAX_REDIRECTS", "5"))
            
            config = cls(
                timeout=base_config.timeout,
                max_retries=base_config.max_retries,
                retry_backoff_factor=base_config.retry_backoff_factor,
                verify_ssl=base_config.verify_ssl,
                pool_connections=pool_connections,
                pool_maxsize=pool_maxsize,
                follow_redirects=follow_redirects,
                http2=http2,
                max_redirects=max_redirects,
            )
            
            log.trace("Loaded HTTP configuration", config=config)
            return config
            
        except (ValueError, TypeError) as e:
            raise TransportConfigurationError(
                f"Invalid HTTP configuration: {e}"
            ) from e


def get_config_value(key: str, default: Any = None, type_func: type = str) -> Any:
    """
    Get configuration value from environment with type conversion.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        type_func: Function to convert string value to desired type
        
    Returns:
        Converted configuration value
        
    Raises:
        TransportConfigurationError: If value conversion fails
    """
    value = os.environ.get(key)
    
    if value is None:
        if default is None:
            raise TransportConfigurationError(
                f"Required configuration '{key}' not found in environment"
            )
        return default
    
    if type_func == bool:
        return value.lower() in ("true", "1", "yes", "on")
    
    try:
        return type_func(value)
    except (ValueError, TypeError) as e:
        raise TransportConfigurationError(
            f"Invalid value for '{key}': {value} (expected {type_func.__name__})"
        ) from e


__all__ = [
    "TransportConfig",
    "HTTPConfig",
    "get_config_value",
]