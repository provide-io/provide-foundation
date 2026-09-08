# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""A log line must not raise into the code that emitted it.

Windows consoles default to cp1252, which cannot encode the emoji this
library logs. `ensure_utf8_stream` reconfigures the stream, but that is a fact
about the stream at one moment: colorama wraps the console on Windows and
holds its own reference, so a write can still raise afterwards. structlog's
PrintLogger writes straight to the file it was given, so it never reaches
`write_to_console` and the handling there.

What that produced was not a broken log line but a broken program: across
supsrc and terraform-provider-tofusoup, 135 tests failed on Windows, and in
the provider the UnicodeEncodeError replaced the real error message --

    Failed to query provider info for hashicorp/aws from terraform registry:
    'charmap' codec can't encode characters in position 0-1

-- so the assertion about the actual failure could not match.

A cp1252 stream reproduces all of that on any platform.
"""

from __future__ import annotations

import io

import pytest

from provide.foundation.utils.streams import UnicodeSafeStream

EMOJI = "🔨🚀 building"


def _cp1252_stream() -> io.TextIOWrapper:
    return io.TextIOWrapper(io.BytesIO(), encoding="cp1252", errors="strict", newline="")


def test_the_bare_stream_raises() -> None:
    """The failure being guarded against, so the guard cannot pass vacuously."""
    with pytest.raises(UnicodeEncodeError):
        _cp1252_stream().write(EMOJI)


def test_the_guarded_stream_does_not_raise() -> None:
    stream = _cp1252_stream()

    UnicodeSafeStream(stream).write(EMOJI)


def test_the_encodable_part_survives() -> None:
    stream = _cp1252_stream()

    UnicodeSafeStream(stream).write(EMOJI)

    stream.flush()
    written = stream.buffer.getvalue().decode("cp1252")
    assert "building" in written


def test_an_encodable_message_is_written_unchanged() -> None:
    stream = _cp1252_stream()

    UnicodeSafeStream(stream).write("plain ascii")

    stream.flush()
    assert stream.buffer.getvalue().decode("cp1252") == "plain ascii"


def test_write_reports_what_it_wrote() -> None:
    assert UnicodeSafeStream(_cp1252_stream()).write("abc") == 3


def test_other_attributes_are_the_wrapped_stream_s() -> None:
    stream = _cp1252_stream()
    safe = UnicodeSafeStream(stream)

    assert safe.encoding == "cp1252"
    assert safe.isatty() is False
    safe.flush()


def test_a_utf8_stream_is_unaffected() -> None:
    stream = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline="")

    UnicodeSafeStream(stream).write(EMOJI)

    stream.flush()
    assert stream.buffer.getvalue().decode("utf-8") == EMOJI


def test_a_proxy_that_cannot_be_reconfigured_is_still_safe() -> None:
    """The colorama shape: a wrapper holding its own reference to the console."""

    class Proxy:
        def __init__(self, wrapped: io.TextIOWrapper) -> None:
            self.wrapped = wrapped
            self.encoding = wrapped.encoding

        def write(self, text: str) -> int:
            return self.wrapped.write(text)

    proxy = Proxy(_cp1252_stream())

    UnicodeSafeStream(proxy).write(EMOJI)


def test_the_emoji_itself_survives_as_utf8() -> None:
    """The byte layer takes UTF-8 regardless of what the text layer encodes.

    Re-encoding the text through cp1252 is the lossy path: every unencodable
    character collapses to the same `?`, so a log line naming which resource
    failed reads identically to one naming a different resource. Writing UTF-8
    under the text layer keeps the characters.
    """
    stream = _cp1252_stream()

    UnicodeSafeStream(stream).write(EMOJI)

    assert stream.buffer.getvalue().decode("utf-8") == EMOJI


def test_a_stream_with_no_byte_layer_still_does_not_raise() -> None:
    """StringIO and test doubles have no `buffer` to write under."""
    stream = io.StringIO()

    UnicodeSafeStream(stream).write(EMOJI)

    assert stream.getvalue() == EMOJI
