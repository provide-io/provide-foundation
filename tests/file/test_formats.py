#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for format-specific file operations."""

from __future__ import annotations

import json
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.formats import (
    read_json,
    read_toml,
    read_yaml,
    write_json,
    write_toml,
    write_yaml,
)


class TestFileFormats(FoundationTestCase):
    """Test format-specific file operations."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    # JSON Tests

    def test_read_json(self, temp_directory: Path) -> None:
        """Test reading JSON file."""
        path = temp_directory / "test.json"
        data = {"name": "test", "value": 42, "items": [1, 2, 3]}
        path.write_text(json.dumps(data))

        result = read_json(path)
        assert result == data

    def test_read_json_missing_file(self, temp_directory: Path) -> None:
        """Test reading missing JSON file returns default."""

        path = temp_directory / "nonexistent.json"

        result = read_json(path)
        assert result is None

        default = {"default": True}
        result = read_json(path, default=default)
        assert result == default

    def test_read_json_invalid(self, temp_directory: Path) -> None:
        """Test reading invalid JSON returns default."""

        path = temp_directory / "invalid.json"
        path.write_text("not valid json {]")

        result = read_json(path)
        assert result is None

        default = {"default": True}
        result = read_json(path, default=default)
        assert result == default

    def test_read_json_empty_file(self, temp_directory: Path) -> None:
        """Test reading empty JSON file returns default."""

        path = temp_directory / "empty.json"
        path.write_text("")

        result = read_json(path)
        assert result is None

    def test_write_json(self, temp_directory: Path) -> None:
        """Test writing JSON file."""

        path = temp_directory / "test.json"
        data = {"name": "test", "value": 42, "nested": {"key": "value"}}

        write_json(path, data)

        assert path.exists()
        loaded = json.loads(path.read_text())
        assert loaded == data

    def test_write_json_pretty(self, temp_directory: Path) -> None:
        """Test writing pretty-printed JSON."""

        path = temp_directory / "test.json"
        data = {"a": 1, "b": 2}

        write_json(path, data, indent=4)

        content = path.read_text()
        assert '{\n    "a": 1' in content

    def test_write_json_compact(self, temp_directory: Path) -> None:
        """Test writing compact JSON."""

        path = temp_directory / "test.json"
        data = {"a": 1, "b": 2}

        write_json(path, data, indent=None)

        content = path.read_text()
        assert content == '{"a": 1, "b": 2}' or content == '{"a":1,"b":2}'

    def test_write_json_sorted_keys(self, temp_directory: Path) -> None:
        """Test writing JSON with sorted keys."""

        path = temp_directory / "test.json"
        data = {"z": 1, "a": 2, "m": 3}

        write_json(path, data, sort_keys=True)

        content = path.read_text()
        # Keys should appear in alphabetical order
        assert content.index('"a"') < content.index('"m"') < content.index('"z"')

    def test_write_json_unicode(self, temp_directory: Path) -> None:
        """Test writing JSON with Unicode characters."""

        path = temp_directory / "test.json"
        data = {"message": "Hello 世界 🚀"}

        write_json(path, data)

        loaded = json.loads(path.read_text())
        assert loaded == data

    def test_write_json_creates_parent_dirs(self, temp_directory: Path) -> None:
        """Test write_json creates parent directories."""

        path = temp_directory / "subdir" / "nested" / "test.json"
        data = {"test": True}

        write_json(path, data)

        assert path.exists()
        assert json.loads(path.read_text()) == data

    def test_write_json_non_atomic(self, temp_directory: Path) -> None:
        """Test non-atomic JSON write."""

        path = temp_directory / "test.json"
        data = {"test": True}

        write_json(path, data, atomic=False)

        assert path.exists()
        assert json.loads(path.read_text()) == data

    # YAML Tests

    def test_read_yaml(self, temp_directory: Path) -> None:
        """Test reading YAML file."""
        yaml = pytest.importorskip("yaml")

        path = temp_directory / "test.yaml"
        data = {"name": "test", "value": 42, "items": [1, 2, 3]}
        path.write_text(yaml.dump(data))

        result = read_yaml(path)
        assert result == data

    def test_read_yaml_missing_file(self, temp_directory: Path) -> None:
        """Test reading missing YAML file returns default."""
        pytest.importorskip("yaml")
        path = temp_directory / "nonexistent.yaml"

        result = read_yaml(path)
        assert result is None

        default = {"default": True}
        result = read_yaml(path, default=default)
        assert result == default

    def test_read_yaml_invalid(self, temp_directory: Path) -> None:
        """Test reading invalid YAML returns default."""
        pytest.importorskip("yaml")
        path = temp_directory / "invalid.yaml"
        path.write_text("@invalid: [yaml content")

        result = read_yaml(path)
        assert result is None

    def test_write_yaml(self, temp_directory: Path) -> None:
        """Test writing YAML file."""
        yaml = pytest.importorskip("yaml")
        path = temp_directory / "test.yaml"
        data = {"name": "test", "value": 42, "nested": {"key": "value"}}

        write_yaml(path, data)

        assert path.exists()
        loaded = yaml.safe_load(path.read_text())
        assert loaded == data

    def test_write_yaml_flow_style(self, temp_directory: Path) -> None:
        """Test writing YAML in flow style."""
        pytest.importorskip("yaml")
        path = temp_directory / "test.yaml"
        data = {"a": [1, 2, 3]}

        write_yaml(path, data, default_flow_style=True)

        content = path.read_text()
        assert "{a: [1, 2, 3]}" in content

    def test_write_yaml_unicode(self, temp_directory: Path) -> None:
        """Test writing YAML with Unicode."""
        yaml = pytest.importorskip("yaml")
        path = temp_directory / "test.yaml"
        data = {"message": "Hello 世界 🚀"}

        write_yaml(path, data)

        loaded = yaml.safe_load(path.read_text())
        assert loaded == data

    # TOML Tests

    def test_read_toml(self, temp_directory: Path) -> None:
        """Test reading TOML file."""

        path = temp_directory / "test.toml"
        toml_content = """
        [package]
        name = "test"
        version = "1.0.0"

