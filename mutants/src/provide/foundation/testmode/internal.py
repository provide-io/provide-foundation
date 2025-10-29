# provide/foundation/testmode/internal.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# internal.py
#
import structlog

"""Internal Reset APIs for Foundation Testing.

This module provides low-level reset functions that testing frameworks
can use to reset Foundation's internal state. These are internal APIs
designed to be called by testkit for proper test isolation.
"""

# Global flags to prevent recursive resets in individual functions
_eventsets_reset_in_progress = False
_hub_reset_in_progress = False
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_reset_event_loops__mutmut_orig() -> None:
    """Close any running event loops to prevent worker shutdown hangs.

    This is critical for pytest-xdist workers to shut down cleanly after
    async tests complete.

    IMPORTANT: This MUST be called AFTER reset_time_machine_state() to ensure
    time patches are stopped before creating a new event loop. Otherwise the
    new loop may cache frozen time.monotonic references.
    """
    try:
        import asyncio

        # Close the current event loop if it's not running
        try:
            loop = asyncio.get_event_loop()
            # Don't close if it's running (we're inside an async context)
            if not loop.is_running() and not loop.is_closed():
                loop.close()
        except RuntimeError:
            # No event loop in this thread, that's fine
            pass

        # DON'T create a new event loop - let pytest-asyncio manage it
        # If we create one here while time patches are still active (fixture cleanup
        # hasn't run yet), the new loop will cache frozen time.monotonic references
    except Exception:
        # If anything fails, continue - better to leak a loop than crash
        pass


def x_reset_event_loops__mutmut_1() -> None:
    """Close any running event loops to prevent worker shutdown hangs.

    This is critical for pytest-xdist workers to shut down cleanly after
    async tests complete.

    IMPORTANT: This MUST be called AFTER reset_time_machine_state() to ensure
    time patches are stopped before creating a new event loop. Otherwise the
    new loop may cache frozen time.monotonic references.
    """
    try:
        import asyncio

        # Close the current event loop if it's not running
        try:
            loop = None
            # Don't close if it's running (we're inside an async context)
            if not loop.is_running() and not loop.is_closed():
                loop.close()
        except RuntimeError:
            # No event loop in this thread, that's fine
            pass

        # DON'T create a new event loop - let pytest-asyncio manage it
        # If we create one here while time patches are still active (fixture cleanup
        # hasn't run yet), the new loop will cache frozen time.monotonic references
    except Exception:
        # If anything fails, continue - better to leak a loop than crash
        pass


def x_reset_event_loops__mutmut_2() -> None:
    """Close any running event loops to prevent worker shutdown hangs.

    This is critical for pytest-xdist workers to shut down cleanly after
    async tests complete.

    IMPORTANT: This MUST be called AFTER reset_time_machine_state() to ensure
    time patches are stopped before creating a new event loop. Otherwise the
    new loop may cache frozen time.monotonic references.
    """
    try:
        import asyncio

        # Close the current event loop if it's not running
        try:
            loop = asyncio.get_event_loop()
            # Don't close if it's running (we're inside an async context)
            if not loop.is_running() or not loop.is_closed():
                loop.close()
        except RuntimeError:
            # No event loop in this thread, that's fine
            pass

        # DON'T create a new event loop - let pytest-asyncio manage it
        # If we create one here while time patches are still active (fixture cleanup
        # hasn't run yet), the new loop will cache frozen time.monotonic references
    except Exception:
        # If anything fails, continue - better to leak a loop than crash
        pass


def x_reset_event_loops__mutmut_3() -> None:
    """Close any running event loops to prevent worker shutdown hangs.

    This is critical for pytest-xdist workers to shut down cleanly after
    async tests complete.

    IMPORTANT: This MUST be called AFTER reset_time_machine_state() to ensure
    time patches are stopped before creating a new event loop. Otherwise the
    new loop may cache frozen time.monotonic references.
    """
    try:
        import asyncio

        # Close the current event loop if it's not running
        try:
            loop = asyncio.get_event_loop()
            # Don't close if it's running (we're inside an async context)
            if loop.is_running() and not loop.is_closed():
                loop.close()
        except RuntimeError:
            # No event loop in this thread, that's fine
            pass

        # DON'T create a new event loop - let pytest-asyncio manage it
        # If we create one here while time patches are still active (fixture cleanup
        # hasn't run yet), the new loop will cache frozen time.monotonic references
    except Exception:
        # If anything fails, continue - better to leak a loop than crash
        pass


def x_reset_event_loops__mutmut_4() -> None:
    """Close any running event loops to prevent worker shutdown hangs.

    This is critical for pytest-xdist workers to shut down cleanly after
    async tests complete.

    IMPORTANT: This MUST be called AFTER reset_time_machine_state() to ensure
    time patches are stopped before creating a new event loop. Otherwise the
    new loop may cache frozen time.monotonic references.
    """
    try:
        import asyncio

        # Close the current event loop if it's not running
        try:
            loop = asyncio.get_event_loop()
            # Don't close if it's running (we're inside an async context)
            if not loop.is_running() and loop.is_closed():
                loop.close()
        except RuntimeError:
            # No event loop in this thread, that's fine
            pass

        # DON'T create a new event loop - let pytest-asyncio manage it
        # If we create one here while time patches are still active (fixture cleanup
        # hasn't run yet), the new loop will cache frozen time.monotonic references
    except Exception:
        # If anything fails, continue - better to leak a loop than crash
        pass


