#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for @injectable decorator functionality.

Tests the @injectable decorator, is_injectable() helper, and validation."""

from __future__ import annotations

import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.hub import injectable, is_injectable
from provide.foundation.testmode import reset_foundation_for_testing


@pytest.fixture(autouse=True)
def reset_foundation() -> None:
    """Reset Foundation state before each test."""
    reset_foundation_for_testing()


# Test Classes for DI


class SimpleService:
    """Service without @injectable decorator."""

    def __init__(self, value: str) -> None:
        self.value = value


@injectable
class InjectableService:
    """Service with @injectable decorator."""

    def __init__(self, value: str) -> None:
        self.value = value


# Tests for @injectable decorator


class TestInjectableDecorator:
    """Tests for the @injectable decorator."""

    def test_injectable_marks_class(self) -> None:
        """Test that @injectable marks class correctly."""
        assert is_injectable(InjectableService)
        assert not is_injectable(SimpleService)

    def test_injectable_requires_type_hints(self) -> None:
        """Test that @injectable requires type hints on all parameters."""
        with pytest.raises(ValidationError) as exc_info:

            @injectable
            class NoTypeHints:
                def __init__(self, value) -> None:
                    self.value = value

        assert "untyped parameters" in str(exc_info.value).lower()
        assert "value" in str(exc_info.value)

    def test_injectable_allows_optional_params(self) -> None:
        """Test that @injectable allows parameters with defaults."""

        @injectable
        class WithDefaults:
            def __init__(self, value: str = "default") -> None:
                self.value = value

        assert is_injectable(WithDefaults)

    def test_injectable_allows_args_kwargs(self) -> None:
        """Test that @injectable allows *args and **kwargs."""

        @injectable
        class WithVarArgs:
            def __init__(self, required: str, *args: int, **kwargs: str) -> None:
                self.required = required
                self.args = args
                self.kwargs = kwargs

        assert is_injectable(WithVarArgs)

    def test_injectable_requires_init_method(self) -> None:
        """Test that @injectable requires __init__ method."""
        with pytest.raises(ValidationError) as exc_info:

            @injectable
            class NoInit:
                pass

        assert "must define its own __init__ method" in str(exc_info.value).lower()

    def test_injectable_preserves_class_behavior(self) -> None:
        """Test that @injectable doesn't modify class behavior."""

        @injectable
        class MyClass:
            def __init__(self, value: str) -> None:
                self.value = value

            def get_value(self) -> str:
                return self.value

        instance = MyClass("test")
        assert instance.value == "test"
        assert instance.get_value() == "test"

    def test_injectable_type_hint_general_exception(self) -> None:
        """Test injectable handles general exceptions from get_type_hints."""
        # Create a class that will cause get_type_hints to fail
        # We'll mock get_type_hints to raise a non-NameError exception
        from unittest.mock import patch

        from provide.foundation.hub.injection import injectable

        class TestClass:
            def __init__(self, param: str) -> None:
                pass

        with patch("provide.foundation.hub.injection.get_type_hints") as mock_get_hints:
            mock_get_hints.side_effect = TypeError("Mock error")

            with pytest.raises(ValidationError) as exc_info:
                injectable(TestClass)

            assert "Failed to get type hints" in str(exc_info.value)
            assert "Mock error" in str(exc_info.value)


# 🧱🏗️🔚
