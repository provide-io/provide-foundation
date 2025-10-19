"""Comprehensive tests for tool downloader.

Tests all functionality in tools/downloader.py including download orchestration,
progress reporting, parallel downloads, and mirror fallback.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

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
        mock_client.stream = AsyncMock()

        # Mock streaming chunks
        async def mock_stream_generator(*args: tuple, **kwargs: dict) -> AsyncGenerator[bytes, None]:
            for chunk in [b"test", b" ", b"content"]:
                yield chunk

        mock_client.stream.return_value = mock_stream_generator()

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

        mock_client.stream = AsyncMock(return_value=mock_stream_generator())

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
        mock_response = AsyncMock()
        mock_response.is_success.return_value = False
        mock_response.status = 404

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

        mock_client.stream = AsyncMock(return_value=mock_stream_generator())

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

        mock_client.stream = AsyncMock(return_value=mock_stream_generator())

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

        mock_client.stream = AsyncMock(return_value=mock_stream_generator())

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

        mock_client.stream = AsyncMock(return_value=mock_stream_generator())

        downloader = ToolDownloader(mock_client)
        dest = tmp_path / "file.txt"

        with pytest.raises(DownloadError):
            await downloader.download_with_progress("https://example.com/file", dest)

        # File should be deleted after error
        assert not dest.exists()


class TestDownloadParallel:
    """Tests for download_parallel method."""

    @pytest.mark.asyncio
    async def test_download_parallel_success(self, tmp_path: Path) -> None:
        """Test successful parallel downloads."""
        mock_client = Mock()

        async def mock_download(url: str, dest: Path, checksum: str | None = None) -> Path:
            dest.write_text(f"content from {url}")
            return dest

        downloader = ToolDownloader(mock_client)

        # Patch download_with_progress
        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            urls = [
                ("https://example.com/file1", tmp_path / "file1.txt"),
                ("https://example.com/file2", tmp_path / "file2.txt"),
                ("https://example.com/file3", tmp_path / "file3.txt"),
            ]

            results = await downloader.download_parallel(urls)

            assert len(results) == 3
            for dest in results:
                assert dest.exists()

    @pytest.mark.asyncio
    async def test_download_parallel_some_failures(self, tmp_path: Path) -> None:
        """Test parallel downloads with some failures."""
        mock_client = Mock()

        async def mock_download(url: str, dest: Path, checksum: str | None = None) -> Path:
            if "fail" in url:
                raise DownloadError(f"Failed to download {url}")
            dest.write_text(f"content from {url}")
            return dest

        downloader = ToolDownloader(mock_client)

        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            urls = [
                ("https://example.com/file1", tmp_path / "file1.txt"),
                ("https://example.com/fail2", tmp_path / "file2.txt"),
                ("https://example.com/file3", tmp_path / "file3.txt"),
            ]

            with pytest.raises(DownloadError, match="Some downloads failed"):
                await downloader.download_parallel(urls)


class TestDownloadWithMirrors:
    """Tests for download_with_mirrors method."""

    @pytest.mark.asyncio
    async def test_download_with_mirrors_first_succeeds(self, tmp_path: Path) -> None:
        """Test successful download from first mirror."""
        mock_client = Mock()

        async def mock_download(url: str, dest: Path, checksum: str | None = None) -> Path:
            dest.write_text(f"content from {url}")
            return dest

        downloader = ToolDownloader(mock_client)

        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            mirrors = [
                "https://mirror1.example.com/file",
                "https://mirror2.example.com/file",
            ]

            dest = tmp_path / "file.txt"
            result = await downloader.download_with_mirrors(mirrors, dest)

            assert result == dest
            assert dest.exists()
            assert "mirror1" in dest.read_text()

    @pytest.mark.asyncio
    async def test_download_with_mirrors_fallback(self, tmp_path: Path) -> None:
        """Test fallback to second mirror after first fails."""
        mock_client = Mock()

        call_count = 0

        async def mock_download(url: str, dest: Path, checksum: str | None = None) -> Path:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise DownloadError("First mirror failed")
            dest.write_text(f"content from {url}")
            return dest

        downloader = ToolDownloader(mock_client)

        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            mirrors = [
                "https://mirror1.example.com/file",
                "https://mirror2.example.com/file",
            ]

            dest = tmp_path / "file.txt"
            result = await downloader.download_with_mirrors(mirrors, dest)

            assert result == dest
            assert dest.exists()
            assert "mirror2" in dest.read_text()

    @pytest.mark.asyncio
    async def test_download_with_mirrors_all_fail(self, tmp_path: Path) -> None:
        """Test when all mirrors fail."""
        mock_client = Mock()

        async def mock_download(url: str, dest: Path, checksum: str | None = None) -> Path:
            raise DownloadError(f"Mirror {url} failed")

        downloader = ToolDownloader(mock_client)

        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            mirrors = [
                "https://mirror1.example.com/file",
                "https://mirror2.example.com/file",
            ]

            dest = tmp_path / "file.txt"

            with pytest.raises(DownloadError, match="All mirrors failed"):
                await downloader.download_with_mirrors(mirrors, dest)

    @pytest.mark.asyncio
    async def test_download_with_mirrors_no_mirrors(self, tmp_path: Path) -> None:
        """Test error when no mirrors provided."""
        mock_client = Mock()
        downloader = ToolDownloader(mock_client)

        dest = tmp_path / "file.txt"

        with pytest.raises(DownloadError, match="No mirrors provided"):
            await downloader.download_with_mirrors([], dest)

    @pytest.mark.asyncio
    async def test_download_with_mirrors_cleans_up_partial(self, tmp_path: Path) -> None:
        """Test that partial downloads are cleaned up between mirror attempts."""
        mock_client = Mock()

        call_count = 0

        async def mock_download(url: str, dest: Path, checksum: str | None = None) -> Path:
            nonlocal call_count
            call_count += 1

            # Create partial file
            dest.write_text("partial content")

            if call_count == 1:
                raise DownloadError("First mirror failed")

            # Second attempt succeeds
            dest.write_text("complete content")
            return dest

        downloader = ToolDownloader(mock_client)

        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            mirrors = [
                "https://mirror1.example.com/file",
                "https://mirror2.example.com/file",
            ]

            dest = tmp_path / "file.txt"
            result = await downloader.download_with_mirrors(mirrors, dest)

            assert result == dest
            assert dest.read_text() == "complete content"


# <3 🧱🤝🔧🪄
