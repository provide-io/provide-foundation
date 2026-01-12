# Your First Application

Build a complete CLI task manager in 15 minutes. This tutorial demonstrates how Foundation's logging, CLI framework, and console output utilities work together.

## What We'll Build

A command-line task manager with:
- Add, complete, and list tasks
- Structured logging for every action
- Clean separation of logs from user output
- Beautiful console output with colors and emojis

**Final result:**
```bash
$ task-manager add "Write documentation"
✅ Successfully added task 1: 'Write documentation'

$ task-manager list
📋 Your Tasks:
  ⏳ [1] Write documentation

$ task-manager complete 1
Task 1 marked as complete.
```

## 1. Project Setup

Create a new project directory:

```bash
mkdir task-manager
cd task-manager
uv add provide-foundation[all]
```

## 2. Create the Application

Create a file named `task_manager.py`:

```python
#!/usr/bin/env python3
# task_manager.py
import sys
from dataclasses import dataclass, field
from datetime import datetime

from provide.foundation import logger, pout, perr, get_hub
from provide.foundation.hub import register_command

# --- Data Model ---
@dataclass
class Task:
    """A simple task model."""
    id: int
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

# --- In-Memory "Database" ---
TASKS: dict[int, Task] = {}
NEXT_ID = 1

# --- CLI Commands ---
@register_command("add")
def add_task(title: str):
    """Add a new task."""
    global NEXT_ID
    task = Task(id=NEXT_ID, title=title)
    TASKS[task.id] = task
    logger.info("task_created", task_id=task.id, title=task.title, emoji="✅")
    pout(f"Successfully added task {task.id}: '{task.title}'", color="green")
    NEXT_ID += 1

@register_command("complete")
def complete_task(task_id: int):
    """Mark a task as completed."""
    if task_id not in TASKS:
        logger.warning("task_not_found", task_id=task_id, emoji="❓")
        perr(f"Error: Task with ID {task_id} not found.", color="red")
        sys.exit(1)

    TASKS[task_id].completed = True
    logger.info("task_completed", task_id=task_id, emoji="🎉")
    pout(f"Task {task_id} marked as complete.", color="cyan")

@register_command("list")
def list_tasks(all: bool = False):
    """List tasks. Use --all to include completed tasks."""
    logger.debug("listing_tasks", show_all=all)
    tasks_to_show = list(TASKS.values())
    if not all:
        tasks_to_show = [t for t in tasks_to_show if not t.completed]

    if not tasks_to_show:
        pout("No tasks to show.", color="yellow")
        return

    pout("📋 Your Tasks:", bold=True)
    for task in tasks_to_show:
        status = "✅" if task.completed else "⏳"
        color = "green" if task.completed else "yellow"
        pout(f"  {status} [{task.id}] {task.title}", color=color)

# --- Main Entry Point ---
if __name__ == "__main__":
    # 1. Get the global Hub instance
    hub = get_hub()

    # 2. The Hub discovers @register_command functions and builds a CLI
    cli = hub.create_cli(name="task-manager")

    # 3. Run the CLI
    logger.info("cli_starting", emoji="🚀")
    cli()
    logger.info("cli_finished", emoji="🏁")
```

*This code is based on `examples/cli/01_cli_application.py`.*

## 3. Run Your Application

### Get Help

```bash
$ python task_manager.py --help
Usage: task-manager [OPTIONS] COMMAND [ARGS]...

  A simple task manager.

Options:
  --help  Show this message and exit.

Commands:
  add       Add a new task.
  complete  Mark a task as completed.
  list      List tasks.
```

### Add Tasks

```bash
$ python task_manager.py add "Write documentation"
✅ Successfully added task 1: 'Write documentation'

$ python task_manager.py add "Review pull requests"
✅ Successfully added task 2: 'Review pull requests'

$ python task_manager.py add "Deploy to production"
✅ Successfully added task 3: 'Deploy to production'
```

### List Tasks

```bash
$ python task_manager.py list
📋 Your Tasks:
  ⏳ [1] Write documentation
  ⏳ [2] Review pull requests
  ⏳ [3] Deploy to production
```

