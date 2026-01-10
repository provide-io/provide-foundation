#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for utils/deps.py module."""

import sys

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
        """Test creating DependencyStatus instances."""
        status = DependencyStatus(
            name="test_lib",
            available=True,
            version="1.0.0",
            description="Test library",
        )

        assert status.name == "test_lib"
        assert status.available is True
        assert status.version == "1.0.0"
        assert status.description == "Test library"

    def test_dependency_status_missing(self) -> None:
        """Test DependencyStatus for missing dependency."""
        status = DependencyStatus(
            name="missing_lib",
            available=False,
            version=None,
            description="Missing library",
        )

        assert status.name == "missing_lib"
        assert status.available is False
        assert status.version is None
        assert status.description == "Missing library"


class TestCheckClick(FoundationTestCase):
    """Test _check_click function."""

    def test_check_click_available(self) -> None:
        """Test _check_click when click is available."""
        with patch.dict(sys.modules, {"click": Mock()}):
            with patch("importlib.metadata.version", return_value="8.1.0"):
                result = _check_click()

                assert result.name == "click"
                assert result.available is True
                assert result.version == "8.1.0"
                assert "CLI features" in result.description

    def test_check_click_available_version_unknown(self) -> None:
        """Test _check_click when click is available but version fails."""
        with patch.dict(sys.modules, {"click": Mock()}):
            with patch("importlib.metadata.version", side_effect=Exception("No version")):
                result = _check_click()

                assert result.name == "click"
                assert result.available is True
                assert result.version == "unknown"
                assert "CLI features" in result.description

    def test_check_click_not_available(self) -> None:
        """Test _check_click when click is not available."""
        # Remove click from modules if it exists
        original_click = sys.modules.get("click")
        if "click" in sys.modules:
            del sys.modules["click"]

        try:
            with patch("builtins.__import__", side_effect=ImportError("No module named 'click'")):
                result = _check_click()

                assert result.name == "click"
                assert result.available is False
                assert result.version is None
                assert "CLI features" in result.description
        finally:
            # Restore click module if it was there
            if original_click is not None:
                sys.modules["click"] = original_click


class TestCheckCryptography(FoundationTestCase):
    """Test _check_cryptography function."""

    def test_check_cryptography_available(self) -> None:
        """Test _check_cryptography when cryptography is available."""
        mock_cryptography = Mock()
        mock_cryptography.__version__ = "3.4.8"

        with patch.dict(sys.modules, {"cryptography": mock_cryptography}):
            result = _check_cryptography()

            assert result.name == "cryptography"
            assert result.available is True
            assert result.version == "3.4.8"
            assert "Crypto features" in result.description

    def test_check_cryptography_not_available(self) -> None:
        """Test _check_cryptography when cryptography is not available."""
        with patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")):
            result = _check_cryptography()

            assert result.name == "cryptography"
            assert result.available is False
            assert result.version is None
            assert "Crypto features" in result.description


class TestCheckOpentelemetry(FoundationTestCase):
    """Test _check_opentelemetry function."""

    def test_check_opentelemetry_available(self) -> None:
        """Test _check_opentelemetry when OpenTelemetry is available."""
        with patch.dict(sys.modules, {"opentelemetry": Mock()}):
            with patch("importlib.metadata.version", return_value="1.15.0"):
                result = _check_opentelemetry()

                assert result.name == "opentelemetry"
                assert result.available is True
                assert result.version == "1.15.0"
                assert "Enhanced telemetry" in result.description

    def test_check_opentelemetry_available_version_unknown(self) -> None:
        """Test _check_opentelemetry when available but version fails."""
        with patch.dict(sys.modules, {"opentelemetry": Mock()}):
            with patch("importlib.metadata.version", side_effect=Exception("No version")):
                result = _check_opentelemetry()

                assert result.name == "opentelemetry"
                assert result.available is True
                assert result.version == "unknown"
                assert "Enhanced telemetry" in result.description

    def test_check_opentelemetry_not_available(self) -> None:
        """Test _check_opentelemetry when OpenTelemetry is not available."""
        with patch("builtins.__import__", side_effect=ImportError("No module named 'opentelemetry'")):
            result = _check_opentelemetry()

            assert result.name == "opentelemetry"
            assert result.available is False
            assert result.version is None
            assert "Enhanced telemetry" in result.description


