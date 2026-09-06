#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

#
# detection.py
#
import os
import sys
from types import FrameType

"""Test Mode Detection for Foundation.

This module provides utilities for detecting various test environments
and adjusting Foundation behavior accordingly.
"""

# Cache for test mode detection to avoid expensive inspect.stack() calls
# Test mode doesn't change during runtime, so we can cache aggressively
_test_mode_cache: bool | None = None

# Cache for click testing detection — inspect.stack() is expensive
_click_testing_cache: bool | None = None


def _clear_test_mode_cache() -> None:
    """Clear the test mode detection cache.

    This is primarily for test isolation - allows tests to reset the cache
    when they need to test different detection scenarios.
    """
    global _test_mode_cache, _click_testing_cache
    _test_mode_cache = None
    _click_testing_cache = None


def is_in_test_mode() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Performance: Results are cached after first detection since test mode
    doesn't change during process lifetime. Use _clear_test_mode_cache()
    in tests for proper isolation.

    Returns:
        True if running in test mode, False otherwise
    """
    global _test_mode_cache

    # Return cached result if available
    if _test_mode_cache is not None:
        return _test_mode_cache

    # Primary indicator: pytest current test environment variable (FAST)
    if "PYTEST_CURRENT_TEST" in os.environ:
        _test_mode_cache = True
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context (FAST)
        if any("pytest" in arg for arg in sys.argv):
            _test_mode_cache = True
            return True

        # Last resort: Walk the call stack via sys._getframe() which is much
        # cheaper than inspect.stack() (avoids inspect.getmodule() and source
        # context lookup per frame).
        cur_frame: FrameType | None = sys._getframe()
        while cur_frame is not None:
            filename = cur_frame.f_code.co_filename
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                _test_mode_cache = True
                return True
            cur_frame = cur_frame.f_back

    # Check for unittest runner in active execution (FAST)
    if "unittest" in sys.modules and any("unittest" in arg for arg in sys.argv):
        _test_mode_cache = True
        return True

    # Not in test mode - cache the negative result too
    _test_mode_cache = False
    return False


def is_in_click_testing() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Results are cached to avoid expensive inspect.stack() calls on
    every stream redirect. Cache is cleared via _clear_test_mode_cache().

    Returns:
        True if running in Click testing context, False otherwise
    """
    global _click_testing_cache

    # Only the environment-variable answer is cached. It describes the process
    # and cannot change during it; the stack walk below describes *this call*
    # and nothing more.
    #
    # Caching the stack-derived answer latched the first Click test's verdict
    # for every later caller in the same process. Under xdist that meant one
    # Click test silently switched off stream redirection for the rest of its
    # worker: `set_log_stream_for_testing` returned without installing the
    # buffer, and tests capturing logs saw an empty one. Measured on this suite,
    # 48 tests were being denied a redirect they had asked for.
    if _click_testing_cache:
        return True

    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing (fast path)
    if config.click_testing:
        _click_testing_cache = True
        return True

    # Walk the call stack via sys._getframe() — avoids the overhead of
    # inspect.stack() (no getmodule() / source context per frame).
    cur_frame: FrameType | None = sys._getframe()
    while cur_frame is not None:
        module = cur_frame.f_globals.get("__name__", "")
        filename = cur_frame.f_code.co_filename

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = cur_frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

        cur_frame = cur_frame.f_back

    return False


def should_allow_stream_redirect() -> bool:
    """Check if stream redirection should be allowed in testing.

    Stream redirection is normally blocked when in Click testing context
    to prevent interference with Click's output capture. This can be
    overridden with FOUNDATION_FORCE_STREAM_REDIRECT=true.

    Returns:
        True if stream redirect is allowed (not in Click testing OR force enabled)
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Allow if force flag is set
    if config.force_stream_redirect:
        return True

    # Otherwise, block if in Click testing
    return not is_in_click_testing()


def should_use_shared_registries(
    use_shared_registries: bool,
    component_registry: object | None,
    command_registry: object | None,
) -> bool:
    """Determine if Hub should use shared registries based on explicit parameters.

    Args:
        use_shared_registries: Explicit user preference
        component_registry: Custom component registry if provided
        command_registry: Custom command registry if provided

    Returns:
        True if shared registries should be used
    """
    # Return explicit preference - no auto-detection magic
    return use_shared_registries


def configure_structlog_for_test_safety() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import sys

    import structlog

    from provide.foundation.logger.defaults import safe_console_renderer
    from provide.foundation.utils.streams import ensure_utf8_stream

    # Configure structlog to use stdout (safe for multiprocessing)
    # Use BoundLogger instead of make_filtering_bound_logger to preserve
    # custom log levels like trace
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            safe_console_renderer(),
        ],
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        # Through ensure_utf8_stream, because every event Foundation logs is
        # emoji-prefixed and a Windows console stream is cp1252, which has no
        # mapping for them. PrintLogger keeps the file object it is given, so a
        # raw stream here makes every later log call raise UnicodeEncodeError
        # into whatever called the logger.
        logger_factory=structlog.PrintLoggerFactory(file=ensure_utf8_stream(sys.stdout)),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


# 🧱🏗️🔚
