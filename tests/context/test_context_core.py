#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the unified Context class."""

import os
from pathlib import Path
import tempfile

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.context import CLIContext as Context
from provide.foundation.errors.runtime import StateError


class TestContext(FoundationTestCase):
    """Test the unified Context class."""

    def test_context_initialization(self) -> None:
        """Test basic context initialization."""
        ctx = Context(log_level="DEBUG", profile="dev", debug=True)

        assert ctx.log_level == "DEBUG"
        assert ctx.profile == "dev"
        assert ctx.debug is True
        assert ctx.json_output is False  # Default

    def test_context_defaults(self) -> None:
        """Test context default values."""
        ctx = Context()

        assert ctx.log_level == "INFO"
        assert ctx.profile == "default"
        assert ctx.debug is False
        assert ctx.json_output is False
        assert ctx.config_file is None
        assert ctx.log_file is None

    def test_context_from_env(self) -> None:
        """Test loading context from environment variables."""
        # Set environment variables
        os.environ["PROVIDE_LOG_LEVEL"] = "WARNING"
        os.environ["PROVIDE_PROFILE"] = "production"
        os.environ["PROVIDE_DEBUG"] = "true"
        os.environ["PROVIDE_JSON_OUTPUT"] = "1"

        try:
            ctx = Context.from_env()

            assert ctx.log_level == "WARNING"
            assert ctx.profile == "production"
            assert ctx.debug is True
            assert ctx.json_output is True
        finally:
            # Clean up
            os.environ.pop("PROVIDE_LOG_LEVEL", None)
            os.environ.pop("PROVIDE_PROFILE", None)
            os.environ.pop("PROVIDE_DEBUG", None)
            os.environ.pop("PROVIDE_JSON_OUTPUT", None)

    def test_context_update_from_env(self) -> None:
        """Test updating existing context from environment."""
        ctx = Context(log_level="INFO", profile="dev")

        os.environ["PROVIDE_LOG_LEVEL"] = "ERROR"

        try:
            ctx.update_from_env()
            assert ctx.log_level == "ERROR"
            assert ctx.profile == "dev"  # Unchanged
        finally:
            os.environ.pop("PROVIDE_LOG_LEVEL", None)

    def test_context_to_dict(self) -> None:
        """Test converting context to dictionary."""
        ctx = Context(
            log_level="DEBUG",
            profile="test",
            debug=True,
            json_output=True,
            config_file=Path("/path/to/config"),
            log_file=Path("/path/to/log"),
        )

        data = ctx.to_dict()

        assert data["log_level"] == "DEBUG"
        assert data["profile"] == "test"
        assert data["debug"] is True
        assert data["json_output"] is True
        assert data["config_file"] == "/path/to/config"
        assert data["log_file"] == "/path/to/log"

    def test_context_from_dict(self) -> None:
        """Test creating context from dictionary."""
        data = {
            "log_level": "WARNING",
            "profile": "staging",
            "debug": False,
            "json_output": True,
            "config_file": "/etc/app/config.toml",
            "log_file": "/var/log/app.log",
        }

        ctx = Context.from_dict(data)

        assert ctx.log_level == "WARNING"
        assert ctx.profile == "staging"
        assert ctx.debug is False
        assert ctx.json_output is True
        assert ctx.config_file == Path("/etc/app/config.toml")
        assert ctx.log_file == Path("/var/log/app.log")

    def test_context_load_config_toml(self) -> None:
        """Test loading configuration from TOML file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write("""
