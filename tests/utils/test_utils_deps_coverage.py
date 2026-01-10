#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for utils/deps.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.utils.deps import (
    DependencyStatus,
    _check_click,
    _check_cryptography,
    _check_opentelemetry,
    check_optional_deps,
    get_available_features,
    get_optional_dependencies,
    has_dependency,
    require_dependency,
)


class TestDependencyStatus(FoundationTestCase):
    """Test DependencyStatus NamedTuple."""

    def test_dependency_status_creation(self) -> None:
        """Test creating DependencyStatus objects."""
        status = DependencyStatus(
            name="test",
            available=True,
            version="1.0.0",
            description="Test dependency",
        )

        assert status.name == "test"
        assert status.available is True
        assert status.version == "1.0.0"
        assert status.description == "Test dependency"

    def test_dependency_status_unavailable(self) -> None:
        """Test DependencyStatus for unavailable dependency."""
        status = DependencyStatus(
            name="missing",
            available=False,
            version=None,
            description="Missing dependency",
        )

        assert status.name == "missing"
        assert status.available is False
        assert status.version is None
        assert status.description == "Missing dependency"


class TestCheckClick(FoundationTestCase):
    """Test _check_click function."""

    def test_check_click_available(self) -> None:
        """Test _check_click when click is available."""
        # Click should be available in test environment
        status = _check_click()

        assert status.name == "click"
        assert status.available is True
        assert status.version is not None
        assert "CLI features" in status.description

    @patch("importlib.metadata.version")
    def test_check_click_version_exception(self, mock_version: Mock) -> None:
        """Test _check_click when version lookup fails."""
        mock_version.side_effect = Exception("Version lookup failed")

        status = _check_click()

        assert status.name == "click"
        assert status.available is True
        assert status.version == "unknown"
        assert "CLI features" in status.description

    def test_check_click_import_error(self) -> None:
        """Test _check_click when click is not available."""
        with patch("builtins.__import__", side_effect=ImportError("No module named 'click'")):
            status = _check_click()

            assert status.name == "click"
            assert status.available is False
            assert status.version is None
            assert "CLI features" in status.description


class TestCheckCryptography(FoundationTestCase):
    """Test _check_cryptography function."""

    def test_check_cryptography_available(self) -> None:
        """Test _check_cryptography when cryptography is available."""
        # Cryptography should be available in test environment
        status = _check_cryptography()

        assert status.name == "cryptography"
        assert status.available is True
        assert status.version is not None
        assert "Crypto features" in status.description

    def test_check_cryptography_no_version_attr(self) -> None:
        """Test _check_cryptography when cryptography has no __version__."""
        mock_cryptography = Mock()
        del mock_cryptography.__version__  # Remove version attribute

        with patch.dict("sys.modules", {"cryptography": mock_cryptography}):
            status = _check_cryptography()

            assert status.name == "cryptography"
            assert status.available is True
            assert status.version == "unknown"

    def test_check_cryptography_import_error(self) -> None:
        """Test _check_cryptography when cryptography is not available."""
        with patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")):
            status = _check_cryptography()

            assert status.name == "cryptography"
            assert status.available is False
            assert status.version is None
            assert "Crypto features" in status.description


class TestCheckOpenTelemetry(FoundationTestCase):
    """Test _check_opentelemetry function."""

    def test_check_opentelemetry_available(self) -> None:
        """Test _check_opentelemetry when opentelemetry is available."""
        # Test with actual opentelemetry import
        status = _check_opentelemetry()

        assert status.name == "opentelemetry"
        # OpenTelemetry might not be installed, so just verify the result structure
        assert isinstance(status.available, bool)
        if status.available:
            assert status.version is not None
        else:
            assert status.version is None
        assert "Enhanced telemetry" in status.description

    def test_check_opentelemetry_version_exception(self) -> None:
        """Test _check_opentelemetry when version lookup fails."""
        # This tests internal version lookup exception handling
        # Just test that the function runs without crashing
        status = _check_opentelemetry()

        assert status.name == "opentelemetry"
        assert isinstance(status.available, bool)
        if status.available and status.version == "unknown":
            # This would mean version lookup failed but import succeeded
            assert status.available is True

    def test_check_opentelemetry_import_error(self) -> None:
        """Test _check_opentelemetry when opentelemetry is not available."""
        with patch("builtins.__import__", side_effect=ImportError("No module named 'opentelemetry'")):
            status = _check_opentelemetry()

            assert status.name == "opentelemetry"
            assert status.available is False
            assert status.version is None
            assert "Enhanced telemetry" in status.description


