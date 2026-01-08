#!/usr/bin/env python3
"""
Side-by-side comparison: Click vs Typer with provide.foundation

This file demonstrates the same CLI application implemented with both Click and Typer.
Run with: python cli_comparison_example.py [click|typer] process --count 100
"""

from __future__ import annotations

import sys
from typing import Annotated

from attrs import define

from provide.foundation import logger
from provide.foundation.config import env_field
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.console.output import pout
from provide.foundation.hub import get_hub

# Check which frameworks are available
try:
    import click

    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False

try:
    import typer

    HAS_TYPER = True
except ImportError:
    HAS_TYPER = False


# ============================================================================
# Shared Configuration (Used by Both)
# ============================================================================


@define
class AppConfig(RuntimeConfig):
    """Application configuration."""

    app_name: str = env_field(env_var="APP_NAME", default="demo-app")
    default_workers: int = env_field(env_var="WORKERS", default=4)
    debug: bool = env_field(env_var="DEBUG", default=False)
    log_level: str = env_field(env_var="LOG_LEVEL", default="INFO")


# ============================================================================
# Business Logic (Framework-Agnostic)
# ============================================================================


def process_tasks(count: int, workers: int, config: AppConfig) -> None:
    """Process tasks - business logic independent of CLI framework."""
    logger.info(
        "Starting task processing",
        count=count,
        workers=workers,
        app_name=config.app_name,
    )

    pout(f"🚀 Processing {count} tasks")
    pout(f"   Workers: {workers}")
    pout(f"   App: {config.app_name}")
    pout(f"   Debug: {config.debug}")

    # Simulate work
    for i in range(min(count, 5)):  # Just show first 5
        logger.debug("Processing task", task_id=i)
        pout(f"   ✓ Task {i + 1}/{count}")

    if count > 5:
        pout(f"   ... ({count - 5} more tasks)")

    logger.info("Task processing complete", count=count)
    pout("\n✅ Done!")


def show_config(config: AppConfig) -> None:
    """Show configuration - framework-agnostic."""
    logger.info("Displaying configuration")

    pout("📋 Current Configuration")
    pout("=" * 50)
    pout(f"  App Name: {config.app_name}")
    pout(f"  Workers: {config.default_workers}")
    pout(f"  Debug: {config.debug}")
    pout(f"  Log Level: {config.log_level}")
    pout("=" * 50)


# ============================================================================
# CLICK IMPLEMENTATION
# ============================================================================

if HAS_CLICK:

    @click.group()
    @click.pass_context
    def click_cli(ctx: click.Context) -> None:
        """Demo application using Click.

        This demonstrates provide.foundation with Click CLI framework.
        """
        # Initialize foundation
        hub = get_hub()
        hub.initialize_foundation()

        # Load configuration
        config = AppConfig.from_env()

        # Store in context for subcommands
        ctx.obj = {"config": config}

        logger.debug("Click CLI initialized", app_name=config.app_name)

    @click_cli.command(name="process")
    @click.option("--count", default=100, type=int, help="Number of tasks to process")
    @click.option("--workers", type=int, help="Number of workers (overrides config)")
    @click.pass_context
    def click_process(ctx: click.Context, count: int, workers: int | None) -> None:
        """Process tasks with Click."""
        config: AppConfig = ctx.obj["config"]
        actual_workers = workers if workers is not None else config.default_workers

        process_tasks(count, actual_workers, config)

    @click_cli.command(name="config")
    @click.pass_context
    def click_config(ctx: click.Context) -> None:
        """Show current configuration with Click."""
        config: AppConfig = ctx.obj["config"]
        show_config(config)

    @click_cli.command(name="status")
    @click.option("--format", type=click.Choice(["text", "json"]), default="text")
    @click.pass_context
    def click_status(ctx: click.Context, format: str) -> None:
        """Show application status with Click."""
        config: AppConfig = ctx.obj["config"]

        if format == "json":
            import json

            pout(
                json.dumps(
                    {
                        "app": config.app_name,
                        "workers": config.default_workers,
                        "debug": config.debug,
                    },
                    indent=2,
                )
            )
        else:
            pout("Status: Running")
            pout(f"App: {config.app_name}")
            pout(f"Workers: {config.default_workers}")


# ============================================================================
# TYPER IMPLEMENTATION
# ============================================================================

