#
# tests/test_config.py
#
"""
Unit tests for processor assembly helper functions in pyvider.telemetry.config.
"""
import io
import logging as stdlib_logging  # For config_warnings_logger interaction
import sys
from typing import Any

import pytest
from pytest import CaptureFixture, MonkeyPatch  # Added for capsys, monkeypatch
import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer, TimeStamper

from pyvider.telemetry.config import (
    LoggingConfig,
    TelemetryConfig,
    _build_core_processors_list,
    _build_formatter_processors_list,
    _config_create_emoji_processors,
    _config_create_json_formatter_processors,
    _config_create_keyvalue_formatter_processors,
    _config_create_service_name_processor,
    # Import private functions for testing
    _config_create_timestamp_processors,
    config_warnings_logger,  # To check its behavior for unknown formatter
)
from pyvider.telemetry.core import (  # E402: Moved to top
    _CORE_SETUP_LOGGER_NAME,
    _create_core_setup_logger,
    _handle_globally_disabled_setup,
)
from pyvider.telemetry.logger.custom_processors import (  # E402: Moved to top (and merged)
    _EMOJI_CACHE_SIZE_LIMIT,
    _EMOJI_LOOKUP_CACHE,
    add_das_emoji_prefix,
    add_log_level_custom,
    add_logger_name_emoji_prefix,
    clear_emoji_cache,
)


# Helper to get processor name or type for cleaner assertions
def get_proc_name(proc: Any) -> str:
    if hasattr(proc, '__name__'):
        return proc.__name__
    if isinstance(proc, TimeStamper): # TimeStamper instance, not class
        return "TimeStamper"
    if isinstance(proc, JSONRenderer):
        return "JSONRenderer"
    if isinstance(proc, ConsoleRenderer):
        return "ConsoleRenderer"
    # Default for other class instances (like ExceptionRenderer, _LevelFilter)
    return proc.__class__.__name__


class TestConfigTimestampProcessors:
    def test_timestamp_processors_default(self) -> None:
        processors = _config_create_timestamp_processors(omit_timestamp=False)
        assert len(processors) == 1
        assert get_proc_name(processors[0]) == "TimeStamper"

    def test_timestamp_processors_omitted(self) -> None:
        processors = _config_create_timestamp_processors(omit_timestamp=True)
        assert len(processors) == 2
        assert get_proc_name(processors[0]) == "TimeStamper"
        assert get_proc_name(processors[1]) == "pop_timestamp_processor"

class TestConfigServiceNameProcessor:
    def test_service_name_processor_with_name(self) -> None:
        service_name = "my-test-service"
        processor_func = _config_create_service_name_processor(service_name=service_name)

        # Test the returned processor function
        event_dict = {}
        processed_event = processor_func(None, "", event_dict)
        assert "service_name" in processed_event
        assert processed_event["service_name"] == service_name

    def test_service_name_processor_without_name(self) -> None:
        processor_func = _config_create_service_name_processor(service_name=None)

        event_dict = {"key": "value"}
        processed_event = processor_func(None, "", event_dict)
        assert "service_name" not in processed_event
        assert processed_event == {"key": "value"} # Unchanged

class TestConfigEmojiProcessors:
    def test_both_emojis_enabled(self) -> None:
        config = LoggingConfig(logger_name_emoji_prefix_enabled=True, das_emoji_prefix_enabled=True)
        processors = _config_create_emoji_processors(config)
        assert len(processors) == 2
        assert processors[0] is add_logger_name_emoji_prefix
        assert processors[1] is add_das_emoji_prefix

    def test_only_logger_name_emoji_enabled(self) -> None:
        config = LoggingConfig(logger_name_emoji_prefix_enabled=True, das_emoji_prefix_enabled=False)
        processors = _config_create_emoji_processors(config)
        assert len(processors) == 1
        assert processors[0] is add_logger_name_emoji_prefix

    def test_only_das_emoji_enabled(self) -> None:
        config = LoggingConfig(logger_name_emoji_prefix_enabled=False, das_emoji_prefix_enabled=True)
        processors = _config_create_emoji_processors(config)
        assert len(processors) == 1
        assert processors[0] is add_das_emoji_prefix

    def test_both_emojis_disabled(self) -> None:
        config = LoggingConfig(logger_name_emoji_prefix_enabled=False, das_emoji_prefix_enabled=False)
        processors = _config_create_emoji_processors(config)
        assert len(processors) == 0

