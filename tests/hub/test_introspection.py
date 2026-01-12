#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for framework-agnostic parameter introspection."""

from __future__ import annotations

import inspect
from typing import Annotated

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.cli.errors import InvalidCLIHintError
from provide.foundation.hub.introspection import (
    ParameterInfo,
    extract_cli_hint,
    introspect_parameters,
)


class TestExtractCLIHint(FoundationTestCase):
    """Test extract_cli_hint function."""

    def test_extract_option_hint(self) -> None:
        """Test extraction of 'option' hint."""
        base_type, hint = extract_cli_hint(Annotated[str, "option"], "user")

        assert base_type is str
        assert hint == "option"

    def test_extract_argument_hint(self) -> None:
        """Test extraction of 'argument' hint."""
        base_type, hint = extract_cli_hint(Annotated[str, "argument"], "name")

        assert base_type is str
        assert hint == "argument"

    def test_no_annotation(self) -> None:
        """Test non-Annotated type returns None hint."""
        base_type, hint = extract_cli_hint(str, "param")

        assert base_type is str
        assert hint is None

    def test_union_type_no_hint(self) -> None:
        """Test Union type without Annotated."""
        base_type, hint = extract_cli_hint(str | None, "param")

        assert base_type == str | None
        assert hint is None

    def test_annotated_int(self) -> None:
        """Test Annotated[int, 'option']."""
        base_type, hint = extract_cli_hint(Annotated[int, "option"], "count")

        assert base_type is int
        assert hint == "option"

    def test_invalid_hint_raises_error(self) -> None:
        """Test invalid hint raises InvalidCLIHintError."""
        with pytest.raises(
            InvalidCLIHintError,
            match=r"Invalid CLI hint 'invalid' for parameter 'user'\. Must be 'option' or 'argument'\.",
        ):
            extract_cli_hint(Annotated[str, "invalid"], "user")

    def test_invalid_hint_error_attributes(self) -> None:
        """Test InvalidCLIHintError has correct attributes."""
        try:
            extract_cli_hint(Annotated[str, "bad_hint"], "param1")
        except InvalidCLIHintError as e:
            assert e.hint == "bad_hint"
            assert e.param_name == "param1"
            assert e.code == "CLI_INVALID_HINT"
        else:
            pytest.fail("Expected InvalidCLIHintError")

    def test_annotated_with_non_string_metadata(self) -> None:
        """Test Annotated with non-string metadata (no hint)."""
        base_type, hint = extract_cli_hint(Annotated[str, 123], "param")

        assert base_type is str
        assert hint is None


class TestIntrospectParameters(FoundationTestCase):
    """Test introspect_parameters function."""

    def test_simple_function(self) -> None:
        """Test introspection of simple function."""

        def greet(name: str) -> None:
            pass

        params = introspect_parameters(greet)

        assert len(params) == 1
        assert params[0].name == "name"
        assert params[0].concrete_type is str
        assert params[0].is_required is True
        assert params[0].has_default is False
        assert params[0].cli_hint is None

    def test_function_with_defaults(self) -> None:
        """Test function with default values."""

        def greet(name: str, greeting: str = "Hello") -> None:
            pass

        params = introspect_parameters(greet)

        assert len(params) == 2
        assert params[0].name == "name"
        assert params[0].is_required is True

        assert params[1].name == "greeting"
        assert params[1].is_required is False
        assert params[1].has_default is True
        assert params[1].default == "Hello"

    def test_function_with_annotated_option(self) -> None:
        """Test function with Annotated[type, 'option']."""

        def create_user(username: Annotated[str, "option"]) -> None:
            pass

        params = introspect_parameters(create_user)

        assert len(params) == 1
        assert params[0].name == "username"
        assert params[0].concrete_type is str
        assert params[0].cli_hint == "option"
        assert params[0].is_required is True

    def test_function_with_annotated_argument(self) -> None:
        """Test function with Annotated[type, 'argument']."""

        def deploy(env: Annotated[str, "argument"] = "staging") -> None:
            pass

        params = introspect_parameters(deploy)

        assert len(params) == 1
        assert params[0].name == "env"
        assert params[0].cli_hint == "argument"
        assert params[0].has_default is True
        assert params[0].default == "staging"

    def test_mixed_annotated_and_regular(self) -> None:
        """Test function with mixed Annotated and regular params."""

        def command(
            user: Annotated[str, "option"],
            action: str,
            verbose: bool = False,
        ) -> None:
            pass

        params = introspect_parameters(command)

        assert len(params) == 3
        assert params[0].name == "user"
        assert params[0].cli_hint == "option"

        assert params[1].name == "action"
        assert params[1].cli_hint is None

        assert params[2].name == "verbose"
        assert params[2].concrete_type is bool
        assert params[2].has_default is True

    def test_skips_special_parameters(self) -> None:
        """Test that self, cls, ctx are skipped."""

        def method(self, cls: type, ctx: dict, name: str) -> None:  # type: ignore[misc]
            pass

        params = introspect_parameters(method)

        assert len(params) == 1
        assert params[0].name == "name"

    def test_no_annotation_defaults_to_str(self) -> None:
        """Test parameter without annotation defaults to str."""

        def command(name) -> None:  # type: ignore[no-untyped-def]
            pass

        params = introspect_parameters(command)

        assert len(params) == 1
        assert params[0].concrete_type is str

    def test_union_type_extraction(self) -> None:
        """Test Union type is extracted correctly."""

        def command(value: str | None = None) -> None:
            pass

        params = introspect_parameters(command)

        assert len(params) == 1
        assert params[0].concrete_type is str  # extract_concrete_type handles Union

    def test_invalid_hint_propagates_error(self) -> None:
        """Test that invalid hints raise InvalidCLIHintError."""

        def bad_command(user: Annotated[str, "invalid_hint"]) -> None:
            pass

        with pytest.raises(
            InvalidCLIHintError,
            match=r"Invalid CLI hint 'invalid_hint'",
        ):
            introspect_parameters(bad_command)


class TestParameterInfo(FoundationTestCase):
    """Test ParameterInfo dataclass."""

    def test_parameter_info_immutable(self) -> None:
        """Test ParameterInfo is frozen/immutable."""
        param = ParameterInfo(
            name="test",
            type_annotation=str,
            concrete_type=str,
            default=inspect.Parameter.empty,
            has_default=False,
            is_required=True,
            cli_hint="option",
        )

        with pytest.raises(Exception):  # attrs raises FrozenInstanceError
            param.name = "changed"  # type: ignore[misc]

    def test_parameter_info_attributes(self) -> None:
        """Test ParameterInfo attributes are accessible."""
        param = ParameterInfo(
            name="username",
            type_annotation=Annotated[str, "option"],
            concrete_type=str,
            default=inspect.Parameter.empty,
            has_default=False,
            is_required=True,
            cli_hint="option",
        )

        assert param.name == "username"
        assert param.type_annotation == Annotated[str, "option"]
        assert param.concrete_type is str
        assert param.cli_hint == "option"
        assert param.is_required is True
        assert param.has_default is False


# 🧱🏗️🔚
