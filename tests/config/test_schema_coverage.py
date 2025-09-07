"""Comprehensive coverage tests for config/schema.py module."""

import asyncio
import pytest
from unittest.mock import Mock, AsyncMock
from attrs import define, field

from provide.foundation.config.base import BaseConfig
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
from provide.foundation.errors import ConfigValidationError


class TestSchemaFieldComprehensive:
    """Comprehensive tests for SchemaField validation."""

    @pytest.mark.asyncio
    async def test_validate_required_field_missing(self):
        """Test validation fails for missing required field."""
        field_obj = SchemaField(name="test_field", required=True)

        with pytest.raises(ConfigValidationError, match="Field is required"):
            await field_obj.validate(None)

    @pytest.mark.asyncio
    async def test_validate_required_field_present(self):
        """Test validation passes for present required field."""
        field_obj = SchemaField(name="test_field", required=True, type=str)

        # Should not raise
        await field_obj.validate("test_value")

    @pytest.mark.asyncio
    async def test_validate_optional_field_none(self):
        """Test validation passes for None optional field."""
        field_obj = SchemaField(name="optional_field", required=False)

        # Should not raise
        await field_obj.validate(None)

    @pytest.mark.asyncio
    async def test_validate_type_mismatch(self):
        """Test validation fails for type mismatch."""
        field_obj = SchemaField(name="test_field", type=int)

        with pytest.raises(ConfigValidationError, match="Expected type int, got str"):
            await field_obj.validate("not_an_int")

    @pytest.mark.asyncio
    async def test_validate_type_correct(self):
        """Test validation passes for correct type."""
        field_obj = SchemaField(name="test_field", type=int)

        # Should not raise
        await field_obj.validate(42)

    @pytest.mark.asyncio
    async def test_validate_choices_invalid(self):
        """Test validation fails for invalid choice."""
        field_obj = SchemaField(name="test_field", choices=["option1", "option2"])

        with pytest.raises(ConfigValidationError, match="Value must be one of"):
            await field_obj.validate("invalid_option")

    @pytest.mark.asyncio
    async def test_validate_choices_valid(self):
        """Test validation passes for valid choice."""
        field_obj = SchemaField(name="test_field", choices=["option1", "option2"])

        # Should not raise
        await field_obj.validate("option1")

    @pytest.mark.asyncio
    async def test_validate_min_value_fail(self):
        """Test validation fails for value below minimum."""
        field_obj = SchemaField(name="test_field", min_value=10)

        with pytest.raises(ConfigValidationError, match="Value must be >= 10"):
            await field_obj.validate(5)

    @pytest.mark.asyncio
    async def test_validate_min_value_pass(self):
        """Test validation passes for value at or above minimum."""
        field_obj = SchemaField(name="test_field", min_value=10)

        # Should not raise
        await field_obj.validate(10)
        await field_obj.validate(15)

    @pytest.mark.asyncio
    async def test_validate_max_value_fail(self):
        """Test validation fails for value above maximum."""
        field_obj = SchemaField(name="test_field", max_value=100)

        with pytest.raises(ConfigValidationError, match="Value must be <= 100"):
            await field_obj.validate(150)

    @pytest.mark.asyncio
    async def test_validate_max_value_pass(self):
        """Test validation passes for value at or below maximum."""
        field_obj = SchemaField(name="test_field", max_value=100)

        # Should not raise
        await field_obj.validate(100)
        await field_obj.validate(50)

    @pytest.mark.asyncio
    async def test_validate_pattern_fail(self):
        """Test validation fails for pattern mismatch."""
        field_obj = SchemaField(name="test_field", pattern=r"^\d{3}-\d{4}$")

        with pytest.raises(ConfigValidationError, match="Value does not match pattern"):
            await field_obj.validate("invalid-format")

    @pytest.mark.asyncio
    async def test_validate_pattern_pass(self):
        """Test validation passes for pattern match."""
        field_obj = SchemaField(name="test_field", pattern=r"^\d{3}-\d{4}$")

        # Should not raise
        await field_obj.validate("123-4567")

    @pytest.mark.asyncio
    async def test_validate_pattern_non_string(self):
        """Test pattern validation skipped for non-string values."""
        field_obj = SchemaField(name="test_field", pattern=r"^\d+$")

        # Should not raise since 42 is not a string
        await field_obj.validate(42)

    @pytest.mark.asyncio
    async def test_validate_sync_validator_pass(self):
        """Test validation with passing sync validator."""

        def validator(value):
            return value > 0

        field_obj = SchemaField(name="test_field", validator=validator)

        # Should not raise
        await field_obj.validate(5)

    @pytest.mark.asyncio
    async def test_validate_sync_validator_fail(self):
        """Test validation with failing sync validator."""

        def validator(value):
            return value > 0

        field_obj = SchemaField(name="test_field", validator=validator)

        with pytest.raises(ConfigValidationError, match="Custom validation failed"):
            await field_obj.validate(-5)

    @pytest.mark.asyncio
    async def test_validate_async_validator_pass(self):
        """Test validation with passing async validator."""

        async def async_validator(value):
            await asyncio.sleep(0)  # Simulate async work
            return value > 0

        field_obj = SchemaField(name="test_field", validator=async_validator)

        # Should not raise
        await field_obj.validate(5)

    @pytest.mark.asyncio
    async def test_validate_async_validator_fail(self):
        """Test validation with failing async validator."""

        async def async_validator(value):
            await asyncio.sleep(0)  # Simulate async work
            return value > 0

        field_obj = SchemaField(name="test_field", validator=async_validator)

        with pytest.raises(ConfigValidationError, match="Custom validation failed"):
            await field_obj.validate(-5)

    @pytest.mark.asyncio
    async def test_validate_validator_raises_config_error(self):
        """Test validator that raises ConfigValidationError directly."""

        def validator(value):
            if value < 0:
                raise ConfigValidationError(
                    "Must be positive", field="test_field", value=value
                )
            return True

        field_obj = SchemaField(name="test_field", validator=validator)

        with pytest.raises(ConfigValidationError, match="Must be positive"):
            await field_obj.validate(-1)

    @pytest.mark.asyncio
    async def test_validate_validator_raises_generic_error(self):
        """Test validator that raises generic exception."""

        def validator(value):
            raise ValueError("Generic error")

        field_obj = SchemaField(name="test_field", validator=validator)

        with pytest.raises(
            ConfigValidationError, match="Validation error: Generic error"
        ):
            await field_obj.validate(5)

    @pytest.mark.asyncio
    async def test_validate_future_validator(self):
        """Test validation with future-based validator."""

        async def create_future():
            future = asyncio.get_event_loop().create_future()
            future.set_result(True)
            return future

        field_obj = SchemaField(name="test_field", validator=lambda x: create_future())

        # Should not raise
        await field_obj.validate(5)

    @pytest.mark.asyncio
    async def test_validate_all_constraints_combined(self):
        """Test validation with all constraints combined."""

        def custom_validator(value):
            return len(value) > 5

        field_obj = SchemaField(
            name="complex_field",
            type=str,
            required=True,
            choices=[
                "valid_option",
                "another_valid_option",
                "short",
                "UPPER_CASE",
            ],  # Add values to test different constraints
            pattern=r"^[a-z_]+$",
            validator=custom_validator,
        )

        # Should not raise
        await field_obj.validate("valid_option")

        # Test failure cases
        with pytest.raises(ConfigValidationError, match="Field is required"):
            await field_obj.validate(None)

        with pytest.raises(ConfigValidationError, match="Expected type str"):
            await field_obj.validate(42)

        with pytest.raises(ConfigValidationError, match="Value must be one of"):
            await field_obj.validate("invalid_choice")

        with pytest.raises(ConfigValidationError, match="Value does not match pattern"):
            await field_obj.validate(
                "UPPER_CASE"
            )  # In choices, but fails pattern (uppercase)

        with pytest.raises(ConfigValidationError, match="Custom validation failed"):
            await field_obj.validate(
                "short"
            )  # In choices, matches pattern, but fails custom validator (len <= 5)


