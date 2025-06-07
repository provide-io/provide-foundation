#!/usr/bin/env python3
# examples/pyvider_telemetry/10_production_patterns.py
"""Demonstrates production-ready logging patterns with Pyvider Telemetry."""

from pathlib import Path
import sys

# Add src to path for examples
example_dir = Path(__file__).resolve().parent.parent  # Go up one level to `examples`
project_root = example_dir.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from pyvider.telemetry import (  # noqa: E402
    LoggingConfig,
    TelemetryConfig,
    logger,
    setup_telemetry,
)
from pyvider.telemetry.core import reset_pyvider_setup_for_testing  # noqa: E402


def example_10_production_patterns() -> None:
    """
    Example 10: Illustrates logging patterns suitable for production environments.

    This includes using structured JSON logging, appropriate log levels (e.g., INFO
    as default, DEBUG for specific problematic modules), and logging key business
    events or health metrics.
    """
    print("\n" + "=" * 60)
    print("🏭 Example 10: Production Patterns")
    print(" Demonstrates: Logging patterns suitable for production environments.")
    print("=" * 60)

    # Production-like configuration
    prod_config = TelemetryConfig(
        service_name="prod-order-service",
        logging=LoggingConfig(
            default_level="INFO",  # Default to INFO to reduce noise
            console_formatter="json",  # Structured JSON for machine parsing
            module_levels={
                "payment_gateway_connector": "DEBUG",  # More detail for a critical integration
                "internal_utils.helpers": "WARNING",  # Less noise from utilities
            },
            omit_timestamp=False,  # Timestamps are crucial in production
            logger_name_emoji_prefix_enabled=False,  # Emojis might be less useful in aggregated JSON logs
            das_emoji_prefix_enabled=False,  # DAS might be preferred as raw keys in JSON
        ),
    )
    setup_telemetry(prod_config)

    # Structured logging for monitoring and alerting
    logger.info(
        "Service health check normal",
        domain="system",
        action="healthcheck",
        status="success",
        response_time_ms=35,
        cpu_usage_percent=15.5,
        memory_usage_mb=128.2,
    )

    logger.warning(
        "High latency detected for upstream service",
        domain="network",
        action="call_upstream",
        status="warning",
        target_service="inventory-api",
        latency_ms=1500,
        threshold_ms=1000,
    )

    logger.error(
        "Order processing failed due to payment authorization error",
        domain="order",
        action="process_payment",
        status="failure",
        order_id="ord_123xyz",
        payment_gateway_error="Insufficient funds",
        alert_level="critical",
    )

    # Business metrics and event logging
    logger.info(
        "New user registration",
        domain="user",
        action="register",
        status="success",
        user_id="usr_abc789",
        signup_channel="organic_search",
    )

    logger.info(
        "Product added to cart",
        domain="cart",
        action="add_item",
        status="success",
        product_id="prod_efg456",
        quantity=2,
        cart_value_usd=79.98,
    )


if __name__ == "__main__":
    # Reset telemetry to ensure this example uses its own configuration
    # and is not affected by previous example runs if scripts were concatenated.
    reset_pyvider_setup_for_testing()
    example_10_production_patterns()
    print("\n✅ Example 10 completed.")
