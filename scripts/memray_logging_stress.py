#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Memray stress test: Logger pipeline.

Exercises the full logging processor chain with 50K messages
through key_value and JSON formatters, emoji processing, and level filtering.
"""

from __future__ import annotations

import io
import sys


def warmup() -> None:
    """Warmup phase to separate import-time allocations."""
    from provide.foundation import LoggingConfig, TelemetryConfig, get_hub, logger

    stream = io.StringIO()
    from provide.testkit import set_log_stream_for_testing

    set_log_stream_for_testing(stream)

    hub = get_hub()
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=False,
        ),
    )
    hub.initialize_foundation(config, force=True)
    test_logger = logger.get_logger("warmup")
    for i in range(100):
        test_logger.info("warmup message", iteration=i)

    set_log_stream_for_testing(None)


def run_stress() -> None:
    """Run the logging stress test."""
    from provide.testkit import reset_foundation_setup_for_testing, set_log_stream_for_testing

    from provide.foundation import LoggingConfig, TelemetryConfig, get_hub, logger

    message_count = 50_000
    stream = io.StringIO()
    set_log_stream_for_testing(stream)

    # Phase 1: key_value formatter with emoji processing
    hub = get_hub()
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        ),
    )
    hub.initialize_foundation(config, force=True)
    kv_logger = logger.get_logger("stress.kv")

    half = message_count // 2
    for i in range(half):
        kv_logger.info(
            f"key_value message {i}",
            iteration=i,
            domain="stress",
            action="test",
            status="running",
        )

    # Phase 2: JSON formatter
    reset_foundation_setup_for_testing()
    stream = io.StringIO()
    set_log_stream_for_testing(stream)

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        ),
    )
    hub = get_hub()
    hub.initialize_foundation(config, force=True)
    json_logger = logger.get_logger("stress.json")

    for i in range(half):
        json_logger.info(
            f"json message {i}",
            iteration=i,
            domain="stress",
            action="serialize",
            extra_data={"nested": {"value": i}},
        )

    # Phase 3: Level filtering (messages should be filtered out)
    filtered_logger = logger.get_logger("stress.filtered")
    for i in range(message_count // 5):
        filtered_logger.debug(f"filtered message {i}")

    set_log_stream_for_testing(None)
    reset_foundation_setup_for_testing()

    print(f"Logging stress complete: {message_count} messages processed", file=sys.stderr)


if __name__ == "__main__":
    warmup()
    run_stress()
