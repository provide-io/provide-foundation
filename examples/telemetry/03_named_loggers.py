#!/usr/bin/env python3
# examples/foundation_telemetry/03_named_loggers.py
"""Demonstrates usage of named loggers for different components."""

# Add src to path for examples
from utils import setup_example_environment, print_example_header, print_example_completion
setup_example_environment()

from provide.foundation import logger, setup_telemetry  # noqa: E402


def example_3_named_loggers() -> None:
    """
    Example 3: Demonstrates usage of named loggers for different components.

    Named loggers help in identifying the source of log messages and allow for
    module-specific log level filtering (shown in a later example).
    """
    print_example_header(3, "Named Loggers", "Creating and using component-specific loggers.")

    # Re-initialize with defaults for this example
    setup_telemetry()

    # Create component-specific loggers
    auth_logger = logger.get_logger("auth.service")
    db_logger = logger.get_logger("database.connection")
    api_logger = logger.get_logger("api.handlers")

    # Each logger's name can be used for emoji prefixing (if enabled)
    # and module-level filtering.
    auth_logger.info("User authentication attempt", user_id="user123")
    db_logger.warning(
        "Database connection pool nearing capacity", pool_size=20, current=18
    )
    api_logger.debug("Request received for /api/users", request_id="req-abc")


if __name__ == "__main__":
    example_3_named_loggers()
    print_example_completion(3)
