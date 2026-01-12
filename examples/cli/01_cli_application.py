#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""CLI Application Example - Complete Hub and Command System

This comprehensive example demonstrates building a full CLI application
with provide.foundation's hub system:

1. Component System:
   - Regular Python classes with context manager support
   - Hub.add_component() method for registration
   - Multi-dimensional registry (resources, services, etc.)
   - Context managers for lifecycle management

2. Command Registration:
   - @register_command decorator for CLI commands
   - Command categories and aliases
   - Integration with Click framework
   - Automatic help generation

3. Hub Management:
   - Centralized component and command registry
   - Dynamic CLI creation from registered commands
   - Context passing between commands

4. Real-world Patterns:
   - Resource lifecycle (database, cache)
   - Service registration (logger)
   - Status reporting
   - Testing utilities

Usage:
    # Run as CLI application
    python examples/cli/01_cli_application.py --help
    python examples/cli/01_cli_application.py status
    python examples/cli/01_cli_application.py test-resources
    python examples/cli/01_cli_application.py list --dimension resource

    # Or import and use programmatically
    from examples.cli.01_cli_application import Hub, DatabaseResource
    hub = Hub()
    hub.add_component(DatabaseResource, name="database", dimension="resource")
    db_class = hub.get_component("database", dimension="resource")
    with db_class("mydb") as db:
        result = db.query("SELECT * FROM users")

Expected output:
    Interactive CLI with multiple commands demonstrating component lifecycle,
    registry management, and command execution.

See Also:
    - examples/03_named_loggers.py for logger component patterns
    - examples/10_production_patterns.py for production CLI patterns

"""

from __future__ import annotations

from provide.foundation.cli import echo_info, echo_success, echo_warning
from provide.foundation.context import CLIContext
from provide.foundation.hub import Hub, register_command

# ==============================================================================
# COMPONENTS
# ==============================================================================


class DatabaseResource:
    """Database connection resource with lifecycle management."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.connected = False

    def __enter__(self) -> DatabaseResource:
        """Context manager entry."""
        echo_info(f"Connecting to database: {self.name}")
        self.connected = True
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        if self.connected:
            echo_info(f"Disconnecting from database: {self.name}")
            self.connected = False

    def query(self, sql: str) -> str:
        """Execute a query."""
        if not self.connected:
            raise RuntimeError("Not connected to database")
        return f"Query result for: {sql}"


class CacheResource:
    """Cache resource for fast data access."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.cache = {}

    def __enter__(self) -> CacheResource:
        """Context manager entry."""
        echo_info(f"Initializing cache: {self.name}")
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        echo_info(f"Clearing cache: {self.name}")
        self.cache.clear()

    def get(self, key: str) -> str | None:
        """Get value from cache."""
        return self.cache.get(key)

    def set(self, key: str, value: str) -> None:
        """Set value in cache."""
        self.cache[key] = value


class LoggerService:
    """Simple logging service."""

    def __init__(self, level: str = "INFO") -> None:
        self.level = level

    def log(self, message: str) -> None:
        """Log a message."""
        print(f"[{self.level}] {message}")


# ==============================================================================
# COMMANDS
# ==============================================================================


@register_command("init", category="project")
def init_command(name: str = "myproject", template: str = "default") -> None:
    """Initialize a new project."""
    echo_success(f"Initializing project '{name}' with template '{template}'")

    # Simulate project initialization
    echo_info("Creating directory structure...")
    echo_info("Installing dependencies...")
    echo_info("Setting up configuration...")

    echo_success(f"Project '{name}' initialized successfully!")


@register_command("status", aliases=["st", "info"])
def status_command(verbose: bool = False) -> None:
    """Show system status."""
    hub = Hub()

    echo_info("System Status")
    echo_info("=" * 40)

    # Show components
    components = hub.list_components()
    echo_info(f"Registered components: {len(components)}")
    if verbose:
        for comp in components:
            echo_info(f"  - {comp}")

    # Show commands
    commands = hub.list_commands()
    echo_info(f"Registered commands: {len(commands)}")
    if verbose:
        for cmd in commands:
            echo_info(f"  - {cmd}")


@register_command("test-resources", category="testing")
def test_resources_command() -> None:
    """Test resource lifecycle management."""
    hub = Hub()

    echo_info("Testing resource lifecycle...")

    # Get resource classes
    db_class = hub.get_component("database", dimension="resource")
    cache_class = hub.get_component("cache", dimension="resource")

    if not db_class or not cache_class:
        echo_warning("Resources not found!")
        return

    # Test database resource
    echo_info("\nTesting database resource:")
    with db_class("test_db") as db:
        result = db.query("SELECT * FROM users")
        echo_success(f"Query executed: {result}")

    # Test cache resource
    echo_info("\nTesting cache resource:")
    with cache_class("test_cache") as cache:
        cache.set("key1", "value1")
        value = cache.get("key1")
        echo_success(f"Cache test: key1 = {value}")

    echo_success("\nResource lifecycle test completed!")


@register_command("list", category="info")
def list_command(dimension: str | None = None) -> None:
    """List registered components by dimension."""
    hub = Hub()

    if dimension:
        items = hub.list_components(dimension=dimension)
        echo_info(f"Components in dimension '{dimension}':")
        for item in items:
            echo_info(f"  - {item}")
    else:
        all_items = hub._component_registry.list_all()
        for dim, items in all_items.items():
            if dim != "command" and items:
                echo_info(f"\n{dim.upper()}:")
                for item in items:
                    echo_info(f"  - {item}")


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================


def create_demo_cli() -> object:
    """Create the demo CLI application."""
    # Create hub with context
    context = CLIContext(log_level="INFO", profile="demo", debug=False)

    hub = Hub(context=context)

    # Register components
    hub.add_component(DatabaseResource, name="database", dimension="resource", version="1.0.0")
    hub.add_component(CacheResource, name="cache", dimension="resource", version="1.0.0")
    hub.add_component(LoggerService, name="logger", dimension="service", version="2.0.0")

    # Create CLI
    cli = hub.create_cli(
        name="hub-demo",
        version="1.0.0",
        help="Foundation Hub Demo Application",
    )

    return cli


if __name__ == "__main__":
    # Create and run the CLI
    cli = create_demo_cli()
    cli()

    # To test without CLI, uncomment:
    # hub = Hub()
    # test_resources_command()
    # status_command(verbose=True)

# 🧱🏗️🔚
