"""Test-driven development tests for ToolDownloader.

Tests for downloading tools with progress, mirrors, and parallel downloads.
"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock, MagicMock, Mock, patch
import pytest

from provide.foundation.tools.downloader import (
    DownloadError,
    ToolDownloader,
)


class TestToolDownloader(FoundationTestCase):
    """Tests for ToolDownloader class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock UniversalClient."""
        client = MagicMock()
        # Make request method return an awaitable
        client.request = AsyncMock()
        # Make stream method return an async iterator
        client.stream = AsyncMock()
        return client

    @pytest.fixture
    def downloader(self, mock_client):
        """Create a ToolDownloader instance."""
        return ToolDownloader(mock_client)

    async def test_download_with_progress_success(self, downloader, mock_client, tmp_path) -> None:
        """Test successful download with progress reporting."""
        dest = tmp_path / "tool.tar.gz"
        url = "https://example.com/tool.tar.gz"

        # Mock response for headers request
        mock_response = MagicMock()
        mock_response.headers = {"content-length": "1000"}
        mock_client.request.return_value = mock_response

        # Mock streaming response
        async def mock_stream():
            chunks = [b"chunk1", b"chunk2", b"chunk3"]
            for chunk in chunks:
                yield chunk

        mock_client.stream.return_value = mock_stream()

        # Add progress callback
        progress_calls = []
        downloader.add_progress_callback(
            lambda d, t: progress_calls.append((d, t)),
        )

        result = await downloader.download_with_progress(url, dest)

        assert result == dest
        assert dest.exists()
        assert dest.read_bytes() == b"chunk1chunk2chunk3"

        # Check progress was reported
        assert len(progress_calls) == 3
        assert progress_calls[0] == (6, 1000)  # len("chunk1")
        assert progress_calls[1] == (12, 1000)  # len("chunk1chunk2")
        assert progress_calls[2] == (18, 1000)  # len("chunk1chunk2chunk3")

        mock_client.request.assert_called_once_with(url, "GET")
        mock_client.stream.assert_called_once_with(url, "GET")

    async def test_download_with_checksum_success(self, downloader, mock_client, tmp_path) -> None:
        """Test download with checksum verification."""
        dest = tmp_path / "tool.tar.gz"
        url = "https://example.com/tool.tar.gz"
        content = b"test content"

        # Mock response for headers request
        mock_response = MagicMock()
        mock_response.headers = {"content-length": str(len(content))}
        mock_client.request.return_value = mock_response

        # Mock streaming response
        async def mock_stream():
            yield content

        mock_client.stream.return_value = mock_stream()

        # Mock checksum verification
        with patch.object(downloader, "verify_checksum") as mock_verify:
            mock_verify.return_value = True

            result = await downloader.download_with_progress(
                url,
                dest,
                checksum="sha256:abc123",
            )

            assert result == dest
            assert dest.exists()
            mock_verify.assert_called_once_with(dest, "sha256:abc123")

    async def test_download_with_checksum_failure(self, downloader, mock_client, tmp_path) -> None:
        """Test download fails when checksum doesn't match."""
        dest = tmp_path / "tool.tar.gz"
        url = "https://example.com/tool.tar.gz"

        # Mock response for headers request
        mock_response = MagicMock()
        mock_response.headers = {}
        mock_client.request.return_value = mock_response

        # Mock streaming response
        async def mock_stream():
            yield b"content"

        mock_client.stream.return_value = mock_stream()

        # Mock checksum verification to fail
        with patch.object(downloader, "verify_checksum") as mock_verify:
            mock_verify.return_value = False

            with pytest.raises(DownloadError, match="Checksum mismatch"):
                await downloader.download_with_progress(
                    url,
                    dest,
                    checksum="sha256:wrong",
                )

            # File should be deleted
            assert not dest.exists()

    async def test_download_parallel(self, downloader, mock_client, tmp_path) -> None:
        """Test parallel downloads of multiple files."""
        urls = [
            ("https://example.com/file1.tar.gz", tmp_path / "file1.tar.gz"),
            ("https://example.com/file2.tar.gz", tmp_path / "file2.tar.gz"),
            ("https://example.com/file3.tar.gz", tmp_path / "file3.tar.gz"),
        ]

        # Mock download_with_progress to create files
        async def mock_download(url, dest, checksum=None):
            dest.write_text(f"Content of {url}")
            return dest

        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            results = await downloader.download_parallel(urls)

            assert len(results) == 3
            assert all(r.exists() for r in results)
            assert results[0].read_text() == "Content of https://example.com/file1.tar.gz"
            assert results[1].read_text() == "Content of https://example.com/file2.tar.gz"
            assert results[2].read_text() == "Content of https://example.com/file3.tar.gz"

    async def test_download_with_mirrors_first_success(self, downloader, mock_client, tmp_path) -> None:
        """Test download with mirrors succeeds on first mirror."""
        dest = tmp_path / "tool.tar.gz"
        mirrors = [
            "https://mirror1.com/tool.tar.gz",
            "https://mirror2.com/tool.tar.gz",
            "https://mirror3.com/tool.tar.gz",
        ]

        # First mirror succeeds
        async def mock_download(url, dest_path):
            return dest_path

        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            result = await downloader.download_with_mirrors(mirrors, dest)

            assert result == dest

    async def test_download_with_mirrors_fallback(self, downloader, mock_client, tmp_path) -> None:
        """Test download falls back to next mirror on failure."""
        dest = tmp_path / "tool.tar.gz"
        mirrors = [
            "https://mirror1.com/tool.tar.gz",
            "https://mirror2.com/tool.tar.gz",
            "https://mirror3.com/tool.tar.gz",
        ]

        # First two mirrors fail, third succeeds
        async def mock_download(url, dest_path):
            if url == mirrors[2]:
                return dest_path
            raise DownloadError(f"Failed to download from {url}")

        with patch.object(downloader, "download_with_progress", side_effect=mock_download):
            result = await downloader.download_with_mirrors(mirrors, dest)

            assert result == dest

    async def test_download_with_mirrors_all_fail(self, downloader, mock_client, tmp_path) -> None:
        """Test download fails when all mirrors fail."""
        dest = tmp_path / "tool.tar.gz"
        mirrors = [
            "https://mirror1.com/tool.tar.gz",
            "https://mirror2.com/tool.tar.gz",
        ]

        # All mirrors fail
        async def mock_download_fail(url, dest_path):
            raise DownloadError("Connection failed")

        with patch.object(downloader, "download_with_progress", side_effect=mock_download_fail):
            with pytest.raises(DownloadError, match="All mirrors failed"):
                await downloader.download_with_mirrors(mirrors, dest)

    def test_add_progress_callback(self, downloader) -> None:
        """Test adding progress callbacks."""
        callback1 = Mock()
        callback2 = Mock()

        downloader.add_progress_callback(callback1)
        downloader.add_progress_callback(callback2)

        # Simulate progress reporting
        downloader._report_progress(100, 1000)

        callback1.assert_called_once_with(100, 1000)
        callback2.assert_called_once_with(100, 1000)

    def test_verify_checksum_sha256(self, downloader, tmp_path) -> None:
        """Test SHA256 checksum verification."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        # SHA256 of "test content" is:
        # 6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72
        expected = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"

        result = downloader.verify_checksum(file_path, expected)
        assert result is True

        result = downloader.verify_checksum(file_path, "wrong_checksum")
        assert result is False

    async def test_download_no_content_length(self, downloader, mock_client, tmp_path) -> None:
        """Test download when server doesn't provide content-length."""
        dest = tmp_path / "tool.tar.gz"
        url = "https://example.com/tool.tar.gz"

        # Mock response for headers request (no content-length)
        mock_response = MagicMock()
        mock_response.headers = {}  # No content-length
        mock_client.request.return_value = mock_response

        # Mock streaming response
        async def mock_stream():
            chunks = [b"chunk1", b"chunk2"]
            for chunk in chunks:
                yield chunk

        mock_client.stream.return_value = mock_stream()

        result = await downloader.download_with_progress(url, dest)

        assert result == dest
        assert dest.read_bytes() == b"chunk1chunk2"

    async def test_download_empty_file(self, downloader, mock_client, tmp_path) -> None:
        """Test downloading an empty file."""
        dest = tmp_path / "empty.txt"
        url = "https://example.com/empty.txt"

        # Mock response for headers request
        mock_response = MagicMock()
        mock_response.headers = {"content-length": "0"}
        mock_client.request.return_value = mock_response

        # Mock streaming response (empty)
        async def mock_stream():
            return
            yield  # Never executed

        mock_client.stream.return_value = mock_stream()

        result = await downloader.download_with_progress(url, dest)

        assert result == dest
        assert dest.exists()
        assert dest.read_bytes() == b""

    async def test_download_network_error(self, downloader, mock_client, tmp_path) -> None:
        """Test handling network errors during download."""
        dest = tmp_path / "tool.tar.gz"
        url = "https://example.com/tool.tar.gz"

        # Mock network error in the request phase
        mock_client.request.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Network error"):
            await downloader.download_with_progress(url, dest)
