#
# core.py
#
"""
Foundation Telemetry Core Initialization and Configuration.
Handles setup, global state, processor chain assembly (including emoji set resolution),
and shutdown for the telemetry system.
"""

import io
import logging as stdlib_logging
import os
from pathlib import Path
import sys
import threading
from typing import Any, TextIO, cast

import structlog
from structlog.types import BindableLogger

from provide.foundation.logger import base as foundation_logger
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)
from provide.foundation.logger.emoji.sets import (
    BUILTIN_EMOJI_SETS,
    LEGACY_DAS_EMOJI_SETS,
)
from provide.foundation.logger.emoji.types import (
    CustomDasEmojiSet,
    EmojiSetConfig,
    FieldToEmojiMapping,
)
from provide.foundation.logger.processors import (
    _build_core_processors_list,
    _build_formatter_processors_list,
)
from provide.foundation.utils.streams import get_safe_stderr

_PROVIDE_SETUP_LOCK = threading.Lock()
_PROVIDE_LOG_STREAM: TextIO = sys.stderr
_LOG_FILE_HANDLE: TextIO | None = None
_CORE_SETUP_LOGGER_NAME = "provide.foundation.core_setup"
_EXPLICIT_SETUP_DONE = False


# Moved to utils.streams to avoid duplication with logger/base.py


def _set_log_stream_for_testing(stream: TextIO | None) -> None:
    global _PROVIDE_LOG_STREAM
    _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr


def _ensure_stderr_default() -> None:
    global _PROVIDE_LOG_STREAM
    if _PROVIDE_LOG_STREAM is sys.stdout:
        _PROVIDE_LOG_STREAM = sys.stderr


def _create_core_setup_logger(globally_disabled: bool = False) -> stdlib_logging.Logger:
    logger = stdlib_logging.getLogger(_CORE_SETUP_LOGGER_NAME)
    for h in list(logger.handlers):
        logger.removeHandler(h)
        try:
            if isinstance(h, stdlib_logging.StreamHandler) and h.stream not in (
                sys.stdout,
                sys.stderr,
                _PROVIDE_LOG_STREAM,
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
            os.getenv("PROVIDE_CORE_SETUP_LOG_LEVEL", "DEBUG").upper(),
            stdlib_logging.DEBUG,
        )
    )
    logger.propagate = False
    return logger


_core_setup_logger = _create_core_setup_logger()

ResolvedEmojiConfig = tuple[list[FieldToEmojiMapping], dict[str, CustomDasEmojiSet]]


def _resolve_active_emoji_config(
    logging_config: LoggingConfig, builtin_emoji_registry: dict[str, EmojiSetConfig]
) -> ResolvedEmojiConfig:
    resolved_fields_dict: dict[str, FieldToEmojiMapping] = {}
    resolved_emoji_sets_dict: dict[str, CustomDasEmojiSet] = {
        s.name: s for s in LEGACY_DAS_EMOJI_SETS
    }

    emoji_sets_to_process: list[EmojiSetConfig] = [
        builtin_emoji_registry[name]
        for name in logging_config.enabled_emoji_sets
        if name in builtin_emoji_registry
    ]
    emoji_sets_to_process.extend(logging_config.custom_emoji_sets)
    emoji_sets_to_process.sort(key=lambda emoji_set: emoji_set.priority)

    ordered_log_keys: list[str] = []
    seen_log_keys: set[str] = set()

    for emoji_set_config in emoji_sets_to_process:
        for emoji_set in emoji_set_config.emoji_sets:
            resolved_emoji_sets_dict[emoji_set.name] = emoji_set
        for field_def in emoji_set_config.field_definitions:
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
    config: TelemetryConfig, resolved_emoji_config: ResolvedEmojiConfig
) -> list[Any]:
    core_processors = _build_core_processors_list(config, resolved_emoji_config)
    formatter_processors = _build_formatter_processors_list(
        config.logging, _PROVIDE_LOG_STREAM
    )
    _core_setup_logger.debug(
        f"📝➡️🎨 Configured {config.logging.console_formatter} renderer."
    )
    return cast(list[Any], core_processors + formatter_processors)


def _apply_structlog_configuration(processors: list[Any]) -> None:
    stream_name = (
        "sys.stderr"
        if sys.stderr == _PROVIDE_LOG_STREAM
        else "custom stream (testing)"
    )
    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM),
        wrapper_class=cast(type[BindableLogger], structlog.BoundLogger),
        cache_logger_on_first_use=True,
    )
    _core_setup_logger.debug(
        f"📝➡️✅ structlog configured. Wrapper: BoundLogger. Output: {stream_name}."
    )


