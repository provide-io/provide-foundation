#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Streaming file operation detection for real-time monitoring."""

import asyncio
from datetime import datetime
from pathlib import Path
import queue
import sys
import tempfile
import time

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    OperationDetector,
)


class StreamingFileMonitor:
    """Example streaming file monitor that processes events as they arrive."""

    def __init__(self, time_window_ms: int = 500) -> None:
        self.detector = OperationDetector(DetectorConfig(time_window_ms=time_window_ms))
        self.operations_detected = []
        self.event_count = 0

    def process_event(self, event: FileEvent) -> None:
        """Process a single file event."""
        self.event_count += 1
        print(f"📥 Event {self.event_count}: {event.event_type} {event.path.name}")

        # Try to detect operation from this event
        operation = self.detector.detect_streaming(event)

        if operation:
            self.operations_detected.append(operation)
            print(f"   🎯 Operation detected: {operation.operation_type.value}")
            print(f"      → {operation.description}")
            print(f"      → Confidence: {operation.confidence:.2f}")

    def flush_pending(self) -> None:
        """Flush any pending operations."""
        pending_ops = self.detector.flush()
        for operation in pending_ops:
            self.operations_detected.append(operation)
            print(f"🔄 Flushed operation: {operation.operation_type.value}")

    def get_summary(self) -> str:
        """Get summary of detected operations."""
        if not self.operations_detected:
            return "No operations detected"

        summary = f"Detected {len(self.operations_detected)} operations:\n"
        for i, op in enumerate(self.operations_detected, 1):
            summary += f"  {i}. {op.operation_type.value} - {op.primary_path.name}\n"

        return summary


def simulate_editor_workflow(monitor: StreamingFileMonitor, base_path: Path) -> None:
    """Simulate various editor save patterns."""

    print("\n🎭 Scenario 1: VSCode Atomic Save")
    print("-" * 30)

    # VSCode pattern: create temp, rename to final
    temp_file = base_path / "document.txt.tmp.vscode123"
    final_file = base_path / "document.txt"

    # Create temp file event
    monitor.process_event(
        FileEvent(
            path=temp_file,
            event_type="created",
            metadata=FileEventMetadata(
                timestamp=datetime.now(), sequence_number=1, size_after=1024, process_name="Code"
            ),
        )
    )

    time.sleep(0.05)  # Brief delay

    # Rename event
    monitor.process_event(
        FileEvent(
            path=temp_file,
            event_type="moved",
            metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=2),
            dest_path=final_file,
        )
    )

    time.sleep(0.1)  # Wait for detection

    print("\n🎭 Scenario 2: Vim with Backup")
    print("-" * 30)

    vim_file = base_path / "config.py"
    backup_file = base_path / "config.py~"

    # Delete original
    monitor.process_event(
        FileEvent(
            path=vim_file,
            event_type="deleted",
            metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=3, size_before=512),
        )
    )

    time.sleep(0.02)

    # Create backup
    monitor.process_event(
        FileEvent(
            path=backup_file,
            event_type="created",
            metadata=FileEventMetadata(
                timestamp=datetime.now(), sequence_number=4, size_after=512, process_name="vim"
            ),
        )
    )

    time.sleep(0.1)

    print("\n🎭 Scenario 3: Batch File Updates")
    print("-" * 30)

    # Simulate code formatter updating multiple files
    for i in range(3):
        file_path = base_path / f"module_{i}.py"

        monitor.process_event(
            FileEvent(
                path=file_path,
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=datetime.now(),
                    sequence_number=5 + i,
                    size_before=200 + i * 10,
                    size_after=250 + i * 10,
                    process_name="black",
                ),
            )
        )

        time.sleep(0.01)  # Very quick succession

    time.sleep(0.2)  # Wait for batch detection


def demonstrate_streaming_with_timeout() -> None:
    """Demonstrate streaming detection with timeout flushing."""

    print("\n⏰ Timeout-based Flushing Demo")
    print("=" * 40)

    # Short time window for quick demo
    monitor = StreamingFileMonitor(time_window_ms=200)
    base_path = Path("/tmp/demo")

    # Create event
    monitor.process_event(
        FileEvent(
            path=base_path / "isolated.txt",
            event_type="created",
            metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=1, size_after=100),
        )
    )

    print("⏳ Waiting for timeout...")
    time.sleep(0.3)  # Wait longer than time window

    # This should trigger a flush
    print("🔄 Triggering flush...")
    monitor.flush_pending()


async def async_monitoring_demo() -> None:
    """Demonstrate async-compatible monitoring."""

    print("\n🔄 Async Monitoring Demo")
    print("=" * 30)

    monitor = StreamingFileMonitor(time_window_ms=300)

    # Simulate async event processing
    events_to_process = queue.Queue()

    # Add some events to queue
    base_path = Path("/tmp/async_demo")

    events_to_process.put(
        FileEvent(
            path=base_path / "async_file.txt",
            event_type="created",
            metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=1, size_after=200),
        )
    )

    events_to_process.put(
        FileEvent(
            path=base_path / "async_file.txt",
            event_type="modified",
            metadata=FileEventMetadata(
                timestamp=datetime.now(), sequence_number=2, size_before=200, size_after=300
            ),
        )
    )

    # Process events asynchronously
    while not events_to_process.empty():
        event = events_to_process.get()
        monitor.process_event(event)

        # Yield control to event loop
        await asyncio.sleep(0.1)

    # Final flush
    monitor.flush_pending()


def main() -> None:
    """Main streaming detection demo."""

    print("=" * 55)

    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"📂 Working directory: {temp_path.name}")

        # Create monitor
        monitor = StreamingFileMonitor(time_window_ms=500)

        # Simulate various workflows
        simulate_editor_workflow(monitor, temp_path)

        # Final flush to catch any pending operations
        print("\n🔄 Final flush...")
        monitor.flush_pending()

        # Show summary
        print("\n📊 Summary")
        print("=" * 20)
        print(monitor.get_summary())

    # Demonstrate timeout behavior
    demonstrate_streaming_with_timeout()

    # Demonstrate async usage
    print("\n🔄 Running async demo...")
    asyncio.run(async_monitoring_demo())

    print("\n✨ Streaming detection demo complete!")


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
