"""
Configuration loaders for various sources.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
from typing import TypeVar

try:
    import aiofiles
except ImportError:
    aiofiles = None

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.types import ConfigDict, ConfigFormat, ConfigSource
from provide.foundation.errors.config import ConfigurationError
from provide.foundation.errors.decorators import with_error_handling
from provide.foundation.errors.resources import NotFoundError
from provide.foundation.file.safe import safe_read_text

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
    ) -> None:
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
                raise ConfigurationError(
                    f"Cannot determine format for file: {self.path}",
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def exists(self) -> bool:
        """Check if configuration file exists."""
        return self.path.exists()

    @with_error_handling(
        context_provider=lambda: {"loader": "FileLoader"},
        error_mapper=lambda e: ConfigurationError(
            f"Failed to load configuration: {e}", code="CONFIG_LOAD_ERROR", cause=e
        )
        if not isinstance(e, ConfigurationError | NotFoundError)
        else e,
    )
    async def load(self, config_class: type[T]) -> T:
        """Load configuration from file."""
        if not self.exists():
            raise NotFoundError(
                f"Configuration file not found: {self.path}",
                code="CONFIG_FILE_NOT_FOUND",
                path=str(self.path),
            )

        data = await self._read_file()
        return config_class.from_dict(data, source=ConfigSource.FILE)

    async def _read_file(self) -> ConfigDict:
        """Read and parse configuration file."""
        if aiofiles:
            async with aiofiles.open(self.path, encoding=self.encoding) as f:
                content = await f.read()
        else:
            # Fallback to synchronous read using Foundation's safe file operations
            content = safe_read_text(self.path, encoding=self.encoding)
            if not content:
                raise ConfigurationError(
                    f"Failed to read config file: {self.path}",
                    code="CONFIG_READ_ERROR",
                    path=str(self.path),
                )

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
            raise ConfigurationError(
                f"Unsupported format: {self.format}",
                code="CONFIG_FORMAT_UNSUPPORTED",
                format=str(self.format),
            )

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
                key = key.strip().lower()  # Convert to lowercase for compatibility
                value = value.strip()

                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    value = value[1:-1]

                result[key] = value

        return result


class RuntimeConfigLoader(ConfigLoader):
    """Load configuration from environment variables."""

    def __init__(
        self, prefix: str = "", delimiter: str = "_", case_sensitive: bool = False
    ) -> None:
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
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )


class DictConfigLoader(ConfigLoader):
    """Load configuration from a dictionary."""

    def __init__(
        self, data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME
    ) -> None:
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
        return config_class.from_dict(self.data, source=self.source)


class MultiSourceLoader(ConfigLoader):
    """Load configuration from multiple sources with precedence."""

    def __init__(self, *loaders: ConfigLoader) -> None:
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
                    new_dict = new_config.to_dict(include_sensitive=True)
                    # Update each field with its proper source
                    for key, value in new_dict.items():
                        source = new_config.get_source(key)
                        if source is not None:
                            config.update({key: value}, source=source)

        return config


class ChainedLoader(ConfigLoader):
    """Try multiple loaders until one succeeds."""

    def __init__(self, *loaders: ConfigLoader) -> None:
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