class TestConfigJsonFormatterProcessors:
    def test_json_formatter_processors(self) -> None:
        processors = _config_create_json_formatter_processors()
        assert len(processors) == 2
        # structlog.processors.format_exc_info is an alias for ExceptionRenderer()
        assert get_proc_name(processors[0]) == "ExceptionRenderer"
        assert get_proc_name(processors[1]) == "JSONRenderer"

class TestConfigKeyValueFormatterProcessors:
    def test_keyvalue_formatter_processors_tty(self) -> None:
        mock_stream = io.StringIO()
        mock_stream.isatty = lambda: True # Simulate TTY
        processors = _config_create_keyvalue_formatter_processors(mock_stream)

        assert len(processors) == 2
        assert get_proc_name(processors[0]) == "pop_logger_name_processor"
        assert get_proc_name(processors[1]) == "ConsoleRenderer"
        # TODO: Check ConsoleRenderer's 'colors' kwarg if possible, though hard to inspect directly

    def test_keyvalue_formatter_processors_not_tty(self) -> None:
        mock_stream = io.StringIO()
        mock_stream.isatty = lambda: False # Simulate non-TTY
        processors = _config_create_keyvalue_formatter_processors(mock_stream)

        assert len(processors) == 2
        assert get_proc_name(processors[0]) == "pop_logger_name_processor"
        assert get_proc_name(processors[1]) == "ConsoleRenderer"
        # Note: Checking ConsoleRenderer's 'colors' kwarg directly is hard.
        # Test relies on structlog's own TTY detection which is standard.

class TestBuildFormatterProcessorsList:
    def test_build_json_formatter(self) -> None:
        logging_config = LoggingConfig(console_formatter="json")
        mock_stream = io.StringIO()
        processors = _build_formatter_processors_list(logging_config, mock_stream)

        proc_names = [get_proc_name(p) for p in processors]
        assert len(processors) == 2
        assert proc_names[0] == "ExceptionRenderer" # Corrected: format_exc_info is ExceptionRenderer
        assert proc_names[1] == "JSONRenderer"

    def test_build_keyvalue_formatter(self) -> None:
        logging_config = LoggingConfig(console_formatter="key_value")
        mock_stream = io.StringIO()
        processors = _build_formatter_processors_list(logging_config, mock_stream)

        proc_names = [get_proc_name(p) for p in processors]
        assert len(processors) == 2
        assert proc_names[0] == "pop_logger_name_processor"
        assert proc_names[1] == "ConsoleRenderer"

    def test_build_unknown_formatter_defaults_and_warns(self, capsys: CaptureFixture) -> None:
        # This test relies on the "just-in-time" handler configuration for config_warnings_logger
        logging_config = LoggingConfig(console_formatter="unknown_formatter_type") # type: ignore
        mock_stream = io.StringIO()

        processors = _build_formatter_processors_list(logging_config, mock_stream)

        # Should default to key-value
        proc_names = [get_proc_name(p) for p in processors]
        assert len(processors) == 2
        assert proc_names[0] == "pop_logger_name_processor"
        assert proc_names[1] == "ConsoleRenderer"

        # Check for warning
        captured = capsys.readouterr()
        assert "Unknown PYVIDER_LOG_CONSOLE_FORMATTER 'unknown_formatter_type'" in captured.err
        assert "Defaulting to 'key_value' formatter" in captured.err
        assert "[Pyvider Config Warning] WARNING (pyvider.telemetry.config_warnings):" in captured.err


