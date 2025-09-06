"""Generate the API reference pages."""

from pathlib import Path

import mkdocs_gen_files

# Map module paths to documentation paths
nav = mkdocs_gen_files.Nav()

# Source root for provide.foundation
src_root = Path("src")

# Process all Python files in the source tree
for path in sorted(src_root.rglob("*.py")):
    # Skip __pycache__ and test files
    if "__pycache__" in str(path) or "test" in path.name:
        continue

    # Skip __init__.py files that are empty or just imports
    if path.name == "__init__.py" and path.stat().st_size < 100:
        continue

    # Convert path to module path
    module_path = path.relative_to(src_root).with_suffix("")

    # Convert to documentation path
    doc_path = Path("api", "reference") / module_path.with_suffix(".md")

    # Calculate full module name
    full_doc_path = Path("api", "reference") / module_path.with_suffix(".md")

    parts = tuple(module_path.parts)

    # Skip private modules (starting with _)
    if any(part.startswith("_") and part != "__init__" for part in parts):
        continue

    # Add to navigation
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")

    nav[parts] = doc_path.as_posix()

    # Generate the markdown file with mkdocstrings reference
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print(f"::: {identifier}", file=fd)

    # Set edit path for the generated file
    mkdocs_gen_files.set_edit_path(full_doc_path, Path("src") / path.relative_to(src_root))

# Create the SUMMARY.md file for literate-nav
with mkdocs_gen_files.open("api/reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

# Create index files for main API sections
api_index_content = """# API Reference

## Core Modules

The core modules provide the fundamental functionality of provide.foundation.

### Logger and Telemetry
- [`provide.foundation.logger`](reference/provide/foundation/logger/index.md) - Structured logging system
- [`provide.foundation.telemetry`](reference/provide/foundation/telemetry/index.md) - Telemetry configuration

### Configuration
- [`provide.foundation.config`](reference/provide/foundation/config/index.md) - Configuration management
- [`provide.foundation.env`](reference/provide/foundation/env/index.md) - Environment variable handling

### CLI Framework
- [`provide.foundation.cli`](reference/provide/foundation/cli/index.md) - Command-line interface framework
- [`provide.foundation.cli.decorators`](reference/provide/foundation/cli/decorators.md) - CLI decorators

### System Utilities
- [`provide.foundation.platform`](reference/provide/foundation/platform/index.md) - Platform detection
- [`provide.foundation.process`](reference/provide/foundation/process/index.md) - Process execution
- [`provide.foundation.console`](reference/provide/foundation/console/index.md) - Console output

### Registry and Hub
- [`provide.foundation.registry`](reference/provide/foundation/registry/index.md) - Object registry pattern
- [`provide.foundation.hub`](reference/provide/foundation/hub/index.md) - Component hub

### Error Handling
- [`provide.foundation.errors`](reference/provide/foundation/errors/index.md) - Error handling utilities

## Emoji Sets

Emoji sets provide domain-specific logging capabilities:

- [`provide.foundation.emoji_sets`](reference/provide/foundation/emoji_sets.md) - Base emoji set system
- HTTP Layer - Web request/response logging
- Database Layer - Database query logging
- LLM Layer - Language model interaction logging

## Usage Examples

### Basic Logging

```python
from provide.foundation import logger

logger.info("Application started", version="1.0.0")
logger.debug("Processing request", request_id="abc123")
logger.error("Failed to connect", error="Connection timeout")
```

### CLI Application

```python
from provide.foundation.cli import register_command

@register_command("hello")
def hello_command(name: str = "World"):
    \"\"\"Say hello to someone.\"\"\"
    print(f"Hello, {name}!")
```

### Configuration Management

```python
from provide.foundation.config import Config

config = Config.from_env()
print(f"Debug mode: {config.debug}")
```

## Module Index

Browse the complete API documentation by module:
"""

with mkdocs_gen_files.open("api/reference/index.md", "w") as f:
    f.write(api_index_content)
