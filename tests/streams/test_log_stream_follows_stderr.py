#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Logging follows sys.stderr rather than the one present at import.

Click's CliRunner and pytest both replace sys.stderr after this package is
imported. A stream captured at import time keeps writing to whatever they
replaced, so the output never reaches the buffer the caller is reading.
"""

from __future__ import annotations

import io
import sys

import pytest

from provide.foundation.streams import core as stream_core


@pytest.fixture(autouse=True)
def _restore_stream() -> None:
    """Each test here moves the module global, so put it back."""
    original = stream_core._PROVIDE_LOG_STREAM
    yield
    stream_core._PROVIDE_LOG_STREAM = original


def test_no_stream_is_captured_at_import() -> None:
    """The default is 'follow stderr', not a reference taken on import."""
    assert stream_core._PROVIDE_LOG_STREAM is None


def test_a_later_stderr_swap_is_picked_up(monkeypatch) -> None:
    """The regression: the global held the pre-swap object forever."""
    stream_core._PROVIDE_LOG_STREAM = None
    swapped = io.StringIO()
    monkeypatch.setattr(sys, "stderr", swapped)

    assert stream_core.get_log_stream() is swapped


def test_writes_reach_the_swapped_stream(monkeypatch) -> None:
    stream_core._PROVIDE_LOG_STREAM = None
    swapped = io.StringIO()
    monkeypatch.setattr(sys, "stderr", swapped)

    stream_core.get_log_stream().write("reached\n")

    assert "reached" in swapped.getvalue()


def test_an_explicitly_set_stream_still_wins(monkeypatch) -> None:
    """Following stderr is the default, not an override of a real choice."""
    chosen = io.StringIO()
    stream_core._PROVIDE_LOG_STREAM = chosen
    monkeypatch.setattr(sys, "stderr", io.StringIO())

    assert stream_core.get_log_stream() is chosen
