#!/usr/bin/env python3
"""
Generates the entire documentation structure for the provide.foundation library.

This script reorganizes the existing documentation into a user-centric structure
based on the Diátaxis framework, separating tutorials, how-to guides, explanations,
and technical references. It also isolates forward-looking design specifications
to avoid confusing users with unimplemented features.

To run:
    python generate_documentation.py [output_directory]

Default output directory is 'docs_generated'.
"""

import sys
from pathlib import Path
import shutil

# ==============================================================================
# Main Orchestration
# ==============================================================================

def main(output_dir_name: str = "docs_generated"):
    """
    Generates the full, reorganized documentation structure.
    """
    root_path = Path(output_dir_name)
    if root_path.exists():
        print(f"Removing existing directory: {root_path}")
        shutil.rmtree(root_path)

    print(f"Creating new documentation in: {root_path}")
    root_path.mkdir()

    # Create top-level structure
    create_toplevel_files(root_path)
    create_tutorials(root_path / "tutorials")
    create_how_to_guides(root_path / "how-to-guides")
    create_explanation(root_path / "explanation")
    create_reference(root_path / "reference")
    create_specs(root_path / "specs")

    print("\n✅ Documentation generation complete.")
    print(f"Run 'mkdocs serve' in the '{root_path}' directory to view the site.")


# ==============================================================================
# Top-Level Structure and Content
# ==============================================================================

def create_toplevel_files(root_path: Path):
    """Creates the main index.md and other top-level files."""
    (root_path / "index.md").write_text(
        """
# Welcome to Provide Foundation

**A comprehensive Python 3.11+ library for building operationally excellent applications.**

Provide Foundation offers a cohesive, "batteries-included" toolkit for structured logging, CLI development, configuration management, and system utilities. It is designed to accelerate the development of robust, production-ready services.

---

## Where to Start

<div class="feature-grid">
  <div class="feature-card">
    <h3>🚀 Tutorials</h3>
    <p>Step-by-step guides to get you started. Perfect for new users.</p>
    <a href="tutorials/01-installation/">Get Started →</a>
  </div>

  <div class="feature-card">
    <h3>🛠️ How-To Guides</h3>
    <p>Practical, goal-oriented recipes for solving common problems.</p>
    <a href="how-to-guides/logging/structured-logging/">Learn More →</a>
  </div>

  <div class="feature-card">
    <h3>🧠 Explanation</h3>
    <p>Deep dives into the concepts and architecture behind the framework.</p>
    <a href="explanation/architecture/">Explore →</a>
  </div>

  <div class="feature-card">
    <h3>📚 API Reference</h3>
    <p>The complete, detailed technical reference for every module and function.</p>
    <a href="reference/">Browse →</a>
  </div>
</div>

## Core Features

- **Structured Logging**: Beautiful, performant logging with emoji-enhanced visual parsing.
- **CLI Framework**: Decorator-based command registration with automatic help generation.
- **Configuration Management**: Type-safe configuration from multiple sources (env, files).
- **Resilience Patterns**: Built-in decorators for Retry, Circuit Breaker, and Fallback.
- **System Utilities**: Cross-platform tools for process execution, file operations, and more.
- **Security**: Utilities for masking secrets and handling sensitive data.
"""
    )


# ==============================================================================
# Section: Tutorials
# ==============================================================================

