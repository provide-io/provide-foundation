#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Simplified tests for config schema to improve code coverage."""

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.config.schema import (
    ConfigSchema,
    SchemaField,
    validate_email,
    validate_path,
    validate_port,
    validate_url,
    validate_url_accessible,
    validate_version,
)


class TestSchemaFieldSimple(FoundationTestCase):
    """Test SchemaField basic functionality."""

    def test_schema_field_initialization(self) -> None:
        """Test SchemaField initialization."""
        field = SchemaField(
            name="test_field",
            field_type=str,
            required=True,
            default="default",
            description="Test field",
            choices=["a", "b"],
            min_value=1,
            max_value=10,
            pattern=r"\d+",
            sensitive=True,
        )

        assert field.name == "test_field"
        assert field.field_type is str
        assert field.required is True
        assert field.default == "default"
        assert field.description == "Test field"
        assert field.choices == ["a", "b"]
        assert field.min_value == 1
        assert field.max_value == 10
        assert field.pattern == r"\d+"
        assert field.sensitive is True

    def test_schema_field_defaults(self) -> None:
        """Test SchemaField with default values."""
        field = SchemaField(name="test_field")

        assert field.name == "test_field"
        assert field.field_type is None
        assert field.required is False
        assert field.default is None
        assert field.description is None
        assert field.choices is None
        assert field.min_value is None
        assert field.max_value is None
        assert field.pattern is None
        assert field.sensitive is False


class TestConfigSchemaSimple(FoundationTestCase):
    """Test ConfigSchema basic functionality."""

    def test_config_schema_initialization_empty(self) -> None:
        """Test ConfigSchema initialization with no fields."""
        schema = ConfigSchema()
        assert schema.fields == []
        assert schema._field_map == {}

    def test_config_schema_initialization_with_fields(self) -> None:
        """Test ConfigSchema initialization with fields."""
        fields = [
            SchemaField(name="field1", field_type=str),
            SchemaField(name="field2", field_type=int),
        ]
        schema = ConfigSchema(fields)

        assert len(schema.fields) == 2
        assert "field1" in schema._field_map
        assert "field2" in schema._field_map

    def test_config_schema_add_field(self) -> None:
        """Test ConfigSchema add_field method."""
        schema = ConfigSchema()
        field = SchemaField(name="new_field", field_type=str)

        schema.add_field(field)

        assert field in schema.fields
        assert schema._field_map["new_field"] == field

    def test_config_schema_apply_defaults_empty_data(self) -> None:
        """Test ConfigSchema apply_defaults with empty data."""
        schema = ConfigSchema(
            [
                SchemaField(name="field1", default="default_value"),
                SchemaField(name="field2", default=42),
            ],
        )

        result = schema.apply_defaults({})

        assert result == {"field1": "default_value", "field2": 42}

    def test_config_schema_apply_defaults_partial_data(self) -> None:
        """Test ConfigSchema apply_defaults with partial data."""
        schema = ConfigSchema(
            [
                SchemaField(name="field1", default="default_value"),
                SchemaField(name="field2", default=42),
            ],
        )

        data = {"field1": "custom_value"}
        result = schema.apply_defaults(data)

        assert result == {"field1": "custom_value", "field2": 42}

    def test_config_schema_apply_defaults_no_defaults(self) -> None:
        """Test ConfigSchema apply_defaults with fields having no defaults."""
        schema = ConfigSchema(
            [
                SchemaField(name="field1"),
                SchemaField(name="field2"),
            ],
        )

        data = {"field1": "value"}
        result = schema.apply_defaults(data)

        assert result == {"field1": "value"}

    def test_config_schema_apply_defaults_none_default(self) -> None:
        """Test ConfigSchema apply_defaults with None defaults."""
        schema = ConfigSchema(
            [
                SchemaField(name="field1", default=None),
                SchemaField(name="field2", default="real_default"),
            ],
        )

        result = schema.apply_defaults({})

        # None defaults are not applied
        assert result == {"field2": "real_default"}

    def test_config_schema_filter_extra_fields(self) -> None:
        """Test ConfigSchema filter_extra_fields."""
        schema = ConfigSchema(
            [
                SchemaField(name="field1"),
                SchemaField(name="field2"),
            ],
        )

        data = {"field1": "value1", "field2": "value2", "extra_field": "extra"}
        result = schema.filter_extra_fields(data)

        assert result == {"field1": "value1", "field2": "value2"}

    def test_config_schema_filter_extra_fields_empty_schema(self) -> None:
        """Test ConfigSchema filter_extra_fields with empty schema."""
        schema = ConfigSchema([])

        data = {"field1": "value1", "field2": "value2"}
        result = schema.filter_extra_fields(data)

        assert result == {}

    def test_config_schema_attr_to_schema_field_required(self) -> None:
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
        assert schema_field.field_type is str
        assert schema_field.required is True
        assert schema_field.description == "Test field"

    def test_config_schema_attr_to_schema_field_with_default(self) -> None:
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

    def test_config_schema_attr_to_schema_field_with_factory(self) -> None:
        """Test ConfigSchema _attr_to_schema_field with factory."""
        mock_attr = Mock()
        mock_attr.name = "test_field"
        mock_attr.default = None
        mock_attr.factory = list
        mock_attr.type = list
        mock_attr.metadata = {}

        schema_field = ConfigSchema._attr_to_schema_field(mock_attr)

        assert schema_field.name == "test_field"
        assert schema_field.required is False