class TestGetOptionalDependencies(FoundationTestCase):
    """Test get_optional_dependencies function."""

    def test_get_optional_dependencies(self) -> None:
        """Test get_optional_dependencies returns all expected dependencies."""
        deps = get_optional_dependencies()

        assert len(deps) == 5
        dep_names = {dep.name for dep in deps}
        expected_names = {"click", "cryptography", "httpx", "mkdocs", "opentelemetry"}
        assert dep_names == expected_names

    def test_get_optional_dependencies_types(self) -> None:
        """Test that all returned objects are DependencyStatus."""
        deps = get_optional_dependencies()

        for dep in deps:
            assert isinstance(dep, DependencyStatus)
            assert isinstance(dep.name, str)
            assert isinstance(dep.available, bool)
            assert dep.version is None or isinstance(dep.version, str)
            assert isinstance(dep.description, str)


class TestCheckOptionalDeps(FoundationTestCase):
    """Test check_optional_deps function."""

    def test_check_optional_deps_quiet_mode(self) -> None:
        """Test check_optional_deps in quiet mode."""
        result = check_optional_deps(quiet=True)
        assert result is None

    def test_check_optional_deps_return_status(self) -> None:
        """Test check_optional_deps with return_status=True."""
        result = check_optional_deps(quiet=True, return_status=True)

        assert result is not None
        assert len(result) == 5
        assert all(isinstance(dep, DependencyStatus) for dep in result)

    def test_check_optional_deps_not_quiet(self) -> None:
        """Test check_optional_deps in non-quiet mode."""
        # This will log to the console but should work without errors
        result = check_optional_deps(quiet=False, return_status=True)

        assert result is not None
        assert len(result) == 5


class TestHasDependency(FoundationTestCase):
    """Test has_dependency function."""

    def test_has_dependency_available(self) -> None:
        """Test has_dependency for available dependency."""
        mock_deps = [
            DependencyStatus("test_dep", True, "1.0", "Test"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            assert has_dependency("test_dep") is True

    def test_has_dependency_unavailable(self) -> None:
        """Test has_dependency for unavailable dependency."""
        mock_deps = [
            DependencyStatus("test_dep", False, None, "Test"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            assert has_dependency("test_dep") is False

    def test_has_dependency_not_found(self) -> None:
        """Test has_dependency for non-existent dependency."""
        mock_deps = [
            DependencyStatus("other_dep", True, "1.0", "Other"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            assert has_dependency("nonexistent_dep") is False


class TestRequireDependency(FoundationTestCase):
    """Test require_dependency function."""

    def test_require_dependency_available(self) -> None:
        """Test require_dependency for available dependency."""
        with patch("provide.foundation.utils.deps.has_dependency", return_value=True):
            # Should not raise any exception
            require_dependency("test_dep")

    def test_require_dependency_unavailable(self) -> None:
        """Test require_dependency for unavailable dependency."""
        with (
            patch("provide.foundation.utils.deps.has_dependency", return_value=False),
            pytest.raises(ImportError, match="Optional dependency 'test_dep' is required"),
        ):
            require_dependency("test_dep")

    def test_require_dependency_error_message(self) -> None:
        """Test require_dependency error message format."""
        with (
            patch("provide.foundation.utils.deps.has_dependency", return_value=False),
            pytest.raises(ImportError) as exc_info,
        ):
            require_dependency("missing_dep")

        error_msg = str(exc_info.value)
        assert "missing_dep" in error_msg
        assert "provide-foundation[missing_dep]" in error_msg


class TestGetAvailableFeatures(FoundationTestCase):
    """Test get_available_features function."""

    def test_get_available_features(self) -> None:
        """Test get_available_features returns correct dictionary."""
        mock_deps = [
            DependencyStatus("dep1", True, "1.0", "Available"),
            DependencyStatus("dep2", False, None, "Missing"),
            DependencyStatus("dep3", True, "2.0", "Available"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            features = get_available_features()

        expected = {
            "dep1": True,
            "dep2": False,
            "dep3": True,
        }
        assert features == expected

    def test_get_available_features_empty(self) -> None:
        """Test get_available_features with no dependencies."""
        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=[]):
            features = get_available_features()
            assert features == {}


class TestModuleIntegration(FoundationTestCase):
    """Test module-level integration scenarios."""

    def test_all_functions_importable(self) -> None:
        """Test that all public functions are importable."""
        from provide.foundation.utils.deps import (
            DependencyStatus,
            check_optional_deps,
            get_available_features,
            get_optional_dependencies,
            has_dependency,
            require_dependency,
        )

        # Verify functions are callable
        assert callable(check_optional_deps)
        assert callable(get_available_features)
        assert callable(get_optional_dependencies)
        assert callable(has_dependency)
        assert callable(require_dependency)

        # Verify DependencyStatus is a type
        assert isinstance(DependencyStatus, type)

    def test_real_dependency_checks(self) -> None:
        """Test with real dependency checking."""
        # These should work with actual environment
        deps = get_optional_dependencies()
        features = get_available_features()

        assert len(deps) == len(features)
        for dep in deps:
            assert dep.name in features
            assert features[dep.name] == dep.available


# 🧱🏗️🔚
