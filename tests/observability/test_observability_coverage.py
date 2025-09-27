"""Comprehensive tests for observability/__init__.py module."""

from __future__ import annotations

from unittest.mock import Mock, patch

from provide.testkit import reset_foundation_setup_for_testing
import pytest


@pytest.fixture(autouse=True)
def reset_foundation() -> None:
    """Reset Foundation state before each test."""
    reset_foundation_setup_for_testing()


class TestObservabilityModule:
    """Test observability module functionality."""

    def test_module_imports_successfully(self) -> None:
        """Test that the module can be imported."""
        import provide.foundation.observability

        assert provide.foundation.observability is not None

    def test_has_otel_detection_without_otel(self) -> None:
        """Test OpenTelemetry detection when not available."""
        # Mock import failure
        with patch("builtins.__import__", side_effect=ImportError("No module named 'opentelemetry'")):
            # Re-import the module to trigger detection logic
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            # Check that _HAS_OTEL is False
            assert not provide.foundation.observability._HAS_OTEL
            assert provide.foundation.observability.otel_trace is None

    def test_has_otel_detection_with_otel(self) -> None:
        """Test OpenTelemetry detection when available."""
        # Create a mock trace module
        mock_trace = Mock()

        with patch.dict("sys.modules", {"opentelemetry.trace": mock_trace}):
            # Re-import the module to trigger detection logic
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            # Check that _HAS_OTEL is True
            assert provide.foundation.observability._HAS_OTEL

    def test_is_openobserve_available_without_otel(self) -> None:
        """Test is_openobserve_available when OpenTelemetry is not available."""
        with patch("provide.foundation.observability._HAS_OTEL", False):
            from provide.foundation.observability import is_openobserve_available

            assert is_openobserve_available() is False

    def test_is_openobserve_available_with_otel_no_client(self) -> None:
        """Test is_openobserve_available when OpenTelemetry is available but OpenObserveClient is not."""
        with patch("provide.foundation.observability._HAS_OTEL", True):
            # Mock globals without OpenObserveClient
            mock_globals: dict[str, object] = {}
            with patch("provide.foundation.observability.globals", return_value=mock_globals):
                from provide.foundation.observability import is_openobserve_available

                assert is_openobserve_available() is False

    def test_is_openobserve_available_with_client(self) -> None:
        """Test is_openobserve_available when both are available."""
        with patch("provide.foundation.observability._HAS_OTEL", True):
            # Mock globals with OpenObserveClient
            mock_globals = {"OpenObserveClient": Mock()}
            with patch("provide.foundation.observability.globals", return_value=mock_globals):
                from provide.foundation.observability import is_openobserve_available

                assert is_openobserve_available() is True

    def test_otel_trace_module_assignment(self) -> None:
        """Test that otel_trace is properly assigned."""
        import provide.foundation.observability

        # The otel_trace should be either None or the trace module
        assert (
            provide.foundation.observability.otel_trace is provide.foundation.observability._otel_trace_module
        )

    def test_type_checking_imports(self) -> None:
        """Test TYPE_CHECKING conditional imports."""
        # This tests that the module structure handles TYPE_CHECKING correctly
        import provide.foundation.observability

        # Should not raise any import errors even if OpenTelemetry is not available
        assert hasattr(provide.foundation.observability, "TYPE_CHECKING")

    def test_module_with_suppressed_import_errors(self) -> None:
        """Test that import errors are properly suppressed."""
        # Test that the module can handle import errors gracefully
        with patch("builtins.__import__", side_effect=ImportError("Import failed")):
            try:
                import importlib

                import provide.foundation.observability

                importlib.reload(provide.foundation.observability)
                # Should not raise an exception
            except ImportError:
                pytest.fail("ImportError should have been suppressed")