def create_tutorials(path: Path):
    """Generates the 'Tutorials' section."""
    path.mkdir()
    (path / "index.md").write_text("# Tutorials\n\nLearn by doing with these step-by-step guides.")

    (path / "01-installation.md").write_text(
        """
# 1. Installation

Installing `provide.foundation` is straightforward. You can use `pip`, `uv`, or your favorite Python package manager.

## Requirements

- Python 3.11 or higher

## Standard Installation

To install the latest stable release from PyPI, run:

```bash
pip install "provide-foundation[all]"
```
*We recommend installing with the `[all]` extra to include all optional dependencies for the best experience.*

## Verifying the Installation

To ensure the library was installed correctly, run the following command in your terminal:

```bash
python -c "from provide.foundation import logger; logger.info('Installation successful!')"
```

If successful, you will see a formatted log message, confirming that the core logging system is working.

---

Next, head to the [**Quick Start**](./02-quick-start.md) guide to write your first application.
"""
    )

    (path / "02-quick-start.md").write_text(
        """
# 2. Quick Start: Your First Log Messages

This guide will walk you through the absolute basics of using `provide.foundation` for logging.

## Zero-Setup Logging

The easiest way to start is to import the global `logger` instance. Create a Python file named `app.py`:

```python
# app.py
from provide.foundation import logger, setup_telemetry

def main():
    """A simple function to demonstrate basic logging."""
    # This single call configures logging with sensible defaults
    setup_telemetry()

    logger.info("Application starting up")

    # Logging with structured context
    logger.info(
        "User logged in",
        user_id="usr_12345",
        source="google_oauth",
        ip_address="192.168.1.101",
    )

    logger.warning("Disk space is running low", free_space_gb=5)

    # Logging an error with exception info
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception(
            "An expected error occurred during a critical calculation",
            error_details="Attempted to divide by zero",
        )

    logger.info("Application shutting down")

if __name__ == "__main__":
    main()
```

## Running the Example

Execute the script from your terminal:

```bash
python app.py
```

## Understanding the Output

You will see beautifully formatted and instantly scannable output in your console:

```
INFO application_startup
INFO User logged in                        user_id=usr_12345 source=google_oauth ip_address=192.168.1.101
WARN Disk space is running low             free_space_gb=5
ERRO An expected error occurred...         error_details="Attempted to divide by zero"
     Traceback (most recent call last):
       ...
INFO Application shutting down
```

### What You're Seeing

1.  **Structured Context**: The keyword arguments you passed are automatically formatted as `key=value` pairs. This is the core of **structured logging**.
2.  **Visual Markers**: The log level (e.g., `INFO`, `WARN`) provides immediate context. With emoji sets enabled, you'd see even richer visual cues.
3.  **Exception Information**: When you use `logger.exception()`, the full exception traceback is automatically captured and included.

---

Congratulations! You've successfully used `provide.foundation` to produce structured, human-readable logs.

Next, let's build a complete application in the [**First Application**](./03-first-application.md) tutorial.
"""
    )

    (path / "03-first-application.md").write_text(
        """
# 3. Your First Application: A CLI Task Manager

Let's build a simple but complete task manager CLI to demonstrate logging, CLI commands, and configuration.

## Step 1: Project Setup

Create a new project directory:

```bash
mkdir task-manager
cd task-manager
pip install "provide-foundation[cli]"
```

## Step 2: Create the Application (`task_manager.py`)

```python
#!/usr/bin/env python3
from provide.foundation import logger, pout, perr, setup_telemetry
from provide.foundation.hub import Hub, register_command

# In-memory storage for our tasks
tasks = {}

@register_command("add")
def add_task(title: str):
    """Add a new task."""
    task_id = f"task_{len(tasks) + 1}"
    tasks[task_id] = {"title": title, "completed": False}
    logger.info("task_created", task_id=task_id, title=title)
    pout(f"✅ Added task: '{title}' (ID: {task_id})")

@register_command("list")
def list_tasks():
    """List all tasks."""
    if not tasks:
        pout("📝 No tasks found.")
        return

    pout("📋 Your Tasks:")
    for task_id, task in tasks.items():
        status = "✅" if task["completed"] else "⏳"
        pout(f"  {status} [{task_id}] {task['title']}")
    logger.debug("tasks_listed", count=len(tasks))

@register_command("complete")
def complete_task(task_id: str):
    """Mark a task as completed."""
    if task_id not in tasks:
        logger.warning("task_not_found", task_id=task_id)
        perr(f"❌ Error: Task with ID '{task_id}' not found.")
        return

    tasks[task_id]["completed"] = True
    logger.info("task_completed", task_id=task_id)
    pout(f"✅ Completed task: '{tasks[task_id]['title']}'")

def main():
    """Sets up and runs the CLI application."""
    # Configure logging and discover registered commands
    setup_telemetry()
    logger.info("task_manager_startup")

    # The Hub automatically discovers @register_command functions
    # and builds a CLI from them.
    hub = Hub()
    cli = hub.create_cli(name="task-manager", description="A simple CLI task manager.")
    cli()

if __name__ == "__main__":
    main()
```

## Step 3: Run Your Application

Make the script executable and try it out:

```bash
chmod +x task_manager.py

# Get help
./task_manager.py --help

# Add some tasks
./task_manager.py add "Learn provide.foundation"
./task_manager.py add "Build an awesome app"

# List your tasks
./task_manager.py list

# Complete a task
./task_manager.py complete task_1

# List again to see the change
./task_manager.py list
```

## What You've Learned

This simple application demonstrates several core features of `provide.foundation`:

-   **Structured Logging**: Every action is logged with context (`logger.info`).
-   **User-Facing Output**: Clean, friendly messages are printed to the console (`pout`, `perr`).
-   **CLI Framework**: A complete CLI with commands, arguments, and help text was created automatically using the `@register_command` decorator and the `Hub`.

This is the power of `provide.foundation`: building robust, observable applications with minimal boilerplate.
"""
    )


