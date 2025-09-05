#
# tests/test_config.py
#
"""Tests for provide.foundation.config module."""

import os
import tempfile
from pathlib import Path

import attrs
import pytest

from provide.foundation.config import BaseConfig, ConfigError, load_config_with_precedence


@attrs.define
class TestConfig(BaseConfig):
    """Test configuration class."""
    name: str = "default"
    port: int = 8080
    debug: bool = False
    timeout: float = 30.0
    data_dir: Path = Path("/tmp")
    optional_field: str | None = None


@attrs.define
class EmptyConfig(BaseConfig):
    """Empty configuration for testing."""
    pass


class TestBaseConfig:
    """Test BaseConfig functionality."""

    def test_default_initialization(self) -> None:
        """Test creating config with defaults."""
        config = TestConfig()
        assert config.name == "default"
        assert config.port == 8080
        assert config.debug is False
        assert config.timeout == 30.0
        assert config.data_dir == Path("/tmp")
        assert config.optional_field is None

    def test_from_dict(self) -> None:
        """Test creating config from dictionary."""
        data = {
            "name": "test_app",
            "port": 9000,
            "debug": True,
            "timeout": 60.5,
            "data_dir": "/var/data",
            "optional_field": "test_value"
        }
        
        config = TestConfig.from_dict(data)
        assert config.name == "test_app"
        assert config.port == 9000
        assert config.debug is True
        assert config.timeout == 60.5
        assert config.data_dir == Path("/var/data")
        assert config.optional_field == "test_value"

    def test_from_dict_with_type_conversion(self) -> None:
        """Test type conversion in from_dict."""
        data = {
            "port": "9000",  # String that should become int
            "timeout": "45.5",  # String that should become float
            "data_dir": "/custom/path"  # String that should become Path
        }
        
        config = TestConfig.from_dict(data)
        assert config.port == 9000
        assert isinstance(config.port, int)
        assert config.timeout == 45.5
        assert isinstance(config.timeout, float)
        assert config.data_dir == Path("/custom/path")
        assert isinstance(config.data_dir, Path)

    def test_from_dict_invalid_types(self) -> None:
        """Test error handling for invalid type conversion."""
        with pytest.raises(ConfigError, match="Invalid integer value"):
            TestConfig.from_dict({"port": "not_a_number"})
        
        with pytest.raises(ConfigError, match="Invalid float value"):
            TestConfig.from_dict({"timeout": "not_a_float"})

    def test_from_env_basic(self) -> None:
        """Test loading from environment variables."""
        env_vars = {
            "NAME": "env_app",
            "PORT": "7000",
            "DEBUG": "true",
            "TIMEOUT": "120.5",
            "DATA_DIR": "/env/data",
            "OPTIONAL_FIELD": "env_value"
        }
        
        # Set environment variables
        original_env = {}
        for key, value in env_vars.items():
            original_env[key] = os.environ.get(key)
            os.environ[key] = value
        
        try:
            config = TestConfig.from_env()
            assert config.name == "env_app"
            assert config.port == 7000
            assert config.debug is True
            assert config.timeout == 120.5
            assert config.data_dir == Path("/env/data")
            assert config.optional_field == "env_value"
        finally:
            # Restore environment
            for key, original_value in original_env.items():
                if original_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = original_value

    def test_from_env_with_prefix(self) -> None:
        """Test loading from environment variables with prefix."""
        env_vars = {
            "MYAPP_NAME": "prefixed_app",
            "MYAPP_PORT": "6000"
        }
        
        original_env = {}
        for key, value in env_vars.items():
            original_env[key] = os.environ.get(key)
            os.environ[key] = value
        
        try:
            config = TestConfig.from_env("MYAPP")
            assert config.name == "prefixed_app"
            assert config.port == 6000
            # Other fields should have defaults
            assert config.debug is False
        finally:
            for key, original_value in original_env.items():
                if original_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = original_value

    def test_from_env_boolean_parsing(self) -> None:
        """Test boolean parsing from environment."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("yes", True),
            ("YES", True),
            ("on", True),
            ("ON", True),
            ("false", False),
            ("False", False),
            ("0", False),
            ("no", False),
            ("off", False),
            ("", False),
            ("anything_else", False)
        ]
        
        for env_value, expected in test_cases:
            os.environ["DEBUG"] = env_value
            try:
                config = TestConfig.from_env()
                assert config.debug == expected, f"Failed for env_value: {env_value}"
            finally:
                os.environ.pop("DEBUG", None)

    def test_from_toml_file(self) -> None:
        """Test loading from TOML file."""
        toml_content = """
name = "toml_app"
port = 5000
debug = true
timeout = 90.0
data_dir = "/toml/data"
optional_field = "toml_value"
"""
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(toml_content)
            toml_path = Path(f.name)
        
        try:
            config = TestConfig.from_toml_file(toml_path)
            assert config.name == "toml_app"
            assert config.port == 5000
            assert config.debug is True
            assert config.timeout == 90.0
            assert config.data_dir == Path("/toml/data")
            assert config.optional_field == "toml_value"
        finally:
            toml_path.unlink()

    def test_from_toml_file_with_nested_section(self) -> None:
        """Test loading from TOML file with nested section."""
        toml_content = """
