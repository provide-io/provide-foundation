#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for configuration schema formatters."""

from __future__ import annotations

import json

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config.bootstrap import discover_and_register_configs
from provide.foundation.config.discovery import ConsolidatedSchema, get_consolidated_schema
from provide.foundation.config.formatters import (
    HumanFormatter,
    JSONFormatter,
    MarkdownFormatter,
    SchemaFormatter,
    YAMLFormatter,
    get_formatter,
)
from provide.foundation.config.schema import ConfigSchema, SchemaField


class TestGetFormatter(FoundationTestCase):
    """Test formatter selection."""

    def test_get_formatter_human(self) -> None:
        """Test getting human formatter."""
        formatter = get_formatter("human")
        assert isinstance(formatter, HumanFormatter)

    def test_get_formatter_json(self) -> None:
        """Test getting JSON formatter."""
        formatter = get_formatter("json")
        assert isinstance(formatter, JSONFormatter)

    def test_get_formatter_yaml(self) -> None:
        """Test getting YAML formatter."""
        formatter = get_formatter("yaml")
        assert isinstance(formatter, YAMLFormatter)

    def test_get_formatter_markdown(self) -> None:
        """Test getting markdown formatter."""
        formatter = get_formatter("markdown")
        assert isinstance(formatter, MarkdownFormatter)

    def test_get_formatter_invalid(self) -> None:
        """Test getting invalid formatter raises error."""
        with pytest.raises(ValueError, match="Unknown format"):
            get_formatter("invalid_format")


class TestHumanFormatter(FoundationTestCase):
    """Test human-readable formatter."""

    def test_human_formatter_implements_interface(self) -> None:
        """Test that HumanFormatter implements SchemaFormatter."""
        formatter = HumanFormatter()
        assert isinstance(formatter, SchemaFormatter)

    def test_human_formatter_basic_output(self) -> None:
        """Test basic human formatter output."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = HumanFormatter()
        output = formatter.format(schema)

        # Should have header
        assert "FOUNDATION CONFIGURATION SCHEMA" in output
        assert "====" in output

    def test_human_formatter_shows_categories(self) -> None:
        """Test that categories are shown."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = HumanFormatter()
        output = formatter.format(schema)

        # Should have category headers
        categories = schema.get_categories()
        for category in categories:
            assert category.upper() in output

    def test_human_formatter_shows_env_vars(self) -> None:
        """Test that environment variables are shown."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = HumanFormatter()
        output = formatter.format(schema)

        # Should have some env vars
        env_vars = schema.get_all_env_vars()
        if len(env_vars) > 0:
            # Check first env var is in output
            assert env_vars[0].env_var in output

    def test_human_formatter_env_only_filter(self) -> None:
        """Test env_only filter."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = HumanFormatter()
        output = formatter.format(schema, env_only=True)

        # Should still have header
        assert "FOUNDATION CONFIGURATION SCHEMA" in output

    def test_human_formatter_category_filter(self) -> None:
        """Test category filter."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = HumanFormatter()
        output = formatter.format(schema, category="logger")

        # Should only have logger category
        assert "LOGGER CONFIGURATION" in output


class TestJSONFormatter(FoundationTestCase):
    """Test JSON formatter."""

    def test_json_formatter_implements_interface(self) -> None:
        """Test that JSONFormatter implements SchemaFormatter."""
        formatter = JSONFormatter()
        assert isinstance(formatter, SchemaFormatter)

    def test_json_formatter_valid_json(self) -> None:
        """Test that JSON formatter produces valid JSON."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = JSONFormatter()
        output = formatter.format(schema)

        # Should be valid JSON
        data = json.loads(output)
        assert isinstance(data, dict)

    def test_json_formatter_has_version(self) -> None:
        """Test that JSON output has version."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = JSONFormatter()
        output = formatter.format(schema)
        data = json.loads(output)

        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_json_formatter_has_configs(self) -> None:
        """Test that JSON output has configs."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = JSONFormatter()
        output = formatter.format(schema)
        data = json.loads(output)

        assert "configs" in data
        assert isinstance(data["configs"], dict)
        assert len(data["configs"]) > 0

    def test_json_formatter_config_structure(self) -> None:
        """Test structure of config entries."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = JSONFormatter()
        output = formatter.format(schema)
        data = json.loads(output)

        # Check first config has expected structure
        if "LoggingConfig" in data["configs"]:
            config = data["configs"]["LoggingConfig"]
            assert "module" in config
            assert "category" in config
            assert "fields" in config
            assert isinstance(config["fields"], dict)

    def test_json_formatter_field_structure(self) -> None:
        """Test structure of field entries."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = JSONFormatter()
        output = formatter.format(schema, env_only=True)
        data = json.loads(output)

        # Find a field with env var
        for _config_name, config_data in data["configs"].items():
            for _field_name, field_data in config_data["fields"].items():
                assert "type" in field_data
                assert "required" in field_data
                if "env_var" in field_data:
                    # Found an env var field
                    assert isinstance(field_data["env_var"], str)
                    return

    def test_json_formatter_env_only_filter(self) -> None:
        """Test env_only filter."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = JSONFormatter()
        output = formatter.format(schema, env_only=True)
        data = json.loads(output)

        # All fields should have env_var
        for config_data in data["configs"].values():
            for field_data in config_data["fields"].values():
                assert "env_var" in field_data

    def test_json_formatter_handles_non_serializable_defaults(self) -> None:
        """Test that non-serializable defaults are converted to strings."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = JSONFormatter()
        output = formatter.format(schema)

        # Should not raise exception
        data = json.loads(output)
        assert isinstance(data, dict)


