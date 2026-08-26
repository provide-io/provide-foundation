#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test that detector priority, not confidence, decides which detector wins.

Priority encodes how specific a pattern is. Confidence is a within-detector
score, so it is not comparable across detectors -- ranking by confidence let a
general detector displace a specific one."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from provide.testkit import FoundationTestCase

from provide.foundation.file.operations.detectors import (
    clear_detector_registry,
    register_detector,
)
from provide.foundation.file.operations.detectors.orchestrator import (
    OperationDetector,
)
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    FileOperation,
    OperationType,
)


def _make_detector(description: str, confidence: float) -> object:
    """Build a detector that always matches, tagged so we can tell who won."""

    def detect(events: list[FileEvent]) -> FileOperation | None:
        return FileOperation(
            operation_type=OperationType.RENAME_SEQUENCE,
            primary_path=events[0].path,
            events=events,
            confidence=confidence,
            description=description,
            start_time=events[0].timestamp,
            end_time=events[-1].timestamp,
            is_atomic=True,
            is_safe=True,
            files_affected=[events[0].path],
        )

    return detect


def _events() -> list[FileEvent]:
    now = datetime.now()
    return [
        FileEvent(
            path=Path("/tmp/final.txt"),
            event_type="moved",
            metadata=FileEventMetadata(timestamp=now, sequence_number=1),
        ),
    ]


class TestDetectorPrioritySelection(FoundationTestCase):
    """Priority beats confidence; confidence only breaks same-priority ties."""

    def setup_method(self) -> None:
        super().setup_method()
        clear_detector_registry()

    def teardown_method(self) -> None:
        clear_detector_registry()
        super().teardown_method()

    def test_higher_priority_wins_over_higher_confidence(self) -> None:
        """A more specific detector is not displaced by a more general one.

        This is the shape that made test_rename_sequence flake on macOS:
        detect_rename_sequence (priority 75, confidence 0.80) was overwritten
        by detect_batch_update (priority 73, confidence 0.85).
        """
        register_detector(name="specific", func=_make_detector("specific", 0.80), priority=75)
        register_detector(name="general", func=_make_detector("general", 0.85), priority=73)

        operations = OperationDetector().detect(_events())

        assert len(operations) == 1
        assert operations[0].description == "specific"

    def test_registration_order_does_not_matter(self) -> None:
        """The general detector registered first must still lose."""
        register_detector(name="general", func=_make_detector("general", 0.85), priority=73)
        register_detector(name="specific", func=_make_detector("specific", 0.80), priority=75)

        operations = OperationDetector().detect(_events())

        assert len(operations) == 1
        assert operations[0].description == "specific"

    def test_confidence_breaks_ties_at_equal_priority(self) -> None:
        """Within one priority band, the higher-confidence match wins."""
        register_detector(name="weaker", func=_make_detector("weaker", 0.75), priority=80)
        register_detector(name="stronger", func=_make_detector("stronger", 0.90), priority=80)

        operations = OperationDetector().detect(_events())

        assert len(operations) == 1
        assert operations[0].description == "stronger"

    def test_subthreshold_match_does_not_block_lower_priority(self) -> None:
        """A high-priority match below min_confidence yields to a qualifying one."""
        register_detector(name="specific", func=_make_detector("specific", 0.50), priority=75)
        register_detector(name="general", func=_make_detector("general", 0.85), priority=73)

        detector = OperationDetector(DetectorConfig(min_confidence=0.7))
        operations = detector.detect(_events())

        assert len(operations) == 1
        assert operations[0].description == "general"

    def test_failing_detector_does_not_claim_priority(self) -> None:
        """A detector that raises must not suppress lower-priority detectors."""

        def boom(events: list[FileEvent]) -> FileOperation | None:
            raise RuntimeError("detector exploded")

        register_detector(name="boom", func=boom, priority=90)
        register_detector(name="general", func=_make_detector("general", 0.85), priority=73)

        operations = OperationDetector().detect(_events())

        assert len(operations) == 1
        assert operations[0].description == "general"


# 🧱🏗️🔚
