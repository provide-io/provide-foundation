#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for event set display utilities.

Tests all functionality in eventsets/display.py including event set formatting
and display."""

from __future__ import annotations

from provide.testkit.mocking import Mock, patch

from provide.foundation.eventsets.display import (
    _format_event_set_config,
    _format_registered_event_sets,
    _format_resolver_state,
    show_event_matrix,
)
from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping


class TestFormatEventSetConfig:
    """Tests for _format_event_set_config function."""

    def test_format_basic_config(self) -> None:
        """Test formatting event set with name and description only."""
        config = EventSet(
            name="test-event-set",
            description="Test event set",
            priority=10,
        )
        lines: list[str] = []

        _format_event_set_config(config, lines)

        assert len(lines) == 2
        assert "test-event-set (priority: 10)" in lines[0]
        assert "Test event set" in lines[1]

    def test_format_config_without_description(self) -> None:
        """Test formatting event set without description."""
        config = EventSet(
            name="minimal-event-set",
            priority=5,
        )
        lines: list[str] = []

        _format_event_set_config(config, lines)

        assert len(lines) == 1
        assert "minimal-event-set (priority: 5)" in lines[0]

    def test_format_config_with_field_mappings(self) -> None:
        """Test formatting event set with field mappings."""
        field_mappings = [
            FieldMapping(log_key="http.method", description="HTTP method"),
            FieldMapping(log_key="http.status", description="HTTP status"),
            FieldMapping(log_key="http.path", description="HTTP path"),
        ]

        config = EventSet(
            name="http-event-set",
            description="HTTP events",
            field_mappings=field_mappings,
            priority=10,
        )
        lines: list[str] = []

        _format_event_set_config(config, lines)

        # Should have name, description, field mappings header, and 3 field items
        assert any("http-event-set (priority: 10)" in line for line in lines)
        assert any("HTTP events" in line for line in lines)
        assert any("Field Mappings (3)" in line for line in lines)
        assert any("http.method" in line for line in lines)
        assert any("http.status" in line for line in lines)
        assert any("http.path" in line for line in lines)

    def test_format_config_with_many_field_mappings(self) -> None:
        """Test formatting event set with more than 5 field mappings."""
        field_mappings = [FieldMapping(log_key=f"field_{i}") for i in range(10)]

        config = EventSet(
            name="large-event-set",
            field_mappings=field_mappings,
            priority=10,
        )
        lines: list[str] = []

        _format_event_set_config(config, lines)

        # Should show first 5 and indicate more
        assert any("Field Mappings (10)" in line for line in lines)
        assert any("... and 5 more" in line for line in lines)

        # Count how many field items are shown
        field_lines = [line for line in lines if "field_" in line and "-" in line]
        assert len(field_lines) == 5  # Only first 5 shown

    def test_format_config_with_event_mappings(self) -> None:
        """Test formatting event set with event mappings."""
        event_mappings = [
            EventMapping(
                name="http-method",
                visual_markers={"GET": "🔍", "POST": "📝"},
                metadata_fields={"GET": {"safe": True}},
                transformations={"GET": lambda x: x.upper()},
            ),
            EventMapping(
                name="http-status",
                visual_markers={"200": "✅", "404": "❌"},
                metadata_fields={},
                transformations={},
            ),
        ]

        config = EventSet(
            name="http-event-set",
            mappings=event_mappings,
            priority=10,
        )
        lines: list[str] = []

        _format_event_set_config(config, lines)

        assert any("Mappings (2)" in line for line in lines)
        assert any("http-method: 2 markers, 1 metadata, 1 transforms" in line for line in lines)
        assert any("http-status: 2 markers, 0 metadata, 0 transforms" in line for line in lines)

    def test_format_config_with_all_features(self) -> None:
        """Test formatting event set with all features."""
        field_mappings = [
            FieldMapping(log_key="http.method"),
            FieldMapping(log_key="http.status"),
        ]

        event_mappings = [
            EventMapping(
                name="method-mapping",
                visual_markers={"GET": "🔍"},
            ),
        ]

        config = EventSet(
            name="comprehensive-set",
            description="Comprehensive test",
            field_mappings=field_mappings,
            mappings=event_mappings,
            priority=100,
        )
        lines: list[str] = []

        _format_event_set_config(config, lines)

        assert any("comprehensive-set (priority: 100)" in line for line in lines)
        assert any("Comprehensive test" in line for line in lines)
        assert any("Field Mappings (2)" in line for line in lines)
        assert any("Mappings (1)" in line for line in lines)


class TestFormatRegisteredEventSets:
    """Tests for _format_registered_event_sets function."""

    def test_format_empty_event_sets(self) -> None:
        """Test formatting with no registered event sets."""
        lines: list[str] = []

        _format_registered_event_sets([], lines)

        assert len(lines) == 1
        assert "(No event sets registered)" in lines[0]

    def test_format_single_event_set(self) -> None:
        """Test formatting with one event set."""
        event_sets = [
            EventSet(name="test-set", description="Test", priority=10),
        ]
        lines: list[str] = []

        _format_registered_event_sets(event_sets, lines)

        assert any("Registered Event Sets (1)" in line for line in lines)
        assert any("test-set (priority: 10)" in line for line in lines)

    def test_format_multiple_event_sets(self) -> None:
        """Test formatting with multiple event sets."""
        event_sets = [
            EventSet(name="set-1", description="First", priority=10),
            EventSet(name="set-2", description="Second", priority=20),
            EventSet(name="set-3", description="Third", priority=30),
        ]
        lines: list[str] = []

        _format_registered_event_sets(event_sets, lines)

        assert any("Registered Event Sets (3)" in line for line in lines)
        assert any("set-1 (priority: 10)" in line for line in lines)
        assert any("set-2 (priority: 20)" in line for line in lines)
        assert any("set-3 (priority: 30)" in line for line in lines)


class TestFormatResolverState:
    """Tests for _format_resolver_state function."""

    def test_format_unresolved_resolver(self) -> None:
        """Test formatting resolver that hasn't been resolved yet."""
        resolver = Mock()
        resolver._resolved = False

        lines: list[str] = []

        _format_resolver_state(resolver, lines)

        assert len(lines) == 1
        assert "(Resolver not yet initialized)" in lines[0]

    def test_format_resolved_empty_resolver(self) -> None:
        """Test formatting resolved resolver with no mappings."""
        resolver = Mock()
        resolver._resolved = True
        resolver._field_mappings = []
        resolver._event_mappings_by_set = {}

        lines: list[str] = []

        _format_resolver_state(resolver, lines)

        assert any("Resolver State:" in line for line in lines)
        assert any("Total Field Mappings: 0" in line for line in lines)
        assert any("Total Event Sets: 0" in line for line in lines)

    def test_format_resolved_with_mappings(self) -> None:
        """Test formatting resolved resolver with mappings."""
        resolver = Mock()
        resolver._resolved = True
        resolver._field_mappings = ["mapping1", "mapping2", "mapping3"]
        resolver._event_mappings_by_set = {"set1": [], "set2": []}

        lines: list[str] = []

        _format_resolver_state(resolver, lines)

        assert any("Resolver State:" in line for line in lines)
        assert any("Total Field Mappings: 3" in line for line in lines)
        assert any("Total Event Sets: 2" in line for line in lines)

    def test_format_resolved_with_visual_markers(self) -> None:
        """Test formatting resolved resolver with visual markers."""
        mapping = Mock()
        mapping.visual_markers = {
            "GET": "🔍",
            "POST": "📝",
            "DELETE": "🗑️",
        }

        resolver = Mock()
        resolver._resolved = True
        resolver._field_mappings = ["mapping1"]
        resolver._event_mappings_by_set = {
            "http-methods": [mapping],
        }

        lines: list[str] = []

        _format_resolver_state(resolver, lines)

        assert any("Sample Visual Markers:" in line for line in lines)
        assert any("http-methods:" in line for line in lines)
        # Should show first 3 markers
        marker_lines = [line for line in lines if "🔍" in line or "📝" in line or "🗑️" in line]
        assert len(marker_lines) <= 3

    def test_format_resolved_with_multiple_sets(self) -> None:
        """Test formatting resolved resolver with multiple event sets."""
        mapping1 = Mock()
        mapping1.visual_markers = {"GET": "🔍"}

        mapping2 = Mock()
        mapping2.visual_markers = {"200": "✅"}

        mapping3 = Mock()
        mapping3.visual_markers = {"ERROR": "❌"}

        resolver = Mock()
        resolver._resolved = True
        resolver._field_mappings = ["m1", "m2", "m3"]
        resolver._event_mappings_by_set = {
            "http-methods": [mapping1],
            "http-status": [mapping2],
            "log-levels": [mapping3],
        }

        lines: list[str] = []

        _format_resolver_state(resolver, lines)

        # Should show up to 3 sets
        assert any("Sample Visual Markers:" in line for line in lines)

    def test_format_resolved_with_empty_visual_markers(self) -> None:
        """Test formatting when mappings have no visual markers."""
        mapping = Mock()
        mapping.visual_markers = {}

        resolver = Mock()
        resolver._resolved = True
        resolver._field_mappings = ["mapping1"]
        resolver._event_mappings_by_set = {
            "test-set": [mapping],
        }

        lines: list[str] = []

        _format_resolver_state(resolver, lines)

        # Should show resolver state but no sample markers
        assert any("Resolver State:" in line for line in lines)
        # Sample Visual Markers section should still appear but no markers shown
        marker_section = any("Sample Visual Markers:" in line for line in lines)
        assert marker_section