# ==============================================================================
# Section: How-To Guides
# ==============================================================================

def create_how_to_guides(path: Path):
    """Generates the 'How-To Guides' section."""
    path.mkdir()
    (path / "index.md").write_text("# How-To Guides\n\nFind solutions to common problems.")

    # Logging Guides
    logging_path = path / "logging"
    logging_path.mkdir()
    (logging_path / "structured-logging.md").write_text(
        """
# How to Use Structured Logging

Structured logging is the practice of treating logs as data. Instead of writing unstructured text strings, you log events with key-value pairs.

## Basic Structured Logging

Use the global `logger` and provide context as keyword arguments.

```python
from provide.foundation import logger, setup_telemetry

setup_telemetry()

# Log an event with structured data
logger.info(
    "user_login_successful",
    user_id="usr_123",
    ip_address="192.168.1.100",
    auth_method="password"
)

# In production (with JSON formatter), this would produce:
# {"event": "user_login_successful", "level": "info", "user_id": "usr_123", ...}
```

## Binding Context

For operations where the same context applies to multiple log entries (like a web request), use `logger.bind()` to create a context-aware logger.

```python
import uuid

request_id = str(uuid.uuid4())

# Create a logger with bound context
request_logger = logger.bind(request_id=request_id)

request_logger.info("request_started", method="GET", path="/api/data")
# ... do some work ...
request_logger.debug("database_query_executed", duration_ms=52)
# ... do more work ...
request_logger.info("request_completed", status_code=200)

# The 'request_id' is automatically included in all three log entries.
```

## Logging Exceptions

Use `logger.exception()` inside an `except` block to automatically capture the full stack trace.

```python
try:
    # Some operation that might fail
    result = 10 / 0
except Exception:
    logger.exception(
        "critical_calculation_failed",
        operation="division",
        dividend=10
    )
```
"""
    )
    (logging_path / "production-logging.md").write_text(
        """
# How to Configure Production-Ready Logging

For production environments, you need logging that is performant, machine-readable, and reliable.

## Use the JSON Formatter

The `json` formatter is essential for production. It outputs each log entry as a single line of JSON, which can be easily ingested and parsed by log aggregation systems like OpenObserve, Datadog, or the ELK stack.

Configure this with an environment variable:

```bash
export PROVIDE_LOG_FORMAT=json
```

## Set an Appropriate Log Level

In production, you typically don't need `DEBUG` or `TRACE` level logs. `INFO` is a good default, while `WARNING` can be used to reduce log volume further.

```bash
export PROVIDE_LOG_LEVEL=INFO
```

## Silence Noisy Libraries

Third-party libraries can be very chatty. You can set specific log levels for them to reduce noise.

```python
from provide.foundation import setup_telemetry, LoggingConfig

# Silence noisy libraries while keeping your app's logs at DEBUG
config = LoggingConfig(
    default_level="DEBUG",
    module_levels={
        "httpx": "WARNING",
        "sqlalchemy.engine": "INFO",
    }
)
setup_telemetry(logging_config=config)
```

## Full Production Configuration Example

Here is a recommended setup for a production service:

```python
# In your application's main entry point
import os
from provide.foundation import setup_telemetry, LoggingConfig

# Best practice: Load from environment or a config file
log_level = os.getenv("LOG_LEVEL", "INFO")
service_name = os.getenv("SERVICE_NAME", "my-awesome-service")

prod_config = LoggingConfig(
    default_level=log_level,
    console_formatter="json",
    # Disable emojis and colors for machine-readable logs
    das_emoji_prefix_enabled=False,
    logger_name_emoji_prefix_enabled=False,
    # Silence common noisy libraries
    module_levels={
        "uvicorn.access": "WARNING",
        "httpx": "WARNING",
    }
)

setup_telemetry(service_name=service_name, logging_config=prod_config)
```
"""
    )
    # ... Other how-to guides would be created similarly ...

    # CLI Guides
    cli_path = path / "cli"
    cli_path.mkdir()
    (cli_path / "building-a-cli.md").write_text(
        """
# How to Build a CLI Application

`provide.foundation` makes building powerful and consistent CLIs simple using a decorator-based approach.

## 1. Registering Commands

A command is a simple Python function decorated with `@register_command`.

```python
from provide.foundation.hub import register_command
from provide.foundation import pout

@register_command
def hello():
    \"\"\"Prints a simple greeting.\"\"\"
    pout("Hello, from your first CLI command!")
```

## 2. Handling Arguments and Options

The framework automatically creates CLI arguments from your function's signature, including type hints and default values.

```python
import click # provide.foundation uses Click under the hood

@register_command
@click.option('--excited', is_flag=True, help='Show more excitement!')
def greet(name: str, excited: bool):
    \"\"\"Greets a specific person.\"\"\"
    message = f"Hello, {name}"
    if excited:
        message += "!!!"
    pout(message)
```

## 3. Creating Nested Commands

Organize your CLI by creating nested commands using dot notation in the command name.

```python
@register_command("db.migrate")
def db_migrate():
    \"\"\"Runs database migrations.\"\"\"
    pout("Running migrations...")

@register_command("db.seed")
def db_seed():
    \"\"\"Seeds the database with initial data.\"\"\"
    pout("Seeding data...")
```
This creates a `db` command group with `migrate` and `seed` subcommands.

## 4. Putting It All Together

Here is a complete, runnable script for a simple CLI application.

```python
#!/usr/bin/env python3
from provide.foundation import setup_telemetry, pout
from provide.foundation.hub import Hub, register_command

# --- Command Definitions ---

@register_command
def hello(name: str = "World"):
    \"\"\"A simple greeting command.\"\"\"
    pout(f"Hello, {name}!")

@register_command("db.migrate")
def db_migrate():
    \"\"\"Runs database migrations.\"\"\"
    pout("Running migrations...")

# --- Main Application Entry Point ---

def main():
    \"\"\"Sets up and runs the CLI application.\"\"\"
    setup_telemetry()

    # The Hub discovers all registered commands and builds the CLI
    hub = Hub()
    cli = hub.create_cli(
        name="my-app",
        description="An awesome app built with provide.foundation."
    )
    cli()

if __name__ == "__main__":
    main()
```
"""
    )

