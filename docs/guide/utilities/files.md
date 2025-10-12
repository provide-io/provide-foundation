# File Operations Guide

File system utilities and operations.

## Overview

The `provide.foundation` library includes utilities for:

- **Atomic Operations** - Safely writing and replacing files
- **Directory Management** - Creating, listing, and managing directories
- **File Formats** - Reading and writing JSON, YAML, and TOML files
- **Safe Operations** - Safely reading, deleting, moving, and copying files
- **Temporary Files** - Creating and managing temporary files and directories

## Atomic Operations

### Atomic Write

Atomically write data to a file. This ensures that the file is never left in a partially written state, even if the application crashes.

```python
from provide.foundation.file.atomic import atomic_write

atomic_write("my-file.txt", b"Hello, World!")
```

## Directory Management

### Ensure Directory Exists

Ensure that a directory exists, creating it if necessary.

```python
from provide.foundation.file.directory import ensure_dir

ensure_dir("/path/to/my/directory")
```

## File Formats

### JSON

Read and write JSON files.

```python
from provide.foundation.file.formats import read_json, write_json

data = {"key": "value"}
write_json("my-file.json", data)

read_data = read_json("my-file.json")
```

### YAML

Read and write YAML files.

```python
from provide.foundation.file.formats import read_yaml, write_yaml

data = {"key": "value"}
write_yaml("my-file.yaml", data)

read_data = read_yaml("my-file.yaml")
```

### TOML

Read and write TOML files.

```python
from provide.foundation.file.formats import read_toml, write_toml

data = {"key": "value"}
write_toml("my-file.toml", data)

read_data = read_toml("my-file.toml")
```

## Safe Operations

### Safe Read

Safely read the contents of a file.

```python
from provide.foundation.file.safe import safe_read

data = safe_read("my-file.txt")
```

### Safe Delete

Safely delete a file.

```python
from provide.foundation.file.safe import safe_delete

safe_delete("my-file.txt")
```

## Temporary Files

### Temporary File

Create a temporary file.

```python
from provide.foundation.file.temp import temp_file

with temp_file() as f:
    f.write(b"Hello, World!")
    f.seek(0)
    data = f.read()
```

### Temporary Directory

Create a temporary directory.

```python
from provide.foundation.file.temp import temp_dir

with temp_dir() as d:
    # ...
```