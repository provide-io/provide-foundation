"""Comprehensive tests for config schema to improve code coverage."""

import asyncio
from unittest.mock import Mock, AsyncMock, patch
import pytest

from attrs import define, field

from provide.foundation.config.schema import (
    SchemaField,
    ConfigSchema,
    validate_schema,
    validate_port,
    validate_url,
    validate_email,
    validate_path,
    validate_version,
    validate_url_accessible,
)
from provide.foundation.config.base import BaseConfig
from provide.foundation.errors import ConfigValidationError


class TestSchemaField:
    """Test SchemaField functionality."""

    @pytest.mark.asyncio
    async def test_schema_field_required_validation_missing(self):
        """Test SchemaField validation with required field missing."""
        field = SchemaField(name="test_field", required=True)
        
        with pytest.raises(ConfigValidationError, match="Field is required"):
            await field.validate(None)

    @pytest.mark.asyncio
    async def test_schema_field_required_validation_present(self):
        """Test SchemaField validation with required field present."""
        field = SchemaField(name="test_field", required=True, type=str)
        
        # Should not raise
        await field.validate("test_value")

    @pytest.mark.asyncio
    async def test_schema_field_optional_none_value(self):
        """Test SchemaField validation with optional field as None."""
        field = SchemaField(name="test_field", required=False, type=str)
        
        # Should not raise for None when not required
        await field.validate(None)

    @pytest.mark.asyncio
    async def test_schema_field_type_validation_correct(self):
        """Test SchemaField type validation with correct type."""
        field = SchemaField(name="test_field", type=str)
        
        await field.validate("test_string")

    @pytest.mark.asyncio
    async def test_schema_field_type_validation_incorrect(self):
        """Test SchemaField type validation with incorrect type."""
        field = SchemaField(name="test_field", type=str)
        
        with pytest.raises(ConfigValidationError, match="Expected type str, got int"):
            await field.validate(42)

    @pytest.mark.asyncio
    async def test_schema_field_choices_validation_valid(self):
        """Test SchemaField choices validation with valid choice."""
        field = SchemaField(name="test_field", choices=["a", "b", "c"])
        
        await field.validate("b")

    @pytest.mark.asyncio
    async def test_schema_field_choices_validation_invalid(self):
        """Test SchemaField choices validation with invalid choice."""
        field = SchemaField(name="test_field", choices=["a", "b", "c"])
        
        with pytest.raises(ConfigValidationError, match="Value must be one of"):
            await field.validate("d")

    @pytest.mark.asyncio
    async def test_schema_field_min_value_validation_valid(self):
        """Test SchemaField min_value validation with valid value."""
        field = SchemaField(name="test_field", min_value=10)
        
        await field.validate(15)

    @pytest.mark.asyncio
    async def test_schema_field_min_value_validation_invalid(self):
        """Test SchemaField min_value validation with invalid value."""
        field = SchemaField(name="test_field", min_value=10)
        
        with pytest.raises(ConfigValidationError, match="Value must be >= 10"):
            await field.validate(5)

    @pytest.mark.asyncio
    async def test_schema_field_max_value_validation_valid(self):
        """Test SchemaField max_value validation with valid value."""
        field = SchemaField(name="test_field", max_value=100)
        
        await field.validate(50)

    @pytest.mark.asyncio
    async def test_schema_field_max_value_validation_invalid(self):
        """Test SchemaField max_value validation with invalid value."""
        field = SchemaField(name="test_field", max_value=100)
        
        with pytest.raises(ConfigValidationError, match="Value must be <= 100"):
            await field.validate(150)

    @pytest.mark.asyncio
    async def test_schema_field_pattern_validation_valid(self):
        """Test SchemaField pattern validation with valid pattern."""
        field = SchemaField(name="test_field", pattern=r"^\d{3}-\d{3}-\d{4}$")
        
        await field.validate("123-456-7890")

    @pytest.mark.asyncio
    async def test_schema_field_pattern_validation_invalid(self):
        """Test SchemaField pattern validation with invalid pattern."""
        field = SchemaField(name="test_field", pattern=r"^\d{3}-\d{3}-\d{4}$")
        
        with pytest.raises(ConfigValidationError, match="Value does not match pattern"):
            await field.validate("invalid-phone")

    @pytest.mark.asyncio
    async def test_schema_field_pattern_validation_non_string(self):
        """Test SchemaField pattern validation skips non-string values."""
        field = SchemaField(name="test_field", pattern=r"^\d+$")
        
        # Should not raise for non-string values
        await field.validate(42)

    @pytest.mark.asyncio
    async def test_schema_field_sync_custom_validator_valid(self):
        """Test SchemaField with sync custom validator - valid."""
        def custom_validator(value):
            return value > 0
        
        field = SchemaField(name="test_field", validator=custom_validator)
        
        await field.validate(5)

    @pytest.mark.asyncio
    async def test_schema_field_sync_custom_validator_invalid(self):
        """Test SchemaField with sync custom validator - invalid."""
        def custom_validator(value):
            return value > 0
        
        field = SchemaField(name="test_field", validator=custom_validator)
        
        with pytest.raises(ConfigValidationError, match="Custom validation failed"):
            await field.validate(-5)

    @pytest.mark.asyncio
    async def test_schema_field_async_custom_validator_valid(self):
        """Test SchemaField with async custom validator - valid."""
        async def async_validator(value):
            return value > 0
        
        field = SchemaField(name="test_field", validator=async_validator)
        
        await field.validate(5)

    @pytest.mark.asyncio
    async def test_schema_field_async_custom_validator_invalid(self):
        """Test SchemaField with async custom validator - invalid."""
        async def async_validator(value):
            return value > 0
        
        field = SchemaField(name="test_field", validator=async_validator)
        
        with pytest.raises(ConfigValidationError, match="Custom validation failed"):
            await field.validate(-5)

    @pytest.mark.asyncio
    async def test_schema_field_custom_validator_exception(self):
        """Test SchemaField custom validator that raises exception."""
        def failing_validator(value):
            raise ValueError("Custom error")
        
        field = SchemaField(name="test_field", validator=failing_validator)
        
        with pytest.raises(ConfigValidationError, match="Validation error: Custom error"):
            await field.validate(5)

    @pytest.mark.asyncio
    async def test_schema_field_custom_validator_config_validation_error(self):
        """Test SchemaField custom validator that raises ConfigValidationError."""
        def validator_raising_config_error(value):
            raise ConfigValidationError("test_field", value, "Custom config error")
        
        field = SchemaField(name="test_field", validator=validator_raising_config_error)
        
        with pytest.raises(ConfigValidationError, match="Custom config error"):
            await field.validate(5)