class TestObservabilityWithOtelAvailable:
    """Test observability functionality when OpenTelemetry is available."""

    def test_openobserve_imports_with_otel(self) -> None:
        """Test OpenObserve imports when OpenTelemetry is available."""
        mock_client = Mock()
        mock_search = Mock()
        mock_stream = Mock()

        # Mock the OpenObserve module
        mock_openobserve = Mock()
        mock_openobserve.OpenObserveClient = mock_client
        mock_openobserve.search_logs = mock_search
        mock_openobserve.stream_logs = mock_stream

        with (
            patch("provide.foundation.observability._HAS_OTEL", True),
            patch.dict("sys.modules", {"provide.foundation.integrations.openobserve": mock_openobserve}),
        ):
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            # Check that __all__ contains expected exports
            assert "OpenObserveClient" in provide.foundation.observability.__all__
            assert "search_logs" in provide.foundation.observability.__all__
            assert "stream_logs" in provide.foundation.observability.__all__

    def test_openobserve_import_failure_handling(self) -> None:
        """Test handling when OpenObserve imports fail."""
        with (
            patch("provide.foundation.observability._HAS_OTEL", True),
            patch("builtins.__import__", side_effect=ImportError("OpenObserve not available")),
        ):
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            # __all__ should be empty when imports fail
            assert provide.foundation.observability.__all__ == []

    def test_click_commands_import_suppression(self) -> None:
        """Test that click command imports are properly suppressed."""
        # Mock successful OpenObserve import but failing click commands
        mock_openobserve = Mock()
        mock_openobserve.OpenObserveClient = Mock()
        mock_openobserve.search_logs = Mock()
        mock_openobserve.stream_logs = Mock()

        def mock_import(name: str, *args: object, **kwargs: object) -> Mock:
            if "commands" in name:
                raise ImportError("Click not available")
            if "openobserve" in name:
                return mock_openobserve
            return Mock()

        with (
            patch("provide.foundation.observability._HAS_OTEL", True),
            patch("builtins.__import__", side_effect=mock_import),
        ):
            import importlib

            import provide.foundation.observability

            # Should not raise an exception despite click import failure
            try:
                importlib.reload(provide.foundation.observability)
            except ImportError:
                pytest.fail("ImportError should have been suppressed for click commands")


class TestObservabilityWithOtelUnavailable:
    """Test observability functionality when OpenTelemetry is not available."""

    def test_empty_exports_without_otel(self) -> None:
        """Test that __all__ is empty when OpenTelemetry is not available."""
        with patch("provide.foundation.observability._HAS_OTEL", False):
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            assert provide.foundation.observability.__all__ == []

    def test_no_openobserve_imports_without_otel(self) -> None:
        """Test that OpenObserve is not imported when OpenTelemetry is unavailable."""
        with patch("provide.foundation.observability._HAS_OTEL", False):
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            # Should not have OpenObserveClient in globals
            assert "OpenObserveClient" not in provide.foundation.observability.__dict__


class TestObservabilityConstants:
    """Test observability module constants and variables."""

    def test_otel_trace_module_variable(self) -> None:
        """Test _otel_trace_module variable handling."""
        import provide.foundation.observability

        # The variable should exist and be either None or a module
        assert hasattr(provide.foundation.observability, "_otel_trace_module")
        otel_module = provide.foundation.observability._otel_trace_module
        assert otel_module is None or hasattr(otel_module, "__name__")

    def test_has_otel_flag(self) -> None:
        """Test _HAS_OTEL flag."""
        import provide.foundation.observability

        # Should be a boolean
        assert isinstance(provide.foundation.observability._HAS_OTEL, bool)

    def test_otel_trace_alias(self) -> None:
        """Test otel_trace alias."""
        import provide.foundation.observability

        # otel_trace should be an alias for _otel_trace_module
        assert (
            provide.foundation.observability.otel_trace is provide.foundation.observability._otel_trace_module
        )


