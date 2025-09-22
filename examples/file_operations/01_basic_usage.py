#!/usr/bin/env python3
# examples/file_operations/01_basic_usage.py
"""Basic usage of file operation detection for monitoring file changes."""

from datetime import datetime, timedelta
from pathlib import Path
import sys
import tempfile
import time

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation.file.operations import (  # noqa: E402
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    OperationDetector,
    extract_original_path,
    is_temp_file,
)


def main() -> None:
    """Demonstrate basic file operation detection."""
    print("🔍 File Operations - Basic Usage Example")
    print("=" * 50)

    # Example 1: Checking if files are temporary
    print("\n📁 Example 1: Temporary File Detection")
    test_files = [
        "document.txt",
        "document.txt.tmp.12345",
        "document.txt~",
        ".document.txt.swp",
        "#document.txt#",
        "document.txt.bak",
    ]

    for file_path in test_files:
        path = Path(file_path)
        is_temp = is_temp_file(path)
        status = "🟡 TEMP" if is_temp else "🟢 NORMAL"
        print(f"  {status}: {file_path}")

        if is_temp:
            original = extract_original_path(path)
            if original:
                print(f"    → Original: {original.name}")

    # Example 2: Creating and analyzing file events
    print("\n⚡ Example 2: Analyzing File Events")

    # Create some sample events (simulating VSCode atomic save)
    now = datetime.now()
    events = [
        FileEvent(
            path=Path("document.txt.tmp.12345"),
            event_type="created",
            metadata=FileEventMetadata(
                timestamp=now, sequence_number=1, size_after=1024, process_name="vscode"
            ),
        ),
        FileEvent(
            path=Path("document.txt.tmp.12345"),
            event_type="moved",
            metadata=FileEventMetadata(
                timestamp=now + timedelta(milliseconds=50), sequence_number=2, size_after=1024
            ),
            dest_path=Path("document.txt"),
        ),
    ]

    # Analyze the events
    detector = OperationDetector()
    operations = detector.detect(events)

    print(f"  📊 Detected {len(operations)} operations:")
    for i, operation in enumerate(operations, 1):
        print(f"    {i}. {operation.operation_type.value}")
        print(f"       → File: {operation.primary_path.name}")
        print(f"       → Confidence: {operation.confidence:.2f}")
        print(f"       → Atomic: {operation.is_atomic}")
        print(f"       → Safe: {operation.is_safe}")
        print(f"       → Description: {operation.description}")

    # Example 3: Custom detector configuration
    print("\n⚙️ Example 3: Custom Detector Configuration")

    # Configure for faster detection with lower confidence threshold
    config = DetectorConfig(
        time_window_ms=100,  # Shorter time window
        min_confidence=0.5,  # Lower confidence threshold
        min_events_for_complex=3,
    )

    _ = OperationDetector(config)  # Example of custom detector
    print(f"  ⏱️ Time window: {config.time_window_ms}ms")
    print(f"  🎯 Min confidence: {config.min_confidence}")
    print(f"  📈 Min events for complex ops: {config.min_events_for_complex}")

    # Example 4: Real file operations
    print("\n📝 Example 4: Real File Operations")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Simulate editor save pattern
        original_file = temp_path / "test.txt"
        temp_file = temp_path / "test.txt.tmp.abc123"

        print(f"  📂 Working in: {temp_path.name}")

        # Create events from real file operations
        real_events = []

        # Create temp file
        temp_file.write_text("Hello, World!")
        real_events.append(
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=datetime.now(), sequence_number=1, size_after=temp_file.stat().st_size
                ),
            )
        )

        time.sleep(0.01)  # Brief pause

        # Rename to final
        temp_file.rename(original_file)
        real_events.append(
            FileEvent(
                path=temp_file,
                event_type="moved",
                metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=2),
                dest_path=original_file,
            )
        )

        # Analyze real events
        real_operations = detector.detect(real_events)
        print(f"  ✅ Detected {len(real_operations)} operations from real files")

        for operation in real_operations:
            print(f"     🎯 {operation.operation_type.value}: {operation.primary_path.name}")

    print("\n✨ File operations detection complete!")


if __name__ == "__main__":
    main()