class TestConfigSchema:
    """Test ConfigSchema functionality."""

    def test_config_schema_initialization_empty(self):
        """Test ConfigSchema initialization with no fields."""
        schema = ConfigSchema()
        assert schema.fields == []
        assert schema._field_map == {}

    def test_config_schema_initialization_with_fields(self):
        """Test ConfigSchema initialization with fields."""
        fields = [
            SchemaField(name="field1", type=str),
            SchemaField(name="field2", type=int),
        ]
        schema = ConfigSchema(fields)
        
        assert len(schema.fields) == 2
        assert "field1" in schema._field_map
        assert "field2" in schema._field_map

    def test_config_schema_add_field(self):
        """Test ConfigSchema add_field method."""
        schema = ConfigSchema()
        field = SchemaField(name="new_field", type=str)
        
        schema.add_field(field)
        
        assert field in schema.fields
        assert schema._field_map["new_field"] == field

    @pytest.mark.asyncio
    async def test_config_schema_validate_missing_required_field(self):
        """Test ConfigSchema validate with missing required field."""
        schema = ConfigSchema([
            SchemaField(name="required_field", required=True),
        ])
        
        data = {"other_field": "value"}
        
        with pytest.raises(ConfigValidationError, match="Required field missing"):
            await schema.validate(data)

    @pytest.mark.asyncio
    async def test_config_schema_validate_all_fields_present(self):
        """Test ConfigSchema validate with all fields present."""
        schema = ConfigSchema([
            SchemaField(name="field1", type=str, required=True),
            SchemaField(name="field2", type=int),
        ])
        
        data = {"field1": "value", "field2": 42}
        
        # Should not raise
        await schema.validate(data)

    @pytest.mark.asyncio
    async def test_config_schema_validate_extra_fields_ignored(self):
        """Test ConfigSchema validate ignores extra fields in data."""
        schema = ConfigSchema([
            SchemaField(name="field1", type=str, required=True),
        ])
        
        data = {"field1": "value", "extra_field": "extra"}
        
        # Should not raise - extra fields are ignored during validation
        await schema.validate(data)

    @pytest.mark.asyncio
    async def test_config_schema_validate_field_validation_called(self):
        """Test ConfigSchema validate calls field validation."""
        mock_field = Mock()
        mock_field.required = False
        mock_field.name = "test_field"
        mock_field.validate = AsyncMock()
        
        schema = ConfigSchema([mock_field])
        data = {"test_field": "value"}
        
        await schema.validate(data)
        
        mock_field.validate.assert_called_once_with("value")

    def test_config_schema_apply_defaults_empty_data(self):
        """Test ConfigSchema apply_defaults with empty data."""
        schema = ConfigSchema([
            SchemaField(name="field1", default="default_value"),
            SchemaField(name="field2", default=42),
        ])
        
        result = schema.apply_defaults({})
        
        assert result == {"field1": "default_value", "field2": 42}

    def test_config_schema_apply_defaults_partial_data(self):
        """Test ConfigSchema apply_defaults with partial data."""
        schema = ConfigSchema([
            SchemaField(name="field1", default="default_value"),
            SchemaField(name="field2", default=42),
        ])
        
        data = {"field1": "custom_value"}
        result = schema.apply_defaults(data)
        
        assert result == {"field1": "custom_value", "field2": 42}

    def test_config_schema_apply_defaults_no_defaults(self):
        """Test ConfigSchema apply_defaults with fields having no defaults."""
        schema = ConfigSchema([
            SchemaField(name="field1"),
            SchemaField(name="field2"),
        ])
        
        data = {"field1": "value"}
        result = schema.apply_defaults(data)
        
        assert result == {"field1": "value"}

    def test_config_schema_apply_defaults_none_default(self):
        """Test ConfigSchema apply_defaults with None defaults."""
        schema = ConfigSchema([
            SchemaField(name="field1", default=None),
            SchemaField(name="field2", default="real_default"),
        ])
        
        result = schema.apply_defaults({})
        
        # None defaults are not applied
        assert result == {"field2": "real_default"}

    def test_config_schema_filter_extra_fields(self):
        """Test ConfigSchema filter_extra_fields."""
        schema = ConfigSchema([
            SchemaField(name="field1"),
            SchemaField(name="field2"),
        ])
        
        data = {"field1": "value1", "field2": "value2", "extra_field": "extra"}
        result = schema.filter_extra_fields(data)
        
        assert result == {"field1": "value1", "field2": "value2"}

    def test_config_schema_filter_extra_fields_empty_schema(self):
        """Test ConfigSchema filter_extra_fields with empty schema."""
        schema = ConfigSchema([])
        
        data = {"field1": "value1", "field2": "value2"}
        result = schema.filter_extra_fields(data)
        
        assert result == {}

    def test_config_schema_from_config_class(self):
        """Test ConfigSchema from_config_class."""
        @define
        class TestConfig(BaseConfig):
            field1: str = field(metadata={"description": "First field"})
            field2: int = field(default=42)
            sensitive_field: str = field(metadata={"sensitive": True})
        
        schema = ConfigSchema.from_config_class(TestConfig)
        
        assert len(schema.fields) == 3
        assert any(f.name == "field1" for f in schema.fields)
        assert any(f.name == "field2" for f in schema.fields)
        assert any(f.name == "sensitive_field" for f in schema.fields)

    def test_config_schema_attr_to_schema_field_required(self):
        """Test ConfigSchema _attr_to_schema_field with required field."""
        # Mock attrs attribute
        mock_attr = Mock()
        mock_attr.name = "test_field"
        mock_attr.default = None
        mock_attr.factory = None
        mock_attr.type = str
        mock_attr.metadata = {"description": "Test field"}
        
        schema_field = ConfigSchema._attr_to_schema_field(mock_attr)
        
        assert schema_field.name == "test_field"
        assert schema_field.type == str
        assert schema_field.required is True
        assert schema_field.description == "Test field"

    def test_config_schema_attr_to_schema_field_with_default(self):
        """Test ConfigSchema _attr_to_schema_field with default value."""
        mock_attr = Mock()
        mock_attr.name = "test_field"
        mock_attr.default = "default_value"
        mock_attr.factory = None
        mock_attr.type = str
        mock_attr.metadata = {"sensitive": True}
        
        schema_field = ConfigSchema._attr_to_schema_field(mock_attr)
        
        assert schema_field.name == "test_field"
        assert schema_field.required is False
        assert schema_field.default == "default_value"
        assert schema_field.sensitive is True

    def test_config_schema_attr_to_schema_field_with_factory(self):
        """Test ConfigSchema _attr_to_schema_field with factory."""
        mock_attr = Mock()
        mock_attr.name = "test_field"
        mock_attr.default = None
        mock_attr.factory = lambda: []
        mock_attr.type = list
        mock_attr.metadata = {}
        
        schema_field = ConfigSchema._attr_to_schema_field(mock_attr)
        
        assert schema_field.name == "test_field"
        assert schema_field.required is False


