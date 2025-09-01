"""
Configuration loaders for various sources.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
from typing import TypeVar

import aiofiles

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.env import EnvConfig
from provide.foundation.config.types import ConfigDict, ConfigFormat, ConfigSource

T = TypeVar("T", bound=BaseConfig)


class ConfigLoader(ABC):
    """Abstract base class for configuration loaders."""

    @abstractmethod
    async def load(self, config_class: type[T]) -> T:
        """
        Load configuration.

        Args:
            config_class: Configuration class to instantiate

        Returns:
            Configuration instance
        """
        pass

    @abstractmethod
    def exists(self) -> bool:
        """
        Check if the configuration source exists.

        Returns:
            True if source exists
        """
        pass


class FileConfigLoader(ConfigLoader):
    """Load configuration from files."""

    def __init__(
        self,
        path: str | Path,
        format: ConfigFormat | None = None,
        encoding: str = "utf-8",
    ):
        """
        Initialize file configuration loader.

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
                raise ValueError(f"Cannot determine format for file: {self.path}")

        self.format = format

    def exists(self) -> bool:
        """Check if configuration file exists."""
        return self.path.exists()

    async def load(self, config_class: type[T]) -> T:
        """Load configuration from file."""
        if not self.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.path}")

        data = await self._read_file()
        return await config_class.from_dict(data, source=ConfigSource.FILE)

    async def _read_file(self) -> ConfigDict:
        """Read and parse configuration file."""
        async with aiofiles.open(self.path, encoding=self.encoding) as f:
            content = await f.read()

        if self.format == ConfigFormat.JSON:
            return json.loads(content)
        elif self.format == ConfigFormat.YAML:
            import yaml

            return yaml.safe_load(content)
        elif self.format == ConfigFormat.TOML:
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib
            return tomllib.loads(content)
        elif self.format == ConfigFormat.INI:
            import configparser

            parser = configparser.ConfigParser()
            parser.read_string(content)
            return self._ini_to_dict(parser)
        elif self.format == ConfigFormat.ENV:
            return self._parse_env_file(content)
        else:
            raise ValueError(f"Unsupported format: {self.format}")

    def _ini_to_dict(self, parser) -> ConfigDict:
        """Convert INI parser to dictionary."""
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))

        # Include DEFAULT section if present
        if parser.defaults():
            result["DEFAULT"] = dict(parser.defaults())

        return result

    def _parse_env_file(self, content: str) -> ConfigDict:
        """Parse .env file format."""
        result = {}

        for line in content.splitlines():
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Parse key=value
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                result[key] = value

        return result


class EnvConfigLoader(ConfigLoader):
    """Load configuration from environment variables."""

    def __init__(
        self, prefix: str = "", delimiter: str = "_", case_sensitive: bool = False
    ):
        """
        Initialize environment configuration loader.

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

    async def load(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, EnvConfig):
            raise TypeError(f"{config_class.__name__} must inherit from EnvConfig")

        return await config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )


class DictConfigLoader(ConfigLoader):
    """Load configuration from a dictionary."""

    def __init__(self, data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME):
        """
        Initialize dictionary configuration loader.

        Args:
            data: Configuration data
            source: Source of the configuration
        """
        self.data = data
        self.source = source

    def exists(self) -> bool:
        """Check if configuration data exists."""
        return self.data is not None

    async def load(self, config_class: type[T]) -> T:
        """Load configuration from dictionary."""
        return await config_class.from_dict(self.data, source=self.source)


class MultiSourceLoader(ConfigLoader):
    """Load configuration from multiple sources with precedence."""

    def __init__(self, *loaders: ConfigLoader):
        """
        Initialize multi-source configuration loader.

        Args:
            *loaders: Configuration loaders in order of precedence (later overrides earlier)
        """
        self.loaders = loaders

    def exists(self) -> bool:
        """Check if any configuration source exists."""
        return any(loader.exists() for loader in self.loaders)

    async def load(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("No configuration sources available")

        config = None

        for loader in self.loaders:
            if loader.exists():
                if config is None:
                    config = await loader.load(config_class)
                else:
                    # Load and merge
                    new_config = await loader.load(config_class)
                    new_dict = await new_config.to_dict(include_sensitive=True)
                    await config.update(
                        new_dict,
                        source=new_config._source_map.get("", ConfigSource.RUNTIME),
                    )

        return config


class ChainedLoader(ConfigLoader):
    """Try multiple loaders until one succeeds."""

    def __init__(self, *loaders: ConfigLoader):
        """
        Initialize chained configuration loader.

        Args:
            *loaders: Configuration loaders to try in order
        """
        self.loaders = loaders

    def exists(self) -> bool:
        """Check if any configuration source exists."""
        return any(loader.exists() for loader in self.loaders)

    async def load(self, config_class: type[T]) -> T:
        """Load configuration from first available source."""
        for loader in self.loaders:
            if loader.exists():
                return await loader.load(config_class)

        raise ValueError("No configuration source available")