# ==============================================================================
# Section: Explanation
# ==============================================================================

def create_explanation(path: Path):
    """Generates the 'Explanation' section."""
    path.mkdir()
    (path / "index.md").write_text("# Explanation\n\nUnderstand the concepts and design behind the framework.")

    (path / "architecture.md").write_text(
        """
# Architecture & Design Philosophy

`provide.foundation` is designed as a **foundation layer**, not a full-stack framework. It provides the essential, cross-cutting infrastructure needed to build any high-quality Python application.

## Core Principles

1.  **Strong Opinions, Graceful Extensibility**: The framework provides a curated, "batteries-included" stack (structlog, attrs, click) that works out of the box. However, its components are designed with protocols and adapters to allow for extension.
2.  **Foundation, Not Framework**: We intentionally exclude components like web servers, ORMs, and message queues. `provide.foundation` sits *below* your framework of choice (like FastAPI or Django), providing a consistent operational layer.
3.  **Developer Experience First**: APIs are designed to be ergonomic, intuitive, and require minimal boilerplate. Features like auto-discovery of CLI commands and zero-config logging exemplify this.
4.  **Observability by Default**: The entire system is built around the concept of structured logging and telemetry, making applications observable from day one.

## The Hub: The Architectural Core

The central architectural pattern is the **Hub** (`provide.foundation.hub.Hub`). It acts as a combined **service locator** and **dependency injection container**.

-   **Registry**: The Hub contains a multi-dimensional `Registry` that stores and categorizes application components (e.g., CLI commands, services, configuration).
-   **Component Lifecycle**: The Hub manages the lifecycle of registered components.
-   **Discovery**: It can automatically discover components, such as CLI commands decorated with `@register_command`.

## Key Design Decisions

### Why `attrs` over `pydantic`?

The framework uses `attrs` for its data classes due to its focus on performance, immutability, and simplicity. While `pydantic` is excellent for data validation (especially for APIs), `attrs` provides a lightweight and highly performant foundation for the framework's internal data structures.

### Global State vs. Dependency Injection

`provide.foundation` uses a pragmatic hybrid approach:
-   **Global Access (Service Locator):** Core infrastructure like the global `logger` and `get_hub()` function are available globally. This is for convenience and to solve the bootstrapping problem for cross-cutting concerns.
-   **Dependency Injection:** The `Hub` also functions as a `Container` that can resolve dependencies for your application's business logic, promoting testability and explicit dependencies where it matters most.

### Threading Model (`threading.RLock`)

The core `Registry` uses a `threading.RLock` for thread safety. This was an intentional choice to ensure that the framework works seamlessly in both synchronous and asynchronous contexts without depending on an active `asyncio` event loop. For the vast majority of applications, the performance impact is negligible. In ultra-high-throughput async applications that frequently modify the registry at runtime, this could become a bottleneck, but such use cases are rare.
"""
    )
    (path / "dependency-injection.md").write_text(
        """
# Explanation: Dependency Injection

`provide.foundation` supports two complementary patterns for managing dependencies:

1.  **Service Locator Pattern** - Simple, global access for framework infrastructure.
2.  **Dependency Injection (DI) Pattern** - Explicit, testable dependencies for application code.

This hybrid approach provides the convenience of a service locator for cross-cutting concerns (like logging) and the explicitness of DI for your core business logic.

## When to Use Which Pattern

-   **Use Service Locator for:** Framework infrastructure (`logger`, `config`), simple scripts, and situations where passing dependencies is impractical (e.g., third-party library callbacks).
-   **Use Dependency Injection for:** Your application's business logic (services, repositories), components that require unit testing, and at the "Composition Root" of your application (e.g., `main.py`).

## Service Locator in Practice

The service locator pattern is what you use when you import global objects.

```python
from provide.foundation import logger, get_hub

# Global logger access (Service Locator)
logger.info("Processing request")

# Global hub access (Service Locator)
hub = get_hub()
db_connection = hub.get_component("database")
```

**Pros:** Simple, convenient, lazy initialization.
**Cons:** Hidden dependencies, can complicate testing if overused.

## Dependency Injection in Practice

The DI pattern makes dependencies explicit through constructor parameters. The `Hub` can act as a DI container to automatically resolve these dependencies.

```python
from provide.foundation.hub import Hub, injectable

# Mark your classes as injectable
@injectable
class DatabaseClient:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        # ... connection logic ...

@injectable
class UserRepository:
    # Dependencies are declared in the constructor
    def __init__(self, db: DatabaseClient, logger: Logger):
        self.db = db
        self.logger = logger

    def find_user(self, user_id: int):
        self.logger.info("Finding user", user_id=user_id)
        # ... database query logic ...

# At your application's entry point (Composition Root)
def main():
    hub = Hub()

    # Register concrete instances of your dependencies
    hub.register(DatabaseClient, DatabaseClient("postgresql://..."))
    hub.register(Logger, logger) # Can register the global logger

    # The container automatically injects the dependencies
    user_repo = hub.resolve(UserRepository)
    user_repo.find_user(42)

if __name__ == "__main__":
    main()```
**Pros:** Explicit dependencies, highly testable, modular.
**Cons:** More verbose, requires setup at the Composition Root.

By using DI for your business logic, you make your code easier to test, refactor, and reason about, while still benefiting from the convenience of the service locator for shared infrastructure.
"""
    )