class TestShowEventMatrix:
    """Tests for show_event_matrix function."""

    @patch("provide.foundation.eventsets.display.log")
    @patch("provide.foundation.eventsets.display.get_resolver")
    @patch("provide.foundation.eventsets.display.get_registry")
    @patch("provide.foundation.eventsets.display.discover_event_sets")
    def test_show_event_matrix_basic(
        self,
        mock_discover: Mock,
        mock_get_registry: Mock,
        mock_get_resolver: Mock,
        mock_log: Mock,
    ) -> None:
        """Test basic show_event_matrix functionality."""
        # Setup mocks
        mock_registry = Mock()
        mock_registry.list_event_sets.return_value = []
        mock_get_registry.return_value = mock_registry

        mock_resolver = Mock()
        mock_resolver._resolved = False
        mock_get_resolver.return_value = mock_resolver

        # Call function
        show_event_matrix()

        # Verify discovery was called
        mock_discover.assert_called_once()

        # Verify resolver.resolve() was called
        mock_resolver.resolve.assert_called_once()

        # Verify logger.info was called
        mock_log.info.assert_called_once()

        # Check that the logged message contains expected sections
        logged_message = mock_log.info.call_args[0][0]
        assert "Foundation Event Sets: Active Configuration" in logged_message
        assert "=" in logged_message

    @patch("provide.foundation.eventsets.display.log")
    @patch("provide.foundation.eventsets.display.get_resolver")
    @patch("provide.foundation.eventsets.display.get_registry")
    @patch("provide.foundation.eventsets.display.discover_event_sets")
    def test_show_event_matrix_with_event_sets(
        self,
        mock_discover: Mock,
        mock_get_registry: Mock,
        mock_get_resolver: Mock,
        mock_log: Mock,
    ) -> None:
        """Test show_event_matrix with registered event sets."""
        # Setup event sets
        event_sets = [
            EventSet(name="http-events", description="HTTP domain", priority=10),
            EventSet(name="llm-events", description="LLM domain", priority=20),
        ]

        mock_registry = Mock()
        mock_registry.list_event_sets.return_value = event_sets
        mock_get_registry.return_value = mock_registry

        mock_resolver = Mock()
        mock_resolver._resolved = True
        mock_resolver._field_mappings = ["m1", "m2"]
        mock_resolver._event_mappings_by_set = {}
        mock_get_resolver.return_value = mock_resolver

        # Call function
        show_event_matrix()

        # Verify logger was called with event set information
        logged_message = mock_log.info.call_args[0][0]
        assert "Registered Event Sets (2)" in logged_message
        assert "http-events" in logged_message
        assert "llm-events" in logged_message

    @patch("provide.foundation.eventsets.display.log")
    @patch("provide.foundation.eventsets.display.get_resolver")
    @patch("provide.foundation.eventsets.display.get_registry")
    @patch("provide.foundation.eventsets.display.discover_event_sets")
    def test_show_event_matrix_with_resolved_state(
        self,
        mock_discover: Mock,
        mock_get_registry: Mock,
        mock_get_resolver: Mock,
        mock_log: Mock,
    ) -> None:
        """Test show_event_matrix with resolved resolver state."""
        mock_registry = Mock()
        mock_registry.list_event_sets.return_value = []
        mock_get_registry.return_value = mock_registry

        mapping = Mock()
        mapping.visual_markers = {"GET": "🔍"}

        mock_resolver = Mock()
        mock_resolver._resolved = True
        mock_resolver._field_mappings = ["m1", "m2", "m3"]
        mock_resolver._event_mappings_by_set = {"http": [mapping]}
        mock_get_resolver.return_value = mock_resolver

        # Call function
        show_event_matrix()

        # Verify resolver state is shown
        logged_message = mock_log.info.call_args[0][0]
        assert "Resolver State:" in logged_message
        assert "Total Field Mappings: 3" in logged_message
        assert "Total Event Sets: 1" in logged_message
        assert "Sample Visual Markers:" in logged_message


# 🧱🏗️🔚
