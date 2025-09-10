"""
Tool download orchestration with progress reporting.

Provides capabilities for downloading tools with progress tracking,
parallel downloads, and mirror support.
"""

import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger
from provide.foundation.resilience import retry, fallback
from provide.foundation.transport import UniversalClient

log = get_logger(__name__)


class DownloadError(FoundationError):
    """Raised when download fails."""
    
    pass


class ToolDownloader:
    """
    Advanced download capabilities for tools.
    
    Features:
    - Progress reporting with callbacks
    - Parallel downloads for multiple files
    - Mirror fallback support
    - Checksum verification
    
    Attributes:
        client: Transport client for HTTP requests.
        progress_callbacks: List of progress callback functions.
    """
    
    def __init__(self, client: UniversalClient):
        """
        Initialize the downloader.
        
        Args:
            client: Universal client for making HTTP requests.
        """
        self.client = client
        self.progress_callbacks: list[Callable[[int, int], None]] = []
    
    def add_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """
        Add a progress callback.
        
        Args:
            callback: Function that receives (downloaded_bytes, total_bytes).
        """
        self.progress_callbacks.append(callback)
    
    def _report_progress(self, downloaded: int, total: int) -> None:
        """
        Report progress to all callbacks.
        
        Args:
            downloaded: Bytes downloaded so far.
            total: Total bytes to download (0 if unknown).
        """
        for callback in self.progress_callbacks:
            try:
                callback(downloaded, total)
            except Exception as e:
                log.warning(f"Progress callback failed: {e}")
    
    @retry(max_attempts=3, base_delay=1.0)
    def download_with_progress(
        self,
        url: str,
        dest: Path,
        checksum: str | None = None
    ) -> Path:
        """
        Download a file with progress reporting.
        
        Args:
            url: URL to download from.
            dest: Destination file path.
            checksum: Optional checksum for verification.
            
        Returns:
            Path to the downloaded file.
            
        Raises:
            DownloadError: If download or verification fails.
        """
        log.debug(f"Downloading {url} to {dest}")
        
        # Ensure parent directory exists
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Stream download with progress
        with self.client.stream("GET", url) as response:
            # Get total size if available
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            
            # Write to file and report progress
            with dest.open("wb") as f:
                for chunk in response.iter_bytes(8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    self._report_progress(downloaded, total_size)
        
        # Verify checksum if provided
        if checksum:
            if not self.verify_checksum(dest, checksum):
                dest.unlink()
                raise DownloadError(f"Checksum mismatch for {url}")
        
        log.info(f"Downloaded {url} successfully")
        return dest
    
    def verify_checksum(self, file_path: Path, expected: str) -> bool:
        """
        Verify file checksum.
        
        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).
            
        Returns:
            True if checksum matches, False otherwise.
        """
        # Default to SHA256
        hasher = hashlib.sha256()
        
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        
        actual = hasher.hexdigest()
        return actual == expected
    
    def download_parallel(
        self,
        urls: list[tuple[str, Path]]
    ) -> list[Path]:
        """
        Download multiple files in parallel.
        
        Args:
            urls: List of (url, destination) tuples.
            
        Returns:
            List of downloaded file paths in the same order as input.
            
        Raises:
            DownloadError: If any download fails.
        """
        errors = []
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all downloads, maintaining order with index
            futures = [
                executor.submit(self.download_with_progress, url, dest)
                for url, dest in urls
            ]
            
            # Collect results in order
            results = []
            for i, future in enumerate(futures):
                url, dest = urls[i]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    errors.append((url, e))
                    log.error(f"Failed to download {url}: {e}")
        
        if errors:
            raise DownloadError(f"Some downloads failed: {errors}")
        
        return results
    
    def download_with_mirrors(
        self,
        mirrors: list[str],
        dest: Path
    ) -> Path:
        """
        Try multiple mirrors until one succeeds using fallback pattern.
        
        Args:
            mirrors: List of mirror URLs to try.
            dest: Destination file path.
            
        Returns:
            Path to downloaded file.
            
        Raises:
            DownloadError: If all mirrors fail.
        """
        from provide.foundation.resilience.fallback import FallbackChain
        
        if not mirrors:
            raise DownloadError("No mirrors provided")
        
        # Create fallback functions for each mirror
        fallback_funcs = []
        for mirror_url in mirrors:
            def create_mirror_func(url):
                def mirror_download():
                    log.debug(f"Trying mirror: {url}")
                    return self.download_with_progress(url, dest)
                return mirror_download
            fallback_funcs.append(create_mirror_func(mirror_url))
        
        # Use FallbackChain to try mirrors in order
        chain = FallbackChain(fallbacks=fallback_funcs[1:])  # All but first are fallbacks
        
        try:
            return chain.execute(fallback_funcs[0])  # First is primary
        except Exception as e:
            raise DownloadError(f"All mirrors failed: {e}")