def _configure_structlog_output(
    config: TelemetryConfig, resolved_emoji_config: ResolvedEmojiConfig
) -> None:
    processors = _build_complete_processor_chain(config, resolved_emoji_config)
    _apply_structlog_configuration(processors)


def _handle_globally_disabled_setup() -> None:
    _core_setup_logger.debug("⚙️➡️🚫 Foundation Telemetry globally disabled.")
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def _reset_foundation_state() -> None:
    """
    Internal function to reset `structlog` and Foundation Telemetry's state.
    """
    global \
        _PROVIDE_LOG_STREAM, \
        _core_setup_logger, \
        _EXPLICIT_SETUP_DONE, \
        _LOG_FILE_HANDLE
    with _PROVIDE_SETUP_LOCK:
        structlog.reset_defaults()
        if _LOG_FILE_HANDLE:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception:
                pass
            _LOG_FILE_HANDLE = None
        foundation_logger.logger._is_configured_by_setup = False
        foundation_logger.logger._active_config = None
        foundation_logger.logger._active_resolved_emoji_config = None
        foundation_logger._LAZY_SETUP_STATE.update(
            {"done": False, "error": None, "in_progress": False}
        )
        _PROVIDE_LOG_STREAM = sys.stderr
        _EXPLICIT_SETUP_DONE = False
        _core_setup_logger = _create_core_setup_logger()


def reset_foundation_setup_for_testing() -> None:
    """
    Public test utility to reset Foundation Telemetry's internal state.
    """
    _reset_foundation_state()


def _internal_setup(
    config: TelemetryConfig | None = None, is_explicit_call: bool = False
) -> None:
    """
    The single, internal setup function that both explicit and lazy setup call.
    It is protected by the _PROVIDE_SETUP_LOCK in its callers.
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
        _core_setup_logger.debug("⚙️➡️🚀 Starting Foundation (structlog) setup...")

    resolved_emoji_config = _resolve_active_emoji_config(
        current_config.logging, BUILTIN_EMOJI_SETS
    )

    if current_config.globally_disabled:
        _handle_globally_disabled_setup()
    else:
        _configure_structlog_output(current_config, resolved_emoji_config)

    foundation_logger.logger._is_configured_by_setup = is_explicit_call
    foundation_logger.logger._active_config = current_config
    foundation_logger.logger._active_resolved_emoji_config = resolved_emoji_config
    foundation_logger._LAZY_SETUP_STATE["done"] = True

    if not current_config.globally_disabled:
        _core_setup_logger.debug("⚙️➡️✅ Foundation (structlog) setup completed.")


def setup_telemetry(config: TelemetryConfig | None = None) -> None:
    """
    Initializes or reconfigures the Foundation Telemetry system.
    """
    global _EXPLICIT_SETUP_DONE, _LOG_FILE_HANDLE, _PROVIDE_LOG_STREAM
    with _PROVIDE_SETUP_LOCK:
        current_config = config if config is not None else TelemetryConfig.from_env()

        if _LOG_FILE_HANDLE and _LOG_FILE_HANDLE is not _PROVIDE_LOG_STREAM:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception:
                pass
            _LOG_FILE_HANDLE = None

        log_file_path = getattr(current_config.logging, "log_file", None)

        is_test_stream = _PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            _PROVIDE_LOG_STREAM, io.TextIOWrapper
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                _LOG_FILE_HANDLE = open(
                    log_file_path, "a", encoding="utf-8", buffering=1
                )
                _PROVIDE_LOG_STREAM = _LOG_FILE_HANDLE
            except Exception as e:
                _core_setup_logger.error(
                    f"Failed to open log file {log_file_path}: {e}"
                )
                _PROVIDE_LOG_STREAM = get_safe_stderr()
        elif not is_test_stream:
            _PROVIDE_LOG_STREAM = get_safe_stderr()

        _internal_setup(current_config, is_explicit_call=True)
        _EXPLICIT_SETUP_DONE = True


async def shutdown_foundation_telemetry(timeout_millis: int = 5000) -> None:
    """
    Gracefully flushes any buffered telemetry, especially for file logging.
    This does NOT perform a full reset, allowing test runners to clean up streams.
    """
    global _LOG_FILE_HANDLE
    _core_setup_logger.debug("🔌➡️🏁 Foundation Telemetry flush called.")
    with _PROVIDE_SETUP_LOCK:
        if _LOG_FILE_HANDLE:
            try:
                # Only flush the handle, do not close or reset state.
                # The test fixture's reset will handle the final close.
                _LOG_FILE_HANDLE.flush()
            except Exception as e:
                _core_setup_logger.error(f"Failed to flush log file handle: {e}")