x_reset_event_loops__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_event_loops__mutmut_1": x_reset_event_loops__mutmut_1,
    "x_reset_event_loops__mutmut_2": x_reset_event_loops__mutmut_2,
    "x_reset_event_loops__mutmut_3": x_reset_event_loops__mutmut_3,
    "x_reset_event_loops__mutmut_4": x_reset_event_loops__mutmut_4,
}


def reset_event_loops(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_event_loops__mutmut_orig, x_reset_event_loops__mutmut_mutants, args, kwargs
    )
    return result


reset_event_loops.__signature__ = _mutmut_signature(x_reset_event_loops__mutmut_orig)
x_reset_event_loops__mutmut_orig.__name__ = "x_reset_event_loops"


def reset_time_machine_state() -> None:
    """Reset time_machine state to ensure time is not frozen.

    NOTE: The actual cleanup is now handled by the _force_time_machine_cleanup
    fixture in tests/conftest.py, which runs BEFORE Foundation teardown.

    This ensures time patches are stopped before pytest-asyncio creates event loops
    for the next test. This function remains as a no-op safety fallback.
    """
    # Cleanup is now handled by conftest fixture which runs earlier
    pass


def reset_structlog_state() -> None:
    """Reset structlog configuration to defaults.

    This is the most fundamental reset - it clears all structlog
    configuration and returns it to an unconfigured state.
    """
    structlog.reset_defaults()