### Complete Tasks

```bash
$ python task_manager.py complete 1
Task 1 marked as complete.

$ python task_manager.py list
📋 Your Tasks:
  ⏳ [2] Review pull requests
  ⏳ [3] Deploy to production

$ python task_manager.py list --all
📋 Your Tasks:
  ✅ [1] Write documentation
  ⏳ [2] Review pull requests
  ⏳ [3] Deploy to production
```

## 4. Understanding the Code

### Declarative CLI Commands

The `@register_command` decorator registers functions as CLI commands:

```python
@register_command("add")
def add_task(title: str):
    """Add a new task."""
    # Function signature becomes CLI arguments
    # Docstring becomes help text
```

Foundation automatically:
- Converts function parameters to CLI arguments
- Generates help text from docstrings
- Handles type conversion (str, int, bool, etc.)

### The create_cli() Method

The `hub.create_cli()` method builds a Click CLI from registered commands:

```python
cli = hub.create_cli(
    name="task-manager",        # CLI program name
    version="1.0.0"             # Version string (optional)
)
```

**Parameters:**
- `name` (str): CLI name shown in help text (default: "cli")
- `version` (str | None): Optional version for `--version` flag
- `**kwargs`: Additional Click Group options (e.g., `help`, `context_settings`)

### Structured Logging

Every action is logged with structured data:

```python
logger.info("task_created", task_id=task.id, title=task.title, emoji="✅")
```

Benefits:
- Easy to search logs for specific events (`task_created`)
- Filterable by any field (`task_id=123`)
- Machine-readable for log aggregation systems

### Output Separation

Foundation separates concerns:

```python
# For system logs (operators/debugging)
logger.info("task_created", task_id=1)

# For user feedback (CLI output)
pout("✅ Successfully added task", color="green")
```

This allows you to:
- Send logs to files/services without cluttering user output
- Format user messages beautifully with colors
- Keep structured logs for analysis

## 5. Adding Persistence (Optional)

Extend the task manager with file-based persistence:

```python
from provide.foundation.serialization import provide_dumps, provide_loads
from pathlib import Path

TASKS_FILE = Path("tasks.json")

def save_tasks():
    """Save tasks to disk."""
    data = {
        "tasks": [
            {"id": t.id, "title": t.title, "completed": t.completed}
            for t in TASKS.values()
        ],
        "next_id": NEXT_ID,
    }
    TASKS_FILE.write_text(provide_dumps(data, indent=2))
    logger.debug("tasks_saved", count=len(TASKS))

def load_tasks():
    """Load tasks from disk."""
    global NEXT_ID
    if not TASKS_FILE.exists():
        return

    data = provide_loads(TASKS_FILE.read_text())
    for task_data in data["tasks"]:
        task = Task(**task_data)
        TASKS[task.id] = task
    NEXT_ID = data["next_id"]
    logger.debug("tasks_loaded", count=len(TASKS))

# Call load_tasks() at startup
# Call save_tasks() after each modification
```

## 6. What You've Learned

✅ **Declarative CLI** - Define commands with `@register_command`
✅ **Structured Logging** - Track actions with key-value logging
✅ **Output Separation** - Logs for operators, `pout`/`perr` for users
✅ **Hub System** - Central registry for commands and components
✅ **Beautiful Console** - Colors and emojis for better UX

## Next Steps

### Explore More Features

- **[CLI Commands Guide](../how-to-guides/cli/commands.md)** - Advanced CLI patterns
- **[Basic Logging](../how-to-guides/logging/basic-logging.md)** - More logging techniques
- **[Retry Patterns](../how-to-guides/resilience/retry.md)** - Add resilience to your app

### See More Examples

Browse the [Examples](examples.md) section for:
- Configuration management
- HTTP client usage
- Async programming
- Production patterns

### Build Production Applications

- Add configuration for different environments
- Implement error handling and retries
- Add metrics and monitoring
- Deploy as a package

---

**Congratulations!** You've built a complete CLI application with Foundation.

**Next:** Explore [How-To Guides](../how-to-guides/logging/basic-logging.md) for specific use cases.
