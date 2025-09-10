"""
Common testing fixtures for the provide-io ecosystem.

Standard mock objects and fixtures that are used across multiple modules
in any project that depends on provide.foundation.
"""

from provide.foundation.testing.common.fixtures import (
    mock_http_config,
    mock_telemetry_config,
    mock_config_source,
    mock_event_emitter,
    mock_transport,
    mock_metrics_collector,
    mock_cache,
    mock_database,
    mock_file_system,
    mock_subprocess,
)

__all__ = [
    "mock_http_config",
    "mock_telemetry_config",
    "mock_config_source",
    "mock_event_emitter",
    "mock_transport",
    "mock_metrics_collector",
    "mock_cache",
    "mock_database",
    "mock_file_system",
    "mock_subprocess",
]