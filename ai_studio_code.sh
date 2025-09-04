#!/bin/bash
# 🛠️ Project Update Script
set -eo pipefail

# --- Logging ---
log_info() { echo -e "ℹ️  $1"; }
log_create() { echo -e "✨ $1"; }
log_update() { echo -e "🔄 $1"; }
log_delete() { echo -e "🔥 $1"; }
log_success() { echo -e "✅ $1"; }

# --- Operations ---
log_info "Applying changes to the project..."

log_update "Updating: src/provide/foundation/core.py"
mkdir -p src/provide/foundation/
cat <<'EOF' > src/provide/foundation/core.py
#
# core.py
#
"""
Foundation Telemetry Core Initialization and Configuration.
Handles setup, global state, processor chain assembly (including semantic layer resolution),
and shutdown for the telemetry system.
"""

import io
import logging as stdlib_logging
import os
import sys
import threading
from pathlib import Path
from typing import Any, TextIO, cast

import structlog
from structlog.types import BindableLogger

from provide.foundation.logger import base as foundation_logger
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)
from provide.foundation.logger.processors import (
    _build_core_processors_list,
    _build_formatter_processors_list,
)
from provide.foundation.semantic_layers import (
    BUILTIN_SEMANTIC_LAYERS,
    LEGACY_DAS_EMOJI_SETS,
)
from provide.foundation.types import (
    CustomDasEmojiSet,
    SemanticFieldDefinition,
    SemanticLayer,
)

_FOUNDATION_SETUP_LOCK = (
    threading.Lock()
)
_FOUNDATION_LOG_STREAM: TextIO = sys.stderr
_LOG_FILE_HANDLE: TextIO | None = None
_CORE_SETUP_LOGGER_NAME = "provide.foundation.core_setup"
_EXPLICIT_SETUP_DONE = False


def _get_safe_stderr() -> TextIO:
    return (
        sys.stderr
        if hasattr(sys, "stderr") and sys.stderr is not None
        else io.StringIO()
    )


def _set_log_stream_for_testing(stream: TextIO | None) -> None:
    global _FOUNDATION_LOG_STREAM
    _FOUNDATION_LOG_STREAM = stream if stream is not None else sys.stderr


def _ensure_stderr_default() -> None:
    global _FOUNDATION_LOG_STREAM
    if _FOUNDATION_LOG_STREAM is sys.stdout:
        _FOUNDATION_LOG_STREAM = sys.stderr


def _create_core_setup_logger(globally_disabled: bool = False) -> stdlib_logging.Logger:
    logger = stdlib_logging.getLogger(_CORE_SETUP_LOGGER_NAME)
    for h in list(logger.handlers):
        logger.removeHandler(h)
        try:
            if isinstance(h, stdlib_logging.StreamHandler) and h.stream not in (
                sys.stdout,
                sys.stderr,
                _FOUNDATION_LOG_STREAM,
            ):
                h.close()
        except Exception:
            pass
    handler: stdlib_logging.Handler = (
        stdlib_logging.NullHandler()
        if globally_disabled
        else stdlib_logging.StreamHandler(sys.stderr)
    )
    if not globally_disabled:
        handler.setFormatter(
            stdlib_logging.Formatter(
                "[Foundation Setup] %(levelname)s (%(name)s): %(message)s"
            )
        )
    logger.addHandler(handler)
    logger.setLevel(
        getattr(
            stdlib_logging,
            os.getenv("FOUNDATION_CORE_SETUP_LOG_LEVEL", "INFO").upper(),
            stdlib_logging.INFO,
        )
    )
    logger.propagate = False
    return logger


_core_setup_logger = _create_core_setup_logger()

ResolvedSemanticConfig = tuple[
    list[SemanticFieldDefinition], dict[str, CustomDasEmojiSet]
]


def _resolve_active_semantic_config(
    logging_config: LoggingConfig, builtin_layers_registry: dict[str, SemanticLayer]
) -> ResolvedSemanticConfig:
    resolved_fields_dict: dict[str, SemanticFieldDefinition] = {}
    resolved_emoji_sets_dict: dict[str, CustomDasEmojiSet] = {
        s.name: s for s in LEGACY_DAS_EMOJI_SETS
    }

    layers_to_process: list[SemanticLayer] = [
        builtin_layers_registry[name]
        for name in logging_config.enabled_semantic_layers
        if name in builtin_layers_registry
    ]
    layers_to_process.extend(logging_config.custom_semantic_layers)
    layers_to_process.sort(key=lambda layer: layer.priority)

    ordered_log_keys: list[str] = []
    seen_log_keys: set[str] = set()

    for layer in layers_to_process:
        for emoji_set in layer.emoji_sets:
            resolved_emoji_sets_dict[emoji_set.name] = emoji_set
        for field_def in layer.field_definitions:
            resolved_fields_dict[field_def.log_key] = field_def
            if field_def.log_key not in seen_log_keys:
                ordered_log_keys.append(field_def.log_key)
                seen_log_keys.add(field_def.log_key)

    for user_emoji_set in logging_config.user_defined_emoji_sets:
        resolved_emoji_sets_dict[user_emoji_set.name] = user_emoji_set

    final_ordered_field_definitions = [
        resolved_fields_dict[log_key] for log_key in ordered_log_keys
    ]
    return final_ordered_field_definitions, resolved_emoji_sets_dict


