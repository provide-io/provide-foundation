"""
Tests for configuration field converters.
"""

import pytest

from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_comma_list,
    parse_console_formatter,
    parse_float_with_validation,
    parse_headers,
    parse_json_dict,
    parse_json_list,
    parse_log_level,
    parse_module_levels,
    parse_rate_limits,
    parse_sample_rate,
    validate_log_level,
    validate_non_negative,
    validate_overflow_policy,
    validate_port,
    validate_positive,
    validate_sample_rate,
)


class TestLogLevelParsing:
    """Test log level parsing and validation."""

    def test_parse_log_level_valid(self):
        """Test parsing valid log levels."""
        assert parse_log_level("debug") == "DEBUG"
        assert parse_log_level("INFO") == "INFO"
        assert parse_log_level("Warning") == "WARNING"
        assert parse_log_level("ERROR") == "ERROR"
        assert parse_log_level("critical") == "CRITICAL"
        assert parse_log_level("TRACE") == "TRACE"

    def test_parse_log_level_invalid(self):
        """Test parsing invalid log levels raises error."""
        with pytest.raises(ValueError, match="Invalid log level"):
            parse_log_level("INVALID")
        
        with pytest.raises(ValueError, match="Invalid log level"):
            parse_log_level("")


class TestConsoleFormatterParsing:
    """Test console formatter parsing."""

    def test_parse_console_formatter_valid(self):
        """Test parsing valid formatters."""
        assert parse_console_formatter("KEY_VALUE") == "key_value"
        assert parse_console_formatter("json") == "json"
        assert parse_console_formatter("JSON") == "json"

    def test_parse_console_formatter_invalid(self):
        """Test parsing invalid formatters raises error."""
        with pytest.raises(ValueError, match="Invalid formatter"):
            parse_console_formatter("xml")
        
        with pytest.raises(ValueError, match="Invalid formatter"):
            parse_console_formatter("yaml")


class TestModuleLevelsParsing:
    """Test module-specific log levels parsing."""

    def test_parse_module_levels_valid(self):
        """Test parsing valid module:level pairs."""
        result = parse_module_levels("auth:DEBUG,database:ERROR")
        assert result == {"auth": "DEBUG", "database": "ERROR"}
        
        result = parse_module_levels("auth.service:TRACE, db.queries:WARNING")
        assert result == {"auth.service": "TRACE", "db.queries": "WARNING"}

    def test_parse_module_levels_empty(self):
        """Test parsing empty string returns empty dict."""
        assert parse_module_levels("") == {}
        assert parse_module_levels("   ") == {}

    def test_parse_module_levels_invalid_format(self):
        """Test invalid formats are skipped silently."""
        result = parse_module_levels("auth:DEBUG,invalid_no_colon,db:INFO")
        assert result == {"auth": "DEBUG", "db": "INFO"}
        
        result = parse_module_levels("auth:INVALID_LEVEL,db:ERROR")
        assert result == {"db": "ERROR"}  # Invalid level skipped

    def test_parse_module_levels_whitespace(self):
        """Test whitespace handling."""
        result = parse_module_levels(" auth : DEBUG , database : ERROR ")
        assert result == {"auth": "DEBUG", "database": "ERROR"}


class TestRateLimitsParsing:
    """Test rate limits parsing."""

    def test_parse_rate_limits_valid(self):
        """Test parsing valid logger:rate:capacity triplets."""
        result = parse_rate_limits("api:10.0:100.0,worker:5:50")
        assert result == {
            "api": (10.0, 100.0),
            "worker": (5.0, 50.0)
        }

    def test_parse_rate_limits_empty(self):
        """Test parsing empty string returns empty dict."""
        assert parse_rate_limits("") == {}
        assert parse_rate_limits("   ") == {}

    def test_parse_rate_limits_invalid_format(self):
        """Test invalid formats are skipped silently."""
        result = parse_rate_limits("api:10:100,invalid:format,worker:5:50")
        assert result == {
            "api": (10.0, 100.0),
            "worker": (5.0, 50.0)
        }
        
        result = parse_rate_limits("api:not_a_number:100")
        assert result == {}  # Invalid number skipped


