#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for dependency-related exceptions."""

from __future__ import annotations

from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.base import FoundationError
from provide.foundation.errors.dependencies import DependencyError, DependencyMismatchError


class TestDependencyError(FoundationTestCase):
    """Test cases for DependencyError."""

    def test_dependency_error_inheritance(self) -> None:
        """Test that DependencyError inherits from FoundationError."""
        assert issubclass(DependencyError, FoundationError)

    def test_dependency_error_basic_creation(self) -> None:
        """Test basic DependencyError creation."""
        error = DependencyError("cryptography")

        assert error.code == "DEPENDENCY_MISSING"
        assert "cryptography" in str(error)
        assert "uv add cryptography" in str(error)
        assert error.context["dependency.package"] == "cryptography"
        assert error.context["dependency.install_command"] == "uv add cryptography"

    def test_dependency_error_with_feature(self) -> None:
        """Test DependencyError with feature parameter."""
        error = DependencyError("cryptography", feature="crypto")

        assert error.code == "DEPENDENCY_MISSING"
        assert "cryptography" in str(error)
        assert "uv add 'provide-foundation[crypto]'" in str(error)
        assert error.context["dependency.package"] == "cryptography"
        assert error.context["dependency.feature"] == "crypto"
        assert error.context["dependency.install_command"] == "uv add 'provide-foundation[crypto]'"

    def test_dependency_error_with_custom_install_command(self) -> None:
        """Test DependencyError with custom install command."""
        custom_cmd = "conda install cryptography"
        error = DependencyError("cryptography", install_command=custom_cmd)

        assert error.code == "DEPENDENCY_MISSING"
        assert "cryptography" in str(error)
        assert custom_cmd in str(error)
        assert error.context["dependency.package"] == "cryptography"
        assert error.context["dependency.install_command"] == custom_cmd

    def test_dependency_error_with_additional_context(self) -> None:
        """Test DependencyError with additional context."""
        error = DependencyError("cryptography", feature="crypto", custom_field="test_value", another_field=42)

        assert error.context["dependency.package"] == "cryptography"
        assert error.context["dependency.feature"] == "crypto"
        assert error.context["custom_field"] == "test_value"
        assert error.context["another_field"] == 42

    def test_dependency_error_to_dict(self) -> None:
        """Test DependencyError serialization to dict."""
        error = DependencyError("cryptography", feature="crypto")
        error_dict = error.to_dict()

        assert error_dict["error.type"] == "DependencyError"
        assert error_dict["error.code"] == "DEPENDENCY_MISSING"
        assert "cryptography" in error_dict["error.message"]
        assert error_dict["dependency.package"] == "cryptography"
        assert error_dict["dependency.feature"] == "crypto"

    def test_dependency_error_feature_priority_over_custom_command(self) -> None:
        """Test that feature parameter takes priority over custom install command."""
        error = DependencyError("cryptography", feature="crypto", install_command="uv add cryptography")

        # Feature should override custom install command
        assert "uv add 'provide-foundation[crypto]'" in str(error)
        assert error.context["dependency.install_command"] == "uv add 'provide-foundation[crypto]'"

    def test_dependency_error_with_cause(self) -> None:
        """Test DependencyError with an underlying cause."""
        cause = ImportError("No module named 'cryptography'")
        error = DependencyError("cryptography", cause=cause)

        assert error.cause is cause
        assert error.__cause__ is cause

        error_dict = error.to_dict()
        assert "No module named 'cryptography'" in error_dict["error.cause"]
        assert error_dict["error.cause_type"] == "ImportError"