class TestYAMLFormatter(FoundationTestCase):
    """Test YAML formatter."""

    def test_yaml_formatter_implements_interface(self) -> None:
        """Test that YAMLFormatter implements SchemaFormatter."""
        formatter = YAMLFormatter()
        assert isinstance(formatter, SchemaFormatter)

    def test_yaml_formatter_basic_output(self) -> None:
        """Test basic YAML formatter output."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = YAMLFormatter()
        output = formatter.format(schema)

        # Should have YAML header
        assert "# Foundation Configuration Schema" in output
        assert "version:" in output
        assert "configs:" in output

    def test_yaml_formatter_shows_config_names(self) -> None:
        """Test that config names are shown."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = YAMLFormatter()
        output = formatter.format(schema)

        # Should have config names
        if "LoggingConfig" in schema.schemas:
            assert "LoggingConfig:" in output

    def test_yaml_formatter_env_only_filter(self) -> None:
        """Test env_only filter."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = YAMLFormatter()
        output = formatter.format(schema, env_only=True)

        # Should still have basic structure
        assert "configs:" in output

    def test_yaml_formatter_category_filter(self) -> None:
        """Test category filter."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = YAMLFormatter()
        output = formatter.format(schema, category="logger")

        # Should only have logger configs
        assert "LoggingConfig:" in output


class TestMarkdownFormatter(FoundationTestCase):
    """Test Markdown formatter."""

    def test_markdown_formatter_implements_interface(self) -> None:
        """Test that MarkdownFormatter implements SchemaFormatter."""
        formatter = MarkdownFormatter()
        assert isinstance(formatter, SchemaFormatter)

    def test_markdown_formatter_basic_output(self) -> None:
        """Test basic Markdown formatter output."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = MarkdownFormatter()
        output = formatter.format(schema)

        # Should have markdown header
        assert "# Foundation Configuration Schema" in output
        assert "##" in output  # Category headers

    def test_markdown_formatter_has_tables(self) -> None:
        """Test that markdown has tables."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = MarkdownFormatter()
        output = formatter.format(schema)

        # Should have table markers
        assert "|" in output
        assert "---" in output

    def test_markdown_formatter_shows_categories(self) -> None:
        """Test that categories are shown."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = MarkdownFormatter()
        output = formatter.format(schema)

        # Should have category headers
        categories = schema.get_categories()
        for category in categories:
            # Look for ## Category Configuration
            assert f"## {category.capitalize()}" in output or category in output.lower()

    def test_markdown_formatter_env_only_changes_headers(self) -> None:
        """Test that env_only changes table headers."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = MarkdownFormatter()
        regular_output = formatter.format(schema, env_only=False)
        env_output = formatter.format(schema, env_only=True)

        # Regular should have "Field" header
        assert "| Field |" in regular_output or "Field" in regular_output

        # Env-only should have "Environment Variable" header
        assert "Environment Variable" in env_output or "Variable" in env_output

    def test_markdown_formatter_category_filter(self) -> None:
        """Test category filter."""
        discover_and_register_configs()
        schema = get_consolidated_schema()

        formatter = MarkdownFormatter()
        output = formatter.format(schema, category="logger")

        # Should mention logger
        assert "logger" in output.lower() or "Logger" in output


class TestFormatterSensitiveHandling(FoundationTestCase):
    """Test sensitive field handling across formatters."""

    def test_human_formatter_masks_sensitive(self) -> None:
        """Test that human formatter masks sensitive fields."""
        # Create schema with sensitive field
        field = SchemaField(
            name="password",
            field_type=str,
            required=False,
            default="secret",
            sensitive=True,
            env_var="PASSWORD",
        )
        schema = ConsolidatedSchema(
            schemas={"TestConfig": ConfigSchema(fields=[field])},
            metadata={"TestConfig": {"category": "test"}},
        )

        formatter = HumanFormatter()
        output = formatter.format(schema, show_sensitive=True)

        # Should mask the default
        assert "***SENSITIVE***" in output or "password" not in output.lower()

    def test_json_formatter_masks_sensitive(self) -> None:
        """Test that JSON formatter masks sensitive fields."""
        field = SchemaField(
            name="password",
            field_type=str,
            required=False,
            default="secret",
            sensitive=True,
            env_var="PASSWORD",
        )
        schema = ConsolidatedSchema(
            schemas={"TestConfig": ConfigSchema(fields=[field])},
            metadata={"TestConfig": {"category": "test"}},
        )

        formatter = JSONFormatter()
        output = formatter.format(schema, show_sensitive=True)
        data = json.loads(output)

        # Should have masked default
        test_config = data["configs"]["TestConfig"]
        password_field = test_config["fields"]["password"]
        assert password_field["default"] == "***SENSITIVE***"


# 🧱🏗️🔚