def _build_complete_processor_chain(
    config: TelemetryConfig, resolved_semantic_config: ResolvedSemanticConfig
) -> list[Any]:
    core_processors = _build_core_processors_list(config, resolved_semantic_config)
    formatter_processors = _build_formatter_processors_list(
        config.logging, _FOUNDATION_LOG_STREAM
    )
    _core_setup_logger.info(
        f"📝➡️🎨 Configured {config.logging.console_formatter} renderer."
    )
    return cast(list[Any], core_processors + formatter_processors)


def _apply_structlog_configuration(processors: list[Any]) -> None:
    stream_name = (
        "sys.stderr"
        if sys.stderr == _FOUNDATION_LOG_STREAM
        else "custom stream (testing)"
    )
    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=_FOUNDATION_LOG_STREAM),
        wrapper_class=cast(type[BindableLogger], structlog.BoundLogger),
        cache_logger_on_first_use=True,
    )
    _core_setup_logger.info(
        f"📝➡️✅ structlog configured. Wrapper: BoundLogger. Output: {stream_name}."
    )


def _configure_structlog_output(
    config: TelemetryConfig, resolved_semantic_config: ResolvedSemanticConfig
) -> None:
    processors = _build_complete_processor_chain(config, resolved_semantic_config)
    _apply_structlog_configuration(processors)


def _handle_globally_disabled_setup() -> None:
    _core_setup_logger.info("⚙️➡️🚫 Foundation Telemetry globally disabled.")
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def reset_foundation_setup_for_testing() -> None:
    """
    Resets `structlog` defaults and Foundation Telemetry's internal logger state.
    This is a test utility and should not be called by production code.
    """
    global _FOUNDATION_LOG_STREAM, _core_setup_logger, _EXPLICIT_SETUP_DONE, _LOG_FILE_HANDLE
    with _FOUNDATION_SETUP_LOCK:
        structlog.reset_defaults()
        if _LOG_FILE_HANDLE:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception:
                pass
            _LOG_FILE_HANDLE = None
        foundation_logger.logger._is_configured_by_setup = False
        foundation_logger.logger._active_config = None
        foundation_logger.logger._active_resolved_semantic_config = None
        foundation_logger._LAZY_SETUP_STATE.update(
            {"done": False, "error": None, "in_progress": False}
        )
        _FOUNDATION_LOG_STREAM = sys.stderr
        _EXPLICIT_SETUP_DONE = False
        _core_setup_logger = _create_core_setup_logger()


def _internal_setup(
    config: TelemetryConfig | None = None, is_explicit_call: bool = False
) -> None:
    """
    The single, internal setup function that both explicit and lazy setup call.
    It is protected by the _FOUNDATION_SETUP_LOCK in its callers.
    """
    global _core_setup_logger

    # This function assumes the lock is already held.
    structlog.reset_defaults()
    foundation_logger.logger._is_configured_by_setup = False
    foundation_logger.logger._active_config = None
    foundation_logger.logger._active_resolved_semantic_config = None
    foundation_logger._LAZY_SETUP_STATE.update(
        {"done": False, "error": None, "in_progress": False}
    )

    current_config = config if config is not None else TelemetryConfig.from_env()
    _core_setup_logger = _create_core_setup_logger(
        globally_disabled=current_config.globally_disabled
    )

    if not current_config.globally_disabled:
        _core_setup_logger.info("⚙️➡️🚀 Starting Foundation (structlog) setup...")

    resolved_semantic_config = _resolve_active_semantic_config(
        current_config.logging, BUILTIN_SEMANTIC_LAYERS
    )

    if current_config.globally_disabled:
        _handle_globally_disabled_setup()
    else:
        _configure_structlog_output(current_config, resolved_semantic_config)

    foundation_logger.logger._is_configured_by_setup = is_explicit_call
    foundation_logger.logger._active_config = current_config
    foundation_logger.logger._active_resolved_semantic_config = resolved_semantic_config
    foundation_logger._LAZY_SETUP_STATE["done"] = True

    if not current_config.globally_disabled:
        _core_setup_logger.info("⚙️➡️✅ Foundation (structlog) setup completed.")


