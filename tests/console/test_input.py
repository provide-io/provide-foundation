#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for console input functions."""

from __future__ import annotations

import asyncio
from io import StringIO
from typing import Never

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.console.input import (
    apin,
    apin_lines,
    apin_stream,
    pin,
    pin_lines,
    pin_stream,
)
from provide.foundation.context import CLIContext


class TestPin(FoundationTestCase):
    """Test basic pin() function."""

    def test_pin_basic_input(self) -> None:
        """Test basic input with pin()."""
        with patch("click.prompt", return_value="test input"):
            result = pin("Enter text: ")
            assert result == "test input"

    def test_pin_with_type_conversion(self) -> None:
        """Test pin() with type conversion."""
        with patch("click.prompt", return_value=42):
            result = pin("Enter number: ", type=int)
            assert result == 42
            assert isinstance(result, int)

    def test_pin_with_default(self) -> None:
        """Test pin() with default value."""
        with patch("click.prompt", return_value="default"):
            result = pin("Enter text: ", default="default")
            assert result == "default"

    def test_pin_password_mode(self) -> None:
        """Test pin() in password mode."""
        with patch("click.prompt", return_value="secret") as mock_prompt:
            result = pin("Password: ", password=True)
            assert result == "secret"
            # Check that hide_input was passed to click.prompt
            assert mock_prompt.call_args[1]["hide_input"] is True

    def test_pin_with_color(self) -> None:
        """Test pin() with colored prompt."""
        with (
            patch("click.prompt", return_value="test") as mock_prompt,
            patch("sys.stdin.isatty", return_value=True),
        ):
            result = pin("Enter: ", color="green", bold=True)
            assert result == "test"
            # The prompt should be styled
            prompt_arg = mock_prompt.call_args[0][0]
            assert isinstance(prompt_arg, str)  # Should be styled string

    def test_pin_json_mode(self) -> None:
        """Test pin() in JSON mode."""
        ctx = CLIContext()
        ctx.json_output = True

        test_input = '{"key": "value"}'
        with (
            patch("sys.stdin", StringIO(test_input)),
            patch(
                "provide.foundation.console.input._get_context",
                return_value=ctx,
            ),
        ):
            result = pin("Enter JSON: ")
            assert result == {"key": "value"}

    def test_pin_json_mode_with_plain_text(self) -> None:
        """Test pin() in JSON mode with plain text input."""
        ctx = CLIContext()
        ctx.json_output = True

        test_input = "plain text\n"
        with (
            patch("sys.stdin", StringIO(test_input)),
            patch(
                "provide.foundation.console.input._get_context",
                return_value=ctx,
            ),
        ):
            result = pin("Enter: ")
            assert result == "plain text"

    def test_pin_json_mode_with_json_key(self) -> None:
        """Test pin() in JSON mode with json_key."""
        ctx = CLIContext()
        ctx.json_output = True

        test_input = "test value\n"
        with (
            patch("sys.stdin", StringIO(test_input)),
            patch(
                "provide.foundation.console.input._get_context",
                return_value=ctx,
            ),
        ):
            result = pin("Enter: ", json_key="input")
            assert result == {"input": "test value"}


