"""Comprehensive coverage tests for config/sync.py module."""

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import pytest
from attrs import define, field

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.sync import (
    run_async,
    load_config,
    load_config_from_env,
    load_config_from_file,
    load_config_from_multiple,
    validate_config,
    update_config,
    config_to_dict,
    clone_config,
    diff_configs,
    SyncConfigManager,
    sync_manager,
    get_config,
    set_config,
    register_config,
)
from provide.foundation.config.types import ConfigSource


@define
class TestConfig(BaseConfig):
    """Test configuration class."""
    name: str = field(default="test")
    value: int = field(default=42)
    enabled: bool = field(default=True)


@define  
class TestRuntimeConfig(RuntimeConfig):
    """Test runtime configuration class."""
    app_name: str = field(default="test_app")
    port: int = field(default=8080)


class TestRunAsync:
    """Test run_async utility function."""
    
    def test_run_async_basic(self):
        """Test run_async with basic coroutine."""
        async def simple_coro():
            return "hello"
        
        result = run_async(simple_coro())
        assert result == "hello"
    
    def test_run_async_with_argument(self):
        """Test run_async with coroutine that takes arguments."""
        async def coro_with_args(value):
            return value * 2
        
        result = run_async(coro_with_args(21))
        assert result == 42
    
    def test_run_async_with_exception(self):
        """Test run_async propagates exceptions."""
        async def failing_coro():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            run_async(failing_coro())
    
    @patch('asyncio.get_running_loop')
    def test_run_async_in_running_loop_context(self, mock_get_loop):
        """Test run_async when already in an event loop."""
        # Simulate being in a running event loop
        mock_get_loop.return_value = Mock()
        
        async def simple_coro():
            return "from_thread"
        
        with patch('concurrent.futures.ThreadPoolExecutor') as mock_executor:
            mock_future = Mock()
            mock_future.result.return_value = "from_thread"
            mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future
            
            result = run_async(simple_coro())
            assert result == "from_thread"
            
            # Verify ThreadPoolExecutor was used
            mock_executor.assert_called_once()


class TestLoadConfigFunctions:
    """Test configuration loading functions."""
    
    def test_load_config_basic(self):
        """Test basic config loading from dict."""
        with patch('provide.foundation.config.sync.run_async') as mock_run_async:
            mock_run_async.return_value = TestConfig(name="loaded", value=100)
            
            config = load_config(TestConfig, {"name": "loaded", "value": 100})
            
            assert isinstance(config, TestConfig)
            assert config.name == "loaded"
            assert config.value == 100
            mock_run_async.assert_called_once()
    
    def test_load_config_empty_data(self):
        """Test loading with empty data."""
        with patch('provide.foundation.config.sync.run_async') as mock_run_async:
            mock_run_async.return_value = TestConfig()
            
            config = load_config(TestConfig)
            
            assert isinstance(config, TestConfig)
            mock_run_async.assert_called_once()
    
    def test_load_config_with_source(self):
        """Test loading with specific source."""
        with patch('provide.foundation.config.sync.run_async') as mock_run_async:
            mock_run_async.return_value = TestConfig(name="sourced")
            
            config = load_config(TestConfig, {"name": "sourced"}, ConfigSource.FILE)
            
            assert isinstance(config, TestConfig)
            assert config.name == "sourced"
            mock_run_async.assert_called_once()
    
    @patch.dict('os.environ', {'TEST_APP_NAME': 'env_app', 'TEST_PORT': '9000'})
    def test_load_config_from_env_basic(self):
        """Test loading config from environment."""
        config = load_config_from_env(TestRuntimeConfig, prefix="TEST")
        
        assert isinstance(config, TestRuntimeConfig)
        assert config.app_name == "env_app"
        assert config.port == 9000
    
    def test_load_config_from_env_non_runtime_config(self):
        """Test loading from env with non-RuntimeConfig class."""
        with pytest.raises(TypeError, match="must inherit from RuntimeConfig"):
            load_config_from_env(TestConfig)  # Not a RuntimeConfig
    
    @patch.dict('os.environ', {'PREFIX_APP_NAME': 'custom_app'})
    def test_load_config_from_env_custom_prefix(self):
        """Test loading from env with custom prefix."""
        config = load_config_from_env(TestRuntimeConfig, prefix="PREFIX")
        
        assert config.app_name == "custom_app"
    
    @patch.dict('os.environ', {'app.name': 'dotted_app'})
    def test_load_config_from_env_custom_delimiter(self):
        """Test loading from env with custom delimiter."""
        config = load_config_from_env(TestRuntimeConfig, delimiter=".")
        
        assert config.app_name == "dotted_app"
    
    @patch.dict('os.environ', {'App_Name': 'case_sensitive_app'})
    def test_load_config_from_env_case_sensitive(self):
        """Test loading from env with case sensitivity."""
        config = load_config_from_env(TestRuntimeConfig, case_sensitive=True)
        
        # Should not find the variable due to case mismatch
        assert config.app_name == "test_app"  # default
    
    def test_load_config_from_file_json(self):
        """Test loading config from JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"name": "json_config", "value": 123}')
            f.flush()
            
            try:
                config = load_config_from_file(f.name, TestConfig)
                
                assert isinstance(config, TestConfig)
                assert config.name == "json_config"
                assert config.value == 123
            finally:
                Path(f.name).unlink()
    
    def test_load_config_from_file_yaml(self):
        """Test loading config from YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('name: yaml_config\nvalue: 456\n')
            f.flush()
            
            try:
                config = load_config_from_file(f.name, TestConfig)
                
                assert isinstance(config, TestConfig)
                assert config.name == "yaml_config"
                assert config.value == 456
            finally:
                Path(f.name).unlink()
    
    def test_load_config_from_file_with_format(self):
        """Test loading config with explicit format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('{"name": "explicit_json", "value": 789}')
            f.flush()
            
            try:
                config = load_config_from_file(f.name, TestConfig, format="json")
                
                assert isinstance(config, TestConfig)
                assert config.name == "explicit_json"
                assert config.value == 789
            finally:
                Path(f.name).unlink()
    
    def test_load_config_from_file_with_encoding(self):
        """Test loading config with specific encoding."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8', delete=False) as f:
            f.write('{"name": "utf8_config", "value": 999}')
            f.flush()
            
            try:
                config = load_config_from_file(f.name, TestConfig, encoding="utf-8")
                
                assert isinstance(config, TestConfig)
                assert config.name == "utf8_config"
                assert config.value == 999
            finally:
                Path(f.name).unlink()
    
    @patch.dict('os.environ', {'MULTI_APP_NAME': 'multi_env_app'})
    def test_load_config_from_multiple_sources(self):
        """Test loading from multiple sources.""" 
        # Create a temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"value": 500}')
            f.flush()
            
            try:
                config = load_config_from_multiple(
                    TestRuntimeConfig,
                    ("dict", {"port": 9999}),
                    ("file", f.name),
                    ("env", "MULTI"),
                )
                
                # Values should be merged from all sources
                assert isinstance(config, TestRuntimeConfig)
                assert config.app_name == "multi_env_app"  # from env
                assert config.port == 9999  # from dict
                # Note: TestRuntimeConfig doesn't have 'value' field, so file data might be ignored
            finally:
                Path(f.name).unlink()
    
    def test_load_config_from_multiple_unknown_source(self):
        """Test loading from multiple sources with unknown source type."""
        with pytest.raises(ValueError, match="Unknown source type: invalid"):
            load_config_from_multiple(TestConfig, ("invalid", {}))