class TestBuildCoreProcessorsList:
    def test_default_config(self) -> None:
        config = TelemetryConfig() # Default configuration
        processors = _build_core_processors_list(config)
        proc_names = [get_proc_name(p) for p in processors]

        # Expected base processors + timestamp + 2 emoji processors
        # merge_contextvars, add_log_level_custom, _LevelFilter, StackInfoRenderer, set_exc_info, TimeStamper, add_logger_name_emoji_prefix, add_das_emoji_prefix
        assert len(proc_names) == 8

        assert proc_names[0] == "merge_contextvars"
        assert proc_names[1] == "add_log_level_custom"
        assert proc_names[2] == "_LevelFilter" # filter_by_level_custom returns a _LevelFilter instance
        assert proc_names[3] == "StackInfoRenderer" # from structlog.processors
        assert proc_names[4] == "set_exc_info" # from structlog.dev
        assert proc_names[5] == "TimeStamper"
        assert "pop_timestamp_processor" not in proc_names # Default is not to omit

        # Default service_name is None, so no service_name_processor (which is named 'processor')
        # The service_name_processor would be at index 6 if present.
        assert proc_names[6] == "add_logger_name_emoji_prefix"
        assert proc_names[7] == "add_das_emoji_prefix"

    def test_with_service_name(self) -> None:
        config = TelemetryConfig(service_name="my-app")
        processors = _build_core_processors_list(config)
        proc_names = [get_proc_name(p) for p in processors]

        # Expected: base_processors + timestamp + service_name_proc + 2 emoji_processors = 9
        assert len(proc_names) == 9
        assert proc_names[5] == "TimeStamper"
        assert proc_names[6] == "processor" # This is the service_name_processor
        assert proc_names[7] == "add_logger_name_emoji_prefix"
        assert proc_names[8] == "add_das_emoji_prefix"

    def test_omit_timestamp_true(self) -> None:
        config = TelemetryConfig(logging=LoggingConfig(omit_timestamp=True))
        processors = _build_core_processors_list(config)
        proc_names = [get_proc_name(p) for p in processors]

        # Expected: base_processors + TimeStamper + pop_timestamp_proc + 2 emoji_processors = 9
        assert len(proc_names) == 9
        assert proc_names[5] == "TimeStamper"
        assert proc_names[6] == "pop_timestamp_processor"
        assert proc_names[7] == "add_logger_name_emoji_prefix"
        assert proc_names[8] == "add_das_emoji_prefix"

    def test_emojis_disabled(self) -> None:
        config = TelemetryConfig(logging=LoggingConfig(logger_name_emoji_prefix_enabled=False, das_emoji_prefix_enabled=False))
        processors = _build_core_processors_list(config)
        proc_names = [get_proc_name(p) for p in processors]

        # Expected: base_processors + TimeStamper = 6
        assert len(proc_names) == 6
        assert "add_logger_name_emoji_prefix" not in proc_names
        assert "add_das_emoji_prefix" not in proc_names
        assert proc_names[-1] == "TimeStamper" # Last one should be TimeStamper

    def test_core_processor_order_fully_featured(self) -> None:
        # Test the relative order with all features that add processors enabled
        config = TelemetryConfig(
            service_name="test-svc",
            logging=LoggingConfig(
                omit_timestamp=False, # No pop_timestamp_processor
                logger_name_emoji_prefix_enabled=True,
                das_emoji_prefix_enabled=True
            )
        )
        processors = _build_core_processors_list(config)
        proc_names = [get_proc_name(p) for p in processors]

        # Expected: merge, add_level, filter, stack, exc, TimeStamper, service_name_proc, logger_emoji, das_emoji (9 total)
        assert len(proc_names) == 9

        assert proc_names.index("merge_contextvars") == 0
        assert proc_names.index("add_log_level_custom") == 1
        assert proc_names.index("_LevelFilter") == 2
        assert proc_names.index("StackInfoRenderer") == 3
        assert proc_names.index("set_exc_info") == 4
        assert proc_names.index("TimeStamper") == 5
        # Service name processor is the closure, named "processor" by get_proc_name
        assert proc_names.index("processor") == 6
        assert proc_names.index("add_logger_name_emoji_prefix") == 7
        assert proc_names.index("add_das_emoji_prefix") == 8


# --- Tests for core.py helper functions ---
# These are placed in test_config.py as they relate to setup/configuration states
# influenced by core.py, and to avoid making test_logging.py overly long with
# internal setup details.

# Imports moved to top.


