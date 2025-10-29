# provide/foundation/cli/shutdown.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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


def _flush_otlp_logs() -> None:
    """Flush OTLP logs if available."""
    try:
        from provide.foundation.logger.processors.otlp import flush_otlp_logs

        flush_otlp_logs()
    except ImportError:
        pass


def x__cleanup_foundation_resources__mutmut_orig() -> None:
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


def x__cleanup_foundation_resources__mutmut_1() -> None:
    """Clean up all Foundation resources.

    This is the central cleanup function called on exit, interrupt, or error.
    It ensures all resources are properly cleaned up exactly once.
    Automatically restores original signal handlers.
    """
    global _cleanup_executed

    if _cleanup_executed:
        return

    _cleanup_executed = None

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


def x__cleanup_foundation_resources__mutmut_2() -> None:
    """Clean up all Foundation resources.

    This is the central cleanup function called on exit, interrupt, or error.
    It ensures all resources are properly cleaned up exactly once.
    Automatically restores original signal handlers.
    """
    global _cleanup_executed

    if _cleanup_executed:
        return

    _cleanup_executed = False

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


def x__cleanup_foundation_resources__mutmut_3() -> None:
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
            log.error(None, error=str(e))
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def x__cleanup_foundation_resources__mutmut_4() -> None:
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
            log.error("Error during cleanup", error=None)
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def x__cleanup_foundation_resources__mutmut_5() -> None:
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
            log.error(error=str(e))
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def x__cleanup_foundation_resources__mutmut_6() -> None:
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
            log.error(
                "Error during cleanup",
            )
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def x__cleanup_foundation_resources__mutmut_7() -> None:
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
            log.error("XXError during cleanupXX", error=str(e))
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def x__cleanup_foundation_resources__mutmut_8() -> None:
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
            log.error("error during cleanup", error=str(e))
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def x__cleanup_foundation_resources__mutmut_9() -> None:
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
            log.error("ERROR DURING CLEANUP", error=str(e))
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def x__cleanup_foundation_resources__mutmut_10() -> None:
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
            log.error("Error during cleanup", error=str(None))
        except Exception:
            # If logging fails, use Foundation's console output as last resort
            perr(f"Error during cleanup: {e}")


def x__cleanup_foundation_resources__mutmut_11() -> None:
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
            perr(None)


x__cleanup_foundation_resources__mutmut_mutants: ClassVar[MutantDict] = {
    "x__cleanup_foundation_resources__mutmut_1": x__cleanup_foundation_resources__mutmut_1,
    "x__cleanup_foundation_resources__mutmut_2": x__cleanup_foundation_resources__mutmut_2,
    "x__cleanup_foundation_resources__mutmut_3": x__cleanup_foundation_resources__mutmut_3,
    "x__cleanup_foundation_resources__mutmut_4": x__cleanup_foundation_resources__mutmut_4,
    "x__cleanup_foundation_resources__mutmut_5": x__cleanup_foundation_resources__mutmut_5,
    "x__cleanup_foundation_resources__mutmut_6": x__cleanup_foundation_resources__mutmut_6,
    "x__cleanup_foundation_resources__mutmut_7": x__cleanup_foundation_resources__mutmut_7,
    "x__cleanup_foundation_resources__mutmut_8": x__cleanup_foundation_resources__mutmut_8,
    "x__cleanup_foundation_resources__mutmut_9": x__cleanup_foundation_resources__mutmut_9,
    "x__cleanup_foundation_resources__mutmut_10": x__cleanup_foundation_resources__mutmut_10,
    "x__cleanup_foundation_resources__mutmut_11": x__cleanup_foundation_resources__mutmut_11,
}


def _cleanup_foundation_resources(*args, **kwargs):
    result = _mutmut_trampoline(
        x__cleanup_foundation_resources__mutmut_orig,
        x__cleanup_foundation_resources__mutmut_mutants,
        args,
        kwargs,
    )
    return result


_cleanup_foundation_resources.__signature__ = _mutmut_signature(x__cleanup_foundation_resources__mutmut_orig)
x__cleanup_foundation_resources__mutmut_orig.__name__ = "x__cleanup_foundation_resources"


