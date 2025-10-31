#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import TypeVar

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.types import ConfigDict, ConfigFormat, ConfigSource
from provide.foundation.errors.config import ConfigurationError
from provide.foundation.errors.decorators import resilient
from provide.foundation.errors.resources import NotFoundError
from provide.foundation.file.safe import safe_read_text
from provide.foundation.serialization import env_loads, ini_loads, json_loads, toml_loads, yaml_loads

"""Configuration loaders for various sources."""

T = TypeVar("T", bound=BaseConfig)


class ConfigLoader(ABC):
    """Abstract base class for configuration loaders.

    Built-in implementations:
    - FileConfigLoader: YAML, JSON, TOML, .env files
    - RuntimeConfigLoader: Environment variables
    - DictConfigLoader: In-memory dictionaries

    For cloud secret managers (Vault, AWS Secrets, Azure Key Vault), implement
    custom loaders following this protocol.

    Examples: docs/guide/advanced/integration-patterns.md#custom-configuration-sources
    """

    @abstractmethod
    def load(self, config_class: type[T]) -> T:
        """Load configuration.

        Args:
            config_class: Configuration class to instantiate

        Returns:
            Configuration instance

        """

    @abstractmethod
    def exists(self) -> bool:
        """Check if the configuration source exists.

        Returns:
            True if source exists

        """


class FileConfigLoader(ConfigLoader):
    """Load configuration from files."""

    def __init__(
        self,
        path: str | Path,
        format: ConfigFormat | None = None,
        encoding: str = "utf-8",
    ) -> None:
        """Initialize file configuration loader.

        Args:
            path: Path to configuration file
            format: File format (auto-detected if None)
            encoding: File encoding

        """
        self.path = Path(path)
        self.encoding = encoding

        if format is None:
            format = ConfigFormat.from_extension(str(self.path))
            if format is None:
                raise ConfigurationError(
                    f"Cannot determine format for file: {self.path}",
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def exists(self) -> bool:
        """Check if configuration file exists."""
        return self.path.exists()

    @resilient(
        context_provider=lambda: {"loader": FileConfigLoader},
        error_mapper=lambda e: ConfigurationError(
            f"Failed to load configuration: {e}",
            code="CONFIG_LOAD_ERROR",
            cause=e,
        )
        if not isinstance(e, ConfigurationError | NotFoundError)
        else e,
    )
    def load(self, config_class: type[T]) -> T:
        """Load configuration from file."""
        from provide.foundation.logger.setup.coordinator import (
            create_foundation_internal_logger,
        )
        from provide.foundation.utils.timing import timed_block

        setup_logger = create_foundation_internal_logger()

        with timed_block(setup_logger, f"Load config from {self.path.name}"):
            if not self.exists():
                raise NotFoundError(
                    f"Configuration file not found: {self.path}",
                    code="CONFIG_FILE_NOT_FOUND",
                    path=str(self.path),
                )

            data = self._read_file()
            return config_class.from_dict(data, source=ConfigSource.FILE)

    def _read_file(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code="CONFIG_READ_ERROR",
                path=str(self.path),
            )

        if self.format == ConfigFormat.JSON:
            return json_loads(content)
        if self.format == ConfigFormat.YAML:
            data = yaml_loads(content)
            # yaml_loads returns None for empty content or comments-only files
            return data if data is not None else {}
        if self.format == ConfigFormat.TOML:
            return toml_loads(content)
        if self.format == ConfigFormat.INI:
            return ini_loads(content)  # type: ignore[return-value]
        if self.format == ConfigFormat.ENV:
            env_data = env_loads(content)
            # Lowercase keys for consistency with Python conventions
            return {key.lower(): value for key, value in env_data.items()}
        raise ConfigurationError(
            f"Unsupported format: {self.format}",
            code="CONFIG_FORMAT_UNSUPPORTED",
            format=str(self.format),
        )


class RuntimeConfigLoader(ConfigLoader):
    """Load configuration from environment variables."""

    def __init__(self, prefix: str = "", delimiter: str = "_", case_sensitive: bool = False) -> None:
        """Initialize environment configuration loader.

        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        """
        self.prefix = prefix
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive

    def exists(self) -> bool:
        """Check if any relevant environment variables exist."""
        if self.prefix:
            prefix_with_delim = f"{self.prefix}{self.delimiter}"
            return any(key.startswith(prefix_with_delim) for key in os.environ)
        return bool(os.environ)

    def load(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )


class DictConfigLoader(ConfigLoader):
    """Load configuration from a dictionary."""

    def __init__(self, data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME) -> None:
        """Initialize dictionary configuration loader.

        Args:
            data: Configuration data
            source: Source of the configuration

        """
        self.data = data
        self.source = source

    def exists(self) -> bool:
        """Check if configuration data exists."""
        return self.data is not None

    def load(self, config_class: type[T]) -> T:
        """Load configuration from dictionary."""
        return config_class.from_dict(self.data, source=self.source)


class MultiSourceLoader(ConfigLoader):
    """Load configuration from multiple sources with precedence."""

    def __init__(self, *loaders: ConfigLoader) -> None:
        """Initialize multi-source configuration loader.

        Args:
            *loaders: Configuration loaders in order of precedence (later overrides earlier)

        """
        self.loaders = loaders

    def exists(self) -> bool:
        """Check if any configuration source exists."""
        return any(loader.exists() for loader in self.loaders)

    def load(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("No configuration sources available")

        config = None

        for loader in self.loaders:
            if loader.exists():
                if config is None:
                    config = loader.load(config_class)
                else:
                    # Load and merge
                    new_config = loader.load(config_class)
                    new_dict = new_config.to_dict(include_sensitive=True)
                    # Update each field with its proper source
                    for key, value in new_dict.items():
                        source = new_config.get_source(key)
                        if source is not None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config


class ChainedLoader(ConfigLoader):
    """Try multiple loaders until one succeeds."""

    def __init__(self, *loaders: ConfigLoader) -> None:
        """Initialize chained configuration loader.

        Args:
            *loaders: Configuration loaders to try in order

        """
        self.loaders = loaders

    def exists(self) -> bool:
        """Check if any configuration source exists."""
        return any(loader.exists() for loader in self.loaders)

    def load(self, config_class: type[T]) -> T:
        """Load configuration from first available source."""
        for loader in self.loaders:
            if loader.exists():
                return loader.load(config_class)

        raise ValueError("No configuration source available")


# 🧱🏗️🔚
