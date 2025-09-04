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
        
        # Close existing file handle if it exists
        if _LOG_FILE_HANDLE:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception:
                pass
            _LOG_FILE_HANDLE = None

        log_file_path = getattr(current_config.logging, 'log_file', None)
        
        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                _LOG_FILE_HANDLE = open(log_file_path, "a", encoding="utf-8")
                _FOUNDATION_LOG_STREAM = _LOG_FILE_HANDLE
            except Exception as e:
                _core_setup_logger.error(f"Failed to open log file {log_file_path}: {e}")
                _FOUNDATION_LOG_STREAM = _get_safe_stderr()
        else:
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

log_update "Updating: src/provide/foundation/logger/config.py"
mkdir -p src/provide/foundation/logger/
cat <<'EOF' > src/provide/foundation/logger/config.py
#
# config.py
#
"""
Foundation Telemetry Configuration Module.
Defines data models for telemetry and logging settings.
"""
from pathlib import Path
from attrs import define, field

from provide.foundation.types import (
    ConsoleFormatterStr,
    CustomDasEmojiSet,
    LogLevelStr,
    SemanticLayer,
)


@define(frozen=True, slots=True)
class LoggingConfig:
    """Configuration specific to logging behavior within Foundation Telemetry."""

    default_level: LogLevelStr = field(default="DEBUG")
    module_levels: dict[str, LogLevelStr] = field(factory=lambda: {})
    console_formatter: ConsoleFormatterStr = field(default="key_value")
    logger_name_emoji_prefix_enabled: bool = field(default=True)
    das_emoji_prefix_enabled: bool = field(default=True)
    omit_timestamp: bool = field(default=False)
    enabled_semantic_layers: list[str] = field(factory=lambda: [])
    custom_semantic_layers: list[SemanticLayer] = field(factory=lambda: [])
    user_defined_emoji_sets: list[CustomDasEmojiSet] = field(factory=lambda: [])
    log_file: Path | None = field(default=None)


@define(frozen=True, slots=True)
class TelemetryConfig:
    """Main configuration object for the Foundation Telemetry system."""

    service_name: str | None = field(default=None)
    logging: LoggingConfig = field(factory=LoggingConfig)
    globally_disabled: bool = field(default=False)

    @classmethod
    def from_env(cls) -> "TelemetryConfig":
        """Creates a `TelemetryConfig` instance by parsing relevant environment variables."""
        from provide.foundation.logger.env import from_env as _from_env

        return _from_env()
EOF

log_update "Updating: tests/cli/test_cli_integration.py"
mkdir -p tests/cli/
cat <<'EOF' > tests/cli/test_cli_integration.py
"""Integration tests for CLI functionality."""

import json
from pathlib import Path
import tempfile
import io

import click
import pytest

from provide.foundation.cli.decorators import (
    flexible_options,
    output_options,
    pass_context,
)
from provide.foundation.cli.utils import (
    setup_cli_logging,
    CliTestRunner,
)
from provide.foundation.context import Context
from provide.foundation.logger import get_logger


class TestCompleteCliIntegration:
    """Test complete CLI with all options working together."""

    def create_test_cli(self):
        """Create a test CLI with all features."""

        @click.group(invoke_without_command=True)
        @flexible_options
        @output_options
        @pass_context
        def cli(ctx: Context, **kwargs) -> None:
            """Test CLI application."""
            for key, value in kwargs.items():
                if value is not None:
                    setattr(ctx, key, value)
            # Configure logging once at the top level.
            setup_cli_logging(ctx)
            if ctx.invoked_subcommand is None:
                logger = get_logger(__name__)
                logger.info("CLI root command executed.")


        @cli.group()
        @pass_context
        def database(ctx: Context) -> None:
            """Database management commands."""
            # No need to re-configure logging, it's inherited via context.
            pass

        @database.command()
        @pass_context
        def migrate(ctx: Context) -> None:
            """Run database migrations."""
            logger = get_logger(__name__)
            logger.info("Running migrations")
            if ctx.json_output:
                click.echo(json.dumps({"status": "success", "migrations": 5}))
            else:
                click.echo("✅ Applied 5 migrations")

        @cli.command()
        @pass_context
        def status(ctx: Context) -> None:
            """Show application status."""
            # No need to re-configure logging.
            logger = get_logger(__name__)
            logger.debug("Checking status")
            if ctx.json_output:
                click.echo(json.dumps({"status": "healthy", "uptime": 3600}))
            else:
                if not ctx.no_emoji:
                    click.echo("🟢 Application is healthy")
                else:
                    click.echo("Application is healthy")

        return cli

    def test_options_at_group_level(self) -> None:
        """Test that options work at the group level."""
        cli = self.create_test_cli()
        runner = CliTestRunner()
        result = runner.invoke(cli, ["--log-level", "DEBUG", "--json", "status"])
        assert result.exit_code == 0
        output = json.loads(result.output.strip().split("\n")[-1])
        assert output["status"] == "healthy"

    def test_options_are_available_to_subcommand(self) -> None:
        """Test that options passed to the group are available to the subcommand."""
        cli = self.create_test_cli()
        runner = CliTestRunner()
        # Correct invocation: options for parent go BEFORE subcommand
        result = runner.invoke(cli, ["--no-emoji", "status"])
        assert result.exit_code == 0
        output = "\n".join([line for line in result.output.strip().split("\n") if not line.startswith('[Foundation Setup]')])
        assert "Application is healthy" in output
        assert "🟢" not in output

    def test_nested_groups_inherit_options(self) -> None:
        """Test that nested groups inherit options."""
        cli = self.create_test_cli()
        runner = CliTestRunner()
        result = runner.invoke(
            cli, ["--json", "--log-level", "WARNING", "database", "migrate"]
        )
        assert result.exit_code == 0
        output = json.loads(result.output.strip().split("\n")[-1])
        assert output["status"] == "success"

    def test_command_options_override_group_options(self) -> None:
        """Test that later options on the same command override earlier ones."""
        cli = self.create_test_cli()
        runner = CliTestRunner(mix_stderr=True)
        result = runner.invoke(
            cli, ["--log-level", "INFO", "--log-level", "DEBUG", "status"]
        )
        assert result.exit_code == 0
        assert "Checking status" in result.output