def x_reset_logger_state__mutmut_orig() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_1() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update(None)
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_2() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"XXdoneXX": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_3() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"DONE": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_4() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": True, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_5() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "XXerrorXX": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_6() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "ERROR": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_7() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "XXin_progressXX": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_8() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "IN_PROGRESS": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_9() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": True})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_10() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = None
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_11() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["XX_is_configured_by_setupXX"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_12() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_IS_CONFIGURED_BY_SETUP"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_13() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = True
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_14() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = ""
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_15() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["XX_active_configXX"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_16() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_ACTIVE_CONFIG"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_17() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = ""
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_18() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["XX_active_resolved_emoji_configXX"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def x_reset_logger_state__mutmut_19() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_ACTIVE_RESOLVED_EMOJI_CONFIG"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


x_reset_logger_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_logger_state__mutmut_1": x_reset_logger_state__mutmut_1,
    "x_reset_logger_state__mutmut_2": x_reset_logger_state__mutmut_2,
    "x_reset_logger_state__mutmut_3": x_reset_logger_state__mutmut_3,
    "x_reset_logger_state__mutmut_4": x_reset_logger_state__mutmut_4,
    "x_reset_logger_state__mutmut_5": x_reset_logger_state__mutmut_5,
    "x_reset_logger_state__mutmut_6": x_reset_logger_state__mutmut_6,
    "x_reset_logger_state__mutmut_7": x_reset_logger_state__mutmut_7,
    "x_reset_logger_state__mutmut_8": x_reset_logger_state__mutmut_8,
    "x_reset_logger_state__mutmut_9": x_reset_logger_state__mutmut_9,
    "x_reset_logger_state__mutmut_10": x_reset_logger_state__mutmut_10,
    "x_reset_logger_state__mutmut_11": x_reset_logger_state__mutmut_11,
    "x_reset_logger_state__mutmut_12": x_reset_logger_state__mutmut_12,
    "x_reset_logger_state__mutmut_13": x_reset_logger_state__mutmut_13,
    "x_reset_logger_state__mutmut_14": x_reset_logger_state__mutmut_14,
    "x_reset_logger_state__mutmut_15": x_reset_logger_state__mutmut_15,
    "x_reset_logger_state__mutmut_16": x_reset_logger_state__mutmut_16,
    "x_reset_logger_state__mutmut_17": x_reset_logger_state__mutmut_17,
    "x_reset_logger_state__mutmut_18": x_reset_logger_state__mutmut_18,
    "x_reset_logger_state__mutmut_19": x_reset_logger_state__mutmut_19,
}


def reset_logger_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_logger_state__mutmut_orig, x_reset_logger_state__mutmut_mutants, args, kwargs
    )
    return result


reset_logger_state.__signature__ = _mutmut_signature(x_reset_logger_state__mutmut_orig)
x_reset_logger_state__mutmut_orig.__name__ = "x_reset_logger_state"


def x_reset_hub_state__mutmut_orig() -> None:
    """Reset Hub state to defaults.

    This clears the Hub registry and resets all Hub components
    to their initial state.
    """
    global _hub_reset_in_progress

    # Prevent recursive resets that can trigger re-initialization
    if _hub_reset_in_progress:
        return

    _hub_reset_in_progress = True
    try:
        try:
            from provide.foundation.hub.manager import clear_hub

            clear_hub()
        except ImportError:
            # Hub module not available, skip
            pass

        try:
            # Also reset the initialized components cache
            from provide.foundation.hub.components import _initialized_components

            _initialized_components.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global component registry (where bootstrap_foundation registers components)
            from provide.foundation.hub.components import _component_registry

            _component_registry.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global command registry (where @register_command decorator registers commands)
            from provide.foundation.hub.registry import _command_registry

            _command_registry.clear()
        except ImportError:
            # Registry module not available, skip
            pass
    finally:
        _hub_reset_in_progress = False

    # NOTE: Event bus clearing removed - it was causing infinite recursion
    # during Foundation reinitialization. Event handlers use weak references
    # and will be garbage collected naturally. The event bus has built-in
    # "already registered" checks to prevent duplicate registrations.


def x_reset_hub_state__mutmut_1() -> None:
    """Reset Hub state to defaults.

    This clears the Hub registry and resets all Hub components
    to their initial state.
    """
    global _hub_reset_in_progress

    # Prevent recursive resets that can trigger re-initialization
    if _hub_reset_in_progress:
        return

    _hub_reset_in_progress = None
    try:
        try:
            from provide.foundation.hub.manager import clear_hub

            clear_hub()
        except ImportError:
            # Hub module not available, skip
            pass

        try:
            # Also reset the initialized components cache
            from provide.foundation.hub.components import _initialized_components

            _initialized_components.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global component registry (where bootstrap_foundation registers components)
            from provide.foundation.hub.components import _component_registry

            _component_registry.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global command registry (where @register_command decorator registers commands)
            from provide.foundation.hub.registry import _command_registry

            _command_registry.clear()
        except ImportError:
            # Registry module not available, skip
            pass
    finally:
        _hub_reset_in_progress = False

    # NOTE: Event bus clearing removed - it was causing infinite recursion
    # during Foundation reinitialization. Event handlers use weak references
    # and will be garbage collected naturally. The event bus has built-in
    # "already registered" checks to prevent duplicate registrations.


def x_reset_hub_state__mutmut_2() -> None:
    """Reset Hub state to defaults.

    This clears the Hub registry and resets all Hub components
    to their initial state.
    """
    global _hub_reset_in_progress

    # Prevent recursive resets that can trigger re-initialization
    if _hub_reset_in_progress:
        return

    _hub_reset_in_progress = False
    try:
        try:
            from provide.foundation.hub.manager import clear_hub

            clear_hub()
        except ImportError:
            # Hub module not available, skip
            pass

        try:
            # Also reset the initialized components cache
            from provide.foundation.hub.components import _initialized_components

            _initialized_components.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global component registry (where bootstrap_foundation registers components)
            from provide.foundation.hub.components import _component_registry

            _component_registry.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global command registry (where @register_command decorator registers commands)
            from provide.foundation.hub.registry import _command_registry

            _command_registry.clear()
        except ImportError:
            # Registry module not available, skip
            pass
    finally:
        _hub_reset_in_progress = False

    # NOTE: Event bus clearing removed - it was causing infinite recursion
    # during Foundation reinitialization. Event handlers use weak references
    # and will be garbage collected naturally. The event bus has built-in
    # "already registered" checks to prevent duplicate registrations.


def x_reset_hub_state__mutmut_3() -> None:
    """Reset Hub state to defaults.

    This clears the Hub registry and resets all Hub components
    to their initial state.
    """
    global _hub_reset_in_progress

    # Prevent recursive resets that can trigger re-initialization
    if _hub_reset_in_progress:
        return

    _hub_reset_in_progress = True
    try:
        try:
            from provide.foundation.hub.manager import clear_hub

            clear_hub()
        except ImportError:
            # Hub module not available, skip
            pass

        try:
            # Also reset the initialized components cache
            from provide.foundation.hub.components import _initialized_components

            _initialized_components.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global component registry (where bootstrap_foundation registers components)
            from provide.foundation.hub.components import _component_registry

            _component_registry.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global command registry (where @register_command decorator registers commands)
            from provide.foundation.hub.registry import _command_registry

            _command_registry.clear()
        except ImportError:
            # Registry module not available, skip
            pass
    finally:
        _hub_reset_in_progress = None

    # NOTE: Event bus clearing removed - it was causing infinite recursion
    # during Foundation reinitialization. Event handlers use weak references
    # and will be garbage collected naturally. The event bus has built-in
    # "already registered" checks to prevent duplicate registrations.


def x_reset_hub_state__mutmut_4() -> None:
    """Reset Hub state to defaults.

    This clears the Hub registry and resets all Hub components
    to their initial state.
    """
    global _hub_reset_in_progress

    # Prevent recursive resets that can trigger re-initialization
    if _hub_reset_in_progress:
        return

    _hub_reset_in_progress = True
    try:
        try:
            from provide.foundation.hub.manager import clear_hub

            clear_hub()
        except ImportError:
            # Hub module not available, skip
            pass

        try:
            # Also reset the initialized components cache
            from provide.foundation.hub.components import _initialized_components

            _initialized_components.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global component registry (where bootstrap_foundation registers components)
            from provide.foundation.hub.components import _component_registry

            _component_registry.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global command registry (where @register_command decorator registers commands)
            from provide.foundation.hub.registry import _command_registry

            _command_registry.clear()
        except ImportError:
            # Registry module not available, skip
            pass
    finally:
        _hub_reset_in_progress = True

    # NOTE: Event bus clearing removed - it was causing infinite recursion
    # during Foundation reinitialization. Event handlers use weak references
    # and will be garbage collected naturally. The event bus has built-in
    # "already registered" checks to prevent duplicate registrations.


x_reset_hub_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_hub_state__mutmut_1": x_reset_hub_state__mutmut_1,
    "x_reset_hub_state__mutmut_2": x_reset_hub_state__mutmut_2,
    "x_reset_hub_state__mutmut_3": x_reset_hub_state__mutmut_3,
    "x_reset_hub_state__mutmut_4": x_reset_hub_state__mutmut_4,
}