class TestPinStream(FoundationTestCase):
    """Test pin_stream() function."""

    def test_pin_stream_basic(self) -> None:
        """Test basic line streaming."""
        test_input = "line1\nline2\nline3\n"
        with patch("sys.stdin", StringIO(test_input)):
            lines = list(pin_stream())
            assert lines == ["line1", "line2", "line3"]

    def test_pin_stream_strips_newlines(self) -> None:
        """Test that pin_stream() strips newlines."""
        test_input = "line1\r\nline2\n\rline3\n"
        with patch("sys.stdin", StringIO(test_input)):
            lines = list(pin_stream())
            assert lines == [
                "line1",
                "line2",
                "\rline3",
            ]  # \r at start is part of content

    def test_pin_stream_empty_lines(self) -> None:
        """Test pin_stream() with empty lines."""
        test_input = "line1\n\nline2\n"
        with patch("sys.stdin", StringIO(test_input)):
            lines = list(pin_stream())
            assert lines == ["line1", "", "line2"]

    def test_pin_stream_json_mode_array(self) -> None:
        """Test pin_stream() in JSON mode with array."""
        ctx = CLIContext()
        ctx.json_output = True

        test_input = '["item1", "item2", "item3"]'
        with (
            patch("sys.stdin", StringIO(test_input)),
            patch(
                "provide.foundation.console.input._get_context",
                return_value=ctx,
            ),
        ):
            lines = list(pin_stream())
            assert lines == ["item1", "item2", "item3"]

    def test_pin_stream_json_mode_object(self) -> None:
        """Test pin_stream() in JSON mode with object."""
        ctx = CLIContext()
        ctx.json_output = True

        test_input = '{"key": "value"}'
        with (
            patch("sys.stdin", StringIO(test_input)),
            patch(
                "provide.foundation.console.input._get_context",
                return_value=ctx,
            ),
        ):
            lines = list(pin_stream())
            assert lines == ['{"key": "value"}']

    def test_pin_stream_json_mode_fallback(self) -> None:
        """Test pin_stream() JSON mode fallback for invalid JSON."""
        ctx = CLIContext()
        ctx.json_output = True

        test_input = "plain\ntext\nlines\n"
        with (
            patch("sys.stdin", StringIO(test_input)),
            patch(
                "provide.foundation.console.input._get_context",
                return_value=ctx,
            ),
        ):
            lines = list(pin_stream())
            assert lines == ["plain", "text", "lines"]


class TestPinLines(FoundationTestCase):
    """Test pin_lines() function."""

    def test_pin_lines_with_count(self) -> None:
        """Test pin_lines() with specific count."""
        test_input = "line1\nline2\nline3\nline4\n"
        with patch("sys.stdin", StringIO(test_input)):
            lines = pin_lines(2)
            assert lines == ["line1", "line2"]

    def test_pin_lines_all(self) -> None:
        """Test pin_lines() reading all lines."""
        test_input = "line1\nline2\nline3\n"
        with patch("sys.stdin", StringIO(test_input)):
            lines = pin_lines()
            assert lines == ["line1", "line2", "line3"]

    def test_pin_lines_empty(self) -> None:
        """Test pin_lines() with empty input."""
        with patch("sys.stdin", StringIO("")):
            lines = pin_lines()
            assert lines == []


class TestAsyncPin(FoundationTestCase):
    """Test async pin functions."""

    @pytest.mark.asyncio
    async def test_apin_basic(self) -> None:
        """Test basic async input."""
        with patch("provide.foundation.console.input.pin", return_value="async test"):
            result = await apin("Enter: ")
            assert result == "async test"

    @pytest.mark.asyncio
    async def test_apin_with_kwargs(self) -> None:
        """Test apin() passes kwargs correctly."""
        with patch("provide.foundation.console.input.pin", return_value=42) as mock_pin:
            result = await apin("Number: ", type=int, default=0)
            assert result == 42
            # Check that pin was called with correct args
            mock_pin.assert_called_once_with("Number: ", type=int, default=0)

    @pytest.mark.asyncio
    @pytest.mark.skip(
        reason="Requires real stdin which is not available in test environment",
    )
    async def test_apin_stream_basic(self) -> None:
        """Test basic async streaming."""
        test_lines = ["line1", "line2", "line3"]

        async def mock_stream():
            for line in test_lines:
                yield line

        # Mock the async generator
        with patch(
            "provide.foundation.console.input.apin_stream",
            return_value=mock_stream(),
        ):
            lines = []
            async for line in apin_stream():
                lines.append(line)
            assert lines == test_lines

    @pytest.mark.asyncio
    async def test_apin_lines_with_count(self) -> None:
        """Test apin_lines() with specific count."""
        test_lines = ["line1", "line2", "line3", "line4"]

        async def mock_stream():
            for line in test_lines:
                yield line

        with patch(
            "provide.foundation.console.input.apin_stream",
            return_value=mock_stream(),
        ):
            lines = await apin_lines(2)
            assert lines == ["line1", "line2"]

    @pytest.mark.asyncio
    async def test_apin_lines_all(self) -> None:
        """Test apin_lines() reading all lines."""
        test_lines = ["line1", "line2", "line3"]

        async def mock_stream():
            for line in test_lines:
                yield line

        with patch(
            "provide.foundation.console.input.apin_stream",
            return_value=mock_stream(),
        ):
            lines = await apin_lines()
            assert lines == test_lines


