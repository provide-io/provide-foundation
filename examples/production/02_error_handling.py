#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Foundation Error Handling Patterns Example

This example demonstrates Foundation's comprehensive error handling utilities,
including context managers, decorators, custom exceptions, and resilience patterns.

Key Features Demonstrated:
- error_boundary context manager for structured error handling
- resilient decorator for automatic error handling
- Foundation's custom exception hierarchy
- Error context capturing and enrichment
- Retry patterns with exponential backoff
- Fallback strategies and error suppression
- Integration with Foundation's logging system

Requirements:
    uv add provide-foundation

Usage:
    python examples/production/02_error_handling.py

Expected output:
    Structured error handling demonstrations with Foundation's error utilities."""

from pathlib import Path
import sys

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent  # Go up from examples to project root
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import (
    get_hub,
    logger,
    pout,
)
from provide.foundation.errors import (
    FoundationError,
    NetworkError,
    NotFoundError,
    ValidationError,
    capture_error_context,
    error_boundary,
    resilient,
)
from provide.foundation.resilience import (
    BackoffStrategy,
)
from provide.foundation.resilience.decorators import (
    circuit_breaker,
    fallback,
    retry,
)


def example_error_handling() -> None:
    """Demonstrates Foundation's comprehensive error handling patterns.

    This example shows how to use Foundation's error handling utilities
    to build robust applications with proper error management, logging,
    and recovery strategies.
    """
    pout("\n" + "=" * 60)
    pout("🛡️ Example: Foundation Error Handling Patterns")
    pout(" Demonstrates: error_boundary, decorators, custom exceptions, retry patterns")
    pout("=" * 60)

    # Initialize Foundation logging
    get_hub().initialize_foundation()

    # Example 1: Error Boundary Context Manager
    pout("\n🔒 Example 1: Error Boundary Context Manager")
    logger.info("Demonstrating error_boundary context manager")

    def risky_database_operation(fail: bool = False) -> dict[str, str]:
        """Simulate a database operation that might fail."""
        if fail:
            raise NetworkError("Database connection timeout", error_code="DB_TIMEOUT")
        return {"status": "success", "data": "user_data"}

    # Error boundary with structured handling
    result = None
    with error_boundary(NetworkError, log_errors=True, reraise=False):
        result = risky_database_operation(fail=True)

    # If we reach here and result is None, the operation failed
    if result is None:
        logger.warning("Database operation failed, using cached data")
        result = {"status": "cached", "data": "cached_user_data"}

    logger.info("Operation completed", result=result)

    # Example 2: resilient Decorator
    pout("\n🎯 Example 2: resilient Decorator")

    @resilient(
        fallback={"error": "Service unavailable"},
        suppress=(NetworkError, ValidationError),
        log_errors=True,
    )
    def fetch_user_profile(user_id: str) -> dict[str, str]:
        """Fetch user profile with automatic error handling."""
        if user_id == "invalid":
            raise ValidationError(f"Invalid user ID: {user_id}")
        if user_id == "network_fail":
            raise NetworkError("External service unavailable")
        return {"user_id": user_id, "name": "John Doe", "email": "john@example.com"}

    # Test successful case
    logger.info("Testing successful user fetch")
    profile = fetch_user_profile("user123")
    logger.info("User profile fetched", profile=profile)

    # Test error cases with automatic handling
    logger.info("Testing validation error case")
    profile = fetch_user_profile("invalid")
    logger.info("Validation error handled", fallback_result=profile)

    logger.info("Testing network error case")
    profile = fetch_user_profile("network_fail")
    logger.info("Network error handled", fallback_result=profile)

    # Example 3: Custom Foundation Exceptions

    class UserServiceError(FoundationError):
        """Custom exception for user service operations."""

        error_code = "USER_SERVICE_ERROR"

        def __init__(self, message: str, user_id: str | None = None) -> None:
            super().__init__(message)
            self.user_id = user_id

    def process_user_action(user_id: str, action: str) -> dict[str, str]:
        """Process user action with custom error handling."""
        if action == "delete_admin":
            raise UserServiceError(
                f"Cannot delete admin user: {user_id}",
                user_id=user_id,
            )
        return {"user_id": user_id, "action": action, "status": "completed"}

    try:
        result = process_user_action("admin_user", "delete_admin")
    except UserServiceError as e:
        # Capture rich error context
        error_context = capture_error_context(e)
        logger.error(
            "User service operation failed",
            error_code=e.error_code,
            user_id=e.user_id,
            error_context=error_context,
            domain="user_service",
            action="delete_user",
            status="error",
        )

    # Example 4: Retry Patterns with Foundation
    pout("\n🔄 Example 4: Retry Patterns and Resilience")

    # Simple retry with decorator
    attempt_count = 0

    @retry(
        NetworkError,
        max_attempts=3,
        base_delay=0.1,
        backoff=BackoffStrategy.EXPONENTIAL,
    )
    def unreliable_api_call() -> dict[str, str]:
        """Simulate an unreliable API call."""
        nonlocal attempt_count
        attempt_count += 1

        logger.info(f"API call attempt {attempt_count}")

        if attempt_count < 3:
            raise NetworkError(f"API temporarily unavailable (attempt {attempt_count})")

        return {"status": "success", "data": "api_response"}

    logger.info("Testing retry pattern")
    try:
        result = unreliable_api_call()
        logger.info("API call succeeded after retries", result=result)
    except NetworkError as e:
        logger.error("API call failed after all retries", error=str(e))

    # Reset for next example
    attempt_count = 0

    # Example 5: Circuit Breaker Pattern
    pout("\n⚡ Example 5: Circuit Breaker Pattern")

    @circuit_breaker(failure_threshold=2, recovery_timeout=0.5)
    def external_service_call(should_fail: bool = False) -> dict[str, str]:
        """External service call with circuit breaker protection."""
        if should_fail:
            raise NetworkError("External service is down")
        return {"status": "success", "service": "external_api"}

    # Test circuit breaker
    logger.info("Testing circuit breaker pattern")

    # First few calls will fail and trigger circuit breaker
    for i in range(4):
        try:
            result = external_service_call(should_fail=i < 3)
            logger.info(f"Service call {i + 1} succeeded", result=result)
        except Exception as e:
            logger.warning(f"Service call {i + 1} failed", error=str(e))

    # Example 6: Fallback Chains
    pout("\n🎯 Example 6: Fallback Strategies")

    @fallback(
        lambda: {"source": "cache", "data": "cached_response"},
        lambda: {"source": "default", "data": "default_response"},
    )
    def get_data_with_fallback() -> dict[str, str]:
        """Get data with multiple fallback strategies."""
        # Simulate primary service failure
        raise NetworkError("Primary service unavailable")

    logger.info("Testing fallback strategies")
    result = get_data_with_fallback()
    logger.info("Fallback strategy used", result=result)

    # Example 7: Error Context Enrichment
    pout("\n📋 Example 7: Error Context Enrichment")

    def complex_operation_with_context() -> None:
        """Operation with rich error context."""
        operation_context = {
            "operation_id": "op_12345",
            "user_id": "user_789",
            "request_id": "req_abcdef",
            "timestamp": "2024-01-15T10:30:00Z",
        }

        try:
            # Simulate an operation that fails
            raise NotFoundError("Resource not found in database")
        except NotFoundError as e:
            # Enrich error with operational context
            error_context = capture_error_context(e)

            logger.error(
                "Complex operation failed with enriched context",
                error=str(e),
                error_context=error_context,
                **operation_context,
                domain="data_access",
                action="fetch_resource",
                status="error",
            )

    logger.info("Testing error context enrichment")
    complex_operation_with_context()

    logger.info(
        "Error handling demonstration completed",
        domain="examples",
        action="demonstrate_error_handling",
        status="complete",
    )


if __name__ == "__main__":
    example_error_handling()

# 🧱🏗️🔚
