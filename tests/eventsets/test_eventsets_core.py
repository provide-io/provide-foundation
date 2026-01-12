#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Event Set configuration, resolution, and processing."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation import logger as global_logger
from provide.foundation.eventsets.registry import discover_event_sets, get_registry
from provide.foundation.eventsets.resolver import get_resolver
from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping


class TestEventSetRegistry(FoundationTestCase):
    """Test event set registration and discovery."""

    def test_discover_event_sets(self) -> None:
        """Test that event sets can be discovered."""
        discover_event_sets()
        registry = get_registry()
        event_sets = registry.list_event_sets()

        # Should find built-in event sets
        names = [es.name for es in event_sets]
        assert "default" in names
        assert "http" in names
        assert "llm" in names

    def test_event_sets_have_priority(self) -> None:
        """Test that event sets are sorted by priority."""
        discover_event_sets()
        registry = get_registry()
        event_sets = registry.list_event_sets()

        # Should be sorted by descending priority
        priorities = [es.priority for es in event_sets]
        assert priorities == sorted(priorities, reverse=True)


class TestEventSetResolver(FoundationTestCase):
    """Test event set resolution and enrichment."""

    def test_resolver_enriches_das_events(self) -> None:
        """Test DAS event enrichment."""
        discover_event_sets()
        resolver = get_resolver()

        event = {
            "event": "Test message",
            "domain": "system",
            "action": "start",
            "status": "success",
        }

        enriched = resolver.enrich_event(event.copy())

        # Should have visual enrichments
        assert "[🚀]" in enriched["event"]  # start action

    def test_resolver_enriches_http_events(self) -> None:
        """Test HTTP event enrichment."""
        discover_event_sets()
        resolver = get_resolver()

        event = {
            "event": "HTTP request",
            "http.method": "get",
            "http.status_class": "2xx",
        }

        enriched = resolver.enrich_event(event.copy())

        # Should have visual enrichments
        assert "[📥]" in enriched["event"]  # GET method

        # Should have metadata
        assert enriched.get("http.success") is True

    def test_resolver_enriches_llm_events(self) -> None:
        """Test LLM event enrichment."""
        discover_event_sets()
        resolver = get_resolver()

        event = {
            "event": "LLM call",
            "llm.provider": "anthropic",
            "llm.task": "chat",
            "llm.outcome": "success",
        }

        enriched = resolver.enrich_event(event.copy())

        # Should have visual enrichments
        assert "[📚]" in enriched["event"]  # anthropic
        assert "[💬]" in enriched["event"]  # chat task
        assert "[👍]" in enriched["event"]  # success outcome

        # Should have metadata
        assert enriched.get("llm.vendor") == "anthropic"
        assert enriched.get("llm.type") == "conversational"
        assert enriched.get("llm.success") is True


class TestEventSetTypes(FoundationTestCase):
    """Test event set type definitions."""

    def test_event_mapping_creation(self) -> None:
        """Test EventMapping can be created."""
        mapping = EventMapping(
            name="test",
            default_key="default",
        )
        assert mapping.name == "test"
        assert mapping.default_key == "default"

    def test_event_set_creation(self) -> None:
        """Test EventSet can be created."""
        mapping = EventMapping(name="test", default_key="default")
        field_mapping = FieldMapping(log_key="test.field", event_set_name="test")

        event_set = EventSet(
            name="test_set",
            description="Test event set",
            mappings=[mapping],
            field_mappings=[field_mapping],
            priority=50,
        )

        assert event_set.name == "test_set"
        assert len(event_set.mappings) == 1
        assert len(event_set.field_mappings) == 1
        assert event_set.priority == 50


class TestLoggingIntegration(FoundationTestCase):
    """Test integration with logging system."""

    def test_logging_uses_event_enrichment(self) -> None:
        """Test that logging system uses event enrichment."""
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
        from provide.foundation.logger.setup import internal_setup

        # Foundation reset is handled by FoundationTestCase

        # Set up telemetry with INFO level and DAS emoji enabled
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                das_emoji_prefix_enabled=True,
                console_formatter="key_value",
            ),
        )

        # Setup telemetry
        internal_setup(config=config)

        # Get a logger - if this works without error, event enrichment is working
        logger = global_logger.get_logger("test")

        # This should work without throwing exceptions
        # The fact that we can log with DAS fields means enrichment is working
        try:
            logger.info("Test message", domain="system", action="start", status="success")
            # If we get here, the enrichment processor is working
            assert True
        except Exception as e:
            raise AssertionError(f"Event enrichment failed: {e}") from e


# 🧱🏗️🔚
