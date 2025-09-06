# File

::: provide.foundation.file

## Overview

The file module provides comprehensive file operations with safety, atomicity, and format support. It's designed to handle common file operations robustly, preventing corruption and data loss through atomic operations, safe error handling, and proper locking mechanisms.

## Key Features

- **Atomic Operations**: Prevent file corruption with temp-file-and-rename pattern
- **Safe Operations**: Error-resistant file operations with graceful fallbacks
- **Format Support**: Native support for JSON, YAML, TOML formats
- **Directory Management**: Safe directory creation and cleanup
- **File Locking**: Prevent concurrent access conflicts
- **Comprehensive Utilities**: Backup, touch, find, and more

## Quick Start

```python
from provide.foundation.file import (
    atomic_write_text, safe_read_text, ensure_dir, 
    read_json, write_json, FileLock
)

# Atomic file writing
atomic_write_text("config.txt", "configuration data")

# Safe file reading with defaults
content = safe_read_text("config.txt", default="default content")

# Directory management
ensure_dir("logs/daily")

# JSON operations
data = {"key": "value"}
write_json("data.json", data)
loaded = read_json("data.json", default={})

# File locking
with FileLock("shared_resource.txt"):
    # Safe concurrent access
    content = safe_read_text("shared_resource.txt")
```

## API Reference

### Atomic Operations

Atomic operations use the temp-file-and-rename pattern to ensure file operations are either complete or not performed at all.

#### `atomic_write(path, data, mode=None, backup=False, preserve_mode=True)`

Write binary data to file atomically.

**Parameters:**
- `path` (str | Path): Target file path
- `data` (bytes): Binary data to write
- `mode` (int, optional): File permissions (e.g., 0o644)
- `backup` (bool): Create .bak file before overwrite (default: False)
- `preserve_mode` (bool): Preserve existing file permissions (default: True)

**Example:**
```python
from provide.foundation.file import atomic_write

data = b"binary configuration data"
atomic_write("config.bin", data, mode=0o600, backup=True)
```

#### `atomic_write_text(path, content, encoding="utf-8", mode=None, backup=False)`

Write text to file atomically.

**Parameters:**
- `path` (str | Path): Target file path
- `content` (str): Text content to write
- `encoding` (str): Text encoding (default: "utf-8")
- `mode` (int, optional): File permissions
- `backup` (bool): Create backup before overwrite

**Example:**
```python
from provide.foundation.file import atomic_write_text

content = "application configuration\nkey=value\n"
atomic_write_text("app.conf", content, backup=True)
```

#### `atomic_replace(source_path, target_path, backup=False)`

Atomically replace target file with source file.

**Parameters:**
- `source_path` (str | Path): Source file to move
- `target_path` (str | Path): Target location
- `backup` (bool): Create backup of target before replace

**Example:**
```python
from provide.foundation.file import atomic_replace

# Safe config update workflow
atomic_write_text("new_config.tmp", new_config)
atomic_replace("new_config.tmp", "config.txt", backup=True)
```

### Safe Operations

Safe operations include error handling and graceful fallbacks.

#### `safe_read(path, default=b"", encoding=None)`

Read file safely with default fallback.

**Parameters:**
- `path` (str | Path): File path to read
- `default` (bytes): Default value if read fails (default: b"")
- `encoding` (str, optional): If provided, decode bytes to string

**Returns:**
- `bytes | str`: File content or default value

#### `safe_read_text(path, default="", encoding="utf-8")`

Read text file safely with default fallback.

**Parameters:**
- `path` (str | Path): File path to read
- `default` (str): Default value if read fails (default: "")
- `encoding` (str): Text encoding (default: "utf-8")

**Returns:**
- `str`: File content or default value

**Example:**
```python
from provide.foundation.file import safe_read_text

# Safe config reading with defaults
config = safe_read_text("app.conf", default="# Default config\n")
log_content = safe_read_text("app.log", default="")
```

#### `safe_copy(source, destination, overwrite=False)`

Copy file safely with error handling.

