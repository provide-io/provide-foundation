# provide/foundation/config/manager.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TypeVar

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.loader import ConfigLoader
from provide.foundation.config.schema import ConfigSchema
from provide.foundation.config.types import ConfigDict, ConfigSource

"""Configuration manager for centralized configuration management."""

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


class ConfigManager:
    """Centralized configuration manager.

    Manages multiple configuration objects and provides a unified interface.
    """

    def xǁConfigManagerǁ__init____mutmut_orig(self) -> None:
        """Initialize configuration manager."""
        self._configs: dict[str, BaseConfig] = {}
        self._schemas: dict[str, ConfigSchema] = {}
        self._loaders: dict[str, ConfigLoader] = {}
        self._defaults: dict[str, ConfigDict] = {}

    def xǁConfigManagerǁ__init____mutmut_1(self) -> None:
        """Initialize configuration manager."""
        self._configs: dict[str, BaseConfig] = None
        self._schemas: dict[str, ConfigSchema] = {}
        self._loaders: dict[str, ConfigLoader] = {}
        self._defaults: dict[str, ConfigDict] = {}

    def xǁConfigManagerǁ__init____mutmut_2(self) -> None:
        """Initialize configuration manager."""
        self._configs: dict[str, BaseConfig] = {}
        self._schemas: dict[str, ConfigSchema] = None
        self._loaders: dict[str, ConfigLoader] = {}
        self._defaults: dict[str, ConfigDict] = {}

    def xǁConfigManagerǁ__init____mutmut_3(self) -> None:
        """Initialize configuration manager."""
        self._configs: dict[str, BaseConfig] = {}
        self._schemas: dict[str, ConfigSchema] = {}
        self._loaders: dict[str, ConfigLoader] = None
        self._defaults: dict[str, ConfigDict] = {}

    def xǁConfigManagerǁ__init____mutmut_4(self) -> None:
        """Initialize configuration manager."""
        self._configs: dict[str, BaseConfig] = {}
        self._schemas: dict[str, ConfigSchema] = {}
        self._loaders: dict[str, ConfigLoader] = {}
        self._defaults: dict[str, ConfigDict] = None

    xǁConfigManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁ__init____mutmut_1": xǁConfigManagerǁ__init____mutmut_1,
        "xǁConfigManagerǁ__init____mutmut_2": xǁConfigManagerǁ__init____mutmut_2,
        "xǁConfigManagerǁ__init____mutmut_3": xǁConfigManagerǁ__init____mutmut_3,
        "xǁConfigManagerǁ__init____mutmut_4": xǁConfigManagerǁ__init____mutmut_4,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁConfigManagerǁ__init____mutmut_orig)
    xǁConfigManagerǁ__init____mutmut_orig.__name__ = "xǁConfigManagerǁ__init__"

    def xǁConfigManagerǁregister__mutmut_orig(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = config

        if schema is not None:
            self._schemas[name] = schema

        if loader is not None:
            self._loaders[name] = loader

        if defaults is not None:
            self._defaults[name] = defaults

    def xǁConfigManagerǁregister__mutmut_1(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is None:
            self._configs[name] = config

        if schema is not None:
            self._schemas[name] = schema

        if loader is not None:
            self._loaders[name] = loader

        if defaults is not None:
            self._defaults[name] = defaults

    def xǁConfigManagerǁregister__mutmut_2(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = None

        if schema is not None:
            self._schemas[name] = schema

        if loader is not None:
            self._loaders[name] = loader

        if defaults is not None:
            self._defaults[name] = defaults

    def xǁConfigManagerǁregister__mutmut_3(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = config

        if schema is None:
            self._schemas[name] = schema

        if loader is not None:
            self._loaders[name] = loader

        if defaults is not None:
            self._defaults[name] = defaults

    def xǁConfigManagerǁregister__mutmut_4(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = config

        if schema is not None:
            self._schemas[name] = None

        if loader is not None:
            self._loaders[name] = loader

        if defaults is not None:
            self._defaults[name] = defaults

    def xǁConfigManagerǁregister__mutmut_5(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = config

        if schema is not None:
            self._schemas[name] = schema

        if loader is None:
            self._loaders[name] = loader

        if defaults is not None:
            self._defaults[name] = defaults

    def xǁConfigManagerǁregister__mutmut_6(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = config

        if schema is not None:
            self._schemas[name] = schema

        if loader is not None:
            self._loaders[name] = None

        if defaults is not None:
            self._defaults[name] = defaults

    def xǁConfigManagerǁregister__mutmut_7(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = config

        if schema is not None:
            self._schemas[name] = schema

        if loader is not None:
            self._loaders[name] = loader

        if defaults is None:
            self._defaults[name] = defaults

    def xǁConfigManagerǁregister__mutmut_8(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = config

        if schema is not None:
            self._schemas[name] = schema

        if loader is not None:
            self._loaders[name] = loader

        if defaults is not None:
            self._defaults[name] = None

    xǁConfigManagerǁregister__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁregister__mutmut_1": xǁConfigManagerǁregister__mutmut_1,
        "xǁConfigManagerǁregister__mutmut_2": xǁConfigManagerǁregister__mutmut_2,
        "xǁConfigManagerǁregister__mutmut_3": xǁConfigManagerǁregister__mutmut_3,
        "xǁConfigManagerǁregister__mutmut_4": xǁConfigManagerǁregister__mutmut_4,
        "xǁConfigManagerǁregister__mutmut_5": xǁConfigManagerǁregister__mutmut_5,
        "xǁConfigManagerǁregister__mutmut_6": xǁConfigManagerǁregister__mutmut_6,
        "xǁConfigManagerǁregister__mutmut_7": xǁConfigManagerǁregister__mutmut_7,
        "xǁConfigManagerǁregister__mutmut_8": xǁConfigManagerǁregister__mutmut_8,
    }

    def register(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁregister__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁregister__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    register.__signature__ = _mutmut_signature(xǁConfigManagerǁregister__mutmut_orig)
    xǁConfigManagerǁregister__mutmut_orig.__name__ = "xǁConfigManagerǁregister"

    def xǁConfigManagerǁunregister__mutmut_orig(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(name, None)
        self._loaders.pop(name, None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_1(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(None, None)
        self._schemas.pop(name, None)
        self._loaders.pop(name, None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_2(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(None)
        self._schemas.pop(name, None)
        self._loaders.pop(name, None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_3(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(
            name,
        )
        self._schemas.pop(name, None)
        self._loaders.pop(name, None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_4(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(None, None)
        self._loaders.pop(name, None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_5(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(None)
        self._loaders.pop(name, None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_6(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(
            name,
        )
        self._loaders.pop(name, None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_7(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(name, None)
        self._loaders.pop(None, None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_8(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(name, None)
        self._loaders.pop(None)
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_9(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(name, None)
        self._loaders.pop(
            name,
        )
        self._defaults.pop(name, None)

    def xǁConfigManagerǁunregister__mutmut_10(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(name, None)
        self._loaders.pop(name, None)
        self._defaults.pop(None, None)

    def xǁConfigManagerǁunregister__mutmut_11(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(name, None)
        self._loaders.pop(name, None)
        self._defaults.pop(None)

    def xǁConfigManagerǁunregister__mutmut_12(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(name, None)
        self._loaders.pop(name, None)
        self._defaults.pop(
            name,
        )

    xǁConfigManagerǁunregister__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁunregister__mutmut_1": xǁConfigManagerǁunregister__mutmut_1,
        "xǁConfigManagerǁunregister__mutmut_2": xǁConfigManagerǁunregister__mutmut_2,
        "xǁConfigManagerǁunregister__mutmut_3": xǁConfigManagerǁunregister__mutmut_3,
        "xǁConfigManagerǁunregister__mutmut_4": xǁConfigManagerǁunregister__mutmut_4,
        "xǁConfigManagerǁunregister__mutmut_5": xǁConfigManagerǁunregister__mutmut_5,
        "xǁConfigManagerǁunregister__mutmut_6": xǁConfigManagerǁunregister__mutmut_6,
        "xǁConfigManagerǁunregister__mutmut_7": xǁConfigManagerǁunregister__mutmut_7,
        "xǁConfigManagerǁunregister__mutmut_8": xǁConfigManagerǁunregister__mutmut_8,
        "xǁConfigManagerǁunregister__mutmut_9": xǁConfigManagerǁunregister__mutmut_9,
        "xǁConfigManagerǁunregister__mutmut_10": xǁConfigManagerǁunregister__mutmut_10,
        "xǁConfigManagerǁunregister__mutmut_11": xǁConfigManagerǁunregister__mutmut_11,
        "xǁConfigManagerǁunregister__mutmut_12": xǁConfigManagerǁunregister__mutmut_12,
    }

    def unregister(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁunregister__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁunregister__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    unregister.__signature__ = _mutmut_signature(xǁConfigManagerǁunregister__mutmut_orig)
    xǁConfigManagerǁunregister__mutmut_orig.__name__ = "xǁConfigManagerǁunregister"

    # Alias for unregister
    def xǁConfigManagerǁremove__mutmut_orig(self, name: str) -> None:
        """Remove a configuration. Alias for unregister."""
        self.unregister(name)

    # Alias for unregister
    def xǁConfigManagerǁremove__mutmut_1(self, name: str) -> None:
        """Remove a configuration. Alias for unregister."""
        self.unregister(None)

    xǁConfigManagerǁremove__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁremove__mutmut_1": xǁConfigManagerǁremove__mutmut_1
    }

    def remove(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁremove__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁremove__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    remove.__signature__ = _mutmut_signature(xǁConfigManagerǁremove__mutmut_orig)
    xǁConfigManagerǁremove__mutmut_orig.__name__ = "xǁConfigManagerǁremove"

    def xǁConfigManagerǁget__mutmut_orig(self, name: str) -> BaseConfig | None:
        """Get a configuration by name.

        Args:
            name: Configuration name

        Returns:
            Configuration instance or None

        """
        return self._configs.get(name)

    def xǁConfigManagerǁget__mutmut_1(self, name: str) -> BaseConfig | None:
        """Get a configuration by name.

        Args:
            name: Configuration name

        Returns:
            Configuration instance or None

        """
        return self._configs.get(None)

    xǁConfigManagerǁget__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁget__mutmut_1": xǁConfigManagerǁget__mutmut_1
    }

    def get(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁget__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁget__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get.__signature__ = _mutmut_signature(xǁConfigManagerǁget__mutmut_orig)
    xǁConfigManagerǁget__mutmut_orig.__name__ = "xǁConfigManagerǁget"

    def xǁConfigManagerǁset__mutmut_orig(self, name: str, config: BaseConfig) -> None:
        """Set a configuration.

        Args:
            name: Configuration name
            config: Configuration instance

        """
        self._configs[name] = config

    def xǁConfigManagerǁset__mutmut_1(self, name: str, config: BaseConfig) -> None:
        """Set a configuration.

        Args:
            name: Configuration name
            config: Configuration instance

        """
        self._configs[name] = None

    xǁConfigManagerǁset__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁset__mutmut_1": xǁConfigManagerǁset__mutmut_1
    }

    def set(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁset__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁset__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    set.__signature__ = _mutmut_signature(xǁConfigManagerǁset__mutmut_orig)
    xǁConfigManagerǁset__mutmut_orig.__name__ = "xǁConfigManagerǁset"

    def xǁConfigManagerǁload__mutmut_orig(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_1(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is not None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_2(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = None
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_3(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(None)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_4(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is not None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_5(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(None)

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_6(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = None

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_7(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(None)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_8(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name not in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_9(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = None
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_10(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) and getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_11(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_12(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(None, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_13(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, None) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_14(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_15(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if (
                    not hasattr(
                        config,
                    )
                    or getattr(config, key) is None
                ):
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_16(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(None, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_17(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, None) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_18(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_19(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if (
                    not hasattr(config, key)
                    or getattr(
                        config,
                    )
                    is None
                ):
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_20(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is not None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_21(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(None, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_22(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, None, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_23(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, None)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_24(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_25(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_26(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(
                        config,
                        key,
                    )

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_27(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name not in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_28(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = None
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_29(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = None
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_30(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=None)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_31(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=False)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_32(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(None)

        # Store configuration
        self._configs[name] = config

        return config

    def xǁConfigManagerǁload__mutmut_33(
        self, name: str, config_class: type[T], loader: ConfigLoader | None = None
    ) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = None

        return config

    xǁConfigManagerǁload__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁload__mutmut_1": xǁConfigManagerǁload__mutmut_1,
        "xǁConfigManagerǁload__mutmut_2": xǁConfigManagerǁload__mutmut_2,
        "xǁConfigManagerǁload__mutmut_3": xǁConfigManagerǁload__mutmut_3,
        "xǁConfigManagerǁload__mutmut_4": xǁConfigManagerǁload__mutmut_4,
        "xǁConfigManagerǁload__mutmut_5": xǁConfigManagerǁload__mutmut_5,
        "xǁConfigManagerǁload__mutmut_6": xǁConfigManagerǁload__mutmut_6,
        "xǁConfigManagerǁload__mutmut_7": xǁConfigManagerǁload__mutmut_7,
        "xǁConfigManagerǁload__mutmut_8": xǁConfigManagerǁload__mutmut_8,
        "xǁConfigManagerǁload__mutmut_9": xǁConfigManagerǁload__mutmut_9,
        "xǁConfigManagerǁload__mutmut_10": xǁConfigManagerǁload__mutmut_10,
        "xǁConfigManagerǁload__mutmut_11": xǁConfigManagerǁload__mutmut_11,
        "xǁConfigManagerǁload__mutmut_12": xǁConfigManagerǁload__mutmut_12,
        "xǁConfigManagerǁload__mutmut_13": xǁConfigManagerǁload__mutmut_13,
        "xǁConfigManagerǁload__mutmut_14": xǁConfigManagerǁload__mutmut_14,
        "xǁConfigManagerǁload__mutmut_15": xǁConfigManagerǁload__mutmut_15,
        "xǁConfigManagerǁload__mutmut_16": xǁConfigManagerǁload__mutmut_16,
        "xǁConfigManagerǁload__mutmut_17": xǁConfigManagerǁload__mutmut_17,
        "xǁConfigManagerǁload__mutmut_18": xǁConfigManagerǁload__mutmut_18,
        "xǁConfigManagerǁload__mutmut_19": xǁConfigManagerǁload__mutmut_19,
        "xǁConfigManagerǁload__mutmut_20": xǁConfigManagerǁload__mutmut_20,
        "xǁConfigManagerǁload__mutmut_21": xǁConfigManagerǁload__mutmut_21,
        "xǁConfigManagerǁload__mutmut_22": xǁConfigManagerǁload__mutmut_22,
        "xǁConfigManagerǁload__mutmut_23": xǁConfigManagerǁload__mutmut_23,
        "xǁConfigManagerǁload__mutmut_24": xǁConfigManagerǁload__mutmut_24,
        "xǁConfigManagerǁload__mutmut_25": xǁConfigManagerǁload__mutmut_25,
        "xǁConfigManagerǁload__mutmut_26": xǁConfigManagerǁload__mutmut_26,
        "xǁConfigManagerǁload__mutmut_27": xǁConfigManagerǁload__mutmut_27,
        "xǁConfigManagerǁload__mutmut_28": xǁConfigManagerǁload__mutmut_28,
        "xǁConfigManagerǁload__mutmut_29": xǁConfigManagerǁload__mutmut_29,
        "xǁConfigManagerǁload__mutmut_30": xǁConfigManagerǁload__mutmut_30,
        "xǁConfigManagerǁload__mutmut_31": xǁConfigManagerǁload__mutmut_31,
        "xǁConfigManagerǁload__mutmut_32": xǁConfigManagerǁload__mutmut_32,
        "xǁConfigManagerǁload__mutmut_33": xǁConfigManagerǁload__mutmut_33,
    }

    def load(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁload__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁload__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    load.__signature__ = _mutmut_signature(xǁConfigManagerǁload__mutmut_orig)
    xǁConfigManagerǁload__mutmut_orig.__name__ = "xǁConfigManagerǁload"

    def xǁConfigManagerǁreload__mutmut_orig(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_1(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_2(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(None)

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_3(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = None
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_4(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = None

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_5(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(None)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_6(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is not None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_7(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(None)

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_8(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = None

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_9(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(None)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_10(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name not in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_11(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = None
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_12(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) and getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_13(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_14(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(None, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_15(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, None) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_16(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_17(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if (
                    not hasattr(
                        new_config,
                    )
                    or getattr(new_config, key) is None
                ):
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_18(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(None, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_19(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, None) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_20(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_21(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if (
                    not hasattr(new_config, key)
                    or getattr(
                        new_config,
                    )
                    is None
                ):
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_22(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is not None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_23(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(None, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_24(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, None, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_25(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, None)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_26(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_27(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_28(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(
                        new_config,
                        key,
                    )

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_29(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name not in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_30(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = None
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_31(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = None
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_32(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=None)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_33(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=False)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_34(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(None)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def xǁConfigManagerǁreload__mutmut_35(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = None

        return new_config

    xǁConfigManagerǁreload__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁreload__mutmut_1": xǁConfigManagerǁreload__mutmut_1,
        "xǁConfigManagerǁreload__mutmut_2": xǁConfigManagerǁreload__mutmut_2,
        "xǁConfigManagerǁreload__mutmut_3": xǁConfigManagerǁreload__mutmut_3,
        "xǁConfigManagerǁreload__mutmut_4": xǁConfigManagerǁreload__mutmut_4,
        "xǁConfigManagerǁreload__mutmut_5": xǁConfigManagerǁreload__mutmut_5,
        "xǁConfigManagerǁreload__mutmut_6": xǁConfigManagerǁreload__mutmut_6,
        "xǁConfigManagerǁreload__mutmut_7": xǁConfigManagerǁreload__mutmut_7,
        "xǁConfigManagerǁreload__mutmut_8": xǁConfigManagerǁreload__mutmut_8,
        "xǁConfigManagerǁreload__mutmut_9": xǁConfigManagerǁreload__mutmut_9,
        "xǁConfigManagerǁreload__mutmut_10": xǁConfigManagerǁreload__mutmut_10,
        "xǁConfigManagerǁreload__mutmut_11": xǁConfigManagerǁreload__mutmut_11,
        "xǁConfigManagerǁreload__mutmut_12": xǁConfigManagerǁreload__mutmut_12,
        "xǁConfigManagerǁreload__mutmut_13": xǁConfigManagerǁreload__mutmut_13,
        "xǁConfigManagerǁreload__mutmut_14": xǁConfigManagerǁreload__mutmut_14,
        "xǁConfigManagerǁreload__mutmut_15": xǁConfigManagerǁreload__mutmut_15,
        "xǁConfigManagerǁreload__mutmut_16": xǁConfigManagerǁreload__mutmut_16,
        "xǁConfigManagerǁreload__mutmut_17": xǁConfigManagerǁreload__mutmut_17,
        "xǁConfigManagerǁreload__mutmut_18": xǁConfigManagerǁreload__mutmut_18,
        "xǁConfigManagerǁreload__mutmut_19": xǁConfigManagerǁreload__mutmut_19,
        "xǁConfigManagerǁreload__mutmut_20": xǁConfigManagerǁreload__mutmut_20,
        "xǁConfigManagerǁreload__mutmut_21": xǁConfigManagerǁreload__mutmut_21,
        "xǁConfigManagerǁreload__mutmut_22": xǁConfigManagerǁreload__mutmut_22,
        "xǁConfigManagerǁreload__mutmut_23": xǁConfigManagerǁreload__mutmut_23,
        "xǁConfigManagerǁreload__mutmut_24": xǁConfigManagerǁreload__mutmut_24,
        "xǁConfigManagerǁreload__mutmut_25": xǁConfigManagerǁreload__mutmut_25,
        "xǁConfigManagerǁreload__mutmut_26": xǁConfigManagerǁreload__mutmut_26,
        "xǁConfigManagerǁreload__mutmut_27": xǁConfigManagerǁreload__mutmut_27,
        "xǁConfigManagerǁreload__mutmut_28": xǁConfigManagerǁreload__mutmut_28,
        "xǁConfigManagerǁreload__mutmut_29": xǁConfigManagerǁreload__mutmut_29,
        "xǁConfigManagerǁreload__mutmut_30": xǁConfigManagerǁreload__mutmut_30,
        "xǁConfigManagerǁreload__mutmut_31": xǁConfigManagerǁreload__mutmut_31,
        "xǁConfigManagerǁreload__mutmut_32": xǁConfigManagerǁreload__mutmut_32,
        "xǁConfigManagerǁreload__mutmut_33": xǁConfigManagerǁreload__mutmut_33,
        "xǁConfigManagerǁreload__mutmut_34": xǁConfigManagerǁreload__mutmut_34,
        "xǁConfigManagerǁreload__mutmut_35": xǁConfigManagerǁreload__mutmut_35,
    }

    def reload(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁreload__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁreload__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    reload.__signature__ = _mutmut_signature(xǁConfigManagerǁreload__mutmut_orig)
    xǁConfigManagerǁreload__mutmut_orig.__name__ = "xǁConfigManagerǁreload"

    def xǁConfigManagerǁupdate__mutmut_orig(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, source)

    def xǁConfigManagerǁupdate__mutmut_1(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, source)

    def xǁConfigManagerǁupdate__mutmut_2(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(None)

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, source)

    def xǁConfigManagerǁupdate__mutmut_3(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = None

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, source)

    def xǁConfigManagerǁupdate__mutmut_4(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name not in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, source)

    def xǁConfigManagerǁupdate__mutmut_5(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = None
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, source)

    def xǁConfigManagerǁupdate__mutmut_6(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key not in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, source)

    def xǁConfigManagerǁupdate__mutmut_7(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(None)

        # Apply updates
        config.update(updates, source)

    def xǁConfigManagerǁupdate__mutmut_8(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(None, source)

    def xǁConfigManagerǁupdate__mutmut_9(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, None)

    def xǁConfigManagerǁupdate__mutmut_10(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(source)

    def xǁConfigManagerǁupdate__mutmut_11(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(
            updates,
        )

    xǁConfigManagerǁupdate__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁupdate__mutmut_1": xǁConfigManagerǁupdate__mutmut_1,
        "xǁConfigManagerǁupdate__mutmut_2": xǁConfigManagerǁupdate__mutmut_2,
        "xǁConfigManagerǁupdate__mutmut_3": xǁConfigManagerǁupdate__mutmut_3,
        "xǁConfigManagerǁupdate__mutmut_4": xǁConfigManagerǁupdate__mutmut_4,
        "xǁConfigManagerǁupdate__mutmut_5": xǁConfigManagerǁupdate__mutmut_5,
        "xǁConfigManagerǁupdate__mutmut_6": xǁConfigManagerǁupdate__mutmut_6,
        "xǁConfigManagerǁupdate__mutmut_7": xǁConfigManagerǁupdate__mutmut_7,
        "xǁConfigManagerǁupdate__mutmut_8": xǁConfigManagerǁupdate__mutmut_8,
        "xǁConfigManagerǁupdate__mutmut_9": xǁConfigManagerǁupdate__mutmut_9,
        "xǁConfigManagerǁupdate__mutmut_10": xǁConfigManagerǁupdate__mutmut_10,
        "xǁConfigManagerǁupdate__mutmut_11": xǁConfigManagerǁupdate__mutmut_11,
    }

    def update(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁupdate__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁupdate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    update.__signature__ = _mutmut_signature(xǁConfigManagerǁupdate__mutmut_orig)
    xǁConfigManagerǁupdate__mutmut_orig.__name__ = "xǁConfigManagerǁupdate"

    def xǁConfigManagerǁreset__mutmut_orig(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(self._defaults[name], ConfigSource.DEFAULT)

    def xǁConfigManagerǁreset__mutmut_1(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(self._defaults[name], ConfigSource.DEFAULT)

    def xǁConfigManagerǁreset__mutmut_2(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(None)

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(self._defaults[name], ConfigSource.DEFAULT)

    def xǁConfigManagerǁreset__mutmut_3(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = None
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(self._defaults[name], ConfigSource.DEFAULT)

    def xǁConfigManagerǁreset__mutmut_4(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name not in self._defaults:
            config.update(self._defaults[name], ConfigSource.DEFAULT)

    def xǁConfigManagerǁreset__mutmut_5(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(None, ConfigSource.DEFAULT)

    def xǁConfigManagerǁreset__mutmut_6(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(self._defaults[name], None)

    def xǁConfigManagerǁreset__mutmut_7(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(ConfigSource.DEFAULT)

    def xǁConfigManagerǁreset__mutmut_8(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(
                self._defaults[name],
            )

    xǁConfigManagerǁreset__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁreset__mutmut_1": xǁConfigManagerǁreset__mutmut_1,
        "xǁConfigManagerǁreset__mutmut_2": xǁConfigManagerǁreset__mutmut_2,
        "xǁConfigManagerǁreset__mutmut_3": xǁConfigManagerǁreset__mutmut_3,
        "xǁConfigManagerǁreset__mutmut_4": xǁConfigManagerǁreset__mutmut_4,
        "xǁConfigManagerǁreset__mutmut_5": xǁConfigManagerǁreset__mutmut_5,
        "xǁConfigManagerǁreset__mutmut_6": xǁConfigManagerǁreset__mutmut_6,
        "xǁConfigManagerǁreset__mutmut_7": xǁConfigManagerǁreset__mutmut_7,
        "xǁConfigManagerǁreset__mutmut_8": xǁConfigManagerǁreset__mutmut_8,
    }

    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁreset__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁreset__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    reset.__signature__ = _mutmut_signature(xǁConfigManagerǁreset__mutmut_orig)
    xǁConfigManagerǁreset__mutmut_orig.__name__ = "xǁConfigManagerǁreset"

    def xǁConfigManagerǁlist_configs__mutmut_orig(self) -> list[str]:
        """List all registered configurations.

        Returns:
            List of configuration names

        """
        return list(self._configs.keys())

    def xǁConfigManagerǁlist_configs__mutmut_1(self) -> list[str]:
        """List all registered configurations.

        Returns:
            List of configuration names

        """
        return list(None)

    xǁConfigManagerǁlist_configs__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁlist_configs__mutmut_1": xǁConfigManagerǁlist_configs__mutmut_1
    }

    def list_configs(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁlist_configs__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁlist_configs__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    list_configs.__signature__ = _mutmut_signature(xǁConfigManagerǁlist_configs__mutmut_orig)
    xǁConfigManagerǁlist_configs__mutmut_orig.__name__ = "xǁConfigManagerǁlist_configs"

    def get_all(self) -> dict[str, BaseConfig]:
        """Get all registered configurations."""
        return self._configs.copy()

    def clear(self) -> None:
        """Clear all configurations."""
        self._configs.clear()
        self._schemas.clear()
        self._loaders.clear()
        self._defaults.clear()

    def xǁConfigManagerǁexport__mutmut_orig(self, name: str, include_sensitive: bool = False) -> ConfigDict:
        """Export a configuration as dictionary.

        Args:
            name: Configuration name
            include_sensitive: Whether to include sensitive fields

        Returns:
            Configuration dictionary

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        return self._configs[name].to_dict(include_sensitive)

    def xǁConfigManagerǁexport__mutmut_1(self, name: str, include_sensitive: bool = True) -> ConfigDict:
        """Export a configuration as dictionary.

        Args:
            name: Configuration name
            include_sensitive: Whether to include sensitive fields

        Returns:
            Configuration dictionary

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        return self._configs[name].to_dict(include_sensitive)

    def xǁConfigManagerǁexport__mutmut_2(self, name: str, include_sensitive: bool = False) -> ConfigDict:
        """Export a configuration as dictionary.

        Args:
            name: Configuration name
            include_sensitive: Whether to include sensitive fields

        Returns:
            Configuration dictionary

        """
        if name in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        return self._configs[name].to_dict(include_sensitive)

    def xǁConfigManagerǁexport__mutmut_3(self, name: str, include_sensitive: bool = False) -> ConfigDict:
        """Export a configuration as dictionary.

        Args:
            name: Configuration name
            include_sensitive: Whether to include sensitive fields

        Returns:
            Configuration dictionary

        """
        if name not in self._configs:
            raise ValueError(None)

        return self._configs[name].to_dict(include_sensitive)

    def xǁConfigManagerǁexport__mutmut_4(self, name: str, include_sensitive: bool = False) -> ConfigDict:
        """Export a configuration as dictionary.

        Args:
            name: Configuration name
            include_sensitive: Whether to include sensitive fields

        Returns:
            Configuration dictionary

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        return self._configs[name].to_dict(None)

    xǁConfigManagerǁexport__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁexport__mutmut_1": xǁConfigManagerǁexport__mutmut_1,
        "xǁConfigManagerǁexport__mutmut_2": xǁConfigManagerǁexport__mutmut_2,
        "xǁConfigManagerǁexport__mutmut_3": xǁConfigManagerǁexport__mutmut_3,
        "xǁConfigManagerǁexport__mutmut_4": xǁConfigManagerǁexport__mutmut_4,
    }

    def export(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁexport__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁexport__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    export.__signature__ = _mutmut_signature(xǁConfigManagerǁexport__mutmut_orig)
    xǁConfigManagerǁexport__mutmut_orig.__name__ = "xǁConfigManagerǁexport"

    def xǁConfigManagerǁexport_all__mutmut_orig(
        self, include_sensitive: bool = False
    ) -> dict[str, ConfigDict]:
        """Export all configurations.

        Args:
            include_sensitive: Whether to include sensitive fields

        Returns:
            Dictionary of all configurations

        """
        result = {}
        for name, config in self._configs.items():
            result[name] = config.to_dict(include_sensitive)
        return result

    def xǁConfigManagerǁexport_all__mutmut_1(self, include_sensitive: bool = True) -> dict[str, ConfigDict]:
        """Export all configurations.

        Args:
            include_sensitive: Whether to include sensitive fields

        Returns:
            Dictionary of all configurations

        """
        result = {}
        for name, config in self._configs.items():
            result[name] = config.to_dict(include_sensitive)
        return result

    def xǁConfigManagerǁexport_all__mutmut_2(self, include_sensitive: bool = False) -> dict[str, ConfigDict]:
        """Export all configurations.

        Args:
            include_sensitive: Whether to include sensitive fields

        Returns:
            Dictionary of all configurations

        """
        result = None
        for name, config in self._configs.items():
            result[name] = config.to_dict(include_sensitive)
        return result

    def xǁConfigManagerǁexport_all__mutmut_3(self, include_sensitive: bool = False) -> dict[str, ConfigDict]:
        """Export all configurations.

        Args:
            include_sensitive: Whether to include sensitive fields

        Returns:
            Dictionary of all configurations

        """
        result = {}
        for name, config in self._configs.items():
            result[name] = None
        return result

    def xǁConfigManagerǁexport_all__mutmut_4(self, include_sensitive: bool = False) -> dict[str, ConfigDict]:
        """Export all configurations.

        Args:
            include_sensitive: Whether to include sensitive fields

        Returns:
            Dictionary of all configurations

        """
        result = {}
        for name, config in self._configs.items():
            result[name] = config.to_dict(None)
        return result

    xǁConfigManagerǁexport_all__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁexport_all__mutmut_1": xǁConfigManagerǁexport_all__mutmut_1,
        "xǁConfigManagerǁexport_all__mutmut_2": xǁConfigManagerǁexport_all__mutmut_2,
        "xǁConfigManagerǁexport_all__mutmut_3": xǁConfigManagerǁexport_all__mutmut_3,
        "xǁConfigManagerǁexport_all__mutmut_4": xǁConfigManagerǁexport_all__mutmut_4,
    }

    def export_all(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁexport_all__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁexport_all__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    export_all.__signature__ = _mutmut_signature(xǁConfigManagerǁexport_all__mutmut_orig)
    xǁConfigManagerǁexport_all__mutmut_orig.__name__ = "xǁConfigManagerǁexport_all"

    # Alias for export_all
    def xǁConfigManagerǁexport_to_dict__mutmut_orig(
        self, include_sensitive: bool = False
    ) -> dict[str, ConfigDict]:
        """Export all configs to dict. Alias for export_all."""
        return self.export_all(include_sensitive)

    # Alias for export_all
    def xǁConfigManagerǁexport_to_dict__mutmut_1(
        self, include_sensitive: bool = True
    ) -> dict[str, ConfigDict]:
        """Export all configs to dict. Alias for export_all."""
        return self.export_all(include_sensitive)

    # Alias for export_all
    def xǁConfigManagerǁexport_to_dict__mutmut_2(
        self, include_sensitive: bool = False
    ) -> dict[str, ConfigDict]:
        """Export all configs to dict. Alias for export_all."""
        return self.export_all(None)

    xǁConfigManagerǁexport_to_dict__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁexport_to_dict__mutmut_1": xǁConfigManagerǁexport_to_dict__mutmut_1,
        "xǁConfigManagerǁexport_to_dict__mutmut_2": xǁConfigManagerǁexport_to_dict__mutmut_2,
    }

    def export_to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁexport_to_dict__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁexport_to_dict__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    export_to_dict.__signature__ = _mutmut_signature(xǁConfigManagerǁexport_to_dict__mutmut_orig)
    xǁConfigManagerǁexport_to_dict__mutmut_orig.__name__ = "xǁConfigManagerǁexport_to_dict"

    def xǁConfigManagerǁload_from_dict__mutmut_orig(
        self, name: str, config_class: type[T], data: ConfigDict
    ) -> T:
        """Load config from dictionary."""
        config = config_class.from_dict(data)
        self._configs[name] = config
        return config

    def xǁConfigManagerǁload_from_dict__mutmut_1(
        self, name: str, config_class: type[T], data: ConfigDict
    ) -> T:
        """Load config from dictionary."""
        config = None
        self._configs[name] = config
        return config

    def xǁConfigManagerǁload_from_dict__mutmut_2(
        self, name: str, config_class: type[T], data: ConfigDict
    ) -> T:
        """Load config from dictionary."""
        config = config_class.from_dict(None)
        self._configs[name] = config
        return config

    def xǁConfigManagerǁload_from_dict__mutmut_3(
        self, name: str, config_class: type[T], data: ConfigDict
    ) -> T:
        """Load config from dictionary."""
        config = config_class.from_dict(data)
        self._configs[name] = None
        return config

    xǁConfigManagerǁload_from_dict__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁload_from_dict__mutmut_1": xǁConfigManagerǁload_from_dict__mutmut_1,
        "xǁConfigManagerǁload_from_dict__mutmut_2": xǁConfigManagerǁload_from_dict__mutmut_2,
        "xǁConfigManagerǁload_from_dict__mutmut_3": xǁConfigManagerǁload_from_dict__mutmut_3,
    }

    def load_from_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁload_from_dict__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁload_from_dict__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    load_from_dict.__signature__ = _mutmut_signature(xǁConfigManagerǁload_from_dict__mutmut_orig)
    xǁConfigManagerǁload_from_dict__mutmut_orig.__name__ = "xǁConfigManagerǁload_from_dict"

    def xǁConfigManagerǁadd_loader__mutmut_orig(self, name: str, loader: ConfigLoader) -> None:
        """Add a loader for a configuration."""
        self._loaders[name] = loader

    def xǁConfigManagerǁadd_loader__mutmut_1(self, name: str, loader: ConfigLoader) -> None:
        """Add a loader for a configuration."""
        self._loaders[name] = None

    xǁConfigManagerǁadd_loader__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁadd_loader__mutmut_1": xǁConfigManagerǁadd_loader__mutmut_1
    }

    def add_loader(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁadd_loader__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁadd_loader__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    add_loader.__signature__ = _mutmut_signature(xǁConfigManagerǁadd_loader__mutmut_orig)
    xǁConfigManagerǁadd_loader__mutmut_orig.__name__ = "xǁConfigManagerǁadd_loader"

    def xǁConfigManagerǁvalidate_all__mutmut_orig(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_1(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(None, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_2(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, None):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_3(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr("validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_4(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(
                config,
            ):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_5(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "XXvalidateXX"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_6(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "VALIDATE"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_7(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name not in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_8(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = None
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_9(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = None
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_10(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=None)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_11(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=False)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_12(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(None, "validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_13(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, None):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_14(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr("validate"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_15(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(
                    schema,
                ):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_16(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "XXvalidateXX"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_17(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "VALIDATE"):
                    schema.validate(config_dict)

    def xǁConfigManagerǁvalidate_all__mutmut_18(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(None)

    xǁConfigManagerǁvalidate_all__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁvalidate_all__mutmut_1": xǁConfigManagerǁvalidate_all__mutmut_1,
        "xǁConfigManagerǁvalidate_all__mutmut_2": xǁConfigManagerǁvalidate_all__mutmut_2,
        "xǁConfigManagerǁvalidate_all__mutmut_3": xǁConfigManagerǁvalidate_all__mutmut_3,
        "xǁConfigManagerǁvalidate_all__mutmut_4": xǁConfigManagerǁvalidate_all__mutmut_4,
        "xǁConfigManagerǁvalidate_all__mutmut_5": xǁConfigManagerǁvalidate_all__mutmut_5,
        "xǁConfigManagerǁvalidate_all__mutmut_6": xǁConfigManagerǁvalidate_all__mutmut_6,
        "xǁConfigManagerǁvalidate_all__mutmut_7": xǁConfigManagerǁvalidate_all__mutmut_7,
        "xǁConfigManagerǁvalidate_all__mutmut_8": xǁConfigManagerǁvalidate_all__mutmut_8,
        "xǁConfigManagerǁvalidate_all__mutmut_9": xǁConfigManagerǁvalidate_all__mutmut_9,
        "xǁConfigManagerǁvalidate_all__mutmut_10": xǁConfigManagerǁvalidate_all__mutmut_10,
        "xǁConfigManagerǁvalidate_all__mutmut_11": xǁConfigManagerǁvalidate_all__mutmut_11,
        "xǁConfigManagerǁvalidate_all__mutmut_12": xǁConfigManagerǁvalidate_all__mutmut_12,
        "xǁConfigManagerǁvalidate_all__mutmut_13": xǁConfigManagerǁvalidate_all__mutmut_13,
        "xǁConfigManagerǁvalidate_all__mutmut_14": xǁConfigManagerǁvalidate_all__mutmut_14,
        "xǁConfigManagerǁvalidate_all__mutmut_15": xǁConfigManagerǁvalidate_all__mutmut_15,
        "xǁConfigManagerǁvalidate_all__mutmut_16": xǁConfigManagerǁvalidate_all__mutmut_16,
        "xǁConfigManagerǁvalidate_all__mutmut_17": xǁConfigManagerǁvalidate_all__mutmut_17,
        "xǁConfigManagerǁvalidate_all__mutmut_18": xǁConfigManagerǁvalidate_all__mutmut_18,
    }

    def validate_all(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁvalidate_all__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁvalidate_all__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    validate_all.__signature__ = _mutmut_signature(xǁConfigManagerǁvalidate_all__mutmut_orig)
    xǁConfigManagerǁvalidate_all__mutmut_orig.__name__ = "xǁConfigManagerǁvalidate_all"

    def xǁConfigManagerǁget_or_create__mutmut_orig(
        self, name: str, config_class: type[T], defaults: ConfigDict | None = None
    ) -> T:
        """Get existing config or create new one with defaults."""
        existing = self.get(name)
        if existing is not None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = config_class.from_dict(defaults or {})
        self._configs[name] = config
        return config

    def xǁConfigManagerǁget_or_create__mutmut_1(
        self, name: str, config_class: type[T], defaults: ConfigDict | None = None
    ) -> T:
        """Get existing config or create new one with defaults."""
        existing = None
        if existing is not None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = config_class.from_dict(defaults or {})
        self._configs[name] = config
        return config

    def xǁConfigManagerǁget_or_create__mutmut_2(
        self, name: str, config_class: type[T], defaults: ConfigDict | None = None
    ) -> T:
        """Get existing config or create new one with defaults."""
        existing = self.get(None)
        if existing is not None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = config_class.from_dict(defaults or {})
        self._configs[name] = config
        return config

    def xǁConfigManagerǁget_or_create__mutmut_3(
        self, name: str, config_class: type[T], defaults: ConfigDict | None = None
    ) -> T:
        """Get existing config or create new one with defaults."""
        existing = self.get(name)
        if existing is None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = config_class.from_dict(defaults or {})
        self._configs[name] = config
        return config

    def xǁConfigManagerǁget_or_create__mutmut_4(
        self, name: str, config_class: type[T], defaults: ConfigDict | None = None
    ) -> T:
        """Get existing config or create new one with defaults."""
        existing = self.get(name)
        if existing is not None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = None
        self._configs[name] = config
        return config

    def xǁConfigManagerǁget_or_create__mutmut_5(
        self, name: str, config_class: type[T], defaults: ConfigDict | None = None
    ) -> T:
        """Get existing config or create new one with defaults."""
        existing = self.get(name)
        if existing is not None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = config_class.from_dict(None)
        self._configs[name] = config
        return config

    def xǁConfigManagerǁget_or_create__mutmut_6(
        self, name: str, config_class: type[T], defaults: ConfigDict | None = None
    ) -> T:
        """Get existing config or create new one with defaults."""
        existing = self.get(name)
        if existing is not None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = config_class.from_dict(defaults and {})
        self._configs[name] = config
        return config

    def xǁConfigManagerǁget_or_create__mutmut_7(
        self, name: str, config_class: type[T], defaults: ConfigDict | None = None
    ) -> T:
        """Get existing config or create new one with defaults."""
        existing = self.get(name)
        if existing is not None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = config_class.from_dict(defaults or {})
        self._configs[name] = None
        return config

    xǁConfigManagerǁget_or_create__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigManagerǁget_or_create__mutmut_1": xǁConfigManagerǁget_or_create__mutmut_1,
        "xǁConfigManagerǁget_or_create__mutmut_2": xǁConfigManagerǁget_or_create__mutmut_2,
        "xǁConfigManagerǁget_or_create__mutmut_3": xǁConfigManagerǁget_or_create__mutmut_3,
        "xǁConfigManagerǁget_or_create__mutmut_4": xǁConfigManagerǁget_or_create__mutmut_4,
        "xǁConfigManagerǁget_or_create__mutmut_5": xǁConfigManagerǁget_or_create__mutmut_5,
        "xǁConfigManagerǁget_or_create__mutmut_6": xǁConfigManagerǁget_or_create__mutmut_6,
        "xǁConfigManagerǁget_or_create__mutmut_7": xǁConfigManagerǁget_or_create__mutmut_7,
    }

    def get_or_create(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigManagerǁget_or_create__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigManagerǁget_or_create__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_or_create.__signature__ = _mutmut_signature(xǁConfigManagerǁget_or_create__mutmut_orig)
    xǁConfigManagerǁget_or_create__mutmut_orig.__name__ = "xǁConfigManagerǁget_or_create"


# Global configuration manager instance
_manager = ConfigManager()


def x_get_config__mutmut_orig(name: str) -> BaseConfig | None:
    """Get a configuration from the global manager.

    Args:
        name: Configuration name

    Returns:
        Configuration instance or None

    """
    return _manager.get(name)


def x_get_config__mutmut_1(name: str) -> BaseConfig | None:
    """Get a configuration from the global manager.

    Args:
        name: Configuration name

    Returns:
        Configuration instance or None

    """
    return _manager.get(None)


x_get_config__mutmut_mutants: ClassVar[MutantDict] = {"x_get_config__mutmut_1": x_get_config__mutmut_1}


def get_config(*args, **kwargs):
    result = _mutmut_trampoline(x_get_config__mutmut_orig, x_get_config__mutmut_mutants, args, kwargs)
    return result


get_config.__signature__ = _mutmut_signature(x_get_config__mutmut_orig)
x_get_config__mutmut_orig.__name__ = "x_get_config"


def x_set_config__mutmut_orig(name: str, config: BaseConfig) -> None:
    """Set a configuration in the global manager.

    Args:
        name: Configuration name
        config: Configuration instance

    """
    _manager.set(name, config)


def x_set_config__mutmut_1(name: str, config: BaseConfig) -> None:
    """Set a configuration in the global manager.

    Args:
        name: Configuration name
        config: Configuration instance

    """
    _manager.set(None, config)


def x_set_config__mutmut_2(name: str, config: BaseConfig) -> None:
    """Set a configuration in the global manager.

    Args:
        name: Configuration name
        config: Configuration instance

    """
    _manager.set(name, None)


def x_set_config__mutmut_3(name: str, config: BaseConfig) -> None:
    """Set a configuration in the global manager.

    Args:
        name: Configuration name
        config: Configuration instance

    """
    _manager.set(config)


def x_set_config__mutmut_4(name: str, config: BaseConfig) -> None:
    """Set a configuration in the global manager.

    Args:
        name: Configuration name
        config: Configuration instance

    """
    _manager.set(
        name,
    )


x_set_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x_set_config__mutmut_1": x_set_config__mutmut_1,
    "x_set_config__mutmut_2": x_set_config__mutmut_2,
    "x_set_config__mutmut_3": x_set_config__mutmut_3,
    "x_set_config__mutmut_4": x_set_config__mutmut_4,
}


def set_config(*args, **kwargs):
    result = _mutmut_trampoline(x_set_config__mutmut_orig, x_set_config__mutmut_mutants, args, kwargs)
    return result


set_config.__signature__ = _mutmut_signature(x_set_config__mutmut_orig)
x_set_config__mutmut_orig.__name__ = "x_set_config"


def x_register_config__mutmut_orig(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, config, schema, loader, defaults)


def x_register_config__mutmut_1(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(None, config, schema, loader, defaults)


def x_register_config__mutmut_2(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, None, schema, loader, defaults)


def x_register_config__mutmut_3(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, config, None, loader, defaults)


def x_register_config__mutmut_4(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, config, schema, None, defaults)


def x_register_config__mutmut_5(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, config, schema, loader, None)


def x_register_config__mutmut_6(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(config, schema, loader, defaults)


def x_register_config__mutmut_7(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, schema, loader, defaults)


def x_register_config__mutmut_8(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, config, loader, defaults)


def x_register_config__mutmut_9(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, config, schema, defaults)


def x_register_config__mutmut_10(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(
        name,
        config,
        schema,
        loader,
    )


x_register_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x_register_config__mutmut_1": x_register_config__mutmut_1,
    "x_register_config__mutmut_2": x_register_config__mutmut_2,
    "x_register_config__mutmut_3": x_register_config__mutmut_3,
    "x_register_config__mutmut_4": x_register_config__mutmut_4,
    "x_register_config__mutmut_5": x_register_config__mutmut_5,
    "x_register_config__mutmut_6": x_register_config__mutmut_6,
    "x_register_config__mutmut_7": x_register_config__mutmut_7,
    "x_register_config__mutmut_8": x_register_config__mutmut_8,
    "x_register_config__mutmut_9": x_register_config__mutmut_9,
    "x_register_config__mutmut_10": x_register_config__mutmut_10,
}


def register_config(*args, **kwargs):
    result = _mutmut_trampoline(
        x_register_config__mutmut_orig, x_register_config__mutmut_mutants, args, kwargs
    )
    return result


register_config.__signature__ = _mutmut_signature(x_register_config__mutmut_orig)
x_register_config__mutmut_orig.__name__ = "x_register_config"


def x_load_config__mutmut_orig(name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
    """Load a configuration using the global manager.

    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader

    Returns:
        Configuration instance

    """
    return _manager.load(name, config_class, loader)


def x_load_config__mutmut_1(name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
    """Load a configuration using the global manager.

    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader

    Returns:
        Configuration instance

    """
    return _manager.load(None, config_class, loader)


def x_load_config__mutmut_2(name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
    """Load a configuration using the global manager.

    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader

    Returns:
        Configuration instance

    """
    return _manager.load(name, None, loader)


def x_load_config__mutmut_3(name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
    """Load a configuration using the global manager.

    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader

    Returns:
        Configuration instance

    """
    return _manager.load(name, config_class, None)


def x_load_config__mutmut_4(name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
    """Load a configuration using the global manager.

    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader

    Returns:
        Configuration instance

    """
    return _manager.load(config_class, loader)


def x_load_config__mutmut_5(name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
    """Load a configuration using the global manager.

    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader

    Returns:
        Configuration instance

    """
    return _manager.load(name, loader)


def x_load_config__mutmut_6(name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
    """Load a configuration using the global manager.

    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader

    Returns:
        Configuration instance

    """
    return _manager.load(
        name,
        config_class,
    )


x_load_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x_load_config__mutmut_1": x_load_config__mutmut_1,
    "x_load_config__mutmut_2": x_load_config__mutmut_2,
    "x_load_config__mutmut_3": x_load_config__mutmut_3,
    "x_load_config__mutmut_4": x_load_config__mutmut_4,
    "x_load_config__mutmut_5": x_load_config__mutmut_5,
    "x_load_config__mutmut_6": x_load_config__mutmut_6,
}


def load_config(*args, **kwargs):
    result = _mutmut_trampoline(x_load_config__mutmut_orig, x_load_config__mutmut_mutants, args, kwargs)
    return result


load_config.__signature__ = _mutmut_signature(x_load_config__mutmut_orig)
x_load_config__mutmut_orig.__name__ = "x_load_config"


# <3 🧱🤝⚙️🪄