class TestAsyncStreamIntegration(FoundationTestCase):
    """Test async streaming with real async I/O."""

    @pytest.mark.asyncio
    async def test_apin_stream_real_async(self) -> None:
        """Test apin_stream() with simulated async stdin."""
        # This tests the actual async implementation
        test_data = b"async line 1\nasync line 2\n"

        # Create a mock async reader
        reader = asyncio.StreamReader()
        reader.feed_data(test_data)
        reader.feed_eof()

        async def mock_connect(*args):
            return (None, None)

        with (
            patch("asyncio.StreamReader", return_value=reader),
            patch("asyncio.get_event_loop") as mock_loop,
        ):
            mock_loop.return_value.connect_read_pipe = mock_connect

            lines = []
            async for line in apin_stream():
                lines.append(line)
                if len(lines) >= 2:  # Stop after expected lines
                    break

            assert lines == ["async line 1", "async line 2"]

    @pytest.mark.asyncio
    async def test_apin_stream_json_mode_async(self) -> None:
        """Test async streaming in JSON mode."""
        ctx = CLIContext()
        ctx.json_output = True

        test_data = ["item1", "item2", "item3"]

        # Mock the executor call for JSON reading
        with patch("asyncio.get_event_loop") as mock_loop:
            future: asyncio.Future[list[str]] = asyncio.Future()
            future.set_result(test_data)
            mock_loop.return_value.run_in_executor.return_value = future

            with patch(
                "provide.foundation.console.input._get_context",
                return_value=ctx,
            ):
                lines = []
                async for line in apin_stream():
                    lines.append(line)

                assert lines == test_data


class TestEdgeCases(FoundationTestCase):
    """Test edge cases and error handling."""

    def test_pin_json_error_handling(self) -> None:
        """Test pin() handles JSON errors gracefully."""
        ctx = CLIContext()
        ctx.json_output = True

        # Simulate an error reading stdin
        with (
            patch("sys.stdin.readline", side_effect=OSError("Read error")),
            patch(
                "provide.foundation.console.input._get_context",
                return_value=ctx,
            ),
        ):
            result = pin("Enter: ", json_key="input")
            assert result == {"input": None, "error": "Read error"}

    def test_pin_stream_logging(self) -> None:
        """Test that pin_stream() logs appropriately."""
        test_input = "line1\nline2\n"

        with (
            patch("sys.stdin", StringIO(test_input)),
            patch("provide.foundation.console.input.log") as mock_log,
        ):
            list(pin_stream())

            # Check debug logging
            mock_log.debug.assert_called()
            # Should log start and end
            assert mock_log.debug.call_count >= 2

    @pytest.mark.asyncio
    async def test_apin_stream_cancellation(self) -> None:
        """Test apin_stream() handles cancellation."""
        reader = asyncio.StreamReader()

        async def cancel_after_delay() -> Never:
            await asyncio.sleep(0.01)
            raise asyncio.CancelledError()

        async def mock_connect(*args):
            return (None, None)

        with (
            patch("asyncio.StreamReader", return_value=reader),
            patch("asyncio.get_event_loop") as mock_loop,
            patch("provide.foundation.console.input.log") as mock_log,
        ):
            mock_loop.return_value.connect_read_pipe = mock_connect
            reader.readline = cancel_after_delay

            lines = []
            async for line in apin_stream():
                lines.append(line)

            # Should have logged cancellation
            mock_log.debug.assert_called()
            assert any("cancelled" in str(call) for call in mock_log.debug.call_args_list)

    @pytest.mark.asyncio
    async def test_apin_stream_error_handling(self) -> None:
        """Test apin_stream() handles errors gracefully."""
        reader = asyncio.StreamReader()

        async def raise_error() -> Never:
            raise ValueError("Test error")

        async def mock_connect(*args):
            return (None, None)

        with (
            patch("asyncio.StreamReader", return_value=reader),
            patch("asyncio.get_event_loop") as mock_loop,
            patch("provide.foundation.console.input.log") as mock_log,
        ):
            mock_loop.return_value.connect_read_pipe = mock_connect
            reader.readline = raise_error

            lines = []
            async for line in apin_stream():
                lines.append(line)

            # Should have logged error
            mock_log.error.assert_called()
            assert "Test error" in str(mock_log.error.call_args)


# 🧱🏗️🔚