def reset_hub_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_hub_state__mutmut_orig, x_reset_hub_state__mutmut_mutants, args, kwargs
    )
    return result


reset_hub_state.__signature__ = _mutmut_signature(x_reset_hub_state__mutmut_orig)
x_reset_hub_state__mutmut_orig.__name__ = "x_reset_hub_state"


def reset_streams_state() -> None:
    """Reset stream state to defaults.

    This resets file streams and other stream-related state
    managed by the streams module.
    """
    try:
        from provide.foundation.streams.file import reset_streams

        reset_streams()
    except ImportError:
        # Streams module not available, skip
        pass


def x_reset_transport_registration_flags__mutmut_orig() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_1() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "XXprovide.foundation.transport.httpXX" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_2() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "PROVIDE.FOUNDATION.TRANSPORT.HTTP" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_3() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" not in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_4() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = None
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_5() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["XXprovide.foundation.transport.httpXX"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_6() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["PROVIDE.FOUNDATION.TRANSPORT.HTTP"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_7() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(None, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_8() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, None):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_9() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr("_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_10() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(
                http_module,
            ):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_11() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "XX_http_transport_registeredXX"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_12() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "_HTTP_TRANSPORT_REGISTERED"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_13() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = None  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def x_reset_transport_registration_flags__mutmut_14() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = True  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


x_reset_transport_registration_flags__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_transport_registration_flags__mutmut_1": x_reset_transport_registration_flags__mutmut_1,
    "x_reset_transport_registration_flags__mutmut_2": x_reset_transport_registration_flags__mutmut_2,
    "x_reset_transport_registration_flags__mutmut_3": x_reset_transport_registration_flags__mutmut_3,
    "x_reset_transport_registration_flags__mutmut_4": x_reset_transport_registration_flags__mutmut_4,
    "x_reset_transport_registration_flags__mutmut_5": x_reset_transport_registration_flags__mutmut_5,
    "x_reset_transport_registration_flags__mutmut_6": x_reset_transport_registration_flags__mutmut_6,
    "x_reset_transport_registration_flags__mutmut_7": x_reset_transport_registration_flags__mutmut_7,
    "x_reset_transport_registration_flags__mutmut_8": x_reset_transport_registration_flags__mutmut_8,
    "x_reset_transport_registration_flags__mutmut_9": x_reset_transport_registration_flags__mutmut_9,
    "x_reset_transport_registration_flags__mutmut_10": x_reset_transport_registration_flags__mutmut_10,
    "x_reset_transport_registration_flags__mutmut_11": x_reset_transport_registration_flags__mutmut_11,
    "x_reset_transport_registration_flags__mutmut_12": x_reset_transport_registration_flags__mutmut_12,
    "x_reset_transport_registration_flags__mutmut_13": x_reset_transport_registration_flags__mutmut_13,
    "x_reset_transport_registration_flags__mutmut_14": x_reset_transport_registration_flags__mutmut_14,
}


def reset_transport_registration_flags(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_transport_registration_flags__mutmut_orig,
        x_reset_transport_registration_flags__mutmut_mutants,
        args,
        kwargs,
    )
    return result


reset_transport_registration_flags.__signature__ = _mutmut_signature(
    x_reset_transport_registration_flags__mutmut_orig
)
x_reset_transport_registration_flags__mutmut_orig.__name__ = "x_reset_transport_registration_flags"


def x_reset_eventsets_state__mutmut_orig() -> None:
    """Reset event set registry and discovery state.

    This clears the event set registry to ensure clean state
    between tests.
    """
    global _eventsets_reset_in_progress

    # Prevent recursive resets that trigger event processor initialization
    if _eventsets_reset_in_progress:
        return

    _eventsets_reset_in_progress = True
    try:
        from provide.foundation.eventsets.registry import clear_registry

        clear_registry()
    except ImportError:
        # Event sets may not be available in all test environments
        pass
    finally:
        _eventsets_reset_in_progress = False


def x_reset_eventsets_state__mutmut_1() -> None:
    """Reset event set registry and discovery state.

    This clears the event set registry to ensure clean state
    between tests.
    """
    global _eventsets_reset_in_progress

    # Prevent recursive resets that trigger event processor initialization
    if _eventsets_reset_in_progress:
        return

    _eventsets_reset_in_progress = None
    try:
        from provide.foundation.eventsets.registry import clear_registry

        clear_registry()
    except ImportError:
        # Event sets may not be available in all test environments
        pass
    finally:
        _eventsets_reset_in_progress = False


def x_reset_eventsets_state__mutmut_2() -> None:
    """Reset event set registry and discovery state.

    This clears the event set registry to ensure clean state
    between tests.
    """
    global _eventsets_reset_in_progress

    # Prevent recursive resets that trigger event processor initialization
    if _eventsets_reset_in_progress:
        return

    _eventsets_reset_in_progress = False
    try:
        from provide.foundation.eventsets.registry import clear_registry

        clear_registry()
    except ImportError:
        # Event sets may not be available in all test environments
        pass
    finally:
        _eventsets_reset_in_progress = False


def x_reset_eventsets_state__mutmut_3() -> None:
    """Reset event set registry and discovery state.

    This clears the event set registry to ensure clean state
    between tests.
    """
    global _eventsets_reset_in_progress

    # Prevent recursive resets that trigger event processor initialization
    if _eventsets_reset_in_progress:
        return

    _eventsets_reset_in_progress = True
    try:
        from provide.foundation.eventsets.registry import clear_registry

        clear_registry()
    except ImportError:
        # Event sets may not be available in all test environments
        pass
    finally:
        _eventsets_reset_in_progress = None


def x_reset_eventsets_state__mutmut_4() -> None:
    """Reset event set registry and discovery state.

    This clears the event set registry to ensure clean state
    between tests.
    """
    global _eventsets_reset_in_progress

    # Prevent recursive resets that trigger event processor initialization
    if _eventsets_reset_in_progress:
        return

    _eventsets_reset_in_progress = True
    try:
        from provide.foundation.eventsets.registry import clear_registry

        clear_registry()
    except ImportError:
        # Event sets may not be available in all test environments
        pass
    finally:
        _eventsets_reset_in_progress = True


x_reset_eventsets_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_eventsets_state__mutmut_1": x_reset_eventsets_state__mutmut_1,
    "x_reset_eventsets_state__mutmut_2": x_reset_eventsets_state__mutmut_2,
    "x_reset_eventsets_state__mutmut_3": x_reset_eventsets_state__mutmut_3,
    "x_reset_eventsets_state__mutmut_4": x_reset_eventsets_state__mutmut_4,
}