# ==============================================================================
# Section: API Reference
# ==============================================================================

def create_reference(path: Path):
    """Generates the 'API Reference' section."""
    path.mkdir()
    (path / "index.md").write_text(
        """
# API Reference

This section provides a detailed, auto-generated reference for every public module, class, and function in the `provide.foundation` library.

Use the navigation on the left to browse the API by module.
"""
    )

    # This script generates the markdown files for the API reference.
    (path / "gen_ref_pages.py").write_text(
        r'''
"""Generate the API reference pages for mkdocs."""

from pathlib import Path
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()
src_root = Path("src/provide/foundation")

for path in sorted(src_root.rglob("*.py")):
    module_path = path.relative_to(src_root).with_suffix("")
    doc_path = path.relative_to(src_root).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    # Skip private modules and empty __init__.py files
    if any(part.startswith("_") for part in parts if part != "__init__"):
        continue
    if path.name == "__init__.py" and path.read_text().strip() == "":
        continue

    # Create a navigation entry
    nav_parts = parts
    if parts[-1] == "__init__":
        nav_parts = parts[:-1]
        full_doc_path = full_doc_path.with_name("index.md")
    nav[nav_parts] = doc_path.as_posix()

    # Create the markdown file
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = "provide.foundation." + ".".join(parts)
        print(f"::: {identifier}", file=fd)

    # Add an edit path
    mkdocs_gen_files.set_edit_path(full_doc_path, "src" / path.relative_to("."))

# Create the navigation file
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
'''
    )