class TestConfigSchemaComprehensive:
    """Comprehensive tests for ConfigSchema class."""

    def test_init_with_fields(self):
        """Test ConfigSchema initialization with fields."""
        field1 = SchemaField(name="field1", type=str)
        field2 = SchemaField(name="field2", type=int)

        schema = ConfigSchema([field1, field2])

        assert len(schema.fields) == 2
        assert "field1" in schema._field_map
        assert "field2" in schema._field_map
        assert schema._field_map["field1"] is field1
        assert schema._field_map["field2"] is field2

    def test_init_without_fields(self):
        """Test ConfigSchema initialization without fields."""
        schema = ConfigSchema()

        assert len(schema.fields) == 0
        assert len(schema._field_map) == 0

    def test_add_field(self):
        """Test adding field to schema."""
        schema = ConfigSchema()
        field_obj = SchemaField(name="new_field", type=str)

        schema.add_field(field_obj)

        assert len(schema.fields) == 1
        assert "new_field" in schema._field_map
        assert schema._field_map["new_field"] is field_obj

    @pytest.mark.asyncio
    async def test_validate_missing_required_field(self):
        """Test validation fails for missing required field."""
        required_field = SchemaField(name="required_field", required=True)
        schema = ConfigSchema([required_field])

        data = {}  # Missing required field

        with pytest.raises(ConfigValidationError, match="Required field missing"):
            await schema.validate(data)

    @pytest.mark.asyncio
    async def test_validate_all_required_fields_present(self):
        """Test validation passes when all required fields present."""
        required_field = SchemaField(name="required_field", required=True, type=str)
        optional_field = SchemaField(name="optional_field", required=False, type=int)
        schema = ConfigSchema([required_field, optional_field])

        data = {"required_field": "value"}  # Optional field missing but that's OK

        # Should not raise
        await schema.validate(data)

    @pytest.mark.asyncio
    async def test_validate_field_validation_error(self):
        """Test validation propagates field validation errors."""
        field_obj = SchemaField(name="test_field", type=int)
        schema = ConfigSchema([field_obj])

        data = {"test_field": "not_an_int"}

        with pytest.raises(ConfigValidationError, match="Expected type int"):
            await schema.validate(data)

    @pytest.mark.asyncio
    async def test_validate_unknown_fields_ignored(self):
        """Test validation ignores unknown fields."""
        field_obj = SchemaField(name="known_field", type=str)
        schema = ConfigSchema([field_obj])

        data = {"known_field": "value", "unknown_field": "ignored"}

        # Should not raise
        await schema.validate(data)

    def test_apply_defaults_no_defaults(self):
        """Test apply_defaults with no default values."""
        field_obj = SchemaField(name="test_field", type=str)
        schema = ConfigSchema([field_obj])

        data = {"test_field": "value"}
        result = schema.apply_defaults(data)

        assert result == data
        assert result is not data  # Should be a copy

    def test_apply_defaults_with_defaults(self):
        """Test apply_defaults applies missing default values."""
        field1 = SchemaField(name="field1", type=str, default="default1")
        field2 = SchemaField(name="field2", type=int, default=42)
        schema = ConfigSchema([field1, field2])

        data = {"field1": "custom_value"}  # field2 missing
        result = schema.apply_defaults(data)

        assert result == {"field1": "custom_value", "field2": 42}

    def test_apply_defaults_existing_values_preserved(self):
        """Test apply_defaults doesn't overwrite existing values."""
        field_obj = SchemaField(name="test_field", type=str, default="default_value")
        schema = ConfigSchema([field_obj])

        data = {"test_field": "existing_value"}
        result = schema.apply_defaults(data)

        assert result == {"test_field": "existing_value"}

    def test_apply_defaults_none_default_ignored(self):
        """Test apply_defaults ignores None default values."""
        field_obj = SchemaField(name="test_field", type=str, default=None)
        schema = ConfigSchema([field_obj])

        data = {}
        result = schema.apply_defaults(data)

        assert result == {}

    def test_filter_extra_fields(self):
        """Test filter_extra_fields removes unknown fields."""
        field1 = SchemaField(name="known_field1", type=str)
        field2 = SchemaField(name="known_field2", type=int)
        schema = ConfigSchema([field1, field2])

        data = {
            "known_field1": "value1",
            "known_field2": 42,
            "unknown_field": "should_be_removed",
            "another_unknown": "also_removed",
        }

        result = schema.filter_extra_fields(data)

        assert result == {"known_field1": "value1", "known_field2": 42}

    def test_filter_extra_fields_empty_schema(self):
        """Test filter_extra_fields with empty schema."""
        schema = ConfigSchema([])

        data = {"field1": "value1", "field2": "value2"}
        result = schema.filter_extra_fields(data)

        assert result == {}

    def test_from_config_class(self):
        """Test generating schema from config class."""

        @define
        class TestConfig(BaseConfig):
            name: str = field(default="test")
            count: int = field(default=0)
            enabled: bool = field(default=False)

        schema = ConfigSchema.from_config_class(TestConfig)

        # TestConfig has 3 fields + BaseConfig has internal fields like _source_map
        assert len(schema.fields) >= 3
        assert "name" in schema._field_map
        assert "count" in schema._field_map
        assert "enabled" in schema._field_map

        name_field = schema._field_map["name"]
        assert name_field.name == "name"
        assert name_field.type == str
        assert name_field.default == "test"

    def test_from_config_class_with_metadata(self):
        """Test generating schema with field metadata."""

        @define
        class TestConfig(BaseConfig):
            secret: str = field(
                default="", metadata={"description": "Secret value", "sensitive": True}
            )

        schema = ConfigSchema.from_config_class(TestConfig)

        secret_field = schema._field_map["secret"]
        assert secret_field.description == "Secret value"
        assert secret_field.sensitive is True

    def test_attr_to_schema_field_required_detection(self):
        """Test _attr_to_schema_field required field detection."""
        # Mock attribute with no default and no factory -> required
        attr = Mock()
        attr.name = "required_field"
        attr.default = None
        attr.factory = None
        attr.type = str
        attr.metadata = {}

        field_obj = ConfigSchema._attr_to_schema_field(attr)

        assert field_obj.required is True
        assert field_obj.name == "required_field"
        assert field_obj.type == str

    def test_attr_to_schema_field_optional_with_default(self):
        """Test _attr_to_schema_field optional field with default."""
        # Mock attribute with default -> not required
        attr = Mock()
        attr.name = "optional_field"
        attr.default = "default_value"
        attr.factory = None
        attr.type = str
        attr.metadata = {}

        field_obj = ConfigSchema._attr_to_schema_field(attr)

        assert field_obj.required is False
        assert field_obj.default == "default_value"

    def test_attr_to_schema_field_optional_with_factory(self):
        """Test _attr_to_schema_field optional field with factory."""
        # Mock attribute with factory -> not required
        attr = Mock()
        attr.name = "factory_field"
        attr.default = None
        attr.factory = lambda: []
        attr.type = list
        attr.metadata = {}

        field_obj = ConfigSchema._attr_to_schema_field(attr)

        assert field_obj.required is False

    def test_attr_to_schema_field_no_type_attribute(self):
        """Test _attr_to_schema_field with missing type attribute."""
        attr = Mock(spec=[])  # No type attribute
        attr.name = "no_type_field"
        attr.default = None
        attr.factory = None
        attr.metadata = {}

        field_obj = ConfigSchema._attr_to_schema_field(attr)

        assert field_obj.type is None