def reset_eventsets_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_eventsets_state__mutmut_orig, x_reset_eventsets_state__mutmut_mutants, args, kwargs
    )
    return result


reset_eventsets_state.__signature__ = _mutmut_signature(x_reset_eventsets_state__mutmut_orig)
x_reset_eventsets_state__mutmut_orig.__name__ = "x_reset_eventsets_state"


def reset_coordinator_state() -> None:
    """Reset setup coordinator state.

    This clears cached coordinator state including setup logger
    cache and other coordinator-managed state.
    """
    try:
        from provide.foundation.logger.setup.coordinator import reset_coordinator_state

        reset_coordinator_state()
    except ImportError:
        # Coordinator module not available, skip
        pass

    try:
        from provide.foundation.logger.setup.coordinator import reset_setup_logger_cache

        reset_setup_logger_cache()
    except ImportError:
        # Setup logger cache not available, skip
        pass


def x_reset_profiling_state__mutmut_orig() -> None:
    """Reset profiling state to defaults.

    This clears profiling metrics and resets profiling components
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        profiler = hub.get_component("profiler")
        if profiler:
            profiler.reset()
    except ImportError:
        # Profiling module or Hub not available, skip
        pass


def x_reset_profiling_state__mutmut_1() -> None:
    """Reset profiling state to defaults.

    This clears profiling metrics and resets profiling components
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = None
        profiler = hub.get_component("profiler")
        if profiler:
            profiler.reset()
    except ImportError:
        # Profiling module or Hub not available, skip
        pass


def x_reset_profiling_state__mutmut_2() -> None:
    """Reset profiling state to defaults.

    This clears profiling metrics and resets profiling components
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        profiler = None
        if profiler:
            profiler.reset()
    except ImportError:
        # Profiling module or Hub not available, skip
        pass


def x_reset_profiling_state__mutmut_3() -> None:
    """Reset profiling state to defaults.

    This clears profiling metrics and resets profiling components
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        profiler = hub.get_component(None)
        if profiler:
            profiler.reset()
    except ImportError:
        # Profiling module or Hub not available, skip
        pass


def x_reset_profiling_state__mutmut_4() -> None:
    """Reset profiling state to defaults.

    This clears profiling metrics and resets profiling components
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        profiler = hub.get_component("XXprofilerXX")
        if profiler:
            profiler.reset()
    except ImportError:
        # Profiling module or Hub not available, skip
        pass


def x_reset_profiling_state__mutmut_5() -> None:
    """Reset profiling state to defaults.

    This clears profiling metrics and resets profiling components
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        profiler = hub.get_component("PROFILER")
        if profiler:
            profiler.reset()
    except ImportError:
        # Profiling module or Hub not available, skip
        pass


x_reset_profiling_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_profiling_state__mutmut_1": x_reset_profiling_state__mutmut_1,
    "x_reset_profiling_state__mutmut_2": x_reset_profiling_state__mutmut_2,
    "x_reset_profiling_state__mutmut_3": x_reset_profiling_state__mutmut_3,
    "x_reset_profiling_state__mutmut_4": x_reset_profiling_state__mutmut_4,
    "x_reset_profiling_state__mutmut_5": x_reset_profiling_state__mutmut_5,
}