**Parameters:**
- `source` (str | Path): Source file path
- `destination` (str | Path): Destination file path
- `overwrite` (bool): Allow overwriting existing files

**Example:**
```python
from provide.foundation.file import safe_copy

# Backup important file
safe_copy("database.db", "backup/database.db.backup")
```

#### `safe_move(source, destination, overwrite=False)`

Move/rename file safely.

**Parameters:**
- `source` (str | Path): Source file path
- `destination` (str | Path): Destination file path
- `overwrite` (bool): Allow overwriting existing files

#### `safe_delete(path, ignore_missing=True)`

Delete file safely.

**Parameters:**
- `path` (str | Path): File path to delete
- `ignore_missing` (bool): Don't raise error if file doesn't exist

### Directory Management

#### `ensure_dir(path, mode=0o755, parents=True)`

Ensure directory exists, creating it if necessary.

**Parameters:**
- `path` (str | Path): Directory path
- `mode` (int): Directory permissions (default: 0o755)
- `parents` (bool): Create parent directories (default: True)

**Example:**
```python
from provide.foundation.file import ensure_dir

# Ensure log directory exists
ensure_dir("logs/application/daily")
ensure_dir("/tmp/myapp", mode=0o700)
```

#### `ensure_parent_dir(filepath, mode=0o755)`

Ensure parent directory of a file exists.

**Parameters:**
- `filepath` (str | Path): File path whose parent directory to create
- `mode` (int): Directory permissions (default: 0o755)

**Example:**
```python
from provide.foundation.file import ensure_parent_dir, atomic_write_text

# Ensure directory structure exists before writing
ensure_parent_dir("logs/app/2024/app.log")
atomic_write_text("logs/app/2024/app.log", log_data)
```

#### `safe_rmtree(path, ignore_errors=True)`

Safely remove directory tree.

**Parameters:**
- `path` (str | Path): Directory path to remove
- `ignore_errors` (bool): Ignore errors during removal

#### `temp_dir(prefix="tmp", cleanup=True)`

Create temporary directory with context manager.

**Parameters:**
- `prefix` (str): Directory name prefix
- `cleanup` (bool): Automatically cleanup on exit

**Returns:**
- Context manager yielding Path object

**Example:**
```python
from provide.foundation.file import temp_dir

with temp_dir(prefix="processing") as tmpdir:
    work_file = tmpdir / "work.txt"
    atomic_write_text(work_file, "temporary processing data")
    # Directory automatically cleaned up
```

### Format-Specific Operations

#### JSON Operations

##### `read_json(path, default=None, encoding="utf-8")`

Read JSON file with error handling.

**Parameters:**
- `path` (str | Path): JSON file path
- `default` (Any): Default value if read fails
- `encoding` (str): Text encoding

**Returns:**
- `Any`: Parsed JSON data or default value

##### `write_json(path, data, indent=2, encoding="utf-8", atomic=True)`

Write data to JSON file.

**Parameters:**
- `path` (str | Path): JSON file path
- `data` (Any): Data to serialize as JSON
- `indent` (int): JSON indentation (default: 2)
- `encoding` (str): Text encoding
- `atomic` (bool): Use atomic write (default: True)

**Example:**
```python
from provide.foundation.file import read_json, write_json

# Write JSON configuration
config = {
    "database": {"host": "localhost", "port": 5432},
    "logging": {"level": "INFO"},
    "features": ["auth", "metrics"]
}
write_json("config.json", config)

# Read with fallback
config = read_json("config.json", default={"logging": {"level": "WARNING"}})
```

#### YAML Operations

##### `read_yaml(path, default=None, encoding="utf-8")`

Read YAML file with error handling.

**Parameters:**
- `path` (str | Path): YAML file path
- `default` (Any): Default value if read fails
- `encoding` (str): Text encoding

##### `write_yaml(path, data, encoding="utf-8", atomic=True)`

Write data to YAML file.