[test]
name = "nested_app"
port = 4000
"""
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(toml_content)
            toml_path = Path(f.name)
        
        try:
            config = TestConfig.from_toml_file(toml_path)
            assert config.name == "nested_app"
            assert config.port == 4000
        finally:
            toml_path.unlink()

    def test_from_toml_file_not_found(self) -> None:
        """Test error when TOML file doesn't exist."""
        with pytest.raises(ConfigError, match="Configuration file not found"):
            TestConfig.from_toml_file("/nonexistent/file.toml")

    def test_from_toml_file_invalid_toml(self) -> None:
        """Test error when TOML file is invalid."""
        invalid_toml = "invalid toml content [[[["
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(invalid_toml)
            toml_path = Path(f.name)
        
        try:
            with pytest.raises(ConfigError, match="Invalid TOML file"):
                TestConfig.from_toml_file(toml_path)
        finally:
            toml_path.unlink()

    def test_merge(self) -> None:
        """Test merging configurations."""
        config1 = TestConfig(name="app1", port=8000)
        config2 = TestConfig(name="app2", debug=True)
        
        merged = config1.merge(config2)
        assert merged.name == "app2"  # config2 takes precedence
        assert merged.port == 8000  # config1 value preserved
        assert merged.debug is True  # config2 value
        assert merged.timeout == 30.0  # default value

    def test_merge_incompatible_types(self) -> None:
        """Test merge with incompatible types."""
        config1 = TestConfig()
        config2 = EmptyConfig()
        
        with pytest.raises(ConfigError, match="Cannot merge"):
            config1.merge(config2)

    def test_to_env_dict(self) -> None:
        """Test converting config to environment dictionary."""
        config = TestConfig(
            name="test_app",
            port=9000,
            debug=True,
            data_dir=Path("/test/data"),
            optional_field="test_value"
        )
        
        env_dict = config.to_env_dict()
        expected = {
            "NAME": "test_app",
            "PORT": "9000",
            "DEBUG": "true",
            "TIMEOUT": "30.0",
            "DATA_DIR": "/test/data",
            "OPTIONAL_FIELD": "test_value"
        }
        assert env_dict == expected

    def test_to_env_dict_with_prefix(self) -> None:
        """Test converting config to environment dictionary with prefix."""
        config = TestConfig(name="test_app", port=9000)
        
        env_dict = config.to_env_dict("MYAPP")
        assert "MYAPP_NAME" in env_dict
        assert "MYAPP_PORT" in env_dict
        assert env_dict["MYAPP_NAME"] == "test_app"
        assert env_dict["MYAPP_PORT"] == "9000"

    def test_to_env_dict_excludes_none(self) -> None:
        """Test that None values are excluded from environment dict."""
        config = TestConfig(optional_field=None)
        
        env_dict = config.to_env_dict()
        assert "OPTIONAL_FIELD" not in env_dict


class TestLoadConfigWithPrecedence:
    """Test the load_config_with_precedence utility."""

    def test_precedence_order(self) -> None:
        """Test that configuration precedence works correctly."""
        # Create TOML file
        toml_content = """
name = "file_app"
port = 3000
debug = false
"""
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(toml_content)
            toml_path = Path(f.name)
        
        # Set environment variable
        os.environ["PORT"] = "4000"
        os.environ["DEBUG"] = "true"
        
        try:
            # Load with precedence: explicit > env > file > defaults
            config = load_config_with_precedence(
                TestConfig,
                config_files=[toml_path],
                explicit_config={"name": "explicit_app"}
            )
            
            # explicit_config should win for name
            assert config.name == "explicit_app"
            # env should win for port and debug
            assert config.port == 4000
            assert config.debug is True
            # defaults for timeout
            assert config.timeout == 30.0
            
        finally:
            os.environ.pop("PORT", None)
            os.environ.pop("DEBUG", None)
            toml_path.unlink()

    def test_multiple_config_files(self) -> None:
        """Test loading from multiple config files with later ones taking precedence."""
        # First file
        toml1_content = """
name = "app1"
port = 1000
debug = false
"""
        
        # Second file
        toml2_content = """
name = "app2"
port = 2000
# debug not specified, should keep value from first file
"""
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f1:
            f1.write(toml1_content)
            toml1_path = Path(f1.name)
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f2:
            f2.write(toml2_content)
            toml2_path = Path(f2.name)
        
        try:
            config = load_config_with_precedence(
                TestConfig,
                config_files=[toml1_path, toml2_path]
            )
            
            assert config.name == "app2"  # Second file wins
            assert config.port == 2000  # Second file wins
            assert config.debug is False  # First file value preserved
            
        finally:
            toml1_path.unlink()
            toml2_path.unlink()

    def test_nonexistent_config_files_ignored(self) -> None:
        """Test that nonexistent config files are ignored."""
        config = load_config_with_precedence(
            TestConfig,
            config_files=[Path("/nonexistent/file.toml")]
        )
        
        # Should use defaults since file doesn't exist
        assert config.name == "default"
        assert config.port == 8080

    def test_empty_config_class(self) -> None:
        """Test with empty configuration class."""
        config = load_config_with_precedence(EmptyConfig)
        assert isinstance(config, EmptyConfig)


# 🏗️🧪⚙️🪄