log_level = "ERROR"
profile = "production"
debug = false
json_output = true
            """)
            config_path = f.name

        try:
            ctx = Context()
            ctx.load_config(config_path)

            assert ctx.log_level == "ERROR"
            assert ctx.profile == "production"
            assert ctx.debug is False
            assert ctx.json_output is True
        finally:
            Path(config_path).unlink()

    def test_context_load_config_json(self) -> None:
        """Test loading configuration from JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("""
{
    "log_level": "WARNING",
    "profile": "staging",
    "debug": true,
    "json_output": false
}
            """)
            config_path = f.name

        try:
            ctx = Context()
            ctx.load_config(config_path)

            assert ctx.log_level == "WARNING"
            assert ctx.profile == "staging"
            assert ctx.debug is True
            assert ctx.json_output is False
        finally:
            Path(config_path).unlink()

    def test_context_load_config_yaml(self) -> None:
        """Test loading configuration from YAML file."""
        pytest.importorskip("yaml")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("""
log_level: INFO
profile: development
debug: true
json_output: true
            """)
            config_path = f.name

        try:
            ctx = Context()
            ctx.load_config(config_path)

            assert ctx.log_level == "INFO"
            assert ctx.profile == "development"
            assert ctx.debug is True
            assert ctx.json_output is True
        finally:
            Path(config_path).unlink()

    def test_context_save_config(self) -> None:
        """Test saving configuration to file."""
        ctx = Context(
            log_level="DEBUG",
            profile="test",
            debug=True,
            json_output=False,
        )

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            config_path = f.name

        try:
            ctx.save_config(config_path)

            # Load it back
            new_ctx = Context()
            new_ctx.load_config(config_path)

            assert new_ctx.log_level == ctx.log_level
            assert new_ctx.profile == ctx.profile
            assert new_ctx.debug == ctx.debug
            assert new_ctx.json_output == ctx.json_output
        finally:
            Path(config_path).unlink()

    def test_context_merge(self) -> None:
        """Test merging contexts with precedence."""
        base_ctx = Context(log_level="INFO", profile="base", debug=False)
        override_ctx = Context(log_level="DEBUG", debug=True)

        merged = base_ctx.merge(override_ctx)

        assert merged.log_level == "DEBUG"  # Overridden
        assert merged.profile == "base"  # Not overridden since override has default value
        assert merged.debug is True  # Overridden

        # Test with explicit None handling
        base_ctx2 = Context(log_level="INFO", profile="production")
        override_ctx2 = Context(
            log_level="WARNING",
            profile="staging",
            config_file=Path("/etc/app.conf"),
        )

        merged2 = base_ctx2.merge(override_ctx2)
        assert merged2.log_level == "WARNING"
        assert merged2.profile == "staging"
        assert merged2.config_file == Path("/etc/app.conf")

    def test_context_logger_property(self) -> None:
        """Test lazy logger initialization."""
        ctx = Context(log_level="DEBUG")

        # Logger should be created on first access
        assert ctx._logger is None
        logger = ctx.logger
        assert logger is not None
        assert ctx._logger is logger

        # Should return same logger on subsequent access
        assert ctx.logger is logger

    def test_context_validation(self) -> None:
        """Test context value validation."""
        # Invalid log level should raise
        with pytest.raises(ValueError, match="must be in"):
            Context(log_level="INVALID")

        # Invalid string values should raise ValueError
        with pytest.raises(ValueError):
            Context(debug="not_a_bool")

        # Invalid numeric values (not 0 or 1) should raise ValueError
        with pytest.raises(ValueError, match="Numeric boolean must be 0 or 1"):
            Context(json_output=123)

    def test_context_environment_precedence(self) -> None:
        """Test that environment variables override config file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write("""
log_level = "INFO"
profile = "config_profile"
            """)
            config_path = f.name

        os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"

        try:
            ctx = Context()
            ctx.load_config(config_path)
            ctx.update_from_env()

            assert ctx.log_level == "DEBUG"  # From env
            assert ctx.profile == "config_profile"  # From config
        finally:
            os.environ.pop("PROVIDE_LOG_LEVEL", None)
            Path(config_path).unlink()

    def test_context_immutable_after_freeze(self) -> None:
        """Test that context can be frozen to prevent changes."""
        ctx = Context(log_level="INFO")
        ctx.freeze()

        # With attrs, we can't dynamically freeze attributes
        # But we can prevent certain operations
        with pytest.raises(StateError, match="Context is frozen"):
            ctx.update_from_env()

    def test_context_copy(self) -> None:
        """Test creating a copy of context."""
        ctx = Context(log_level="DEBUG", profile="original")
        copy = ctx.copy()

        assert copy.log_level == ctx.log_level
        assert copy.profile == ctx.profile
        assert copy is not ctx

        # Modifying copy shouldn't affect original
        copy.log_level = "INFO"
        assert ctx.log_level == "DEBUG"


# 🧱🏗️🔚
