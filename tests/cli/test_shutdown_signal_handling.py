#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for signal handler management in CLI shutdown."""

from __future__ import annotations

import signal
import threading
from typing import Any

import pytest

from provide.foundation.cli.shutdown import (
    register_cleanup_handlers,
    unregister_cleanup_handlers,
)

# Global lock to prevent parallel execution of signal handler tests
_signal_test_lock = threading.Lock()


@pytest.mark.usefixtures("_signal_handler_isolation")
class TestSignalHandlerManagement:
    """Test signal handler registration and restoration."""

    @pytest.fixture(autouse=True)
    def _signal_handler_isolation(self) -> None:
        """Ensure signal handler tests don't run in parallel."""
        # Acquire lock to serialize these tests
        _signal_test_lock.acquire()
        try:
            # Ensure clean slate - unregister any Foundation handlers first
            unregister_cleanup_handlers()

            # Set to a known baseline (default handler)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            signal.signal(signal.SIGTERM, signal.SIG_DFL)

            # Save baseline handlers
            self.original_sigint = signal.getsignal(signal.SIGINT)
            self.original_sigterm = signal.getsignal(signal.SIGTERM)

            yield

            # Always clean up after tests
            unregister_cleanup_handlers()
            # Restore to baseline state
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
        finally:
            # Release lock
            _signal_test_lock.release()

    def test_register_handlers_changes_signal_handlers(self) -> None:
        """Test that registering handlers changes signal handlers."""
        # Register our handlers
        register_cleanup_handlers(manage_signals=True)

        # Get current handlers
        current_sigint = signal.getsignal(signal.SIGINT)
        current_sigterm = signal.getsignal(signal.SIGTERM)

        # Should be different from original
        assert current_sigint != self.original_sigint
        assert current_sigterm != self.original_sigterm

    def test_register_without_signal_management_preserves_handlers(self) -> None:
        """Test that registering without signal management preserves handlers."""
        # Register without signal management
        register_cleanup_handlers(manage_signals=False)

        # Get current handlers
        current_sigint = signal.getsignal(signal.SIGINT)
        current_sigterm = signal.getsignal(signal.SIGTERM)

        # Should be same as original
        assert current_sigint == self.original_sigint
        assert current_sigterm == self.original_sigterm

    def test_unregister_restores_original_handlers(self) -> None:
        """Test that unregistering restores original signal handlers."""
        # Register our handlers
        register_cleanup_handlers(manage_signals=True)

        # Verify handlers changed
        assert signal.getsignal(signal.SIGINT) != self.original_sigint

        # Unregister
        unregister_cleanup_handlers()

        # Handlers should be restored
        assert signal.getsignal(signal.SIGINT) == self.original_sigint
        assert signal.getsignal(signal.SIGTERM) == self.original_sigterm

    def test_custom_signal_handlers_are_preserved(self) -> None:
        """Test that custom signal handlers set before registration are preserved."""

        # Define custom handlers
        def custom_sigint_handler(signum: int, frame: Any) -> None:
            pass

        def custom_sigterm_handler(signum: int, frame: Any) -> None:
            pass

        # Set custom handlers
        signal.signal(signal.SIGINT, custom_sigint_handler)
        signal.signal(signal.SIGTERM, custom_sigterm_handler)

        # Register Foundation handlers
        register_cleanup_handlers(manage_signals=True)

        # Verify Foundation handlers are active
        assert signal.getsignal(signal.SIGINT) != custom_sigint_handler

        # Unregister
        unregister_cleanup_handlers()

        # Custom handlers should be restored
        assert signal.getsignal(signal.SIGINT) == custom_sigint_handler
        assert signal.getsignal(signal.SIGTERM) == custom_sigterm_handler

    def test_double_register_is_safe(self) -> None:
        """Test that registering handlers twice doesn't cause issues."""
        # Register once
        register_cleanup_handlers(manage_signals=True)
        first_handler = signal.getsignal(signal.SIGINT)

        # Register again
        register_cleanup_handlers(manage_signals=True)
        second_handler = signal.getsignal(signal.SIGINT)

        # Should have same handler
        assert first_handler == second_handler

        # Cleanup
        unregister_cleanup_handlers()

    def test_manage_signals_false_for_library_use(self) -> None:
        """Test manage_signals=False pattern for library integration."""

        # Define app's signal handler
        def app_signal_handler(signum: int, frame: Any) -> None:
            """Application's signal handler."""

        # App sets its own handlers
        signal.signal(signal.SIGINT, app_signal_handler)
        signal.signal(signal.SIGTERM, app_signal_handler)

        # Foundation registers without managing signals (library mode)
        register_cleanup_handlers(manage_signals=False)

        # App's handlers should still be active
        assert signal.getsignal(signal.SIGINT) == app_signal_handler
        assert signal.getsignal(signal.SIGTERM) == app_signal_handler

        # Cleanup
        unregister_cleanup_handlers()

        # App's handlers still intact
        assert signal.getsignal(signal.SIGINT) == app_signal_handler
        assert signal.getsignal(signal.SIGTERM) == app_signal_handler


__all__ = ["TestSignalHandlerManagement"]

# 🧱🏗️🔚