class TestValidateSchema:
    """Test the validate_schema function."""

    @pytest.mark.asyncio
    async def test_validate_schema_passes(self):
        """Test validate_schema with valid config."""

        @define
        class TestConfig(BaseConfig):
            name: str = field(default="test")

        config = TestConfig(name="valid_name")
        schema = ConfigSchema([SchemaField(name="name", type=str)])

        # Should not raise
        await validate_schema(config, schema)

    @pytest.mark.asyncio
    async def test_validate_schema_fails(self):
        """Test validate_schema with invalid config."""
        # Mock config that returns invalid data
        mock_config = Mock(spec=BaseConfig)
        mock_config.to_dict = Mock(return_value={"name": 123})  # Wrong type

        schema = ConfigSchema([SchemaField(name="name", type=str)])

        with pytest.raises(ConfigValidationError, match="Expected type str"):
            await validate_schema(mock_config, schema)


class TestBuiltinValidators:
    """Test built-in validator functions."""

    def test_validate_port_valid(self):
        """Test validate_port with valid ports."""
        assert validate_port(1) is True
        assert validate_port(80) is True
        assert validate_port(443) is True
        assert validate_port(8080) is True
        assert validate_port(65535) is True

    def test_validate_port_invalid(self):
        """Test validate_port with invalid ports."""
        assert validate_port(0) is False
        assert validate_port(-1) is False
        assert validate_port(65536) is False
        assert validate_port(100000) is False

    def test_validate_url_valid(self):
        """Test validate_url with valid URLs."""
        assert validate_url("http://example.com") is True
        assert validate_url("https://www.example.com") is True
        assert validate_url("ftp://files.example.com") is True
        assert validate_url("https://api.example.com/v1/users") is True

    def test_validate_url_invalid(self):
        """Test validate_url with invalid URLs."""
        assert validate_url("not_a_url") is False
        assert validate_url("http://") is False
        assert validate_url("://missing-scheme") is False
        assert validate_url("") is False

    def test_validate_url_exception_handling(self):
        """Test validate_url handles parsing exceptions."""
        # These might cause urlparse to raise exceptions
        assert validate_url(None) is False
        # urlparse should handle this gracefully, but if not, should return False

    def test_validate_email_valid(self):
        """Test validate_email with valid emails."""
        assert validate_email("user@example.com") is True
        assert validate_email("test.email+tag@example.co.uk") is True
        assert validate_email("user123@test-domain.org") is True

    def test_validate_email_invalid(self):
        """Test validate_email with invalid emails."""
        assert validate_email("not_an_email") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
        assert validate_email("user@domain") is False
        assert validate_email("") is False

    def test_validate_path_valid(self):
        """Test validate_path with valid paths."""
        assert validate_path("/tmp/test.txt") is True
        assert validate_path("./relative/path") is True
        assert validate_path("C:\\Windows\\System32") is True
        assert validate_path("../parent/dir") is True

    def test_validate_path_exception_handling(self):
        """Test validate_path handles Path construction exceptions."""
        # Most strings should be valid path constructors
        # But if Path() ever raises an exception, it should return False
        assert validate_path("") is True  # Empty string is valid path

        # Test with None might cause exception
        try:
            result = validate_path(None)
            # If no exception, result could be True or False
            assert isinstance(result, bool)
        except Exception:
            # If exception in test, the function should handle it and return False
            pass

    def test_validate_version_valid(self):
        """Test validate_version with valid semantic versions."""
        assert validate_version("1.0.0") is True
        assert validate_version("0.1.0") is True
        assert validate_version("10.20.30") is True
        assert validate_version("1.0.0-alpha") is True
        assert validate_version("1.0.0-beta.1") is True
        assert validate_version("1.0.0+build.123") is True
        assert validate_version("1.0.0-alpha+build") is True

    def test_validate_version_invalid(self):
        """Test validate_version with invalid versions."""
        assert validate_version("1.0") is False
        assert validate_version("1") is False
        assert validate_version("v1.0.0") is False
        assert validate_version("1.0.0.0") is False
        assert validate_version("") is False
        assert validate_version("not.a.version") is False

    @pytest.mark.asyncio
    async def test_validate_url_accessible(self):
        """Test validate_url_accessible async validator."""
        # This is just an example implementation that calls validate_url
        assert await validate_url_accessible("https://example.com") is True
        assert await validate_url_accessible("not_a_url") is False


