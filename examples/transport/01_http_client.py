#!/usr/bin/env python3
"""
Example: Transport Client Usage with Foundation Mocking

Demonstrates using the Foundation transport system for HTTP requests with:
- Basic HTTP methods (GET, POST, PUT, DELETE)
- UniversalClient for session management
- Middleware pipeline configuration
- Error handling
- Response processing
- Foundation's mocking for self-contained examples

This example showcases the full transport API using Foundation's testing utilities
for realistic but controlled scenarios.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path for imports
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from provide.foundation import setup_telemetry, logger
from provide.foundation.transport import (
    get, post, put, delete,
    UniversalClient,
    get_default_client
)
from provide.foundation.transport.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    RetryMiddleware,
    MiddlewarePipeline,
    create_default_pipeline
)
from provide.foundation.transport.errors import (
    TransportError,
    TransportTimeoutError,
    TransportConnectionError,
    HTTPResponseError
)
from provide.foundation.resilience.retry import RetryPolicy, BackoffStrategy
from provide.foundation.testing.mocking import Mock, AsyncMock, patch
from provide.foundation.transport.base import Response


async def demonstrate_basic_requests():
    """Show basic HTTP request methods using Foundation mocking."""
    logger.info("basic_requests_started", demo="transport_client_mocked")
    
    # Mock GET response
    mock_get_response = Response(
        status=200,
        headers={"content-type": "application/json"},
        body=b'{"args": {"demo": "foundation", "example": "transport"}, "url": "https://api.example.com/get"}',
        elapsed_ms=142.5
    )
    
    # Mock POST response  
    mock_post_response = Response(
        status=201,
        headers={"content-type": "application/json"},
        body=b'{"json": {"name": "Foundation Demo", "version": "1.0.0"}, "url": "https://api.example.com/post"}',
        elapsed_ms=245.0
    )
    
    with patch('provide.foundation.transport.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_get_response
        
        logger.info("making_mocked_get_request", url="https://api.example.com/get")
        response = await get(
            "https://api.example.com/get",
            params={"demo": "foundation", "example": "transport"}
        )
        
        if response.is_success():
            data = response.json()
            logger.info("get_request_success", 
                       status=response.status,
                       args=data.get("args", {}),
                       mocked=True)
    
    with patch('provide.foundation.transport.post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_post_response
        
        logger.info("making_mocked_post_request", url="https://api.example.com/post")
        response = await post(
            "https://api.example.com/post",
            body={
                "name": "Foundation Demo",
                "version": "1.0.0",
                "features": ["transport", "middleware", "telemetry"]
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.is_success():
            data = response.json()
            logger.info("post_request_success",
                       status=response.status,
                       json_echo=data.get("json", {}),
                       mocked=True)
    
    logger.info("basic_requests_completed")


async def demonstrate_client_session():
    """Show UniversalClient for session management with mocked responses."""
    logger.info("client_session_started", demo="transport_client_mocked")
    
    # Create client with custom configuration
    client = UniversalClient(
        default_headers={
            "User-Agent": "Foundation-Demo/1.0",
            "Accept": "application/json"
        },
        default_timeout=30.0
    )
    
    # Mock responses for different endpoints
    mock_responses = {
        "users": Response(
            status=200,
            headers={"content-type": "application/json"},
            body=b'{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}',
            elapsed_ms=156.7
        ),
        "create": Response(
            status=201,
            headers={"content-type": "application/json"},
            body=b'{"id": 3, "name": "New User", "email": "user@example.com", "created": true}',
            elapsed_ms=234.1
        ),
        "update": Response(
            status=200,
            headers={"content-type": "application/json"},
            body=b'{"id": 3, "name": "Updated User", "status": "active", "updated": true}',
            elapsed_ms=189.3
        )
    }
    
    async with client:
        logger.info("making_multiple_mocked_requests", count=3)
        
        # Mock the client methods
        with patch.object(client, 'get', new_callable=AsyncMock) as mock_client_get:
            mock_client_get.return_value = mock_responses["users"]
            
            users_response = await client.get(
                "https://api.example.com/users",
                params={"endpoint": "users", "page": 1}
            )
            
            if users_response.is_success():
                logger.info("users_request_success", 
                           status=users_response.status,
                           duration_ms=users_response.elapsed_ms,
                           mocked=True)
        
        with patch.object(client, 'post', new_callable=AsyncMock) as mock_client_post:
            mock_client_post.return_value = mock_responses["create"]
            
            create_response = await client.post(
                "https://api.example.com/users",
                body={"name": "New User", "email": "user@example.com"}
            )
            
            if create_response.is_success():
                logger.info("create_request_success",
                           status=create_response.status,
                           duration_ms=create_response.elapsed_ms,
                           mocked=True)
        
        with patch.object(client, 'put', new_callable=AsyncMock) as mock_client_put:
            mock_client_put.return_value = mock_responses["update"]
            
            update_response = await client.put(
                "https://api.example.com/users/3",
                body={"name": "Updated User", "status": "active"}
            )
            
            if update_response.is_success():
                logger.info("update_request_success",
                           status=update_response.status,
                           duration_ms=update_response.elapsed_ms,
                           mocked=True)
    
    logger.info("client_session_completed")


async def demonstrate_middleware():
    """Show middleware configuration and usage with mocked responses."""
    logger.info("middleware_demo_started", demo="transport_client_mocked")
    
    # Create custom middleware pipeline
    retry_policy = RetryPolicy(
        max_attempts=3,
        backoff=BackoffStrategy.EXPONENTIAL,
        base_delay=1.0,
        max_delay=10.0,
        jitter=True
    )
    
    pipeline = MiddlewarePipeline([
        LoggingMiddleware(log_requests=True, log_responses=True),
        MetricsMiddleware(),
        RetryMiddleware(policy=retry_policy)
    ])
    
    client = UniversalClient(middleware=pipeline)
    
    # Mock successful response
    mock_success_response = Response(
        status=200,
        headers={"content-type": "application/json"},
        body=b'{"status": "success", "middleware": "processed"}',
        elapsed_ms=98.4
    )
    
    async with client:
        logger.info("middleware_configured", 
                   middlewares=["logging", "metrics", "retry"])
        
        with patch.object(client, 'get', new_callable=AsyncMock) as mock_client_get:
            mock_client_get.return_value = mock_success_response
            
            # Request will be processed through middleware
            response = await client.get(
                "https://api.example.com/status",
                timeout=5.0
            )
            
            logger.info("middleware_request_completed",
                       status=response.status,
                       middlewares_applied=True,
                       mocked=True)
    
    logger.info("middleware_demo_completed")


async def demonstrate_error_handling():
    """Show comprehensive error handling with mocked error scenarios."""
    logger.info("error_handling_demo_started", demo="transport_client_mocked")
    
    # Define mock error scenarios
    error_scenarios = [
        ("timeout", TransportTimeoutError("Request timed out", request=None)),
        ("not_found", Response(status=404, headers={}, body=b'{"error": "Not Found"}', elapsed_ms=45.2)),
        ("server_error", Response(status=500, headers={}, body=b'{"error": "Internal Server Error"}', elapsed_ms=123.8)),
        ("connection_failed", TransportConnectionError("Connection failed", request=None))
    ]
    
    for scenario_name, error_or_response in error_scenarios:
        try:
            logger.info("testing_mocked_error_scenario", scenario=scenario_name)
            
            if isinstance(error_or_response, Exception):
                # Mock an exception
                with patch('provide.foundation.transport.get', new_callable=AsyncMock) as mock_get:
                    mock_get.side_effect = error_or_response
                    response = await get("https://api.example.com/test", timeout=2.0)
            else:
                # Mock an error response
                with patch('provide.foundation.transport.get', new_callable=AsyncMock) as mock_get:
                    mock_get.return_value = error_or_response
                    response = await get("https://api.example.com/test", timeout=2.0)
                
                if not response.is_success():
                    logger.warning("http_error_response",
                                  scenario=scenario_name,
                                  status=response.status,
                                  mocked=True)
                else:
                    logger.info("unexpected_success",
                               scenario=scenario_name,
                               status=response.status,
                               mocked=True)
                
        except TransportTimeoutError:
            logger.error("timeout_error", scenario=scenario_name, mocked=True)
            
        except TransportConnectionError as e:
            logger.error("connection_error", 
                        scenario=scenario_name, 
                        error=str(e),
                        mocked=True)
            
        except HTTPResponseError as e:
            logger.error("http_response_error",
                        scenario=scenario_name,
                        status=e.status_code,
                        mocked=True)
            
        except TransportError as e:
            logger.error("transport_error",
                        scenario=scenario_name,
                        error=str(e),
                        error_type=type(e).__name__,
                        mocked=True)
    
    logger.info("error_handling_demo_completed")


async def demonstrate_response_processing():
    """Show different response processing techniques with mocked data."""
    logger.info("response_processing_started", demo="transport_client_mocked")
    
    # Mock different response types
    json_response_mock = Response(
        status=200,
        headers={"content-type": "application/json"},
        body=b'{"slideshow": {"author": "Foundation", "title": "Transport Demo"}}',
        elapsed_ms=67.3
    )
    
    text_response_mock = Response(
        status=200,
        headers={"content-type": "text/plain"},
        body=b"User-agent: *\nDisallow: /private\nAllow: /public",
        elapsed_ms=34.1
    )
    
    headers_response_mock = Response(
        status=200,
        headers={
            "content-type": "application/json",
            "x-custom-header": "demo-value",
            "x-server": "foundation-transport"
        },
        body=b'{"custom_header": "demo-value", "server": "foundation-transport"}',
        elapsed_ms=89.7
    )
    
    # Test JSON response processing
    with patch('provide.foundation.transport.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = json_response_mock
        json_response = await get("https://api.example.com/json")
        
        if json_response.is_success():
            data = json_response.json()
            logger.info("json_response_processed",
                       type="json",
                       keys=list(data.keys()) if isinstance(data, dict) else None,
                       mocked=True)
    
    # Test text response processing
    with patch('provide.foundation.transport.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = text_response_mock
        text_response = await get("https://api.example.com/robots.txt")
        
        if text_response.is_success():
            text_content = text_response.text
            logger.info("text_response_processed",
                       type="text",
                       length=len(text_content),
                       preview=text_content[:50] + "..." if len(text_content) > 50 else text_content,
                       mocked=True)
    
    # Test headers inspection
    with patch('provide.foundation.transport.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = headers_response_mock
        headers_response = await get("https://api.example.com/headers")
        
        if headers_response.is_success():
            logger.info("headers_response_processed",
                       type="headers",
                       response_headers=dict(headers_response.headers),
                       content_type=headers_response.headers.get("content-type"),
                       mocked=True)
    
    logger.info("response_processing_completed")


async def demonstrate_default_client():
    """Show usage of the global default client with mocked responses."""
    logger.info("default_client_demo_started", demo="transport_client_mocked")
    
    # The global functions use a default client instance
    client = get_default_client()
    logger.info("default_client_retrieved", client_id=id(client), mocked=True)
    
    # Mock responses for default client usage
    uuid_response_mock = Response(
        status=200,
        headers={"content-type": "application/json"},
        body=b'{"uuid": "550e8400-e29b-41d4-a716-446655440000"}',
        elapsed_ms=78.2
    )
    
    post_response_mock = Response(
        status=201,
        headers={"content-type": "application/json"},
        body=b'{"data": {"test": "data"}, "created": true}',
        elapsed_ms=156.4
    )
    
    get_response_mock = Response(
        status=200,
        headers={"content-type": "application/json"},
        body=b'{"method": "GET", "client": "default"}',
        elapsed_ms=92.7
    )
    
    # Test direct function calls (which use the default client)
    with patch('provide.foundation.transport.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = uuid_response_mock
        response1 = await get("https://api.example.com/uuid")
    
    with patch('provide.foundation.transport.post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value = post_response_mock
        response2 = await post("https://api.example.com/post", body={"test": "data"})
    
    if response1.is_success() and response2.is_success():
        logger.info("default_client_requests_success",
                   get_status=response1.status,
                   post_status=response2.status,
                   mocked=True)
    
    # Test manual client usage (same instance)
    with patch.object(client, 'get', new_callable=AsyncMock) as mock_client_get:
        mock_client_get.return_value = get_response_mock
        response3 = await client.get("https://api.example.com/get")
        
        if response3.is_success():
            logger.info("manual_default_client_success",
                       status=response3.status,
                       mocked=True)
    
    logger.info("default_client_demo_completed")


async def main():
    """Run all transport client demonstrations using Foundation mocking."""
    logger.info("transport_client_example_started", 
               version="1.0.0",
               examples=["basic", "session", "middleware", "errors", "processing", "default_client"],
               mocking="foundation_testing_utilities")
    
    # Run each demonstration
    await demonstrate_basic_requests()
    await demonstrate_client_session()
    await demonstrate_middleware()
    await demonstrate_error_handling()
    await demonstrate_response_processing()
    await demonstrate_default_client()
    
    logger.info("transport_client_example_completed", 
               demos_completed=6,
               status="success",
               dogfooding="100_percent_foundation")


if __name__ == "__main__":
    # Initialize Foundation telemetry
    setup_telemetry()
    
    # Run the async example
    asyncio.run(main())