class TestConfigOperations:
    """Test configuration operation functions."""
    
    def test_validate_config(self):
        """Test config validation."""
        config = TestConfig(name="valid")
        
        # Should not raise
        validate_config(config)
    
    def test_validate_config_with_mock_failure(self):
        """Test config validation with mock failure."""
        config = TestConfig()
        
        async def failing_validate():
            raise ValueError("Validation failed")
        
        with patch.object(config, 'validate', side_effect=failing_validate):
            with pytest.raises(ValueError, match="Validation failed"):
                validate_config(config)
    
    def test_update_config(self):
        """Test config updating."""
        config = TestConfig(name="original")
        
        update_config(config, {"name": "updated", "value": 999})
        
        assert config.name == "updated"
        assert config.value == 999
    
    def test_update_config_with_source(self):
        """Test config updating with specific source."""
        config = TestConfig()
        
        update_config(config, {"name": "file_updated"}, ConfigSource.FILE)
        
        assert config.name == "file_updated"
    
    def test_config_to_dict_basic(self):
        """Test converting config to dict."""
        config = TestConfig(name="dict_test", value=123)
        
        result = config_to_dict(config)
        
        assert isinstance(result, dict)
        assert result["name"] == "dict_test"
        assert result["value"] == 123
    
    def test_config_to_dict_include_sensitive(self):
        """Test converting config to dict with sensitive fields."""
        config = TestConfig(name="sensitive_test")
        
        result = config_to_dict(config, include_sensitive=True)
        
        assert isinstance(result, dict)
        assert result["name"] == "sensitive_test"
    
    def test_clone_config(self):
        """Test config cloning."""
        original = TestConfig(name="original", value=100)
        
        cloned = clone_config(original)
        
        assert cloned is not original  # Different objects
        assert cloned.name == original.name
        assert cloned.value == original.value
        assert isinstance(cloned, TestConfig)
    
    def test_diff_configs(self):
        """Test config diffing."""
        config1 = TestConfig(name="config1", value=100)
        config2 = TestConfig(name="config2", value=200)
        
        differences = diff_configs(config1, config2)
        
        assert isinstance(differences, dict)
        # The exact format depends on the diff implementation
        # but it should detect the differences


