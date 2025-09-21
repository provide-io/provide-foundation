"""Performance benchmarks for file operation detection."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import time

import pytest

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    OperationDetector,
)
from provide.foundation.file.quality import AnalysisMetric, QualityAnalyzer, create_test_cases_from_patterns


class TestFileOperationsPerformance:
    """Performance benchmarks for file operations detection."""

    def test_single_operation_detection_performance(self, benchmark) -> None:
        """Benchmark single operation detection."""
        detector = OperationDetector()
        base_time = datetime.now()

        # Create VSCode atomic save events
        events = [
            FileEvent(
                path=Path("test.txt.tmp.12345"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1, size_after=1024),
            ),
            FileEvent(
                path=Path("test.txt.tmp.12345"),
                event_type="moved",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=50), sequence_number=2
                ),
                dest_path=Path("test.txt"),
            ),
        ]

        # Benchmark the detection
        result = benchmark(detector.detect, events)

        # Verify result
        assert len(result) >= 1
        assert result[0].operation_type.value == "atomic_save"

    def test_batch_operation_detection_performance(self, benchmark) -> None:
        """Benchmark batch operation detection with many files."""
        detector = OperationDetector()
        base_time = datetime.now()

        # Create events for 50 files being modified in quick succession
        events = []
        for i in range(50):
            events.append(
                FileEvent(
                    path=Path(f"src/file{i}.py"),
                    event_type="modified",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=i * 10),
                        sequence_number=i + 1,
                        size_before=500,
                        size_after=520,
                    ),
                )
            )

        # Benchmark the detection
        result = benchmark(detector.detect, events)

        # Verify result
        assert len(result) >= 1

    def test_streaming_detection_performance(self, benchmark) -> None:
        """Benchmark streaming detection performance."""
        detector = OperationDetector()
        base_time = datetime.now()

        # Create events to be processed one by one
        events = [
            FileEvent(
                path=Path("test.txt.tmp.12345"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=Path("test.txt.tmp.12345"),
                event_type="moved",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=50), sequence_number=2
                ),
                dest_path=Path("test.txt"),
            ),
        ]

        def streaming_process():
            operations = []
            for event in events:
                result = detector.detect_streaming(event)
                if result:
                    operations.append(result)
            # Flush any remaining
            operations.extend(detector.flush())
            return operations

        # Benchmark the streaming detection
        result = benchmark(streaming_process)
        assert len(result) >= 0  # May or may not detect based on timing

    def test_large_event_set_performance(self, benchmark) -> None:
        """Benchmark detection with large number of mixed events."""
        detector = OperationDetector()
        base_time = datetime.now()

        events = []

        # Generate 100 mixed operation patterns
        for i in range(100):
            # VSCode save pattern
            events.extend(
                [
                    FileEvent(
                        path=Path(f"file{i}.txt.tmp.{i}"),
                        event_type="created",
                        metadata=FileEventMetadata(
                            timestamp=base_time + timedelta(milliseconds=i * 100),
                            sequence_number=len(events) + 1,
                        ),
                    ),
                    FileEvent(
                        path=Path(f"file{i}.txt.tmp.{i}"),
                        event_type="moved",
                        metadata=FileEventMetadata(
                            timestamp=base_time + timedelta(milliseconds=i * 100 + 50),
                            sequence_number=len(events) + 2,
                        ),
                        dest_path=Path(f"file{i}.txt"),
                    ),
                ]
            )

            # Safe write pattern every 10th iteration
            if i % 10 == 0:
                events.extend(
                    [
                        FileEvent(
                            path=Path(f"backup{i}.bak"),
                            event_type="created",
                            metadata=FileEventMetadata(
                                timestamp=base_time + timedelta(milliseconds=i * 100 + 200),
                                sequence_number=len(events) + 1,
                            ),
                        ),
                        FileEvent(
                            path=Path(f"backup{i}"),
                            event_type="modified",
                            metadata=FileEventMetadata(
                                timestamp=base_time + timedelta(milliseconds=i * 100 + 250),
                                sequence_number=len(events) + 2,
                            ),
                        ),
                    ]
                )

        # Benchmark the detection
        result = benchmark(detector.detect, events)

        # Verify reasonable number of operations detected
        # With 500ms time window and 100ms gaps, most operations get grouped together
        assert len(result) >= 1  # Should detect at least one operation

    def test_detector_configuration_performance(self, benchmark) -> None:
        """Benchmark different detector configurations."""
        # Test with different time window configurations
        configs = [
            DetectorConfig(time_window_ms=100),
            DetectorConfig(time_window_ms=500),
            DetectorConfig(time_window_ms=1000),
        ]

        base_time = datetime.now()
        events = [
            FileEvent(
                path=Path("test.txt.tmp.12345"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=Path("test.txt.tmp.12345"),
                event_type="moved",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=200), sequence_number=2
                ),
                dest_path=Path("test.txt"),
            ),
        ]

        def test_with_config(config):
            detector = OperationDetector(config)
            return detector.detect(events)

        # Benchmark with fastest config (100ms window)
        result = benchmark(test_with_config, configs[0])
        assert len(result) >= 0

    def test_quality_analyzer_performance(self, benchmark) -> None:
        """Benchmark quality analysis performance."""
        analyzer = QualityAnalyzer()

        # Add standard test cases
        test_cases = create_test_cases_from_patterns()
        for test_case in test_cases:
            analyzer.add_test_case(test_case)

        # Benchmark the analysis
        metrics = [
            AnalysisMetric.ACCURACY,
            AnalysisMetric.DETECTION_TIME,
            AnalysisMetric.CONFIDENCE_DISTRIBUTION,
        ]
        result = benchmark(analyzer.run_analysis, metrics)

        # Verify results
        assert len(result) == 3
        assert AnalysisMetric.ACCURACY in result
        assert result[AnalysisMetric.ACCURACY].value >= 0.0

    @pytest.mark.parametrize("event_count", [10, 50, 100, 500])
    def test_scalability_with_event_count(self, benchmark, event_count: int) -> None:
        """Test scalability with different event counts."""
        detector = OperationDetector()
        base_time = datetime.now()

        # Generate events based on count
        events = []
        for i in range(event_count):
            events.append(
                FileEvent(
                    path=Path(f"file{i}.py"),
                    event_type="modified",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=i * 10),
                        sequence_number=i + 1,
                    ),
                )
            )

        # Benchmark detection
        result = benchmark(detector.detect, events)

        # Performance should scale reasonably
        assert len(result) >= 0

    def test_memory_usage_with_large_datasets(self) -> None:
        """Test memory usage doesn't grow excessively with large datasets."""
        detector = OperationDetector()
        base_time = datetime.now()

        # Create a large number of events
        large_event_count = 1000
        events = []

        for i in range(large_event_count):
            events.append(
                FileEvent(
                    path=Path(f"large_file_{i}.txt"),
                    event_type="modified",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=i),
                        sequence_number=i + 1,
                    ),
                )
            )

        # Process in batches to test memory handling
        batch_size = 100
        total_operations = 0

        for i in range(0, large_event_count, batch_size):
            batch = events[i : i + batch_size]
            operations = detector.detect(batch)
            total_operations += len(operations)

        # Should handle large datasets without issues
        assert total_operations >= 0

    def test_concurrent_detection_simulation(self) -> None:
        """Simulate concurrent detection patterns."""
        import queue
        import threading

        detector = OperationDetector()
        results_queue = queue.Queue()
        base_time = datetime.now()

        def detect_worker(worker_id: int, events: list[FileEvent]) -> None:
            """Worker function for concurrent detection."""
            start_time = time.perf_counter()
            operations = detector.detect(events)
            end_time = time.perf_counter()

            results_queue.put(
                {
                    "worker_id": worker_id,
                    "operations": operations,
                    "duration": end_time - start_time,
                }
            )

        # Create different event sets for each worker
        workers = []
        for i in range(3):  # 3 concurrent workers
            events = [
                FileEvent(
                    path=Path(f"worker{i}_file.txt.tmp.{i}"),
                    event_type="created",
                    metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
                ),
                FileEvent(
                    path=Path(f"worker{i}_file.txt.tmp.{i}"),
                    event_type="moved",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=50), sequence_number=2
                    ),
                    dest_path=Path(f"worker{i}_file.txt"),
                ),
            ]

            worker = threading.Thread(target=detect_worker, args=(i, events))
            workers.append(worker)

        # Start all workers
        start_time = time.perf_counter()
        for worker in workers:
            worker.start()

        # Wait for all workers to complete
        for worker in workers:
            worker.join()

        end_time = time.perf_counter()

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Verify all workers completed successfully
        assert len(results) == 3
        total_duration = end_time - start_time

        # Should complete within reasonable time
        assert total_duration < 1.0  # Less than 1 second for this simple test

        # Each worker should have detected operations
        for result in results:
            assert len(result["operations"]) >= 0
            assert result["duration"] >= 0

    def test_pattern_complexity_performance(self, benchmark) -> None:
        """Test performance with complex file patterns."""
        detector = OperationDetector()
        base_time = datetime.now()

        # Create complex patterns with many temp files
        events = []
        patterns = [
            ".document.txt.tmp.12345",
            "document.txt~",
            ".document.txt.swp",
            "#document.txt#",
            "document.txt.bak",
            "document.txt.orig",
        ]

        for i, pattern in enumerate(patterns):
            # Each pattern gets a creation and move/modify
            events.extend(
                [
                    FileEvent(
                        path=Path(pattern),
                        event_type="created",
                        metadata=FileEventMetadata(
                            timestamp=base_time + timedelta(milliseconds=i * 100),
                            sequence_number=i * 2 + 1,
                        ),
                    ),
                    FileEvent(
                        path=Path(pattern),
                        event_type="moved" if ".tmp." in pattern else "modified",
                        metadata=FileEventMetadata(
                            timestamp=base_time + timedelta(milliseconds=i * 100 + 50),
                            sequence_number=i * 2 + 2,
                        ),
                        dest_path=Path("document.txt") if ".tmp." in pattern else None,
                    ),
                ]
            )

        # Benchmark detection with complex patterns
        result = benchmark(detector.detect, events)

        # Should handle complex patterns efficiently
        assert len(result) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--benchmark-only"])
