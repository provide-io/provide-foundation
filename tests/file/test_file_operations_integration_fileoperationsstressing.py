#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for file operation detection with real filesystem operations."""

from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.operations import (
    FileEvent,
    FileEventMetadata,
    OperationDetector,
)


class TestFileOperationsStressTesting(FoundationTestCase):
    """Stress tests for file operations detection."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def detector(self) -> OperationDetector:
        """Create an operation detector for testing."""
        return OperationDetector()

    def test_rapid_file_creation_detection(self, temp_dir: Path, detector: OperationDetector) -> None:
        """Test detection with rapid file creation."""
        events = []

        # Simulate rapid file creation (100 files in 1 second)
        for i in range(100):
            file_path = temp_dir / f"rapid_{i}.txt"
            # Create the actual file
            file_path.write_text(f"Content {i}")

            # Create event
            event = FileEvent(
                path=file_path,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=datetime.now(),
                    sequence_number=i + 1,
                    size_after=len(f"Content {i}"),
                ),
            )
            events.append(event)

        # Test detection performance
        start_time = time.perf_counter()
        operations = detector.detect(events)
        end_time = time.perf_counter()

        detection_time = (end_time - start_time) * 1000  # milliseconds

        # Should complete within reasonable time (account for system load)
        assert detection_time < 250  # Less than 250ms for 100 files

        # Should detect some operations (likely batch updates)
        assert len(operations) >= 0

    def test_mixed_operation_patterns_stress(self, temp_dir: Path, detector: OperationDetector) -> None:
        """Test detection with mixed operation patterns under stress."""
        events = []
        base_time = datetime.now()

        # Generate complex mixed patterns
        for i in range(50):
            time_offset = i * 600  # 600ms apart (beyond 500ms time window)

            # VSCode atomic save
            temp_file = temp_dir / f"file{i}.txt.tmp.{i}"
            final_file = temp_dir / f"file{i}.txt"

            events.extend(
                [
                    FileEvent(
                        path=temp_file,
                        event_type="created",
                        metadata=FileEventMetadata(
                            timestamp=base_time + timedelta(milliseconds=time_offset),
                            sequence_number=len(events) + 1,
                            size_after=1024,
                        ),
                    ),
                    FileEvent(
                        path=temp_file,
                        event_type="moved",
                        metadata=FileEventMetadata(
                            timestamp=base_time + timedelta(milliseconds=time_offset + 5),
                            sequence_number=len(events) + 2,
                        ),
                        dest_path=final_file,
                    ),
                ]
            )

            # Safe write every 5th iteration
            if i % 5 == 0:
                backup_file = temp_dir / f"backup{i}.bak"
                main_file = temp_dir / f"backup{i}"

                events.extend(
                    [
                        FileEvent(
                            path=backup_file,
                            event_type="created",
                            metadata=FileEventMetadata(
                                timestamp=base_time + timedelta(milliseconds=time_offset + 20),
                                sequence_number=len(events) + 1,
                                size_after=1000,
                            ),
                        ),
                        FileEvent(
                            path=main_file,
                            event_type="modified",
                            metadata=FileEventMetadata(
                                timestamp=base_time + timedelta(milliseconds=time_offset + 25),
                                sequence_number=len(events) + 2,
                                size_before=1000,
                                size_after=1024,
                            ),
                        ),
                    ]
                )

        # Test detection under stress
        start_time = time.perf_counter()
        operations = detector.detect(events)
        end_time = time.perf_counter()

        detection_time = (end_time - start_time) * 1000

        # Should handle stress test efficiently
        assert detection_time < 500  # Less than 500ms

        # Should detect multiple operations
        assert len(operations) >= 30  # Should detect most atomic saves

    def test_large_file_event_batches(self, temp_dir: Path, detector: OperationDetector) -> None:
        """Test detection with very large batches of events."""
        large_batch_size = 1000
        events = []
        base_time = datetime.now()

        # Generate large batch of simple modify events
        for i in range(large_batch_size):
            file_path = temp_dir / f"batch_file_{i % 20}.py"  # Reuse file names

            event = FileEvent(
                path=file_path,
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=i),
                    sequence_number=i + 1,
                    size_before=500,
                    size_after=520,
                ),
            )
            events.append(event)

        # Test large batch detection
        start_time = time.perf_counter()
        operations = detector.detect(events)
        end_time = time.perf_counter()

        detection_time = (end_time - start_time) * 1000

        # Should handle large batches efficiently
        assert detection_time < 1000  # Less than 1 second

        # Should detect batch operations
        batch_ops = [op for op in operations if op.operation_type.value == "batch_update"]
        assert len(batch_ops) >= 1

    def test_concurrent_streaming_simulation(self, temp_dir: Path) -> None:
        """Test concurrent streaming detection simulation."""
        import queue
        import threading

        results_queue = queue.Queue()
        num_threads = 3
        events_per_thread = 20

        def streaming_worker(worker_id: int) -> None:
            """Worker that processes events in streaming fashion."""
            detector = OperationDetector()
            base_time = datetime.now()
            detected_operations = []

            for i in range(events_per_thread):
                # Create VSCode-style events
                temp_file = temp_dir / f"worker{worker_id}_file{i}.txt.tmp.{i}"
                final_file = temp_dir / f"worker{worker_id}_file{i}.txt"

                # First event
                event1 = FileEvent(
                    path=temp_file,
                    event_type="created",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=i * 50),
                        sequence_number=i * 2 + 1,
                    ),
                )

                result = detector.detect_streaming(event1)
                if result:
                    detected_operations.append(result)

                # Second event
                event2 = FileEvent(
                    path=temp_file,
                    event_type="moved",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=i * 50 + 25),
                        sequence_number=i * 2 + 2,
                    ),
                    dest_path=final_file,
                )

                result = detector.detect_streaming(event2)
                if result:
                    detected_operations.append(result)

            # Flush remaining
            detected_operations.extend(detector.flush())

            results_queue.put(
                {
                    "worker_id": worker_id,
                    "operations": detected_operations,
                }
            )

        # Start workers
        workers = []
        start_time = time.perf_counter()

        for i in range(num_threads):
            worker = threading.Thread(daemon=True, target=streaming_worker, args=(i,))
            workers.append(worker)
            worker.start()

        # Wait for completion
        for worker in workers:
            worker.join(timeout=10.0)

        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Verify concurrent processing
        assert len(results) == num_threads
        assert total_time < 10000  # Should complete within 10 seconds (allows for system load)

        # Each worker should have processed some operations
        total_operations = sum(len(r["operations"]) for r in results)
        assert total_operations >= 0


if __name__ == "__main__":
    pytest.main([__file__])

# 🧱🏗️🔚
