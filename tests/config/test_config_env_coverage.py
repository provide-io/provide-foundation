"""Comprehensive coverage tests for config/env.py module."""

import asyncio
import os
from unittest.mock import Mock, patch, AsyncMock
import tempfile
import pytest
from attrs import define

from provide.foundation.config.base import field
from provide.foundation.config.env import (
    RuntimeConfig,
    env_field,
    get_env,
    get_env_async,
)
from provide.foundation.utils.parsing import parse_bool, parse_list, parse_dict


class TestAsyncEnvFunctions:
    """Test async environment variable functions."""
    
    @pytest.mark.asyncio
    async def test_get_env_async_existing_variable(self):
        """Test get_env_async with existing environment variable."""
        with patch.dict(os.environ, {"TEST_ASYNC_VAR": "async_value"}):
            result = await get_env_async("TEST_ASYNC_VAR")
            assert result == "async_value"
    
    @pytest.mark.asyncio
    async def test_get_env_async_missing_with_default(self):
        """Test get_env_async with missing variable and default."""
        result = await get_env_async("MISSING_ASYNC_VAR", default="default_value")
        assert result == "default_value"
    
    @pytest.mark.asyncio
    async def test_get_env_async_missing_required(self):
        """Test get_env_async with missing required variable."""
        with pytest.raises(ValueError, match="Required environment variable"):
            await get_env_async("MISSING_REQUIRED_VAR", required=True)
    
    @pytest.mark.asyncio
    async def test_get_env_async_file_secret(self):
        """Test get_env_async with file-based secret."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("secret_content\n")
            temp_file.flush()
            
            try:
                with patch.dict(os.environ, {"ASYNC_SECRET": f"file://{temp_file.name}"}):
                    # Mock aiofiles if not available
                    with patch('provide.foundation.config.env.aiofiles') as mock_aiofiles:
                        mock_file = AsyncMock()
                        mock_file.read.return_value = "secret_content\n"
                        mock_aiofiles.open.return_value.__aenter__.return_value = mock_file
                        
                        result = await get_env_async("ASYNC_SECRET")
                        assert result == "secret_content"
            finally:
                os.unlink(temp_file.name)
    
    @pytest.mark.asyncio
    async def test_get_env_async_file_secret_error(self):
        """Test get_env_async with file reading error."""
        with patch.dict(os.environ, {"ASYNC_SECRET": "file:///nonexistent/file"}):
            with patch('provide.foundation.config.env.aiofiles') as mock_aiofiles:
                mock_aiofiles.open.side_effect = FileNotFoundError("File not found")
                
                with pytest.raises(ValueError, match="Failed to read secret from file"):
                    await get_env_async("ASYNC_SECRET")
    
    @pytest.mark.asyncio
    async def test_get_env_async_no_secret_file_support(self):
        """Test get_env_async with secret_file=False."""
        with patch.dict(os.environ, {"ASYNC_VAR": "file://should_not_read"}):
            result = await get_env_async("ASYNC_VAR", secret_file=False)
            assert result == "file://should_not_read"


class TestAiofilesImportHandling:
    """Test handling of aiofiles import."""
    
    def test_aiofiles_not_available(self):
        """Test behavior when aiofiles is not available."""
        # This tests the import error handling at lines 14-15
        with patch.dict('sys.modules', {'aiofiles': None}):
            # Re-import the module to test the import error path
            import importlib
            import provide.foundation.config.env
            importlib.reload(provide.foundation.config.env)
            
            # The module should still work without aiofiles
            assert provide.foundation.config.env.aiofiles is None


class TestAsyncRuntimeConfig:
    """Test async functionality in RuntimeConfig."""
    
    @define
    class AsyncTestConfig(RuntimeConfig):
        """Test config for async operations."""
        app_name: str = env_field(default="async_app")
        port: int = env_field(default=9000, parser=int)
        debug: bool = env_field(default=False, parser=parse_bool)
        api_key: str = env_field(env_var="API_SECRET", default="")
    
    @pytest.mark.asyncio
    async def test_from_env_async_basic(self):
        """Test basic async environment loading."""
        with patch.dict(os.environ, {
            "ASYNC_APP_NAME": "test_async_app",
            "ASYNC_PORT": "8080", 
            "ASYNC_DEBUG": "true"
        }):
            config = await self.AsyncTestConfig.from_env_async(prefix="ASYNC")
            
            assert config.app_name == "test_async_app"
            assert config.port == 8080
            assert config.debug is True
    
    @pytest.mark.asyncio 
    async def test_from_env_async_with_file_secrets(self):
        """Test async environment loading with file-based secrets."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("secret_api_key\n")
            temp_file.flush()
            
            try:
                with patch.dict(os.environ, {
                    "API_SECRET": f"file://{temp_file.name}",
                    "ASYNC_APP_NAME": "secret_app"
                }):
                    # Mock aiofiles for async file reading
                    with patch('provide.foundation.config.env.aiofiles') as mock_aiofiles:
                        mock_file = AsyncMock()
                        mock_file.read.return_value = "secret_api_key\n"
                        mock_aiofiles.open.return_value.__aenter__.return_value = mock_file
                        
                        config = await self.AsyncTestConfig.from_env_async(prefix="ASYNC")
                        
                        assert config.app_name == "secret_app"
                        assert config.api_key == "secret_api_key"
            finally:
                os.unlink(temp_file.name)
    
    @pytest.mark.asyncio
    async def test_from_env_async_no_async_secrets(self):
        """Test async loading with use_async_secrets=False."""
        with patch.dict(os.environ, {"ASYNC_APP_NAME": "sync_app"}):
            config = await self.AsyncTestConfig.from_env_async(
                prefix="ASYNC", 
                use_async_secrets=False
            )
            
            assert config.app_name == "sync_app"
    
    @pytest.mark.asyncio
    async def test_from_env_async_parallel_secret_reading(self):
        """Test parallel async secret reading."""
        # Create multiple secret files
        secret_files = []
        try:
            for i in range(2):  # Reduced to 2 for simplicity
                temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
                temp_file.write(f"secret_{i}\n")
                temp_file.flush()
                temp_file.close()
                secret_files.append(temp_file.name)
            
            with patch.dict(os.environ, {
                "SECRET_1": f"file://{secret_files[0]}",
                "SECRET_2": f"file://{secret_files[1]}"
            }):
                @define
                class MultiSecretConfig(RuntimeConfig):
                    secret1: str = env_field(env_var="SECRET_1", default="")
                    secret2: str = env_field(env_var="SECRET_2", default="")
                
                # Mock aiofiles with proper async context
                with patch('provide.foundation.config.env.aiofiles') as mock_aiofiles:
                    def mock_open(path):
                        mock_file = AsyncMock()
                        # Simulate file content based on path
                        if secret_files[0] in path:
                            mock_file.read.return_value = "secret_0\n"
                        elif secret_files[1] in path:
                            mock_file.read.return_value = "secret_1\n"
                        return AsyncMock(__aenter__=AsyncMock(return_value=mock_file))
                    
                    mock_aiofiles.open.side_effect = mock_open
                    
                    config = await MultiSecretConfig.from_env_async()
                    
                    # Verify secrets were processed
                    assert config.secret1 == "secret_0"
                    assert config.secret2 == "secret_1"
        finally:
            for file_path in secret_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
    
    @pytest.mark.asyncio
    async def test_from_env_async_parser_error(self):
        """Test async loading with parser error."""
        with patch.dict(os.environ, {"ASYNC_PORT": "invalid_port"}):
            with pytest.raises(ValueError, match="Failed to parse"):
                await self.AsyncTestConfig.from_env_async(prefix="ASYNC")
    
    @pytest.mark.asyncio
    async def test_read_secret_async_without_aiofiles(self):
        """Test _read_secret_async fallback when aiofiles not available."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("fallback_secret\n")
            temp_file.flush()
            
            try:
                # Mock aiofiles as None to test fallback
                with patch('provide.foundation.config.env.aiofiles', None):
                    result = await RuntimeConfig._read_secret_async(temp_file.name)
                    assert result == "fallback_secret"
            finally:
                os.unlink(temp_file.name)
    
    @pytest.mark.asyncio
    async def test_read_secret_async_file_error(self):
        """Test _read_secret_async with file error."""
        with pytest.raises(ValueError, match="Failed to read secret from file"):
            await RuntimeConfig._read_secret_async("/nonexistent/file")


class TestEnvFieldCreation:
    """Test env_field function."""
    
    def test_env_field_with_env_var(self):
        """Test env_field with explicit env_var."""
        field_obj = env_field(env_var="CUSTOM_VAR", default="test")
        
        assert field_obj.metadata.get("env_var") == "CUSTOM_VAR"
    
    def test_env_field_with_env_prefix(self):
        """Test env_field with env_prefix."""
        field_obj = env_field(env_prefix="PREFIX", default="test")
        
        assert field_obj.metadata.get("env_prefix") == "PREFIX"
    
    def test_env_field_with_parser(self):
        """Test env_field with custom parser."""
        field_obj = env_field(parser=int, default=0)
        
        assert field_obj.metadata.get("env_parser") == int
    
    def test_env_field_with_all_options(self):
        """Test env_field with all options."""
        field_obj = env_field(
            env_var="FULL_VAR",
            env_prefix="FULL",
            parser=str.upper,
            default="test"
        )
        
        assert field_obj.metadata.get("env_var") == "FULL_VAR"
        assert field_obj.metadata.get("env_prefix") == "FULL"
        assert field_obj.metadata.get("env_parser") == str.upper


class TestRuntimeConfigAdvanced:
    """Test advanced RuntimeConfig functionality."""
    
    @define
    class AdvancedConfig(RuntimeConfig):
        """Advanced test configuration."""
        name: str = env_field(default="advanced")
        count: int = env_field(default=0)
        enabled: bool = env_field(default=False)
        tags: list[str] = env_field(factory=list, parser=parse_list)
        settings: dict[str, str] = env_field(factory=dict, parser=parse_dict)
        custom: str = env_field(env_var="SPECIAL_VAR", default="")
        prefixed: str = env_field(env_prefix="CUSTOM", default="")
    
    def test_from_env_case_sensitive(self):
        """Test from_env with case_sensitive=True."""
        with patch.dict(os.environ, {
            "name": "case_sensitive_name",  # lowercase
            "COUNT": "42"  # uppercase
        }):
            config = self.AdvancedConfig.from_env(case_sensitive=True)
            
            # Should find the exact case match
            assert config.name == "case_sensitive_name"
            # COUNT should not match count field
            assert config.count == 0  # default value
    
    def test_from_env_file_secret_sync(self):
        """Test from_env with file-based secrets (sync version)."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("sync_secret_value\n")
            temp_file.flush()
            
            try:
                with patch.dict(os.environ, {
                    "SPECIAL_VAR": f"file://{temp_file.name}"  # Use correct env var
                }):
                    config = self.AdvancedConfig.from_env()
                    assert config.custom == "sync_secret_value"
            finally:
                os.unlink(temp_file.name)
    
    def test_from_env_file_secret_error_sync(self):
        """Test from_env with file reading error (sync version)."""
        with patch.dict(os.environ, {"SPECIAL_VAR": "file:///nonexistent/file"}):
            with pytest.raises(ValueError, match="Failed to read secret from file"):
                self.AdvancedConfig.from_env()
    
    def test_from_env_parser_error_sync(self):
        """Test from_env with parser error (sync version)."""
        with patch.dict(os.environ, {"COUNT": "not_a_number"}):
            # The auto parser should handle int conversion
            with pytest.raises(ValueError):
                self.AdvancedConfig.from_env()
    
    def test_from_env_env_prefix_field(self):
        """Test from_env with field-specific env_prefix."""
        with patch.dict(os.environ, {"CUSTOM_PREFIXED": "prefixed_value"}):
            config = self.AdvancedConfig.from_env()
            assert config.prefixed == "prefixed_value"
    
    def test_auto_parse_method(self):
        """Test _auto_parse static method."""
        # Create a mock attribute
        mock_attr = Mock()
        mock_attr.type = int
        mock_attr.name = "test_field"
        
        # Test auto parsing
        result = RuntimeConfig._auto_parse(mock_attr, "42")
        assert result == 42
    
    def test_to_env_dict_comprehensive(self):
        """Test to_env_dict with comprehensive values."""
        config = self.AdvancedConfig(
            name="test_app",
            count=100,
            enabled=True,
            tags=["tag1", "tag2", "tag3"],
            settings={"key1": "val1", "key2": "val2"},
            custom="custom_val",
            prefixed="prefix_val"
        )
        
        env_dict = config.to_env_dict(prefix="TEST")
        
        assert env_dict["TEST_NAME"] == "test_app"
        assert env_dict["TEST_COUNT"] == "100"
        assert env_dict["TEST_ENABLED"] == "true"
        assert env_dict["TEST_TAGS"] == "tag1,tag2,tag3"
        assert env_dict["TEST_SETTINGS"] == "key1=val1,key2=val2"
        assert env_dict["SPECIAL_VAR"] == "custom_val"  # Uses custom env_var
        assert env_dict["CUSTOM_PREFIXED"] == "prefix_val"  # Uses custom env_prefix
    
    def test_to_env_dict_skip_none_values(self):
        """Test to_env_dict skips None values."""
        config = self.AdvancedConfig(
            name="test",
            count=None,  # This should be skipped
            enabled=False  # This should be included
        )
        
        env_dict = config.to_env_dict()
        
        assert "NAME" in env_dict
        assert "COUNT" not in env_dict  # None value skipped
        assert env_dict["ENABLED"] == "false"  # False is included
    
    def test_to_env_dict_boolean_conversion(self):
        """Test to_env_dict boolean value conversion."""
        config = self.AdvancedConfig(enabled=True)
        env_dict = config.to_env_dict()
        assert env_dict["ENABLED"] == "true"
        
        config = self.AdvancedConfig(enabled=False)  
        env_dict = config.to_env_dict()
        assert env_dict["ENABLED"] == "false"
    
    def test_to_env_dict_other_types(self):
        """Test to_env_dict with other value types."""
        @define
        class TypeTestConfig(RuntimeConfig):
            float_val: float = field(default=0.0)
            none_val: str | None = field(default=None)
            complex_val: complex = field(default=complex(1, 2))
        
        config = TypeTestConfig(
            float_val=3.14159,
            none_val=None,
            complex_val=complex(2, 3)
        )
        
        env_dict = config.to_env_dict()
        
        assert env_dict["FLOAT_VAL"] == "3.14159"
        assert "NONE_VAL" not in env_dict  # None skipped
        assert env_dict["COMPLEX_VAL"] == "(2+3j)"