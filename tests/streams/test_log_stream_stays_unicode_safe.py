#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The log stream stays safe to write emoji to, however it is reconfigured.

Wrapping the stream once during setup is not enough: every path that swaps the
stream rebuilds structlog's logger factory, and a rebuild that reaches for the
raw stream discards the wrapping. These tests pin the property at the points
where it was previously lost.
"""

from __future__ import annotations

import io

import structlog

from provide.foundation.streams import core as stream_core
from provide.foundation.utils.streams import UnicodeSafeStream, unicode_safe


class _Cp1252Stream(io.TextIOWrapper):
    """A text stream that raises on emoji, the way a Windows console does."""

    def __init__(self) -> None:
        super().__init__(io.BytesIO(), encoding="cp1252", newline="")


def _factory_file() -> object:
    """The stream structlog's configured logger factory writes through."""
    return structlog.get_config()["logger_factory"]._file


def test_a_cp1252_stream_is_what_this_guards_against() -> None:
    """The stand-in really does raise, so the tests below prove something."""
    stream = _Cp1252Stream()
    try:
        stream.write("🐍")
    except UnicodeEncodeError:
        return
    raise AssertionError("the cp1252 stand-in accepted an emoji")


def test_reconfiguring_keeps_the_factory_wrapped(monkeypatch) -> None:
    """The regression: reconfiguration rebuilt the factory from the raw stream."""
    monkeypatch.setattr(stream_core, "_PROVIDE_LOG_STREAM", _Cp1252Stream())

    stream_core._reconfigure_structlog_stream()

    assert isinstance(_factory_file(), UnicodeSafeStream)


def test_a_reconfigured_logger_survives_an_emoji(monkeypatch) -> None:
    """What the wrapping is for: the write must not raise into the caller."""
    monkeypatch.setattr(stream_core, "_PROVIDE_LOG_STREAM", _Cp1252Stream())
    stream_core._reconfigure_structlog_stream()

    _factory_file().write("🐍 emoji\n")


def test_the_testmode_reset_leaves_a_wrapped_factory(monkeypatch) -> None:
    """pytest is where colorama wraps the console, so this path matters most.

    reset_structlog_state builds its own factory over sys.stdout; before the
    fix that stream reached structlog raw.
    """
    from provide.foundation.testmode.internal import reset_structlog_state

    monkeypatch.setattr("sys.stdout", _Cp1252Stream())
    reset_structlog_state()

    assert isinstance(_factory_file(), UnicodeSafeStream)
    _factory_file().write("\U0001f40d testmode\n")


def test_wrapping_an_already_wrapped_stream_does_not_nest() -> None:
    wrapped = UnicodeSafeStream(_Cp1252Stream())

    assert unicode_safe(wrapped) is wrapped