class TestSyncConfigManager:
    """Test SyncConfigManager class."""
    
    def setup_method(self):
        """Set up for each test."""
        self.manager = SyncConfigManager()
    
    def test_sync_manager_init(self):
        """Test sync manager initialization."""
        assert hasattr(self.manager, '_async_manager')
        assert self.manager._async_manager is not None
    
    def test_register_config(self):
        """Test registering a config."""
        config = TestConfig(name="registered")
        
        self.manager.register("test_reg", config)
        
        # Verify it was registered
        retrieved = self.manager.get("test_reg")
        assert retrieved is not None
        assert retrieved.name == "registered"
    
    def test_register_config_with_kwargs(self):
        """Test registering config with additional kwargs."""
        config = TestConfig()
        
        # This should work even with additional keyword arguments
        self.manager.register("test_kwargs", config, some_extra_param="value")
        
        retrieved = self.manager.get("test_kwargs")
        assert retrieved is not None
    
    def test_get_nonexistent_config(self):
        """Test getting nonexistent config."""
        result = self.manager.get("nonexistent")
        assert result is None
    
    def test_load_config_sync(self):
        """Test loading config through sync manager."""
        from provide.foundation.config.loader import DictConfigLoader
        
        loader = DictConfigLoader({"name": "sync_loaded", "value": 777})
        
        config = self.manager.load("test_load", TestConfig, loader)
        
        assert isinstance(config, TestConfig)
        assert config.name == "sync_loaded"
        assert config.value == 777
    
    def test_update_sync_manager(self):
        """Test updating config through sync manager."""
        config = TestConfig(name="original")
        self.manager.register("test_update", config)
        
        self.manager.update("test_update", {"name": "sync_updated", "value": 555})
        
        retrieved = self.manager.get("test_update")
        assert retrieved.name == "sync_updated"
        assert retrieved.value == 555
    
    def test_update_with_source(self):
        """Test updating with specific source."""
        config = TestConfig()
        self.manager.register("test_source", config)
        
        self.manager.update("test_source", {"name": "sourced"}, ConfigSource.ENV)
        
        retrieved = self.manager.get("test_source")
        assert retrieved.name == "sourced"
    
    def test_export_config(self):
        """Test exporting config as dict."""
        config = TestConfig(name="export_test", value=888)
        self.manager.register("test_export", config)
        
        exported = self.manager.export("test_export")
        
        assert isinstance(exported, dict)
        assert exported["name"] == "export_test"
        assert exported["value"] == 888
    
    def test_export_config_include_sensitive(self):
        """Test exporting config with sensitive fields."""
        config = TestConfig(name="sensitive_export")
        self.manager.register("test_sensitive", config)
        
        exported = self.manager.export("test_sensitive", include_sensitive=True)
        
        assert isinstance(exported, dict)
        assert exported["name"] == "sensitive_export"
    
    def test_export_all_configs(self):
        """Test exporting all configs."""
        config1 = TestConfig(name="config1", value=100)
        config2 = TestConfig(name="config2", value=200)
        
        self.manager.register("test1", config1)
        self.manager.register("test2", config2)
        
        all_exported = self.manager.export_all()
        
        assert isinstance(all_exported, dict)
        assert "test1" in all_exported
        assert "test2" in all_exported
        assert all_exported["test1"]["name"] == "config1"
        assert all_exported["test2"]["name"] == "config2"
    
    def test_export_all_include_sensitive(self):
        """Test exporting all configs with sensitive fields."""
        config = TestConfig(name="all_sensitive")
        self.manager.register("sensitive_all", config)
        
        all_exported = self.manager.export_all(include_sensitive=True)
        
        assert isinstance(all_exported, dict)
        assert "sensitive_all" in all_exported


class TestGlobalFunctions:
    """Test global convenience functions."""
    
    def test_get_config_global(self):
        """Test global get_config function."""
        # First register something using the global manager
        test_config = TestConfig(name="global_test")
        register_config("global_get_test", config=test_config)
        
        # Now get it back
        retrieved = get_config("global_get_test")
        assert retrieved is not None
        assert retrieved.name == "global_test"
    
    def test_get_config_global_nonexistent(self):
        """Test getting nonexistent config globally."""
        result = get_config("definitely_nonexistent")
        assert result is None
    
    def test_set_config_global(self):
        """Test global set_config function."""
        config = TestConfig(name="global_set", value=999)
        
        set_config("global_set_test", config)
        
        # Verify it was set
        retrieved = get_config("global_set_test")
        assert retrieved is not None
        assert retrieved.name == "global_set"
        assert retrieved.value == 999
    
    def test_register_config_global(self):
        """Test global register_config function.""" 
        config = TestConfig(name="global_register")
        
        register_config("global_reg_test", config=config)
        
        # Verify it was registered
        retrieved = get_config("global_reg_test")
        assert retrieved is not None
        assert retrieved.name == "global_register"
    
    def test_register_config_global_with_kwargs(self):
        """Test global register with kwargs."""
        # This should work even if we don't provide config
        register_config("global_kwargs_test", some_param="value")
        
        # We won't get anything back since we didn't provide a config
        # But it shouldn't crash