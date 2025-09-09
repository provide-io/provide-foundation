"""
Hub configuration management utilities.

Provides functions for resolving configuration values from registered sources,
loading configurations, and managing the configuration chain.
"""

import asyncio
import inspect
from typing import Any, TypeVar

from provide.foundation.errors.decorators import with_error_handling
from provide.foundation.hub.registry import RegistryEntry
from provide.foundation.logger import get_logger

T = TypeVar("T")

log = get_logger(__name__)


def _get_registry_and_lock():
    """Get registry and lock from components module."""
    from provide.foundation.hub.components import get_component_registry, _registry_lock, ComponentCategory
    return get_component_registry(), _registry_lock, ComponentCategory


@with_error_handling(fallback=None, suppress=(Exception,))
def resolve_config_value(key: str) -> Any:
    """Resolve configuration value using priority-ordered sources."""
    registry, registry_lock, ComponentCategory = _get_registry_and_lock()
    
    with registry_lock:
        # Get all config sources
        all_entries = list(registry)
        config_sources = [
            entry
            for entry in all_entries
            if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
        ]

        # Sort by priority (highest first)
        config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

        # Try each source
        for entry in config_sources:
            source = entry.value
            if hasattr(source, "get_value"):
                # Try to get value, continue on error
                try:
                    value = source.get_value(key)
                    if value is not None:
                        return value
                except Exception:
                    continue

        return None


def get_config_chain() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, registry_lock, ComponentCategory = _get_registry_and_lock()
    
    with registry_lock:
        # Get all config sources
        all_entries = list(registry)
        config_sources = [
            entry
            for entry in all_entries
            if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
        ]

        # Sort by priority (highest first)
        config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return config_sources


@with_error_handling(
    fallback={},
    context_provider=lambda: {"function": "load_all_configs"}
)
async def load_all_configs() -> dict[str, Any]:
    """Load configurations from all registered sources."""
    configs = {}
    chain = get_config_chain()

    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                if inspect.iscoroutinefunction(source.load_config):
                    source_config = await source.load_config()
                else:
                    source_config = source.load_config()

                if source_config:
                    configs.update(source_config)
            except Exception as e:
                log.warning(
                    "Config source failed to load", source=entry.name, error=str(e)
                )

    return configs


def load_config_from_registry(config_class: type[T]) -> T:
    """
    Load configuration from registry sources.
    
    Args:
        config_class: Configuration class to instantiate
        
    Returns:
        Configuration instance loaded from registry sources
    """
    registry, registry_lock, ComponentCategory = _get_registry_and_lock()
    
    with registry_lock:
        # Get configuration data from registry
        config_data = {}
        
        # Load from all config sources
        chain = get_config_chain()
        for entry in chain:
            source = entry.value
            if hasattr(source, "load_config"):
                try:
                    # Skip async sources in sync context
                    if inspect.iscoroutinefunction(source.load_config):
                        log.debug("Skipping async config source in sync context", source=entry.name)
                        continue
                    
                    source_data = source.load_config()
                    if source_data:
                        config_data.update(source_data)
                except Exception as e:
                    log.warning(
                        "Failed to load config from source", 
                        source=entry.name, 
                        error=str(e)
                    )
        
        # Create config instance
        return config_class.from_dict(config_data)


__all__ = [
    "resolve_config_value",
    "get_config_chain", 
    "load_all_configs",
    "load_config_from_registry",
]