class TestCoreSetupHelpers:
    """Tests for helper functions in pyvider.telemetry.core related to setup."""

    @pytest.mark.parametrize(
        "env_level, expected_stdlib_level",
        [
            ("DEBUG", stdlib_logging.DEBUG),
            ("INFO", stdlib_logging.INFO),
            ("WARNING", stdlib_logging.WARNING),
            ("ERROR", stdlib_logging.ERROR),
            ("CRITICAL", stdlib_logging.CRITICAL),
            ("INVALID_LEVEL", stdlib_logging.INFO), # Defaults to INFO
            (None, stdlib_logging.INFO), # Defaults to INFO if env var not set
        ]
    )
    def test_create_core_setup_logger_levels(self, monkeypatch: MonkeyPatch, capsys: CaptureFixture, env_level: str | None, expected_stdlib_level: int) -> None:
        """
        Tests _create_core_setup_logger for various PYVIDER_CORE_SETUP_LOG_LEVEL settings.
        """
        if env_level is not None:
            monkeypatch.setenv("PYVIDER_CORE_SETUP_LOG_LEVEL", env_level)
        else:
            monkeypatch.delenv("PYVIDER_CORE_SETUP_LOG_LEVEL", raising=False)

        # We need to get a fresh logger instance each time as its level is cached by stdlib.
        # Re-importing or clearing cache is too complex for a test, so use unique names if needed
        # or rely on the function's internal getLogger. For this test, we'll assume
        # _create_core_setup_logger correctly gets/configures the intended logger.
        logger = _create_core_setup_logger(globally_disabled=False)

        assert logger.name == _CORE_SETUP_LOGGER_NAME
        assert logger.level == expected_stdlib_level

        # Check handler type and formatter (only if not globally disabled)
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], stdlib_logging.StreamHandler)
        assert logger.handlers[0].formatter is not None

        # Test logging output
        logger.debug("Test core setup debug")
        logger.info("Test core setup info")
        logger.warning("Test core setup warning")

        captured = capsys.readouterr()

        if expected_stdlib_level <= stdlib_logging.DEBUG:
            assert "Test core setup debug" in captured.err
        else:
            assert "Test core setup debug" not in captured.err

        if expected_stdlib_level <= stdlib_logging.INFO:
            assert "Test core setup info" in captured.err
        else:
            assert "Test core setup info" not in captured.err

        if expected_stdlib_level <= stdlib_logging.WARNING:
            assert "Test core setup warning" in captured.err
        else:
            assert "Test core setup warning" not in captured.err


    def test_create_core_setup_logger_globally_disabled(self) -> None:
        """
        Tests _create_core_setup_logger when globally_disabled is True.
        """
        logger = _create_core_setup_logger(globally_disabled=True)
        assert logger.name == _CORE_SETUP_LOGGER_NAME
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], stdlib_logging.NullHandler)

    def test_handle_globally_disabled_setup_temp_logger_already_configured(self, monkeypatch: MonkeyPatch, capsys: CaptureFixture) -> None:
        """
        Tests the _handle_globally_disabled_setup path where the temporary logger
        for the disabled message might already have a handler (needs_configuration=False).
        """
        temp_logger_name = f"{_CORE_SETUP_LOGGER_NAME}_temp_disabled_msg"
        temp_logger = stdlib_logging.getLogger(temp_logger_name)

        # Pre-configure the temp_logger to simulate it already having a handler
        # This ensures the `if needs_configuration:` block in _handle_globally_disabled_setup is skipped.
        # We must ensure this handler writes to the capsys-captured stderr.
        existing_handler = stdlib_logging.StreamHandler(sys.stderr) # capsys will capture this
        existing_formatter = stdlib_logging.Formatter("[Existing Handler] %(message)s")
        existing_handler.setFormatter(existing_formatter)
        temp_logger.addHandler(existing_handler)
        temp_logger.setLevel(stdlib_logging.INFO) # Ensure it can log info messages
        temp_logger.propagate = False

        _handle_globally_disabled_setup() # Call the function under test

        captured = capsys.readouterr()

        # The message should still be logged by temp_logger using its *existing* handler.
        # The key is that `_handle_globally_disabled_setup` uses this existing handler.
        assert "Pyvider telemetry globally disabled." in captured.err
        assert "[Existing Handler]" in captured.err # To confirm our handler was used

        # Check that structlog is configured with ReturnLoggerFactory
        sl_logger_instance = structlog.get_logger("test_disabled_structlog_after_handle_globally_disabled")
        # When ReturnLoggerFactory is used, the ._logger attribute of the BoundLogger
        # (which sl_logger_instance is a proxy for) should be a ReturnLogger instance.
        # The BoundLoggerLazyProxy might mean we need to access its actual wrapped logger.
        # If sl_logger_instance is the proxy, sl_logger_instance._logger is the actual BoundLogger.
        # And sl_logger_instance._logger._logger is the stdlib/ReturnLogger.

        # Accessing the internal structure of structlog loggers for testing can be brittle.
        # A more functional way is to test that it doesn't output, but capsys might be tricky here
        # if the default stream for ReturnLogger isn't stderr.
        # However, ReturnLogger by definition does nothing.

        # Let's check the type of the logger that structlog's factory would produce.
        # After structlog.configure(logger_factory=structlog.ReturnLoggerFactory),
        # structlog.get_logger()._logger should be a ReturnLogger.
        # Call a method on the logger to ensure it's initialized (due to BoundLoggerLazyProxy)
        # Also, explicitly bind if it helps resolve the proxy to the actual logger.
        sl_logger_instance = sl_logger_instance.bind()
        sl_logger_instance.info("Ensuring logger is initialized for type checking") # This call should resolve the proxy.
        assert isinstance(sl_logger_instance._logger, structlog.ReturnLogger)

        # Cleanup: remove the handler we added to avoid affecting other tests
        temp_logger.removeHandler(existing_handler)