**Parameters:**
- `path` (str | Path): YAML file path
- `data` (Any): Data to serialize as YAML
- `encoding` (str): Text encoding
- `atomic` (bool): Use atomic write (default: True)

**Example:**
```python
from provide.foundation.file import read_yaml, write_yaml

# Write YAML configuration
config = {
    "server": {"host": "0.0.0.0", "port": 8000},
    "workers": 4
}
write_yaml("config.yaml", config)

# Read with defaults
config = read_yaml("config.yaml", default={"workers": 1})
```

#### TOML Operations

##### `read_toml(path, default=None, encoding="utf-8")`

Read TOML file with error handling.

**Parameters:**
- `path` (str | Path): TOML file path
- `default` (Any): Default value if read fails
- `encoding` (str): Text encoding

##### `write_toml(path, data, encoding="utf-8", atomic=True)`

Write data to TOML file.

**Parameters:**
- `path` (str | Path): TOML file path
- `data` (Any): Data to serialize as TOML
- `encoding` (str): Text encoding
- `atomic` (bool): Use atomic write (default: True)

### File Locking

#### `FileLock(filepath, timeout=10)`

File-based locking for concurrent access control.

**Parameters:**
- `filepath` (str | Path): Path to the lock file
- `timeout` (float): Maximum time to wait for lock (default: 10 seconds)

**Example:**
```python
from provide.foundation.file import FileLock, LockError

try:
    with FileLock("shared_resource.lock", timeout=5):
        # Critical section - only one process can execute this
        data = safe_read_text("shared_resource.txt")
        data += "new entry\n"
        atomic_write_text("shared_resource.txt", data)
except LockError:
    print("Could not acquire lock within timeout")
```

#### `LockError`

Exception raised when file lock cannot be acquired.

### Utility Functions

#### `find_files(directory, pattern="*", recursive=True, files_only=True)`

Find files matching pattern.

**Parameters:**
- `directory` (str | Path): Directory to search
- `pattern` (str): Glob pattern (default: "*")
- `recursive` (bool): Search subdirectories (default: True)
- `files_only` (bool): Return only files, not directories

**Returns:**
- `list[Path]`: List of matching file paths

**Example:**
```python
from provide.foundation.file import find_files

# Find all Python files
py_files = find_files("src", "*.py", recursive=True)

# Find config files
configs = find_files(".", "config.*", recursive=False)
```

#### `backup_file(filepath, suffix=".bak", timestamp=False)`

Create backup copy of file.

**Parameters:**
- `filepath` (str | Path): File to backup
- `suffix` (str): Backup file suffix (default: ".bak")
- `timestamp` (bool): Add timestamp to suffix

**Returns:**
- `Path`: Backup file path

**Example:**
```python
from provide.foundation.file import backup_file

# Simple backup
backup_path = backup_file("important.db")
# Creates important.db.bak

# Timestamped backup
backup_path = backup_file("config.json", timestamp=True)
# Creates config.json.bak.20240101_120000
```

#### `touch(filepath, mode=0o644)`

Create empty file or update modification time.

**Parameters:**
- `filepath` (str | Path): File path
- `mode` (int): File permissions for new files

#### `get_size(filepath)`

Get file size in bytes.

**Parameters:**
- `filepath` (str | Path): File path

**Returns:**
- `int`: File size in bytes

#### `get_mtime(filepath)`

Get file modification time as timestamp.

**Parameters:**
- `filepath` (str | Path): File path

**Returns:**
- `float`: Modification time timestamp

## Error Handling

The file module provides comprehensive error handling:

- **FileNotFoundError**: When files don't exist (handled gracefully by safe_* functions)
- **PermissionError**: When lacking file system permissions
- **OSError**: For general I/O errors
- **LockError**: When file locks cannot be acquired
- **json.JSONDecodeError**: For invalid JSON (handled by format functions)
- **yaml.YAMLError**: For invalid YAML (handled by format functions)

## Best Practices

### 1. Always Use Atomic Operations for Critical Files

