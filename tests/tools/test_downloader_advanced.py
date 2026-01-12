#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ToolDownloader advanced features.

Tests parallel downloads and mirror fallback functionality."""

from __future__ import annotations

from pathlib import Path

from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.tools.downloader import DownloadError, ToolDownloader


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


# 🧱🏗️🔚