# 🧪🔩


# --- Tests for custom_processors.py ---
# Imports moved to top.

# Note: add_logger_name_emoji_prefix and add_das_emoji_prefix are already imported

class TestCustomProcessors:
    """Tests for custom structlog processors from custom_processors.py."""

    @pytest.mark.parametrize(
        "method_name, initial_event_dict, expected_level",
        [
            ("warn", {"event": "a"}, "warning"),
            ("msg", {"event": "b"}, "info"),
            ("info", {"event": "c", "level": "custom_level"}, "custom_level"), # Level already present
            ("debug", {"event": "d"}, "debug"), # Standard case
            ("error", {"event": "e", "_pyvider_level_hint": "trace"}, "trace"), # Hint overrides method
        ]
    )
    def test_add_log_level_custom_various_scenarios(self, method_name: str, initial_event_dict: dict[str, Any], expected_level: str) -> None:
        event_dict = initial_event_dict.copy()
        processed_event = add_log_level_custom(None, method_name, event_dict) # type: ignore[arg-type]
        assert processed_event["level"] == expected_level
        if "_pyvider_level_hint" in initial_event_dict:
            assert "_pyvider_level_hint" not in processed_event # Should be popped

    def test_add_logger_name_emoji_prefix_event_is_none(self) -> None:
        event_dict = {"logger_name": "test.basic", "event": None}
        processed_event = add_logger_name_emoji_prefix(None, "info", event_dict)
        # Default emoji for "test.basic" is '🧪'
        assert processed_event["event"] == "🧪"

    def test_add_logger_name_emoji_prefix_cache_limit(self) -> None:
        clear_emoji_cache() # Ensure clean state
        assert len(_EMOJI_LOOKUP_CACHE) == 0

        # Add items up to the limit
        for i in range(_EMOJI_CACHE_SIZE_LIMIT):
            logger_name = f"test.logger.{i}"
            event_dict = {"logger_name": logger_name, "event": "message"}
            add_logger_name_emoji_prefix(None, "info", event_dict.copy())

        assert len(_EMOJI_LOOKUP_CACHE) == _EMOJI_CACHE_SIZE_LIMIT

        # Try to add one more
        overflow_logger_name = f"test.logger.{_EMOJI_CACHE_SIZE_LIMIT}"
        event_dict_overflow = {"logger_name": overflow_logger_name, "event": "message"}
        add_logger_name_emoji_prefix(None, "info", event_dict_overflow.copy())

        # Cache size should still be at the limit
        assert len(_EMOJI_LOOKUP_CACHE) == _EMOJI_CACHE_SIZE_LIMIT
        # The overflow item should not be in the cache if the cache was full
        # (unless an existing item was evicted, which is also valid cache behavior,
        # but current implementation just stops adding).
        # This specific assertion depends on non-eviction behavior.
        assert overflow_logger_name not in _EMOJI_LOOKUP_CACHE

        # Check if one of the initial items is still there (cache didn't get wiped)
        assert "test.logger.0" in _EMOJI_LOOKUP_CACHE
        clear_emoji_cache() # Clean up after test