class TestObservabilityEdgeCases:
    """Test edge cases and error conditions."""

    def test_partial_import_success(self) -> None:
        """Test behavior when some imports succeed and others fail."""
        mock_openobserve = Mock()
        mock_openobserve.OpenObserveClient = Mock()
        mock_openobserve.search_logs = Mock()
        mock_openobserve.stream_logs = Mock()

        # Mock partial import success (OpenObserve succeeds, commands fail)
        def selective_import(name: str, *args: object, **kwargs: object) -> object:
            if "commands" in name:
                raise ImportError("Commands not available")
            if "integrations.openobserve" in name and "commands" not in name:
                return mock_openobserve
            # Use the real __import__ function for other imports
            return __import__(name)

        with (
            patch("provide.foundation.observability._HAS_OTEL", True),
            patch("builtins.__import__", side_effect=selective_import),
        ):
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            # Should have main exports but not commands
            assert "OpenObserveClient" in provide.foundation.observability.__all__
            assert "search_logs" in provide.foundation.observability.__all__
            assert "stream_logs" in provide.foundation.observability.__all__

    def test_globals_function_call(self) -> None:
        """Test the globals() function call in is_openobserve_available."""
        # Test that the function properly calls globals()
        with patch("provide.foundation.observability._HAS_OTEL", True):
            from provide.foundation.observability import is_openobserve_available

            # Create a mock that returns different values for globals()
            with patch("provide.foundation.observability.globals") as mock_globals:
                mock_globals.return_value = {"OpenObserveClient": Mock()}
                assert is_openobserve_available() is True

                mock_globals.return_value = {}
                assert is_openobserve_available() is False


class TestModuleIntegration:
    """Test module-level integration scenarios."""

    def test_module_attributes(self) -> None:
        """Test that expected module attributes exist."""
        import provide.foundation.observability

        # Check essential attributes
        assert hasattr(provide.foundation.observability, "_HAS_OTEL")
        assert hasattr(provide.foundation.observability, "_otel_trace_module")
        assert hasattr(provide.foundation.observability, "otel_trace")
        assert hasattr(provide.foundation.observability, "is_openobserve_available")
        assert hasattr(provide.foundation.observability, "__all__")

    def test_is_openobserve_available_function_signature(self) -> None:
        """Test is_openobserve_available function signature."""
        from provide.foundation.observability import is_openobserve_available

        # Should be callable with no arguments
        assert callable(is_openobserve_available)
        # Should return a boolean
        result = is_openobserve_available()
        assert isinstance(result, bool)

    def test_docstring_exists(self) -> None:
        """Test that the module has a docstring."""
        import provide.foundation.observability

        assert provide.foundation.observability.__doc__ is not None
        assert "Observability module for Foundation" in provide.foundation.observability.__doc__

    def test_conditional_imports_structure(self) -> None:
        """Test the conditional import structure."""
        import provide.foundation.observability

        # The module should handle TYPE_CHECKING correctly
        assert hasattr(provide.foundation.observability, "TYPE_CHECKING")

        # Should have suppress context manager
        from contextlib import suppress

        assert suppress is not None


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_production_environment_simulation(self) -> None:
        """Test behavior in a production-like environment."""
        # Simulate production where OpenTelemetry might be available
        mock_trace = Mock()
        mock_trace.__name__ = "opentelemetry.trace"

        with patch.dict("sys.modules", {"opentelemetry.trace": mock_trace}):
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            # Should properly detect OpenTelemetry
            assert provide.foundation.observability._HAS_OTEL is True

    def test_development_environment_simulation(self) -> None:
        """Test behavior in development environment without optional deps."""
        # Simulate development where OpenTelemetry is not installed
        with patch("builtins.__import__", side_effect=ImportError("Not installed")):
            import importlib

            import provide.foundation.observability

            importlib.reload(provide.foundation.observability)

            # Should gracefully handle missing dependencies
            assert provide.foundation.observability._HAS_OTEL is False
            assert provide.foundation.observability.is_openobserve_available() is False

    def test_feature_detection_workflow(self) -> None:
        """Test typical feature detection workflow."""
        from provide.foundation.observability import is_openobserve_available

        # This is how the function would typically be used
        if is_openobserve_available():
            # In real code, this would use OpenObserve features
            pass
        else:
            # Fallback behavior
            pass

        # Should not raise any exceptions
        assert isinstance(is_openobserve_available(), bool)
