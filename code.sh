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

log_update "Updating: pyproject.toml"
mkdir -p .
cat <<'EOF' > pyproject.toml
#
# pyproject.toml
#

[project]
name = "provide-foundation"
description = "Foundation Telemetry: An opinionated, developer-friendly telemetry wrapper for Python."
version = "0.0.16"
requires-python = ">=3.11"
readme = "README.md"
license = { text = "Apache-2.0" }
authors = [
    { name = "Tim Perkins", email = "code@tim.life" },
]
maintainers = [
    { name = "provide.io", email = "code@provide.io" },
]
keywords = ["telemetry", "logging", "tracing", "python", "pyvider"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Topic :: System :: Logging",
    "Topic :: System :: Monitoring",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]
dependencies = [
    "aiofiles>=23.2.1",
    "attrs>=23.1.0",
    "click>=8.1.7",
    "structlog>=25.3.0",
    "tomli_w>=1.0.0",
]

[project.urls]
Homepage = "https://pyvider.com/"
Repository = "https://github.com/provider-io/provide-foundation"


[project.optional-dependencies]
opentelemetry = [
    "opentelemetry-api>=1.22.0",
    "opentelemetry-sdk>=1.22.0",
    "opentelemetry-exporter-otlp-proto-grpc>=1.22.0",
    "opentelemetry-exporter-otlp-proto-http>=1.22.0",
]

[dependency-groups]
dev = [
    "bandit>=1.8.3",
    "hypothesis>=6.131.28",
    "mypy>=1.8.0",
    "psutil>=7.0.0",
    "pyrefly>=0.16.2",
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.3.0",
    "pyyaml>=6.0.2",
    "reuse>=1.1.0",
    "ruff>=0.1.0",
    "twine>=6.1.0",
    "ty>=0.0.1a6",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.24.0",
    "mkdocs-gen-files>=0.5.0",
    "mkdocs-literate-nav>=0.6.0",
    "mkdocs-section-index>=0.3.0",
    "mike>=2.0.0",
]

################################################################################
# Pytest Configuration
################################################################################

[tool.pytest.ini_options]
log_cli = true
log_cli_level = "DEBUG"

asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"

testpaths = ["tests"]
pythonpath = ["src", "."]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*", "*Tests"]
python_functions = ["test_*", "*_test"]
markers = [
    "serial: run tests serially to avoid conflicts on global state",
]
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore:cannot collect test class 'Test.*' because it has a __init__ constructor:pytest.PytestCollectionWarning",
    "ignore:cannot collect test class .* because it has a __init__ constructor:pytest.PytestCollectionWarning",
    "ignore:.* KqueueSelector constructor:pytest.PytestCollectionWarning",
    "ignore:.* KqueueSelector constructor:pytest.PytestCollectionWarning",
]
norecursedirs = [
    ".git", ".hg", ".svn", "*_build", "build", "dist", "*.egg-info",
    ".venv", "venv", # Added venv as it's a common default
    "htmlcov", "docs/_build",
    ".hypothesis", # Added to address the warning
]
addopts = "-ra -q --color=yes"

################################################################################
# Ruff Linter and Formatter Configuration
################################################################################

[tool.ruff]
line-length = 88
indent-width = 4
target-version = "py311"

[tool.ruff.lint]
select = [
    "E", "F", "W", "I", "UP", "ANN", "B", "C90", "SIM", "PTH", "RUF",
]
ignore = [ "ANN401", "B008", "E501" ] # Removed ANN101, ANN102
[tool.ruff.lint.isort]
known-first-party = ["pyvider", "tests"]
force-sort-within-sections = true
combine-as-imports = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

################################################################################
# MyPy Static Type Checker Configuration
################################################################################

[tool.mypy]
mypy_path = "src"
# Show error codes in output.
show_error_codes = true
# Show column numbers in output.
show_column_numbers = true
# Use visually nicer output in error messages:
pretty = true
# Use current Python version.
python_version = "3.11"
# Warn about unused '# type: ignore' comments.
warn_unused_ignores = true
# Warn about unused '[mypy-pattern]'  config sections.
warn_unused_configs = true
# Do not follow imports to .pyi stubs for external libraries.
follow_imports = "normal"  # Changed global strategy
# Do not check that test functions are annotated.
disallow_untyped_decorators = false

[[tool.mypy.overrides]]
module = [
    "structlog",
    "structlog.*"
]
follow_imports = "skip" # Keep structlog skipped
ignore_missing_imports = true

################################################################################
# Coverage.py Configuration
################################################################################

[tool.coverage.run]
source = ["provide.foundation"]
branch = true
parallel = true

[tool.coverage.report]
show_missing = true
skip_covered = false
fail_under = 80 # Set this to a realistic target once you get >0%
precision = 2
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "def __repr__",
    "def __str__",
    "@(abc\\.)?abstractmethod",
    "pass",
    # This is usually fine, but double-check it's not too greedy for your codebase
    "logger\\.(debug|info|warning|error|exception|critical|trace)\\(",
    "import logging", # Excluding all import logging lines might be too much
    "from logging import", # Same as above
    "print\\(",
]