# ==============================================================================
# Section: Specifications (for future/unimplemented features)
# ==============================================================================

def create_specs(path: Path):
    """Generates the 'Specifications' section for forward-looking designs."""
    path.mkdir()
    (path / "index.md").write_text(
        """
# Design Specifications

!!! warning "Forward-Looking Information"
    The documents in this section are **design specifications** for planned or future features. They do **not** represent the current state of the library. They are provided for architectural review and to give insight into the project's roadmap.
"""
    )
    (path / "profiling-system.md").write_text(
        """
# Spec: Enterprise Profiling System

!!! info "Planned Enterprise Feature"
    This document specifies a planned enterprise-grade profiling system. The core infrastructure exists, but features like adaptive sampling, decorators, and advanced exporters are not yet implemented.

## Overview

The profiling system will provide lightweight, production-ready performance monitoring with zero-config defaults and enterprise-grade extensibility.

## Core Components

1.  **`ProfilingComponent`**: A Hub-managed component that controls the profiling lifecycle (`enable`, `disable`, `reset`).
2.  **`ProfilingProcessor`**: A `structlog` processor that collects performance metrics from log events based on a sample rate.
3.  **`ProfileMetrics`**: A data class that stores and calculates key metrics like throughput, latency, and overhead.

## Planned Enterprise Features

-   **Decorator-Based Tracking**: Decorators like `@profile_function` and `@profile_async` to automatically monitor function and method performance without manual instrumentation.
-   **Adaptive Sampling**: Intelligent sampling that automatically adjusts collection rates based on system load, error rates, and other real-time patterns to minimize overhead.
-   **Exporter Abstraction**: A universal exporter interface to seamlessly integrate with monitoring backends like Prometheus, Datadog, and OpenTelemetry.
-   **Advanced Configuration**: Granular control over memory tracking, buffering, batching, and security (e.g., data sanitization).

## Example Future Usage (Decorator)

```python
# This is a future, unimplemented feature
from provide.foundation.profiling.decorators import profile_async

@profile_async(
    name="api.get_user",
    track_memory=True,
    sample_rate=0.1 # 10% sampling for this specific function
)
async def get_user(user_id: int):
    # This function's execution time, memory usage, and call count
    # would be automatically tracked.
    user = await db.fetch_user(user_id)
    return user
```
"""
    )
    (path / "plugin-system.md").write_text(
        """
# Spec: Automatic Plugin Discovery

!!! info "Planned Feature"
    This document specifies the design for enabling automatic plugin discovery and dependency injection. The underlying discovery mechanism exists but is not yet automatically invoked by the Hub.

## Overview

The goal is to enhance the existing `Hub` and `Registry` to automatically discover and load components from installed packages via entry points, providing a zero-config plugin experience.

## Proposed Architecture

1.  **Auto-Discovery in Hub**: The `Hub.initialize_foundation()` method will be updated to scan for standard entry point groups (e.g., `provide.foundation.components`).
2.  **Dependency Injection**: The `Hub` will be enhanced with a `resolve()` method that can instantiate classes and automatically inject their dependencies (registered in the Hub) via their constructor's type hints.
3.  **Decorator Enhancements**: Decorators like `@component` and `@resource` will be introduced to declaratively register classes with the Hub and mark them for auto-discovery.

## Example Future Usage

```python
# --- In a plugin package's pyproject.toml ---
[project.entry-points."provide.foundation.components"]
my_plugin_service = "my_plugin.services:MyPluginService"

# --- In my_plugin/services.py ---
from provide.foundation.hub.decorators import component
from provide.foundation.hub.injection import inject

@component
class MyPluginService:
    # Dependencies will be auto-injected by the Hub
    def __init__(self, db: DatabaseClient, logger: Logger = inject()):
        self.db = db
        self.logger = logger

    def run(self):
        self.logger.info("Plugin service is running!")

# --- In the main application ---
from provide.foundation.hub import get_hub

hub = get_hub()
hub.initialize_foundation() # This will auto-discover and register MyPluginService

# The Hub can now resolve the plugin service with its dependencies
plugin_service = hub.resolve(MyPluginService)
plugin_service.run()
```
"""
    )


if __name__ == "__main__":
    output_directory = sys.argv[1] if len(sys.argv) > 1 else "docs_generated"
    main(output_directory)