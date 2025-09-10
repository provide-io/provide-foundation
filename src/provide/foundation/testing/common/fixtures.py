"""
Common Mock Objects and Fixtures.

Reusable mock objects for configuration, logging, and other common
testing scenarios across the provide-io ecosystem.
"""

from unittest.mock import Mock, MagicMock, PropertyMock
from typing import Any

import pytest

from provide.foundation import TelemetryConfig
from provide.foundation.logger.config.logging import LoggingConfig


@pytest.fixture
def mock_http_config():
    """
    Standard HTTP configuration for testing.
    
    Returns:
        HTTPConfig with common test settings.
    """
    from provide.foundation.transport.config import HTTPConfig
    
    return HTTPConfig(
        timeout=30.0,
        max_retries=3,
        retry_backoff_factor=0.5,
        verify_ssl=True,
        pool_connections=10,
        pool_maxsize=100,
        follow_redirects=True,
        http2=True,
        max_redirects=5,
    )




@pytest.fixture
def mock_telemetry_config():
    """
    Standard telemetry configuration for testing.
    
    Returns:
        TelemetryConfig with debug logging enabled.
    """
    return TelemetryConfig(
        logging=LoggingConfig(default_level="DEBUG"),
        globally_disabled=False,
        service_name="test_service",
        service_version="1.0.0",
    )


@pytest.fixture
def mock_config_source():
    """
    Mock configuration source for testing config loading.
    
    Returns:
        Mock that simulates a configuration source.
    """
    source = Mock()
    source.load = Mock(return_value={"key": "value", "nested": {"key": "value"}})
    source.exists = Mock(return_value=True)
    source.reload = Mock()
    source.watch = Mock()
    source.priority = 100
    source.name = "mock_source"
    
    return source


@pytest.fixture
def mock_event_emitter():
    """
    Mock event emitter for testing event-driven components.
    
    Returns:
        Mock with emit, on, off methods.
    """
    emitter = Mock()
    emitter.emit = Mock()
    emitter.on = Mock()
    emitter.off = Mock()
    emitter.once = Mock()
    emitter.listeners = Mock(return_value=[])
    emitter.remove_all_listeners = Mock()
    
    return emitter


@pytest.fixture
def mock_transport():
    """
    Mock transport for testing network operations.
    
    Returns:
        Mock transport with request/response methods.
    """
    transport = Mock()
    transport.request = Mock(return_value={"status": 200, "data": {}})
    transport.get = Mock(return_value={"status": 200, "data": {}})
    transport.post = Mock(return_value={"status": 200, "data": {}})
    transport.put = Mock(return_value={"status": 200, "data": {}})
    transport.delete = Mock(return_value={"status": 204})
    transport.close = Mock()
    
    return transport


@pytest.fixture
def mock_metrics_collector():
    """
    Mock metrics collector for testing instrumentation.
    
    Returns:
        Mock with common metrics methods.
    """
    collector = Mock()
    collector.increment = Mock()
    collector.decrement = Mock()
    collector.gauge = Mock()
    collector.histogram = Mock()
    collector.timer = Mock()
    collector.flush = Mock()
    
    # Add context manager support for timing
    timer_cm = Mock()
    timer_cm.__enter__ = Mock(return_value=timer_cm)
    timer_cm.__exit__ = Mock(return_value=None)
    collector.timer.return_value = timer_cm
    
    return collector


@pytest.fixture
def mock_cache():
    """
    Mock cache for testing caching behavior.
    
    Returns:
        Mock with get, set, delete, clear methods.
    """
    cache_data = {}
    
    cache = Mock()
    cache.get = Mock(side_effect=lambda k, default=None: cache_data.get(k, default))
    cache.set = Mock(side_effect=lambda k, v, ttl=None: cache_data.update({k: v}))
    cache.delete = Mock(side_effect=lambda k: cache_data.pop(k, None))
    cache.clear = Mock(side_effect=cache_data.clear)
    cache.exists = Mock(side_effect=lambda k: k in cache_data)
    cache.keys = Mock(return_value=list(cache_data.keys()))
    
    # Store reference to data for test assertions
    cache._data = cache_data
    
    return cache


@pytest.fixture
def mock_database():
    """
    Mock database connection for testing.
    
    Returns:
        Mock with execute, fetch, commit, rollback methods.
    """
    db = Mock()
    db.execute = Mock(return_value=Mock(rowcount=1))
    db.fetch = Mock(return_value=[])
    db.fetchone = Mock(return_value=None)
    db.fetchall = Mock(return_value=[])
    db.commit = Mock()
    db.rollback = Mock()
    db.close = Mock()
    db.is_connected = PropertyMock(return_value=True)
    
    # Add context manager support
    db.__enter__ = Mock(return_value=db)
    db.__exit__ = Mock(return_value=None)
    
    return db


@pytest.fixture
def mock_file_system():
    """
    Mock file system operations.
    
    Returns:
        Mock with read, write, exists, delete methods.
    """
    fs = Mock()
    fs.read = Mock(return_value=b"content")
    fs.write = Mock()
    fs.exists = Mock(return_value=True)
    fs.delete = Mock()
    fs.mkdir = Mock()
    fs.rmdir = Mock()
    fs.list = Mock(return_value=[])
    fs.stat = Mock(return_value=Mock(st_size=1024, st_mtime=0))
    
    return fs


@pytest.fixture
def mock_subprocess():
    """
    Mock subprocess for testing command execution.
    
    Returns:
        Mock with run, Popen methods.
    """
    subprocess = Mock()
    
    # Mock run method
    result = Mock()
    result.returncode = 0
    result.stdout = "output"
    result.stderr = ""
    subprocess.run = Mock(return_value=result)
    
    # Mock Popen
    process = Mock()
    process.communicate = Mock(return_value=("output", ""))
    process.returncode = 0
    process.pid = 12345
    process.poll = Mock(return_value=0)
    process.wait = Mock(return_value=0)
    subprocess.Popen = Mock(return_value=process)
    
    return subprocess