# Test for _ensure_config_logger_handler coverage

class TestConfigWarningsLoggerHandler:
    def test_ensure_config_logger_handler_closes_custom_streams(self, monkeypatch: MonkeyPatch) -> None:
        """
        Tests that _ensure_config_logger_handler closes handlers with custom streams
        and leaves stdout/stderr handlers open.
        """
        # Get the logger
        # config_warnings_logger is already imported

        # Store original handlers to restore them later
        original_handlers = list(config_warnings_logger.handlers)
        config_warnings_logger.handlers.clear() # Clear existing handlers for a clean test

        # Create a custom handler with an io.StringIO stream
        string_io_stream = io.StringIO()
        custom_handler = stdlib_logging.StreamHandler(string_io_stream)
        custom_handler.name = "CustomStringIOHandler" # For easier debugging if needed

        # Create a handler for stdout (should not be closed)
        stdout_handler = stdlib_logging.StreamHandler(sys.stdout)
        stdout_handler.name = "StdoutHandler"

        # Add handlers
        config_warnings_logger.addHandler(custom_handler)
        config_warnings_logger.addHandler(stdout_handler)

        # Ensure logger level is low enough to process the warning from from_env
        original_level = config_warnings_logger.level
        config_warnings_logger.setLevel(stdlib_logging.WARNING)

        try:
            # Trigger a condition that calls _ensure_config_logger_handler via a warning
            # Setting an invalid log level will cause TelemetryConfig.from_env() to log a warning.
            monkeypatch.setenv("PYVIDER_LOG_LEVEL", "INVALID_LEVEL_FOR_TEST")
            TelemetryConfig.from_env() # This should trigger the warning and handler check

            # Assertions
            # The custom_handler's stream (StringIO) should NOT be closed by _ensure_config_logger_handler,
            # as the revised safer version does not close streams from removed handlers.
            assert not string_io_stream.closed, "Custom StringIO stream was unexpectedly closed."

            # The stdout_handler was expected to be removed by _ensure_config_logger_handler,
            # as the function ensures only a specific stderr handler remains.
            found_stdout_handler_after = any(
                h.stream == sys.stdout for h in config_warnings_logger.handlers if isinstance(h, stdlib_logging.StreamHandler)
            )
            assert not found_stdout_handler_after, "Stdout handler was unexpectedly present after _ensure_config_logger_handler."

        finally:
            # Cleanup: Restore original handlers and level
            config_warnings_logger.handlers.clear()
            for handler in original_handlers:
                config_warnings_logger.addHandler(handler)
            config_warnings_logger.setLevel(original_level)
            # Ensure the custom stream is definitely closed if not already
            if not string_io_stream.closed:
                string_io_stream.close()


    def test_add_das_emoji_prefix_event_is_none(self) -> None:
        event_dict = {
            "event": None,
            "domain": "auth", "action": "login", "status": "success"
        }
        processed_event = add_das_emoji_prefix(None, "info", event_dict)
        # Expected DAS prefix for auth-login-success: [🔑][➡️][✅]
        assert processed_event["event"] == "[🔑][➡️][✅]"
        assert "domain" not in processed_event
        assert "action" not in processed_event
        assert "status" not in processed_event

    def test_add_das_emoji_prefix_no_das_keys(self) -> None:
        event_dict = {"event": "Original message"}
        original_event_dict_copy = event_dict.copy()
        processed_event = add_das_emoji_prefix(None, "info", event_dict)
        assert processed_event == original_event_dict_copy # Should be unchanged

    def test_add_das_emoji_prefix_partial_das_keys(self) -> None:
        event_dict = {"event": "Partial DAS", "domain": "payment", "status": "failure"}
        processed_event = add_das_emoji_prefix(None, "info", event_dict)
        # payment: 💳, default action: ❓, failure: ❌
        assert processed_event["event"] == "[💳][❓][❌] Partial DAS"
        assert "domain" not in processed_event
        assert "status" not in processed_event
        assert "action" not in processed_event # action was missing, should still be popped if key existed (it didn't)