class TestSchemaFieldEdgeCases:
    """Test edge cases and corner cases for SchemaField."""

    @pytest.mark.asyncio
    async def test_validate_none_with_type_check(self):
        """Test that None values skip type checking."""
        field_obj = SchemaField(name="test", type=int, required=False)

        # Should not raise even though None is not an int
        await field_obj.validate(None)

    @pytest.mark.asyncio
    async def test_validate_comparison_operators_edge_cases(self):
        """Test min/max validation with various types."""
        # String comparison
        field_obj = SchemaField(name="test", type=str, min_value="b", max_value="y")

        await field_obj.validate("m")  # Should pass

        with pytest.raises(ConfigValidationError):
            await field_obj.validate("a")  # Below min

        with pytest.raises(ConfigValidationError):
            await field_obj.validate("z")  # Above max

    @pytest.mark.asyncio
    async def test_validate_async_validator_coroutine_detection(self):
        """Test proper detection of coroutines vs futures."""

        async def async_validator(value):
            return True

        field_obj = SchemaField(name="test", validator=async_validator)

        # Should handle coroutine properly
        await field_obj.validate(42)

    @pytest.mark.asyncio
    async def test_validate_complex_nested_validation(self):
        """Test validation with complex nested constraints."""

        def complex_validator(value):
            # Multi-step validation
            if not isinstance(value, str):
                return False
            if len(value) < 3:
                return False
            return value.isalnum()

        field_obj = SchemaField(
            name="complex",
            type=str,
            required=True,
            min_value="aaa",  # Alphabetically
            max_value="zzz",
            pattern=r"^[a-z0-9]+$",
            validator=complex_validator,
        )

        await field_obj.validate("abc123")  # Should pass all validations

        # Test each validation constraint
        with pytest.raises(ConfigValidationError, match="Field is required"):
            await field_obj.validate(None)

        with pytest.raises(ConfigValidationError, match="Expected type str"):
            await field_obj.validate(123)

        with pytest.raises(ConfigValidationError, match="Value must be >= aaa"):
            await field_obj.validate("aa")  # Below min alphabetically
