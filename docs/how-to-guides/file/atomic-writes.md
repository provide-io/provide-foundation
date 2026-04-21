# Atomic File Writes

Learn how to safely write files with atomic operations to prevent data corruption.

## Overview

Atomic writes ensure that file operations either complete fully or not at all, preventing partial writes and corruption.

## Basic Atomic Write

```python
from provide.foundation.file import atomic_write

# Write safely - creates temp file, then renames
atomic_write(
    path="config.json",
    content='{"setting": "value"}'
)

# If interrupted, original file is unchanged
# If successful, original is replaced atomically
```

## Atomic Write with Path Object

```python
from pathlib import Path
from provide.foundation.file import atomic_write

config_file = Path("config.json")

atomic_write(
    path=config_file,
    content='{"updated": true}'
)
```

## Binary File Writes

```python
# Write binary data atomically
image_data = b'\x89PNG\r\n\x1a\n...'

atomic_write(
    path="image.png",
    content=image_data,
    mode="wb"
)
```

## Atomic JSON Write

```python
from provide.foundation.serialization import provide_dumps
from provide.foundation.file import atomic_write

data = {
    "users": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
}

# Serialize and write atomically
atomic_write(
    path="users.json",
    content=provide_dumps(data, indent=2)
)
```

## Create Parent Directories

```python
# Automatically create parent directories
atomic_write(
    path="data/config/settings.json",
    content='{"key": "value"}',
    create_parents=True
)
```

## Preserve File Permissions

```python
import os

# Set specific permissions
atomic_write(
    path="secrets.txt",
    content="secret_data",
    mode="w",
    permissions=0o600  # Only owner can read/write
)
```

## Atomic Update Pattern

Safe read-modify-write:

```python
from pathlib import Path
from provide.foundation.serialization import provide_loads, provide_dumps
from provide.foundation.file import atomic_write

def update_config(key: str, value: str):
    """Safely update a single config value."""
    config_file = Path("config.json")

    # Read current config
    if config_file.exists():
        config = provide_loads(config_file.read_text())
    else:
        config = {}

    # Modify
    config[key] = value

    # Write atomically
    atomic_write(
        path=config_file,
        content=provide_dumps(config, indent=2)
    )
```

## Why Atomic Writes Matter

**Without atomic writes:**
```python
# ❌ Dangerous - can corrupt file if interrupted
with open("config.json", "w") as f:
    f.write('{"partial":')  # If crash happens here...
    f.write(' "data"}')     # ...file is corrupted
```

**With atomic writes:**
```python
# ✅ Safe - original file unchanged until write completes
atomic_write(
    path="config.json",
    content='{"complete": "data"}'
)
# Original file only replaced when write is complete
```

## Error Handling

```python
from provide.foundation.file import atomic_write
from provide.foundation.errors import FileOperationError

try:
    atomic_write(
        path="/readonly/file.txt",
        content="data"
    )
except FileOperationError as e:
    logger.error("write_failed", error=str(e))
```

## Next Steps

- **[File Watching](watching.md)** - Monitor file changes
- **[API Reference: File](../../reference/provide/foundation/file/index.md)** - Complete file API

---

**See also:** [examples/file_operations/01_basic_usage.py](https://github.com/provide-io/provide-foundation/blob/main/examples/file_operations/01_basic_usage.py)
