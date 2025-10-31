#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Example: Transport Client Usage with Foundation Mocking

Demonstrates using the Foundation transport system for HTTP requests with:
- Basic HTTP methods (GET, POST, PUT, DELETE)
- UniversalClient for session management
- Middleware pipeline configuration
- Error handling
- Response processing
- Foundation's mocking for self-contained examples

This example showcases the full transport API using Foundation's testing utilities
for realistic but controlled scenarios."""

import asyncio
from pathlib import Path
import sys

# Add project root to path for imports
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))


from provide.testkit import AsyncMock, Mock, patch

from provide.foundation import get_hub, logger
from provide.foundation.resilience.retry import BackoffStrategy, RetryPolicy
from provide.foundation.transport import (
    UniversalClient,
    get,
    get_default_client,
    post,
)
from provide.foundation.transport.errors import (
    HTTPResponseError,
    TransportConnectionError,
    TransportError,
    TransportTimeoutError,
)
from provide.foundation.transport.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    MiddlewarePipeline,
    RetryMiddleware,
)


async def demonstrate_basic_requests() -> None:
    """Show basic HTTP request methods using Foundation mocking."""
    logger.info("basic_requests_started", demo="transport_client_mocked")

    # Mock httpx responses
    mock_get_httpx_response = Mock()
    mock_get_httpx_response.status_code = 200
    mock_get_httpx_response.headers = {"content-type": "application/json"}
    mock_get_httpx_response.content = (
        b'{"args": {"demo": "foundation", "example": "transport"}, "url": "https://api.example.com/get"}'
    )
    mock_get_httpx_response.elapsed = Mock()
    mock_get_httpx_response.elapsed.total_seconds.return_value = 0.1425

    mock_post_httpx_response = Mock()
    mock_post_httpx_response.status_code = 201
    mock_post_httpx_response.headers = {"content-type": "application/json"}
    mock_post_httpx_response.content = (
        b'{"json": {"name": "Foundation Demo", "version": "1.0.0"}, "url": "https://api.example.com/post"}'
    )
    mock_post_httpx_response.elapsed = Mock()
    mock_post_httpx_response.elapsed.total_seconds.return_value = 0.245

    # Mock httpx.AsyncClient.request method
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:
        # Configure mock to return appropriate responses based on method
        def mock_request_side_effect(method, **kwargs):
            if method == "GET":
                return mock_get_httpx_response
            if method == "POST":
                return mock_post_httpx_response
            raise ValueError(f"Unexpected method: {method}")

        mock_httpx_request.side_effect = mock_request_side_effect

        logger.info("making_mocked_get_request", url="https://api.example.com/get")
        response = await get(
            "https://api.example.com/get",
            params={"demo": "foundation", "example": "transport"},
        )

        if response.is_success():
            data = response.json()
            logger.info("get_request_success", status=response.status, args=data.get("args", {}), mocked=True)

        logger.info("making_mocked_post_request", url="https://api.example.com/post")
        response = await post(
            "https://api.example.com/post",
            body={
                "name": "Foundation Demo",
                "version": "1.0.0",
                "features": ["transport", "middleware", "telemetry"],
            },
            headers={"Content-Type": "application/json"},
        )

        if response.is_success():
            data = response.json()
            logger.info(
                "post_request_success", status=response.status, json_echo=data.get("json", {}), mocked=True
            )

    logger.info("basic_requests_completed")


async def demonstrate_client_session() -> None:
    """Show UniversalClient for session management with mocked responses."""
    logger.info("client_session_started", demo="transport_client_mocked")

    # Create client with custom configuration
    client = UniversalClient(
        hub=get_hub(),
        default_headers={
            "User-Agent": "Foundation-Demo/1.0",
            "Accept": "application/json",
        },
        default_timeout=30.0,
    )

    # Mock httpx responses for different endpoints
    mock_users_response = Mock()
    mock_users_response.status_code = 200
    mock_users_response.headers = {"content-type": "application/json"}
    mock_users_response.content = b'{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}'
    mock_users_response.elapsed = Mock()
    mock_users_response.elapsed.total_seconds.return_value = 0.1567

    mock_create_response = Mock()
    mock_create_response.status_code = 201
    mock_create_response.headers = {"content-type": "application/json"}
    mock_create_response.content = (
        b'{"id": 3, "name": "New User", "email": "user@example.com", "created": true}'
    )
    mock_create_response.elapsed = Mock()
    mock_create_response.elapsed.total_seconds.return_value = 0.2341

    mock_update_response = Mock()
    mock_update_response.status_code = 200
    mock_update_response.headers = {"content-type": "application/json"}
    mock_update_response.content = b'{"id": 3, "name": "Updated User", "status": "active", "updated": true}'
    mock_update_response.elapsed = Mock()
    mock_update_response.elapsed.total_seconds.return_value = 0.1893

    async with client:
        logger.info("making_multiple_mocked_requests", count=3)

        # Mock httpx.AsyncClient.request for all client operations
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:

            def mock_request_side_effect(method, url, **kwargs):
                if "users" in url and method == "GET":
                    return mock_users_response
                if "users" in url and method == "POST":
                    return mock_create_response
                if "users/3" in url and method == "PUT":
                    return mock_update_response
                raise ValueError(f"Unexpected request: {method} {url}")

            mock_httpx_request.side_effect = mock_request_side_effect

            users_response = await client.get(
                "https://api.example.com/users",
                params={"endpoint": "users", "page": 1},
            )

            if users_response.is_success():
                logger.info(
                    "users_request_success",
                    status=users_response.status,
                    duration_ms=users_response.elapsed_ms,
                    mocked=True,
                )

            create_response = await client.post(
                "https://api.example.com/users",
                body={"name": "New User", "email": "user@example.com"},
            )

            if create_response.is_success():
                logger.info(
                    "create_request_success",
                    status=create_response.status,
                    duration_ms=create_response.elapsed_ms,
                    mocked=True,
                )

            update_response = await client.put(
                "https://api.example.com/users/3",
                body={"name": "Updated User", "status": "active"},
            )

            if update_response.is_success():
                logger.info(
                    "update_request_success",
                    status=update_response.status,
                    duration_ms=update_response.elapsed_ms,
                    mocked=True,
                )

    logger.info("client_session_completed")


async def demonstrate_middleware() -> None:
    """Show middleware configuration and usage with mocked responses."""
    logger.info("middleware_demo_started", demo="transport_client_mocked")

    # Create custom middleware pipeline
    retry_policy = RetryPolicy(
        max_attempts=3,
        backoff=BackoffStrategy.EXPONENTIAL,
        base_delay=1.0,
        max_delay=10.0,
        jitter=True,
    )

    pipeline = MiddlewarePipeline(
        [
            LoggingMiddleware(log_requests=True, log_responses=True),
            MetricsMiddleware(),
            RetryMiddleware(policy=retry_policy),
        ]
    )

    client = UniversalClient(hub=get_hub(), middleware=pipeline)

    # Mock successful httpx response
    mock_success_httpx_response = Mock()
    mock_success_httpx_response.status_code = 200
    mock_success_httpx_response.headers = {"content-type": "application/json"}
    mock_success_httpx_response.content = b'{"status": "success", "middleware": "processed"}'
    mock_success_httpx_response.elapsed = Mock()
    mock_success_httpx_response.elapsed.total_seconds.return_value = 0.0984

    async with client:
        logger.info("middleware_configured", middlewares=["logging", "metrics", "retry"])

        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:
            mock_httpx_request.return_value = mock_success_httpx_response

            # Request will be processed through middleware
            response = await client.get(
                "https://api.example.com/status",
                timeout=5.0,
            )

            logger.info(
                "middleware_request_completed", status=response.status, middlewares_applied=True, mocked=True
            )

    logger.info("middleware_demo_completed")


async def demonstrate_error_handling() -> None:
    """Show comprehensive error handling with mocked error scenarios."""
    logger.info("error_handling_demo_started", demo="transport_client_mocked")

    # Define mock error scenarios with httpx responses
    mock_not_found_response = Mock()
    mock_not_found_response.status_code = 404
    mock_not_found_response.headers = {}
    mock_not_found_response.content = b'{"error": "Not Found"}'
    mock_not_found_response.elapsed = Mock()
    mock_not_found_response.elapsed.total_seconds.return_value = 0.0452

    mock_server_error_response = Mock()
    mock_server_error_response.status_code = 500
    mock_server_error_response.headers = {}
    mock_server_error_response.content = b'{"error": "Internal Server Error"}'
    mock_server_error_response.elapsed = Mock()
    mock_server_error_response.elapsed.total_seconds.return_value = 0.1238

    error_scenarios = [
        ("timeout", TransportTimeoutError("Request timed out", request=None)),
        ("not_found", mock_not_found_response),
        ("server_error", mock_server_error_response),
        ("connection_failed", TransportConnectionError("Connection failed", request=None)),
    ]

    for scenario_name, error_or_response in error_scenarios:
        try:
            logger.info("testing_mocked_error_scenario", scenario=scenario_name)

            if isinstance(error_or_response, Exception):
                # Mock an exception at httpx level
                with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:
                    mock_httpx_request.side_effect = error_or_response
                    response = await get("https://api.example.com/test", timeout=2.0)
            else:
                # Mock an error response at httpx level
                with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:
                    mock_httpx_request.return_value = error_or_response
                    response = await get("https://api.example.com/test", timeout=2.0)

                if not response.is_success():
                    logger.warning(
                        "http_error_response", scenario=scenario_name, status=response.status, mocked=True
                    )
                else:
                    logger.info(
                        "unexpected_success", scenario=scenario_name, status=response.status, mocked=True
                    )

        except TransportTimeoutError:
            logger.error("timeout_error", scenario=scenario_name, mocked=True)

        except TransportConnectionError as e:
            logger.error("connection_error", scenario=scenario_name, error=str(e), mocked=True)

        except HTTPResponseError as e:
            logger.error("http_response_error", scenario=scenario_name, status=e.status_code, mocked=True)

        except TransportError as e:
            logger.error(
                "transport_error",
                scenario=scenario_name,
                error=str(e),
                error_type=type(e).__name__,
                mocked=True,
            )

    logger.info("error_handling_demo_completed")


async def demonstrate_response_processing() -> None:
    """Show different response processing techniques with mocked data."""
    logger.info("response_processing_started", demo="transport_client_mocked")

    # Mock different httpx response types
    json_httpx_response = Mock()
    json_httpx_response.status_code = 200
    json_httpx_response.headers = {"content-type": "application/json"}
    json_httpx_response.content = b'{"slideshow": {"author": "Foundation", "title": "Transport Demo"}}'
    json_httpx_response.elapsed = Mock()
    json_httpx_response.elapsed.total_seconds.return_value = 0.0673

    text_httpx_response = Mock()
    text_httpx_response.status_code = 200
    text_httpx_response.headers = {"content-type": "text/plain"}
    text_httpx_response.content = b"User-agent: *\nDisallow: /private\nAllow: /public"
    text_httpx_response.elapsed = Mock()
    text_httpx_response.elapsed.total_seconds.return_value = 0.0341

    headers_httpx_response = Mock()
    headers_httpx_response.status_code = 200
    headers_httpx_response.headers = {
        "content-type": "application/json",
        "x-custom-header": "demo-value",
        "x-server": "foundation-transport",
    }
    headers_httpx_response.content = b'{"custom_header": "demo-value", "server": "foundation-transport"}'
    headers_httpx_response.elapsed = Mock()
    headers_httpx_response.elapsed.total_seconds.return_value = 0.0897

    # Test JSON response processing
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:
        mock_httpx_request.return_value = json_httpx_response
        json_response = await get("https://api.example.com/json")

        if json_response.is_success():
            data = json_response.json()
            logger.info(
                "json_response_processed",
                type="json",
                keys=list(data.keys()) if isinstance(data, dict) else None,
                mocked=True,
            )

    # Test text response processing
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:
        mock_httpx_request.return_value = text_httpx_response
        text_response = await get("https://api.example.com/robots.txt")

        if text_response.is_success():
            text_content = text_response.text
            logger.info(
                "text_response_processed",
                type="text",
                length=len(text_content),
                preview=text_content[:50] + "..." if len(text_content) > 50 else text_content,
                mocked=True,
            )

    # Test headers inspection
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:
        mock_httpx_request.return_value = headers_httpx_response
        headers_response = await get("https://api.example.com/headers")

        if headers_response.is_success():
            logger.info(
                "headers_response_processed",
                type="headers",
                response_headers=dict(headers_response.headers),
                content_type=headers_response.headers.get("content-type"),
                mocked=True,
            )

    logger.info("response_processing_completed")


async def demonstrate_default_client() -> None:
    """Show usage of the global default client with mocked responses."""
    logger.info("default_client_demo_started", demo="transport_client_mocked")

    # The global functions use a default client instance
    client = get_default_client()
    logger.info("default_client_retrieved", client_id=id(client), mocked=True)

    # Mock httpx responses for default client usage
    uuid_httpx_response = Mock()
    uuid_httpx_response.status_code = 200
    uuid_httpx_response.headers = {"content-type": "application/json"}
    uuid_httpx_response.content = b'{"uuid": "550e8400-e29b-41d4-a716-446655440000"}'
    uuid_httpx_response.elapsed = Mock()
    uuid_httpx_response.elapsed.total_seconds.return_value = 0.0782

    post_httpx_response = Mock()
    post_httpx_response.status_code = 201
    post_httpx_response.headers = {"content-type": "application/json"}
    post_httpx_response.content = b'{"data": {"test": "data"}, "created": true}'
    post_httpx_response.elapsed = Mock()
    post_httpx_response.elapsed.total_seconds.return_value = 0.1564

    get_httpx_response = Mock()
    get_httpx_response.status_code = 200
    get_httpx_response.headers = {"content-type": "application/json"}
    get_httpx_response.content = b'{"method": "GET", "client": "default"}'
    get_httpx_response.elapsed = Mock()
    get_httpx_response.elapsed.total_seconds.return_value = 0.0927

    # Test direct function calls (which use the default client)
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_httpx_request:

        def mock_request_side_effect(method, url, **kwargs):
            if "uuid" in url:
                return uuid_httpx_response
            if method == "POST":
                return post_httpx_response
            if "get" in url:
                return get_httpx_response
            raise ValueError(f"Unexpected request: {method} {url}")

        mock_httpx_request.side_effect = mock_request_side_effect

        response1 = await get("https://api.example.com/uuid")
        response2 = await post("https://api.example.com/post", body={"test": "data"})

        if response1.is_success() and response2.is_success():
            logger.info(
                "default_client_requests_success",
                get_status=response1.status,
                post_status=response2.status,
                mocked=True,
            )

        # Test manual client usage (same instance)
        response3 = await client.get("https://api.example.com/get")

        if response3.is_success():
            logger.info("manual_default_client_success", status=response3.status, mocked=True)

    logger.info("default_client_demo_completed")


async def main() -> None:
    """Run all transport client demonstrations using Foundation mocking."""
    logger.info(
        "transport_client_example_started",
        version="1.0.0",
        examples=["basic", "session", "middleware", "errors", "processing", "default_client"],
        mocking="foundation_testing_utilities",
    )

    # Run each demonstration
    await demonstrate_basic_requests()
    await demonstrate_client_session()
    await demonstrate_middleware()
    await demonstrate_error_handling()
    await demonstrate_response_processing()
    await demonstrate_default_client()

    logger.info(
        "transport_client_example_completed",
        demos_completed=6,
        status="success",
        dogfooding="100_percent_foundation",
    )


if __name__ == "__main__":
    # Initialize Foundation telemetry
    get_hub().initialize_foundation()

    # Run the async example
    asyncio.run(main())

# 🧱🏗️🔚