class TestDependencyMismatchError(FoundationTestCase):
    """Test cases for DependencyMismatchError."""

    def test_dependency_mismatch_error_inheritance(self) -> None:
        """Test that DependencyMismatchError inherits from FoundationError."""
        assert issubclass(DependencyMismatchError, FoundationError)

    def test_dependency_mismatch_error_basic_creation(self) -> None:
        """Test basic DependencyMismatchError creation."""
        error = DependencyMismatchError("cryptography", required_version=">=3.0.0", current_version="2.9.2")

        assert error.code == "DEPENDENCY_VERSION_MISMATCH"
        assert "cryptography" in str(error)
        assert ">=3.0.0" in str(error)
        assert "2.9.2" in str(error)
        assert "uv add 'cryptography>=3.0.0'" in str(error)

        assert error.context["dependency.package"] == "cryptography"
        assert error.context["dependency.required_version"] == ">=3.0.0"
        assert error.context["dependency.current_version"] == "2.9.2"

    def test_dependency_mismatch_error_with_additional_context(self) -> None:
        """Test DependencyMismatchError with additional context."""
        error = DependencyMismatchError(
            "cryptography",
            required_version=">=3.0.0",
            current_version="2.9.2",
            system_info="Ubuntu 20.04",
            check_source="requirements.txt",
        )

        assert error.context["dependency.package"] == "cryptography"
        assert error.context["dependency.required_version"] == ">=3.0.0"
        assert error.context["dependency.current_version"] == "2.9.2"
        assert error.context["system_info"] == "Ubuntu 20.04"
        assert error.context["check_source"] == "requirements.txt"

    def test_dependency_mismatch_error_to_dict(self) -> None:
        """Test DependencyMismatchError serialization to dict."""
        error = DependencyMismatchError("cryptography", required_version=">=3.0.0", current_version="2.9.2")
        error_dict = error.to_dict()

        assert error_dict["error.type"] == "DependencyMismatchError"
        assert error_dict["error.code"] == "DEPENDENCY_VERSION_MISMATCH"
        assert "cryptography" in error_dict["error.message"]
        assert error_dict["dependency.package"] == "cryptography"
        assert error_dict["dependency.required_version"] == ">=3.0.0"
        assert error_dict["dependency.current_version"] == "2.9.2"

    def test_dependency_mismatch_error_with_cause(self) -> None:
        """Test DependencyMismatchError with an underlying cause."""
        cause = ImportError("cryptography 2.9.2 is too old")
        error = DependencyMismatchError(
            "cryptography", required_version=">=3.0.0", current_version="2.9.2", cause=cause
        )

        assert error.cause is cause
        assert error.__cause__ is cause

        error_dict = error.to_dict()
        assert "cryptography 2.9.2 is too old" in error_dict["error.cause"]
        assert error_dict["error.cause_type"] == "ImportError"


class TestDependencyErrorIntegration(FoundationTestCase):
    """Integration tests for dependency errors."""

    def test_errors_can_be_raised_and_caught(self) -> Never:
        """Test that dependency errors can be raised and caught properly."""
        # Test DependencyError
        with pytest.raises(DependencyError) as exc_info:
            raise DependencyError("test-package", feature="test")

        error = exc_info.value
        assert error.code == "DEPENDENCY_MISSING"
        assert "test-package" in str(error)

        # Test DependencyMismatchError
        with pytest.raises(DependencyMismatchError) as exc_info:
            raise DependencyMismatchError("test-package", required_version=">=2.0.0", current_version="1.5.0")

        error = exc_info.value
        assert error.code == "DEPENDENCY_VERSION_MISMATCH"
        assert "test-package" in str(error)

    def test_errors_can_be_caught_as_foundation_error(self) -> Never:
        """Test that dependency errors can be caught as FoundationError."""
        with pytest.raises(FoundationError):
            raise DependencyError("test-package")

        with pytest.raises(FoundationError):
            raise DependencyMismatchError("test-package", required_version=">=2.0.0", current_version="1.5.0")

    def test_error_context_is_preserved_in_exception_chain(self) -> None:
        """Test that error context is preserved when chaining exceptions."""
        original_error = ImportError("No module named 'test_package'")

        dependency_error = DependencyError("test_package", feature="test", cause=original_error)

        # Context should be preserved
        assert dependency_error.context["dependency.package"] == "test_package"
        assert dependency_error.context["dependency.feature"] == "test"

        # Cause chain should be preserved
        assert dependency_error.__cause__ is original_error

        # Should be able to serialize with all context
        error_dict = dependency_error.to_dict()
        assert error_dict["dependency.package"] == "test_package"
        assert error_dict["dependency.feature"] == "test"
        assert "No module named 'test_package'" in error_dict["error.cause"]


# 🧱🏗️🔚
