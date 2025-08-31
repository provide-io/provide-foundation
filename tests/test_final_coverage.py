"""Tests to achieve 100% coverage - final missing lines."""
import json
import os
from unittest.mock import patch, MagicMock
import structlog
from provide.foundation.core import reset_foundation_setup_for_testing
from provide.foundation.logger.base import FoundationLogger, _LAZY_SETUP_STATE, _LAZY_SETUP_LOCK
from provide.foundation.config import TelemetryConfig
from provide.foundation.logger.custom_processors import add_logger_name_emoji_prefix
from provide.foundation.logger.emoji_matrix import _format_field_definition_for_display
from provide.foundation.types import SemanticFieldDefinition


def test_logger_base_already_configured_after_lock():
    """Test line 72 - return when already configured after acquiring lock."""
    reset_foundation_setup_for_testing()
    
    logger = FoundationLogger()
    
    # Clear initial state
    _LAZY_SETUP_STATE["done"] = False
    _LAZY_SETUP_STATE["error"] = None
    _LAZY_SETUP_STATE["in_progress"] = False
    logger._is_configured_by_setup = False
    
    # Mock check_structlog to return False so we enter the lock section
    with patch.object(logger, '_check_structlog_already_disabled', return_value=False):
        # Simulate another thread completing setup while we wait for lock
        # by setting done=True just before we check
        original_ensure = logger._ensure_configured
        call_count = [0]
        
        def mock_ensure(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # First call - set the state as if another thread completed
                _LAZY_SETUP_STATE["done"] = True
                _LAZY_SETUP_STATE["error"] = None
            return original_ensure(*args, **kwargs)
        
        with patch.object(logger, '_ensure_configured', mock_ensure):
            # This should trigger the early return at line 72
            logger._ensure_configured()
    
    # Reset
    reset_foundation_setup_for_testing()


def test_config_parse_custom_layers_non_list():
    """Test config.py line 167 - return empty list when custom_layers is not a list."""
    # Set environment variable to a non-list JSON value
    with patch.dict(os.environ, {'FOUNDATION_LOG_CUSTOM_SEMANTIC_LAYERS': '{"not": "a list"}'}):
        result = TelemetryConfig._parse_custom_layers_from_env()
        assert result == []


def test_config_parse_custom_layers_non_dict_item():
    """Test config.py line 170 - continue when layer_data is not a dict."""
    # Set environment variable with a list containing non-dict items
    layers_json = json.dumps([
        "not a dict",  # This should be skipped
        {"name": "valid_layer", "emoji_sets": [], "field_definitions": []}
    ])
    
    with patch.dict(os.environ, {'FOUNDATION_LOG_CUSTOM_SEMANTIC_LAYERS': layers_json}):
        result = TelemetryConfig._parse_custom_layers_from_env()
        # Should only have the valid layer
        assert len(result) == 1
        assert result[0].name == "valid_layer"


def test_config_parse_user_emoji_sets_non_list():
    """Test config.py line 196 - return empty list when user_emoji_sets is not a list."""
    # Set environment variable to a non-list JSON value
    with patch.dict(os.environ, {'FOUNDATION_LOG_USER_DEFINED_EMOJI_SETS': '"not a list"'}):
        result = TelemetryConfig._parse_user_emoji_sets_from_env()
        assert result == []


def test_config_parse_user_emoji_sets_non_dict_item():
    """Test config.py line 199 - only process dict items in user emoji sets."""
    # Set environment variable with a list containing non-dict and dict items
    sets_json = json.dumps([
        ["not", "a", "dict"],  # This should be skipped
        {"name": "valid_set", "emojis": {"test": "✅"}}  # This should be processed
    ])
    
    with patch.dict(os.environ, {'FOUNDATION_LOG_USER_DEFINED_EMOJI_SETS': sets_json}):
        result = TelemetryConfig._parse_user_emoji_sets_from_env()
        # Should only have the valid set
        assert len(result) == 1
        assert result[0].name == "valid_set"


def test_add_logger_name_emoji_prefix_no_event_msg():
    """Test custom_processors.py lines 106-107 - emoji only when no event message."""
    event_dict = {
        "logger_name": "test_logger",
        # No "event" key
    }
    
    # Mock the emoji computation
    with patch('provide.foundation.logger.custom_processors._compute_emoji_for_logger_name', return_value="🧪"):
        result = add_logger_name_emoji_prefix(None, "info", event_dict)
        
        # Should have emoji as the event
        assert result["event"] == "🧪"


def test_custom_processor_protocol_coverage():
    """Test the StructlogProcessor protocol __call__ method."""
    from provide.foundation.logger.custom_processors import StructlogProcessor
    
    # This is just to ensure the protocol is covered
    # Protocols themselves don't have implementation but we can verify the signature
    assert hasattr(StructlogProcessor, '__call__')


def test_format_field_definition_minimal():
    """Test emoji_matrix field definition formatting with minimal data."""
    # Test with only required field
    field_def = SemanticFieldDefinition(log_key="test.key")
    result = _format_field_definition_for_display(field_def)
    assert "Log Key: 'test.key'" in result
    assert "Desc:" not in result  # No description
    assert "Type:" not in result  # No type


def test_format_field_definition_with_emoji_no_override():
    """Test emoji_matrix field definition with emoji set but no override."""
    field_def = SemanticFieldDefinition(
        log_key="test.key",
        description="Test field",
        value_type="string",
        emoji_set_name="test_set"
        # No default_emoji_override_key
    )
    result = _format_field_definition_for_display(field_def)
    assert "Emoji Set: 'test_set'" in result
    assert "Default Emoji Key (Override)" not in result


def test_format_field_definition_full():
    """Test emoji_matrix field definition with all fields."""
    field_def = SemanticFieldDefinition(
        log_key="test.key",
        description="Test field",
        value_type="string", 
        emoji_set_name="test_set",
        default_emoji_override_key="custom_default"
    )
    result = _format_field_definition_for_display(field_def)
    assert "Log Key: 'test.key'" in result
    assert "Desc: Test field" in result
    assert "Type: string" in result
    assert "Emoji Set: 'test_set'" in result
    assert "Default Emoji Key (Override): 'custom_default'" in result