class TestLoggingIntegration:
    """Test that logging options actually affect logging behavior."""

    def test_log_level_affects_output(self, captured_stderr_for_foundation: io.StringIO) -> None:
        @click.command()
        @flexible_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            setup_cli_logging(ctx)
            logger = get_logger(__name__)
            logger.debug("Debug message")
            logger.info("Info message")
        runner = CliTestRunner()
        result = runner.invoke(cmd, ["--log-level", "INFO"])
        assert result.exit_code == 0
        output = captured_stderr_for_foundation.getvalue()
        assert "Debug message" not in output
        assert "Info message" in output

    def test_log_format_changes_output(self, captured_stderr_for_foundation: io.StringIO) -> None:
        @click.command()
        @flexible_options
        @output_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            setup_cli_logging(ctx)
            logger = get_logger(__name__)
            logger.info("Test message", extra_field="value")
        runner = CliTestRunner()
        result = runner.invoke(cmd, ["--log-level", "INFO", "--log-format", "json"])
        assert result.exit_code == 0
        output = captured_stderr_for_foundation.getvalue()
        app_logs = [line for line in output.splitlines() if not line.startswith('[Foundation Setup]')]
        log_data = json.loads(app_logs[-1])
        assert "Test message" in log_data["event"]
        assert log_data["extra_field"] == "value"

    def test_log_file_writes_to_file(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            log_file = Path(f.name)
        try:
            @click.command()
            @flexible_options
            @pass_context
            def cmd(ctx: Context, **kwargs) -> None:
                setup_cli_logging(ctx)
                logger = get_logger(__name__)
                logger.info("Message to file")
            runner = CliTestRunner()
            result = runner.invoke(cmd, ["--log-file", str(log_file), "--log-level", "INFO"])
            assert result.exit_code == 0
            content = log_file.read_text()
            assert "Message to file" in content
        finally:
            log_file.unlink(missing_ok=True)


class TestOutputFormatting:
    """Test output formatting options."""

    def test_json_output_format(self) -> None:
        @click.command()
        @output_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            if ctx.json_output:
                click.echo(json.dumps({"result": "success", "count": 42}))
            else:
                click.echo("Result: success (42 items)")
        runner = CliTestRunner()
        result = runner.invoke(cmd, ["--json"])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["result"] == "success"

    def test_no_color_option(self) -> None:
        @click.command()
        @output_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            click.secho("Colored text", fg="green", color=not ctx.no_color)
        runner = CliTestRunner()
        result = runner.invoke(cmd, ["--no-color"])
        assert result.exit_code == 0
        assert "\x1b" not in result.output

    def test_no_emoji_option(self) -> None:
        @click.command()
        @output_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            click.echo("✅ Success" if not ctx.no_emoji else "Success")
        runner = CliTestRunner()
        result = runner.invoke(cmd, ["--no-emoji"])
        assert result.exit_code == 0
        assert "✅" not in result.output


class TestConfigurationLoading:
    """Test configuration file and profile loading."""

    def test_config_file_loading(self) -> None:
        config_data = {"log_level": "WARNING", "profile": "testing"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            config_file = Path(f.name)
        try:
            @click.command()
            @flexible_options
            @pass_context
            def cmd(ctx: Context, **kwargs) -> None:
                click.echo(f"profile={ctx.profile}")
            runner = CliTestRunner()
            result = runner.invoke(cmd, ["--config", str(config_file)])
            assert result.exit_code == 0
            assert "profile=testing" in result.output
        finally:
            config_file.unlink(missing_ok=True)


class TestRealWorldScenarios:
    """Test real-world CLI usage scenarios."""

    def test_debugging_production_issue(self) -> None:
        @click.group()
        @flexible_options
        @output_options
        @pass_context
        def cli(ctx: Context, **kwargs) -> None:
            setup_cli_logging(ctx)
        @cli.command()
        @pass_context
        def diagnose(ctx: Context) -> None:
            if ctx.profile == "production":
                assert ctx.log_level == "DEBUG"
                assert ctx.json_output is True
                assert ctx.log_file is not None
            click.echo(json.dumps({"diagnosis": "complete"}))
        runner = CliTestRunner()
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
            log_file = Path(f.name)
        try:
            result = runner.invoke(
                cli,
                [
                    "--profile", "production",
                    "--log-level", "DEBUG",
                    "--json",
                    "--log-file", str(log_file),
                    "diagnose",
                ],
            )
            assert result.exit_code == 0
            output = json.loads(result.output.strip().split("\n")[-1])
            assert output["diagnosis"] == "complete"
        finally:
            log_file.unlink(missing_ok=True)

    def test_interactive_development(self) -> None:
        @click.command()
        @flexible_options
        @output_options
        @pass_context
        def develop(ctx: Context, **kwargs) -> None:
            setup_cli_logging(ctx)
            logger = get_logger(__name__)
            logger.debug("Debug information here")
            click.echo("🔧 Development mode active")
        runner = CliTestRunner(mix_stderr=True)
        result = runner.invoke(develop, ["--log-level", "DEBUG"])
        assert result.exit_code == 0
        assert "🔧 Development mode active" in result.output
        assert "Debug information here" in result.output
EOF

log_success "Project update complete."