def reset_profiling_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_profiling_state__mutmut_orig, x_reset_profiling_state__mutmut_mutants, args, kwargs
    )
    return result


reset_profiling_state.__signature__ = _mutmut_signature(x_reset_profiling_state__mutmut_orig)
x_reset_profiling_state__mutmut_orig.__name__ = "x_reset_profiling_state"


def reset_global_coordinator() -> None:
    """Reset the global initialization coordinator state for testing.

    This function resets the singleton InitializationCoordinator state
    to ensure proper test isolation between test runs.

    WARNING: This should only be called from test code or test fixtures.
    Production code should not reset the global coordinator state.
    """
    try:
        from provide.foundation.hub.initialization import _coordinator

        _coordinator.reset_state()
    except ImportError:
        # Initialization module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_orig() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_1() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = None

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_2() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = None
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_3() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["XXcircuit_breakerXX", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_4() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["CIRCUIT_BREAKER", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_5() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "XXcircuit_breaker_testXX"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_6() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "CIRCUIT_BREAKER_TEST"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_7() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(None):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_8() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = None
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_9() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(None, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_10() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=None)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_11() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_12() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(
                    name,
                )
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_13() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(None)

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_14() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(None))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_15() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = None
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_16() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 1
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_17() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                or id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_18() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(None) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_19() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker)) and id(obj) in decorator_tracked_ids:
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_20() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_21() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found = 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_22() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found -= 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_23() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 2
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_24() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found >= 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def x__reset_direct_circuit_breaker_instances__mutmut_25() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 1:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


x__reset_direct_circuit_breaker_instances__mutmut_mutants: ClassVar[MutantDict] = {
    "x__reset_direct_circuit_breaker_instances__mutmut_1": x__reset_direct_circuit_breaker_instances__mutmut_1,
    "x__reset_direct_circuit_breaker_instances__mutmut_2": x__reset_direct_circuit_breaker_instances__mutmut_2,
    "x__reset_direct_circuit_breaker_instances__mutmut_3": x__reset_direct_circuit_breaker_instances__mutmut_3,
    "x__reset_direct_circuit_breaker_instances__mutmut_4": x__reset_direct_circuit_breaker_instances__mutmut_4,
    "x__reset_direct_circuit_breaker_instances__mutmut_5": x__reset_direct_circuit_breaker_instances__mutmut_5,
    "x__reset_direct_circuit_breaker_instances__mutmut_6": x__reset_direct_circuit_breaker_instances__mutmut_6,
    "x__reset_direct_circuit_breaker_instances__mutmut_7": x__reset_direct_circuit_breaker_instances__mutmut_7,
    "x__reset_direct_circuit_breaker_instances__mutmut_8": x__reset_direct_circuit_breaker_instances__mutmut_8,
    "x__reset_direct_circuit_breaker_instances__mutmut_9": x__reset_direct_circuit_breaker_instances__mutmut_9,
    "x__reset_direct_circuit_breaker_instances__mutmut_10": x__reset_direct_circuit_breaker_instances__mutmut_10,
    "x__reset_direct_circuit_breaker_instances__mutmut_11": x__reset_direct_circuit_breaker_instances__mutmut_11,
    "x__reset_direct_circuit_breaker_instances__mutmut_12": x__reset_direct_circuit_breaker_instances__mutmut_12,
    "x__reset_direct_circuit_breaker_instances__mutmut_13": x__reset_direct_circuit_breaker_instances__mutmut_13,
    "x__reset_direct_circuit_breaker_instances__mutmut_14": x__reset_direct_circuit_breaker_instances__mutmut_14,
    "x__reset_direct_circuit_breaker_instances__mutmut_15": x__reset_direct_circuit_breaker_instances__mutmut_15,
    "x__reset_direct_circuit_breaker_instances__mutmut_16": x__reset_direct_circuit_breaker_instances__mutmut_16,
    "x__reset_direct_circuit_breaker_instances__mutmut_17": x__reset_direct_circuit_breaker_instances__mutmut_17,
    "x__reset_direct_circuit_breaker_instances__mutmut_18": x__reset_direct_circuit_breaker_instances__mutmut_18,
    "x__reset_direct_circuit_breaker_instances__mutmut_19": x__reset_direct_circuit_breaker_instances__mutmut_19,
    "x__reset_direct_circuit_breaker_instances__mutmut_20": x__reset_direct_circuit_breaker_instances__mutmut_20,
    "x__reset_direct_circuit_breaker_instances__mutmut_21": x__reset_direct_circuit_breaker_instances__mutmut_21,
    "x__reset_direct_circuit_breaker_instances__mutmut_22": x__reset_direct_circuit_breaker_instances__mutmut_22,
    "x__reset_direct_circuit_breaker_instances__mutmut_23": x__reset_direct_circuit_breaker_instances__mutmut_23,
    "x__reset_direct_circuit_breaker_instances__mutmut_24": x__reset_direct_circuit_breaker_instances__mutmut_24,
    "x__reset_direct_circuit_breaker_instances__mutmut_25": x__reset_direct_circuit_breaker_instances__mutmut_25,
}


