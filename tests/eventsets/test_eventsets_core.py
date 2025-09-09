# tests/test_eventsets.py
"""
Tests for Event Set configuration, resolution, and processing.
"""

from collections.abc import Callable
import io

import pytest

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    logger as global_logger,
)
from provide.foundation.eventsets.registry import discover_event_sets, get_registry
from provide.foundation.eventsets.resolver import get_resolver
from provide.foundation.testing.logger import reset_foundation_setup_for_testing
from provide.foundation.eventsets.types import (
    EventMapping,
    EventSet,
    FieldMapping,
)


class TestEventSetRegistry:
    """Test event set registration and discovery."""
    
    def test_discover_event_sets(self):
        """Test that event sets can be discovered."""
        discover_event_sets()
        registry = get_registry()
        event_sets = registry.list_event_sets()
        
        # Should find built-in event sets
        names = [es.name for es in event_sets]
        assert "default" in names
        assert "http" in names
        assert "llm" in names
        
    def test_event_sets_have_priority(self):
        """Test that event sets are sorted by priority."""
        discover_event_sets()
        registry = get_registry()
        event_sets = registry.list_event_sets()
        
        # Should be sorted by descending priority
        priorities = [es.priority for es in event_sets]
        assert priorities == sorted(priorities, reverse=True)


class TestEventSetResolver:
    """Test event set resolution and enrichment."""
    
    def test_resolver_enriches_das_events(self):
        """Test DAS event enrichment."""
        discover_event_sets()
        resolver = get_resolver()
        
        event = {
            "event": "Test message",
            "domain": "system",
            "action": "start", 
            "status": "success"
        }
        
        enriched = resolver.enrich_event(event.copy())
        
        # Should have visual enrichments
        assert "[⚙️]" in enriched["event"]  # system domain
        assert "[🚀]" in enriched["event"]  # start action
        assert "[✅]" in enriched["event"]  # success status
        
    def test_resolver_enriches_http_events(self):
        """Test HTTP event enrichment."""
        discover_event_sets()
        resolver = get_resolver()
        
        event = {
            "event": "HTTP request",
            "http.method": "get",
            "http.status_class": "2xx"
        }
        
        enriched = resolver.enrich_event(event.copy())
        
        # Should have visual enrichments
        assert "[📥]" in enriched["event"]  # GET method
        assert "[✅]" in enriched["event"]  # 2xx status
        
        # Should have metadata
        assert enriched.get("http.success") is True
        
    def test_resolver_enriches_llm_events(self):
        """Test LLM event enrichment."""
        discover_event_sets()
        resolver = get_resolver()
        
        event = {
            "event": "LLM call",
            "llm.provider": "anthropic",
            "llm.task": "chat",
            "llm.outcome": "success"
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


class TestEventSetTypes:
    """Test event set type definitions."""
    
    def test_event_mapping_creation(self):
        """Test EventMapping can be created."""
        mapping = EventMapping(
            name="test",
            visual_markers={"test": "🧪"},
            default_key="default"
        )
        assert mapping.name == "test"
        assert mapping.visual_markers["test"] == "🧪"
        assert mapping.default_key == "default"
        
    def test_event_set_creation(self):
        """Test EventSet can be created."""
        mapping = EventMapping(name="test", visual_markers={"test": "🧪"})
        field_mapping = FieldMapping(log_key="test.field", event_set_name="test")
        
        event_set = EventSet(
            name="test_set",
            description="Test event set",
            mappings=[mapping],
            field_mappings=[field_mapping],
            priority=50
        )
        
        assert event_set.name == "test_set"
        assert len(event_set.mappings) == 1
        assert len(event_set.field_mappings) == 1
        assert event_set.priority == 50


class TestLoggingIntegration:
    """Test integration with logging system."""
    
    def test_logging_uses_event_enrichment(self):
        """Test that logging system uses event enrichment."""
        from provide.foundation.logger.config import LoggingConfig
        from provide.foundation.config.telemetry import TelemetryConfig
        from provide.foundation.logger.setup import internal_setup
        from io import StringIO
        import sys
        
        reset_foundation_setup_for_testing()
        
        # Set up telemetry with INFO level and DAS emoji enabled
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                das_emoji_prefix_enabled=True,
                console_formatter="key_value"
            )
        )
        
        # Capture output
        captured_output = StringIO()
        original_stderr = sys.stderr
        sys.stderr = captured_output
        
        try:
            # Setup telemetry
            internal_setup(config=config, log_stderr=captured_output)
            
            # Get a logger and log with DAS fields
            logger = global_logger.get_logger("test")
            logger.info("Test message", domain="system", action="start", status="success")
            output = captured_output.getvalue()
            
            # Should contain emoji enrichments
            assert "⚙️" in output or "🚀" in output or "✅" in output, f"Missing emojis in output: {output}"
            
        finally:
            sys.stderr = original_stderr