@pytest.mark.asyncio
async def test_validate_schema_function():
    """Test validate_schema function."""
    @define
    class TestConfig(BaseConfig):
        field1: str
    
    config = TestConfig(field1="value")
    schema = ConfigSchema([
        SchemaField(name="field1", type=str, required=True),
    ])
    
    # Mock the to_dict method
    with patch.object(config, 'to_dict', new_callable=AsyncMock) as mock_to_dict:
        mock_to_dict.return_value = {"field1": "value"}
        
        # Should not raise
        await validate_schema(config, schema)
        
        mock_to_dict.assert_called_once_with(include_sensitive=True)


class TestValidators:
    """Test built-in validator functions."""

    def test_validate_port_valid_ports(self):
        """Test validate_port with valid port numbers."""
        assert validate_port(80) is True
        assert validate_port(443) is True
        assert validate_port(8080) is True
        assert validate_port(1) is True
        assert validate_port(65535) is True

    def test_validate_port_invalid_ports(self):
        """Test validate_port with invalid port numbers."""
        assert validate_port(0) is False
        assert validate_port(-1) is False
        assert validate_port(65536) is False
        assert validate_port(100000) is False

    def test_validate_url_valid_urls(self):
        """Test validate_url with valid URLs."""
        assert validate_url("http://example.com") is True
        assert validate_url("https://www.example.com") is True
        assert validate_url("ftp://ftp.example.com") is True
        assert validate_url("https://example.com/path?query=value") is True

    def test_validate_url_invalid_urls(self):
        """Test validate_url with invalid URLs."""
        assert validate_url("not-a-url") is False
        assert validate_url("http://") is False
        assert validate_url("://example.com") is False
        assert validate_url("") is False

    def test_validate_url_malformed_url_exception(self):
        """Test validate_url handles malformed URLs that raise exceptions."""
        # Test with a mock that raises exception
        with patch('urllib.parse.urlparse', side_effect=Exception):
            assert validate_url("any-url") is False

    def test_validate_email_valid_emails(self):
        """Test validate_email with valid email addresses."""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True
        assert validate_email("test+tag@example.org") is True
        assert validate_email("123@domain.net") is True

    def test_validate_email_invalid_emails(self):
        """Test validate_email with invalid email addresses."""
        assert validate_email("not-an-email") is False
        assert validate_email("@example.com") is False
        assert validate_email("test@") is False
        assert validate_email("test.example.com") is False
        assert validate_email("") is False

    def test_validate_path_valid_paths(self):
        """Test validate_path with valid paths."""
        assert validate_path("/usr/local/bin") is True
        assert validate_path("./relative/path") is True
        assert validate_path("C:\\Windows\\System32") is True
        assert validate_path("~/.config") is True

    def test_validate_path_empty_path(self):
        """Test validate_path with empty path."""
        assert validate_path("") is True  # Empty path is valid for Path()

    def test_validate_path_invalid_path_exception(self):
        """Test validate_path handles paths that raise exceptions."""
        with patch('pathlib.Path', side_effect=Exception):
            assert validate_path("any-path") is False

    def test_validate_version_valid_versions(self):
        """Test validate_version with valid semantic versions."""
        assert validate_version("1.0.0") is True
        assert validate_version("10.20.30") is True
        assert validate_version("1.0.0-alpha") is True
        assert validate_version("1.0.0-beta.1") is True
        assert validate_version("1.0.0+build.123") is True
        assert validate_version("1.0.0-alpha+build") is True

    def test_validate_version_invalid_versions(self):
        """Test validate_version with invalid versions."""
        assert validate_version("1.0") is False
        assert validate_version("v1.0.0") is False
        assert validate_version("1.0.0.0") is False
        assert validate_version("") is False
        assert validate_version("not-a-version") is False

    @pytest.mark.asyncio
    async def test_validate_url_accessible(self):
        """Test validate_url_accessible function."""
        # Since this is just an example that delegates to validate_url
        assert await validate_url_accessible("http://example.com") is True
        assert await validate_url_accessible("not-a-url") is False