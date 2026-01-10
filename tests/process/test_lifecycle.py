#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for process lifecycle management."""

from __future__ import annotations

import asyncio
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.process import ProcessError
from provide.foundation.errors.runtime import StateError
from provide.foundation.process.lifecycle import ManagedProcess, wait_for_process_output


class TestManagedProcess(FoundationTestCase):
    """Test ManagedProcess functionality."""

    def test_init(self) -> None:
        """Test ManagedProcess initialization."""
        process = ManagedProcess(["echo", "hello"])
        assert process.command == ["echo", "hello"]
        assert process.cwd is None
        assert process.capture_output is True
        assert process.process is None
        assert process.pid is None
        assert not process.is_running()

    def test_init_with_options(self, tmp_path: Path) -> None:
        """Test ManagedProcess initialization with options."""
        process = ManagedProcess(
            ["pwd"],
            cwd=tmp_path,
            env={"TEST_VAR": "test_value"},
            capture_output=True,
            stderr_relay=False,
        )
        assert process.command == ["pwd"]
        assert process.cwd == str(tmp_path)
        assert process.capture_output is True
        assert process.stderr_relay is False

    def test_launch_and_cleanup(self) -> None:
        """Test basic process launch and cleanup."""
        process = ManagedProcess(["echo", "hello"])

        # Process should not be running initially
        assert not process.is_running()
        assert process.pid is None

        # Launch the process
        process.launch()

        # Process should be running (briefly)
        assert process.process is not None
        assert process.pid is not None

        # Wait for completion and cleanup
        if process.process:
            process.process.wait()
        process.cleanup()

    def test_launch_twice_raises_error(self) -> None:
        """Test that launching twice raises an error."""
        process = ManagedProcess(["echo", "hello"])
        process.launch()

        with pytest.raises(StateError, match="already been started"):
            process.launch()

        process.cleanup()

    def test_launch_invalid_command_raises_error(self) -> None:
        """Test that invalid command raises ProcessError."""
        process = ManagedProcess(["nonexistent_command_12345"])

        with pytest.raises(ProcessError, match="Failed to launch process"):
            process.launch()

    def test_terminate_gracefully(self) -> None:
        """Test graceful process termination."""
        # Use a longer-running command for better testing
        process = ManagedProcess(["sleep", "1"])
        process.launch()

        # Process should be running
        assert process.is_running()

        # Terminate gracefully
        result = process.terminate_gracefully(timeout=2.0)
        assert result is True  # Should terminate gracefully
        assert not process.is_running()

        process.cleanup()

    def test_terminate_not_running_process(self) -> None:
        """Test terminating a process that's not running."""
        process = ManagedProcess(["echo", "hello"])

        # Should return True for not-running process
        result = process.terminate_gracefully()
        assert result is True

    def test_context_manager(self) -> None:
        """Test using ManagedProcess as a context manager."""
        with ManagedProcess(["echo", "hello"]) as process:
            assert process.process is not None
            assert process.pid is not None

        # Process should be cleaned up after exiting context
        assert not process.is_running()

    @pytest.mark.asyncio
    async def test_read_line_async(self) -> None:
        """Test async line reading."""
        process = ManagedProcess(["echo", "hello world"])
        process.launch()

        try:
            line = await process.read_line_async(timeout=5.0)
            assert "hello world" in line
        finally:
            process.terminate_gracefully()
            process.cleanup()

    @pytest.mark.asyncio
    async def test_read_line_async_no_stdout(self) -> None:
        """Test reading from process without stdout."""
        process = ManagedProcess(["echo", "hello"], capture_output=False)
        process.launch()

        try:
            with pytest.raises(ProcessError, match="stdout not available"):
                await process.read_line_async()
        finally:
            process.terminate_gracefully()
            process.cleanup()

    @pytest.mark.asyncio
    async def test_read_line_async_timeout(self) -> None:
        """Test read timeout."""
        # Use a process that will delay before producing output
        process = ManagedProcess(["sleep", "1"])
        process.launch()

        try:
            with pytest.raises(TimeoutError, match="Read timeout"):
                await process.read_line_async(timeout=0.1)
        finally:
            process.terminate_gracefully()
            process.cleanup()

    @pytest.mark.asyncio
    async def test_read_char_async(self) -> None:
        """Test async character reading."""
        # Use printf to output without newline
        process = ManagedProcess(["printf", "a"])
        process.launch()

        try:
            char = await process.read_char_async(timeout=5.0)
            assert char == "a"
        finally:
            process.terminate_gracefully()
            process.cleanup()


class TestWaitForProcessOutput(FoundationTestCase):
    """Test wait_for_process_output function."""

    @pytest.mark.asyncio
    async def test_wait_for_simple_output(self) -> None:
        """Test waiting for simple output pattern."""
        process = ManagedProcess(["echo", "hello|world|test"])
        process.launch()

        try:
            output = await wait_for_process_output(
                process,
                expected_parts=["|"],
                timeout=5.0,
            )
            assert "hello|world|test" in output
        finally:
            process.terminate_gracefully()
            process.cleanup()

    @pytest.mark.asyncio
    async def test_wait_for_complex_pattern(self) -> None:
        """Test waiting for complex output pattern."""
        # Simulate a handshake-like output with multiple separators
        process = ManagedProcess(["echo", "1|2|protocol|4|5|6"])
        process.launch()

        try:
            output = await wait_for_process_output(
                process,
                expected_parts=["|", "protocol"],
                timeout=5.0,
            )
            assert "1|2|protocol|4|5|6" in output
        finally:
            process.terminate_gracefully()
            process.cleanup()

    @pytest.mark.asyncio
    async def test_wait_for_output_timeout(self) -> None:
        """Test timeout when expected output doesn't appear."""
        # Use a longer-running process to test actual timeout
        process = ManagedProcess(["sleep", "1"])
        process.launch()

        try:
            with pytest.raises(TimeoutError, match="Expected pattern"):
                await wait_for_process_output(
                    process,
                    expected_parts=["nonexistent_pattern"],
                    timeout=0.5,
                )
        finally:
            process.terminate_gracefully()
            process.cleanup()

    @pytest.mark.asyncio
    async def test_wait_for_output_process_exit(self) -> None:
        """Test behavior when process exits before pattern found."""

        process = ManagedProcess(["echo", "hello"])
        process.launch()

        # Wait a bit for the echo to complete
        await asyncio.sleep(0.1)

        try:
            with pytest.raises(ProcessError, match="Process exited"):
                await wait_for_process_output(
                    process,
                    expected_parts=["nonexistent_pattern"],
                    timeout=2.0,
                )
        finally:
            process.cleanup()

    @pytest.mark.asyncio
    async def test_wait_for_output_empty_pattern(self) -> None:
        """Test with empty expected parts."""
        process = ManagedProcess(["echo", "hello"])
        process.launch()

        try:
            output = await wait_for_process_output(
                process,
                expected_parts=[],  # Empty pattern should match immediately
                timeout=5.0,
            )
            assert "hello" in output
        finally:
            process.terminate_gracefully()
            process.cleanup()


# 🧱🏗️🔚
