"""
TDD tests for emoji set and processor component registration.

This test suite covers emoji set registration, discovery, priority ordering,
and processor pipeline management through the registry system.
"""

import asyncio
from collections.abc import AsyncIterator, Iterator
import threading
from typing import Any
from unittest.mock import Mock, AsyncMock

import pytest
from structlog.typing import EventDict

from provide.foundation.config.base import BaseConfig
from provide.foundation.hub.registry import Registry, RegistryEntry
from provide.foundation.logger.config import LoggingConfig, TelemetryConfig


# Configuration source tests removed - module doesn't exist yet


class TestProcessorRegistration:
    """Test processor registration and pipeline management."""

    def test_processors_register_in_processor_category(self):
        """Log processors must register in PROCESSOR category."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )

        registry = get_component_registry()

        # Create a test processor
        def test_processor(logger, method_name, event_dict):
            event_dict["processed"] = True
            return event_dict

        # Register the processor
        registry.register(
            name="test_processor",
            value=test_processor,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={
                "priority": 50,
                "stage": "pre_format",
                "async": False,
            },
        )

        # Verify registration
        retrieved_processor = registry.get(
            "test_processor", ComponentCategory.PROCESSOR.value
        )
        assert retrieved_processor is test_processor

    def test_processor_pipeline_ordering(self):
        """Processors must be executed in priority order."""
        from provide.foundation.hub.components import (
            get_processor_pipeline,
            bootstrap_foundation,
        )

        pipeline = get_processor_pipeline()

        # If pipeline is empty (due to test isolation), re-bootstrap
        if len(pipeline) == 0:
            bootstrap_foundation()
            pipeline = get_processor_pipeline()

        # Pipeline should be ordered by priority
        assert len(pipeline) > 0

        for i in range(len(pipeline) - 1):
            current_priority = pipeline[i].metadata.get("priority", 0)
            next_priority = pipeline[i + 1].metadata.get("priority", 0)
            assert current_priority >= next_priority

    def test_async_processor_support(self):
        """Registry must support async processors."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )

        registry = get_component_registry()

        # Create async processor
        async def async_processor(logger, method_name, event_dict):
            await asyncio.sleep(0)  # Simulate async work
            event_dict["async_processed"] = True
            return event_dict

        registry.register(
            name="async_processor",
            value=async_processor,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"async": True, "priority": 60},
        )

        # Should be retrievable
        retrieved = registry.get("async_processor", ComponentCategory.PROCESSOR.value)
        assert retrieved is async_processor

    def test_processor_stage_filtering(self):
        """Processors must be filterable by processing stage."""
        from provide.foundation.hub.components import get_processors_for_stage

        pre_format_processors = get_processors_for_stage("pre_format")
        post_format_processors = get_processors_for_stage("post_format")

        assert isinstance(pre_format_processors, list)
        assert isinstance(post_format_processors, list)

        # Each should contain only processors for that stage
        for processor in pre_format_processors:
            assert processor.metadata.get("stage") == "pre_format"

    def test_conditional_processor_execution(self):
        """Processors must support conditional execution based on metadata."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )

        registry = get_component_registry()

        # Processor with conditions
        def conditional_processor(logger, method_name, event_dict):
            return event_dict

        registry.register(
            name="conditional_processor",
            value=conditional_processor,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={
                "conditions": {
                    "min_level": "INFO",
                    "domains": ["http", "database"],
                },
                "priority": 30,
            },
        )

        entry = registry.get_entry(
            "conditional_processor", ComponentCategory.PROCESSOR.value
        )
        assert "conditions" in entry.metadata
        assert entry.metadata["conditions"]["min_level"] == "INFO"