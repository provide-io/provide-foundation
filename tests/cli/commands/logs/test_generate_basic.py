#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for CLI logs generate command."""

from __future__ import annotations

import threading

from provide.testkit import FoundationTestCase

from provide.foundation.cli.commands.logs.constants import (
    BURROUGHS_PHRASES,
    OPERATIONS,
    SERVICE_NAMES,
)
from provide.foundation.cli.commands.logs.generator import LogGenerator


class TestConstants(FoundationTestCase):
    """Test module constants."""

    def test_burroughs_phrases_exist(self) -> None:
        """Test that Burroughs phrases are defined."""
        assert isinstance(BURROUGHS_PHRASES, list)
        assert len(BURROUGHS_PHRASES) > 0
        assert all(isinstance(phrase, str) for phrase in BURROUGHS_PHRASES)

    def test_service_names_exist(self) -> None:
        """Test that service names are defined."""
        assert isinstance(SERVICE_NAMES, list)
        assert len(SERVICE_NAMES) > 0
        assert all(isinstance(name, str) for name in SERVICE_NAMES)

    def test_operations_exist(self) -> None:
        """Test that operations are defined."""
        assert isinstance(OPERATIONS, list)
        assert len(OPERATIONS) > 0
        assert all(isinstance(op, str) for op in OPERATIONS)

    def test_has_click_flag_exists(self) -> None:
        """Test that _HAS_CLICK flag is defined."""
        from provide.foundation.cli.deps import _HAS_CLICK

        assert isinstance(_HAS_CLICK, bool)


class TestTraceSpanGeneration(FoundationTestCase):
    """Test trace and span ID generation."""

    def test_generate_trace_id(self) -> None:
        """Test trace ID generation."""
        generator = LogGenerator()
        trace_id = generator.generate_trace_id()
        assert trace_id == "trace_00000000"

        # Second call should increment
        trace_id_2 = generator.generate_trace_id()
        assert trace_id_2 == "trace_00000001"

    def test_generate_span_id(self) -> None:
        """Test span ID generation."""
        generator = LogGenerator()
        span_id = generator.generate_span_id()
        assert span_id == "span_00000000"

        # Second call should increment
        span_id_2 = generator.generate_span_id()
        assert span_id_2 == "span_00000001"

    def test_trace_id_thread_safety(self) -> None:
        """Test that trace ID generation is thread-safe."""
        generator = LogGenerator()
        trace_ids = []

        def generate_multiple() -> None:
            for _ in range(10):
                trace_ids.append(generator.generate_trace_id())

        threads = [threading.Thread(daemon=True, target=generate_multiple) for _ in range(5)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10.0)

        # Should have 50 unique trace IDs
        assert len(trace_ids) == 50
        assert len(set(trace_ids)) == 50

    def test_span_id_thread_safety(self) -> None:
        """Test that span ID generation is thread-safe."""
        generator = LogGenerator()
        span_ids = []

        def generate_multiple() -> None:
            for _ in range(10):
                span_ids.append(generator.generate_span_id())

        threads = [threading.Thread(daemon=True, target=generate_multiple) for _ in range(5)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10.0)

        # Should have 50 unique span IDs
        assert len(span_ids) == 50
        assert len(set(span_ids)) == 50


# 🧱🏗️🔚