class TestGetOptionalDependencies(FoundationTestCase):
    """Test get_optional_dependencies function."""

    def test_get_optional_dependencies_returns_list(self) -> None:
        """Test that get_optional_dependencies returns expected dependencies."""
        with (
            patch("provide.foundation.utils.deps._check_click") as mock_click,
            patch("provide.foundation.utils.deps._check_cryptography") as mock_crypto,
            patch("provide.foundation.utils.deps._check_opentelemetry") as mock_otel,
        ):
            mock_click.return_value = DependencyStatus("click", True, "8.1.0", "CLI")
            mock_crypto.return_value = DependencyStatus("cryptography", False, None, "Crypto")
            mock_otel.return_value = DependencyStatus("opentelemetry", True, "1.15.0", "Telemetry")

            result = get_optional_dependencies()

            assert len(result) == 5
            assert result[0].name == "click"
            assert result[1].name == "cryptography"
            assert result[2].name == "httpx"
            assert result[3].name == "mkdocs"
            assert result[4].name == "opentelemetry"

            mock_click.assert_called_once()
            mock_crypto.assert_called_once()
            mock_otel.assert_called_once()


class TestCheckOptionalDeps(FoundationTestCase):
    """Test check_optional_deps function."""

    def test_check_optional_deps_quiet_mode(self) -> None:
        """Test check_optional_deps in quiet mode."""
        mock_deps = [
            DependencyStatus("click", True, "8.1.0", "CLI features"),
            DependencyStatus("cryptography", False, None, "Crypto features"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            result = check_optional_deps(quiet=True, return_status=False)

            assert result is None

    def test_check_optional_deps_return_status(self) -> None:
        """Test check_optional_deps with return_status=True."""
        mock_deps = [
            DependencyStatus("click", True, "8.1.0", "CLI features"),
            DependencyStatus("cryptography", False, None, "Crypto features"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            result = check_optional_deps(quiet=True, return_status=True)

            assert result == mock_deps

    def test_check_optional_deps_verbose_all_available(self) -> None:
        """Test check_optional_deps verbose mode with all dependencies available."""
        mock_deps = [
            DependencyStatus("click", True, "8.1.0", "CLI features"),
            DependencyStatus("cryptography", True, "3.4.8", "Crypto features"),
        ]

        with (
            patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps),
            patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger,
        ):
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            result = check_optional_deps(quiet=False, return_status=True)

            assert result == mock_deps
            # Verify logging calls
            assert mock_logger.info.call_count >= 5  # Header, separator, deps, summary, celebration

    def test_check_optional_deps_verbose_some_missing(self) -> None:
        """Test check_optional_deps verbose mode with some dependencies missing."""
        mock_deps = [
            DependencyStatus("click", True, "8.1.0", "CLI features"),
            DependencyStatus("cryptography", False, None, "Crypto features"),
        ]

        with (
            patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps),
            patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger,
        ):
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            result = check_optional_deps(quiet=False, return_status=True)

            assert result == mock_deps
            # Verify logging mentions missing features
            log_calls = [call.args[0] for call in mock_logger.info.call_args_list]
            assert any("Missing features" in call for call in log_calls)

    def test_check_optional_deps_verbose_none_available(self) -> None:
        """Test check_optional_deps verbose mode with no dependencies available."""
        mock_deps = [
            DependencyStatus("click", False, None, "CLI features"),
            DependencyStatus("cryptography", False, None, "Crypto features"),
        ]

        with (
            patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps),
            patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger,
        ):
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            result = check_optional_deps(quiet=False, return_status=True)

            assert result == mock_deps
            # Verify logging suggests installing all features
            log_calls = [call.args[0] for call in mock_logger.info.call_args_list]
            assert any("provide-foundation[all]" in call for call in log_calls)


class TestHasDependency(FoundationTestCase):
    """Test has_dependency function."""

    def test_has_dependency_exists_and_available(self) -> None:
        """Test has_dependency for existing available dependency."""
        mock_deps = [
            DependencyStatus("click", True, "8.1.0", "CLI features"),
            DependencyStatus("cryptography", False, None, "Crypto features"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            result = has_dependency("click")
            assert result is True

    def test_has_dependency_exists_but_not_available(self) -> None:
        """Test has_dependency for existing but unavailable dependency."""
        mock_deps = [
            DependencyStatus("click", True, "8.1.0", "CLI features"),
            DependencyStatus("cryptography", False, None, "Crypto features"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            result = has_dependency("cryptography")
            assert result is False

    def test_has_dependency_not_exists(self) -> None:
        """Test has_dependency for non-existent dependency."""
        mock_deps = [
            DependencyStatus("click", True, "8.1.0", "CLI features"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            result = has_dependency("nonexistent")
            assert result is False


class TestRequireDependency(FoundationTestCase):
    """Test require_dependency function."""

    def test_require_dependency_available(self) -> None:
        """Test require_dependency for available dependency."""
        with patch("provide.foundation.utils.deps.has_dependency", return_value=True):
            # Should not raise
            require_dependency("click")

    def test_require_dependency_not_available(self) -> None:
        """Test require_dependency for unavailable dependency."""
        with patch("provide.foundation.utils.deps.has_dependency", return_value=False):
            with pytest.raises(ImportError) as exc_info:
                require_dependency("missing_lib")

            assert "Optional dependency 'missing_lib' is required" in str(exc_info.value)
            assert "uv add 'provide-foundation[missing_lib]'" in str(exc_info.value)


class TestGetAvailableFeatures(FoundationTestCase):
    """Test get_available_features function."""

    def test_get_available_features(self) -> None:
        """Test get_available_features returns correct mapping."""
        mock_deps = [
            DependencyStatus("click", True, "8.1.0", "CLI features"),
            DependencyStatus("cryptography", False, None, "Crypto features"),
            DependencyStatus("opentelemetry", True, "1.15.0", "Telemetry"),
        ]

        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=mock_deps):
            result = get_available_features()

            expected = {
                "click": True,
                "cryptography": False,
                "opentelemetry": True,
            }
            assert result == expected

    def test_get_available_features_empty(self) -> None:
        """Test get_available_features with no dependencies."""
        with patch("provide.foundation.utils.deps.get_optional_dependencies", return_value=[]):
            result = get_available_features()
            assert result == {}


class TestIntegration(FoundationTestCase):
    """Integration tests for multiple functions working together."""

    def test_full_workflow_all_available(self) -> None:
        """Test full workflow when all dependencies are available."""
        # Mock all dependencies as available
        with (
            patch("provide.foundation.utils.deps._check_click") as mock_click,
            patch("provide.foundation.utils.deps._check_cryptography") as mock_crypto,
            patch("provide.foundation.utils.deps._check_opentelemetry") as mock_otel,
        ):
            mock_click.return_value = DependencyStatus("click", True, "8.1.0", "CLI")
            mock_crypto.return_value = DependencyStatus("cryptography", True, "3.4.8", "Crypto")
            mock_otel.return_value = DependencyStatus("opentelemetry", True, "1.15.0", "Telemetry")

            # Test the workflow
            deps = get_optional_dependencies()
            assert len(deps) == 5
            assert all(dep.available for dep in deps)

            # Test has_dependency
            assert has_dependency("click") is True
            assert has_dependency("cryptography") is True
            assert has_dependency("httpx") is True
            assert has_dependency("mkdocs") is True
            assert has_dependency("opentelemetry") is True
            assert has_dependency("nonexistent") is False

            # Test require_dependency (should not raise)
            require_dependency("click")
            require_dependency("cryptography")

            # Test get_available_features
            features = get_available_features()
            assert features["click"] is True
            assert features["cryptography"] is True
            assert features["opentelemetry"] is True

    def test_full_workflow_mixed_availability(self) -> None:
        """Test full workflow with mixed dependency availability."""
        with (
            patch("provide.foundation.utils.deps._check_click") as mock_click,
            patch("provide.foundation.utils.deps._check_cryptography") as mock_crypto,
            patch("provide.foundation.utils.deps._check_opentelemetry") as mock_otel,
        ):
            mock_click.return_value = DependencyStatus("click", True, "8.1.0", "CLI")
            mock_crypto.return_value = DependencyStatus("cryptography", False, None, "Crypto")
            mock_otel.return_value = DependencyStatus("opentelemetry", False, None, "Telemetry")

            # Test mixed availability
            assert has_dependency("click") is True
            assert has_dependency("cryptography") is False
            assert has_dependency("opentelemetry") is False

            # Test require_dependency
            require_dependency("click")  # Should not raise

            with pytest.raises(ImportError):
                require_dependency("cryptography")

            with pytest.raises(ImportError):
                require_dependency("opentelemetry")

            # Test get_available_features
            features = get_available_features()
            assert features["click"] is True
            assert features["cryptography"] is False
            assert features["opentelemetry"] is False


# 🧱🏗️🔚