def _reset_direct_circuit_breaker_instances(*args, **kwargs):
    result = _mutmut_trampoline(
        x__reset_direct_circuit_breaker_instances__mutmut_orig,
        x__reset_direct_circuit_breaker_instances__mutmut_mutants,
        args,
        kwargs,
    )
    return result


_reset_direct_circuit_breaker_instances.__signature__ = _mutmut_signature(
    x__reset_direct_circuit_breaker_instances__mutmut_orig
)
x__reset_direct_circuit_breaker_instances__mutmut_orig.__name__ = "x__reset_direct_circuit_breaker_instances"


def x_reset_circuit_breaker_state__mutmut_orig() -> None:
    """Reset all circuit breaker instances to ensure test isolation.

    This function resets all circuit breaker instances that were created
    by the @circuit_breaker decorator and direct instantiation to ensure
    their state doesn't leak between tests.
    """
    # Reset all CircuitBreaker instances created directly (not via decorator)
    # Do this FIRST to catch all instances before decorator reset
    _reset_direct_circuit_breaker_instances()

    try:
        import asyncio

        from provide.foundation.resilience.decorators import (
            reset_circuit_breakers_for_testing,
            reset_test_circuit_breakers,
        )

        # Reset both production and test circuit breakers
        # These are now async functions, so we need to run them in an event loop

        # Check if we're in an async context (running event loop)
        try:
            asyncio.get_running_loop()
            # We're in an async context - skip reset to avoid blocking
            # This shouldn't happen in practice since reset is called from sync fixtures
            return
        except RuntimeError:
            # No running loop - we're in sync context, safe to proceed
            pass

        # Use asyncio.run() to create fresh event loop for each call
        # This is more reliable than trying to reuse get_event_loop()
        asyncio.run(reset_circuit_breakers_for_testing())
        asyncio.run(reset_test_circuit_breakers())
    except ImportError:
        # Resilience decorators module not available, skip
        pass


def x_reset_circuit_breaker_state__mutmut_1() -> None:
    """Reset all circuit breaker instances to ensure test isolation.

    This function resets all circuit breaker instances that were created
    by the @circuit_breaker decorator and direct instantiation to ensure
    their state doesn't leak between tests.
    """
    # Reset all CircuitBreaker instances created directly (not via decorator)
    # Do this FIRST to catch all instances before decorator reset
    _reset_direct_circuit_breaker_instances()

    try:
        import asyncio

        from provide.foundation.resilience.decorators import (
            reset_circuit_breakers_for_testing,
            reset_test_circuit_breakers,
        )

        # Reset both production and test circuit breakers
        # These are now async functions, so we need to run them in an event loop

        # Check if we're in an async context (running event loop)
        try:
            asyncio.get_running_loop()
            # We're in an async context - skip reset to avoid blocking
            # This shouldn't happen in practice since reset is called from sync fixtures
            return
        except RuntimeError:
            # No running loop - we're in sync context, safe to proceed
            pass

        # Use asyncio.run() to create fresh event loop for each call
        # This is more reliable than trying to reuse get_event_loop()
        asyncio.run(None)
        asyncio.run(reset_test_circuit_breakers())
    except ImportError:
        # Resilience decorators module not available, skip
        pass


def x_reset_circuit_breaker_state__mutmut_2() -> None:
    """Reset all circuit breaker instances to ensure test isolation.

    This function resets all circuit breaker instances that were created
    by the @circuit_breaker decorator and direct instantiation to ensure
    their state doesn't leak between tests.
    """
    # Reset all CircuitBreaker instances created directly (not via decorator)
    # Do this FIRST to catch all instances before decorator reset
    _reset_direct_circuit_breaker_instances()

    try:
        import asyncio

        from provide.foundation.resilience.decorators import (
            reset_circuit_breakers_for_testing,
            reset_test_circuit_breakers,
        )

        # Reset both production and test circuit breakers
        # These are now async functions, so we need to run them in an event loop

        # Check if we're in an async context (running event loop)
        try:
            asyncio.get_running_loop()
            # We're in an async context - skip reset to avoid blocking
            # This shouldn't happen in practice since reset is called from sync fixtures
            return
        except RuntimeError:
            # No running loop - we're in sync context, safe to proceed
            pass

        # Use asyncio.run() to create fresh event loop for each call
        # This is more reliable than trying to reuse get_event_loop()
        asyncio.run(reset_circuit_breakers_for_testing())
        asyncio.run(None)
    except ImportError:
        # Resilience decorators module not available, skip
        pass


x_reset_circuit_breaker_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_circuit_breaker_state__mutmut_1": x_reset_circuit_breaker_state__mutmut_1,
    "x_reset_circuit_breaker_state__mutmut_2": x_reset_circuit_breaker_state__mutmut_2,
}


def reset_circuit_breaker_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_circuit_breaker_state__mutmut_orig, x_reset_circuit_breaker_state__mutmut_mutants, args, kwargs
    )
    return result


reset_circuit_breaker_state.__signature__ = _mutmut_signature(x_reset_circuit_breaker_state__mutmut_orig)
x_reset_circuit_breaker_state__mutmut_orig.__name__ = "x_reset_circuit_breaker_state"


