#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Configuration management CLI commands.

This module provides CLI commands for inspecting and managing Foundation
configuration schemas."""

from __future__ import annotations

from provide.foundation.cli.deps import _HAS_CLICK, click

if _HAS_CLICK:
    from provide.foundation.cli.helpers import requires_click
    from provide.foundation.cli.shutdown import with_cleanup
    from provide.foundation.console.output import perr, pout
    from provide.foundation.process import exit_error

    @click.group("config", help="Configuration management commands")
    def config_group() -> None:
        """Configuration management commands."""
        pass

    @config_group.command("schema")
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["human", "json", "yaml", "markdown"]),
        default="human",
        help="Output format for schema",
    )
    @click.option(
        "--category",
        "-c",
        help="Filter by category (e.g., logger, transport)",
    )
    @click.option(
        "--env-only",
        is_flag=True,
        help="Show only environment variables",
    )
    @click.option(
        "--show-sensitive",
        is_flag=True,
        help="Include sensitive fields (masked by default)",
    )
    @click.option(
        "--output",
        "-o",
        type=click.Path(),
        help="Output to file instead of stdout",
    )
    @requires_click
    @with_cleanup
    def schema_command(
        format: str,
        category: str | None,
        env_only: bool,
        show_sensitive: bool,
        output: str | None,
    ) -> None:
        """Display all available configuration options and their schemas.

        This command introspects all registered configuration classes and displays
        their schemas, including environment variable mappings, types, defaults,
        and descriptions.

        Examples:

            # Display all configuration in human-readable format
            foundation config schema

            # Show only environment variables in JSON format
            foundation config schema --env-only --format json

            # Filter by category and output to file
            foundation config schema --category logger --output config.md --format markdown

            # Include sensitive fields (they will be masked)
            foundation config schema --show-sensitive

        """
        try:
            # Import here to avoid circular dependencies
            from provide.foundation.config.discovery import get_consolidated_schema
            from provide.foundation.config.formatters import get_formatter

            # Get consolidated schema
            schema = get_consolidated_schema()

            # Check if any schemas found
            if not schema.schemas:
                perr("No configuration schemas found. Ensure Foundation is initialized.")
                exit_error("No schemas available", code=1)

            # Get formatter
            try:
                formatter = get_formatter(format)
            except ValueError as e:
                perr(f"Invalid format: {e}")
                exit_error("Invalid format", code=1)

            # Format output
            result = formatter.format(
                schema,
                env_only=env_only,
                show_sensitive=show_sensitive,
                category=category,
            )

            # Output result
            if output:
                from pathlib import Path

                try:
                    Path(output).write_text(result)
                    pout(f"Schema written to {output}")
                except OSError as e:
                    perr(f"Failed to write to file: {e}")
                    exit_error("File write failed", code=1)
            else:
                pout(result)

        except Exception as e:
            perr(f"Failed to generate schema: {e}")
            exit_error("Schema generation failed", code=1)

    __all__ = ["config_group", "schema_command"]

else:
    # Stub when click is not available
    def config_group(*args: object, **kwargs: object) -> None:
        raise ImportError(
            "CLI commands require optional dependencies. Install with: pip install 'provide-foundation[cli]'"
        )

    __all__ = []

# 🧱🏗️🔚
