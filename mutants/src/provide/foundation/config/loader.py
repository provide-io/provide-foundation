# provide/foundation/config/loader.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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

    def xǁFileConfigLoaderǁ__init____mutmut_orig(
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

    def xǁFileConfigLoaderǁ__init____mutmut_1(
        self,
        path: str | Path,
        format: ConfigFormat | None = None,
        encoding: str = "XXutf-8XX",
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

    def xǁFileConfigLoaderǁ__init____mutmut_2(
        self,
        path: str | Path,
        format: ConfigFormat | None = None,
        encoding: str = "UTF-8",
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

    def xǁFileConfigLoaderǁ__init____mutmut_3(
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
        self.path = None
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

    def xǁFileConfigLoaderǁ__init____mutmut_4(
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
        self.path = Path(None)
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

    def xǁFileConfigLoaderǁ__init____mutmut_5(
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
        self.encoding = None

        if format is None:
            format = ConfigFormat.from_extension(str(self.path))
            if format is None:
                raise ConfigurationError(
                    f"Cannot determine format for file: {self.path}",
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_6(
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

        if format is not None:
            format = ConfigFormat.from_extension(str(self.path))
            if format is None:
                raise ConfigurationError(
                    f"Cannot determine format for file: {self.path}",
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_7(
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
            format = None
            if format is None:
                raise ConfigurationError(
                    f"Cannot determine format for file: {self.path}",
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_8(
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
            format = ConfigFormat.from_extension(None)
            if format is None:
                raise ConfigurationError(
                    f"Cannot determine format for file: {self.path}",
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_9(
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
            format = ConfigFormat.from_extension(str(None))
            if format is None:
                raise ConfigurationError(
                    f"Cannot determine format for file: {self.path}",
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_10(
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
            if format is not None:
                raise ConfigurationError(
                    f"Cannot determine format for file: {self.path}",
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_11(
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
                    None,
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_12(
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
                    code=None,
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_13(
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
                    path=None,
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_14(
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
                    code="CONFIG_FORMAT_UNKNOWN",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_15(
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
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_16(
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
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_17(
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
                    code="XXCONFIG_FORMAT_UNKNOWNXX",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_18(
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
                    code="config_format_unknown",
                    path=str(self.path),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_19(
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
                    path=str(None),
                )

        self.format = format

    def xǁFileConfigLoaderǁ__init____mutmut_20(
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

        self.format = None

    xǁFileConfigLoaderǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileConfigLoaderǁ__init____mutmut_1": xǁFileConfigLoaderǁ__init____mutmut_1,
        "xǁFileConfigLoaderǁ__init____mutmut_2": xǁFileConfigLoaderǁ__init____mutmut_2,
        "xǁFileConfigLoaderǁ__init____mutmut_3": xǁFileConfigLoaderǁ__init____mutmut_3,
        "xǁFileConfigLoaderǁ__init____mutmut_4": xǁFileConfigLoaderǁ__init____mutmut_4,
        "xǁFileConfigLoaderǁ__init____mutmut_5": xǁFileConfigLoaderǁ__init____mutmut_5,
        "xǁFileConfigLoaderǁ__init____mutmut_6": xǁFileConfigLoaderǁ__init____mutmut_6,
        "xǁFileConfigLoaderǁ__init____mutmut_7": xǁFileConfigLoaderǁ__init____mutmut_7,
        "xǁFileConfigLoaderǁ__init____mutmut_8": xǁFileConfigLoaderǁ__init____mutmut_8,
        "xǁFileConfigLoaderǁ__init____mutmut_9": xǁFileConfigLoaderǁ__init____mutmut_9,
        "xǁFileConfigLoaderǁ__init____mutmut_10": xǁFileConfigLoaderǁ__init____mutmut_10,
        "xǁFileConfigLoaderǁ__init____mutmut_11": xǁFileConfigLoaderǁ__init____mutmut_11,
        "xǁFileConfigLoaderǁ__init____mutmut_12": xǁFileConfigLoaderǁ__init____mutmut_12,
        "xǁFileConfigLoaderǁ__init____mutmut_13": xǁFileConfigLoaderǁ__init____mutmut_13,
        "xǁFileConfigLoaderǁ__init____mutmut_14": xǁFileConfigLoaderǁ__init____mutmut_14,
        "xǁFileConfigLoaderǁ__init____mutmut_15": xǁFileConfigLoaderǁ__init____mutmut_15,
        "xǁFileConfigLoaderǁ__init____mutmut_16": xǁFileConfigLoaderǁ__init____mutmut_16,
        "xǁFileConfigLoaderǁ__init____mutmut_17": xǁFileConfigLoaderǁ__init____mutmut_17,
        "xǁFileConfigLoaderǁ__init____mutmut_18": xǁFileConfigLoaderǁ__init____mutmut_18,
        "xǁFileConfigLoaderǁ__init____mutmut_19": xǁFileConfigLoaderǁ__init____mutmut_19,
        "xǁFileConfigLoaderǁ__init____mutmut_20": xǁFileConfigLoaderǁ__init____mutmut_20,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFileConfigLoaderǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁFileConfigLoaderǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁFileConfigLoaderǁ__init____mutmut_orig)
    xǁFileConfigLoaderǁ__init____mutmut_orig.__name__ = "xǁFileConfigLoaderǁ__init__"

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

    def xǁFileConfigLoaderǁ_read_file__mutmut_orig(self) -> ConfigDict:
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_1(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = None
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_2(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(None, encoding=self.encoding)
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_3(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=None)
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_4(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(encoding=self.encoding)
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_5(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(
            self.path,
        )
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_6(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if content:
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_7(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                None,
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_8(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code=None,
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_9(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code="CONFIG_READ_ERROR",
                path=None,
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_10(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_11(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_12(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code="CONFIG_READ_ERROR",
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_13(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code="XXCONFIG_READ_ERRORXX",
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_14(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code="config_read_error",
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_15(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code="CONFIG_READ_ERROR",
                path=str(None),
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_16(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code="CONFIG_READ_ERROR",
                path=str(self.path),
            )

        if self.format != ConfigFormat.JSON:
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_17(self) -> ConfigDict:
        """Read and parse configuration file."""
        content = safe_read_text(self.path, encoding=self.encoding)
        if not content:
            raise ConfigurationError(
                f"Failed to read config file: {self.path}",
                code="CONFIG_READ_ERROR",
                path=str(self.path),
            )

        if self.format == ConfigFormat.JSON:
            return json_loads(None)
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_18(self) -> ConfigDict:
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
        if self.format != ConfigFormat.YAML:
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_19(self) -> ConfigDict:
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
            data = None
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_20(self) -> ConfigDict:
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
            data = yaml_loads(None)
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_21(self) -> ConfigDict:
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
            return data if data is None else {}
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_22(self) -> ConfigDict:
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
        if self.format != ConfigFormat.TOML:
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_23(self) -> ConfigDict:
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
            return toml_loads(None)
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_24(self) -> ConfigDict:
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
        if self.format != ConfigFormat.INI:
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

    def xǁFileConfigLoaderǁ_read_file__mutmut_25(self) -> ConfigDict:
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
            return ini_loads(None)  # type: ignore[return-value]
        if self.format == ConfigFormat.ENV:
            env_data = env_loads(content)
            # Lowercase keys for consistency with Python conventions
            return {key.lower(): value for key, value in env_data.items()}
        raise ConfigurationError(
            f"Unsupported format: {self.format}",
            code="CONFIG_FORMAT_UNSUPPORTED",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_26(self) -> ConfigDict:
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
        if self.format != ConfigFormat.ENV:
            env_data = env_loads(content)
            # Lowercase keys for consistency with Python conventions
            return {key.lower(): value for key, value in env_data.items()}
        raise ConfigurationError(
            f"Unsupported format: {self.format}",
            code="CONFIG_FORMAT_UNSUPPORTED",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_27(self) -> ConfigDict:
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
            env_data = None
            # Lowercase keys for consistency with Python conventions
            return {key.lower(): value for key, value in env_data.items()}
        raise ConfigurationError(
            f"Unsupported format: {self.format}",
            code="CONFIG_FORMAT_UNSUPPORTED",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_28(self) -> ConfigDict:
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
            env_data = env_loads(None)
            # Lowercase keys for consistency with Python conventions
            return {key.lower(): value for key, value in env_data.items()}
        raise ConfigurationError(
            f"Unsupported format: {self.format}",
            code="CONFIG_FORMAT_UNSUPPORTED",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_29(self) -> ConfigDict:
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
            return {key.upper(): value for key, value in env_data.items()}
        raise ConfigurationError(
            f"Unsupported format: {self.format}",
            code="CONFIG_FORMAT_UNSUPPORTED",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_30(self) -> ConfigDict:
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
            None,
            code="CONFIG_FORMAT_UNSUPPORTED",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_31(self) -> ConfigDict:
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
            code=None,
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_32(self) -> ConfigDict:
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
            format=None,
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_33(self) -> ConfigDict:
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
            code="CONFIG_FORMAT_UNSUPPORTED",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_34(self) -> ConfigDict:
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
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_35(self) -> ConfigDict:
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
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_36(self) -> ConfigDict:
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
            code="XXCONFIG_FORMAT_UNSUPPORTEDXX",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_37(self) -> ConfigDict:
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
            code="config_format_unsupported",
            format=str(self.format),
        )

    def xǁFileConfigLoaderǁ_read_file__mutmut_38(self) -> ConfigDict:
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
            format=str(None),
        )

    xǁFileConfigLoaderǁ_read_file__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileConfigLoaderǁ_read_file__mutmut_1": xǁFileConfigLoaderǁ_read_file__mutmut_1,
        "xǁFileConfigLoaderǁ_read_file__mutmut_2": xǁFileConfigLoaderǁ_read_file__mutmut_2,
        "xǁFileConfigLoaderǁ_read_file__mutmut_3": xǁFileConfigLoaderǁ_read_file__mutmut_3,
        "xǁFileConfigLoaderǁ_read_file__mutmut_4": xǁFileConfigLoaderǁ_read_file__mutmut_4,
        "xǁFileConfigLoaderǁ_read_file__mutmut_5": xǁFileConfigLoaderǁ_read_file__mutmut_5,
        "xǁFileConfigLoaderǁ_read_file__mutmut_6": xǁFileConfigLoaderǁ_read_file__mutmut_6,
        "xǁFileConfigLoaderǁ_read_file__mutmut_7": xǁFileConfigLoaderǁ_read_file__mutmut_7,
        "xǁFileConfigLoaderǁ_read_file__mutmut_8": xǁFileConfigLoaderǁ_read_file__mutmut_8,
        "xǁFileConfigLoaderǁ_read_file__mutmut_9": xǁFileConfigLoaderǁ_read_file__mutmut_9,
        "xǁFileConfigLoaderǁ_read_file__mutmut_10": xǁFileConfigLoaderǁ_read_file__mutmut_10,
        "xǁFileConfigLoaderǁ_read_file__mutmut_11": xǁFileConfigLoaderǁ_read_file__mutmut_11,
        "xǁFileConfigLoaderǁ_read_file__mutmut_12": xǁFileConfigLoaderǁ_read_file__mutmut_12,
        "xǁFileConfigLoaderǁ_read_file__mutmut_13": xǁFileConfigLoaderǁ_read_file__mutmut_13,
        "xǁFileConfigLoaderǁ_read_file__mutmut_14": xǁFileConfigLoaderǁ_read_file__mutmut_14,
        "xǁFileConfigLoaderǁ_read_file__mutmut_15": xǁFileConfigLoaderǁ_read_file__mutmut_15,
        "xǁFileConfigLoaderǁ_read_file__mutmut_16": xǁFileConfigLoaderǁ_read_file__mutmut_16,
        "xǁFileConfigLoaderǁ_read_file__mutmut_17": xǁFileConfigLoaderǁ_read_file__mutmut_17,
        "xǁFileConfigLoaderǁ_read_file__mutmut_18": xǁFileConfigLoaderǁ_read_file__mutmut_18,
        "xǁFileConfigLoaderǁ_read_file__mutmut_19": xǁFileConfigLoaderǁ_read_file__mutmut_19,
        "xǁFileConfigLoaderǁ_read_file__mutmut_20": xǁFileConfigLoaderǁ_read_file__mutmut_20,
        "xǁFileConfigLoaderǁ_read_file__mutmut_21": xǁFileConfigLoaderǁ_read_file__mutmut_21,
        "xǁFileConfigLoaderǁ_read_file__mutmut_22": xǁFileConfigLoaderǁ_read_file__mutmut_22,
        "xǁFileConfigLoaderǁ_read_file__mutmut_23": xǁFileConfigLoaderǁ_read_file__mutmut_23,
        "xǁFileConfigLoaderǁ_read_file__mutmut_24": xǁFileConfigLoaderǁ_read_file__mutmut_24,
        "xǁFileConfigLoaderǁ_read_file__mutmut_25": xǁFileConfigLoaderǁ_read_file__mutmut_25,
        "xǁFileConfigLoaderǁ_read_file__mutmut_26": xǁFileConfigLoaderǁ_read_file__mutmut_26,
        "xǁFileConfigLoaderǁ_read_file__mutmut_27": xǁFileConfigLoaderǁ_read_file__mutmut_27,
        "xǁFileConfigLoaderǁ_read_file__mutmut_28": xǁFileConfigLoaderǁ_read_file__mutmut_28,
        "xǁFileConfigLoaderǁ_read_file__mutmut_29": xǁFileConfigLoaderǁ_read_file__mutmut_29,
        "xǁFileConfigLoaderǁ_read_file__mutmut_30": xǁFileConfigLoaderǁ_read_file__mutmut_30,
        "xǁFileConfigLoaderǁ_read_file__mutmut_31": xǁFileConfigLoaderǁ_read_file__mutmut_31,
        "xǁFileConfigLoaderǁ_read_file__mutmut_32": xǁFileConfigLoaderǁ_read_file__mutmut_32,
        "xǁFileConfigLoaderǁ_read_file__mutmut_33": xǁFileConfigLoaderǁ_read_file__mutmut_33,
        "xǁFileConfigLoaderǁ_read_file__mutmut_34": xǁFileConfigLoaderǁ_read_file__mutmut_34,
        "xǁFileConfigLoaderǁ_read_file__mutmut_35": xǁFileConfigLoaderǁ_read_file__mutmut_35,
        "xǁFileConfigLoaderǁ_read_file__mutmut_36": xǁFileConfigLoaderǁ_read_file__mutmut_36,
        "xǁFileConfigLoaderǁ_read_file__mutmut_37": xǁFileConfigLoaderǁ_read_file__mutmut_37,
        "xǁFileConfigLoaderǁ_read_file__mutmut_38": xǁFileConfigLoaderǁ_read_file__mutmut_38,
    }

    def _read_file(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFileConfigLoaderǁ_read_file__mutmut_orig"),
            object.__getattribute__(self, "xǁFileConfigLoaderǁ_read_file__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _read_file.__signature__ = _mutmut_signature(xǁFileConfigLoaderǁ_read_file__mutmut_orig)
    xǁFileConfigLoaderǁ_read_file__mutmut_orig.__name__ = "xǁFileConfigLoaderǁ_read_file"


class RuntimeConfigLoader(ConfigLoader):
    """Load configuration from environment variables."""

    def xǁRuntimeConfigLoaderǁ__init____mutmut_orig(
        self, prefix: str = "", delimiter: str = "_", case_sensitive: bool = False
    ) -> None:
        """Initialize environment configuration loader.

        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        """
        self.prefix = prefix
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive

    def xǁRuntimeConfigLoaderǁ__init____mutmut_1(
        self, prefix: str = "XXXX", delimiter: str = "_", case_sensitive: bool = False
    ) -> None:
        """Initialize environment configuration loader.

        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        """
        self.prefix = prefix
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive

    def xǁRuntimeConfigLoaderǁ__init____mutmut_2(
        self, prefix: str = "", delimiter: str = "XX_XX", case_sensitive: bool = False
    ) -> None:
        """Initialize environment configuration loader.

        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        """
        self.prefix = prefix
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive

    def xǁRuntimeConfigLoaderǁ__init____mutmut_3(
        self, prefix: str = "", delimiter: str = "_", case_sensitive: bool = True
    ) -> None:
        """Initialize environment configuration loader.

        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        """
        self.prefix = prefix
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive

    def xǁRuntimeConfigLoaderǁ__init____mutmut_4(
        self, prefix: str = "", delimiter: str = "_", case_sensitive: bool = False
    ) -> None:
        """Initialize environment configuration loader.

        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        """
        self.prefix = None
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive

    def xǁRuntimeConfigLoaderǁ__init____mutmut_5(
        self, prefix: str = "", delimiter: str = "_", case_sensitive: bool = False
    ) -> None:
        """Initialize environment configuration loader.

        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        """
        self.prefix = prefix
        self.delimiter = None
        self.case_sensitive = case_sensitive

    def xǁRuntimeConfigLoaderǁ__init____mutmut_6(
        self, prefix: str = "", delimiter: str = "_", case_sensitive: bool = False
    ) -> None:
        """Initialize environment configuration loader.

        Args:
            prefix: Prefix for environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        """
        self.prefix = prefix
        self.delimiter = delimiter
        self.case_sensitive = None

    xǁRuntimeConfigLoaderǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁRuntimeConfigLoaderǁ__init____mutmut_1": xǁRuntimeConfigLoaderǁ__init____mutmut_1,
        "xǁRuntimeConfigLoaderǁ__init____mutmut_2": xǁRuntimeConfigLoaderǁ__init____mutmut_2,
        "xǁRuntimeConfigLoaderǁ__init____mutmut_3": xǁRuntimeConfigLoaderǁ__init____mutmut_3,
        "xǁRuntimeConfigLoaderǁ__init____mutmut_4": xǁRuntimeConfigLoaderǁ__init____mutmut_4,
        "xǁRuntimeConfigLoaderǁ__init____mutmut_5": xǁRuntimeConfigLoaderǁ__init____mutmut_5,
        "xǁRuntimeConfigLoaderǁ__init____mutmut_6": xǁRuntimeConfigLoaderǁ__init____mutmut_6,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁRuntimeConfigLoaderǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁRuntimeConfigLoaderǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁRuntimeConfigLoaderǁ__init____mutmut_orig)
    xǁRuntimeConfigLoaderǁ__init____mutmut_orig.__name__ = "xǁRuntimeConfigLoaderǁ__init__"

    def xǁRuntimeConfigLoaderǁexists__mutmut_orig(self) -> bool:
        """Check if any relevant environment variables exist."""
        if self.prefix:
            prefix_with_delim = f"{self.prefix}{self.delimiter}"
            return any(key.startswith(prefix_with_delim) for key in os.environ)
        return bool(os.environ)

    def xǁRuntimeConfigLoaderǁexists__mutmut_1(self) -> bool:
        """Check if any relevant environment variables exist."""
        if self.prefix:
            prefix_with_delim = None
            return any(key.startswith(prefix_with_delim) for key in os.environ)
        return bool(os.environ)

    def xǁRuntimeConfigLoaderǁexists__mutmut_2(self) -> bool:
        """Check if any relevant environment variables exist."""
        if self.prefix:
            prefix_with_delim = f"{self.prefix}{self.delimiter}"
            return any(None)
        return bool(os.environ)

    def xǁRuntimeConfigLoaderǁexists__mutmut_3(self) -> bool:
        """Check if any relevant environment variables exist."""
        if self.prefix:
            prefix_with_delim = f"{self.prefix}{self.delimiter}"
            return any(key.startswith(None) for key in os.environ)
        return bool(os.environ)

    def xǁRuntimeConfigLoaderǁexists__mutmut_4(self) -> bool:
        """Check if any relevant environment variables exist."""
        if self.prefix:
            prefix_with_delim = f"{self.prefix}{self.delimiter}"
            return any(key.startswith(prefix_with_delim) for key in os.environ)
        return bool(None)

    xǁRuntimeConfigLoaderǁexists__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁRuntimeConfigLoaderǁexists__mutmut_1": xǁRuntimeConfigLoaderǁexists__mutmut_1,
        "xǁRuntimeConfigLoaderǁexists__mutmut_2": xǁRuntimeConfigLoaderǁexists__mutmut_2,
        "xǁRuntimeConfigLoaderǁexists__mutmut_3": xǁRuntimeConfigLoaderǁexists__mutmut_3,
        "xǁRuntimeConfigLoaderǁexists__mutmut_4": xǁRuntimeConfigLoaderǁexists__mutmut_4,
    }

    def exists(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁRuntimeConfigLoaderǁexists__mutmut_orig"),
            object.__getattribute__(self, "xǁRuntimeConfigLoaderǁexists__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    exists.__signature__ = _mutmut_signature(xǁRuntimeConfigLoaderǁexists__mutmut_orig)
    xǁRuntimeConfigLoaderǁexists__mutmut_orig.__name__ = "xǁRuntimeConfigLoaderǁexists"

    def xǁRuntimeConfigLoaderǁload__mutmut_orig(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_1(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_2(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(None, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_3(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, None):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_4(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_5(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(
            config_class,
        ):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_6(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(None)

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_7(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=None,
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_8(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=None,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_9(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
            case_sensitive=None,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_10(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            delimiter=self.delimiter,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_11(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            case_sensitive=self.case_sensitive,
        )

    def xǁRuntimeConfigLoaderǁload__mutmut_12(self, config_class: type[T]) -> T:
        """Load configuration from environment variables."""
        if not issubclass(config_class, RuntimeConfig):
            raise TypeError(f"{config_class.__name__} must inherit from RuntimeConfig")

        return config_class.from_env(
            prefix=self.prefix,
            delimiter=self.delimiter,
        )

    xǁRuntimeConfigLoaderǁload__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁRuntimeConfigLoaderǁload__mutmut_1": xǁRuntimeConfigLoaderǁload__mutmut_1,
        "xǁRuntimeConfigLoaderǁload__mutmut_2": xǁRuntimeConfigLoaderǁload__mutmut_2,
        "xǁRuntimeConfigLoaderǁload__mutmut_3": xǁRuntimeConfigLoaderǁload__mutmut_3,
        "xǁRuntimeConfigLoaderǁload__mutmut_4": xǁRuntimeConfigLoaderǁload__mutmut_4,
        "xǁRuntimeConfigLoaderǁload__mutmut_5": xǁRuntimeConfigLoaderǁload__mutmut_5,
        "xǁRuntimeConfigLoaderǁload__mutmut_6": xǁRuntimeConfigLoaderǁload__mutmut_6,
        "xǁRuntimeConfigLoaderǁload__mutmut_7": xǁRuntimeConfigLoaderǁload__mutmut_7,
        "xǁRuntimeConfigLoaderǁload__mutmut_8": xǁRuntimeConfigLoaderǁload__mutmut_8,
        "xǁRuntimeConfigLoaderǁload__mutmut_9": xǁRuntimeConfigLoaderǁload__mutmut_9,
        "xǁRuntimeConfigLoaderǁload__mutmut_10": xǁRuntimeConfigLoaderǁload__mutmut_10,
        "xǁRuntimeConfigLoaderǁload__mutmut_11": xǁRuntimeConfigLoaderǁload__mutmut_11,
        "xǁRuntimeConfigLoaderǁload__mutmut_12": xǁRuntimeConfigLoaderǁload__mutmut_12,
    }

    def load(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁRuntimeConfigLoaderǁload__mutmut_orig"),
            object.__getattribute__(self, "xǁRuntimeConfigLoaderǁload__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    load.__signature__ = _mutmut_signature(xǁRuntimeConfigLoaderǁload__mutmut_orig)
    xǁRuntimeConfigLoaderǁload__mutmut_orig.__name__ = "xǁRuntimeConfigLoaderǁload"


class DictConfigLoader(ConfigLoader):
    """Load configuration from a dictionary."""

    def xǁDictConfigLoaderǁ__init____mutmut_orig(
        self, data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME
    ) -> None:
        """Initialize dictionary configuration loader.

        Args:
            data: Configuration data
            source: Source of the configuration

        """
        self.data = data
        self.source = source

    def xǁDictConfigLoaderǁ__init____mutmut_1(
        self, data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME
    ) -> None:
        """Initialize dictionary configuration loader.

        Args:
            data: Configuration data
            source: Source of the configuration

        """
        self.data = None
        self.source = source

    def xǁDictConfigLoaderǁ__init____mutmut_2(
        self, data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME
    ) -> None:
        """Initialize dictionary configuration loader.

        Args:
            data: Configuration data
            source: Source of the configuration

        """
        self.data = data
        self.source = None

    xǁDictConfigLoaderǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDictConfigLoaderǁ__init____mutmut_1": xǁDictConfigLoaderǁ__init____mutmut_1,
        "xǁDictConfigLoaderǁ__init____mutmut_2": xǁDictConfigLoaderǁ__init____mutmut_2,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDictConfigLoaderǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁDictConfigLoaderǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁDictConfigLoaderǁ__init____mutmut_orig)
    xǁDictConfigLoaderǁ__init____mutmut_orig.__name__ = "xǁDictConfigLoaderǁ__init__"

    def xǁDictConfigLoaderǁexists__mutmut_orig(self) -> bool:
        """Check if configuration data exists."""
        return self.data is not None

    def xǁDictConfigLoaderǁexists__mutmut_1(self) -> bool:
        """Check if configuration data exists."""
        return self.data is None

    xǁDictConfigLoaderǁexists__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDictConfigLoaderǁexists__mutmut_1": xǁDictConfigLoaderǁexists__mutmut_1
    }

    def exists(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDictConfigLoaderǁexists__mutmut_orig"),
            object.__getattribute__(self, "xǁDictConfigLoaderǁexists__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    exists.__signature__ = _mutmut_signature(xǁDictConfigLoaderǁexists__mutmut_orig)
    xǁDictConfigLoaderǁexists__mutmut_orig.__name__ = "xǁDictConfigLoaderǁexists"

    def xǁDictConfigLoaderǁload__mutmut_orig(self, config_class: type[T]) -> T:
        """Load configuration from dictionary."""
        return config_class.from_dict(self.data, source=self.source)

    def xǁDictConfigLoaderǁload__mutmut_1(self, config_class: type[T]) -> T:
        """Load configuration from dictionary."""
        return config_class.from_dict(None, source=self.source)

    def xǁDictConfigLoaderǁload__mutmut_2(self, config_class: type[T]) -> T:
        """Load configuration from dictionary."""
        return config_class.from_dict(self.data, source=None)

    def xǁDictConfigLoaderǁload__mutmut_3(self, config_class: type[T]) -> T:
        """Load configuration from dictionary."""
        return config_class.from_dict(source=self.source)

    def xǁDictConfigLoaderǁload__mutmut_4(self, config_class: type[T]) -> T:
        """Load configuration from dictionary."""
        return config_class.from_dict(
            self.data,
        )

    xǁDictConfigLoaderǁload__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDictConfigLoaderǁload__mutmut_1": xǁDictConfigLoaderǁload__mutmut_1,
        "xǁDictConfigLoaderǁload__mutmut_2": xǁDictConfigLoaderǁload__mutmut_2,
        "xǁDictConfigLoaderǁload__mutmut_3": xǁDictConfigLoaderǁload__mutmut_3,
        "xǁDictConfigLoaderǁload__mutmut_4": xǁDictConfigLoaderǁload__mutmut_4,
    }

    def load(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDictConfigLoaderǁload__mutmut_orig"),
            object.__getattribute__(self, "xǁDictConfigLoaderǁload__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    load.__signature__ = _mutmut_signature(xǁDictConfigLoaderǁload__mutmut_orig)
    xǁDictConfigLoaderǁload__mutmut_orig.__name__ = "xǁDictConfigLoaderǁload"


class MultiSourceLoader(ConfigLoader):
    """Load configuration from multiple sources with precedence."""

    def xǁMultiSourceLoaderǁ__init____mutmut_orig(self, *loaders: ConfigLoader) -> None:
        """Initialize multi-source configuration loader.

        Args:
            *loaders: Configuration loaders in order of precedence (later overrides earlier)

        """
        self.loaders = loaders

    def xǁMultiSourceLoaderǁ__init____mutmut_1(self, *loaders: ConfigLoader) -> None:
        """Initialize multi-source configuration loader.

        Args:
            *loaders: Configuration loaders in order of precedence (later overrides earlier)

        """
        self.loaders = None

    xǁMultiSourceLoaderǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁMultiSourceLoaderǁ__init____mutmut_1": xǁMultiSourceLoaderǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultiSourceLoaderǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMultiSourceLoaderǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁMultiSourceLoaderǁ__init____mutmut_orig)
    xǁMultiSourceLoaderǁ__init____mutmut_orig.__name__ = "xǁMultiSourceLoaderǁ__init__"

    def xǁMultiSourceLoaderǁexists__mutmut_orig(self) -> bool:
        """Check if any configuration source exists."""
        return any(loader.exists() for loader in self.loaders)

    def xǁMultiSourceLoaderǁexists__mutmut_1(self) -> bool:
        """Check if any configuration source exists."""
        return any(None)

    xǁMultiSourceLoaderǁexists__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁMultiSourceLoaderǁexists__mutmut_1": xǁMultiSourceLoaderǁexists__mutmut_1
    }

    def exists(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultiSourceLoaderǁexists__mutmut_orig"),
            object.__getattribute__(self, "xǁMultiSourceLoaderǁexists__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    exists.__signature__ = _mutmut_signature(xǁMultiSourceLoaderǁexists__mutmut_orig)
    xǁMultiSourceLoaderǁexists__mutmut_orig.__name__ = "xǁMultiSourceLoaderǁexists"

    def xǁMultiSourceLoaderǁload__mutmut_orig(self, config_class: type[T]) -> T:
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

    def xǁMultiSourceLoaderǁload__mutmut_1(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if self.exists():
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

    def xǁMultiSourceLoaderǁload__mutmut_2(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError(None)

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

    def xǁMultiSourceLoaderǁload__mutmut_3(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("XXNo configuration sources availableXX")

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

    def xǁMultiSourceLoaderǁload__mutmut_4(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("no configuration sources available")

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

    def xǁMultiSourceLoaderǁload__mutmut_5(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("NO CONFIGURATION SOURCES AVAILABLE")

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

    def xǁMultiSourceLoaderǁload__mutmut_6(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("No configuration sources available")

        config = ""

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

    def xǁMultiSourceLoaderǁload__mutmut_7(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("No configuration sources available")

        config = None

        for loader in self.loaders:
            if loader.exists():
                if config is not None:
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

    def xǁMultiSourceLoaderǁload__mutmut_8(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("No configuration sources available")

        config = None

        for loader in self.loaders:
            if loader.exists():
                if config is None:
                    config = None
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

    def xǁMultiSourceLoaderǁload__mutmut_9(self, config_class: type[T]) -> T:
        """Load and merge configuration from multiple sources."""
        if not self.exists():
            raise ValueError("No configuration sources available")

        config = None

        for loader in self.loaders:
            if loader.exists():
                if config is None:
                    config = loader.load(None)
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

    def xǁMultiSourceLoaderǁload__mutmut_10(self, config_class: type[T]) -> T:
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
                    new_config = None
                    new_dict = new_config.to_dict(include_sensitive=True)
                    # Update each field with its proper source
                    for key, value in new_dict.items():
                        source = new_config.get_source(key)
                        if source is not None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_11(self, config_class: type[T]) -> T:
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
                    new_config = loader.load(None)
                    new_dict = new_config.to_dict(include_sensitive=True)
                    # Update each field with its proper source
                    for key, value in new_dict.items():
                        source = new_config.get_source(key)
                        if source is not None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_12(self, config_class: type[T]) -> T:
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
                    new_dict = None
                    # Update each field with its proper source
                    for key, value in new_dict.items():
                        source = new_config.get_source(key)
                        if source is not None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_13(self, config_class: type[T]) -> T:
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
                    new_dict = new_config.to_dict(include_sensitive=None)
                    # Update each field with its proper source
                    for key, value in new_dict.items():
                        source = new_config.get_source(key)
                        if source is not None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_14(self, config_class: type[T]) -> T:
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
                    new_dict = new_config.to_dict(include_sensitive=False)
                    # Update each field with its proper source
                    for key, value in new_dict.items():
                        source = new_config.get_source(key)
                        if source is not None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_15(self, config_class: type[T]) -> T:
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
                        source = None
                        if source is not None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_16(self, config_class: type[T]) -> T:
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
                        source = new_config.get_source(None)
                        if source is not None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_17(self, config_class: type[T]) -> T:
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
                        if source is None:
                            config.update({key: value}, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_18(self, config_class: type[T]) -> T:
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
                            config.update(None, source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_19(self, config_class: type[T]) -> T:
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
                            config.update({key: value}, source=None)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_20(self, config_class: type[T]) -> T:
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
                            config.update(source=source)

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_21(self, config_class: type[T]) -> T:
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
                            config.update(
                                {key: value},
                            )

        if config is None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_22(self, config_class: type[T]) -> T:
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

        if config is not None:
            raise ValueError("Failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_23(self, config_class: type[T]) -> T:
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
            raise ValueError(None)
        return config

    def xǁMultiSourceLoaderǁload__mutmut_24(self, config_class: type[T]) -> T:
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
            raise ValueError("XXFailed to load configuration from any sourceXX")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_25(self, config_class: type[T]) -> T:
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
            raise ValueError("failed to load configuration from any source")
        return config

    def xǁMultiSourceLoaderǁload__mutmut_26(self, config_class: type[T]) -> T:
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
            raise ValueError("FAILED TO LOAD CONFIGURATION FROM ANY SOURCE")
        return config

    xǁMultiSourceLoaderǁload__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁMultiSourceLoaderǁload__mutmut_1": xǁMultiSourceLoaderǁload__mutmut_1,
        "xǁMultiSourceLoaderǁload__mutmut_2": xǁMultiSourceLoaderǁload__mutmut_2,
        "xǁMultiSourceLoaderǁload__mutmut_3": xǁMultiSourceLoaderǁload__mutmut_3,
        "xǁMultiSourceLoaderǁload__mutmut_4": xǁMultiSourceLoaderǁload__mutmut_4,
        "xǁMultiSourceLoaderǁload__mutmut_5": xǁMultiSourceLoaderǁload__mutmut_5,
        "xǁMultiSourceLoaderǁload__mutmut_6": xǁMultiSourceLoaderǁload__mutmut_6,
        "xǁMultiSourceLoaderǁload__mutmut_7": xǁMultiSourceLoaderǁload__mutmut_7,
        "xǁMultiSourceLoaderǁload__mutmut_8": xǁMultiSourceLoaderǁload__mutmut_8,
        "xǁMultiSourceLoaderǁload__mutmut_9": xǁMultiSourceLoaderǁload__mutmut_9,
        "xǁMultiSourceLoaderǁload__mutmut_10": xǁMultiSourceLoaderǁload__mutmut_10,
        "xǁMultiSourceLoaderǁload__mutmut_11": xǁMultiSourceLoaderǁload__mutmut_11,
        "xǁMultiSourceLoaderǁload__mutmut_12": xǁMultiSourceLoaderǁload__mutmut_12,
        "xǁMultiSourceLoaderǁload__mutmut_13": xǁMultiSourceLoaderǁload__mutmut_13,
        "xǁMultiSourceLoaderǁload__mutmut_14": xǁMultiSourceLoaderǁload__mutmut_14,
        "xǁMultiSourceLoaderǁload__mutmut_15": xǁMultiSourceLoaderǁload__mutmut_15,
        "xǁMultiSourceLoaderǁload__mutmut_16": xǁMultiSourceLoaderǁload__mutmut_16,
        "xǁMultiSourceLoaderǁload__mutmut_17": xǁMultiSourceLoaderǁload__mutmut_17,
        "xǁMultiSourceLoaderǁload__mutmut_18": xǁMultiSourceLoaderǁload__mutmut_18,
        "xǁMultiSourceLoaderǁload__mutmut_19": xǁMultiSourceLoaderǁload__mutmut_19,
        "xǁMultiSourceLoaderǁload__mutmut_20": xǁMultiSourceLoaderǁload__mutmut_20,
        "xǁMultiSourceLoaderǁload__mutmut_21": xǁMultiSourceLoaderǁload__mutmut_21,
        "xǁMultiSourceLoaderǁload__mutmut_22": xǁMultiSourceLoaderǁload__mutmut_22,
        "xǁMultiSourceLoaderǁload__mutmut_23": xǁMultiSourceLoaderǁload__mutmut_23,
        "xǁMultiSourceLoaderǁload__mutmut_24": xǁMultiSourceLoaderǁload__mutmut_24,
        "xǁMultiSourceLoaderǁload__mutmut_25": xǁMultiSourceLoaderǁload__mutmut_25,
        "xǁMultiSourceLoaderǁload__mutmut_26": xǁMultiSourceLoaderǁload__mutmut_26,
    }

    def load(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultiSourceLoaderǁload__mutmut_orig"),
            object.__getattribute__(self, "xǁMultiSourceLoaderǁload__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    load.__signature__ = _mutmut_signature(xǁMultiSourceLoaderǁload__mutmut_orig)
    xǁMultiSourceLoaderǁload__mutmut_orig.__name__ = "xǁMultiSourceLoaderǁload"


class ChainedLoader(ConfigLoader):
    """Try multiple loaders until one succeeds."""

    def xǁChainedLoaderǁ__init____mutmut_orig(self, *loaders: ConfigLoader) -> None:
        """Initialize chained configuration loader.

        Args:
            *loaders: Configuration loaders to try in order

        """
        self.loaders = loaders

    def xǁChainedLoaderǁ__init____mutmut_1(self, *loaders: ConfigLoader) -> None:
        """Initialize chained configuration loader.

        Args:
            *loaders: Configuration loaders to try in order

        """
        self.loaders = None

    xǁChainedLoaderǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁChainedLoaderǁ__init____mutmut_1": xǁChainedLoaderǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁChainedLoaderǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁChainedLoaderǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁChainedLoaderǁ__init____mutmut_orig)
    xǁChainedLoaderǁ__init____mutmut_orig.__name__ = "xǁChainedLoaderǁ__init__"

    def xǁChainedLoaderǁexists__mutmut_orig(self) -> bool:
        """Check if any configuration source exists."""
        return any(loader.exists() for loader in self.loaders)

    def xǁChainedLoaderǁexists__mutmut_1(self) -> bool:
        """Check if any configuration source exists."""
        return any(None)

    xǁChainedLoaderǁexists__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁChainedLoaderǁexists__mutmut_1": xǁChainedLoaderǁexists__mutmut_1
    }

    def exists(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁChainedLoaderǁexists__mutmut_orig"),
            object.__getattribute__(self, "xǁChainedLoaderǁexists__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    exists.__signature__ = _mutmut_signature(xǁChainedLoaderǁexists__mutmut_orig)
    xǁChainedLoaderǁexists__mutmut_orig.__name__ = "xǁChainedLoaderǁexists"

    def xǁChainedLoaderǁload__mutmut_orig(self, config_class: type[T]) -> T:
        """Load configuration from first available source."""
        for loader in self.loaders:
            if loader.exists():
                return loader.load(config_class)

        raise ValueError("No configuration source available")

    def xǁChainedLoaderǁload__mutmut_1(self, config_class: type[T]) -> T:
        """Load configuration from first available source."""
        for loader in self.loaders:
            if loader.exists():
                return loader.load(None)

        raise ValueError("No configuration source available")

    def xǁChainedLoaderǁload__mutmut_2(self, config_class: type[T]) -> T:
        """Load configuration from first available source."""
        for loader in self.loaders:
            if loader.exists():
                return loader.load(config_class)

        raise ValueError(None)

    def xǁChainedLoaderǁload__mutmut_3(self, config_class: type[T]) -> T:
        """Load configuration from first available source."""
        for loader in self.loaders:
            if loader.exists():
                return loader.load(config_class)

        raise ValueError("XXNo configuration source availableXX")

    def xǁChainedLoaderǁload__mutmut_4(self, config_class: type[T]) -> T:
        """Load configuration from first available source."""
        for loader in self.loaders:
            if loader.exists():
                return loader.load(config_class)

        raise ValueError("no configuration source available")

    def xǁChainedLoaderǁload__mutmut_5(self, config_class: type[T]) -> T:
        """Load configuration from first available source."""
        for loader in self.loaders:
            if loader.exists():
                return loader.load(config_class)

        raise ValueError("NO CONFIGURATION SOURCE AVAILABLE")

    xǁChainedLoaderǁload__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁChainedLoaderǁload__mutmut_1": xǁChainedLoaderǁload__mutmut_1,
        "xǁChainedLoaderǁload__mutmut_2": xǁChainedLoaderǁload__mutmut_2,
        "xǁChainedLoaderǁload__mutmut_3": xǁChainedLoaderǁload__mutmut_3,
        "xǁChainedLoaderǁload__mutmut_4": xǁChainedLoaderǁload__mutmut_4,
        "xǁChainedLoaderǁload__mutmut_5": xǁChainedLoaderǁload__mutmut_5,
    }

    def load(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁChainedLoaderǁload__mutmut_orig"),
            object.__getattribute__(self, "xǁChainedLoaderǁload__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    load.__signature__ = _mutmut_signature(xǁChainedLoaderǁload__mutmut_orig)
    xǁChainedLoaderǁload__mutmut_orig.__name__ = "xǁChainedLoaderǁload"


# <3 🧱🤝⚙️🪄
