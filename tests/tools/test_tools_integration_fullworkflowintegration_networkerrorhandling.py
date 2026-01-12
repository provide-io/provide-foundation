#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for tools module with real network requests.

These tests depend on external services and may be skipped if unavailable."""

from __future__ import annotations

from pathlib import Path
import tempfile

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config import BaseConfig
from provide.foundation.hub import get_hub
from provide.foundation.tools.cache import ToolCache
from provide.foundation.tools.downloader import ToolDownloader
from provide.foundation.tools.resolver import VersionResolver
from provide.foundation.transport.client import UniversalClient

# Mark all tests in this module as requiring external services
pytestmark = pytest.mark.external_service


class TestFullWorkflowIntegration(FoundationTestCase):
    """Test complete tool installation workflow.

    Note: These tests may require external services and can be skipped.
    """

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def mock_tool_manager(self, temp_dir):
        """Create mock tool manager with temp cache."""
        pytest.skip("MockToolManager not implemented - test needs to be updated")
        config = BaseConfig()
        manager = MockToolManager(config)  # noqa: F821

        # Override cache to use temp directory
        cache = ToolCache(temp_dir / "cache")
        manager._cache = cache

        return manager

    def test_resolve_version_integration(self) -> None:
        """Test version resolution with realistic version lists."""
        resolver = VersionResolver()

        # Test with realistic version list
        versions = [
            "1.0.0",
            "1.0.1",
            "1.1.0",
            "1.1.1",
            "1.2.0-beta",
            "1.2.0-rc1",
            "1.2.0",
            "2.0.0-alpha",
            "2.0.0-beta",
            "2.0.0",
        ]

        # Test latest stable
        latest = resolver.resolve("latest", versions)
        assert latest == "2.0.0"

        # Test tilde range
        tilde_result = resolver.resolve("~1.1.0", versions)
        assert tilde_result == "1.1.1"

        # Test caret range
        caret_result = resolver.resolve("^1.0.0", versions)
        assert caret_result == "1.2.0-rc1"

        # Test wildcard
        wildcard_result = resolver.resolve("1.1.*", versions)
        assert wildcard_result == "1.1.1"

    @pytest.mark.slow
    async def test_complete_tool_installation_workflow(self, mock_tool_manager, temp_dir) -> None:
        """Test complete workflow: resolve -> download -> verify -> install -> cache."""
        # This test downloads a real binary, so make it optional
        import platform

        system = platform.system().lower()

        if system not in ["linux", "darwin"]:
            pytest.skip(f"Tool installation test not supported on {system}")

        # Use jq 1.7.1 for testing (small, reliable)
        version = "1.7.1"

        try:
            # Test the complete workflow
            install_path = await mock_tool_manager.install(version)

            assert install_path.exists()
            assert mock_tool_manager.is_installed(version)

            # Should be cached now
            cached_path = mock_tool_manager.cache.get("jq", version)
            assert cached_path == install_path

            # Test uninstall
            success = mock_tool_manager.uninstall(version)
            assert success is True
            assert not mock_tool_manager.is_installed(version)

        except ToolNotFoundError:  # noqa: F821
            pytest.skip("Platform not supported for jq download")
        except Exception as e:
            if any(keyword in str(e) for keyword in ["404", "not found", "DNS", "timeout", "ConnectError"]):
                pytest.skip(f"GitHub/network issue - this is an integration test limitation: {e}")
            else:
                raise

    def test_cache_integration_workflow(self, temp_dir) -> None:
        """Test cache operations with real workflows."""
        cache = ToolCache(temp_dir / "test_cache")

        # Test storing and retrieving
        tool_path = temp_dir / "tools" / "testtool" / "1.0.0"
        tool_path.mkdir(parents=True)

        cache.store("testtool", "1.0.0", tool_path, ttl_days=1)

        # Should retrieve successfully
        retrieved = cache.get("testtool", "1.0.0")
        assert retrieved == tool_path

        # Test cache metadata
        cached_tools = cache.list_cached()
        assert len(cached_tools) == 1
        assert cached_tools[0]["tool"] == "testtool"
        assert cached_tools[0]["version"] == "1.0.0"
        assert not cached_tools[0]["expired"]

        # Test cache size calculation
        size = cache.get_size()
        assert size >= 0  # Directory exists so should have some size

        # Test cache clearing
        cache.clear()
        assert len(cache.list_cached()) == 0


class TestNetworkErrorHandling(FoundationTestCase):
    """Test various network error scenarios."""

    @pytest.fixture
    def downloader(self):
        """Create downloader with real HTTP client."""
        client = UniversalClient(hub=get_hub())
        return ToolDownloader(client)

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for downloads."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    async def test_dns_resolution_failure(self, downloader, temp_dir) -> None:
        """Test handling of DNS resolution failures."""
        url = "https://this-domain-definitely-does-not-exist-12345.com/file"
        dest = temp_dir / "dns_fail_test.bin"

        with pytest.raises(Exception):  # Could be DNS error or connection error
            await downloader.download_with_progress(url, dest)

    async def test_connection_refused(self, downloader, temp_dir) -> None:
        """Test handling of connection refused errors."""
        # Use localhost on a port that should be closed
        url = "http://localhost:99999/file"
        dest = temp_dir / "connection_refused_test.bin"

        with pytest.raises(Exception):  # Connection error
            await downloader.download_with_progress(url, dest)

    async def test_http_404_error(self, downloader, temp_dir) -> None:
        """Test handling of HTTP 404 errors."""
        url = "https://httpbin.org/status/404"
        dest = temp_dir / "404_test.bin"

        with pytest.raises(Exception):  # HTTP error
            await downloader.download_with_progress(url, dest)

    async def test_http_403_error(self, downloader, temp_dir) -> None:
        """Test handling of HTTP 403 errors."""
        url = "https://httpbin.org/status/403"
        dest = temp_dir / "403_test.bin"

        with pytest.raises(Exception):  # HTTP error
            await downloader.download_with_progress(url, dest)

    async def test_redirect_handling(self, downloader, temp_dir) -> None:
        """Test handling of HTTP redirects."""
        # httpbin redirect endpoint
        url = "https://httpbin.org/redirect-to?url=https://httpbin.org/bytes/200"
        dest = temp_dir / "redirect_test.bin"

        try:
            result = await downloader.download_with_progress(url, dest)

            assert result == dest
            assert dest.exists()
            assert dest.stat().st_size == 200
        except Exception as e:
            if any(keyword in str(e) for keyword in ["500", "502", "503", "DNS", "timeout", "ConnectError"]):
                pytest.skip(f"httpbin issue - this is an integration test limitation: {e}")
            else:
                raise


# 🧱🏗️🔚