def x__signal_handler__mutmut_orig(signum: int, frame: Any) -> None:
    """Handle interrupt signals (SIGINT, SIGTERM).

    Args:
        signum: Signal number
        frame: Current stack frame

    """
    signal_name = signal.Signals(signum).name
    log.info(f"Received {signal_name}, cleaning up...")

    # Run cleanup
    _cleanup_foundation_resources()

    # Exit with appropriate code
    sys.exit(EXIT_SIGINT if signum == signal.SIGINT else 1)


def x__signal_handler__mutmut_1(signum: int, frame: Any) -> None:
    """Handle interrupt signals (SIGINT, SIGTERM).

    Args:
        signum: Signal number
        frame: Current stack frame

    """
    signal_name = None
    log.info(f"Received {signal_name}, cleaning up...")

    # Run cleanup
    _cleanup_foundation_resources()

    # Exit with appropriate code
    sys.exit(EXIT_SIGINT if signum == signal.SIGINT else 1)


def x__signal_handler__mutmut_2(signum: int, frame: Any) -> None:
    """Handle interrupt signals (SIGINT, SIGTERM).

    Args:
        signum: Signal number
        frame: Current stack frame

    """
    signal_name = signal.Signals(None).name
    log.info(f"Received {signal_name}, cleaning up...")

    # Run cleanup
    _cleanup_foundation_resources()

    # Exit with appropriate code
    sys.exit(EXIT_SIGINT if signum == signal.SIGINT else 1)


def x__signal_handler__mutmut_3(signum: int, frame: Any) -> None:
    """Handle interrupt signals (SIGINT, SIGTERM).

    Args:
        signum: Signal number
        frame: Current stack frame

    """
    signal_name = signal.Signals(signum).name
    log.info(None)

    # Run cleanup
    _cleanup_foundation_resources()

    # Exit with appropriate code
    sys.exit(EXIT_SIGINT if signum == signal.SIGINT else 1)


def x__signal_handler__mutmut_4(signum: int, frame: Any) -> None:
    """Handle interrupt signals (SIGINT, SIGTERM).

    Args:
        signum: Signal number
        frame: Current stack frame

    """
    signal_name = signal.Signals(signum).name
    log.info(f"Received {signal_name}, cleaning up...")

    # Run cleanup
    _cleanup_foundation_resources()

    # Exit with appropriate code
    sys.exit(None)


def x__signal_handler__mutmut_5(signum: int, frame: Any) -> None:
    """Handle interrupt signals (SIGINT, SIGTERM).

    Args:
        signum: Signal number
        frame: Current stack frame

    """
    signal_name = signal.Signals(signum).name
    log.info(f"Received {signal_name}, cleaning up...")

    # Run cleanup
    _cleanup_foundation_resources()

    # Exit with appropriate code
    sys.exit(EXIT_SIGINT if signum != signal.SIGINT else 1)


def x__signal_handler__mutmut_6(signum: int, frame: Any) -> None:
    """Handle interrupt signals (SIGINT, SIGTERM).

    Args:
        signum: Signal number
        frame: Current stack frame

    """
    signal_name = signal.Signals(signum).name
    log.info(f"Received {signal_name}, cleaning up...")

    # Run cleanup
    _cleanup_foundation_resources()

    # Exit with appropriate code
    sys.exit(EXIT_SIGINT if signum == signal.SIGINT else 2)


x__signal_handler__mutmut_mutants: ClassVar[MutantDict] = {
    "x__signal_handler__mutmut_1": x__signal_handler__mutmut_1,
    "x__signal_handler__mutmut_2": x__signal_handler__mutmut_2,
    "x__signal_handler__mutmut_3": x__signal_handler__mutmut_3,
    "x__signal_handler__mutmut_4": x__signal_handler__mutmut_4,
    "x__signal_handler__mutmut_5": x__signal_handler__mutmut_5,
    "x__signal_handler__mutmut_6": x__signal_handler__mutmut_6,
}