def setup_telemetry(config: TelemetryConfig | None = None) -> None:
    """
    Initializes or reconfigures the Foundation Telemetry system.
    """
    global _EXPLICIT_SETUP_DONE, _LOG_FILE_HANDLE, _FOUNDATION_LOG_STREAM
    with _FOUNDATION_SETUP_LOCK:
        current_config = config if config is not None else TelemetryConfig.from_env()
        
        if _LOG_FILE_HANDLE and _LOG_FILE_HANDLE is not _FOUNDATION_LOG_STREAM:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception:
                pass
            _LOG_FILE_HANDLE = None

        log_file_path = getattr(current_config.logging, 'log_file', None)
        
        # Preserve testing stream if it's already set and not stderr
        is_test_stream = _FOUNDATION_LOG_STREAM is not sys.stderr and not isinstance(_FOUNDATION_LOG_STREAM, io.TextIOWrapper)

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                # Use line buffering (buffering=1) for files to ensure logs are written promptly.
                _LOG_FILE_HANDLE = open(log_file_path, "a", encoding="utf-8", buffering=1)
                _FOUNDATION_LOG_STREAM = _LOG_FILE_HANDLE
            except Exception as e:
                _core_setup_logger.error(f"Failed to open log file {log_file_path}: {e}")
                _FOUNDATION_LOG_STREAM = _get_safe_stderr()
        elif not is_test_stream:
             _FOUNDATION_LOG_STREAM = _get_safe_stderr()

        _internal_setup(current_config, is_explicit_call=True)
        _EXPLICIT_SETUP_DONE = True


async def shutdown_foundation_telemetry(timeout_millis: int = 5000) -> None:
    global _LOG_FILE_HANDLE
    _core_setup_logger.info("🔌➡️🏁 Foundation Telemetry shutdown called.")
    with _FOUNDATION_SETUP_LOCK:
        if _LOG_FILE_HANDLE:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception as e:
                _core_setup_logger.error(f"Failed to close log file handle: {e}")
            _LOG_FILE_HANDLE = None
EOF

log_update "Updating: src/provide/foundation/utils/timing.py"
mkdir -p src/provide/foundation/utils/
cat <<'EOF' > src/provide/foundation/utils/timing.py
"""
Timing and performance utilities.

Provides context managers and utilities for timing operations and logging performance.
"""

from collections.abc import Generator
from contextlib import contextmanager
import contextvars
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from provide.foundation.logger.base import FoundationLogger


# Context variable for trace_id (applications can set this for request tracing)
_FOUNDATION_CONTEXT_TRACE_ID = contextvars.ContextVar(
    "foundation_context_trace_id", default=None
)


@contextmanager
def timed_block(
    logger_instance: "FoundationLogger",
    event_name: str,
    layer_keys: dict[str, Any] | None = None,
    initial_kvs: dict[str, Any] | None = None,
    **extra_kvs: Any,
) -> Generator[dict[str, Any], None, None]:
    """
    Context manager that logs the duration of a code block.

    Logs at DEBUG when entering, INFO on success, ERROR on exception.

    Args:
        logger_instance: Logger to use for output
        event_name: Name of the operation being timed
        layer_keys: Semantic layer keys (e.g., llm-specific keys)
        initial_kvs: Initial key-value pairs to include in logs
        **extra_kvs: Additional key-value pairs

    Yields:
        A mutable dict that can be updated with additional context

    Example:
        >>> with timed_block(logger, "database_query") as ctx:
        >>>     ctx["query"] = "SELECT * FROM users"
        >>>     result = db.query("SELECT * FROM users")
        >>>     ctx["rows"] = len(result)
    """
    # Combine all key-value pairs
    all_kvs = {}
    if layer_keys:
        all_kvs.update(layer_keys)
    if initial_kvs:
        all_kvs.update(initial_kvs)
    all_kvs.update(extra_kvs)

    # Try to get trace_id from context
    trace_id = _FOUNDATION_CONTEXT_TRACE_ID.get()
    if trace_id and "trace_id" not in all_kvs:
        all_kvs["trace_id"] = trace_id

    # Create context dict that can be modified
    context: dict[str, Any] = {}

    # Log start
    logger_instance.debug(f"{event_name} started", **all_kvs)

    start_time = time.perf_counter()
    try:
        yield context

        # Success - calculate duration and log
        duration = time.perf_counter() - start_time
        all_kvs.update(context)
        all_kvs["duration_seconds"] = round(duration, 3)
        all_kvs["outcome"] = "success"

        logger_instance.info(f"{event_name} completed", **all_kvs)

    except Exception as e:
        # Error - calculate duration and log with exception
        duration = time.perf_counter() - start_time
        all_kvs.update(context)
        all_kvs["duration_seconds"] = round(duration, 3)
        all_kvs["outcome"] = "error"
        all_kvs["error.message"] = str(e)
        all_kvs["error.type"] = type(e).__name__

        logger_instance.error(f"{event_name} failed", exc_info=True, **all_kvs)
        raise
