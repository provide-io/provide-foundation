#!/usr/bin/env python3
"""
Example: Transport Client Usage

Demonstrates using the Foundation transport system for HTTP requests with:
- Basic HTTP methods (GET, POST, PUT, DELETE)
- UniversalClient for session management
- Middleware pipeline configuration
- Error handling
- Response processing

This example showcases the full transport API with realistic usage patterns.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path for imports
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent
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


async def demonstrate_basic_requests():
    """Show basic HTTP request methods."""
    logger.info("basic_requests_started", demo="transport_client")
    
    # These would be real API calls in practice
    # For this demo, they'll fail but show the patterns
    
    try:
        # GET request
        logger.info("making_get_request", url="https://httpbin.org/get")
        response = await get(
            "https://httpbin.org/get",
            params={"demo": "foundation", "example": "transport"}
        )
        
        if response.is_success():
            data = response.json()
            logger.info("get_request_success", 
                       status=response.status,
                       args=data.get("args", {}))
        
    except TransportError as e:
        logger.error("get_request_failed", error=str(e))
    
    try:
        # POST request with JSON
        logger.info("making_post_request", url="https://httpbin.org/post")
        response = await post(
            "https://httpbin.org/post",
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
                       json_echo=data.get("json", {}))
        
    except TransportError as e:
        logger.error("post_request_failed", error=str(e))
    
    logger.info("basic_requests_completed")


async def demonstrate_client_session():
    """Show UniversalClient for session management."""
    logger.info("client_session_started", demo="transport_client")
    
    # Create client with custom configuration
    client = UniversalClient(
        default_headers={
            "User-Agent": "Foundation-Demo/1.0",
            "Accept": "application/json"
        },
        default_timeout=30.0
    )
    
    try:
        async with client:
            # Multiple requests using same client session
            logger.info("making_multiple_requests", count=3)
            
            # GET request
            users_response = await client.get(
                "https://httpbin.org/get",
                params={"endpoint": "users", "page": 1}
            )
            
            if users_response.is_success():
                logger.info("users_request_success", 
                           status=users_response.status,
                           duration_ms=users_response.elapsed_ms)
            
            # POST request
            create_response = await client.post(
                "https://httpbin.org/post",
                body={"name": "New User", "email": "user@example.com"}
            )
            
            if create_response.is_success():
                logger.info("create_request_success",
                           status=create_response.status,
                           duration_ms=create_response.elapsed_ms)
            
            # PUT request
            update_response = await client.put(
                "https://httpbin.org/put",
                body={"name": "Updated User", "status": "active"}
            )
            
            if update_response.is_success():
                logger.info("update_request_success",
                           status=update_response.status,
                           duration_ms=update_response.elapsed_ms)
            
    except TransportError as e:
        logger.error("client_session_failed", error=str(e))
    
    logger.info("client_session_completed")


async def demonstrate_middleware():
    """Show middleware configuration and usage."""
    logger.info("middleware_demo_started", demo="transport_client")
    
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
    
    try:
        async with client:
            logger.info("middleware_configured", 
                       middlewares=["logging", "metrics", "retry"])
            
            # Request will be processed through middleware
            response = await client.get(
                "https://httpbin.org/status/200",
                timeout=5.0
            )
            
            logger.info("middleware_request_completed",
                       status=response.status,
                       middlewares_applied=True)
            
    except TransportError as e:
        logger.error("middleware_request_failed", error=str(e))
    
    logger.info("middleware_demo_completed")


async def demonstrate_error_handling():
    """Show comprehensive error handling."""
    logger.info("error_handling_demo_started", demo="transport_client")
    
    # Test different error scenarios
    error_scenarios = [
        ("timeout", "https://httpbin.org/delay/10"),
        ("not_found", "https://httpbin.org/status/404"),
        ("server_error", "https://httpbin.org/status/500"),
        ("invalid_domain", "https://this-domain-does-not-exist.invalid/data")
    ]
    
    for scenario_name, url in error_scenarios:
        try:
            logger.info("testing_error_scenario", scenario=scenario_name, url=url)
            
            response = await get(url, timeout=2.0)
            
            if not response.is_success():
                logger.warning("http_error_response",
                              scenario=scenario_name,
                              status=response.status,
                              url=url)
            else:
                logger.info("unexpected_success",
                           scenario=scenario_name,
                           status=response.status)
                
        except TransportTimeoutError:
            logger.error("timeout_error", scenario=scenario_name, url=url)
            
        except TransportConnectionError as e:
            logger.error("connection_error", 
                        scenario=scenario_name, 
                        url=url,
                        error=str(e))
            
        except HTTPResponseError as e:
            logger.error("http_response_error",
                        scenario=scenario_name,
                        status=e.status_code,
                        url=url)
            
        except TransportError as e:
            logger.error("transport_error",
                        scenario=scenario_name,
                        error=str(e),
                        error_type=type(e).__name__)
    
    logger.info("error_handling_demo_completed")


async def demonstrate_response_processing():
    """Show different response processing techniques."""
    logger.info("response_processing_started", demo="transport_client")
    
    try:
        # JSON response
        json_response = await get("https://httpbin.org/json")
        if json_response.is_success():
            data = json_response.json()
            logger.info("json_response_processed",
                       type="json",
                       keys=list(data.keys()) if isinstance(data, dict) else None)
        
        # Text response
        text_response = await get("https://httpbin.org/robots.txt")
        if text_response.is_success():
            text_content = text_response.text
            logger.info("text_response_processed",
                       type="text",
                       length=len(text_content),
                       preview=text_content[:50] + "..." if len(text_content) > 50 else text_content)
        
        # Headers inspection
        headers_response = await get("https://httpbin.org/response-headers",
                                   params={"X-Custom-Header": "demo-value"})
        if headers_response.is_success():
            logger.info("headers_response_processed",
                       type="headers",
                       response_headers=dict(headers_response.headers),
                       content_type=headers_response.headers.get("content-type"))
    
    except TransportError as e:
        logger.error("response_processing_failed", error=str(e))
    
    logger.info("response_processing_completed")


async def demonstrate_default_client():
    """Show usage of the global default client."""
    logger.info("default_client_demo_started", demo="transport_client")
    
    # The global functions use a default client instance
    client = get_default_client()
    logger.info("default_client_retrieved", client_id=id(client))
    
    try:
        # Direct function calls use the default client
        response1 = await get("https://httpbin.org/uuid")
        response2 = await post("https://httpbin.org/post", body={"test": "data"})
        
        if response1.is_success() and response2.is_success():
            logger.info("default_client_requests_success",
                       get_status=response1.status,
                       post_status=response2.status)
        
        # Manual client usage (same instance)
        response3 = await client.get("https://httpbin.org/get")
        if response3.is_success():
            logger.info("manual_default_client_success",
                       status=response3.status)
    
    except TransportError as e:
        logger.error("default_client_failed", error=str(e))
    
    logger.info("default_client_demo_completed")


async def main():
    """Run all transport client demonstrations."""
    logger.info("transport_client_example_started", 
               version="1.0.0",
               examples=["basic", "session", "middleware", "errors", "processing", "default_client"])
    
    # Run each demonstration
    await demonstrate_basic_requests()
    await demonstrate_client_session()
    await demonstrate_middleware()
    await demonstrate_error_handling()
    await demonstrate_response_processing()
    await demonstrate_default_client()
    
    logger.info("transport_client_example_completed", 
               demos_completed=6,
               status="success")


if __name__ == "__main__":
    # Initialize Foundation telemetry
    setup_telemetry()
    
    # Run the async example
    asyncio.run(main())