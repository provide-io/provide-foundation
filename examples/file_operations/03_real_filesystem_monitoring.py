#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Real filesystem monitoring with watchdog integration."""

from datetime import datetime
from pathlib import Path
import sys
import tempfile
from threading import Event as ThreadEvent
import time

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from watchdog.events import FileSystemEvent, FileSystemEventHandler
    from watchdog.observers import Observer

    WATCHDOG_AVAILABLE = True
except ImportError:
    print("⚠️  Watchdog not available. Install with: uv add watchdog")
    WATCHDOG_AVAILABLE = False

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    OperationDetector,
)


class FileOperationMonitor(FileSystemEventHandler):
    """Real filesystem monitor that integrates with file operation detection."""

    def __init__(self, watch_path: Path, time_window_ms: int = 500) -> None:
        super().__init__()
        self.watch_path = watch_path
        self.detector = OperationDetector(DetectorConfig(time_window_ms=time_window_ms))
        self.sequence_counter = 0
        self.operations_detected = []
        self._stop_event = ThreadEvent()

    def _create_file_event(self, event: FileSystemEvent, event_type: str) -> FileEvent:
        """Convert watchdog event to FileEvent."""
        self.sequence_counter += 1

        # Get file size if possible
        size_after = None
        if event_type in ("created", "modified") and Path(event.src_path).exists():
            try:
                size_after = Path(event.src_path).stat().st_size
            except (OSError, FileNotFoundError):
                size_after = None

        metadata = FileEventMetadata(
            timestamp=datetime.now(),
            sequence_number=self.sequence_counter,
            size_after=size_after,
        )

        dest_path = None
        if hasattr(event, "dest_path") and event.dest_path:
            dest_path = Path(event.dest_path)

        return FileEvent(
            path=Path(event.src_path),
            event_type=event_type,
            metadata=metadata,
            dest_path=dest_path,
        )

    def _process_file_event(self, file_event: FileEvent) -> None:
        """Process a file event and check for operations."""
        try:
            # Resolve both paths to handle symlinks properly
            resolved_file = file_event.path.resolve()
            resolved_watch = self.watch_path.resolve()
            rel_path = resolved_file.relative_to(resolved_watch)
        except ValueError:
            # Fallback to just the filename if relative path fails
            rel_path = file_event.path.name
        print(f"📥 {file_event.event_type.upper()}: {rel_path}")

        # Try streaming detection
        operation = self.detector.detect_streaming(file_event)

        if operation:
            self.operations_detected.append(operation)
            try:
                resolved_primary = operation.primary_path.resolve()
                resolved_watch = self.watch_path.resolve()
                rel_primary = resolved_primary.relative_to(resolved_watch)
            except ValueError:
                rel_primary = operation.primary_path.name
            print(f"   🎯 {operation.operation_type.value}: {rel_primary}")
            print(f"      Confidence: {operation.confidence:.2f}")

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_event = self._create_file_event(event, "created")
            self._process_file_event(file_event)

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_event = self._create_file_event(event, "modified")
            self._process_file_event(file_event)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_event = self._create_file_event(event, "deleted")
            self._process_file_event(file_event)

    def on_moved(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_event = self._create_file_event(event, "moved")
            self._process_file_event(file_event)

    def flush_pending(self) -> None:
        """Flush any pending operations."""
        pending_ops = self.detector.flush()
        for operation in pending_ops:
            self.operations_detected.append(operation)
            try:
                resolved_primary = operation.primary_path.resolve()
                resolved_watch = self.watch_path.resolve()
                rel_primary = resolved_primary.relative_to(resolved_watch)
            except ValueError:
                rel_primary = operation.primary_path.name
            print(f"🔄 Flushed: {operation.operation_type.value} - {rel_primary}")

    def get_summary(self) -> str:
        """Get summary of all detected operations."""
        if not self.operations_detected:
            return "No operations detected."

        summary = f"Detected {len(self.operations_detected)} operations:\n"

        # Group by operation type
        by_type = {}
        for op in self.operations_detected:
            op_type = op.operation_type.value
            if op_type not in by_type:
                by_type[op_type] = []
            by_type[op_type].append(op)

        for op_type, ops in by_type.items():
            summary += f"  📊 {op_type}: {len(ops)} operations\n"
            for op in ops[:3]:  # Show first 3
                try:
                    resolved_primary = op.primary_path.resolve()
                    resolved_watch = self.watch_path.resolve()
                    rel_path = resolved_primary.relative_to(resolved_watch)
                except ValueError:
                    rel_path = op.primary_path.name
                summary += f"     → {rel_path} (confidence: {op.confidence:.2f})\n"

            if len(ops) > 3:
                summary += f"     ... and {len(ops) - 3} more\n"

        return summary


def simulate_vscode_save(file_path: Path) -> None:
    """Simulate VSCode atomic save pattern."""
    print(f"\n🎯 Simulating VSCode save: {file_path.name}")

    # VSCode creates a temp file, writes to it, then renames
    temp_file = file_path.with_suffix(f"{file_path.suffix}.tmp.{int(time.time())}")

    # Write to temp file
    temp_file.write_text("Hello from VSCode simulation!")
    time.sleep(0.05)  # Brief pause

    # Rename temp to final
    temp_file.rename(file_path)
    time.sleep(0.1)  # Allow event processing


def simulate_vim_save(file_path: Path) -> None:
    """Simulate Vim save pattern with backup."""
    print(f"\n🎯 Simulating Vim save: {file_path.name}")

    # First create the original file
    file_path.write_text("Original content")
    time.sleep(0.1)

    # Vim creates backup, deletes original, creates new
    backup_file = file_path.with_suffix(file_path.suffix + "~")

    # Create backup
    backup_file.write_text("Original content")
    time.sleep(0.05)

    # Delete original
    file_path.unlink()
    time.sleep(0.05)

    # Create new file
    file_path.write_text("Updated content from Vim!")
    time.sleep(0.1)


def simulate_batch_operation(base_path: Path) -> None:
    """Simulate batch file operations (like code formatting)."""
    print(f"\n🎯 Simulating batch operation in: {base_path.name}")

    # Create multiple files rapidly
    for i in range(5):
        file_path = base_path / f"module_{i}.py"
        file_path.write_text(f"# Module {i}\nprint('Hello from module {i}')\n")
        time.sleep(0.02)  # Very quick succession

    time.sleep(0.2)  # Allow batch detection


def simulate_safe_write(file_path: Path) -> None:
    """Simulate safe write with backup creation."""
    print(f"\n🎯 Simulating safe write: {file_path.name}")

    # Create original file
    file_path.write_text("Important data")
    time.sleep(0.1)

    # Create backup
    backup_file = file_path.with_suffix(".bak")
    backup_file.write_text("Important data")
    time.sleep(0.05)

    # Modify original
    file_path.write_text("Updated important data")
    time.sleep(0.1)


def main() -> None:
    """Main real filesystem monitoring demo."""

    if not WATCHDOG_AVAILABLE:
        print("This example requires the watchdog library.")
        print("Install it with: uv add watchdog")
        return

    print("=" * 55)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"📂 Monitoring directory: {temp_path.name}")

        # Create monitor
        monitor = FileOperationMonitor(temp_path, time_window_ms=300)

        # Set up watchdog observer
        observer = Observer()
        observer.schedule(monitor, str(temp_path), recursive=True)

        try:
            # Start monitoring
            observer.start()
            print("👀 Started monitoring...")
            time.sleep(0.1)  # Allow observer to start

            # Create subdirectory for batch operations
            batch_dir = temp_path / "src"
            batch_dir.mkdir()

            # Simulate various editor behaviors
            simulate_vscode_save(temp_path / "document.txt")
            simulate_vim_save(temp_path / "config.py")
            simulate_batch_operation(batch_dir)
            simulate_safe_write(temp_path / "important.dat")

            # Wait for all events to be processed
            print("\n⏳ Waiting for final events...")
            time.sleep(1.0)

            # Flush any pending operations
            print("\n🔄 Flushing pending operations...")
            monitor.flush_pending()

        finally:
            # Stop observer
            observer.stop()
            observer.join(timeout=2.0)

        # Show summary
        print("\n📊 Final Summary")
        print("=" * 25)
        print(monitor.get_summary())

        # Show operation details
        if monitor.operations_detected:
            print("\n🔍 Operation Details:")
            for i, op in enumerate(monitor.operations_detected, 1):
                try:
                    resolved_primary = op.primary_path.resolve()
                    resolved_temp = temp_path.resolve()
                    rel_path = resolved_primary.relative_to(resolved_temp)
                except ValueError:
                    rel_path = op.primary_path.name
                print(f"  {i}. {op.operation_type.value}")
                print(f"     File: {rel_path}")
                print(f"     Duration: {op.duration_ms:.1f}ms")
                print(f"     Events: {op.event_count}")
                print(f"     Atomic: {op.is_atomic}")
                print(f"     Safe: {op.is_safe}")
                if op.has_backup:
                    print("     Has backup: Yes")
                print()

    print("✨ Real filesystem monitoring demo complete!")


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
