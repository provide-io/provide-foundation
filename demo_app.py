#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Demo application showcasing provide.foundation features.

This demo application demonstrates key features:
- Zero-config structured logging with emojis
- Configuration management with environment variables
- Resilience patterns (retry, circuit breaker)
- Error handling with context
- Console I/O utilities
"""

from attrs import define

from provide.foundation import (
    BackoffStrategy,
    circuit_breaker,
    logger,
    perr,
    pout,
    retry,
)
from provide.foundation.config import env_field
from provide.foundation.config.env import RuntimeConfig


@define
class AppConfig(RuntimeConfig):
    """Application configuration loaded from environment."""

    app_name: str = env_field(env_var="APP_NAME", default="demo-app")
    max_retries: int = env_field(env_var="MAX_RETRIES", default=3)
    timeout_seconds: int = env_field(env_var="TIMEOUT", default=30)
    debug_mode: bool = env_field(env_var="DEBUG", default=False)


def demo_logging() -> None:
    """Demonstrate structured logging with emojis."""
    pout("\n📝 DEMO: Structured Logging")
    pout("─" * 60)

    logger.info("Application started", component="main", version="1.0.0")
    logger.debug("Debug information", user_id="user_123", session="abc-456")
    logger.warning("Resource usage high", cpu_percent=85, memory_mb=512)
    logger.error("Operation failed", error_code="E500", retry_count=2)

    pout("✅ Structured logs with automatic emoji prefixes")


def demo_configuration():
    """Demonstrate configuration management."""
    pout("\n⚙️ DEMO: Configuration Management")
    pout("─" * 60)

    config = AppConfig.from_env()

    logger.info(
        "Configuration loaded",
        app_name=config.app_name,
        max_retries=config.max_retries,
        timeout=config.timeout_seconds,
        debug=config.debug_mode,
    )

    pout(f"App Name: {config.app_name}")
    pout(f"Max Retries: {config.max_retries}")
    pout(f"Timeout: {config.timeout_seconds}s")
    pout(f"Debug Mode: {config.debug_mode}")
    pout("✅ Type-safe configuration with environment variables")

    return config


@retry(max_attempts=3, backoff=BackoffStrategy.EXPONENTIAL, base_delay=0.1)
def unreliable_operation(attempt_count: list[int]) -> str:
    """Simulates an unreliable operation that needs retries."""
    attempt_count[0] += 1

    if attempt_count[0] < 3:
        logger.warning(
            "Operation failed, retrying...",
            attempt=attempt_count[0],
            max_attempts=3,
        )
        raise ValueError(f"Failed attempt {attempt_count[0]}")

    logger.info("Operation succeeded", attempt=attempt_count[0])
    return "Success!"


def demo_resilience() -> None:
    """Demonstrate resilience patterns."""
    pout("\n🔄 DEMO: Resilience Patterns (Retry)")
    pout("─" * 60)

    attempt_count = [0]

    try:
        result = unreliable_operation(attempt_count)
        pout(f"Result: {result}")
        pout(f"Total attempts: {attempt_count[0]}")
        pout("✅ Automatic retry with exponential backoff")
    except Exception as e:
        perr(f"Failed after retries: {e}")


@circuit_breaker(failure_threshold=2, recovery_timeout=5.0)
def protected_operation(should_fail: bool) -> str:
    """Operation protected by circuit breaker."""
    if should_fail:
        raise RuntimeError("Service unavailable")
    return "OK"


def demo_circuit_breaker() -> None:
    """Demonstrate circuit breaker pattern."""
    pout("\n⚡ DEMO: Circuit Breaker")
    pout("─" * 60)

    # First call succeeds
    try:
        result = protected_operation(False)
        pout(f"Call 1 (success): {result}")
    except Exception as e:
        perr(f"Call 1 failed: {e}")

    # Subsequent calls fail, triggering circuit breaker
    for i in range(2, 5):
        try:
            result = protected_operation(True)
            pout(f"Call {i}: {result}")
        except Exception as e:
            logger.warning(f"Call {i} failed", error=str(e), call_number=i)

    pout("✅ Circuit breaker protects against cascading failures")


def demo_error_handling() -> None:
    """Demonstrate error handling with context."""
    pout("\n❌ DEMO: Error Handling")
    pout("─" * 60)

    try:
        # Simulate a risky operation
        raise ValueError("Something went wrong")
    except ValueError as e:
        logger.exception("Caught exception with full context", operation="risky_operation")
        pout(f"Error caught and logged: {e}")

    pout("✅ Automatic exception logging with stack traces")


def main() -> None:
    """Run all demos."""
    pout("\n" + "=" * 60)
    pout("🚀 provide.foundation - Demo Application")
    pout("=" * 60)

    # Load configuration
    config = demo_configuration()

    # Demonstrate features
    demo_logging()
    demo_resilience()
    demo_circuit_breaker()
    demo_error_handling()

    # Summary
    pout("\n" + "=" * 60)
    pout("✨ Demo Complete!")
    pout("=" * 60)
    pout("\n📚 Key Features Demonstrated:")
    pout("  • Structured logging with emoji enrichment")
    pout("  • Type-safe configuration from environment")
    pout("  • Retry pattern with exponential backoff")
    pout("  • Circuit breaker for fault tolerance")
    pout("  • Error boundaries with fallbacks")
    pout("  • Console I/O utilities (pout/perr)")

    logger.info("Demo application completed", app_name=config.app_name)


if __name__ == "__main__":
    main()