def _signal_handler(*args, **kwargs):
    result = _mutmut_trampoline(
        x__signal_handler__mutmut_orig, x__signal_handler__mutmut_mutants, args, kwargs
    )
    return result


_signal_handler.__signature__ = _mutmut_signature(x__signal_handler__mutmut_orig)
x__signal_handler__mutmut_orig.__name__ = "x__signal_handler"


def x__restore_signal_handlers__mutmut_orig() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_1() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_2() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_3() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(None, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_4() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, None)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_5() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(_original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_6() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(
            signal.SIGINT,
        )

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_7() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_8() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(None, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_9() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, None)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_10() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(_original_sigterm_handler)

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_11() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(
            signal.SIGTERM,
        )

    _handlers_registered = False
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_12() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = None
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_13() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = True
    log.trace("Restored original signal handlers")


def x__restore_signal_handlers__mutmut_14() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace(None)


def x__restore_signal_handlers__mutmut_15() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("XXRestored original signal handlersXX")


def x__restore_signal_handlers__mutmut_16() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("restored original signal handlers")


def x__restore_signal_handlers__mutmut_17() -> None:
    """Restore original signal handlers.

    This is called automatically during cleanup to ensure we don't
    leave Foundation's handlers active when we shouldn't.
    """
    global _handlers_registered

    if not _handlers_registered:
        return

    if _original_sigint_handler is not None:
        signal.signal(signal.SIGINT, _original_sigint_handler)

    if _original_sigterm_handler is not None:
        signal.signal(signal.SIGTERM, _original_sigterm_handler)

    _handlers_registered = False
    log.trace("RESTORED ORIGINAL SIGNAL HANDLERS")


x__restore_signal_handlers__mutmut_mutants: ClassVar[MutantDict] = {
    "x__restore_signal_handlers__mutmut_1": x__restore_signal_handlers__mutmut_1,
    "x__restore_signal_handlers__mutmut_2": x__restore_signal_handlers__mutmut_2,
    "x__restore_signal_handlers__mutmut_3": x__restore_signal_handlers__mutmut_3,
    "x__restore_signal_handlers__mutmut_4": x__restore_signal_handlers__mutmut_4,
    "x__restore_signal_handlers__mutmut_5": x__restore_signal_handlers__mutmut_5,
    "x__restore_signal_handlers__mutmut_6": x__restore_signal_handlers__mutmut_6,
    "x__restore_signal_handlers__mutmut_7": x__restore_signal_handlers__mutmut_7,
    "x__restore_signal_handlers__mutmut_8": x__restore_signal_handlers__mutmut_8,
    "x__restore_signal_handlers__mutmut_9": x__restore_signal_handlers__mutmut_9,
    "x__restore_signal_handlers__mutmut_10": x__restore_signal_handlers__mutmut_10,
    "x__restore_signal_handlers__mutmut_11": x__restore_signal_handlers__mutmut_11,
    "x__restore_signal_handlers__mutmut_12": x__restore_signal_handlers__mutmut_12,
    "x__restore_signal_handlers__mutmut_13": x__restore_signal_handlers__mutmut_13,
    "x__restore_signal_handlers__mutmut_14": x__restore_signal_handlers__mutmut_14,
    "x__restore_signal_handlers__mutmut_15": x__restore_signal_handlers__mutmut_15,
    "x__restore_signal_handlers__mutmut_16": x__restore_signal_handlers__mutmut_16,
    "x__restore_signal_handlers__mutmut_17": x__restore_signal_handlers__mutmut_17,
}


def _restore_signal_handlers(*args, **kwargs):
    result = _mutmut_trampoline(
        x__restore_signal_handlers__mutmut_orig, x__restore_signal_handlers__mutmut_mutants, args, kwargs
    )
    return result


_restore_signal_handlers.__signature__ = _mutmut_signature(x__restore_signal_handlers__mutmut_orig)
x__restore_signal_handlers__mutmut_orig.__name__ = "x__restore_signal_handlers"


def x_register_cleanup_handlers__mutmut_orig(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_1(*, manage_signals: bool = False) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_2(*, manage_signals: bool = True) -> None:
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
    atexit.register(None)

    # Register signal handlers if requested
    if manage_signals:
        # Save original handlers
        _original_sigint_handler = signal.getsignal(signal.SIGINT)
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_3(*, manage_signals: bool = True) -> None:
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
        _original_sigint_handler = None
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_4(*, manage_signals: bool = True) -> None:
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
        _original_sigint_handler = signal.getsignal(None)
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_5(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = None

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_6(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(None)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_7(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(None, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_8(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, None)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_9(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(_signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_10(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(
            signal.SIGINT,
        )
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_11(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(None, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_12(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, None)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_13(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(_signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_14(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(
            signal.SIGTERM,
        )

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_15(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = None
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_16(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = False
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_17(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace(None)
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_18(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("XXRegistered cleanup handlers with signal managementXX")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_19(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("registered cleanup handlers with signal management")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_20(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("REGISTERED CLEANUP HANDLERS WITH SIGNAL MANAGEMENT")
    else:
        log.trace("Registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_21(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace(None)


def x_register_cleanup_handlers__mutmut_22(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("XXRegistered cleanup handlers (signal management disabled)XX")


def x_register_cleanup_handlers__mutmut_23(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("registered cleanup handlers (signal management disabled)")


def x_register_cleanup_handlers__mutmut_24(*, manage_signals: bool = True) -> None:
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
        _original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        # Register our handlers
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        _handlers_registered = True
        log.trace("Registered cleanup handlers with signal management")
    else:
        log.trace("REGISTERED CLEANUP HANDLERS (SIGNAL MANAGEMENT DISABLED)")


x_register_cleanup_handlers__mutmut_mutants: ClassVar[MutantDict] = {
    "x_register_cleanup_handlers__mutmut_1": x_register_cleanup_handlers__mutmut_1,
    "x_register_cleanup_handlers__mutmut_2": x_register_cleanup_handlers__mutmut_2,
    "x_register_cleanup_handlers__mutmut_3": x_register_cleanup_handlers__mutmut_3,
    "x_register_cleanup_handlers__mutmut_4": x_register_cleanup_handlers__mutmut_4,
    "x_register_cleanup_handlers__mutmut_5": x_register_cleanup_handlers__mutmut_5,
    "x_register_cleanup_handlers__mutmut_6": x_register_cleanup_handlers__mutmut_6,
    "x_register_cleanup_handlers__mutmut_7": x_register_cleanup_handlers__mutmut_7,
    "x_register_cleanup_handlers__mutmut_8": x_register_cleanup_handlers__mutmut_8,
    "x_register_cleanup_handlers__mutmut_9": x_register_cleanup_handlers__mutmut_9,
    "x_register_cleanup_handlers__mutmut_10": x_register_cleanup_handlers__mutmut_10,
    "x_register_cleanup_handlers__mutmut_11": x_register_cleanup_handlers__mutmut_11,
    "x_register_cleanup_handlers__mutmut_12": x_register_cleanup_handlers__mutmut_12,
    "x_register_cleanup_handlers__mutmut_13": x_register_cleanup_handlers__mutmut_13,
    "x_register_cleanup_handlers__mutmut_14": x_register_cleanup_handlers__mutmut_14,
    "x_register_cleanup_handlers__mutmut_15": x_register_cleanup_handlers__mutmut_15,
    "x_register_cleanup_handlers__mutmut_16": x_register_cleanup_handlers__mutmut_16,
    "x_register_cleanup_handlers__mutmut_17": x_register_cleanup_handlers__mutmut_17,
    "x_register_cleanup_handlers__mutmut_18": x_register_cleanup_handlers__mutmut_18,
    "x_register_cleanup_handlers__mutmut_19": x_register_cleanup_handlers__mutmut_19,
    "x_register_cleanup_handlers__mutmut_20": x_register_cleanup_handlers__mutmut_20,
    "x_register_cleanup_handlers__mutmut_21": x_register_cleanup_handlers__mutmut_21,
    "x_register_cleanup_handlers__mutmut_22": x_register_cleanup_handlers__mutmut_22,
    "x_register_cleanup_handlers__mutmut_23": x_register_cleanup_handlers__mutmut_23,
    "x_register_cleanup_handlers__mutmut_24": x_register_cleanup_handlers__mutmut_24,
}


def register_cleanup_handlers(*args, **kwargs):
    result = _mutmut_trampoline(
        x_register_cleanup_handlers__mutmut_orig, x_register_cleanup_handlers__mutmut_mutants, args, kwargs
    )
    return result


register_cleanup_handlers.__signature__ = _mutmut_signature(x_register_cleanup_handlers__mutmut_orig)
x_register_cleanup_handlers__mutmut_orig.__name__ = "x_register_cleanup_handlers"


def x_unregister_cleanup_handlers__mutmut_orig() -> None:
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


def x_unregister_cleanup_handlers__mutmut_1() -> None:
    """Unregister cleanup handlers (mainly for testing).

    Restores original signal handlers and removes atexit hook.
    """
    global _cleanup_executed

    # Restore original signal handlers
    _restore_signal_handlers()

    # Remove atexit handler
    with contextlib.suppress(None):
        atexit.unregister(_cleanup_foundation_resources)

    # Reset cleanup flag
    _cleanup_executed = False

    log.trace("Unregister cleanup handlers")


def x_unregister_cleanup_handlers__mutmut_2() -> None:
    """Unregister cleanup handlers (mainly for testing).

    Restores original signal handlers and removes atexit hook.
    """
    global _cleanup_executed

    # Restore original signal handlers
    _restore_signal_handlers()

    # Remove atexit handler
    with contextlib.suppress(ValueError):
        atexit.unregister(None)

    # Reset cleanup flag
    _cleanup_executed = False

    log.trace("Unregister cleanup handlers")


def x_unregister_cleanup_handlers__mutmut_3() -> None:
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
    _cleanup_executed = None

    log.trace("Unregister cleanup handlers")


def x_unregister_cleanup_handlers__mutmut_4() -> None:
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
    _cleanup_executed = True

    log.trace("Unregister cleanup handlers")


def x_unregister_cleanup_handlers__mutmut_5() -> None:
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

    log.trace(None)


def x_unregister_cleanup_handlers__mutmut_6() -> None:
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

    log.trace("XXUnregister cleanup handlersXX")


def x_unregister_cleanup_handlers__mutmut_7() -> None:
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

    log.trace("unregister cleanup handlers")


def x_unregister_cleanup_handlers__mutmut_8() -> None:
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

    log.trace("UNREGISTER CLEANUP HANDLERS")


x_unregister_cleanup_handlers__mutmut_mutants: ClassVar[MutantDict] = {
    "x_unregister_cleanup_handlers__mutmut_1": x_unregister_cleanup_handlers__mutmut_1,
    "x_unregister_cleanup_handlers__mutmut_2": x_unregister_cleanup_handlers__mutmut_2,
    "x_unregister_cleanup_handlers__mutmut_3": x_unregister_cleanup_handlers__mutmut_3,
    "x_unregister_cleanup_handlers__mutmut_4": x_unregister_cleanup_handlers__mutmut_4,
    "x_unregister_cleanup_handlers__mutmut_5": x_unregister_cleanup_handlers__mutmut_5,
    "x_unregister_cleanup_handlers__mutmut_6": x_unregister_cleanup_handlers__mutmut_6,
    "x_unregister_cleanup_handlers__mutmut_7": x_unregister_cleanup_handlers__mutmut_7,
    "x_unregister_cleanup_handlers__mutmut_8": x_unregister_cleanup_handlers__mutmut_8,
}


def unregister_cleanup_handlers(*args, **kwargs):
    result = _mutmut_trampoline(
        x_unregister_cleanup_handlers__mutmut_orig, x_unregister_cleanup_handlers__mutmut_mutants, args, kwargs
    )
    return result


unregister_cleanup_handlers.__signature__ = _mutmut_signature(x_unregister_cleanup_handlers__mutmut_orig)
x_unregister_cleanup_handlers__mutmut_orig.__name__ = "x_unregister_cleanup_handlers"


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


# <3 🧱🤝💻🪄
