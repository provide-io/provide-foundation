#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from pathlib import Path

from provide.foundation.crypto.hashing import hash_file
from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger
from provide.foundation.resilience import RetryExecutor, RetryPolicy
from provide.foundation.transport import UniversalClient

"""Tool download orchestration with progress reporting.

Provides capabilities for downloading tools with progress tracking,
parallel downloads, and mirror support.
"""

log = get_logger(__name__)


class DownloadError(FoundationError):
    """Raised when download fails."""


class ToolDownloader:
    """Advanced download capabilities for tools.

    Features:
    - Progress reporting with callbacks
    - Parallel downloads for multiple files
    - Mirror fallback support
    - Checksum verification

    Attributes:
        client: Transport client for HTTP requests.
        progress_callbacks: List of progress callback functions.
        retry_policy: Policy for retry behavior on downloads.

    """

    def __init__(
        self,
        client: UniversalClient,
        time_source: Callable[[], float] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize the downloader.

        Args:
            client: Universal client for making HTTP requests.
            time_source: Optional time source for testing (defaults to time.time).
            async_sleep_func: Optional async sleep function for testing (defaults to asyncio.sleep).

        """
        self.client = client
        self.progress_callbacks: list[Callable[[int, int], None]] = []

        # Create retry policy for downloads
        self.retry_policy = RetryPolicy(max_attempts=3, base_delay=1.0)
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def add_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """Add a progress callback.

        Args:
            callback: Function that receives (downloaded_bytes, total_bytes).

        """
        self.progress_callbacks.append(callback)

    def _report_progress(self, downloaded: int, total: int) -> None:
        """Report progress to all callbacks.

        Args:
            downloaded: Bytes downloaded so far.
            total: Total bytes to download (0 if unknown).

        """
        for callback in self.progress_callbacks:
            try:
                callback(downloaded, total)
            except Exception as e:
                log.warning(f"Progress callback failed: {e}")

    async def download_with_progress(self, url: str, dest: Path, checksum: str | None = None) -> Path:
        """Download a file with progress reporting.

        Args:
            url: URL to download from.
            dest: Destination file path.
            checksum: Optional checksum for verification.

        Returns:
            Path to the downloaded file.

        Raises:
            DownloadError: If download or verification fails.

        """

        async def _download() -> Path:
            """Inner download function that will be retried."""
            log.debug(f"Downloading {url} to {dest}")

            # Ensure parent directory exists
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Stream download with progress
            total_size = 0
            downloaded = 0

            try:
                # Use the client to make a request first to get headers
                response = await self.client.request(url, "GET")

                # Check for HTTP errors (4xx/5xx status codes)
                if not response.is_success():
                    raise DownloadError(f"HTTP {response.status} error for {url}")

                total_size = int(response.headers.get("content-length", 0))

                # Write to file and report progress
                with dest.open("wb") as f:
                    async for chunk in self.client.stream(url, "GET"):
                        f.write(chunk)
                        downloaded += len(chunk)
                        self._report_progress(downloaded, total_size)

            except Exception as e:
                if dest.exists():
                    dest.unlink()
                raise DownloadError(f"Failed to download {url}: {e}") from e

            # Verify checksum if provided
            if checksum and not self.verify_checksum(dest, checksum):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    def verify_checksum(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Uses Foundation's hash_file() for consistent hashing behavior.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).

        Returns:
            True if checksum matches, False otherwise.

        """
        # Use Foundation's hash_file with SHA256 (default)
        actual = hash_file(file_path, algorithm="sha256")
        return actual == expected

    async def download_parallel(self, urls: list[tuple[str, Path]]) -> list[Path]:
        """Download multiple files in parallel.

        Args:
            urls: List of (url, destination) tuples.

        Returns:
            List of downloaded file paths in the same order as input.

        Raises:
            DownloadError: If any download fails.

        """
        import asyncio

        errors = []

        # Create tasks for all downloads
        tasks = [self.download_with_progress(url, dest) for url, dest in urls]

        # Execute downloads concurrently
        results = []
        task_results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(task_results):
            url, _dest = urls[i]
            if isinstance(result, Exception):
                errors.append((url, result))
                log.error(f"Failed to download {url}: {result}")
            else:
                results.append(result)

        if errors:
            raise DownloadError(f"Some downloads failed: {errors}")

        return results  # type: ignore[return-value]

    async def download_with_mirrors(self, mirrors: list[str], dest: Path) -> Path:
        """Try multiple mirrors until one succeeds using fallback pattern.

        Args:
            mirrors: List of mirror URLs to try.
            dest: Destination file path.

        Returns:
            Path to downloaded file.

        Raises:
            DownloadError: If all mirrors fail.

        """
        if not mirrors:
            raise DownloadError("No mirrors provided")

        last_error = None

        # Try each mirror in sequence
        for mirror_url in mirrors:
            try:
                log.debug(f"Trying mirror: {mirror_url}")
                return await self.download_with_progress(mirror_url, dest)
            except Exception as e:
                last_error = e
                log.warning(f"Mirror {mirror_url} failed: {e}")
                # Clean up any partial download
                if dest.exists():
                    dest.unlink()

        # All mirrors failed
        raise DownloadError(f"All mirrors failed: {last_error}") from last_error


# 🧱🏗️🔚
