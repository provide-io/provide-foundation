"""
Synchronous wrappers for the async configuration system.

These wrappers allow using the async config system in synchronous contexts
like CLI tools, scripts, and frameworks that don't support async.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, TypeVar

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.loader import (
    DictConfigLoader,
    FileConfigLoader,
    MultiSourceLoader,
)
from provide.foundation.config.manager import ConfigManager
from provide.foundation.config.types import ConfigDict, ConfigSource
from provide.foundation.config.loader import ConfigLoader

T = TypeVar("T", bound=BaseConfig)


def run_async(coro):
    """
    Run an async coroutine in a sync context.

    Creates a new event loop if needed or uses the existing one.
    """
    try:
        # Try to get the current event loop
        asyncio.get_running_loop()
        # If we're here, we're already in an async context
        # This shouldn't happen in sync code, but handle it gracefully
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        # No event loop, create one
        return asyncio.run(coro)


def load_config(
    config_class: type[T],
    data: ConfigDict | None = None,
    source: ConfigSource = ConfigSource.RUNTIME,
) -> T:
    """
    Load configuration from dictionary (sync wrapper).

    Args:
        config_class: Configuration class
        data: Configuration data
        source: Source of the configuration

    Returns:
        Configuration instance
    """
    if data is None:
        data = {}
    return run_async(config_class.from_dict(data, source))


def load_config_from_env(
    config_class: type[T],
    prefix: str = "",
    delimiter: str = "_",
    case_sensitive: bool = False,
) -> T:
    """
    Load configuration from environment variables (sync wrapper).

    Args:
        config_class: Configuration class (must inherit from RuntimeConfig)
        prefix: Prefix for environment variables
        delimiter: Delimiter between prefix and field name
        case_sensitive: Whether variable names are case-sensitive

    Returns:
        Configuration instance
    """
    if not issubclass(config_class, RuntimeConfig):
        raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

    return run_async(
        config_class.from_env(
            prefix=prefix,
            delimiter=delimiter,
            case_sensitive=case_sensitive,
            use_async_secrets=False,  # Use sync I/O in sync context
        )
    )


def load_config_from_file(
    path: str | Path,
    config_class: type[T],
    format: str | None = None,
    encoding: str = "utf-8",
) -> T:
    """
    Load configuration from file (sync wrapper).

    Args:
        path: Path to configuration file
        config_class: Configuration class
        format: File format (auto-detected if None)
        encoding: File encoding

    Returns:
        Configuration instance
    """
    loader = FileConfigLoader(path, format=format, encoding=encoding)
    return run_async(loader.load(config_class))


def load_config_from_multiple(
    config_class: type[T],
    *sources: tuple[str, Any],
) -> T:
    """
    Load configuration from multiple sources (sync wrapper).

    Args:
        config_class: Configuration class
        *sources: Tuples of (source_type, source_data) where:
            - source_type: "file", "env", "dict"
            - source_data: Path for file, prefix for env, dict for dict

    Returns:
        Configuration instance merged from all sources
    """
    loaders = []

    for source_type, source_data in sources:
        if source_type == "file":
            loaders.append(FileConfigLoader(source_data))
        elif source_type == "env":
            from provide.foundation.config.loader import RuntimeConfigLoader

            loaders.append(RuntimeConfigLoader(prefix=source_data))
        elif source_type == "dict":
            loaders.append(DictConfigLoader(source_data))
        else:
            raise ValueError(f"Unknown source type: {source_type}")

    multi_loader = MultiSourceLoader(*loaders)
    return run_async(multi_loader.load(config_class))


def validate_config(config: BaseConfig) -> None:
    """
    Validate a configuration instance (sync wrapper).

    Args:
        config: Configuration instance to validate
    """
    run_async(config.validate())


def update_config(
    config: BaseConfig, updates: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME
) -> None:
    """
    Update configuration with new values (sync wrapper).

    Args:
        config: Configuration instance
        updates: Dictionary of updates
        source: Source of the updates
    """
    run_async(config.update(updates, source))


def config_to_dict(config: BaseConfig, include_sensitive: bool = False) -> ConfigDict:
    """
    Convert configuration to dictionary (sync wrapper).

    Args:
        config: Configuration instance
        include_sensitive: Whether to include sensitive fields

    Returns:
        Dictionary representation
    """
    return run_async(config.to_dict(include_sensitive))


def clone_config(config: T) -> T:
    """
    Create a deep copy of configuration (sync wrapper).

    Args:
        config: Configuration instance

    Returns:
        Cloned configuration
    """
    return run_async(config.clone())


def diff_configs(
    config1: BaseConfig, config2: BaseConfig
) -> dict[str, tuple[Any, Any]]:
    """
    Compare two configurations (sync wrapper).

    Args:
        config1: First configuration
        config2: Second configuration

    Returns:
        Dictionary of differences
    """
    return run_async(config1.diff(config2))


class SyncConfigManager:
    """
    Synchronous wrapper for ConfigManager.

    Provides a sync interface to the async ConfigManager.
    """

    def __init__(self, loader: ConfigLoader | None = None) -> None:
        """Initialize sync config manager.
        
        Args:
            loader: Optional config loader for loading configurations.
        """
        self._async_manager = ConfigManager()
        self._loader = loader

    def register(self, name: str, config: BaseConfig | None = None, **kwargs) -> None:
        """Register a configuration (sync)."""
        run_async(self._async_manager.register(name, config, **kwargs))

    def get(self, name: str) -> BaseConfig | None:
        """Get a configuration by name (sync)."""
        return run_async(self._async_manager.get(name))

    def load(self, name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
        """Load a configuration (sync).
        
        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)
            
        Returns:
            Configuration instance
        """
        return run_async(self._async_manager.load(name, config_class, loader))

    def update(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration (sync)."""
        run_async(self._async_manager.update(name, updates, source))

    def export(self, name: str, include_sensitive: bool = False) -> ConfigDict:
        """Export a configuration as dictionary (sync)."""
        return run_async(self._async_manager.export(name, include_sensitive))

    def export_all(self, include_sensitive: bool = False) -> dict[str, ConfigDict]:
        """Export all configurations (sync)."""
        return run_async(self._async_manager.export_all(include_sensitive))


# Global sync manager instance
sync_manager = SyncConfigManager()


# Convenience functions using the global sync manager
def get_config(name: str) -> BaseConfig | None:
    """Get a configuration from the global sync manager."""
    return sync_manager.get(name)


def set_config(name: str, config: BaseConfig) -> None:
    """Set a configuration in the global sync manager."""
    sync_manager.register(name, config=config)


def register_config(name: str, **kwargs) -> None:
    """Register a configuration with the global sync manager."""
    sync_manager.register(name, **kwargs)