class TestBoolExtendedParsing:
    """Test extended boolean parsing."""

    @pytest.mark.parametrize("value,expected", [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("yes", True),
        ("Yes", True),
        ("1", True),
        ("on", True),
        ("ON", True),
        ("false", False),
        ("False", False),
        ("no", False),
        ("0", False),
        ("off", False),
        ("OFF", False),
        ("", False),
        ("anything_else", False),
    ])
    def test_parse_bool_extended(self, value, expected):
        """Test parsing various boolean representations."""
        assert parse_bool_extended(value) == expected


class TestFloatValidationParsing:
    """Test float parsing with validation."""

    def test_parse_float_with_validation_valid(self):
        """Test parsing valid floats."""
        assert parse_float_with_validation("3.14") == 3.14
        assert parse_float_with_validation("10") == 10.0
        assert parse_float_with_validation("-5.5") == -5.5

    def test_parse_float_with_validation_range(self):
        """Test parsing with range validation."""
        assert parse_float_with_validation("5.0", min_val=0.0, max_val=10.0) == 5.0
        
        with pytest.raises(ValueError, match="below minimum"):
            parse_float_with_validation("-1.0", min_val=0.0)
        
        with pytest.raises(ValueError, match="above maximum"):
            parse_float_with_validation("11.0", max_val=10.0)

    def test_parse_float_with_validation_invalid(self):
        """Test parsing invalid floats raises error."""
        with pytest.raises(ValueError, match="Invalid float"):
            parse_float_with_validation("not_a_number")


class TestSampleRateParsing:
    """Test sample rate parsing."""

    def test_parse_sample_rate_valid(self):
        """Test parsing valid sample rates."""
        assert parse_sample_rate("0.0") == 0.0
        assert parse_sample_rate("0.5") == 0.5
        assert parse_sample_rate("1.0") == 1.0

    def test_parse_sample_rate_invalid_range(self):
        """Test parsing sample rates outside 0-1 range."""
        with pytest.raises(ValueError, match="below minimum"):
            parse_sample_rate("-0.1")
        
        with pytest.raises(ValueError, match="above maximum"):
            parse_sample_rate("1.1")


class TestHeadersParsing:
    """Test HTTP headers parsing."""

    def test_parse_headers_valid(self):
        """Test parsing valid header pairs."""
        result = parse_headers("Authorization=Bearer token,Content-Type=application/json")
        assert result == {
            "Authorization": "Bearer token",
            "Content-Type": "application/json"
        }

    def test_parse_headers_empty(self):
        """Test parsing empty string returns empty dict."""
        assert parse_headers("") == {}
        assert parse_headers("   ") == {}

    def test_parse_headers_invalid_format(self):
        """Test invalid formats are skipped."""
        result = parse_headers("Valid=value,InvalidNoEquals,Another=one")
        assert result == {
            "Valid": "value",
            "Another": "one"
        }

    def test_parse_headers_whitespace(self):
        """Test whitespace handling."""
        result = parse_headers(" Key1 = Value1 , Key2 = Value2 ")
        assert result == {
            "Key1": "Value1",
            "Key2": "Value2"
        }


class TestCommaListParsing:
    """Test comma-separated list parsing."""

    def test_parse_comma_list_valid(self):
        """Test parsing comma-separated strings."""
        assert parse_comma_list("a,b,c") == ["a", "b", "c"]
        assert parse_comma_list(" a , b , c ") == ["a", "b", "c"]

    def test_parse_comma_list_empty(self):
        """Test parsing empty string returns empty list."""
        assert parse_comma_list("") == []
        assert parse_comma_list("   ") == []

    def test_parse_comma_list_single(self):
        """Test parsing single item."""
        assert parse_comma_list("single") == ["single"]


class TestJsonParsing:
    """Test JSON parsing functions."""

    def test_parse_json_dict_valid(self):
        """Test parsing valid JSON objects."""
        result = parse_json_dict('{"key": "value", "number": 42}')
        assert result == {"key": "value", "number": 42}

    def test_parse_json_dict_empty(self):
        """Test parsing empty string returns empty dict."""
        assert parse_json_dict("") == {}
        assert parse_json_dict("   ") == {}

    def test_parse_json_dict_invalid(self):
        """Test parsing invalid JSON raises error."""
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_json_dict("not json")
        
        with pytest.raises(ValueError, match="Expected JSON object"):
            parse_json_dict('["list", "not", "dict"]')

    def test_parse_json_list_valid(self):
        """Test parsing valid JSON arrays."""
        result = parse_json_list('["a", "b", "c"]')
        assert result == ["a", "b", "c"]

    def test_parse_json_list_empty(self):
        """Test parsing empty string returns empty list."""
        assert parse_json_list("") == []
        assert parse_json_list("   ") == []

    def test_parse_json_list_invalid(self):
        """Test parsing invalid JSON raises error."""
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_json_list("not json")
        
        with pytest.raises(ValueError, match="Expected JSON array"):
            parse_json_list('{"key": "value"}')


