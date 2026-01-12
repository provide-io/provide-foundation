#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Example demonstrating Foundation's built-in distributed tracing capabilities.

Shows how to use the tracer module for operation timing, context tracking,
and building trace hierarchies without external dependencies."""

import asyncio
from typing import Any

from provide.foundation import logger
from provide.foundation.tracer import (
    Span,
    get_trace_context,
    with_span,
)

# Logger auto-initializes on first use - no setup required!


def simulate_database_query(query: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Simulate a database query with tracing."""
    with with_span("database_query") as span:
        span.set_tag("query_type", query.split()[0].upper())
        span.set_tag("table", "users" if "users" in query else "orders")

        if params:
            span.set_tag("param_count", len(params))

        # Log with trace context
        trace_ctx = get_trace_context()
        logger.info(
            "Executing database query",
            query=query,
            trace_id=trace_ctx["trace_id"],
            span_id=trace_ctx["span_id"],
        )

        # In real applications, this would be an actual database query
        # No artificial delays needed for demonstration

        # Simulate occasional errors (deterministic for demo)
        if len(query) % 10 == 0:  # Every 10th query fails for demo
            error_msg = f"Database timeout for query: {query[:50]}..."
            span.set_error(error_msg)
            logger.error("Database query failed", error=error_msg, trace_id=trace_ctx["trace_id"])
            raise RuntimeError(error_msg)

        # Deterministic execution time based on query length
        execution_time_ms = (len(query) % 50 + 10) * 5  # 50-295ms range

        logger.info(
            "Database query completed", execution_time_ms=execution_time_ms, trace_id=trace_ctx["trace_id"]
        )

        return {
            "rows": len(query) % 100 + 1,  # Deterministic row count for demo
            "execution_time_ms": execution_time_ms,
        }


def call_external_service(service_name: str, endpoint: str) -> dict[str, Any]:
    """Simulate external service call with tracing."""
    with with_span("external_service_call") as span:
        span.set_tag("service", service_name)
        span.set_tag("endpoint", endpoint)
        span.set_tag("timeout_ms", 5000)

        trace_ctx = get_trace_context()
        logger.info(
            "Calling external service", service=service_name, endpoint=endpoint, trace_id=trace_ctx["trace_id"]
        )

        # Simulate network call (deterministic for demo)
        response_time = (len(service_name) % 10 + 1) * 0.03  # Deterministic timing

        # Deterministic status codes for demo
        status_code = 200 if len(endpoint) % 5 != 0 else (404 if len(endpoint) % 3 == 0 else 500)
        span.set_tag("status_code", status_code)
        span.set_tag("response_time_ms", response_time * 1000)

        if status_code >= 400:
            error_msg = f"HTTP {status_code} from {service_name}{endpoint}"
            span.set_error(error_msg)
            logger.error(
                "External service call failed",
                service=service_name,
                status_code=status_code,
                trace_id=trace_ctx["trace_id"],
            )
            raise RuntimeError(error_msg)

        logger.info(
            "External service call completed",
            service=service_name,
            status_code=status_code,
            response_time_ms=response_time * 1000,
            trace_id=trace_ctx["trace_id"],
        )

        return {
            "status_code": status_code,
            "response_time_ms": response_time * 1000,
            "data": {"result": "success"},
        }


def process_user_registration(user_data: dict[str, Any]) -> dict[str, Any]:
    """Process user registration with comprehensive tracing."""
    with with_span("user_registration") as span:
        span.set_tag("user_email", user_data.get("email", "unknown"))
        span.set_tag("registration_type", user_data.get("type", "standard"))

        trace_ctx = get_trace_context()
        logger.info("Starting user registration", email=user_data.get("email"), trace_id=trace_ctx["trace_id"])

        try:
            # Step 1: Validate user data
            with with_span("validation") as validation_span:
                validation_span.set_tag("fields_count", len(user_data))

                # Simulate validation

                required_fields = ["email", "password", "name"]
                missing_fields = [f for f in required_fields if f not in user_data]

                if missing_fields:
                    error_msg = f"Missing required fields: {missing_fields}"
                    validation_span.set_error(error_msg)
                    raise ValueError(error_msg)

                validation_span.set_tag("validation_result", "passed")
                logger.info("User data validation passed", trace_id=trace_ctx["trace_id"])

            # Step 2: Check if user already exists
            existing_user = simulate_database_query(
                "SELECT id FROM users WHERE email = ?",
                {"email": user_data["email"]},
            )

            if existing_user["rows"] > 0:
                error_msg = f"User with email {user_data['email']} already exists"
                span.set_error(error_msg)
                raise ValueError(error_msg)

            # Step 3: Create user record
            simulate_database_query(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                {
                    "email": user_data["email"],
                    "name": user_data["name"],
                    "password_hash": "hashed_password",
                },
            )

            user_id = 1000 + (hash(user_data["email"]) * 123) % 9000  # Deterministic user IDs for demo
            span.set_tag("user_id", user_id)

            # Step 4: Send welcome email (external service)
            try:
                call_external_service("email_service", "/send_welcome")
                span.set_tag("welcome_email_sent", True)
            except RuntimeError as e:
                # Don't fail registration if email fails
                logger.warning(
                    "Welcome email failed, continuing registration",
                    error=str(e),
                    trace_id=trace_ctx["trace_id"],
                )
                span.set_tag("welcome_email_sent", False)

            # Step 5: Log to analytics service
            try:
                call_external_service("analytics", "/track_registration")
                span.set_tag("analytics_tracked", True)
            except RuntimeError as e:
                # Don't fail registration if analytics fails
                logger.warning("Analytics tracking failed", error=str(e), trace_id=trace_ctx["trace_id"])
                span.set_tag("analytics_tracked", False)

            span.set_tag("registration_status", "completed")
            logger.info(
                "User registration completed successfully",
                user_id=user_id,
                email=user_data["email"],
                trace_id=trace_ctx["trace_id"],
            )

            return {
                "user_id": user_id,
                "status": "success",
                "trace_id": trace_ctx["trace_id"],
                "duration_ms": span.duration_ms(),
            }

        except Exception as e:
            span.set_error(str(e))
            logger.error(
                "User registration failed",
                error=str(e),
                email=user_data.get("email"),
                trace_id=trace_ctx["trace_id"],
            )
            raise


