# provide/foundation/tools/downloader.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁToolDownloaderǁ__init____mutmut_orig(
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

    def xǁToolDownloaderǁ__init____mutmut_1(
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
        self.client = None
        self.progress_callbacks: list[Callable[[int, int], None]] = []

        # Create retry policy for downloads
        self.retry_policy = RetryPolicy(max_attempts=3, base_delay=1.0)
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_2(
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
        self.progress_callbacks: list[Callable[[int, int], None]] = None

        # Create retry policy for downloads
        self.retry_policy = RetryPolicy(max_attempts=3, base_delay=1.0)
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_3(
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
        self.retry_policy = None
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_4(
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
        self.retry_policy = RetryPolicy(max_attempts=None, base_delay=1.0)
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_5(
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
        self.retry_policy = RetryPolicy(max_attempts=3, base_delay=None)
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_6(
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
        self.retry_policy = RetryPolicy(base_delay=1.0)
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_7(
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
        self.retry_policy = RetryPolicy(
            max_attempts=3,
        )
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_8(
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
        self.retry_policy = RetryPolicy(max_attempts=4, base_delay=1.0)
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_9(
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
        self.retry_policy = RetryPolicy(max_attempts=3, base_delay=2.0)
        self._retry_executor = RetryExecutor(
            self.retry_policy,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_10(
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
        self._retry_executor = None

    def xǁToolDownloaderǁ__init____mutmut_11(
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
            None,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_12(
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
            time_source=None,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_13(
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
            async_sleep_func=None,
        )

    def xǁToolDownloaderǁ__init____mutmut_14(
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
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_15(
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
            async_sleep_func=async_sleep_func,
        )

    def xǁToolDownloaderǁ__init____mutmut_16(
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
        )

    xǁToolDownloaderǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolDownloaderǁ__init____mutmut_1": xǁToolDownloaderǁ__init____mutmut_1,
        "xǁToolDownloaderǁ__init____mutmut_2": xǁToolDownloaderǁ__init____mutmut_2,
        "xǁToolDownloaderǁ__init____mutmut_3": xǁToolDownloaderǁ__init____mutmut_3,
        "xǁToolDownloaderǁ__init____mutmut_4": xǁToolDownloaderǁ__init____mutmut_4,
        "xǁToolDownloaderǁ__init____mutmut_5": xǁToolDownloaderǁ__init____mutmut_5,
        "xǁToolDownloaderǁ__init____mutmut_6": xǁToolDownloaderǁ__init____mutmut_6,
        "xǁToolDownloaderǁ__init____mutmut_7": xǁToolDownloaderǁ__init____mutmut_7,
        "xǁToolDownloaderǁ__init____mutmut_8": xǁToolDownloaderǁ__init____mutmut_8,
        "xǁToolDownloaderǁ__init____mutmut_9": xǁToolDownloaderǁ__init____mutmut_9,
        "xǁToolDownloaderǁ__init____mutmut_10": xǁToolDownloaderǁ__init____mutmut_10,
        "xǁToolDownloaderǁ__init____mutmut_11": xǁToolDownloaderǁ__init____mutmut_11,
        "xǁToolDownloaderǁ__init____mutmut_12": xǁToolDownloaderǁ__init____mutmut_12,
        "xǁToolDownloaderǁ__init____mutmut_13": xǁToolDownloaderǁ__init____mutmut_13,
        "xǁToolDownloaderǁ__init____mutmut_14": xǁToolDownloaderǁ__init____mutmut_14,
        "xǁToolDownloaderǁ__init____mutmut_15": xǁToolDownloaderǁ__init____mutmut_15,
        "xǁToolDownloaderǁ__init____mutmut_16": xǁToolDownloaderǁ__init____mutmut_16,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolDownloaderǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁToolDownloaderǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁToolDownloaderǁ__init____mutmut_orig)
    xǁToolDownloaderǁ__init____mutmut_orig.__name__ = "xǁToolDownloaderǁ__init__"

    def xǁToolDownloaderǁadd_progress_callback__mutmut_orig(
        self, callback: Callable[[int, int], None]
    ) -> None:
        """Add a progress callback.

        Args:
            callback: Function that receives (downloaded_bytes, total_bytes).

        """
        self.progress_callbacks.append(callback)

    def xǁToolDownloaderǁadd_progress_callback__mutmut_1(self, callback: Callable[[int, int], None]) -> None:
        """Add a progress callback.

        Args:
            callback: Function that receives (downloaded_bytes, total_bytes).

        """
        self.progress_callbacks.append(None)

    xǁToolDownloaderǁadd_progress_callback__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolDownloaderǁadd_progress_callback__mutmut_1": xǁToolDownloaderǁadd_progress_callback__mutmut_1
    }

    def add_progress_callback(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolDownloaderǁadd_progress_callback__mutmut_orig"),
            object.__getattribute__(self, "xǁToolDownloaderǁadd_progress_callback__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    add_progress_callback.__signature__ = _mutmut_signature(
        xǁToolDownloaderǁadd_progress_callback__mutmut_orig
    )
    xǁToolDownloaderǁadd_progress_callback__mutmut_orig.__name__ = "xǁToolDownloaderǁadd_progress_callback"

    def xǁToolDownloaderǁ_report_progress__mutmut_orig(self, downloaded: int, total: int) -> None:
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

    def xǁToolDownloaderǁ_report_progress__mutmut_1(self, downloaded: int, total: int) -> None:
        """Report progress to all callbacks.

        Args:
            downloaded: Bytes downloaded so far.
            total: Total bytes to download (0 if unknown).

        """
        for callback in self.progress_callbacks:
            try:
                callback(None, total)
            except Exception as e:
                log.warning(f"Progress callback failed: {e}")

    def xǁToolDownloaderǁ_report_progress__mutmut_2(self, downloaded: int, total: int) -> None:
        """Report progress to all callbacks.

        Args:
            downloaded: Bytes downloaded so far.
            total: Total bytes to download (0 if unknown).

        """
        for callback in self.progress_callbacks:
            try:
                callback(downloaded, None)
            except Exception as e:
                log.warning(f"Progress callback failed: {e}")

    def xǁToolDownloaderǁ_report_progress__mutmut_3(self, downloaded: int, total: int) -> None:
        """Report progress to all callbacks.

        Args:
            downloaded: Bytes downloaded so far.
            total: Total bytes to download (0 if unknown).

        """
        for callback in self.progress_callbacks:
            try:
                callback(total)
            except Exception as e:
                log.warning(f"Progress callback failed: {e}")

    def xǁToolDownloaderǁ_report_progress__mutmut_4(self, downloaded: int, total: int) -> None:
        """Report progress to all callbacks.

        Args:
            downloaded: Bytes downloaded so far.
            total: Total bytes to download (0 if unknown).

        """
        for callback in self.progress_callbacks:
            try:
                callback(
                    downloaded,
                )
            except Exception as e:
                log.warning(f"Progress callback failed: {e}")

    def xǁToolDownloaderǁ_report_progress__mutmut_5(self, downloaded: int, total: int) -> None:
        """Report progress to all callbacks.

        Args:
            downloaded: Bytes downloaded so far.
            total: Total bytes to download (0 if unknown).

        """
        for callback in self.progress_callbacks:
            try:
                callback(downloaded, total)
            except Exception as e:
                log.warning(None)

    xǁToolDownloaderǁ_report_progress__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolDownloaderǁ_report_progress__mutmut_1": xǁToolDownloaderǁ_report_progress__mutmut_1,
        "xǁToolDownloaderǁ_report_progress__mutmut_2": xǁToolDownloaderǁ_report_progress__mutmut_2,
        "xǁToolDownloaderǁ_report_progress__mutmut_3": xǁToolDownloaderǁ_report_progress__mutmut_3,
        "xǁToolDownloaderǁ_report_progress__mutmut_4": xǁToolDownloaderǁ_report_progress__mutmut_4,
        "xǁToolDownloaderǁ_report_progress__mutmut_5": xǁToolDownloaderǁ_report_progress__mutmut_5,
    }

    def _report_progress(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolDownloaderǁ_report_progress__mutmut_orig"),
            object.__getattribute__(self, "xǁToolDownloaderǁ_report_progress__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _report_progress.__signature__ = _mutmut_signature(xǁToolDownloaderǁ_report_progress__mutmut_orig)
    xǁToolDownloaderǁ_report_progress__mutmut_orig.__name__ = "xǁToolDownloaderǁ_report_progress"

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_orig(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_1(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            log.debug(None)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_2(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            dest.parent.mkdir(parents=None, exist_ok=True)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_3(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            dest.parent.mkdir(parents=True, exist_ok=None)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_4(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            dest.parent.mkdir(exist_ok=True)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_5(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            dest.parent.mkdir(
                parents=True,
            )

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_6(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            dest.parent.mkdir(parents=False, exist_ok=True)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_7(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            dest.parent.mkdir(parents=True, exist_ok=False)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_8(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            total_size = None
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_9(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            total_size = 1
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_10(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            downloaded = None

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_11(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            downloaded = 1

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_12(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                response = None

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_13(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                response = await self.client.request(None, "GET")

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_14(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                response = await self.client.request(url, None)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_15(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                response = await self.client.request("GET")

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_16(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                response = await self.client.request(
                    url,
                )

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_17(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                response = await self.client.request(url, "XXGETXX")

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_18(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                response = await self.client.request(url, "get")

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_19(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                if response.is_success():
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_20(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                    raise DownloadError(None)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_21(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = None

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_22(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = int(None)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_23(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = int(response.headers.get(None, 0))

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_24(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = int(response.headers.get("content-length", None))

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_25(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = int(response.headers.get(0))

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_26(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = int(
                    response.headers.get(
                        "content-length",
                    )
                )

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_27(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = int(response.headers.get("XXcontent-lengthXX", 0))

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_28(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = int(response.headers.get("CONTENT-LENGTH", 0))

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_29(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

                total_size = int(response.headers.get("content-length", 1))

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_30(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                with dest.open(None) as f:
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_31(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                with dest.open("XXwbXX") as f:
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_32(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                with dest.open("WB") as f:
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_33(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                    async for chunk in self.client.stream(None, "GET"):
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_34(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                    async for chunk in self.client.stream(url, None):
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_35(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                    async for chunk in self.client.stream("GET"):
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_36(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                    async for chunk in self.client.stream(
                        url,
                    ):
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_37(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                    async for chunk in self.client.stream(url, "XXGETXX"):
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_38(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                    async for chunk in self.client.stream(url, "get"):
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_39(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                        f.write(None)
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_40(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                        downloaded = len(chunk)
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_41(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                        downloaded -= len(chunk)
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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_42(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                        self._report_progress(None, total_size)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_43(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                        self._report_progress(downloaded, None)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_44(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                        self._report_progress(total_size)

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_45(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                        self._report_progress(
                            downloaded,
                        )

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

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_46(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                raise DownloadError(None) from e

            # Verify checksum if provided
            if checksum and not self.verify_checksum(dest, checksum):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_47(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            if checksum or not self.verify_checksum(dest, checksum):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_48(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            if checksum and self.verify_checksum(dest, checksum):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_49(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            if checksum and not self.verify_checksum(None, checksum):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_50(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            if checksum and not self.verify_checksum(dest, None):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_51(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            if checksum and not self.verify_checksum(checksum):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_52(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
            if checksum and not self.verify_checksum(
                dest,
            ):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_53(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
                raise DownloadError(None)

            log.info(f"Downloaded {url} successfully")
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_54(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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

            log.info(None)
            return dest

        # Execute with retry
        return await self._retry_executor.execute_async(_download)

    async def xǁToolDownloaderǁdownload_with_progress__mutmut_55(
        self, url: str, dest: Path, checksum: str | None = None
    ) -> Path:
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
        return await self._retry_executor.execute_async(None)

    xǁToolDownloaderǁdownload_with_progress__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolDownloaderǁdownload_with_progress__mutmut_1": xǁToolDownloaderǁdownload_with_progress__mutmut_1,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_2": xǁToolDownloaderǁdownload_with_progress__mutmut_2,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_3": xǁToolDownloaderǁdownload_with_progress__mutmut_3,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_4": xǁToolDownloaderǁdownload_with_progress__mutmut_4,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_5": xǁToolDownloaderǁdownload_with_progress__mutmut_5,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_6": xǁToolDownloaderǁdownload_with_progress__mutmut_6,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_7": xǁToolDownloaderǁdownload_with_progress__mutmut_7,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_8": xǁToolDownloaderǁdownload_with_progress__mutmut_8,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_9": xǁToolDownloaderǁdownload_with_progress__mutmut_9,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_10": xǁToolDownloaderǁdownload_with_progress__mutmut_10,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_11": xǁToolDownloaderǁdownload_with_progress__mutmut_11,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_12": xǁToolDownloaderǁdownload_with_progress__mutmut_12,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_13": xǁToolDownloaderǁdownload_with_progress__mutmut_13,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_14": xǁToolDownloaderǁdownload_with_progress__mutmut_14,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_15": xǁToolDownloaderǁdownload_with_progress__mutmut_15,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_16": xǁToolDownloaderǁdownload_with_progress__mutmut_16,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_17": xǁToolDownloaderǁdownload_with_progress__mutmut_17,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_18": xǁToolDownloaderǁdownload_with_progress__mutmut_18,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_19": xǁToolDownloaderǁdownload_with_progress__mutmut_19,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_20": xǁToolDownloaderǁdownload_with_progress__mutmut_20,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_21": xǁToolDownloaderǁdownload_with_progress__mutmut_21,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_22": xǁToolDownloaderǁdownload_with_progress__mutmut_22,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_23": xǁToolDownloaderǁdownload_with_progress__mutmut_23,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_24": xǁToolDownloaderǁdownload_with_progress__mutmut_24,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_25": xǁToolDownloaderǁdownload_with_progress__mutmut_25,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_26": xǁToolDownloaderǁdownload_with_progress__mutmut_26,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_27": xǁToolDownloaderǁdownload_with_progress__mutmut_27,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_28": xǁToolDownloaderǁdownload_with_progress__mutmut_28,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_29": xǁToolDownloaderǁdownload_with_progress__mutmut_29,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_30": xǁToolDownloaderǁdownload_with_progress__mutmut_30,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_31": xǁToolDownloaderǁdownload_with_progress__mutmut_31,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_32": xǁToolDownloaderǁdownload_with_progress__mutmut_32,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_33": xǁToolDownloaderǁdownload_with_progress__mutmut_33,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_34": xǁToolDownloaderǁdownload_with_progress__mutmut_34,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_35": xǁToolDownloaderǁdownload_with_progress__mutmut_35,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_36": xǁToolDownloaderǁdownload_with_progress__mutmut_36,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_37": xǁToolDownloaderǁdownload_with_progress__mutmut_37,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_38": xǁToolDownloaderǁdownload_with_progress__mutmut_38,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_39": xǁToolDownloaderǁdownload_with_progress__mutmut_39,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_40": xǁToolDownloaderǁdownload_with_progress__mutmut_40,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_41": xǁToolDownloaderǁdownload_with_progress__mutmut_41,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_42": xǁToolDownloaderǁdownload_with_progress__mutmut_42,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_43": xǁToolDownloaderǁdownload_with_progress__mutmut_43,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_44": xǁToolDownloaderǁdownload_with_progress__mutmut_44,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_45": xǁToolDownloaderǁdownload_with_progress__mutmut_45,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_46": xǁToolDownloaderǁdownload_with_progress__mutmut_46,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_47": xǁToolDownloaderǁdownload_with_progress__mutmut_47,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_48": xǁToolDownloaderǁdownload_with_progress__mutmut_48,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_49": xǁToolDownloaderǁdownload_with_progress__mutmut_49,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_50": xǁToolDownloaderǁdownload_with_progress__mutmut_50,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_51": xǁToolDownloaderǁdownload_with_progress__mutmut_51,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_52": xǁToolDownloaderǁdownload_with_progress__mutmut_52,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_53": xǁToolDownloaderǁdownload_with_progress__mutmut_53,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_54": xǁToolDownloaderǁdownload_with_progress__mutmut_54,
        "xǁToolDownloaderǁdownload_with_progress__mutmut_55": xǁToolDownloaderǁdownload_with_progress__mutmut_55,
    }

    def download_with_progress(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolDownloaderǁdownload_with_progress__mutmut_orig"),
            object.__getattribute__(self, "xǁToolDownloaderǁdownload_with_progress__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    download_with_progress.__signature__ = _mutmut_signature(
        xǁToolDownloaderǁdownload_with_progress__mutmut_orig
    )
    xǁToolDownloaderǁdownload_with_progress__mutmut_orig.__name__ = "xǁToolDownloaderǁdownload_with_progress"

    def xǁToolDownloaderǁverify_checksum__mutmut_orig(self, file_path: Path, expected: str) -> bool:
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

    def xǁToolDownloaderǁverify_checksum__mutmut_1(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Uses Foundation's hash_file() for consistent hashing behavior.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).

        Returns:
            True if checksum matches, False otherwise.

        """
        # Use Foundation's hash_file with SHA256 (default)
        actual = None
        return actual == expected

    def xǁToolDownloaderǁverify_checksum__mutmut_2(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Uses Foundation's hash_file() for consistent hashing behavior.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).

        Returns:
            True if checksum matches, False otherwise.

        """
        # Use Foundation's hash_file with SHA256 (default)
        actual = hash_file(None, algorithm="sha256")
        return actual == expected

    def xǁToolDownloaderǁverify_checksum__mutmut_3(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Uses Foundation's hash_file() for consistent hashing behavior.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).

        Returns:
            True if checksum matches, False otherwise.

        """
        # Use Foundation's hash_file with SHA256 (default)
        actual = hash_file(file_path, algorithm=None)
        return actual == expected

    def xǁToolDownloaderǁverify_checksum__mutmut_4(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Uses Foundation's hash_file() for consistent hashing behavior.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).

        Returns:
            True if checksum matches, False otherwise.

        """
        # Use Foundation's hash_file with SHA256 (default)
        actual = hash_file(algorithm="sha256")
        return actual == expected

    def xǁToolDownloaderǁverify_checksum__mutmut_5(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Uses Foundation's hash_file() for consistent hashing behavior.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).

        Returns:
            True if checksum matches, False otherwise.

        """
        # Use Foundation's hash_file with SHA256 (default)
        actual = hash_file(
            file_path,
        )
        return actual == expected

    def xǁToolDownloaderǁverify_checksum__mutmut_6(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Uses Foundation's hash_file() for consistent hashing behavior.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).

        Returns:
            True if checksum matches, False otherwise.

        """
        # Use Foundation's hash_file with SHA256 (default)
        actual = hash_file(file_path, algorithm="XXsha256XX")
        return actual == expected

    def xǁToolDownloaderǁverify_checksum__mutmut_7(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Uses Foundation's hash_file() for consistent hashing behavior.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).

        Returns:
            True if checksum matches, False otherwise.

        """
        # Use Foundation's hash_file with SHA256 (default)
        actual = hash_file(file_path, algorithm="SHA256")
        return actual == expected

    def xǁToolDownloaderǁverify_checksum__mutmut_8(self, file_path: Path, expected: str) -> bool:
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
        return actual != expected

    xǁToolDownloaderǁverify_checksum__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolDownloaderǁverify_checksum__mutmut_1": xǁToolDownloaderǁverify_checksum__mutmut_1,
        "xǁToolDownloaderǁverify_checksum__mutmut_2": xǁToolDownloaderǁverify_checksum__mutmut_2,
        "xǁToolDownloaderǁverify_checksum__mutmut_3": xǁToolDownloaderǁverify_checksum__mutmut_3,
        "xǁToolDownloaderǁverify_checksum__mutmut_4": xǁToolDownloaderǁverify_checksum__mutmut_4,
        "xǁToolDownloaderǁverify_checksum__mutmut_5": xǁToolDownloaderǁverify_checksum__mutmut_5,
        "xǁToolDownloaderǁverify_checksum__mutmut_6": xǁToolDownloaderǁverify_checksum__mutmut_6,
        "xǁToolDownloaderǁverify_checksum__mutmut_7": xǁToolDownloaderǁverify_checksum__mutmut_7,
        "xǁToolDownloaderǁverify_checksum__mutmut_8": xǁToolDownloaderǁverify_checksum__mutmut_8,
    }

    def verify_checksum(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolDownloaderǁverify_checksum__mutmut_orig"),
            object.__getattribute__(self, "xǁToolDownloaderǁverify_checksum__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    verify_checksum.__signature__ = _mutmut_signature(xǁToolDownloaderǁverify_checksum__mutmut_orig)
    xǁToolDownloaderǁverify_checksum__mutmut_orig.__name__ = "xǁToolDownloaderǁverify_checksum"

    async def xǁToolDownloaderǁdownload_parallel__mutmut_orig(
        self, urls: list[tuple[str, Path]]
    ) -> list[Path]:
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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_1(self, urls: list[tuple[str, Path]]) -> list[Path]:
        """Download multiple files in parallel.

        Args:
            urls: List of (url, destination) tuples.

        Returns:
            List of downloaded file paths in the same order as input.

        Raises:
            DownloadError: If any download fails.

        """
        import asyncio

        errors = None

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_2(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        tasks = None

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_3(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        tasks = [self.download_with_progress(None, dest) for url, dest in urls]

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_4(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        tasks = [self.download_with_progress(url, None) for url, dest in urls]

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_5(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        tasks = [self.download_with_progress(dest) for url, dest in urls]

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_6(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        tasks = [
            self.download_with_progress(
                url,
            )
            for url, dest in urls
        ]

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_7(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        results = None
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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_8(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        task_results = None

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_9(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        task_results = await asyncio.gather(*tasks, return_exceptions=None)

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_10(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        task_results = await asyncio.gather(return_exceptions=True)

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_11(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        task_results = await asyncio.gather(
            *tasks,
        )

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_12(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
        task_results = await asyncio.gather(*tasks, return_exceptions=False)

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

    async def xǁToolDownloaderǁdownload_parallel__mutmut_13(self, urls: list[tuple[str, Path]]) -> list[Path]:
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

        for i, result in enumerate(None):
            url, _dest = urls[i]
            if isinstance(result, Exception):
                errors.append((url, result))
                log.error(f"Failed to download {url}: {result}")
            else:
                results.append(result)

        if errors:
            raise DownloadError(f"Some downloads failed: {errors}")

        return results  # type: ignore[return-value]

    async def xǁToolDownloaderǁdownload_parallel__mutmut_14(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
            url, _dest = None
            if isinstance(result, Exception):
                errors.append((url, result))
                log.error(f"Failed to download {url}: {result}")
            else:
                results.append(result)

        if errors:
            raise DownloadError(f"Some downloads failed: {errors}")

        return results  # type: ignore[return-value]

    async def xǁToolDownloaderǁdownload_parallel__mutmut_15(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
                errors.append(None)
                log.error(f"Failed to download {url}: {result}")
            else:
                results.append(result)

        if errors:
            raise DownloadError(f"Some downloads failed: {errors}")

        return results  # type: ignore[return-value]

    async def xǁToolDownloaderǁdownload_parallel__mutmut_16(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
                log.error(None)
            else:
                results.append(result)

        if errors:
            raise DownloadError(f"Some downloads failed: {errors}")

        return results  # type: ignore[return-value]

    async def xǁToolDownloaderǁdownload_parallel__mutmut_17(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
                results.append(None)

        if errors:
            raise DownloadError(f"Some downloads failed: {errors}")

        return results  # type: ignore[return-value]

    async def xǁToolDownloaderǁdownload_parallel__mutmut_18(self, urls: list[tuple[str, Path]]) -> list[Path]:
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
            raise DownloadError(None)

        return results  # type: ignore[return-value]

    xǁToolDownloaderǁdownload_parallel__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolDownloaderǁdownload_parallel__mutmut_1": xǁToolDownloaderǁdownload_parallel__mutmut_1,
        "xǁToolDownloaderǁdownload_parallel__mutmut_2": xǁToolDownloaderǁdownload_parallel__mutmut_2,
        "xǁToolDownloaderǁdownload_parallel__mutmut_3": xǁToolDownloaderǁdownload_parallel__mutmut_3,
        "xǁToolDownloaderǁdownload_parallel__mutmut_4": xǁToolDownloaderǁdownload_parallel__mutmut_4,
        "xǁToolDownloaderǁdownload_parallel__mutmut_5": xǁToolDownloaderǁdownload_parallel__mutmut_5,
        "xǁToolDownloaderǁdownload_parallel__mutmut_6": xǁToolDownloaderǁdownload_parallel__mutmut_6,
        "xǁToolDownloaderǁdownload_parallel__mutmut_7": xǁToolDownloaderǁdownload_parallel__mutmut_7,
        "xǁToolDownloaderǁdownload_parallel__mutmut_8": xǁToolDownloaderǁdownload_parallel__mutmut_8,
        "xǁToolDownloaderǁdownload_parallel__mutmut_9": xǁToolDownloaderǁdownload_parallel__mutmut_9,
        "xǁToolDownloaderǁdownload_parallel__mutmut_10": xǁToolDownloaderǁdownload_parallel__mutmut_10,
        "xǁToolDownloaderǁdownload_parallel__mutmut_11": xǁToolDownloaderǁdownload_parallel__mutmut_11,
        "xǁToolDownloaderǁdownload_parallel__mutmut_12": xǁToolDownloaderǁdownload_parallel__mutmut_12,
        "xǁToolDownloaderǁdownload_parallel__mutmut_13": xǁToolDownloaderǁdownload_parallel__mutmut_13,
        "xǁToolDownloaderǁdownload_parallel__mutmut_14": xǁToolDownloaderǁdownload_parallel__mutmut_14,
        "xǁToolDownloaderǁdownload_parallel__mutmut_15": xǁToolDownloaderǁdownload_parallel__mutmut_15,
        "xǁToolDownloaderǁdownload_parallel__mutmut_16": xǁToolDownloaderǁdownload_parallel__mutmut_16,
        "xǁToolDownloaderǁdownload_parallel__mutmut_17": xǁToolDownloaderǁdownload_parallel__mutmut_17,
        "xǁToolDownloaderǁdownload_parallel__mutmut_18": xǁToolDownloaderǁdownload_parallel__mutmut_18,
    }

    def download_parallel(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolDownloaderǁdownload_parallel__mutmut_orig"),
            object.__getattribute__(self, "xǁToolDownloaderǁdownload_parallel__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    download_parallel.__signature__ = _mutmut_signature(xǁToolDownloaderǁdownload_parallel__mutmut_orig)
    xǁToolDownloaderǁdownload_parallel__mutmut_orig.__name__ = "xǁToolDownloaderǁdownload_parallel"

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_orig(
        self, mirrors: list[str], dest: Path
    ) -> Path:
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

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_1(self, mirrors: list[str], dest: Path) -> Path:
        """Try multiple mirrors until one succeeds using fallback pattern.

        Args:
            mirrors: List of mirror URLs to try.
            dest: Destination file path.

        Returns:
            Path to downloaded file.

        Raises:
            DownloadError: If all mirrors fail.

        """
        if mirrors:
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

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_2(self, mirrors: list[str], dest: Path) -> Path:
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
            raise DownloadError(None)

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

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_3(self, mirrors: list[str], dest: Path) -> Path:
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
            raise DownloadError("XXNo mirrors providedXX")

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

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_4(self, mirrors: list[str], dest: Path) -> Path:
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
            raise DownloadError("no mirrors provided")

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

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_5(self, mirrors: list[str], dest: Path) -> Path:
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
            raise DownloadError("NO MIRRORS PROVIDED")

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

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_6(self, mirrors: list[str], dest: Path) -> Path:
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

        last_error = ""

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

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_7(self, mirrors: list[str], dest: Path) -> Path:
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
                log.debug(None)
                return await self.download_with_progress(mirror_url, dest)
            except Exception as e:
                last_error = e
                log.warning(f"Mirror {mirror_url} failed: {e}")
                # Clean up any partial download
                if dest.exists():
                    dest.unlink()

        # All mirrors failed
        raise DownloadError(f"All mirrors failed: {last_error}") from last_error

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_8(self, mirrors: list[str], dest: Path) -> Path:
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
                return await self.download_with_progress(None, dest)
            except Exception as e:
                last_error = e
                log.warning(f"Mirror {mirror_url} failed: {e}")
                # Clean up any partial download
                if dest.exists():
                    dest.unlink()

        # All mirrors failed
        raise DownloadError(f"All mirrors failed: {last_error}") from last_error

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_9(self, mirrors: list[str], dest: Path) -> Path:
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
                return await self.download_with_progress(mirror_url, None)
            except Exception as e:
                last_error = e
                log.warning(f"Mirror {mirror_url} failed: {e}")
                # Clean up any partial download
                if dest.exists():
                    dest.unlink()

        # All mirrors failed
        raise DownloadError(f"All mirrors failed: {last_error}") from last_error

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_10(self, mirrors: list[str], dest: Path) -> Path:
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
                return await self.download_with_progress(dest)
            except Exception as e:
                last_error = e
                log.warning(f"Mirror {mirror_url} failed: {e}")
                # Clean up any partial download
                if dest.exists():
                    dest.unlink()

        # All mirrors failed
        raise DownloadError(f"All mirrors failed: {last_error}") from last_error

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_11(self, mirrors: list[str], dest: Path) -> Path:
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
                return await self.download_with_progress(
                    mirror_url,
                )
            except Exception as e:
                last_error = e
                log.warning(f"Mirror {mirror_url} failed: {e}")
                # Clean up any partial download
                if dest.exists():
                    dest.unlink()

        # All mirrors failed
        raise DownloadError(f"All mirrors failed: {last_error}") from last_error

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_12(self, mirrors: list[str], dest: Path) -> Path:
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
                last_error = None
                log.warning(f"Mirror {mirror_url} failed: {e}")
                # Clean up any partial download
                if dest.exists():
                    dest.unlink()

        # All mirrors failed
        raise DownloadError(f"All mirrors failed: {last_error}") from last_error

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_13(self, mirrors: list[str], dest: Path) -> Path:
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
                log.warning(None)
                # Clean up any partial download
                if dest.exists():
                    dest.unlink()

        # All mirrors failed
        raise DownloadError(f"All mirrors failed: {last_error}") from last_error

    async def xǁToolDownloaderǁdownload_with_mirrors__mutmut_14(self, mirrors: list[str], dest: Path) -> Path:
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
        raise DownloadError(None) from last_error

    xǁToolDownloaderǁdownload_with_mirrors__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_1": xǁToolDownloaderǁdownload_with_mirrors__mutmut_1,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_2": xǁToolDownloaderǁdownload_with_mirrors__mutmut_2,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_3": xǁToolDownloaderǁdownload_with_mirrors__mutmut_3,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_4": xǁToolDownloaderǁdownload_with_mirrors__mutmut_4,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_5": xǁToolDownloaderǁdownload_with_mirrors__mutmut_5,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_6": xǁToolDownloaderǁdownload_with_mirrors__mutmut_6,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_7": xǁToolDownloaderǁdownload_with_mirrors__mutmut_7,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_8": xǁToolDownloaderǁdownload_with_mirrors__mutmut_8,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_9": xǁToolDownloaderǁdownload_with_mirrors__mutmut_9,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_10": xǁToolDownloaderǁdownload_with_mirrors__mutmut_10,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_11": xǁToolDownloaderǁdownload_with_mirrors__mutmut_11,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_12": xǁToolDownloaderǁdownload_with_mirrors__mutmut_12,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_13": xǁToolDownloaderǁdownload_with_mirrors__mutmut_13,
        "xǁToolDownloaderǁdownload_with_mirrors__mutmut_14": xǁToolDownloaderǁdownload_with_mirrors__mutmut_14,
    }

    def download_with_mirrors(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolDownloaderǁdownload_with_mirrors__mutmut_orig"),
            object.__getattribute__(self, "xǁToolDownloaderǁdownload_with_mirrors__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    download_with_mirrors.__signature__ = _mutmut_signature(
        xǁToolDownloaderǁdownload_with_mirrors__mutmut_orig
    )
    xǁToolDownloaderǁdownload_with_mirrors__mutmut_orig.__name__ = "xǁToolDownloaderǁdownload_with_mirrors"


# <3 🧱🤝🔧🪄
