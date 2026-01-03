# File Operations Examples

This directory contains examples demonstrating how to use the provide-foundation file operations module for intelligent detection and analysis of file system events.

## Overview

The file operations module provides sophisticated detection of file operation patterns, converting low-level filesystem events into higher-level semantic operations like:

- **Atomic saves** (VSCode, Sublime Text patterns)
- **Safe writes** with backup creation
- **Batch operations** (code formatters, build tools)
- **Rename sequences**
- **Backup creation**

## Examples

### 1. Basic Usage (`01_basic_usage.py`)

**Purpose**: Introduction to core concepts and basic API usage.

**What it demonstrates**:
- Temporary file pattern detection
- Creating and analyzing file events
- Custom detector configuration
- Working with real files

**Key concepts**:
```python
from provide.foundation.file.operations import (
    OperationDetector,
    FileEvent,
    FileEventMetadata,
    is_temp_file,
    extract_original_path
)

# Detect temp files
is_temp = is_temp_file(Path("document.txt.tmp.12345"))

# Analyze events
detector = OperationDetector()
operations = detector.detect(events)
```

**Run with**: `python 01_basic_usage.py`

### 2. Streaming Detection (`02_streaming_detection.py`)

**Purpose**: Real-time event processing for continuous monitoring.

**What it demonstrates**:
- Streaming vs batch processing
- Time-window based flushing
- Async-compatible processing
- Handling event sequences

**Key concepts**:
```python
# Process events as they arrive
operation = detector.detect_streaming(event)

# Flush pending operations after timeout
pending_ops = detector.flush()
```

**Run with**: `python 02_streaming_detection.py`

### 3. Real Filesystem Monitoring (`03_real_filesystem_monitoring.py`)

**Purpose**: Integration with watchdog for actual filesystem monitoring.

**What it demonstrates**:
- Watchdog integration
- Converting filesystem events to FileEvents
- Real editor save pattern simulation
- Production-focused monitoring setup

**Key concepts**:
```python
class FileOperationMonitor(FileSystemEventHandler):
    def on_created(self, event):
        file_event = self._create_file_event(event, "created")
        operation = self.detector.detect_streaming(file_event)
```

**Requirements**: `uv add watchdog`
**Run with**: `python 03_real_filesystem_monitoring.py`

## Common Patterns

### Basic Operation Detection

```python
from provide.foundation.file.operations import OperationDetector, OperationType

detector = OperationDetector()
operations = detector.detect(events)

for operation in operations:
    if operation.operation_type == OperationType.ATOMIC_SAVE:
        print(f"Atomic save detected: {operation.primary_path}")
```

### Custom Configuration

```python
from provide.foundation.file.operations import DetectorConfig

config = DetectorConfig(
    time_window_ms=200,      # Shorter time window
    min_confidence=0.8,      # Higher confidence threshold
    min_events_for_complex=3 # Minimum events for batch operations
)

detector = OperationDetector(config)
```

### Streaming Processing

```python
# For real-time monitoring
operation = detector.detect_streaming(event)
if operation:
    print(f"Operation detected: {operation.operation_type.value}")

# Periodically flush pending operations
pending_operations = detector.flush()
```

## Operation Types

The detector can identify these operation types:

| Type | Description | Example |
|------|-------------|---------|
| `ATOMIC_SAVE` | Atomic file replacement via temp file | VSCode save pattern |
| `SAFE_WRITE` | Write with backup creation | Editor with backup |
| `BATCH_UPDATE` | Multiple files changed rapidly | Code formatter |
| `RENAME_SEQUENCE` | Chain of file renames | File reorganization |
| `BACKUP_CREATE` | Backup file creation | Manual backup |

## Editor Patterns Detected

### VSCode/Sublime Text
```
1. Create: document.txt.tmp.12345
2. Move: document.txt.tmp.12345 → document.txt
```

### Vim/Emacs
```
1. Delete: document.txt
2. Create: document.txt~ (backup)
3. Create: document.txt (new content)
```

### Safe Write
```
1. Create: document.txt.bak
2. Modify: document.txt
```

## Rich Metadata

Each FileEvent includes comprehensive metadata:

```python
metadata = FileEventMetadata(
    timestamp=datetime.now(),
    sequence_number=1,
    size_before=100,
    size_after=200,
    permissions=0o644,
    process_name="vscode",
    process_id=1234,
    user="developer",
    extra={"custom": "data"}
)
```

## Performance Considerations

- **Time Windows**: Shorter windows (100-200ms) for responsive detection
- **Confidence Thresholds**: Higher thresholds (0.8+) for fewer false positives
- **Streaming vs Batch**: Use streaming for real-time, batch for analysis
- **Event Filtering**: Filter directory events and irrelevant files

## Integration Examples

### With File Watchers
```python
class MyFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.detector = OperationDetector()

    def on_any_event(self, event):
        if not event.is_directory:
            file_event = self.convert_event(event)
            operation = self.detector.detect_streaming(file_event)
            if operation:
                self.handle_operation(operation)
```

### With Async Frameworks
```python
async def process_file_events(event_stream):
    detector = OperationDetector()

    async for event in event_stream:
        operation = detector.detect_streaming(event)
        if operation:
            await handle_operation(operation)
```

## Testing

The examples include test scenarios that verify:
- ✅ Atomic save detection (VSCode pattern)
- ✅ Backup-based saves (Vim pattern)
- ✅ Batch operations (formatters)
- ✅ Safe writes with backups
- ✅ Rename sequences
- ✅ Streaming vs batch processing
- ✅ Real filesystem integration

Run the integration tests with:
```bash
cd /path/to/provide-foundation
pytest tests/test_file_operations_integration.py -v
```