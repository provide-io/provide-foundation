#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.logger import get_logger
from provide.foundation.testmode.decorators import skip_in_test_mode

"""Process title management.

Provides utilities for setting and getting process titles, making processes
identifiable in system monitoring tools like ps, top, and htop.

Automatically disabled in test mode (via @skip_in_test_mode decorator) to
prevent test interference and ensure proper test isolation, especially with
parallel test execution (pytest-xdist).

Requires the optional 'setproctitle' package for full functionality.
Install with: pip install provide-foundation[process]
"""

log = get_logger(__name__)

# Try to import setproctitle
try:
    import setproctitle

    _HAS_SETPROCTITLE = True
except ImportError:
    _HAS_SETPROCTITLE = False
    log.debug(
        "setproctitle not available, process title management disabled",
        hint="Install with: pip install provide-foundation[process]",
    )


@skip_in_test_mode(return_value=True, reason="Process title changes interfere with test isolation")
def set_process_title(title: str) -> bool:
    """Set the process title visible in system monitoring tools.

    The process title is what appears in ps, top, htop, and other system
    monitoring tools. This is useful for identifying processes, especially
    in multi-process applications or long-running services.

    Automatically disabled in test mode (via @skip_in_test_mode decorator) to
    prevent interference with test isolation and parallel test execution.

    Args:
        title: The title to set for the current process

    Returns:
        True if the title was set successfully (or skipped in test mode),
        False if setproctitle is not available

    Example:
        >>> from provide.foundation.process import set_process_title
        >>> set_process_title("my-worker-process")
        True
        >>> # Process will now show as "my-worker-process" in ps/top

    """
    if not _HAS_SETPROCTITLE:
        log.debug(
            "Cannot set process title - setproctitle not available",
            title=title,
            hint="Install with: pip install provide-foundation[process]",
        )
        return False

    try:
        setproctitle.setproctitle(title)
        log.debug("Process title set", title=title)
        return True
    except Exception as e:
        log.warning("Failed to set process title", title=title, error=str(e))
        return False


@skip_in_test_mode(return_value=None, reason="Process title queries interfere with test isolation")
def get_process_title() -> str | None:
    """Get the current process title.

    Automatically returns None in test mode (via @skip_in_test_mode decorator)
    to prevent test interference.

    Returns:
        The current process title, or None if setproctitle is not available
        or running in test mode

    Example:
        >>> from provide.foundation.process import get_process_title, set_process_title
        >>> set_process_title("my-process")
        True
        >>> get_process_title()
        'my-process'

    """
    if not _HAS_SETPROCTITLE:
        return None

    try:
        return setproctitle.getproctitle()
    except Exception as e:
        log.debug("Failed to get process title", error=str(e))
        return None


def has_setproctitle() -> bool:
    """Check if setproctitle is available.

    Returns:
        True if setproctitle is available, False otherwise

    Example:
        >>> from provide.foundation.process import has_setproctitle
        >>> if has_setproctitle():
        ...     # Use process title features
        ...     pass

    """
    return _HAS_SETPROCTITLE


@skip_in_test_mode(return_value=True, reason="Process title changes interfere with test isolation")
def set_process_title_from_argv() -> bool:
    """Set process title from argv, preserving the invoked command name.

    Extracts the command name from sys.argv[0] (including symlinks) and
    formats it with the remaining arguments to create a clean process title.

    This handles symlinks correctly - if you have a symlink 'whatever' pointing
    to 'pyvider', and run 'whatever run --config foo.yml', the process title
    will be 'whatever run --config foo.yml'.

    Automatically disabled in test mode (via @skip_in_test_mode decorator) to
    prevent interference with test isolation and parallel test execution.

    Returns:
        True if the title was set successfully (or skipped in test mode),
        False if setproctitle is not available

    Example:
        >>> # If invoked as: pyvider run --config foo.yml
        >>> from provide.foundation.process import set_process_title_from_argv
        >>> set_process_title_from_argv()
        True
        >>> # Process will show as "pyvider run --config foo.yml" in ps/top

        >>> # If invoked via symlink: whatever run
        >>> # (where whatever -> pyvider)
        >>> set_process_title_from_argv()
        True
        >>> # Process will show as "whatever run" in ps/top

    """
    from pathlib import Path
    import sys

    # Extract command name from argv[0] - preserves symlink names
    cmd_name = Path(sys.argv[0]).name
    args = sys.argv[1:]

    # Format title as "cmd arg1 arg2..."
    title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

    return set_process_title(title)


__all__ = [
    "get_process_title",
    "has_setproctitle",
    "set_process_title",
    "set_process_title_from_argv",
]

# 🧱🏗️🔚
