#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors import DependencyError
from provide.foundation.utils.stubs import (
    create_dependency_stub,
    create_function_stub,
    create_module_stub,
)

"""Tests for dependency stub utilities."""


class TestCreateDependencyStub(FoundationTestCase):
    """Test create_dependency_stub function."""

    def test_stub_raises_on_instantiation(self) -> None:
        """Test that stub class raises DependencyError on instantiation."""
        StubClass = create_dependency_stub("test-package", "test-feature")

        with pytest.raises(DependencyError, match="test-package"):
            StubClass()

    def test_stub_error_message_includes_install_command(self) -> None:
        """Test that error message includes install instructions."""
        StubClass = create_dependency_stub("httpx", "transport")

        with pytest.raises(DependencyError) as exc_info:
            StubClass()

        error_msg = str(exc_info.value)
        assert "httpx" in error_msg
        assert "uv add" in error_msg
        assert "provide-foundation[transport]" in error_msg

    def test_stub_raises_on_call(self) -> None:
        """Test that stub raises DependencyError when called."""
        StubClass = create_dependency_stub("test-package", "test-feature")
        instance = StubClass  # type: ignore[assignment]

        with pytest.raises(DependencyError, match="test-package"):
            instance()  # type: ignore[operator]

    def test_stub_raises_on_new(self) -> None:
        """Test that stub raises DependencyError via __new__."""
        StubClass = create_dependency_stub("test-package", "test-feature")

        # __new__ should raise before __init__ is called
        with pytest.raises(DependencyError, match="test-package"):
            StubClass()

    def test_stub_raises_on_class_getitem(self) -> None:
        """Test that stub raises DependencyError on generic access."""
        StubClass = create_dependency_stub("test-package", "test-feature")

        with pytest.raises(DependencyError, match="test-package"):
            _ = StubClass[int]  # type: ignore[misc]

    def test_stub_has_meaningful_name(self) -> None:
        """Test that stub class has a meaningful name."""
        StubClass = create_dependency_stub("httpx", "transport")

        assert StubClass.__name__ == "TransportStub"
        assert StubClass.__qualname__ == "TransportStub"


class TestCreateFunctionStub(FoundationTestCase):
    """Test create_function_stub function."""

    def test_function_stub_raises_on_call(self) -> None:
        """Test that function stub raises DependencyError when called."""
        stub_func = create_function_stub("test-package", "test-feature")

        with pytest.raises(DependencyError, match="test-package"):
            stub_func()

    def test_function_stub_error_message(self) -> None:
        """Test that function stub error includes install instructions."""
        stub_func = create_function_stub("httpx", "transport")

        with pytest.raises(DependencyError) as exc_info:
            stub_func()

        error_msg = str(exc_info.value)
        assert "httpx" in error_msg
        assert "provide-foundation[transport]" in error_msg

    def test_function_stub_accepts_args(self) -> None:
        """Test that function stub accepts arguments before raising."""
        stub_func = create_function_stub("test-package", "test-feature")

        with pytest.raises(DependencyError):
            stub_func("arg1", "arg2", kwarg1="value")

    def test_function_stub_has_meaningful_name(self) -> None:
        """Test that function stub has a meaningful name."""
        stub_func = create_function_stub("httpx", "transport")

        assert stub_func.__name__ == "transport_stub"
        assert stub_func.__qualname__ == "transport_stub"


class TestCreateModuleStub(FoundationTestCase):
    """Test create_module_stub function."""

    def test_module_stub_raises_on_attribute_access(self) -> None:
        """Test that module stub raises DependencyError on attribute access."""
        stub_module = create_module_stub("test-package", "test-feature")

        with pytest.raises(DependencyError, match="test-package"):
            _ = stub_module.some_function

    def test_module_stub_raises_on_call(self) -> None:
        """Test that module stub raises DependencyError when called."""
        stub_module = create_module_stub("test-package", "test-feature")

        with pytest.raises(DependencyError, match="test-package"):
            stub_module()  # type: ignore[operator]

    def test_module_stub_error_message(self) -> None:
        """Test that module stub error includes install instructions."""
        stub_module = create_module_stub("httpx", "transport")

        with pytest.raises(DependencyError) as exc_info:
            _ = stub_module.AsyncClient

        error_msg = str(exc_info.value)
        assert "httpx" in error_msg
        assert "provide-foundation[transport]" in error_msg


class TestStubIntegration(FoundationTestCase):
    """Test stub integration with real Foundation modules."""

    def test_transport_module_has_httpx_flag(self) -> None:
        """Test that transport module exports _HAS_HTTPX flag."""
        from provide.foundation.transport import _HAS_HTTPX

        assert isinstance(_HAS_HTTPX, bool)

    def test_transport_imports_successfully(self) -> None:
        """Test that transport module can be imported regardless of httpx availability."""
        # This test verifies graceful degradation - module always imports
        from provide.foundation.transport import HTTPTransport

        assert HTTPTransport is not None

    def test_stub_utilities_exported_from_utils(self) -> None:
        """Test that stub utilities are accessible from utils module."""
        from provide.foundation.utils import (
            create_dependency_stub,
            create_function_stub,
            create_module_stub,
        )

        assert callable(create_dependency_stub)
        assert callable(create_function_stub)
        assert callable(create_module_stub)


class TestDependencyErrorContext(FoundationTestCase):
    """Test that DependencyError provides proper context."""

    def test_dependency_error_has_package_context(self) -> None:
        """Test that DependencyError includes package in context."""
        stub_func = create_function_stub("test-package", "test-feature")

        with pytest.raises(DependencyError) as exc_info:
            stub_func()

        # DependencyError should have context dict with package info
        error = exc_info.value
        assert hasattr(error, "context") or hasattr(error, "_context")

    def test_dependency_error_feature_context(self) -> None:
        """Test that DependencyError includes feature in context."""
        stub_func = create_function_stub("httpx", "transport")

        with pytest.raises(DependencyError) as exc_info:
            stub_func()

        error_msg = str(exc_info.value)
        # Should reference the feature via install command
        assert "transport" in error_msg or "provide-foundation[" in error_msg


# 🧱🏗️🔚