[dependencies]
foo = "1.2.3"
"""
        path.write_text(toml_content)

        result = read_toml(path)
        assert result["package"]["name"] == "test"
        assert result["dependencies"]["foo"] == "1.2.3"

    def test_read_toml_missing_file(self, temp_directory: Path) -> None:
        """Test reading missing TOML file returns default."""

        path = temp_directory / "nonexistent.toml"

        result = read_toml(path)
        assert result == {}

        default = {"default": True}
        result = read_toml(path, default=default)
        assert result == default

    def test_read_toml_invalid(self, temp_directory: Path) -> None:
        """Test reading invalid TOML returns default."""

        path = temp_directory / "invalid.toml"
        path.write_text("[invalid toml content")

        result = read_toml(path)
        assert result == {}

    def test_read_toml_empty_file(self, temp_directory: Path) -> None:
        """Test reading empty TOML file."""

        path = temp_directory / "empty.toml"
        path.write_text("")

        result = read_toml(path)
        assert result == {}

    def test_write_toml(self, temp_directory: Path) -> None:
        """Test writing TOML file."""
        pytest.importorskip("tomli_w")
        import tomllib

        path = temp_directory / "test.toml"
        data = {
            "package": {"name": "test", "version": "1.0.0"},
            "dependencies": {"foo": "1.2.3"},
        }

        write_toml(path, data)

        assert path.exists()
        loaded = tomllib.loads(path.read_text())
        assert loaded == data

    def test_write_toml_creates_parent_dirs(self, temp_directory: Path) -> None:
        """Test write_toml creates parent directories."""
        pytest.importorskip("tomli_w")
        path = temp_directory / "subdir" / "nested" / "test.toml"
        data = {"test": {"value": True}}

        write_toml(path, data)

        assert path.exists()

    def test_write_toml_non_atomic(self, temp_directory: Path) -> None:
        """Test non-atomic TOML write."""
        pytest.importorskip("tomli_w")
        path = temp_directory / "test.toml"
        data = {"test": True}

        write_toml(path, data, atomic=False)

        assert path.exists()


# 🧱🏗️🔚
