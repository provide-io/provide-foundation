# Nested Commands

Build complex command hierarchies using provide.foundation's nested command system.

## Overview

Nested commands allow you to create structured CLI applications with logical groupings. Commands can be organized into hierarchies using dot notation.

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
```

This will create a command `app` with a subcommand `config`, which in turn has three subcommands: `show`, `set`, and `reset`.

### Deep Nesting

You can create multiple levels of nesting:

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
```

This creates the following command structure:
- `project env dev setup`
- `project env dev teardown`
- `project env prod deploy`

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

## Related Topics

- [Command Registration](commands.md) - Basic command registration
- [Arguments & Options](arguments.md) - Adding arguments to commands
- [Output Formatting](output.md) - Formatting command output