def x_reset_state_managers__mutmut_orig() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr(logger_state_manager, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_1() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = None

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr(logger_state_manager, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_2() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = None
            if logger_state_manager and hasattr(logger_state_manager, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_3() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component(None)
            if logger_state_manager and hasattr(logger_state_manager, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_4() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("XXlogger_state_managerXX")
            if logger_state_manager and hasattr(logger_state_manager, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_5() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("LOGGER_STATE_MANAGER")
            if logger_state_manager and hasattr(logger_state_manager, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_6() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager or hasattr(logger_state_manager, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_7() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr(None, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_8() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr(logger_state_manager, None):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_9() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr("reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_10() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr(
                logger_state_manager,
            ):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_11() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr(logger_state_manager, "XXreset_to_defaultXX"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_state_managers__mutmut_12() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr(logger_state_manager, "RESET_TO_DEFAULT"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


x_reset_state_managers__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_state_managers__mutmut_1": x_reset_state_managers__mutmut_1,
    "x_reset_state_managers__mutmut_2": x_reset_state_managers__mutmut_2,
    "x_reset_state_managers__mutmut_3": x_reset_state_managers__mutmut_3,
    "x_reset_state_managers__mutmut_4": x_reset_state_managers__mutmut_4,
    "x_reset_state_managers__mutmut_5": x_reset_state_managers__mutmut_5,
    "x_reset_state_managers__mutmut_6": x_reset_state_managers__mutmut_6,
    "x_reset_state_managers__mutmut_7": x_reset_state_managers__mutmut_7,
    "x_reset_state_managers__mutmut_8": x_reset_state_managers__mutmut_8,
    "x_reset_state_managers__mutmut_9": x_reset_state_managers__mutmut_9,
    "x_reset_state_managers__mutmut_10": x_reset_state_managers__mutmut_10,
    "x_reset_state_managers__mutmut_11": x_reset_state_managers__mutmut_11,
    "x_reset_state_managers__mutmut_12": x_reset_state_managers__mutmut_12,
}


def reset_state_managers(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_state_managers__mutmut_orig, x_reset_state_managers__mutmut_mutants, args, kwargs
    )
    return result


reset_state_managers.__signature__ = _mutmut_signature(x_reset_state_managers__mutmut_orig)
x_reset_state_managers__mutmut_orig.__name__ = "x_reset_state_managers"


def x_reset_configuration_state__mutmut_orig() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr(config_manager, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_1() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = None

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr(config_manager, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_2() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = None
            if config_manager and hasattr(config_manager, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_3() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component(None)
            if config_manager and hasattr(config_manager, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_4() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("XXconfig_managerXX")
            if config_manager and hasattr(config_manager, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_5() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("CONFIG_MANAGER")
            if config_manager and hasattr(config_manager, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_6() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager or hasattr(config_manager, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_7() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr(None, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_8() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr(config_manager, None):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_9() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr("clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_10() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr(
                config_manager,
            ):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_11() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr(config_manager, "XXclear_allXX"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def x_reset_configuration_state__mutmut_12() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr(config_manager, "CLEAR_ALL"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


x_reset_configuration_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_configuration_state__mutmut_1": x_reset_configuration_state__mutmut_1,
    "x_reset_configuration_state__mutmut_2": x_reset_configuration_state__mutmut_2,
    "x_reset_configuration_state__mutmut_3": x_reset_configuration_state__mutmut_3,
    "x_reset_configuration_state__mutmut_4": x_reset_configuration_state__mutmut_4,
    "x_reset_configuration_state__mutmut_5": x_reset_configuration_state__mutmut_5,
    "x_reset_configuration_state__mutmut_6": x_reset_configuration_state__mutmut_6,
    "x_reset_configuration_state__mutmut_7": x_reset_configuration_state__mutmut_7,
    "x_reset_configuration_state__mutmut_8": x_reset_configuration_state__mutmut_8,
    "x_reset_configuration_state__mutmut_9": x_reset_configuration_state__mutmut_9,
    "x_reset_configuration_state__mutmut_10": x_reset_configuration_state__mutmut_10,
    "x_reset_configuration_state__mutmut_11": x_reset_configuration_state__mutmut_11,
    "x_reset_configuration_state__mutmut_12": x_reset_configuration_state__mutmut_12,
}


def reset_configuration_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_configuration_state__mutmut_orig, x_reset_configuration_state__mutmut_mutants, args, kwargs
    )
    return result


reset_configuration_state.__signature__ = _mutmut_signature(x_reset_configuration_state__mutmut_orig)
x_reset_configuration_state__mutmut_orig.__name__ = "x_reset_configuration_state"


def reset_version_cache() -> None:
    """Reset version cache to defaults.

    This clears the cached version to ensure clean state
    between tests, allowing each test to verify different
    version resolution scenarios.
    """
    try:
        from provide.foundation._version import (  # type: ignore[import-untyped]
            reset_version_cache as _reset_cache,
        )

        _reset_cache()
    except ImportError:
        # Version module not available, skip
        pass


# <3 🧱🤝🧪🪄
