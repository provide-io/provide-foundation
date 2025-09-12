"""
Subprocess-specific test fixtures for process testing.

Provides fixtures for mocking and testing subprocess operations,
stream handling, and process communication.
"""

from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture
def mock_async_process() -> AsyncMock:
    """
    Mock async subprocess for testing.

    Returns:
        AsyncMock configured as a subprocess with common attributes.
    """
    mock_process = AsyncMock()
    mock_process.communicate = AsyncMock(return_value=(b"output", b""))
    mock_process.returncode = 0
    mock_process.pid = 12345
    mock_process.stdin = AsyncMock()
    mock_process.stdout = AsyncMock()
    mock_process.stderr = AsyncMock()
    mock_process.wait = AsyncMock(return_value=0)
    mock_process.kill = Mock()
    mock_process.terminate = Mock()

    return mock_process


@pytest.fixture
async def async_stream_reader() -> AsyncMock:
    """
    Mock async stream reader for subprocess stdout/stderr.

    Returns:
        AsyncMock configured as a stream reader.
    """
    reader = AsyncMock()

    # Simulate reading lines
    async def readline_side_effect():
        for line in [b"line1\n", b"line2\n", b""]:
            yield line

    reader.readline = AsyncMock(side_effect=readline_side_effect().__anext__)
    reader.read = AsyncMock(return_value=b"full content")
    reader.at_eof = Mock(side_effect=[False, False, True])

    return reader


@pytest.fixture
def async_subprocess():
    """
    Create mock async subprocess for testing.

    Returns:
        Function that creates mock subprocess with configurable behavior.
    """

    def _create_subprocess(
        returncode: int = 0, stdout: bytes = b"", stderr: bytes = b"", pid: int = 12345
    ) -> AsyncMock:
        """
        Create a mock async subprocess.

        Args:
            returncode: Process return code
            stdout: Process stdout output
            stderr: Process stderr output
            pid: Process ID

        Returns:
            AsyncMock configured as subprocess
        """
        process = AsyncMock()
        process.returncode = returncode
        process.pid = pid
        process.communicate = AsyncMock(return_value=(stdout, stderr))
        process.wait = AsyncMock(return_value=returncode)
        process.kill = Mock()
        process.terminate = Mock()
        process.send_signal = Mock()

        # Add stdout/stderr as async stream readers
        process.stdout = AsyncMock()
        process.stdout.read = AsyncMock(return_value=stdout)
        process.stdout.readline = AsyncMock(side_effect=[stdout, b""])
        process.stdout.at_eof = Mock(side_effect=[False, True])

        process.stderr = AsyncMock()
        process.stderr.read = AsyncMock(return_value=stderr)
        process.stderr.readline = AsyncMock(side_effect=[stderr, b""])
        process.stderr.at_eof = Mock(side_effect=[False, True])

        process.stdin = AsyncMock()
        process.stdin.write = AsyncMock()
        process.stdin.drain = AsyncMock()
        process.stdin.close = Mock()

        return process

    return _create_subprocess


@pytest.fixture
def async_mock_server():
    """
    Create a mock async server for testing.

    Returns:
        Mock server with async methods.
    """

    class AsyncMockServer:
        def __init__(self):
            self.started = False
            self.connections = []
            self.requests = []

        async def start(self, host: str = "localhost", port: int = 8080):
            """Start the mock server."""
            self.started = True
            self.host = host
            self.port = port

        async def stop(self):
            """Stop the mock server."""
            self.started = False
            for conn in self.connections:
                await conn.close()

        async def handle_connection(self, reader, writer):
            """Mock connection handler."""
            conn = {"reader": reader, "writer": writer}
            self.connections.append(conn)

            # Mock reading request
            data = await reader.read(1024)
            self.requests.append(data)

            # Mock sending response
            writer.write(b"HTTP/1.1 200 OK\r\n\r\nOK")
            await writer.drain()

            writer.close()
            await writer.wait_closed()

        def get_url(self) -> str:
            """Get server URL."""
            return f"http://{self.host}:{self.port}"

    return AsyncMockServer()


@pytest.fixture
def async_test_client():
    """
    Create an async HTTP test client.

    Returns:
        Mock async HTTP client for testing.
    """

    class AsyncTestClient:
        def __init__(self):
            self.responses = {}
            self.requests = []

        def set_response(self, url: str, response: dict):
            """Set a mock response for a URL."""
            self.responses[url] = response

        async def get(self, url: str, **kwargs) -> dict:
            """Mock GET request."""
            self.requests.append({"method": "GET", "url": url, "kwargs": kwargs})
            return self.responses.get(url, {"status": 404, "body": "Not Found"})

        async def post(self, url: str, data=None, **kwargs) -> dict:
            """Mock POST request."""
            self.requests.append({"method": "POST", "url": url, "data": data, "kwargs": kwargs})
            return self.responses.get(url, {"status": 200, "body": "OK"})

        async def close(self):
            """Close the client."""
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            await self.close()

    return AsyncTestClient()


__all__ = [
    "async_mock_server",
    "async_stream_reader",
    "async_subprocess",
    "async_test_client",
    "mock_async_process",
]
