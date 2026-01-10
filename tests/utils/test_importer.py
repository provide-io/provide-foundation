#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import sys
import threading

from provide.testkit.mocking import patch
import pytest

from provide.foundation.utils.importer import MAX_LAZY_IMPORT_DEPTH, lazy_import

"""Tests for the lazy import utility module."""


class TestLazyImport:
    """Test lazy_import function."""

    def test_lazy_import_valid_module(self) -> None:
        """Test lazy importing a valid module."""
        # Import the logger module lazily
        module = lazy_import("provide.foundation", "logger")
        assert module is not None
        assert hasattr(module, "get_logger")
        assert "provide.foundation.logger" in sys.modules

    def test_lazy_import_already_cached(self) -> None:
        """Test lazy importing a module that's already in sys.modules."""
        # First import
        module1 = lazy_import("provide.foundation", "errors")
        # Second import should return cached version
        module2 = lazy_import("provide.foundation", "errors")
        assert module1 is module2
        assert id(module1) == id(module2)

    def test_lazy_import_invalid_module(self) -> None:
        """Test lazy importing a module that doesn't exist."""
        with pytest.raises(ImportError, match="No module named"):
            lazy_import("provide.foundation", "nonexistent_module_xyz")

    def test_lazy_import_recursion_depth_limit(self) -> None:
        """Test that recursion depth is limited."""
        # Mock the thread-local to simulate deep recursion
        with patch("provide.foundation.utils.importer._thread_local") as mock_tl:
            mock_tl.getattr_in_progress = set()
            mock_tl.import_depth = MAX_LAZY_IMPORT_DEPTH
            mock_tl.import_chain = ["module1", "module2", "module3"]

            with pytest.raises(RecursionError, match=r"Lazy import depth limit.*exceeded"):
                lazy_import("provide.foundation", "logger")

    def test_lazy_import_circular_import_detection(self) -> None:
        """Test that circular imports are detected."""
        # Mock the thread-local to simulate circular import
        with patch("provide.foundation.utils.importer._thread_local") as mock_tl:
            mock_tl.getattr_in_progress = {"logger"}
            mock_tl.import_depth = 1
            mock_tl.import_chain = ["errors"]

            with pytest.raises(AttributeError, match="circular import detected"):
                lazy_import("provide.foundation", "logger")

    def test_lazy_import_corrupted_module_state(self) -> None:
        """Test handling of corrupted module in sys.modules."""
        module_name = "provide.foundation.test_corrupted_module"

        # Add a None entry to simulate corruption
        sys.modules[module_name] = None  # type: ignore[assignment]

        try:
            # Should handle the corrupted state and attempt re-import
            with pytest.raises(ImportError):
                lazy_import("provide.foundation", "test_corrupted_module")

            # Verify it was removed from sys.modules
            assert module_name not in sys.modules
        finally:
            # Clean up
            sys.modules.pop(module_name, None)

    def test_lazy_import_special_module_click_missing(self) -> None:
        """Test special error message for CLI module when click is missing."""
        # Clear CLI module from cache to ensure fresh import
        cli_module_key = "provide.foundation.cli"
        if cli_module_key in sys.modules:
            del sys.modules[cli_module_key]

        with patch("builtins.__import__") as mock_import:
            # Simulate ImportError mentioning 'click'
            mock_import.side_effect = ImportError("No module named 'click'")

            with pytest.raises(ImportError, match="CLI features require optional dependencies"):
                lazy_import("provide.foundation", "cli")

    def test_lazy_import_thread_safety(self) -> None:
        """Test that lazy imports are thread-safe."""
        results: list[object] = []
        errors: list[Exception] = []

        def import_module() -> None:
            try:
                module = lazy_import("provide.foundation", "config")
                results.append(module)
            except Exception as e:
                errors.append(e)

        # Create multiple threads trying to import the same module
        threads = [threading.Thread(target=import_module) for _ in range(10)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All threads should succeed
        assert len(errors) == 0, f"Unexpected errors: {errors}"
        assert len(results) == 10

        # All results should be the same module instance
        assert all(r is results[0] for r in results)

    def test_lazy_import_recursion_guard_cleanup(self) -> None:
        """Test that recursion guards are properly cleaned up after import."""
        # Import a module
        module = lazy_import("provide.foundation", "platform")
        assert module is not None

        # After successful import, thread-local should be clean
        from provide.foundation.utils.importer import _thread_local

        if hasattr(_thread_local, "getattr_in_progress"):
            assert "platform" not in _thread_local.getattr_in_progress
            # Depth should be back to 0 or uninitialized
            if hasattr(_thread_local, "import_depth"):
                assert _thread_local.import_depth == 0

    def test_lazy_import_error_propagation(self) -> None:
        """Test that import errors are properly propagated."""
        with pytest.raises(ImportError) as exc_info:
            lazy_import("provide.foundation", "definitely_not_a_real_module")

        # Should contain the module name in the error
        assert "definitely_not_a_real_module" in str(exc_info.value)

    def test_lazy_import_module_attributes(self) -> None:
        """Test that imported module has expected attributes."""
        module = lazy_import("provide.foundation", "resilience")
        assert module is not None

        # Check for key exports from resilience module
        assert hasattr(module, "retry")
        assert hasattr(module, "circuit_breaker")
        assert hasattr(module, "fallback")

    def test_lazy_import_submodule_path(self) -> None:
        """Test lazy import creates correct module path."""
        module = lazy_import("provide.foundation", "hub")
        assert module.__name__ == "provide.foundation.hub"
        assert "provide.foundation.hub" in sys.modules


class TestLazyImportEdgeCases:
    """Test edge cases and error conditions."""

    def test_thread_local_initialization(self) -> None:
        """Test thread-local state is initialized correctly."""
        from provide.foundation.utils.importer import _thread_local

        # Clear any existing state
        if hasattr(_thread_local, "getattr_in_progress"):
            delattr(_thread_local, "getattr_in_progress")
        if hasattr(_thread_local, "import_depth"):
            delattr(_thread_local, "import_depth")
        if hasattr(_thread_local, "import_chain"):
            delattr(_thread_local, "import_chain")

        # Import should initialize thread-local state
        module = lazy_import("provide.foundation", "context")
        assert module is not None

        # Thread-local should now be initialized
        assert hasattr(_thread_local, "getattr_in_progress")
        assert hasattr(_thread_local, "import_depth")
        assert hasattr(_thread_local, "import_chain")

    def test_import_chain_tracking(self) -> None:
        """Test that import chain is properly tracked."""
        from provide.foundation.utils.importer import _thread_local

        # Manually set up a chain
        if not hasattr(_thread_local, "getattr_in_progress"):
            _thread_local.getattr_in_progress = set()
            _thread_local.import_depth = 0
            _thread_local.import_chain = []

        initial_depth = _thread_local.import_depth
        initial_chain_len = len(_thread_local.import_chain)

        # Import a module
        module = lazy_import("provide.foundation", "tracer")
        assert module is not None

        # After import, depth should be back to initial
        assert _thread_local.import_depth == initial_depth
        # Chain should be back to initial length
        assert len(_thread_local.import_chain) == initial_chain_len

    def test_concurrent_different_modules(self) -> None:
        """Test concurrent imports of different modules."""
        modules: dict[str, object] = {}
        errors: list[Exception] = []
        lock = threading.Lock()

        def import_module(name: str) -> None:
            try:
                module = lazy_import("provide.foundation", name)
                with lock:
                    modules[name] = module
            except Exception as e:
                with lock:
                    errors.append(e)

        # Import different modules concurrently
        module_names = ["errors", "config", "logger", "resilience", "hub"]
        threads = [threading.Thread(target=import_module, args=(name,)) for name in module_names]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All imports should succeed
        assert len(errors) == 0, f"Unexpected errors: {errors}"
        assert len(modules) == len(module_names)

        # Each module should be valid
        for name in module_names:
            assert modules[name] is not None
            assert f"provide.foundation.{name}" in sys.modules

    def test_import_with_mock_failure(self) -> None:
        """Test behavior when __import__ fails."""
        with patch("builtins.__import__") as mock_import:
            mock_import.side_effect = ImportError("Simulated import failure")

            with pytest.raises(ImportError, match="Simulated import failure"):
                lazy_import("provide.foundation", "fake_module")

    def test_special_modules_dict(self) -> None:
        """Test SPECIAL_MODULES contains expected entries."""
        from provide.foundation.utils.importer import SPECIAL_MODULES

        assert "cli" in SPECIAL_MODULES
        assert "uv add" in SPECIAL_MODULES["cli"]
        assert "provide-foundation[cli]" in SPECIAL_MODULES["cli"]


# 🧱🏗️🔚
