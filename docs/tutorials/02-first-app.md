# Tutorial: Your First CLI Application

In this tutorial, we'll build a simple but complete task manager CLI. This will demonstrate how `provide.foundation`'s logging, CLI framework, and console output utilities work together.

## What We'll Build

A CLI tool to add, complete, and list tasks, showcasing:
- Structured logging for every action.
- Declarative CLI commands with arguments.
- Clean separation of logs from user-facing output.

## 1. Project Setup

Create a new project directory and install the framework.

```bash
mkdir task-manager
cd task-manager
pip install "provide-foundation[all]"```

## 2. Create the Application

Create a file named `task_manager.py`:

```python
#!/usr/bin/env python3
# task_manager.py
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

from provide.foundation import logger, pout, perr, setup_telemetry
from provide.foundation.hub import Hub, register_command

# --- Data Model ---
@dataclass
class Task:
    """A simple task model."""
    id: int
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

# --- In-Memory "Database" ---
TASKS: Dict[int, Task] = {}
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
    logger.info("task_completed", task_id=task.id, emoji="🎉")
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
    setup_telemetry()
    hub = Hub()
    cli = hub.create_cli(name="task-manager", description="A simple task manager.")
    logger.info("cli_starting", emoji="🚀")
    cli()
    logger.info("cli_finished", emoji="🏁")
```
*This code is a simplified version of `examples/cli/01_cli_application.py`.*

## 3. Run Your Application

Let's use the CLI we just built.

```bash
# Get help for the main command
$ python task_manager.py --help
Usage: task-manager [OPTIONS] COMMAND [ARGS]...

  A simple task manager.

Options:
  --help  Show this message and exit.

Commands:
  add       Add a new task.
  complete  Mark a task as completed.
  list      List tasks.

# Add some tasks
$ python task_manager.py add "Write documentation"
✅ Successfully added task 1: 'Write documentation'

# List pending tasks
$ python task_manager.py list
📋 Your Tasks:
  ⏳ Write documentation

# Complete a task
$ python task_manager.py complete 1
Task 1 marked as complete.
```

## 4. What You've Learned

-   **Declarative CLI:** You defined your CLI by simply writing Python functions and decorating them with `@register_command`.
-   **Structured Logging:** Every action (`task_created`, `task_completed`) is logged with structured data.
-   **Separation of Concerns:** `logger` is for system logs, while `pout` and `perr` are for user-facing output.

---

**Next Steps:**
- Dive into the **[How-To Guides](../how-to-guides/cli/commands/)** to learn more about building CLIs.
