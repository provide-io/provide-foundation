# provide/foundation/streams/console.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# console.py
#
import sys
from typing import TextIO

from provide.foundation.streams.config import get_stream_config
from provide.foundation.streams.core import get_log_stream

"""Console stream utilities for Foundation.
Handles console-specific stream operations and formatting.
"""
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


def get_console_stream() -> TextIO:
    """Get the appropriate console stream for output."""
    return get_log_stream()


def x_is_tty__mutmut_orig() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr(stream, "isatty") and stream.isatty()


def x_is_tty__mutmut_1() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = None
    return hasattr(stream, "isatty") and stream.isatty()


def x_is_tty__mutmut_2() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr(stream, "isatty") or stream.isatty()


def x_is_tty__mutmut_3() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr(None, "isatty") and stream.isatty()


def x_is_tty__mutmut_4() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr(stream, None) and stream.isatty()


def x_is_tty__mutmut_5() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr("isatty") and stream.isatty()


def x_is_tty__mutmut_6() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return (
        hasattr(
            stream,
        )
        and stream.isatty()
    )


def x_is_tty__mutmut_7() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr(stream, "XXisattyXX") and stream.isatty()


def x_is_tty__mutmut_8() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr(stream, "ISATTY") and stream.isatty()


x_is_tty__mutmut_mutants: ClassVar[MutantDict] = {
    "x_is_tty__mutmut_1": x_is_tty__mutmut_1,
    "x_is_tty__mutmut_2": x_is_tty__mutmut_2,
    "x_is_tty__mutmut_3": x_is_tty__mutmut_3,
    "x_is_tty__mutmut_4": x_is_tty__mutmut_4,
    "x_is_tty__mutmut_5": x_is_tty__mutmut_5,
    "x_is_tty__mutmut_6": x_is_tty__mutmut_6,
    "x_is_tty__mutmut_7": x_is_tty__mutmut_7,
    "x_is_tty__mutmut_8": x_is_tty__mutmut_8,
}


def is_tty(*args, **kwargs):
    result = _mutmut_trampoline(x_is_tty__mutmut_orig, x_is_tty__mutmut_mutants, args, kwargs)
    return result


is_tty.__signature__ = _mutmut_signature(x_is_tty__mutmut_orig)
x_is_tty__mutmut_orig.__name__ = "x_is_tty"


def x_supports_color__mutmut_orig() -> bool:
    """Check if the current stream supports color output."""
    config = get_stream_config()

    if config.no_color:
        return False

    if config.force_color:
        return True

    # Check if we're in a TTY
    return is_tty()


def x_supports_color__mutmut_1() -> bool:
    """Check if the current stream supports color output."""
    config = None

    if config.no_color:
        return False

    if config.force_color:
        return True

    # Check if we're in a TTY
    return is_tty()


def x_supports_color__mutmut_2() -> bool:
    """Check if the current stream supports color output."""
    config = get_stream_config()

    if config.no_color:
        return True

    if config.force_color:
        return True

    # Check if we're in a TTY
    return is_tty()


def x_supports_color__mutmut_3() -> bool:
    """Check if the current stream supports color output."""
    config = get_stream_config()

    if config.no_color:
        return False

    if config.force_color:
        return False

    # Check if we're in a TTY
    return is_tty()


x_supports_color__mutmut_mutants: ClassVar[MutantDict] = {
    "x_supports_color__mutmut_1": x_supports_color__mutmut_1,
    "x_supports_color__mutmut_2": x_supports_color__mutmut_2,
    "x_supports_color__mutmut_3": x_supports_color__mutmut_3,
}


def supports_color(*args, **kwargs):
    result = _mutmut_trampoline(x_supports_color__mutmut_orig, x_supports_color__mutmut_mutants, args, kwargs)
    return result


supports_color.__signature__ = _mutmut_signature(x_supports_color__mutmut_orig)
x_supports_color__mutmut_orig.__name__ = "x_supports_color"


def x_write_to_console__mutmut_orig(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_1(
    message: str, stream: TextIO | None = None, log_fallback: bool = False
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_2(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = None
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_3(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream and get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_4(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(None)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_5(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    None,
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_6(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=None,
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_7(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=None,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_8(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=None,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_9(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_10(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_11(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_12(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_13(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "XXConsole write failed, falling back to stderrXX",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_14(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_15(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "CONSOLE WRITE FAILED, FALLING BACK TO STDERR",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_16(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(None),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_17(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(None).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_18(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(None).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_19(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(None)
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_20(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(None) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_21(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "XXCritical system failure: unable to write debug information to any streamXX"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_22(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_23(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "CRITICAL SYSTEM FAILURE: UNABLE TO WRITE DEBUG INFORMATION TO ANY STREAM"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


def x_write_to_console__mutmut_24(
    message: str, stream: TextIO | None = None, log_fallback: bool = True
) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(None)
        sys.stderr.flush()


x_write_to_console__mutmut_mutants: ClassVar[MutantDict] = {
    "x_write_to_console__mutmut_1": x_write_to_console__mutmut_1,
    "x_write_to_console__mutmut_2": x_write_to_console__mutmut_2,
    "x_write_to_console__mutmut_3": x_write_to_console__mutmut_3,
    "x_write_to_console__mutmut_4": x_write_to_console__mutmut_4,
    "x_write_to_console__mutmut_5": x_write_to_console__mutmut_5,
    "x_write_to_console__mutmut_6": x_write_to_console__mutmut_6,
    "x_write_to_console__mutmut_7": x_write_to_console__mutmut_7,
    "x_write_to_console__mutmut_8": x_write_to_console__mutmut_8,
    "x_write_to_console__mutmut_9": x_write_to_console__mutmut_9,
    "x_write_to_console__mutmut_10": x_write_to_console__mutmut_10,
    "x_write_to_console__mutmut_11": x_write_to_console__mutmut_11,
    "x_write_to_console__mutmut_12": x_write_to_console__mutmut_12,
    "x_write_to_console__mutmut_13": x_write_to_console__mutmut_13,
    "x_write_to_console__mutmut_14": x_write_to_console__mutmut_14,
    "x_write_to_console__mutmut_15": x_write_to_console__mutmut_15,
    "x_write_to_console__mutmut_16": x_write_to_console__mutmut_16,
    "x_write_to_console__mutmut_17": x_write_to_console__mutmut_17,
    "x_write_to_console__mutmut_18": x_write_to_console__mutmut_18,
    "x_write_to_console__mutmut_19": x_write_to_console__mutmut_19,
    "x_write_to_console__mutmut_20": x_write_to_console__mutmut_20,
    "x_write_to_console__mutmut_21": x_write_to_console__mutmut_21,
    "x_write_to_console__mutmut_22": x_write_to_console__mutmut_22,
    "x_write_to_console__mutmut_23": x_write_to_console__mutmut_23,
    "x_write_to_console__mutmut_24": x_write_to_console__mutmut_24,
}


def write_to_console(*args, **kwargs):
    result = _mutmut_trampoline(
        x_write_to_console__mutmut_orig, x_write_to_console__mutmut_mutants, args, kwargs
    )
    return result


write_to_console.__signature__ = _mutmut_signature(x_write_to_console__mutmut_orig)
x_write_to_console__mutmut_orig.__name__ = "x_write_to_console"


# <3 🧱🤝🌊🪄