if HAS_TYPER:
    typer_app = typer.Typer(
        help="Demo application using Typer. This demonstrates provide.foundation with Typer CLI framework."
    )

    # Dependency injection for config
    def get_config() -> AppConfig:
        """Get configuration as a dependency."""
        hub = get_hub()
        hub.initialize_foundation()
        config = AppConfig.from_env()
        logger.debug("Typer CLI initialized", app_name=config.app_name)
        return config

    @typer_app.command(name="process")
    def typer_process(
        count: Annotated[int, typer.Option(help="Number of tasks to process")] = 100,
        workers: Annotated[int | None, typer.Option(help="Number of workers (overrides config)")] = None,
        config: Annotated[AppConfig, typer.Depends(get_config)] = None,
    ) -> None:
        """Process tasks with Typer."""
        actual_workers = workers if workers is not None else config.default_workers
        process_tasks(count, actual_workers, config)

    @typer_app.command(name="config")
    def typer_config(
        config: Annotated[AppConfig, typer.Depends(get_config)] = None,
    ) -> None:
        """Show current configuration with Typer."""
        show_config(config)

    @typer_app.command(name="status")
    def typer_status(
        format: Annotated[str, typer.Option(help="Output format")] = "text",
        config: Annotated[AppConfig, typer.Depends(get_config)] = None,
    ) -> None:
        """Show application status with Typer."""
        if format == "json":
            import json

            typer.echo(
                json.dumps(
                    {
                        "app": config.app_name,
                        "workers": config.default_workers,
                        "debug": config.debug,
                    },
                    indent=2,
                )
            )
        else:
            typer.echo("Status: Running")
            typer.echo(f"App: {config.app_name}")
            typer.echo(f"Workers: {config.default_workers}")


# ============================================================================
# COMPARISON DEMO
# ============================================================================


def show_comparison() -> None:
    """Show side-by-side comparison."""
    pout("=" * 70)
    pout("🔍 Click vs Typer Comparison for provide.foundation")
    pout("=" * 70)
    pout("")

    pout("Available Frameworks:")
    pout(f"  Click: {'✅ Available' if HAS_CLICK else '❌ Not installed'}")
    pout(f"  Typer: {'✅ Available' if HAS_TYPER else '❌ Not installed'}")
    pout("")

    if HAS_CLICK:
        pout("Click Example:")
        pout("  python cli_comparison_example.py click process --count 100 --workers 8")
        pout("  python cli_comparison_example.py click config")
        pout("  python cli_comparison_example.py click status --format json")
        pout("")

    if HAS_TYPER:
        pout("Typer Example:")
        pout("  python cli_comparison_example.py typer process --count 100 --workers 8")
        pout("  python cli_comparison_example.py typer config")
        pout("  python cli_comparison_example.py typer status --format json")
        pout("")

    pout("Key Differences:")
    pout("")
    pout("📋 Click (Explicit & Stable):")
    pout("  + Industry standard, battle-tested")
    pout("  + Explicit context passing")
    pout("  + Full control over parsing")
    pout("  - More boilerplate decorators")
    pout("  - Types not inferred from hints")
    pout("")
    pout("🎯 Typer (Modern & Ergonomic):")
    pout("  + Less boilerplate code")
    pout("  + Types from hints automatically")
    pout("  + Dependency injection")
    pout("  - More magic/implicit behavior")
    pout("  - Additional dependencies")
    pout("")

    pout("Code Comparison (lines for same functionality):")
    pout("  Click:  ~25 lines of code")
    pout("  Typer:  ~18 lines of code (-28%)")
    pout("")

    pout("For provide.foundation:")
    pout("  ✅ Click is the right choice (stability for foundation lib)")
    pout("  ✅ Applications can use either (both work great)")
    pout("")
    pout("=" * 70)


# ============================================================================
# MAIN
# ============================================================================


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_comparison()
        sys.exit(0)

    framework = sys.argv[1].lower()

    if framework == "click":
        if not HAS_CLICK:
            pout("❌ Click not installed. Install with: pip install click")
            sys.exit(1)
        # Remove 'click' from argv so Click sees normal args
        sys.argv.pop(1)
        click_cli()

    elif framework == "typer":
        if not HAS_TYPER:
            pout("❌ Typer not installed. Install with: pip install typer")
            sys.exit(1)
        # Remove 'typer' from argv so Typer sees normal args
        sys.argv.pop(1)
        typer_app()

    else:
        pout(f"❌ Unknown framework: {framework}")
        pout("   Use: click or typer")
        pout("")
        show_comparison()
        sys.exit(1)
