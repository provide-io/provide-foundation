# File Operations Guide

File system utilities and operations.

## Overview

The provide.foundation library includes utilities for:

- **Directory Management** - Creating, listing, and managing directories
- **File Operations** - Reading, writing, and manipulating files
- **Path Handling** - Cross-platform path operations
- **Async File I/O** - Non-blocking file operations

## Common Patterns

### Directory Operations

```python
from provide.foundation.file import directory

# List directory contents
contents = await directory.list_async('/path/to/directory')

# Create directory with parents
await directory.ensure_async('/path/to/new/directory')
```

### File Operations

```python
from provide.foundation.file import operations

# Read file content
content = await operations.read_async('/path/to/file.txt')

# Write file content
await operations.write_async('/path/to/file.txt', content)
```