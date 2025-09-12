"""
Transport and Network Testing Fixtures.

Fixtures and helpers for testing network operations, including
mock servers, free port allocation, and HTTP client mocking.
"""

from collections.abc import Generator
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import threading
from typing import Any

import pytest


@pytest.fixture
def free_port() -> int:
    """
    Get a free port for testing.

    Returns:
        An available port number on localhost.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


@pytest.fixture
def mock_server(free_port) -> Generator[dict[str, Any], None, None]:
    """
    Create a simple mock HTTP server for testing.

    Args:
        free_port: Free port number from fixture.

    Yields:
        Dict with server info including url, port, and server instance.
    """
    responses = {}
    requests_received = []

    class MockHandler(BaseHTTPRequestHandler):
        """Handler for mock HTTP server."""

        def do_GET(self):
            """Handle GET requests."""
            requests_received.append({"method": "GET", "path": self.path, "headers": dict(self.headers)})

            response = responses.get(self.path, {"status": 404, "body": b"Not Found"})
            self.send_response(response["status"])
            for header, value in response.get("headers", {}).items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response["body"])

        def do_POST(self):
            """Handle POST requests."""
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length else b""

            requests_received.append(
                {
                    "method": "POST",
                    "path": self.path,
                    "headers": dict(self.headers),
                    "body": body,
                }
            )

            response = responses.get(self.path, {"status": 200, "body": b"OK"})
            self.send_response(response["status"])
            for header, value in response.get("headers", {}).items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response["body"])

        def log_message(self, format, *args):
            """Suppress log messages."""
            pass

    server = HTTPServer(("localhost", free_port), MockHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    yield {
        "url": f"http://localhost:{free_port}",
        "port": free_port,
        "server": server,
        "responses": responses,
        "requests": requests_received,
    }

    server.shutdown()
    server.server_close()


@pytest.fixture
def httpx_mock_responses():
    """
    Pre-configured responses for HTTPX mocking.

    Returns:
        Dict of common mock responses.
    """
    return {
        "success": {
            "status_code": 200,
            "json": {"status": "ok", "data": {}},
        },
        "created": {
            "status_code": 201,
            "json": {"id": "123", "created": True},
        },
        "not_found": {
            "status_code": 404,
            "json": {"error": "Not found"},
        },
        "server_error": {
            "status_code": 500,
            "json": {"error": "Internal server error"},
        },
        "unauthorized": {
            "status_code": 401,
            "json": {"error": "Unauthorized"},
        },
        "rate_limited": {
            "status_code": 429,
            "headers": {"Retry-After": "60"},
            "json": {"error": "Rate limit exceeded"},
        },
    }


@pytest.fixture
def mock_websocket():
    """
    Mock WebSocket connection for testing.

    Returns:
        Mock WebSocket with send, receive, close methods.
    """
    from unittest.mock import AsyncMock, Mock

    ws = Mock()
    ws.send = AsyncMock()
    ws.receive = AsyncMock(return_value={"type": "text", "data": "message"})
    ws.close = AsyncMock()
    ws.accept = AsyncMock()
    ws.ping = AsyncMock()
    ws.pong = AsyncMock()

    # State properties
    ws.closed = False
    ws.url = "ws://localhost:8000/ws"

    return ws


@pytest.fixture
def mock_dns_resolver():
    """
    Mock DNS resolver for testing.

    Returns:
        Mock resolver with resolve method.
    """
    from unittest.mock import Mock

    resolver = Mock()
    resolver.resolve = Mock(return_value=["127.0.0.1", "::1"])
    resolver.reverse = Mock(return_value="localhost")
    resolver.clear_cache = Mock()

    return resolver


@pytest.fixture
def tcp_client_server(free_port) -> Generator[dict[str, Any], None, None]:
    """
    Create a TCP client-server pair for testing.

    Yields:
        Dict with client socket, server socket, and port info.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", free_port))
    server_socket.listen(1)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Run server accept in thread
    connection = None

    def accept_connection():
        nonlocal connection
        connection, _ = server_socket.accept()

    accept_thread = threading.Thread(target=accept_connection)
    accept_thread.daemon = True
    accept_thread.start()

    # Connect client
    client_socket.connect(("localhost", free_port))
    accept_thread.join(timeout=1)

    yield {
        "client": client_socket,
        "server": connection,
        "server_socket": server_socket,
        "port": free_port,
    }

    # Cleanup
    client_socket.close()
    if connection:
        connection.close()
    server_socket.close()


@pytest.fixture
def mock_ssl_context():
    """
    Mock SSL context for testing secure connections.

    Returns:
        Mock SSL context with common methods.
    """
    from unittest.mock import Mock

    context = Mock()
    context.load_cert_chain = Mock()
    context.load_verify_locations = Mock()
    context.set_ciphers = Mock()
    context.wrap_socket = Mock()
    context.check_hostname = True
    context.verify_mode = 2  # ssl.CERT_REQUIRED

    return context


@pytest.fixture
def network_timeout():
    """
    Provide network timeout configuration for tests.

    Returns:
        Dict with timeout values for different operations.
    """
    return {
        "connect": 5.0,
        "read": 10.0,
        "write": 10.0,
        "total": 30.0,
    }


@pytest.fixture
def mock_http_headers():
    """
    Common HTTP headers for testing.

    Returns:
        Dict of typical HTTP headers.
    """
    return {
        "User-Agent": "TestClient/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer test_token",
        "X-Request-ID": "test-request-123",
        "X-Correlation-ID": "test-correlation-456",
    }