class TestValidators(FoundationTestCase):
    """Test built-in validator functions."""

    def test_validate_port_valid_ports(self) -> None:
        """Test validate_port with valid port numbers."""
        assert validate_port(80) is True
        assert validate_port(443) is True
        assert validate_port(8080) is True
        assert validate_port(1) is True
        assert validate_port(65535) is True

    def test_validate_port_invalid_ports(self) -> None:
        """Test validate_port with invalid port numbers."""
        assert validate_port(0) is False
        assert validate_port(-1) is False
        assert validate_port(65536) is False
        assert validate_port(100000) is False

    def test_validate_url_valid_urls(self) -> None:
        """Test validate_url with valid URLs."""
        assert validate_url("http://example.com") is True
        assert validate_url("https://www.example.com") is True
        assert validate_url("ftp://ftp.example.com") is True
        assert validate_url("https://example.com/path?query=value") is True

    def test_validate_url_invalid_urls(self) -> None:
        """Test validate_url with invalid URLs."""
        assert validate_url("not-a-url") is False
        assert validate_url("http://") is False
        assert validate_url("://example.com") is False
        assert validate_url("") is False

    def test_validate_url_malformed_url_exception(self) -> None:
        """Test validate_url handles malformed URLs that raise exceptions."""
        # Test with a mock that raises exception
        with patch("urllib.parse.urlparse", side_effect=Exception):
            assert validate_url("any-url") is False

    def test_validate_email_valid_emails(self) -> None:
        """Test validate_email with valid email addresses."""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True
        assert validate_email("test+tag@example.org") is True
        assert validate_email("123@domain.net") is True

    def test_validate_email_invalid_emails(self) -> None:
        """Test validate_email with invalid email addresses."""
        assert validate_email("not-an-email") is False
        assert validate_email("@example.com") is False
        assert validate_email("test@") is False
        assert validate_email("test.example.com") is False
        assert validate_email("") is False

    def test_validate_path_valid_paths(self) -> None:
        """Test validate_path with valid paths."""
        assert validate_path("/usr/local/bin") is True
        assert validate_path("./relative/path") is True
        assert validate_path("C:\\Windows\\System32") is True
        assert validate_path("~/.config") is True

    def test_validate_path_empty_path(self) -> None:
        """Test validate_path with empty path."""
        assert validate_path("") is True  # Empty path is valid for Path()

    def test_validate_path_invalid_path_exception(self) -> None:
        """Test validate_path handles paths that raise exceptions."""
        with patch("pathlib.Path", side_effect=Exception):
            assert validate_path("any-path") is False

    def test_validate_version_valid_versions(self) -> None:
        """Test validate_version with valid semantic versions."""
        assert validate_version("1.0.0") is True
        assert validate_version("10.20.30") is True
        assert validate_version("1.0.0-alpha") is True
        assert validate_version("1.0.0-beta.1") is True
        assert validate_version("1.0.0+build.123") is True
        assert validate_version("1.0.0-alpha+build") is True

    def test_validate_version_invalid_versions(self) -> None:
        """Test validate_version with invalid versions."""
        assert validate_version("1.0") is False
        assert validate_version("v1.0.0") is False
        assert validate_version("1.0.0.0") is False
        assert validate_version("") is False
        assert validate_version("not-a-version") is False

    def test_validate_url_accessible(self) -> None:
        """Test validate_url_accessible function."""
        # Since this is just an example that delegates to validate_url
        assert validate_url_accessible("http://example.com") is True
        assert validate_url_accessible("not-a-url") is False


# 🧱🏗️🔚
