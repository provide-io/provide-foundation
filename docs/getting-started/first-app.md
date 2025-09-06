# Your First Application

Build a complete application using provide.foundation's logging, CLI, and configuration features.

## What We'll Build

A simple task manager CLI that demonstrates:
- Structured logging with emoji sets
- CLI command registration
- Configuration management
- Error handling
- Console output

## Step 1: Project Setup

Create a new project directory:

```bash
mkdir task-manager
cd task-manager
pip install provide-foundation
```

## Step 2: Create the Application

Create `task_manager.py`:

```python
#!/usr/bin/env python3
"""
Task Manager - A provide.foundation example application
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from provide.foundation import logger, pout, perr
from provide.foundation.cli import register_command, run_cli
from provide.foundation.config import Config
from provide.foundation.platform import get_system_info

# Configure logging
logger.info("task_manager_started", 
            version="1.0.0",
            platform=get_system_info().platform)

@dataclass
class Task:
    """A simple task model."""
    id: str
    title: str
    description: str
    completed: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class TaskManager:
    """Manages tasks with provide.foundation logging."""
    
    def __init__(self, storage_path: Path = Path("tasks.json")):
        self.storage_path = storage_path
        self.tasks: dict[str, Task] = {}
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from storage."""
        if self.storage_path.exists():
            logger.info("tasks_loaded", path=str(self.storage_path))
            # In real app, deserialize from JSON
        else:
            logger.info("tasks_initialized", path=str(self.storage_path))
    
    def add_task(self, title: str, description: str) -> Task:
        """Add a new task."""
        task_id = f"task_{len(self.tasks) + 1}"
        task = Task(id=task_id, title=title, description=description)
        
        self.tasks[task_id] = task
        
        logger.info("task_created",
                   task_id=task_id,
                   title=title)
        
        return task
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed."""
        if task_id not in self.tasks:
            logger.warning("task_not_found", task_id=task_id)
            return False
        
        self.tasks[task_id].completed = True
        logger.info("task_completed", task_id=task_id)
        return True
    
    def list_tasks(self, show_completed: bool = True) -> list[Task]:
        """List all tasks."""
        tasks = list(self.tasks.values())
        
        if not show_completed:
            tasks = [t for t in tasks if not t.completed]
        
        logger.debug("tasks_listed", 
                    count=len(tasks),
                    show_completed=show_completed)
        
        return tasks

# Global task manager instance
manager = TaskManager()

# CLI Commands
@register_command("add")
def add_task(title: str, description: str = ""):
    """Add a new task."""
    try:
        task = manager.add_task(title, description)
        pout(f"✅ Added task: {task.title}")
        return 0
    except Exception as e:
        logger.exception("task_add_failed", error=str(e))
        perr(f"❌ Failed to add task: {e}")
        return 1

@register_command("complete")
def complete_task(task_id: str):
    """Mark a task as completed."""
    if manager.complete_task(task_id):
        pout(f"✅ Completed task: {task_id}")
        return 0
    else:
        perr(f"❌ Task not found: {task_id}")
        return 1

@register_command("list")
def list_tasks(all: bool = False):
    """List tasks (use --all to include completed)."""
    tasks = manager.list_tasks(show_completed=all)
    
    if not tasks:
        pout("📝 No tasks found")
        return 0
    
    pout("📋 Tasks:")
    for task in tasks:
        status = "✅" if task.completed else "⏳"
        pout(f"  {status} [{task.id}] {task.title}")
        if task.description:
            pout(f"      {task.description}")
    
    return 0

@register_command("stats")
def show_stats():
    """Show task statistics."""
    all_tasks = manager.list_tasks(show_completed=True)
    completed = sum(1 for t in all_tasks if t.completed)
    pending = len(all_tasks) - completed
    
    pout("📊 Task Statistics:")
    pout(f"  Total: {len(all_tasks)}")
    pout(f"  Completed: {completed}")
    pout(f"  Pending: {pending}")
    
    if all_tasks:
        completion_rate = (completed / len(all_tasks)) * 100
        pout(f"  Completion Rate: {completion_rate:.1f}%")
    
    logger.info("stats_displayed",
               total=len(all_tasks),
               completed=completed,
               pending=pending)
    
    return 0

if __name__ == "__main__":
    # Run the CLI
    run_cli()
```

