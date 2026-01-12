#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for config manager module."""

from attrs import define
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock

from provide.foundation.config.base import BaseConfig, field
from provide.foundation.config.loader import ConfigLoader
from provide.foundation.config.manager import (
    _manager,
    get_config,
    load_config,
    register_config,
    set_config,
)
from provide.foundation.config.schema import ConfigSchema


@define
class SampleConfigClass(BaseConfig):
    """Sample configuration class for testing."""

    name: str = field(default="test")


class TestGlobalFunctions(FoundationTestCase):
    """Test global configuration manager functions."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Reset global manager
        _manager.clear()
        self.test_config = SampleConfigClass(name="global_test")

    def test_get_config_global(self) -> None:
        """Test global get_config function."""
        _manager._configs["test"] = self.test_config

        result = get_config("test")

        assert result is self.test_config

    def test_set_config_global(self) -> None:
        """Test global set_config function."""
        set_config("test", self.test_config)

        assert _manager._configs["test"] is self.test_config

    def test_register_config_global(self) -> None:
        """Test global register_config function."""
        schema = Mock(spec=ConfigSchema)
        loader = Mock(spec=ConfigLoader)
        defaults = {"name": "default"}

        register_config("test", self.test_config, schema, loader, defaults)

        assert _manager._configs["test"] is self.test_config
        assert _manager._schemas["test"] is schema
        assert _manager._loaders["test"] is loader
        assert _manager._defaults["test"] == defaults

    def test_load_config_global(self) -> None:
        """Test global load_config function."""
        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=self.test_config)

        result = load_config("test", SampleConfigClass, loader)

        assert result is self.test_config
        loader.load.assert_called_once_with(SampleConfigClass)


# 🧱🏗️🔚
