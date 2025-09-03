# CLI Framework API

Command-line interface framework for provide.foundation.

## Available Modules

- [Decorators](decorators.md) - Command registration and argument decorators
- [CLI Utils](base.md) - CLI utilities and helper functions  
- [Testing](helpers.md) - CLI testing utilities

## Quick Reference

### Command Registration

```python
from provide.foundation.cli import register_command

@register_command("hello")
def hello_command(name: str = "World"):
    """Say hello to someone."""
    print(f"Hello, {name}!")
```

### Nested Commands

```python
@register_command("db.migrate")
def migrate():
    """Run database migrations."""
    pass

@register_command("db.seed")  
def seed():
    """Seed the database."""
    pass
```

### With Options

```python
from provide.foundation.cli import option, argument

@register_command("deploy")
@option("--environment", "-e", default="staging")
@option("--dry-run", is_flag=True)
@argument("service")
def deploy(service: str, environment: str, dry_run: bool):
    """Deploy a service."""
    if dry_run:
        print(f"Would deploy {service} to {environment}")
    else:
        print(f"Deploying {service} to {environment}")
```