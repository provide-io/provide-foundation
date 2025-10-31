#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import atexit
from collections.abc import Callable
import contextlib
import functools
import signal
import sys
from typing import Any, ParamSpec, TypeVar

from provide.foundation.config.defaults import EXIT_SIGINT
from provide.foundation.console.output import perr
from provide.foundation.hub.foundation import get_foundation_logger
from provide.foundation.hub.lifecycle import cleanup_all_components

"""CLI shutdown and cleanup infrastructure.

Provides signal handling, atexit cleanup, and decorators for graceful
shutdown of CLI commands with resource cleanup.
"""

log = get_foundation_logger()

# Track if cleanup has already run
_cleanup_executed = False
_original_sigint_handler: Any = None
_original_sigterm_handler: Any = None
_handlers_registered = False


def _flush_otlp_logs() -> None:
    """Flush OTLP logs if available."""
    try:
        from provide.foundation.logger.processors.otlp import flush_otlp_logs

        flush_otlp_logs()
    except ImportError:
        pass


def _cleanup_foundation_resources() -> None:
    """Clean up all Foundation resources.

    This is the central cleanup function called on exit, interrupt, or error.
    It ensures all resources are properly cleaned up exactly once.
    Automatically restores original signal handlers.
    """
    global _cleanup_executed

    if _cleanup_executed:
        return

    _cleanup_executed = True

    try:
        # Flush OTLP logs first (before component cleanup)
        _flush_otlp_logs()

        # Clean up all registered components
        cleanup_all_components()

        # Restore original signal handlers automatically
        _restore_signal_handlers()

    except Exception as e:
        # Log cleanup errors but don't raise - we're already exiting
        try:
            log.error("Error during cleanup", error=str(e))
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def _signal_handler(signum: int, frame: Any) -> None:
    """Handle interrupt signals (SIGINT, SIGTERM on Unix).

    Args:
        signum: Signal number
        frame: Current stack frame

    Note:
        On Windows, only SIGINT is supported. SIGTERM doesn't exist.
    """
    signal_name = signal.Signals(signum).name
    log.info(f"Received {signal_name}, cleaning up...")

    # Run cleanup
    _cleanup_foundation_resources()

    # Exit with appropriate code
    sys.exit(EXIT_SIGINT if signum == signal.SIGINT else 1)


def _restore_signal_handlers() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    # SIGTERM only exists on Unix-like systems
    if sys.platform != "win32" and _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def register_cleanup_handlers(*, manage_signals: bool = True) -> None:
    """Register signal handlers and atexit cleanup.

    This should be called once at CLI startup to ensure cleanup
    happens on all exit paths.

    Args:
        manage_signals: If True, register signal handlers. If False, only
            register atexit cleanup. Set to False if an application built
            with this framework is being used as a library by another process
            that manages its own signals.

    Note:
        Signal handlers are automatically restored during cleanup.

    """
    global _original_sigint_handler, _original_sigterm_handler, _handlers_registered

    # Register atexit cleanup
    atexit.register(_cleanup_foundation_resources)

    # Register signal handlers if requested
    if manage_signals:
        # Save original handlers
        _original_sigint_handler = signal.getsignal(signal.SIGINT)

        # SIGTERM only exists on Unix-like systems
        if sys.platform != "win32":
            _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)

        # Register SIGTERM handler on Unix only
        if sys.platform != "win32":
            signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def unregister_cleanup_handlers() -> None:
    """Unregister cleanup handlers (mainly for testing).

    Restores original signal handlers and removes atexit hook.
    """
    global _cleanup_executed

    # Restore original signal handlers
    _restore_signal_handlers()

    # Remove atexit handler
    with contextlib.suppress(ValueError):
        atexit.unregister(_cleanup_foundation_resources)

    # Reset cleanup flag
    _cleanup_executed = False

    log.trace("Unregister cleanup handlers")


# Type variables for decorator
P = ParamSpec("P")
R = TypeVar("R")


def with_cleanup(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to ensure cleanup on CLI command exit.

    Wraps a CLI command function to:
    1. Handle KeyboardInterrupt gracefully
    2. Ensure cleanup on all exit paths
    3. Provide consistent error handling

    Example:
        @click.command()
        @with_cleanup
        def my_command(ctx: click.Context) -> None:
            # Command implementation
            pass

    Args:
        func: CLI command function to wrap

    Returns:
        Wrapped function with cleanup

    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            # Execute the command
            return func(*args, **kwargs)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            try:
                # Try to use click for pretty output if available
                from provide.foundation.cli.deps import click

                click.echo("\n⛔ Command interrupted by user")
            except ImportError:
                # Use Foundation's console output
                perr("\n⛔ Command interrupted by user")

            # Cleanup will be handled by atexit/signal handlers
            sys.exit(EXIT_SIGINT)

        except Exception as e:
            # Log unexpected errors
            log.error("Command failed with unexpected error", error=str(e), exc_info=True)

            # Cleanup will be handled by atexit
            raise

    return wrapper


__all__ = [
    "register_cleanup_handlers",
    "unregister_cleanup_handlers",
    "with_cleanup",
]

# 🧱🏗️🔚
