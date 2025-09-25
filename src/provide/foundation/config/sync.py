from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from concurrent.futures import Future
from pathlib import Path
import threading
from typing import Any, TypeVar

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.loader import (
    ConfigLoader,
    DictConfigLoader,
    FileConfigLoader,
    MultiSourceLoader,
)
from provide.foundation.config.manager import ConfigManager
from provide.foundation.config.types import ConfigDict, ConfigSource

"""Synchronous wrappers for the async configuration system.

These wrappers allow using the async config system in synchronous contexts
like CLI tools, scripts, and frameworks that don't support async.
"""

T = TypeVar("T", bound=BaseConfig)


def _run_coro_from_sync(coro: Awaitable[Any]) -> Any:
    """Run an async coroutine from a synchronous context safely.

    This function intelligently detects the environment:
    1. If no event loop is running, it creates one with `asyncio.run()`.
    2. If an event loop is running on another thread, it uses
       `asyncio.run_coroutine_threadsafe()` to schedule the coroutine.
    3. If an event loop is running on the *current* thread, it raises a
       RuntimeError to prevent misuse and guide the user to the async API.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Case 1: No running event loop. Safe to use asyncio.run().
        return asyncio.run(coro)

    # Case 2 & 3: An event loop is running.
    if loop.is_running():
        current_thread = threading.current_thread()
        loop_thread = getattr(loop, "_thread_id", None)  # Not public, but a common attribute

        # Check if we are in the loop's thread.
        # This is not perfectly reliable but works for common asyncio implementations.
        is_loop_thread = loop_thread is not None and current_thread.ident == loop_thread

        if is_loop_thread:
            # Case 3: Running on the same thread as the loop. This is an anti-pattern.
            raise RuntimeError(
                "Cannot call synchronous wrapper from a running event loop. "
                "Use the 'async' version of the function instead."
            )
        else:
            # Case 2: Running in a different thread. Use run_coroutine_threadsafe.
            future: Future = asyncio.run_coroutine_threadsafe(coro, loop)
            return future.result()  # Blocks until the coroutine is done.

    # Fallback for loops that are not running, though this case is rare.
    return asyncio.run(coro)


def run_async(coro: Any) -> Any:
    """Run an async coroutine in a sync context.

    Creates a new event loop if needed or uses the existing one safely.
    """
    return _run_coro_from_sync(coro)


def load_config(
    config_class: type[T],
    data: ConfigDict | None = None,
    source: ConfigSource = ConfigSource.RUNTIME,
) -> T:
    """Load configuration from dictionary (sync wrapper).

    Args:
        config_class: Configuration class
        data: Configuration data
        source: Source of the configuration

    Returns:
        Configuration instance

    """
    if data is None:
        data = {}
    # BaseConfig.from_dict is not async, so no wrapper needed here.
    return config_class.from_dict(data, source)


def load_config_from_env(
    config_class: type[T],
    prefix: str = "",
    delimiter: str = "_",
    case_sensitive: bool = False,
) -> T:
    """Load configuration from environment variables (sync wrapper).

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

    # The async version handles async secret fetching, so we wrap it.
    return run_async(
        config_class.from_env_async(
            prefix=prefix,
            delimiter=delimiter,
            case_sensitive=case_sensitive,
        ),
    )


def load_config_from_file(
    path: str | Path,
    config_class: type[T],
    format: str | None = None,
    encoding: str = "utf-8",
) -> T:
    """Load configuration from file (sync wrapper).

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
    """Load configuration from multiple sources (sync wrapper).

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
    """Validate a configuration instance (sync wrapper).

    Args:
        config: Configuration instance to validate

    """
    run_async(config.validate())


def update_config(
    config: BaseConfig,
    updates: ConfigDict,
    source: ConfigSource = ConfigSource.RUNTIME,
) -> None:
    """Update configuration with new values (sync wrapper).

    Args:
        config: Configuration instance
        updates: Dictionary of updates
        source: Source of the updates

    """
    # BaseConfig.update is not async
    config.update(updates, source)


def config_to_dict(config: BaseConfig, include_sensitive: bool = False) -> ConfigDict:
    """Convert configuration to dictionary (sync wrapper).

    Args:
        config: Configuration instance
        include_sensitive: Whether to include sensitive fields

    Returns:
        Dictionary representation

    """
    # BaseConfig.to_dict is not async
    return config.to_dict(include_sensitive)


def clone_config(config: T) -> T:
    """Create a deep copy of configuration (sync wrapper).

    Args:
        config: Configuration instance

    Returns:
        Cloned configuration

    """
    # BaseConfig.clone is not async
    return config.clone()


def diff_configs(config1: BaseConfig, config2: BaseConfig) -> dict[str, tuple[Any, Any]]:
    """Compare two configurations (sync wrapper).

    Args:
        config1: First configuration
        config2: Second configuration

    Returns:
        Dictionary of differences

    """
    # BaseConfig.diff is not async
    return config1.diff(config2)


class SyncConfigManager:
    """Synchronous wrapper for ConfigManager.

    Provides a sync interface to the async ConfigManager.
    """

    def __init__(self, loader: ConfigLoader | None = None) -> None:
        """Initialize sync config manager.

        Args:
            loader: Optional config loader for loading configurations.

        """
        self._async_manager = ConfigManager()
        self._loader = loader

    def register(self, name: str, config: BaseConfig | None = None, **kwargs: Any) -> None:
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


def register_config(name: str, **kwargs: Any) -> None:
    """Register a configuration with the global sync manager."""
    sync_manager.register(name, **kwargs)
