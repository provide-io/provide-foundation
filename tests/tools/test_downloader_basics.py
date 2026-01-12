#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ToolDownloader basic functionality.

Tests initialization, callbacks, progress reporting, and checksum verification."""

from __future__ import annotations

from pathlib import Path

from provide.testkit.mocking import Mock

from provide.foundation.tools.downloader import DownloadError, ToolDownloader


class TestDownloadError:
    """Tests for DownloadError exception."""

    def test_download_error_inheritance(self) -> None:
        """Test that DownloadError inherits from FoundationError."""
        from provide.foundation.errors import FoundationError

        error = DownloadError("Test error")
        assert isinstance(error, FoundationError)


class TestToolDownloaderInit:
    """Tests for ToolDownloader initialization."""

    def test_downloader_creation(self) -> None:
        """Test basic downloader initialization."""
        mock_client = Mock()
        downloader = ToolDownloader(mock_client)

        assert downloader.client == mock_client
        assert downloader.progress_callbacks == []
        assert downloader.retry_policy is not None
        assert downloader.retry_policy.max_attempts == 3
        assert downloader.retry_policy.base_delay == 1.0

    def test_downloader_with_custom_time_source(self) -> None:
        """Test downloader with custom time source for testing."""
        mock_client = Mock()
        time_source = Mock(return_value=1234567890.0)

        downloader = ToolDownloader(mock_client, time_source=time_source)

        assert downloader.client == mock_client

    def test_downloader_with_async_sleep_func(self) -> None:
        """Test downloader with custom async sleep function."""
        mock_client = Mock()

        async def custom_sleep(delay: float) -> None:
            pass

        downloader = ToolDownloader(mock_client, async_sleep_func=custom_sleep)

        assert downloader.client == mock_client


class TestAddProgressCallback:
    """Tests for add_progress_callback method."""

    def test_add_single_callback(self) -> None:
        """Test adding a single progress callback."""
        mock_client = Mock()
        downloader = ToolDownloader(mock_client)

        callback = Mock()
        downloader.add_progress_callback(callback)

        assert len(downloader.progress_callbacks) == 1
        assert downloader.progress_callbacks[0] == callback

    def test_add_multiple_callbacks(self) -> None:
        """Test adding multiple progress callbacks."""
        mock_client = Mock()
        downloader = ToolDownloader(mock_client)

        callback1 = Mock()
        callback2 = Mock()

        downloader.add_progress_callback(callback1)
        downloader.add_progress_callback(callback2)

        assert len(downloader.progress_callbacks) == 2


class TestReportProgress:
    """Tests for _report_progress method."""

    def test_report_progress_calls_all_callbacks(self) -> None:
        """Test that progress is reported to all callbacks."""
        mock_client = Mock()
        downloader = ToolDownloader(mock_client)

        callback1 = Mock()
        callback2 = Mock()

        downloader.add_progress_callback(callback1)
        downloader.add_progress_callback(callback2)

        downloader._report_progress(100, 200)

        callback1.assert_called_once_with(100, 200)
        callback2.assert_called_once_with(100, 200)

    def test_report_progress_handles_callback_exception(self) -> None:
        """Test that callback exceptions don't prevent other callbacks."""
        mock_client = Mock()
        downloader = ToolDownloader(mock_client)

        callback1 = Mock(side_effect=Exception("Callback error"))
        callback2 = Mock()

        downloader.add_progress_callback(callback1)
        downloader.add_progress_callback(callback2)

        # Should not raise
        downloader._report_progress(100, 200)

        # Second callback should still be called
        callback2.assert_called_once_with(100, 200)


class TestVerifyChecksum:
    """Tests for verify_checksum method."""

    def test_verify_checksum_match(self, tmp_path: Path) -> None:
        """Test checksum verification with matching hash."""
        mock_client = Mock()
        downloader = ToolDownloader(mock_client)

        # Create a file with known content
        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        # Calculate SHA256 hash for "test content"
        # echo -n "test content" | shasum -a 256
        # 6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72
        expected = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"

        result = downloader.verify_checksum(file_path, expected)

        assert result is True

    def test_verify_checksum_mismatch(self, tmp_path: Path) -> None:
        """Test checksum verification with non-matching hash."""
        mock_client = Mock()
        downloader = ToolDownloader(mock_client)

        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        # Wrong hash
        expected = "0000000000000000000000000000000000000000000000000000000000000000"

        result = downloader.verify_checksum(file_path, expected)

        assert result is False


# 🧱🏗️🔚
