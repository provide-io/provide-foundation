"""Tests for HTTP transport log sanitization."""

from __future__ import annotations

import io

import pytest
from pytest_httpx import HTTPXMock

from provide.foundation.transport import HTTPTransport, Request
from provide.foundation.transport.config import HTTPConfig


@pytest.fixture
def http_transport() -> HTTPTransport:
    """HTTP transport instance for testing."""
    config = HTTPConfig(timeout=30.0)
    return HTTPTransport(config=config)


@pytest.mark.asyncio
async def test_sensitive_query_params_redacted_in_logs(
    http_transport: HTTPTransport,
    httpx_mock: HTTPXMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that sensitive query parameters are redacted in logs."""
    # Mock response
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/users?api_key=secret123&user_id=456",
        json={"result": "success"},
        status_code=200,
    )

    request = Request(
        uri="https://api.example.com/users?api_key=secret123&user_id=456",
        method="GET",
    )

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200

    # Check logs - api_key should be redacted but user_id should be visible
    log_output = caplog.text
    assert "[REDACTED]" in log_output, "Sensitive param not redacted in logs"
    assert "secret123" not in log_output, "Secret value leaked in logs"
    assert "user_id=456" in log_output, "Safe param not present in logs"


@pytest.mark.asyncio
async def test_multiple_sensitive_params_redacted(
    http_transport: HTTPTransport,
    httpx_mock: HTTPXMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that multiple sensitive query parameters are all redacted."""
    uri = "https://api.example.com/auth?api_key=key123&token=tok456&password=pass789&user=john"

    httpx_mock.add_response(
        method="POST",
        url=uri,
        json={"authenticated": True},
        status_code=200,
    )

    request = Request(uri=uri, method="POST")

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200

    log_output = caplog.text

    # All sensitive values should be redacted
    assert "key123" not in log_output
    assert "tok456" not in log_output
    assert "pass789" not in log_output

    # Safe param should be visible
    assert "user=john" in log_output

    # Should have multiple redactions
    assert log_output.count("[REDACTED]") >= 3


@pytest.mark.asyncio
async def test_uri_without_params_unchanged(
    http_transport: HTTPTransport,
    httpx_mock: HTTPXMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that URIs without query params are logged unchanged."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/users",
        json={"users": []},
        status_code=200,
    )

    request = Request(
        uri="https://api.example.com/users",
        method="GET",
    )

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200

    log_output = caplog.text
    assert "https://api.example.com/users" in log_output
    assert "[REDACTED]" not in log_output


@pytest.mark.asyncio
async def test_streaming_request_sanitizes_uri(
    http_transport: HTTPTransport,
    httpx_mock: HTTPXMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that streaming requests also sanitize URIs in logs."""
    uri = "https://api.example.com/stream?api_key=stream_secret&limit=100"

    httpx_mock.add_response(
        method="GET",
        url=uri,
        content=b"chunk1chunk2chunk3",
        status_code=200,
    )

    request = Request(uri=uri, method="GET")

    chunks = []
    async with http_transport:
        async for chunk in http_transport.stream(request):
            chunks.append(chunk)

    assert b"".join(chunks) == b"chunk1chunk2chunk3"

    log_output = caplog.text

    # Sensitive param should be redacted
    assert "stream_secret" not in log_output
    assert "[REDACTED]" in log_output

    # Safe param should be visible
    assert "limit=100" in log_output

    # Should contain streaming indicator
    assert "Streaming" in log_output or "🌊" in log_output


@pytest.mark.asyncio
async def test_actual_request_sent_with_real_values(
    http_transport: HTTPTransport,
    httpx_mock: HTTPXMock,
) -> None:
    """Test that actual HTTP request contains real values, not redacted."""
    # Mock with callback to inspect request
    requests_received = []

    def callback(request: httpx.Request) -> httpx.Response:
        requests_received.append(request)
        return httpx.Response(200, json={"ok": True})

    httpx_mock.add_callback(callback)

    uri = "https://api.example.com/data?api_key=real_key123&page=1"
    request = Request(uri=uri, method="GET")

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200
    assert len(requests_received) == 1

    # Verify the actual request had the real api_key
    actual_request = requests_received[0]
    assert "api_key=real_key123" in str(actual_request.url)
    assert "page=1" in str(actual_request.url)


@pytest.mark.asyncio
async def test_uri_with_fragment_preserved(
    http_transport: HTTPTransport,
    httpx_mock: HTTPXMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that URI fragments are preserved during sanitization."""
    uri = "https://api.example.com/docs?token=secret#section"

    httpx_mock.add_response(
        method="GET",
        url=uri,
        content=b"documentation",
        status_code=200,
    )

    request = Request(uri=uri, method="GET")

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200

    log_output = caplog.text

    # Token should be redacted
    assert "secret" not in log_output

    # Fragment should be preserved
    assert "#section" in log_output


@pytest.mark.asyncio
async def test_case_insensitive_param_matching(
    http_transport: HTTPTransport,
    httpx_mock: HTTPXMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that sensitive param matching is case-insensitive."""
    # Use different cases for sensitive params
    uri = "https://api.example.com/auth?API_KEY=upper&Token=mixed&password=lower"

    httpx_mock.add_response(
        method="GET",
        url=uri,
        json={"authenticated": True},
        status_code=200,
    )

    request = Request(uri=uri, method="GET")

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200

    log_output = caplog.text

    # All variations should be redacted
    assert "upper" not in log_output
    assert "mixed" not in log_output
    assert "lower" not in log_output
    assert log_output.count("[REDACTED]") >= 3


@pytest.mark.asyncio
async def test_empty_param_values_handled(
    http_transport: HTTPTransport,
    httpx_mock: HTTPXMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that empty parameter values are handled correctly."""
    uri = "https://api.example.com/test?api_key=&normal_param=value"

    httpx_mock.add_response(
        method="GET",
        url=uri,
        json={"result": "ok"},
        status_code=200,
    )

    request = Request(uri=uri, method="GET")

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200

    log_output = caplog.text

    # Empty api_key should still be redacted
    assert "api_key=[REDACTED]" in log_output

    # Normal param should be visible
    assert "normal_param=value" in log_output