async def async_user_operations() -> None:
    """Example of tracing async operations."""
    logger.info("Starting async user operations example")

    with with_span("async_batch_processing") as batch_span:
        batch_span.set_tag("operation_type", "bulk_user_update")

        trace_ctx = get_trace_context()
        logger.info("Processing user batch", trace_id=trace_ctx["trace_id"])

        # Simulate processing multiple users concurrently
        user_ids = [1001, 1002, 1003, 1004, 1005]
        batch_span.set_tag("user_count", len(user_ids))

        async def process_single_user(user_id: int):
            """Process a single user (async)."""
            # Note: In real async code, you'd need to properly propagate context
            with with_span(f"process_user_{user_id}") as user_span:
                user_span.set_tag("user_id", user_id)

                # Simulate async work
                # In real applications, this would be actual work

                # Simulate database update
                result = simulate_database_query(
                    f"UPDATE users SET last_active = NOW() WHERE id = {user_id}",
                )

                user_span.set_tag("rows_updated", result["rows"])
                return {"user_id": user_id, "updated": True}

        # Process users concurrently
        results = await asyncio.gather(*[process_single_user(uid) for uid in user_ids], return_exceptions=True)

        successful = sum(1 for r in results if not isinstance(r, Exception))
        failed = len(results) - successful

        batch_span.set_tag("successful_updates", successful)
        batch_span.set_tag("failed_updates", failed)

        logger.info(
            "Async batch processing completed",
            successful=successful,
            failed=failed,
            trace_id=trace_ctx["trace_id"],
        )


def trace_analysis_example() -> None:
    """Example showing how to analyze trace data."""
    logger.info("=== Trace Analysis Example ===")

    traces = []

    # Generate sample traces
    for i in range(3):
        user_data = {
            "email": f"user{i}@example.com",
            "name": f"User {i}",
            "password": "secure_password",
            "type": "premium" if i % 2 == 0 else "standard",  # Deterministic type
        }

        try:
            result = process_user_registration(user_data)
            traces.append(result)
        except Exception as e:
            logger.error(f"Registration failed for user {i}", error=str(e))

    # Analyze trace performance
    if traces:
        durations = [t["duration_ms"] for t in traces]
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)

        logger.info(
            "Trace Analysis Results",
            total_traces=len(traces),
            avg_duration_ms=round(avg_duration, 2),
            max_duration_ms=round(max_duration, 2),
            min_duration_ms=round(min_duration, 2),
        )


def main() -> None:
    """Main demonstration of tracing capabilities."""
    logger.info("🔍 Starting Foundation Tracing Demo")

    # Example 1: Simple operation tracing
    logger.info("\n=== Example 1: Simple Operation Tracing ===")
    with with_span("simple_operation") as span:
        span.set_tag("component", "demo")

        logger.info("Performing simple operation")

        span.set_tag("operation_result", "success")
        logger.info("Simple operation completed", duration_ms=span.duration_ms())

    # Example 2: Complex nested tracing
    logger.info("\n=== Example 2: Complex User Registration ===")
    user_data = {
        "email": "john.doe@example.com",
        "name": "John Doe",
        "password": "secure_password123",
        "type": "premium",
    }

    try:
        result = process_user_registration(user_data)
        logger.info("Registration succeeded", **result)
    except Exception as e:
        logger.error("Registration failed", error=str(e))

    # Example 3: Manual span management
    logger.info("\n=== Example 3: Manual Span Management ===")
    manual_span = Span(name="manual_operation")
    manual_span.set_tag("method", "manual")

    # Do some work
    manual_span.set_tag("checkpoint_1", "passed")

    manual_span.set_tag("checkpoint_2", "passed")

    manual_span.finish()

    # Convert to dict for logging
    span_data = manual_span.to_dict()
    logger.info("Manual span completed", **span_data)

    # Example 4: Async operations
    logger.info("\n=== Example 4: Async Operations ===")
    asyncio.run(async_user_operations())

    # Example 5: Trace analysis
    logger.info("\n=== Example 5: Trace Analysis ===")
    trace_analysis_example()

    logger.info("🎉 Foundation Tracing Demo completed!")


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
