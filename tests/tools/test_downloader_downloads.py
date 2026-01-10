#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ToolDownloader download functionality.

Tests download_with_progress method including success cases, errors, and checksums."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path

from provide.testkit.mocking import AsyncMock, Mock
import pytest

from provide.foundation.tools.downloader import DownloadError, ToolDownloader


class TestDownloadWithProgress:
    """Tests for download_with_progress method."""

    @pytest.mark.asyncio
    async def test_download_with_progress_success(self, tmp_path: Path) -> None:
        """Test successful download with progress reporting."""
        mock_client = Mock()
        mock_response = AsyncMock()
        mock_response.is_success.return_value = True
        mock_response.status = 200
        mock_response.headers = {"content-length": "12"}

        mock_client.request = AsyncMock(return_value=mock_response)

        # Mock streaming chunks - assign the async generator function directly
        async def mock_stream_generator(*args: tuple, **kwargs: dict) -> AsyncGenerator[bytes, None]:
            for chunk in [b"test", b" ", b"content"]:
                yield chunk

        mock_client.stream = mock_stream_generator

        downloader = ToolDownloader(mock_client)
        dest = tmp_path / "downloaded.txt"

        result = await downloader.download_with_progress("https://example.com/file", dest)

        assert result == dest
        assert dest.exists()
        assert dest.read_bytes() == b"test content"

    @pytest.mark.asyncio
    async def test_download_with_progress_calls_callback(self, tmp_path: Path) -> None:
        """Test that progress callbacks are called during download."""
        mock_client = Mock()
        mock_response = AsyncMock()
        mock_response.is_success.return_value = True
        mock_response.status = 200
        mock_response.headers = {"content-length": "12"}

        mock_client.request = AsyncMock(return_value=mock_response)

        async def mock_stream_generator(*args: tuple, **kwargs: dict) -> AsyncGenerator[bytes, None]:
            yield b"test"
            yield b" content"

        mock_client.stream = mock_stream_generator

        downloader = ToolDownloader(mock_client)
        callback = Mock()
        downloader.add_progress_callback(callback)

        dest = tmp_path / "downloaded.txt"
        await downloader.download_with_progress("https://example.com/file", dest)

        # Should be called at least once
        assert callback.call_count >= 1

    @pytest.mark.asyncio
    async def test_download_with_progress_http_error(self, tmp_path: Path) -> None:
        """Test download failure on HTTP error."""
        mock_client = Mock()
        mock_response = Mock()  # Use regular Mock, not AsyncMock
        mock_response.is_success = Mock(return_value=False)  # Make is_success a regular mock
        mock_response.status = 404
        mock_response.headers = {}

        mock_client.request = AsyncMock(return_value=mock_response)

        downloader = ToolDownloader(mock_client)
        dest = tmp_path / "downloaded.txt"

        with pytest.raises(DownloadError, match="HTTP 404 error"):
            await downloader.download_with_progress("https://example.com/file", dest)

    @pytest.mark.asyncio
    async def test_download_with_progress_creates_parent_dir(self, tmp_path: Path) -> None:
        """Test that download creates parent directories."""
        mock_client = Mock()
        mock_response = AsyncMock()
        mock_response.is_success.return_value = True
        mock_response.status = 200
        mock_response.headers = {"content-length": "7"}

        mock_client.request = AsyncMock(return_value=mock_response)

        async def mock_stream_generator(*args: tuple, **kwargs: dict) -> AsyncGenerator[bytes, None]:
            yield b"content"

        mock_client.stream = mock_stream_generator

        downloader = ToolDownloader(mock_client)
        dest = tmp_path / "nested" / "dir" / "file.txt"

        result = await downloader.download_with_progress("https://example.com/file", dest)

        assert result.parent.exists()
        assert result.exists()

    @pytest.mark.asyncio
    async def test_download_with_progress_checksum_success(self, tmp_path: Path) -> None:
        """Test download with valid checksum."""
        mock_client = Mock()
        mock_response = AsyncMock()
        mock_response.is_success.return_value = True
        mock_response.status = 200
        mock_response.headers = {"content-length": "12"}

        mock_client.request = AsyncMock(return_value=mock_response)

        async def mock_stream_generator(*args: tuple, **kwargs: dict) -> AsyncGenerator[bytes, None]:
            yield b"test content"

        mock_client.stream = mock_stream_generator

        downloader = ToolDownloader(mock_client)
        dest = tmp_path / "file.txt"

        expected_hash = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"

        result = await downloader.download_with_progress(
            "https://example.com/file", dest, checksum=expected_hash
        )

        assert result == dest
        assert dest.exists()

    @pytest.mark.asyncio
    async def test_download_with_progress_checksum_mismatch(self, tmp_path: Path) -> None:
        """Test download with invalid checksum."""
        mock_client = Mock()
        mock_response = AsyncMock()
        mock_response.is_success.return_value = True
        mock_response.status = 200
        mock_response.headers = {"content-length": "12"}

        mock_client.request = AsyncMock(return_value=mock_response)

        async def mock_stream_generator(*args: tuple, **kwargs: dict) -> AsyncGenerator[bytes, None]:
            yield b"test content"

        mock_client.stream = mock_stream_generator

        downloader = ToolDownloader(mock_client)
        dest = tmp_path / "file.txt"

        wrong_hash = "0000000000000000000000000000000000000000000000000000000000000000"

        with pytest.raises(DownloadError, match="Checksum mismatch"):
            await downloader.download_with_progress("https://example.com/file", dest, checksum=wrong_hash)

        # File should be deleted after checksum failure
        assert not dest.exists()

    @pytest.mark.asyncio
    async def test_download_with_progress_cleans_up_on_error(self, tmp_path: Path) -> None:
        """Test that partial download is cleaned up on error."""
        mock_client = Mock()
        mock_response = AsyncMock()
        mock_response.is_success.return_value = True
        mock_response.status = 200
        mock_response.headers = {"content-length": "12"}

        mock_client.request = AsyncMock(return_value=mock_response)

        # Mock stream that raises exception
        async def mock_stream_generator(*args: tuple, **kwargs: dict) -> AsyncGenerator[bytes, None]:
            yield b"test"
            raise Exception("Connection lost")

        mock_client.stream = mock_stream_generator

        downloader = ToolDownloader(mock_client)
        dest = tmp_path / "file.txt"

        with pytest.raises(DownloadError):
            await downloader.download_with_progress("https://example.com/file", dest)

        # File should be deleted after error
        assert not dest.exists()


# 🧱🏗️🔚