```python
# Good: Atomic write prevents corruption
atomic_write_text("config.txt", new_config)

# Bad: Direct write can leave partial data
with open("config.txt", "w") as f:
    f.write(new_config)
```

### 2. Use Safe Operations with Defaults

```python
# Good: Graceful handling of missing files
config = read_json("config.json", default={"debug": False})

# Better: Safe reading with explicit defaults
content = safe_read_text("log.txt", default="")
```

### 3. Ensure Directories Before Writing

```python
# Good: Ensure path exists
ensure_parent_dir("logs/app/error.log")
atomic_write_text("logs/app/error.log", log_data)

# Better: Use higher-level functions
ensure_dir("logs/app")
```

### 4. Use Locking for Shared Resources

```python
# Good: Protect concurrent access
with FileLock("shared.txt.lock"):
    data = safe_read_text("shared.txt")
    # Modify data
    atomic_write_text("shared.txt", modified_data)
```

### 5. Handle Cleanup with Context Managers

```python
# Good: Automatic cleanup
with temp_dir(prefix="processing") as tmpdir:
    work_file = tmpdir / "temp.txt"
    atomic_write_text(work_file, data)
    # Process data
    # Directory cleaned up automatically
```

## Complete Examples

### Safe Configuration Management

```python
from provide.foundation.file import (
    read_json, write_json, backup_file, 
    atomic_write_text, ensure_parent_dir
)
import json

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.default_config = {
            "logging": {"level": "INFO"},
            "database": {"timeout": 30},
            "features": []
        }
    
    def load_config(self):
        """Load configuration with fallback to defaults."""
        return read_json(self.config_path, default=self.default_config.copy())
    
    def save_config(self, config):
        """Save configuration with backup."""
        ensure_parent_dir(self.config_path)
        
        # Create backup if file exists
        try:
            backup_file(self.config_path, timestamp=True)
        except FileNotFoundError:
            pass  # No existing file to backup
        
        # Atomic write ensures consistency
        write_json(self.config_path, config)
    
    def update_config(self, updates):
        """Safely update configuration."""
        config = self.load_config()
        config.update(updates)
        self.save_config(config)

# Usage
config_mgr = ConfigManager("config/app.json")
config_mgr.update_config({"logging": {"level": "DEBUG"}})
```

### Batch File Processing

```python
from provide.foundation.file import (
    find_files, atomic_write_text, safe_read_text,
    temp_dir, ensure_dir
)

def process_text_files(source_dir: str, output_dir: str):
    """Process all text files with backup and error handling."""
    
    # Find all text files
    text_files = find_files(source_dir, "*.txt", recursive=True)
    
    ensure_dir(output_dir)
    
    with temp_dir(prefix="processing") as tmpdir:
        processed_count = 0
        
        for file_path in text_files:
            try:
                # Safe read with default
                content = safe_read_text(file_path, default="")
                
                if not content.strip():
                    continue
                
                # Process content (example: add header)
                processed_content = f"# Processed file: {file_path.name}\n\n{content}"
                
                # Create output path
                output_path = Path(output_dir) / file_path.name
                
                # Atomic write to prevent corruption
                atomic_write_text(output_path, processed_content)
                processed_count += 1
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        print(f"Successfully processed {processed_count} files")

# Usage
process_text_files("documents", "processed_documents")
```

## Thread Safety

- **Atomic Operations**: Thread-safe by design
- **File Locks**: Explicitly handle concurrent access
- **Safe Operations**: Individual operations are atomic
- **Directory Operations**: Use appropriate locking for shared directories

## Performance Considerations

- **Large Files**: Use streaming operations where possible
- **Batch Operations**: Group multiple file operations
- **Temporary Files**: Clean up temporary files promptly
- **Lock Timeouts**: Use appropriate timeouts for locks

## See Also

- [Crypto Module](../crypto/api-index.md) - For file integrity verification
- [Context Module](../context/api-index.md) - For configuration management
- [Process Module](../process/api-index.md) - For external command execution
- [File Operations Guide](../../guide/utilities/files.md) - Usage patterns and examples