EOF

log_update "Updating: tests/utils/test_utils_coverage.py"
mkdir -p tests/utils/
cat <<'EOF' > tests/utils/test_utils_coverage.py
"""
Additional tests for provide.foundation.utils to increase code coverage.
"""
import io
from attrs import define, field, fields
import pytest

from provide.foundation import logger, TelemetryConfig, setup_telemetry, LoggingConfig
from provide.foundation.utils import timed_block
from provide.foundation.utils.formatting import format_table, to_camel_case
from provide.foundation.utils.parsing import auto_parse, parse_typed_value


class TestCaseConversionCoverage:
    """Coverage for case conversion functions."""

    def test_to_camel_case_empty_string(self) -> None:
        """Test to_camel_case with an empty string."""
        assert to_camel_case("") == ""


class TestTableFormattingCoverage:
    """Coverage for table formatting edge cases."""

    def test_format_table_empty_rows(self) -> None:
        """Test format_table with headers but no rows."""
        headers = ["Header 1", "Header 2"]
        rows = []
        table = format_table(headers, rows)
        assert "Header 1" in table
        assert "Header 2" in table
        assert len(table.splitlines()) == 2  # Header and separator line

    def test_format_table_ragged_rows(self) -> None:
        """Test format_table with rows of different lengths."""
        headers = ["A", "B", "C"]
        rows = [["1", "2"], ["4", "5", "6"]]
        table = format_table(headers, rows)
        # Should not raise an error and should format correctly
        assert "1" in table
        assert "2" in table
        assert "6" in table

    def test_format_table_alignment_mismatch(self) -> None:
        """Test format_table with more alignment options than headers."""
        headers = ["A", "B"]
        rows = [["1", "2"]]
        table = format_table(headers, rows, alignment=["l", "c", "r"])
        assert "1" in table
        assert "2" in table

    def test_format_table_no_headers_or_rows(self) -> None:
        """Test format_table with no headers and no rows."""
        assert format_table([], []) == ""


class TestParsingCoverage:
    """Coverage for parsing utility functions."""

    def test_parse_typed_value_unsupported_origin(self) -> None:
        """Test parse_typed_value with a type origin it doesn't handle."""
        # It should fall back to returning the original string value.
        result = parse_typed_value("some_value", set)
        assert result == "some_value"

    def test_auto_parse_with_string_type_hints(self) -> None:
        """Test auto_parse for attrs fields with string type hints."""
        @define
        class DummyConfig:
            int_val: 'int'
            bool_val: 'bool'
            list_val: 'list'
            dict_val: 'dict'
            unknown_val: 'SomeUnknownType'

        attrs_fields = {f.name: f for f in fields(DummyConfig)}

        assert auto_parse(attrs_fields['int_val'], "42") == 42
        assert auto_parse(attrs_fields['bool_val'], "true") is True
        assert auto_parse(attrs_fields['list_val'], "a,b") == ["a", "b"]
        assert auto_parse(attrs_fields['dict_val'], "k=v") == {"k": "v"}
        assert auto_parse(attrs_fields['unknown_val'], "some_string") == "some_string"

    def test_auto_parse_no_type_hint(self) -> None:
        """Test auto_parse for an attrs field with no type hint."""
        @define
        class NoTypeHintConfig:
            val: Any = field()

        no_type_field = fields(NoTypeHintConfig).val
        assert auto_parse(no_type_field, "a_string") == "a_string"


class TestTimingCoverage:
    """Coverage for timing utility functions."""

    def test_timed_block_context_modification(self, captured_stderr_for_foundation: io.StringIO) -> None:
        """Test that modifying the context dict within a timed_block works."""
        setup_telemetry(TelemetryConfig())

        with timed_block(logger, "test_op") as ctx:
            ctx["records"] = 100
            ctx["status_custom"] = "success" # Use a non-special key

        output = captured_stderr_for_foundation.getvalue()
        assert "records=100" in output
        assert "status_custom=success" in output
        assert "outcome=success" in output

    def test_timed_block_debug_message(self, captured_stderr_for_foundation: io.StringIO) -> None:
        """Test that the initial debug message is logged when level is DEBUG."""
        setup_telemetry(TelemetryConfig(logging=LoggingConfig(default_level="DEBUG")))

        with timed_block(logger, "debug_test_op"):
            pass

        output = captured_stderr_for_foundation.getvalue()
        # Check for both the "started" and "completed" messages
        assert "debug_test_op started" in output
        assert "debug_test_op completed" in output
EOF

log_success "Project update complete."