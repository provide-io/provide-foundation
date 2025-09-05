"""Tests for the testing module warning system."""

import os
import sys
import warnings
from unittest.mock import patch

import pytest


class TestTestingWarnings:
    """Test the warning system for testing helpers."""

    def test_is_testing_context_detects_pytest(self):
        """Test that pytest context is detected."""
        # pytest should already be in sys.modules
        from provide.foundation.testing import _is_testing_context
        
        assert _is_testing_context() is True

    def test_is_testing_context_detects_unittest(self):
        """Test that unittest context is detected.""" 
        from provide.foundation.testing import _is_testing_context
        
        with patch.dict(sys.modules, {"unittest": True}):
            assert _is_testing_context() is True

    def test_is_testing_context_detects_env_var(self):
        """Test that TESTING environment variable is detected."""
        from provide.foundation.testing import _is_testing_context
        
        with patch.dict(os.environ, {"TESTING": "true"}):
            assert _is_testing_context() is True

    def test_is_testing_context_detects_pytest_current_test(self):
        """Test that PYTEST_CURRENT_TEST is detected."""
        from provide.foundation.testing import _is_testing_context
        
        with patch.dict(os.environ, {"PYTEST_CURRENT_TEST": "test_example.py::test_func"}):
            assert _is_testing_context() is True

    def test_is_testing_context_detects_argv(self):
        """Test that pytest in argv is detected."""
        from provide.foundation.testing import _is_testing_context
        
        with patch.object(sys, 'argv', ['python', '-m', 'pytest']):
            assert _is_testing_context() is True

    def test_warn_testing_active_issues_warning(self):
        """Test that warning is issued when testing helpers are active."""
        from provide.foundation.testing import _warn_testing_active
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _warn_testing_active()
            
            assert len(w) == 1
            assert "Foundation testing helpers are active" in str(w[0].message)
            assert w[0].category == UserWarning

    def test_warning_suppression_env_var(self):
        """Test that warnings can be suppressed via environment variable."""
        from provide.foundation.testing import _warn_testing_active
        
        with patch.dict(os.environ, {"FOUNDATION_SUPPRESS_TESTING_WARNINGS": "1"}):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                _warn_testing_active()
                
                assert len(w) == 0

    def test_should_warn_logic(self):
        """Test the _should_warn function logic."""
        from provide.foundation.testing import _should_warn
        
        # Should not warn if suppressed
        with patch.dict(os.environ, {"FOUNDATION_SUPPRESS_TESTING_WARNINGS": "1"}):
            assert _should_warn() is False

    def test_lazy_import_works(self):
        """Test that lazy imports work correctly."""
        # Import a specific function to trigger lazy loading
        from provide.foundation.testing import reset_foundation_setup_for_testing
        
        assert callable(reset_foundation_setup_for_testing)

    def test_lazy_import_raises_for_nonexistent(self):
        """Test that lazy import raises AttributeError for non-existent attributes."""
        import provide.foundation.testing as testing
        
        with pytest.raises(AttributeError):
            _ = testing.nonexistent_function

    def test_all_expected_functions_available(self):
        """Test that all expected functions are available in __all__."""
        from provide.foundation.testing import __all__
        
        expected_functions = [
            "_is_testing_context",
            "MockContext", 
            "isolated_cli_runner",
            "reset_foundation_setup_for_testing",
            "set_log_stream_for_testing",
            "captured_stderr_for_foundation",
            "client_cert",
            "default_container_directory",
        ]
        
        for func in expected_functions:
            assert func in __all__, f"{func} not in __all__"

    def test_warning_issued_on_import(self):
        """Test that warning is issued when testing module is imported."""
        # This test is tricky because the module is already imported
        # We'll test the warning mechanism indirectly
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Import specific function to potentially trigger warning
            from provide.foundation.testing import _warn_testing_active
            _warn_testing_active()
            
            # Should have at least one warning
            warning_messages = [str(warning.message) for warning in w]
            assert any("Foundation testing helpers are active" in msg for msg in warning_messages)