class TestValidators:
    """Test validator functions."""

    def test_validate_log_level(self):
        """Test log level validator."""
        # Valid levels should not raise
        validate_log_level(None, type('attr', (), {'name': 'test'})(), "DEBUG")
        validate_log_level(None, type('attr', (), {'name': 'test'})(), "INFO")
        
        # Invalid level should raise
        with pytest.raises(ValueError, match="Invalid log level"):
            validate_log_level(None, type('attr', (), {'name': 'test'})(), "INVALID")

    def test_validate_sample_rate(self):
        """Test sample rate validator."""
        # Valid rates should not raise
        validate_sample_rate(None, type('attr', (), {'name': 'test'})(), 0.0)
        validate_sample_rate(None, type('attr', (), {'name': 'test'})(), 0.5)
        validate_sample_rate(None, type('attr', (), {'name': 'test'})(), 1.0)
        
        # Invalid rates should raise
        with pytest.raises(ValueError, match="must be between"):
            validate_sample_rate(None, type('attr', (), {'name': 'test'})(), -0.1)
        
        with pytest.raises(ValueError, match="must be between"):
            validate_sample_rate(None, type('attr', (), {'name': 'test'})(), 1.1)

    def test_validate_port(self):
        """Test port number validator."""
        # Valid ports should not raise
        validate_port(None, type('attr', (), {'name': 'test'})(), 1)
        validate_port(None, type('attr', (), {'name': 'test'})(), 8080)
        validate_port(None, type('attr', (), {'name': 'test'})(), 65535)
        
        # Invalid ports should raise
        with pytest.raises(ValueError, match="must be between"):
            validate_port(None, type('attr', (), {'name': 'test'})(), 0)
        
        with pytest.raises(ValueError, match="must be between"):
            validate_port(None, type('attr', (), {'name': 'test'})(), 65536)

    def test_validate_positive(self):
        """Test positive value validator."""
        # Valid values should not raise
        validate_positive(None, type('attr', (), {'name': 'test'})(), 1)
        validate_positive(None, type('attr', (), {'name': 'test'})(), 0.1)
        validate_positive(None, type('attr', (), {'name': 'test'})(), 100)
        
        # Invalid values should raise
        with pytest.raises(ValueError, match="must be positive"):
            validate_positive(None, type('attr', (), {'name': 'test'})(), 0)
        
        with pytest.raises(ValueError, match="must be positive"):
            validate_positive(None, type('attr', (), {'name': 'test'})(), -1)

    def test_validate_non_negative(self):
        """Test non-negative value validator."""
        # Valid values should not raise
        validate_non_negative(None, type('attr', (), {'name': 'test'})(), 0)
        validate_non_negative(None, type('attr', (), {'name': 'test'})(), 1)
        validate_non_negative(None, type('attr', (), {'name': 'test'})(), 100)
        
        # Invalid values should raise
        with pytest.raises(ValueError, match="must be non-negative"):
            validate_non_negative(None, type('attr', (), {'name': 'test'})(), -1)
        
        with pytest.raises(ValueError, match="must be non-negative"):
            validate_non_negative(None, type('attr', (), {'name': 'test'})(), -0.1)

    def test_validate_overflow_policy(self):
        """Test overflow policy validator."""
        # Valid policies should not raise
        validate_overflow_policy(None, type('attr', (), {'name': 'test'})(), "drop_oldest")
        validate_overflow_policy(None, type('attr', (), {'name': 'test'})(), "drop_newest")
        validate_overflow_policy(None, type('attr', (), {'name': 'test'})(), "block")
        
        # Invalid policies should raise
        with pytest.raises(ValueError, match="Invalid overflow policy"):
            validate_overflow_policy(None, type('attr', (), {'name': 'test'})(), "invalid")
        
        with pytest.raises(ValueError, match="Invalid overflow policy"):
            validate_overflow_policy(None, type('attr', (), {'name': 'test'})(), "")