# Nested Commands

Build complex command hierarchies using provide.foundation's nested command system.

## Overview

Nested commands allow you to create structured CLI applications with logical groupings. Commands can be organized into hierarchies using dot notation or explicit groups.

## Dot Notation

### Basic Nesting

Use dots to create nested command structures:

```python
from provide.foundation.hub import register_command

@register_command("app.config.show")
def show_config():
    """Show application configuration."""
    print("Configuration...")

@register_command("app.config.set")
def set_config():
    """Set configuration values."""
    print("Setting config...")

@register_command("app.config.reset")
def reset_config():
    """Reset to default configuration."""
    print("Resetting config...")

# Usage:
# myapp app config show
# myapp app config set
# myapp app config reset
```

### Deep Nesting

Create multiple levels of nesting:

```python
@register_command("project.env.dev.setup")
def setup_dev():
    """Setup development environment."""
    pass

@register_command("project.env.dev.teardown")
def teardown_dev():
    """Teardown development environment."""
    pass

@register_command("project.env.prod.deploy")
def deploy_prod():
    """Deploy to production."""
    pass

# Creates structure:
# myapp project env dev setup
# myapp project env dev teardown  
# myapp project env prod deploy
```

## Explicit Groups

### Group Definition

Define groups explicitly for better control:

```python
@register_command("db", group=True, description="Database operations")
def db_group():
    """Database management commands."""
    pass

@register_command("cache", group=True, description="Cache management")
def cache_group():
    """Cache operations."""
    pass
```

### Adding Commands to Groups

Add commands to defined groups:

```python
# Define the group
@register_command("api", group=True, description="API management")
def api_group():
    pass

# Add commands to the group
@register_command("api.start")
@click.option('--port', type=int, default=8000)
def api_start(port):
    """Start the API server."""
    print(f"Starting API on port {port}")

@register_command("api.stop")
def api_stop():
    """Stop the API server."""
    print("Stopping API...")

@register_command("api.status")
def api_status():
    """Check API status."""
    print("API is running")
```

## Command Organization

### Logical Grouping

Organize commands by functionality:

```python
# Database commands
@register_command("db.migrate.up")
def migrate_up():
    """Run migrations."""
    pass

@register_command("db.migrate.down")
def migrate_down():
    """Rollback migrations."""
    pass

@register_command("db.migrate.status")
def migrate_status():
    """Show migration status."""
    pass

# Cache commands
@register_command("cache.clear.all")
def clear_all_cache():
    """Clear all caches."""
    pass

@register_command("cache.clear.redis")
def clear_redis():
    """Clear Redis cache."""
    pass

@register_command("cache.stats")
def cache_stats():
    """Show cache statistics."""
    pass
```

## Best Practices

### Naming Conventions

Use consistent naming patterns:

```python
# Good: Clear hierarchy
@register_command("resource.action.target")
# Examples:
@register_command("db.migrate.up")
@register_command("cache.clear.all")
@register_command("api.auth.refresh")

# Avoid: Inconsistent patterns
@register_command("migrate-database")  # Mixed style
@register_command("clearCache")        # CamelCase
```

### Shallow vs Deep

Balance hierarchy depth - 2-3 levels is usually optimal:

```python
# Good: Clear and memorable
@register_command("app.config.get")
@register_command("app.db.migrate")

# Too deep: Hard to remember and type
@register_command("app.subsystem.component.feature.action.target")
```

## Complete Example

Here's a complete nested CLI application:

```python
#!/usr/bin/env python
"""Multi-tier CLI application."""

import click
from provide.foundation.hub import register_command, HubManager
from provide.foundation import logger

# === Application Management ===
@register_command("app", group=True, description="Application management")
def app_group():
    pass

@register_command("app.start")
@click.option('--daemon', is_flag=True)
def app_start(daemon):
    """Start the application."""
    mode = "daemon" if daemon else "foreground"
    logger.info(f"Starting app in {mode} mode")

@register_command("app.stop")
def app_stop():
    """Stop the application."""
    logger.info("Stopping app")

# === Database Operations ===
@register_command("db.migrate.up")
@click.option('--version', help='Target version')
def db_migrate_up(version):
    """Run database migrations."""
    logger.info(f"Migrating up to {version or 'latest'}")

@register_command("db.migrate.down")
@click.option('--steps', type=int, default=1)
def db_migrate_down(steps):
    """Rollback database migrations."""
    logger.info(f"Rolling back {steps} migration(s)")

# === Cache Management ===
@register_command("cache.clear")
@click.option('--pattern', help='Key pattern to clear')
def cache_clear(pattern):
    """Clear cache entries."""
    if pattern:
        logger.info(f"Clearing cache pattern: {pattern}")
    else:
        logger.info("Clearing all cache")

def main():
    """Create and run the CLI."""
    manager = HubManager(
        name="myapp",
        description="Complex CLI Application"
    )
    cli = manager.create_cli()
    cli()

if __name__ == "__main__":
    main()
```

## Related Topics

- [Command Registration](commands.md) - Basic command registration
- [Arguments & Options](arguments.md) - Adding arguments to commands
- [Output Formatting](output.md) - Formatting nested command output