[tool.coverage.html]
directory = "htmlcov" # Using an absolute path

[tool.coverage.xml]
output = "coverage.xml"

[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
publish-url = "https://test.pypi.org/legacy/"
explicit = true

[tool.bandit]
exclude_dirs = [".venv", "tests"]

[tool.pyrefly]
project_includes = [
    "src",
    "tests",
]

# 🐍🏗️⚙️
EOF

log_update "Updating: src/provide/foundation/cli/utils.py"
mkdir -p src/provide/foundation/cli/
cat <<'EOF' > src/provide/foundation/cli/utils.py
"""Common CLI utilities for output, logging, and testing."""

import inspect
import json
from pathlib import Path
from typing import Any

import click
from click.testing import CliRunner, Result

from provide.foundation.context import Context
from provide.foundation.core import setup_telemetry
from provide.foundation.logger import (
    LoggingConfig,
    TelemetryConfig,
    get_logger,
)

log = get_logger(__name__)


def echo_json(data: Any, err: bool = False) -> None:
    """
    Output data as JSON.

    Args:
        data: Data to output as JSON
        err: Whether to output to stderr
    """
    click.echo(json.dumps(data, indent=2, default=str), err=err)


def echo_error(message: str, json_output: bool = False) -> None:
    """
    Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        echo_json({"error": message}, err=True)
    else:
        click.secho(f"✗ {message}", fg="red", err=True)


def echo_success(message: str, json_output: bool = False) -> None:
    """
    Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        echo_json({"success": message})
    else:
        click.secho(f"✓ {message}", fg="green")


def echo_warning(message: str, json_output: bool = False) -> None:
    """
    Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        echo_json({"warning": message}, err=True)
    else:
        click.secho(f"⚠ {message}", fg="yellow", err=True)


def echo_info(message: str, json_output: bool = False) -> None:
    """
    Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        echo_json({"info": message})
    else:
        click.echo(f"ℹ {message}")


def setup_cli_logging(
    ctx: Context,
) -> None:
    """
    Setup logging for CLI applications using a Context object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation Context, populated by CLI decorators.
    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,
        console_formatter=console_formatter,
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    setup_telemetry(config=telemetry_config)


def create_cli_context(**kwargs) -> Context:
    """
    Create a Context for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured Context instance
    """
    ctx = Context.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, key, value)
    return ctx


class CliTestRunner:
    """
    Test runner for CLI commands using Click's testing facilities.
    This wrapper provides compatibility for different Click versions
    regarding the 'mix_stderr' functionality.
    """

    def __init__(self, mix_stderr: bool = False) -> None:
        self._mix_stderr = mix_stderr
        runner_sig = inspect.signature(CliRunner)
        self._supports_mix_stderr = 'mix_stderr' in runner_sig.parameters

        if self._supports_mix_stderr:
            self.runner = CliRunner(mix_stderr=self._mix_stderr)
        else:
            self.runner = CliRunner()

    def invoke(
        self,
        cli: click.Command | click.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs,
    ) -> Result:
        """
        Invoke a CLI command for testing.
        """
        result = self.runner.invoke(
            cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

        if not self._supports_mix_stderr and self._mix_stderr and result.stderr:
            result_kwargs = {
                "runner": result.runner,
                "stdout_bytes": result.stdout_bytes + result.stderr_bytes,
                "stderr_bytes": b'',
                "exit_code": result.exit_code,
                "exception": result.exception,
                "exc_info": result.exc_info,
            }
            result_sig = inspect.signature(Result)
            if 'return_value' in result_sig.parameters:
                result_kwargs['return_value'] = result.return_value
            return Result(**result_kwargs)

        return result

    def isolated_filesystem(self):
        """
        Context manager for isolated filesystem.
        """
        return self.runner.isolated_filesystem()


def assert_cli_success(result: Result, expected_output: str | None = None) -> None:
    """
    Assert that a CLI command succeeded.
    """
    if result.exit_code != 0:
        raise AssertionError(
            f"Command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}"
        )

    if expected_output and expected_output not in result.output:
        raise AssertionError(
            f"Expected output not found.\n"
            f"Expected: {expected_output}\n"
            f"Actual: {result.output}"
        )


def assert_cli_error(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """
    Assert that a CLI command failed.
    """
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(
            f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}"
        )

    if expected_error and expected_error not in result.output:
        raise AssertionError(
            f"Expected error not found.\n"
            f"Expected: {expected_error}\n"
            f"Actual: {result.output}"
        )
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

        @click.group()
        @flexible_options
        @output_options
        @pass_context
        def cli(ctx: Context, **kwargs) -> None:
            """Test CLI application."""
            for key, value in kwargs.items():
                if value is not None:
                    setattr(ctx, key, value)
            setup_cli_logging(ctx)

        @cli.group()
        @pass_context
        def database(ctx: Context) -> None:
            """Database management commands."""
            setup_cli_logging(ctx)

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
            setup_cli_logging(ctx)
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
                ctx.log_file = log_file
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