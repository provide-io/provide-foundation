"""
Common testing fixtures for the provide-io ecosystem.

Standard mock objects and fixtures that are used across multiple modules
in any project that depends on provide.foundation.
"""

from provide.foundation.testing.common.fixtures import (
    mock_cache,
    mock_config_source,
    mock_database,
    mock_event_emitter,
    mock_file_system,
    mock_http_config,
    mock_metrics_collector,
    mock_subprocess,
    mock_telemetry_config,
    mock_transport,
)

__all__ = [
    "mock_cache",
    "mock_config_source",
    "mock_database",
    "mock_event_emitter",
    "mock_file_system",
    "mock_http_config",
    "mock_metrics_collector",
    "mock_subprocess",
    "mock_telemetry_config",
    "mock_transport",
]
