#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import io
import sys
from typing import TextIO

"""Stream utilities for foundation library."""


# Attribute names a stream proxy uses for the stream it writes through.
# colorama's StreamWrapper keeps the original as `wrapped`; other proxies use
# `stream`. A proxy that forwards neither `reconfigure` nor `buffer` cannot be
# secured through itself, so the stream underneath has to be reached directly.
_PROXIED_STREAM_ATTRIBUTES = ("wrapped", "stream")


def _is_utf8(encoding: str) -> bool:
    """Whether an encoding name denotes UTF-8, however it is spelled."""
    return encoding.lower().replace("-", "").replace("_", "") == "utf8"


def _reconfigure_to_utf8(stream: object) -> bool:
    """Reconfigure one stream object in place. True when it is safe afterwards."""
    encoding = getattr(stream, "encoding", None)
    if encoding is None:
        # No encoding to fail on -- StringIO and friends take str directly.
        return True
    if _is_utf8(encoding):
        return True

    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(encoding="utf-8", errors="replace")
            return True
        except Exception:
            # reconfigure may fail on non-standard streams
            return False
    return False


def _secure_proxied_streams(stream: object) -> bool:
    """Reconfigure the streams a proxy writes through, however deeply nested.

    Returns True when a proxied stream was found and made safe, which means
    writes through the proxy no longer raise even though the proxy itself
    exposed no way to reconfigure it.
    """
    secured = False
    seen: set[int] = {id(stream)}
    pending: list[object] = [stream]

    while pending:
        current = pending.pop()
        for attribute in _PROXIED_STREAM_ATTRIBUTES:
            nested = getattr(current, attribute, None)
            # A cycle, or a proxy pointing at itself, must not loop forever.
            if nested is None or id(nested) in seen:
                continue
            seen.add(id(nested))
            if _reconfigure_to_utf8(nested):
                secured = True
            pending.append(nested)

    return secured


def ensure_utf8_stream(stream: TextIO) -> TextIO:
    """Ensure a text stream uses UTF-8 encoding with error replacement.

    On Windows, console streams default to legacy encodings (e.g., cp1252)
    which cannot encode Unicode characters like emoji. This function
    reconfigures or wraps such streams to use UTF-8 with 'replace' error
    handling, preventing UnicodeEncodeError in logging paths.

    On non-Windows platforms or for streams that already use UTF-8 or
    have no encoding attribute (e.g., StringIO), the stream is returned
    unchanged.

    Args:
        stream: A text stream to ensure UTF-8 encoding on.

    Returns:
        The stream, possibly reconfigured or wrapped for UTF-8 safety.

    """
    if stream is None:
        return stream

    # Only act on streams that have a non-UTF-8 encoding
    encoding = getattr(stream, "encoding", None)
    if encoding is None:
        return stream

    # Already UTF-8 — nothing to do
    if _is_utf8(encoding):
        return stream

    # Try reconfigure (available on Python 3.7+ for standard streams)
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
            return stream
        except Exception:
            # reconfigure may fail on non-standard streams
            pass

    # A proxy reports the encoding of the stream it writes through but may
    # expose no way to reconfigure itself. Securing that stream directly makes
    # writes through the proxy safe, so the proxy is still what callers get.
    if _secure_proxied_streams(stream):
        return stream

    # Fallback: wrap the underlying buffer with a UTF-8 TextIOWrapper
    buffer = getattr(stream, "buffer", None)
    if buffer is not None:
        try:
            wrapper = io.TextIOWrapper(buffer, encoding="utf-8", errors="replace", line_buffering=True)
            # Prevent the wrapper from closing the underlying buffer on GC
            wrapper._owner = False  # type: ignore[attr-defined]
            return wrapper
        except Exception:
            pass

    # Cannot reconfigure — return as-is (best effort)
    return stream


def get_safe_stderr() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return ensure_utf8_stream(sys.stderr)
    else:
        return io.StringIO()


def get_foundation_log_stream(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return ensure_utf8_stream(sys.stdout)
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


# 🧱🏗️🔚
