#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Setup and performance edge case tests for Foundation Telemetry."""

from __future__ import annotations

from collections.abc import Callable
import io

import pytest

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    get_hub,
    logger,  # This is the global FoundationLogger instance
)


def test_repeated_setup_calls(
    setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_foundation: io.StringIO,
) -> None:
    """Tests behavior with repeated setup calls."""
    config1 = TelemetryConfig(
        service_name="service1",
        logging=LoggingConfig(default_level="DEBUG"),
    )
    config2 = TelemetryConfig(
        service_name="service2",
        logging=LoggingConfig(default_level="INFO"),
    )

    # First setup
    setup_foundation_telemetry_for_test(config1)
    logger.info("Message after first setup")

    # Second setup (should reconfigure)
    setup_foundation_telemetry_for_test(config2)
    logger.info("Message after second setup")
    logger.debug("Debug message (should be filtered in INFO level)")

    output = captured_stderr_for_foundation.getvalue()

    assert "service1" in output
    assert "service2" in output
    assert "Debug message" not in output


def test_concurrent_setup_calls() -> None:
    """Tests thread safety of setup calls."""
    import threading

    configs = [TelemetryConfig(service_name=f"service{i}") for i in range(5)]

    setup_results: list[str | None] = []
    exceptions: list[Exception] = []

    def setup_worker(config: TelemetryConfig) -> None:
        try:
            hub = get_hub()
            hub.initialize_foundation(config, force=True)
            setup_results.append(config.service_name)
        except Exception as e:  # pragma: no cover
            exceptions.append(e)

    threads = []
    for config_item in configs:
        thread = threading.Thread(daemon=True, target=setup_worker, args=(config_item,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join(timeout=5.0)

    assert len(exceptions) == 0, f"Concurrent setup failed: {exceptions}"
    assert len(setup_results) == len(configs)
    pass  # Foundation reset handled by FoundationTestCase


def test_memory_usage_with_large_configs() -> None:
    """Tests memory behavior with large configurations."""
    large_module_levels = {f"module.{i}.submodule.{j}": "DEBUG" for i in range(100) for j in range(10)}

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            module_levels=large_module_levels,  # type: ignore [arg-type]
        ),
    )

    try:
        hub = get_hub()
        hub.initialize_foundation(config, force=True)
        for i in range(0, 100, 10):
            test_logger = logger.get_logger(f"module.{i}.submodule.5")
            test_logger.info(f"Message from module {i}")
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Large configuration failed: {e}")
    finally:
        pass  # Foundation reset handled by FoundationTestCase


def test_performance_with_disabled_features(
    setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_foundation: io.StringIO,
) -> None:
    """Tests performance when emoji features are disabled."""
    import os
    import time

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=False,
        ),
    )
    setup_foundation_telemetry_for_test(config)
    test_logger = logger.get_logger("performance.test")
    start_time = time.time()
    message_count = 1000
    for i in range(message_count):
        test_logger.info(f"Performance test message {i}", iteration=i)
    end_time = time.time()
    duration = end_time - start_time
    output = captured_stderr_for_foundation.getvalue()
    lines = [
        line
        for line in output.strip().splitlines()
        if not line.startswith("[Foundation Setup]")
        and "Configuring structlog output processors" not in line
        and "🗣️ Registered item" not in line
        and not ("[trace    ]" in line or "trace    " in line)
        and line.strip()
    ]
    assert len(lines) == message_count
    # Guard against division by zero when test completes very quickly (parallel execution)
    messages_per_second = message_count / duration if duration > 0 else float("inf")
    if os.environ.get("PYTEST_XDIST_WORKER"):
        min_mps = 200
    else:
        min_mps = 500
    override = os.environ.get("FOUNDATION_TEST_PERF_MIN_MPS")
    if override:
        try:
            min_mps = int(override)
        except ValueError:
            pass
    assert messages_per_second > min_mps, f"Performance too slow: {messages_per_second:.1f} msg/sec"


# 🧱🏗️🔚
