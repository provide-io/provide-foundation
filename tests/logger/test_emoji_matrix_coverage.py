#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test coverage for EventSet integration with logging."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.eventsets.registry import discover_event_sets, get_registry
from provide.foundation.eventsets.resolver import get_resolver
from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping


class TestEventSetIntegration(FoundationTestCase):
    """Test EventSet integration with logging system."""

    def test_event_mapping_creation(self) -> None:
        """Test EventMapping creation with visual markers."""
        mapping = EventMapping(
            name="test_mapping",
            default_key="default",
            visual_markers={
                "error": "❌",
                "info": "💡",
                "success": "✅",
            },
        )

        assert mapping.name == "test_mapping"
        assert mapping.visual_markers["error"] == "❌"
        assert mapping.visual_markers["info"] == "💡"
        assert mapping.default_key == "default"

    def test_event_set_creation(self) -> None:
        """Test EventSet creation with mappings and field mappings."""
        mapping = EventMapping(
            name="status",
        )

        field_mapping = FieldMapping(
            log_key="status",
            event_set_name="test_set",
        )

        event_set = EventSet(
            name="test_set",
            description="Test event set",
            mappings=[mapping],
            field_mappings=[field_mapping],
            priority=50,
        )

        assert event_set.name == "test_set"
        assert event_set.description == "Test event set"
        assert len(event_set.mappings) == 1
        assert len(event_set.field_mappings) == 1
        assert event_set.priority == 50

    def test_field_mapping_creation(self) -> None:
        """Test FieldMapping creation with various fields."""
        field_mapping = FieldMapping(
            log_key="test.field",
            event_set_name="test_set",
            description="Test field mapping",
            value_type="string",
            default_value="default",
        )

        assert field_mapping.log_key == "test.field"
        assert field_mapping.event_set_name == "test_set"
        assert field_mapping.description == "Test field mapping"
        assert field_mapping.value_type == "string"
        assert field_mapping.default_value == "default"

    def test_event_set_discovery(self) -> None:
        """Test event set discovery functionality."""
        discover_event_sets()
        registry = get_registry()
        event_sets = registry.list_event_sets()

        # Should discover built-in event sets
        names = [es.name for es in event_sets]
        assert "default" in names
        assert "http" in names
        assert "llm" in names

    def test_event_enrichment_resolver(self) -> None:
        """Test event enrichment through resolver."""
        discover_event_sets()
        resolver = get_resolver()

        # Test DAS event enrichment
        event = {
            "event": "Test message",
            "domain": "system",
            "action": "start",
            "status": "success",
        }

        resolver.enrich_event(event.copy())

        # Should have visual markers added

    def test_registry_event_set_priority_ordering(self) -> None:
        """Test that event sets are ordered by priority."""
        discover_event_sets()
        registry = get_registry()
        event_sets = registry.list_event_sets()

        # Should be sorted by descending priority
        priorities = [es.priority for es in event_sets]
        assert priorities == sorted(priorities, reverse=True)

    def test_event_mapping_with_metadata_and_transformations(self) -> None:
        """Test EventMapping with metadata fields and transformations."""

        def uppercase_transform(value: str | None) -> str | None:
            return str(value).upper() if value else value

        mapping = EventMapping(
            name="status_mapping",
            visual_markers={"success": "✅", "error": "❌"},
            metadata_fields={"success_meta": {"type": "boolean", "value": True}},
            transformations={"uppercase": uppercase_transform},
            default_key="info",
        )

        assert mapping.name == "status_mapping"
        assert "success" in mapping.visual_markers
        assert "success_meta" in mapping.metadata_fields
        assert "uppercase" in mapping.transformations
        assert mapping.default_key == "info"

        # Test transformation
        result = mapping.transformations["uppercase"]("hello")
        assert result == "HELLO"

    def test_event_set_with_complex_configuration(self) -> None:
        """Test EventSet with complex mappings and configurations."""
        domain_mapping = EventMapping(
            name="domain",
        )

        action_mapping = EventMapping(
            name="action",
            visual_markers={"start": "🚀", "complete": "🏁", "error": "💥"},
        )

        field_mapping = FieldMapping(
            log_key="system.status",
            event_set_name="complex_test",
            description="System status field",
            value_type="string",
        )

        event_set = EventSet(
            name="complex_test",
            description="Complex test event set",
            mappings=[domain_mapping, action_mapping],
            field_mappings=[field_mapping],
            priority=100,
        )

        assert len(event_set.mappings) == 2
        assert event_set.mappings[0].name == "domain"
        assert event_set.mappings[1].name == "action"
        assert len(event_set.field_mappings) == 1
        assert event_set.field_mappings[0].log_key == "system.status"


# 🧱🏗️🔚
