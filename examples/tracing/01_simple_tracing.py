#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Simple example showing basic tracing with Foundation.

Demonstrates how to add operation timing and context tracking
to your applications without external dependencies."""

from provide.foundation import logger
from provide.foundation.tracer import get_trace_context, with_span

# Logger auto-initializes on first use - no setup required!


def fetch_user_data(user_id: int) -> dict:
    """Fetch user data with tracing."""
    with with_span("fetch_user_data") as span:
        # Add metadata to the span
        span.set_tag("user_id", user_id)
        span.set_tag("operation", "database_query")

        # Get trace context for logging
        trace_ctx = get_trace_context()
        logger.info("Fetching user data", user_id=user_id, trace_id=trace_ctx["trace_id"])

        # Simulate database query with real work
        # In real applications, this would be an actual database call

        # Log completion with timing
        logger.info(
            "User data fetched",
            user_id=user_id,
            duration_ms=span.duration_ms(),
            trace_id=trace_ctx["trace_id"],
        )

        return {
            "id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com",
        }


def process_order(order_data: dict) -> dict:
    """Process an order with nested tracing."""
    with with_span("process_order") as span:
        span.set_tag("order_id", order_data["id"])
        span.set_tag("item_count", len(order_data["items"]))

        trace_ctx = get_trace_context()
        logger.info("Processing order", order_id=order_data["id"], trace_id=trace_ctx["trace_id"])

        # Step 1: Validate order
        with with_span("validate_order") as validation_span:
            validation_span.set_tag("validation_type", "inventory_check")

            logger.info("Validating order", trace_id=trace_ctx["trace_id"])

            # Simulate validation logic
            if len(order_data["items"]) == 0:
                error_msg = "Order has no items"
                validation_span.set_error(error_msg)
                raise ValueError(error_msg)

        # Step 2: Calculate total
        with with_span("calculate_total") as calc_span:
            calc_span.set_tag("currency", "USD")

            logger.info("Calculating order total", trace_id=trace_ctx["trace_id"])

            total = sum(item["price"] * item["quantity"] for item in order_data["items"])
            calc_span.set_tag("total_amount", total)

        # Step 3: Process payment
        with with_span("process_payment") as payment_span:
            payment_span.set_tag("payment_method", order_data.get("payment_method", "credit_card"))
            payment_span.set_tag("amount", total)

            logger.info("Processing payment", amount=total, trace_id=trace_ctx["trace_id"])

            # Simulate payment processing
            payment_span.set_tag("payment_status", "completed")

        span.set_tag("order_status", "completed")
        span.set_tag("total_amount", total)

        logger.info(
            "Order processed successfully",
            order_id=order_data["id"],
            total=total,
            duration_ms=span.duration_ms(),
            trace_id=trace_ctx["trace_id"],
        )

        return {
            "order_id": order_data["id"],
            "status": "completed",
            "total": total,
            "trace_id": trace_ctx["trace_id"],
        }


def batch_process_users(user_ids: list[int]) -> list[dict]:
    """Process multiple users with tracing."""
    with with_span("batch_process_users") as span:
        span.set_tag("batch_size", len(user_ids))

        trace_ctx = get_trace_context()
        logger.info("Starting batch user processing", user_count=len(user_ids), trace_id=trace_ctx["trace_id"])

        results = []
        for user_id in user_ids:
            try:
                # Each user fetch creates a child span
                user_data = fetch_user_data(user_id)
                results.append(user_data)
            except Exception as e:
                logger.error(
                    "Failed to process user", user_id=user_id, error=str(e), trace_id=trace_ctx["trace_id"]
                )

        span.set_tag("successful_count", len(results))
        span.set_tag("failed_count", len(user_ids) - len(results))

        logger.info(
            "Batch processing completed",
            processed=len(results),
            failed=len(user_ids) - len(results),
            trace_id=trace_ctx["trace_id"],
        )

        return results


def main() -> None:
    """Simple tracing demonstration."""
    logger.info("🔍 Simple Tracing Demo")

    # Example 1: Single operation
    logger.info("\n=== Fetching Single User ===")
    user = fetch_user_data(12345)
    logger.info("Result", user_name=user["name"])

    # Example 2: Nested operations
    logger.info("\n=== Processing Order ===")
    order = {
        "id": "ORD-001",
        "items": [
            {"name": "Widget", "price": 29.99, "quantity": 2},
            {"name": "Gadget", "price": 15.50, "quantity": 1},
        ],
        "payment_method": "credit_card",
    }

    try:
        result = process_order(order)
        logger.info("Order completed", order_id=result["order_id"], total=result["total"])
    except Exception as e:
        logger.error("Order failed", error=str(e))

    # Example 3: Batch processing
    logger.info("\n=== Batch Processing Users ===")
    user_ids = [1, 2, 3, 4, 5]
    users = batch_process_users(user_ids)
    logger.info("Batch completed", users_processed=len(users))

    # Example 4: Error handling
    logger.info("\n=== Error Handling Example ===")
    bad_order = {
        "id": "ORD-002",
        "items": [],  # Empty items will cause validation error
        "payment_method": "credit_card",
    }

    try:
        process_order(bad_order)
    except ValueError as e:
        logger.info("Expected error caught", error=str(e))


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
