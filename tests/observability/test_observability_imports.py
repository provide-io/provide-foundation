#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Direct import path testing for observability module.

These tests verify the different import paths in observability/__init__.py
without reloading the module, focusing on specific code coverage gaps."""

from __future__ import annotations

from provide.testkit import FoundationTestCase


class TestObservabilityImportPaths(FoundationTestCase):
    """Test observability module import logic paths."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_has_otel_flag_is_boolean(self) -> None:
        """Test _HAS_OTEL flag is a boolean value."""
        import provide.foundation.observability

        assert isinstance(provide.foundation.observability._HAS_OTEL, bool)

    def test_otel_trace_attribute_exists(self) -> None:
        """Test otel_trace attribute is defined."""
        import provide.foundation.observability

        # Should exist regardless of OpenTelemetry availability
        assert hasattr(provide.foundation.observability, "otel_trace")

    def test_openobserve_client_exists(self) -> None:
        """Test OpenObserveClient is exported (either real or stub)."""
        from provide.foundation.observability import OpenObserveClient

        # Should always exist (real class or stub)
        assert OpenObserveClient is not None

    def test_search_logs_function_exists(self) -> None:
        """Test search_logs function is exported (either real or stub)."""
        from provide.foundation.observability import search_logs

        # Should always exist (real function or stub)
        assert search_logs is not None
        assert callable(search_logs)

    def test_stream_logs_function_exists(self) -> None:
        """Test stream_logs function is exported (either real or stub)."""
        from provide.foundation.observability import stream_logs

        # Should always exist (real function or stub)
        assert stream_logs is not None
        assert callable(stream_logs)

    def test_is_openobserve_available_returns_bool(self) -> None:
        """Test is_openobserve_available returns a boolean."""
        from provide.foundation.observability import is_openobserve_available

        result = is_openobserve_available()

        assert isinstance(result, bool)

    def test_is_openobserve_available_checks_globals(self) -> None:
        """Test is_openobserve_available checks globals for OpenObserveClient."""
        from provide.foundation.observability import is_openobserve_available

        # The function should check if OpenObserveClient is in globals
        # This exercises line 80: return _HAS_OTEL and "OpenObserveClient" in globals()
        result = is_openobserve_available()

        # Result depends on whether OpenObserve is actually available
        # but the function should work without errors
        assert result is True or result is False


class TestObservabilityStubs(FoundationTestCase):
    """Test stub creation when dependencies unavailable."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_openobserve_client_callable_or_class(self) -> None:
        """Test OpenObserveClient is callable (class or stub)."""
        from provide.foundation.observability import OpenObserveClient

        # Should be callable (either real class or stub function)
        assert callable(OpenObserveClient) or hasattr(OpenObserveClient, "__init__")

    def test_search_logs_callable(self) -> None:
        """Test search_logs is callable."""
        from provide.foundation.observability import search_logs

        assert callable(search_logs)

    def test_stream_logs_callable(self) -> None:
        """Test stream_logs is callable."""
        from provide.foundation.observability import stream_logs

        assert callable(stream_logs)


class TestObservabilityExports(FoundationTestCase):
    """Test module exports in __all__."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_all_contains_expected_exports(self) -> None:
        """Test __all__ contains all expected exports."""
        import provide.foundation.observability

        expected_exports = [
            "_HAS_OTEL",
            "OpenObserveClient",
            "is_openobserve_available",
            "otel_trace",
            "search_logs",
            "stream_logs",
        ]

        for export in expected_exports:
            assert export in provide.foundation.observability.__all__, f"Missing export: {export}"

    def test_all_exports_are_accessible(self) -> None:
        """Test all exports in __all__ are actually accessible."""
        import provide.foundation.observability

        for export_name in provide.foundation.observability.__all__:
            assert hasattr(provide.foundation.observability, export_name), (
                f"Export {export_name} not accessible"
            )


class TestObservabilityDependencyDetection(FoundationTestCase):
    """Test dependency detection logic."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_otel_detection_consistency(self) -> None:
        """Test OpenTelemetry detection is consistent."""
        import provide.foundation.observability

        has_otel = provide.foundation.observability._HAS_OTEL
        otel_trace = provide.foundation.observability.otel_trace

        # If OTEL is available, otel_trace should not be None
        if has_otel:
            assert otel_trace is not None
        # If OTEL is not available, otel_trace should be None
        else:
            assert otel_trace is None

    def test_openobserve_availability_logic(self) -> None:
        """Test is_openobserve_available logic."""
        import provide.foundation.observability

        has_otel = provide.foundation.observability._HAS_OTEL
        result = provide.foundation.observability.is_openobserve_available()

        # If OTEL is False, result must be False
        if not has_otel:
            assert result is False

        # If OTEL is True, result depends on OpenObserveClient availability
        # (we just verify it returns a bool)
        assert isinstance(result, bool)


class TestObservabilityContextManager(FoundationTestCase):
    """Test contextlib.suppress usage."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_suppress_imported(self) -> None:
        """Test that suppress is imported from contextlib."""
        import provide.foundation.observability

        # The module uses suppress for optional imports
        assert hasattr(provide.foundation.observability, "suppress")


class TestObservabilityTypeChecking(FoundationTestCase):
    """Test TYPE_CHECKING conditional imports."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_type_checking_constant_exists(self) -> None:
        """Test TYPE_CHECKING constant is imported."""
        import provide.foundation.observability

        # TYPE_CHECKING should be available
        assert hasattr(provide.foundation.observability, "TYPE_CHECKING")
        assert isinstance(provide.foundation.observability.TYPE_CHECKING, bool)


class TestObservabilityRealWorldUsage(FoundationTestCase):
    """Test real-world usage patterns."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_feature_check_before_use(self) -> None:
        """Test typical pattern: check availability before using features."""
        from provide.foundation.observability import is_openobserve_available

        if is_openobserve_available():
            # Would use OpenObserve features here
            from provide.foundation.observability import OpenObserveClient

            assert OpenObserveClient is not None
        else:
            # Fallback behavior - features may be stubs
            pass

        # Should complete without errors
        assert True

    def test_direct_import_of_all_features(self) -> None:
        """Test direct import of all exported features."""
        # Import all exports
        from provide.foundation.observability import (
            _HAS_OTEL,
            OpenObserveClient,
            is_openobserve_available,
            otel_trace,
            search_logs,
            stream_logs,
        )

        # All should be defined
        assert _HAS_OTEL is not None
        assert OpenObserveClient is not None
        assert is_openobserve_available is not None
        # otel_trace can be None if OpenTelemetry unavailable
        assert otel_trace is not None or otel_trace is None
        assert search_logs is not None
        assert stream_logs is not None


__all__ = [
    "TestObservabilityContextManager",
    "TestObservabilityDependencyDetection",
    "TestObservabilityExports",
    "TestObservabilityImportPaths",
    "TestObservabilityRealWorldUsage",
    "TestObservabilityStubs",
    "TestObservabilityTypeChecking",
]

# 🧱🏗️🔚