## Step 3: Run Your Application

Make it executable and try it out:

```bash
chmod +x task_manager.py

# Add tasks
./task_manager.py add "Write documentation" --description "Create user guide"
./task_manager.py add "Review PR" --description "Review pull request #42"

# List tasks
./task_manager.py list

# Complete a task
./task_manager.py complete task_1

# Show statistics
./task_manager.py stats
```

## Step 4: Add Configuration

Create a configuration file `config.yaml`:

```yaml
telemetry:
  level: INFO
  format: pretty
  enable_emoji: true

task_manager:
  storage_path: ~/.task_manager/tasks.json
  auto_save: true
  max_tasks: 1000
```

Update the application to use configuration:

```python
from provide.foundation.config import Config

# Load configuration
config = Config.from_file("config.yaml")

# Use in TaskManager
class TaskManager:
    def __init__(self):
        self.storage_path = Path(config.get("task_manager.storage_path", "tasks.json"))
        self.auto_save = config.get("task_manager.auto_save", True)
        self.max_tasks = config.get("task_manager.max_tasks", 1000)
```

## Step 5: Understanding Emoji Sets

Emoji sets provide automatic emoji mapping for structured log fields:

```python
from provide.foundation import logger

# When you log with semantic field names, emojis are added automatically
# For example, if HTTP emoji set is enabled:

logger.info("http_request",
    **{"http.method": "GET",        # Automatically gets 📥 emoji
       "http.status_code": 200,      # Automatically gets ✅ emoji
       "http.target": "/api/tasks"})

# For task operations, you can define custom semantic fields:
from provide.foundation.types import EmojiSetConfig, CustomDasEmojiSet, FieldToEmojiMapping

# Define emoji mappings for task operations
TASK_EMOJI_SETS = [
    CustomDasEmojiSet(
        name="task_action",
        emojis={
            "create": "🆕",
            "complete": "✅",
            "delete": "🗑️",
            "update": "✏️",
            "default": "📝"
        },
        default_emoji_key="default"
    )
]

# Create emoji set configuration
TASK_LAYER = EmojiSetConfig(
    name="task",
    description="Task management operations",
    emoji_sets=TASK_EMOJI_SETS,
    field_definitions=[
        FieldToEmojiMapping(
            log_key="task.action",
            emoji_set_name="task_action"
        )
    ]
)

# Then when you log with these field names:
logger.info("task_operation",
    **{"task.action": "create",      # Gets 🆕 emoji automatically
       "task.id": "task_1",
       "task.title": "My Task"})
```

## What You've Learned

This application demonstrates:

✅ **Structured Logging**: Every operation is logged with context
✅ **CLI Framework**: Commands with arguments and options
✅ **Configuration**: YAML-based configuration management
✅ **Error Handling**: Graceful error recovery with logging
✅ **Console Output**: User-friendly output with emojis
✅ **Emoji Sets**: Domain-specific emoji mapping for visual log parsing

## Next Steps

1. **Add persistence**: Save tasks to JSON file
2. **Add search**: Implement task search functionality
3. **Add due dates**: Track task deadlines
4. **Add categories**: Organize tasks by category
5. **Add export**: Export tasks to CSV/JSON

## Complete Example

The full example is available at:
[GitHub: provide-foundation-examples](https://github.com/provide-io/provide-foundation/tree/main/examples/task-manager)

## Key Takeaways

- **Start simple**: Use basic features first, add complexity as needed
- **Log everything**: Structured logging helps debugging and monitoring
- **Use emoji sets**: Domain-specific logging improves clarity
- **Handle errors gracefully**: Always log errors with context
- **Provide feedback**: Use pout/perr for user feedback

Ready to explore more? Check out the [User Guide](../guide/index.md) →