#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A log call must not raise because of what the stream can encode.

Foundation's loggers prefix events with emoji. A Windows console stream is
cp1252, which has no mapping for them, so a stream handed to structlog without
passing through ensure_utf8_stream turns every log call into a
UnicodeEncodeError -- raised into whatever called the logger, not into the
logging machinery.
"""

from __future__ import annotations

import io

import structlog

from provide.foundation.logger.config.base import get_config_logger
from provide.foundation.testmode.detection import configure_structlog_for_test_safety
from provide.foundation.utils.streams import ensure_utf8_stream

ROCKET = "\U0001f680"


def _cp1252_stream() -> io.TextIOWrapper:
    """A stream that encodes like a Windows console, on any platform."""
    return io.TextIOWrapper(io.BytesIO(), encoding="cp1252", errors="strict")


class _ColoramaLikeProxy:
    """Stands in for colorama's AnsiToWin32 wrapper.

    It reports the encoding of the stream it wrapped and forwards writes to it,
    which is how a cp1252 stream survives behind something that looks reconfigured.
    """

    def __init__(self, wrapped: io.TextIOWrapper) -> None:
        self.wrapped = wrapped

    def write(self, text: str) -> int:
        return self.wrapped.write(text)

    def flush(self) -> None:
        self.wrapped.flush()

    def __getattr__(self, name: str) -> object:
        return getattr(self.wrapped, name)


def test_test_safety_config_gives_structlog_an_encodable_stream(monkeypatch) -> None:
    """configure_structlog_for_test_safety must not hand over a raw cp1252 stdout."""
    stream = _cp1252_stream()
    monkeypatch.setattr("sys.stdout", stream)

    configure_structlog_for_test_safety()

    # The emoji is the payload every Foundation log line carries.
    structlog.get_logger().info(f"{ROCKET} starting")

    stream.flush()


def test_ensure_utf8_stream_reaches_a_stream_behind_a_proxy() -> None:
    """A cp1252 stream stays cp1252 unless the helper follows the proxy to it."""
    inner = _cp1252_stream()
    proxy = _ColoramaLikeProxy(inner)

    ensure_utf8_stream(proxy)

    proxy.write(f"{ROCKET} starting")
    proxy.flush()


def test_config_logger_fallback_stream_is_encodable(monkeypatch) -> None:
    """The config logger's fallback runs after stream selection already failed.

    It carries the same emoji-prefixed events as every other Foundation logger,
    so reaching for a raw console stream there raises on the first line.
    """
    stream = _cp1252_stream()
    monkeypatch.setattr("sys.stderr", stream)

    def _no_stream_available(_output_setting: str) -> object:
        raise RuntimeError("stream selection failed")

    monkeypatch.setattr(
        "provide.foundation.utils.streams.get_foundation_log_stream",
        _no_stream_available,
    )

    get_config_logger().warning(f"{ROCKET} falling back")

    stream.flush()


# 🧱🏗️🔚
