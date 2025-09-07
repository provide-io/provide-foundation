"""
Transport configuration with Foundation config integration.
"""

import os

from attrs import define

from provide.foundation.config import BaseConfig, field
from provide.foundation.config.loader import RuntimeConfigLoader
from provide.foundation.config.manager import register_config
from provide.foundation.config.types import ConfigSource
from provide.foundation.logger import get_logger

log = get_logger(__name__)


@define(slots=True, repr=False)
class TransportConfig(BaseConfig):
    """Base configuration for all transports."""
    
    timeout: float = field(
        default=30.0,
        env_var="PROVIDE_TRANSPORT_TIMEOUT",
        description="Request timeout in seconds",
    )
    max_retries: int = field(
        default=3,
        env_var="PROVIDE_TRANSPORT_MAX_RETRIES",
        description="Maximum number of retry attempts",
    )
    retry_backoff_factor: float = field(
        default=0.5,
        env_var="PROVIDE_TRANSPORT_RETRY_BACKOFF_FACTOR", 
        description="Backoff multiplier for retries",
    )
    verify_ssl: bool = field(
        default=True,
        env_var="PROVIDE_TRANSPORT_VERIFY_SSL",
        description="Whether to verify SSL certificates",
    )
    
    @classmethod
    def from_env(cls, strict: bool = True) -> "TransportConfig":
        """Load configuration from environment variables."""
        config_dict = {}
        
        if timeout := os.getenv("PROVIDE_TRANSPORT_TIMEOUT"):
            try:
                config_dict["timeout"] = float(timeout)
            except ValueError:
                if strict:
                    log.warning(
                        "Invalid transport timeout value, using field default",
                        invalid_value=timeout,
                    )
        
        if max_retries := os.getenv("PROVIDE_TRANSPORT_MAX_RETRIES"):
            try:
                config_dict["max_retries"] = int(max_retries)
            except ValueError:
                if strict:
                    log.warning(
                        "Invalid max retries value, using field default",
                        invalid_value=max_retries,
                    )
        
        if backoff := os.getenv("PROVIDE_TRANSPORT_RETRY_BACKOFF_FACTOR"):
            try:
                config_dict["retry_backoff_factor"] = float(backoff)
            except ValueError:
                if strict:
                    log.warning(
                        "Invalid backoff factor value, using field default",
                        invalid_value=backoff,
                    )
        
        if verify_ssl := os.getenv("PROVIDE_TRANSPORT_VERIFY_SSL"):
            config_dict["verify_ssl"] = verify_ssl.lower() == "true"
        
        config = cls.from_dict(config_dict, source=ConfigSource.ENV)
        log.trace("Loaded transport configuration from environment", config_dict=config_dict)
        return config


@define(slots=True, repr=False)
class HTTPConfig(TransportConfig):
    """HTTP-specific configuration."""
    
    pool_connections: int = field(
        default=10,
        env_var="PROVIDE_HTTP_POOL_CONNECTIONS",
        description="Number of connection pools to cache",
    )
    pool_maxsize: int = field(
        default=100,
        env_var="PROVIDE_HTTP_POOL_MAXSIZE", 
        description="Maximum number of connections per pool",
    )
    follow_redirects: bool = field(
        default=True,
        env_var="PROVIDE_HTTP_FOLLOW_REDIRECTS",
        description="Whether to automatically follow redirects",
    )
    http2: bool = field(
        default=False,
        env_var="PROVIDE_HTTP_USE_HTTP2",
        description="Enable HTTP/2 support",
    )
    max_redirects: int = field(
        default=5,
        env_var="PROVIDE_HTTP_MAX_REDIRECTS",
        description="Maximum number of redirects to follow",
    )
    
    @classmethod
    def from_env(cls, strict: bool = True) -> "HTTPConfig":
        """Load HTTP configuration from environment variables."""
        # Start with base transport config
        base_config = TransportConfig.from_env(strict=strict)
        config_dict = base_config.to_dict(include_sensitive=True)
        
        # Add HTTP-specific settings
        if pool_connections := os.getenv("PROVIDE_HTTP_POOL_CONNECTIONS"):
            try:
                config_dict["pool_connections"] = int(pool_connections)
            except ValueError:
                if strict:
                    log.warning(
                        "Invalid pool connections value, using field default",
                        invalid_value=pool_connections,
                    )
        
        if pool_maxsize := os.getenv("PROVIDE_HTTP_POOL_MAXSIZE"):
            try:
                config_dict["pool_maxsize"] = int(pool_maxsize)
            except ValueError:
                if strict:
                    log.warning(
                        "Invalid pool maxsize value, using field default",
                        invalid_value=pool_maxsize,
                    )
        
        if follow_redirects := os.getenv("PROVIDE_HTTP_FOLLOW_REDIRECTS"):
            config_dict["follow_redirects"] = follow_redirects.lower() == "true"
        
        if http2 := os.getenv("PROVIDE_HTTP_USE_HTTP2"):
            config_dict["http2"] = http2.lower() == "true"
        
        if max_redirects := os.getenv("PROVIDE_HTTP_MAX_REDIRECTS"):
            try:
                config_dict["max_redirects"] = int(max_redirects)
            except ValueError:
                if strict:
                    log.warning(
                        "Invalid max redirects value, using field default",
                        invalid_value=max_redirects,
                    )
        
        config = cls.from_dict(config_dict, source=ConfigSource.ENV)
        log.trace("Loaded HTTP configuration from environment", config_dict=config_dict)
        return config


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