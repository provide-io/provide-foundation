# File Watching

Learn how to monitor files and directories for changes in real-time.

## Overview

Foundation provides file watching capabilities to detect when files are created, modified, or deleted.

## Basic File Watching

```python
from provide.foundation.file.operations import FileOperationDetector
from provide.foundation import logger

async def watch_config():
    """Watch configuration file for changes."""
    detector = FileOperationDetector()

    async for event in detector.watch("config.yaml"):
        logger.info(
            "config_changed",
            file=event.file_path,
            operation=event.operation_type
        )
        # Reload configuration
        reload_config()
```

## Watch Multiple Files

```python
files_to_watch = [
    "config.yaml",
    "secrets.env",
    "database.json"
]

async for event in detector.watch_multiple(files_to_watch):
    logger.info("file_changed", file=event.file_path)
    handle_change(event)
```

## Watch Directory

```python
async def watch_directory():
    """Watch all files in a directory."""
    detector = FileOperationDetector()

    async for event in detector.watch_directory("./config"):
        if event.operation_type == "created":
            logger.info("new_file", file=event.file_path)
        elif event.operation_type == "modified":
            logger.info("file_updated", file=event.file_path)
        elif event.operation_type == "deleted":
            logger.warning("file_removed", file=event.file_path)
```

## Filter by File Type

```python
from pathlib import Path

async def watch_yaml_files():
    """Watch only YAML files."""
    detector = FileOperationDetector()

    async for event in detector.watch_directory("./"):
        path = Path(event.file_path)
        if path.suffix in [".yaml", ".yml"]:
            logger.info("yaml_changed", file=path.name)
            process_yaml(path)
```

## Debouncing Changes

Handle rapid successive changes:

```python
import asyncio
from collections import defaultdict

async def watch_with_debounce():
    """Debounce file changes to avoid processing too frequently."""
    detector = FileOperationDetector()
    pending_changes = defaultdict(asyncio.Event)

    async def process_after_delay(file_path: str):
        """Process file after 500ms of no changes."""
        await asyncio.sleep(0.5)
        logger.info("processing_file", file=file_path)
        process_file(file_path)

    async for event in detector.watch_directory("./watched"):
        # Cancel pending task if exists
        if event.file_path in pending_changes:
            pending_changes[event.file_path].set()

        # Start new debounced task
        event = asyncio.Event()
        pending_changes[event.file_path] = event
        asyncio.create_task(process_after_delay(event.file_path))
```

## Streaming File Detection

Detect when files are being actively written:

```python
async def detect_streaming():
    """Detect when files are being streamed/written."""
    detector = FileOperationDetector()

    async for event in detector.detect_streaming_operations("logfile.txt"):
        if event.is_streaming:
            logger.debug("file_being_written", file=event.file_path)
        else:
            logger.info("file_write_complete", file=event.file_path)
            # Safe to process now
            process_complete_file(event.file_path)
```

## Hot Reload Pattern

Automatically reload configuration on changes:

```python
from provide.foundation.file.operations import FileOperationDetector
from provide.foundation.serialization import provide_loads
from pathlib import Path

class ConfigWatcher:
    def __init__(self, config_file: str):
        self.config_file = Path(config_file)
        self.config = {}
        self.detector = FileOperationDetector()

    async def start(self):
        """Start watching and reload on changes."""
        # Load initial config
        self.reload()

        # Watch for changes
        async for event in self.detector.watch(self.config_file):
            logger.info("config_reloaded")
            self.reload()

    def reload(self):
        """Reload configuration from file."""
        content = self.config_file.read_text()
        self.config = provide_loads(content)

# Usage
watcher = ConfigWatcher("config.json")
asyncio.run(watcher.start())
```

## Stop Watching

```python
detector = FileOperationDetector()

# Watch in background task
watch_task = asyncio.create_task(
    watch_files(detector)
)

# Later, stop watching
watch_task.cancel()
await detector.stop()
```

## Next Steps

- **[Atomic Writes](atomic-writes.md)** - Safe file writes
- **[API Reference: File Operations](../../reference/provide/foundation/file/operations/index.md)** - Complete file operations API

---

**See also:** [examples/file_operations/02_streaming_detection.py](https://github.com/provide-io/provide-foundation/blob/main/examples/file_operations/02_streaming_detection.py)
