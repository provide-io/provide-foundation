"""Test coverage for emoji matrix module."""

from unittest.mock import Mock, patch
import pytest

from provide.foundation.logger.emoji import matrix
from provide.foundation.logger.emoji.types import EmojiSet, FieldToEmojiMapping


class TestEmojiMatrixCoverage:
    """Test emoji matrix functionality."""
    
    def test_primary_emoji_constants(self):
        """Test PRIMARY_EMOJI constant is defined correctly."""
        assert "system" in matrix.PRIMARY_EMOJI
        assert matrix.PRIMARY_EMOJI["system"] == "⚙️"
        assert "default" in matrix.PRIMARY_EMOJI
        assert matrix.PRIMARY_EMOJI["default"] == "❓"
        
        # Check it's a proper dict
        assert isinstance(matrix.PRIMARY_EMOJI, dict)
        assert len(matrix.PRIMARY_EMOJI) > 10
    
    def test_secondary_emoji_constants(self):
        """Test SECONDARY_EMOJI constant is defined correctly."""
        assert "init" in matrix.SECONDARY_EMOJI
        assert matrix.SECONDARY_EMOJI["init"] == "🌱"
        assert "default" in matrix.SECONDARY_EMOJI
        assert matrix.SECONDARY_EMOJI["default"] == "❓"
        
        # Check it's a proper dict
        assert isinstance(matrix.SECONDARY_EMOJI, dict)
        assert len(matrix.SECONDARY_EMOJI) > 10
    
    def test_tertiary_emoji_constants(self):
        """Test TERTIARY_EMOJI constant is defined correctly."""
        assert "success" in matrix.TERTIARY_EMOJI
        assert matrix.TERTIARY_EMOJI["success"] == "✅"
        assert "default" in matrix.TERTIARY_EMOJI
        assert matrix.TERTIARY_EMOJI["default"] == "➡️"
        
        # Check it's a proper dict
        assert isinstance(matrix.TERTIARY_EMOJI, dict)
        assert len(matrix.TERTIARY_EMOJI) > 10
    
    def test_format_emoji_set_for_display(self):
        """Test _format_emoji_set_for_display function."""
        emoji_set = EmojiSet(
            name="test_set",
            emojis={"key1": "🔥", "key2": "⭐", "abc": "🎯"},
            default_emoji_key="key1"
        )
        
        result = matrix._format_emoji_set_for_display(emoji_set)
        
        assert isinstance(result, list)
        assert len(result) >= 4  # Header + at least 3 emoji lines
        
        # Check header
        assert "test_set" in result[0]
        assert "key1" in result[0]
        
        # Check content has sorted emoji mappings
        content = "\n".join(result[1:])
        assert "🎯  -> Abc" in content  # abc should be capitalized and sorted first
        assert "🔥  -> Key1" in content
        assert "⭐  -> Key2" in content
    
    def test_format_field_definition_for_display_basic(self):
        """Test _format_field_definition_for_display with basic field definition."""
        field_def = FieldToEmojiMapping(
            log_key="test_key",
            description=None,
            value_type=None,
            emoji_set_name=None,
            default_emoji_override_key=None
        )
        
        result = matrix._format_field_definition_for_display(field_def)
        
        assert isinstance(result, str)
        assert "Log Key: 'test_key'" in result
        assert "Desc:" not in result  # No description
        assert "Type:" not in result  # No value_type
        assert "Emoji Set:" not in result  # No emoji_set_name
    
    def test_format_field_definition_for_display_complete(self):
        """Test _format_field_definition_for_display with complete field definition."""
        field_def = FieldToEmojiMapping(
            log_key="complete_key",
            description="Test description",
            value_type="string",
            emoji_set_name="test_set",
            default_emoji_override_key="override_key"
        )
        
        result = matrix._format_field_definition_for_display(field_def)
        
        assert "Log Key: 'complete_key'" in result
        assert "Desc: Test description" in result
        assert "Type: string" in result
        assert "Emoji Set: 'test_set'" in result
        assert "Default Emoji Key (Override): 'override_key'" in result
    
    def test_format_field_definition_for_display_partial(self):
        """Test _format_field_definition_for_display with partial field definition."""
        field_def = FieldToEmojiMapping(
            log_key="partial_key",
            description="Partial desc",
            value_type=None,
            emoji_set_name="partial_set",
            default_emoji_override_key=None  # No override
        )
        
        result = matrix._format_field_definition_for_display(field_def)
        
        assert "Log Key: 'partial_key'" in result
        assert "Desc: Partial desc" in result
        assert "Type:" not in result  # No value_type
        assert "Emoji Set: 'partial_set'" in result
        assert "Default Emoji Key (Override):" not in result  # No override
    
    def test_show_emoji_matrix_disabled(self):
        """Test show_emoji_matrix when disabled."""
        mock_logger = Mock()
        mock_logger._ensure_configured = Mock()
        
        # Mock telemetry config to disable show_emoji_matrix
        mock_config = Mock()
        mock_config.logging.show_emoji_matrix = False
        mock_logger._active_config = mock_config
        
        with patch('provide.foundation.logger.emoji.matrix.foundation_logger_base.logger', mock_logger):
            matrix.show_emoji_matrix()
            
            # Should configure but not proceed
            mock_logger._ensure_configured.assert_called_once()
    
    def test_show_emoji_matrix_no_config(self):
        """Test show_emoji_matrix when no config is available."""
        mock_logger = Mock()
        mock_logger._ensure_configured = Mock()
        mock_logger._active_config = None  # No config
        
        with patch('provide.foundation.logger.emoji.matrix.foundation_logger_base.logger', mock_logger):
            matrix.show_emoji_matrix()
            
            # Should configure but not proceed
            mock_logger._ensure_configured.assert_called_once()
    
    def test_show_emoji_matrix_with_core_das(self):
        """Test show_emoji_matrix with core DAS emoji system active."""
        mock_logger = Mock()
        mock_logger._ensure_configured = Mock()
        
        # Mock telemetry config to enable show_emoji_matrix
        mock_config = Mock()
        mock_config.logging.show_emoji_matrix = True
        mock_logger._active_config = mock_config
        
        # Mock no resolved emoji config (means core DAS is active)
        mock_logger._active_resolved_emoji_config = None
        
        # Mock the get_logger method
        mock_matrix_logger = Mock()
        mock_logger.get_logger.return_value = mock_matrix_logger
        
        with patch('provide.foundation.logger.emoji.matrix.foundation_logger_base.logger', mock_logger):
            matrix.show_emoji_matrix()
            
            # Should get the matrix logger
            mock_logger.get_logger.assert_called_once_with("provide.foundation.emoji_matrix_display")
            
            # Should log the core DAS info
            mock_matrix_logger.info.assert_called_once()
            logged_content = mock_matrix_logger.info.call_args[0][0]
            assert "Foundation Telemetry: Emoji configuration not yet resolved or available." in logged_content
    
    def test_emoji_constants_have_defaults(self):
        """Test that all emoji constant dicts have 'default' keys."""
        assert "default" in matrix.PRIMARY_EMOJI
        assert "default" in matrix.SECONDARY_EMOJI
        assert "default" in matrix.TERTIARY_EMOJI
    
    def test_emoji_constants_are_dicts(self):
        """Test that emoji constants are proper dictionaries."""
        assert isinstance(matrix.PRIMARY_EMOJI, dict)
        assert isinstance(matrix.SECONDARY_EMOJI, dict)
        assert isinstance(matrix.TERTIARY_EMOJI, dict)
        
        # Should have substantial content
        assert len(matrix.PRIMARY_EMOJI) > 5
        assert len(matrix.SECONDARY_EMOJI) > 5  
        assert len(matrix.TERTIARY_EMOJI) > 5
    
    def test_emoji_values_are_strings(self):
        """Test that emoji values are all strings."""
        for emoji_dict in [matrix.PRIMARY_EMOJI, matrix.SECONDARY_EMOJI, matrix.TERTIARY_EMOJI]:
            for key, value in emoji_dict.items():
                assert isinstance(key, str), f"Key {key} is not a string"
                assert isinstance(value, str), f"Value {value} for key {key} is not a string"