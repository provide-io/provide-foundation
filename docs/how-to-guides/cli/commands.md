# How to Register CLI Commands

`provide.foundation` simplifies CLI development by allowing you to register Python functions as commands using decorators.

## Basic Command Registration

Use the `@register_command` decorator to expose a function as a CLI command.

```python
# From: examples/cli/01_cli_application.py
from provide.foundation.hub import register_command
from provide.foundation.cli import echo_success

@register_command("init")
def init_command(name: str = "myproject", template: str = "default"):
    """Initialize a new project."""
    echo_success(f"Initializing project '{name}' with template '{template}'")
```
-   **Function Signature:** The framework inspects parameters (`name`, `template`) and type hints to create CLI arguments and options.
-   **Docstring:** The docstring is automatically used to generate the help text.

## Nested Commands

Organize commands into groups using dot notation.

```python
# From: examples/cli/02_dogfooding_cli.py (conceptual)
@register_command("db.migrate")
def migrate_database():
    """Run database migrations."""
    pout("Running migrations...")

@register_command("db.seed")
def seed_database():
    """Seed the database."""
    pout("Seeding database...")
```
This creates a `db` command group with `migrate` and `seed` subcommands.

## Command Metadata

Add metadata like aliases and categories for better organization.

```python
# From: examples/cli/01_cli_application.py
@register_command("status", aliases=["st", "info"], category="info")
def status_command(verbose: bool = False):
    """Show system status."""
    # ...
```
-   `aliases`: The command can be called as `status`, `st`, or `info`.
-   `category`: Groups the command under "info" in the main help text.
