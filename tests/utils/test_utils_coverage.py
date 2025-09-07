"""
Additional tests for provide.foundation.utils to increase code coverage.
"""
import io
from typing import Any

from attrs import define, field, fields

from provide.foundation import LoggingConfig, TelemetryConfig, logger, setup_telemetry
from provide.foundation.utils import timed_block
from provide.foundation.utils.formatting import format_table, to_camel_case
from provide.foundation.utils.parsing import auto_parse, parse_typed_value


class TestCaseConversionCoverage:
    """Coverage for case conversion functions."""

    def test_to_camel_case_empty_string(self) -> None:
        """Test to_camel_case with an empty string."""
        assert to_camel_case("") == ""


class TestTableFormattingCoverage:
    """Coverage for table formatting edge cases."""

    def test_format_table_empty_rows(self) -> None:
        """Test format_table with headers but no rows."""
        headers = ["Header 1", "Header 2"]
        rows = []
        table = format_table(headers, rows)
        assert "Header 1" in table
        assert "Header 2" in table
        assert len(table.splitlines()) == 2  # Header and separator line

    def test_format_table_ragged_rows(self) -> None:
        """Test format_table with rows of different lengths."""
        headers = ["A", "B", "C"]
        rows = [["1", "2"], ["4", "5", "6"]]
        table = format_table(headers, rows)
        # Should not raise an error and should format correctly
        assert "1" in table
        assert "2" in table
        assert "6" in table

    def test_format_table_alignment_mismatch(self) -> None:
        """Test format_table with more alignment options than headers."""
        headers = ["A", "B"]
        rows = [["1", "2"]]
        table = format_table(headers, rows, alignment=["l", "c", "r"])
        assert "1" in table
        assert "2" in table

    def test_format_table_no_headers_or_rows(self) -> None:
        """Test format_table with no headers and no rows."""
        assert format_table([], []) == ""


class TestParsingCoverage:
    """Coverage for parsing utility functions."""

    def test_parse_typed_value_unsupported_origin(self) -> None:
        """Test parse_typed_value with a type origin it doesn't handle."""
        # It should fall back to returning the original string value.
        result = parse_typed_value("some_value", set)
        assert result == "some_value"

    def test_auto_parse_with_string_type_hints(self) -> None:
        """Test auto_parse for attrs fields with string type hints."""
        @define
        class DummyConfig:
            int_val: 'int'
            bool_val: 'bool'
            list_val: 'list'
            dict_val: 'dict'
            unknown_val: 'SomeUnknownType'

        attrs_fields = {f.name: f for f in fields(DummyConfig)}

        assert auto_parse(attrs_fields['int_val'], "42") == 42
        assert auto_parse(attrs_fields['bool_val'], "true") is True
        assert auto_parse(attrs_fields['list_val'], "a,b") == ["a", "b"]
        assert auto_parse(attrs_fields['dict_val'], "k=v") == {"k": "v"}
        assert auto_parse(attrs_fields['unknown_val'], "some_string") == "some_string"

    def test_auto_parse_no_type_hint(self) -> None:
        """Test auto_parse for an attrs field with no type hint."""
        @define
        class NoTypeHintConfig:
            val: Any = field()

        no_type_field = fields(NoTypeHintConfig).val
        assert auto_parse(no_type_field, "a_string") == "a_string"


class TestTimingCoverage:
    """Coverage for timing utility functions."""

    def test_timed_block_context_modification(self, captured_stderr_for_foundation: io.StringIO) -> None:
        """Test that modifying the context dict within a timed_block works."""
        setup_telemetry(TelemetryConfig())

        with timed_block(logger, "test_op") as ctx:
            ctx["records"] = 100
            ctx["status_custom"] = "success" # Use a non-special key

        output = captured_stderr_for_foundation.getvalue()
        # Verify that the modifications to the context dict are present in the final log.
        assert "records=100" in output
        assert "status_custom=success" in output
        assert "outcome=success" in output

    def test_timed_block_debug_message(self, captured_stderr_for_foundation: io.StringIO) -> None:
        """Test that the initial debug message is logged when level is DEBUG."""
        setup_telemetry(TelemetryConfig(logging=LoggingConfig(default_level="DEBUG")))

        with timed_block(logger, "debug_test_op"):
            pass

        output = captured_stderr_for_foundation.getvalue()
        # Check for both the "started" and "completed" messages
        assert "debug_test_op started" in output
        assert "debug_test_op completed" in output


class TestEnvUtilsCoverage:
    """Coverage for environment utilities."""
    
    def test_get_bool_edge_cases(self):
        """Test edge cases for get_bool function."""
        import os
        from unittest.mock import patch
        from provide.foundation.utils.env import get_bool
        from provide.foundation.errors.config import ValidationError
        
        # Test with empty string (should be False)
        with patch.dict(os.environ, {"TEST_BOOL": ""}):
            assert get_bool("TEST_BOOL") is False
        
        # Test with whitespace
        with patch.dict(os.environ, {"TEST_BOOL": "  true  "}):
            assert get_bool("TEST_BOOL") is True
        
        # Test invalid value raises ValidationError
        with patch.dict(os.environ, {"TEST_BOOL": "invalid"}):
            try:
                get_bool("TEST_BOOL")
                assert False, "Should have raised ValidationError"
            except ValidationError as e:
                assert "Invalid boolean value" in str(e)
    
    def test_get_int_edge_cases(self):
        """Test edge cases for get_int function."""
        import os
        from unittest.mock import patch
        from provide.foundation.utils.env import get_int
        from provide.foundation.errors.config import ValidationError
        
        # Test negative numbers
        with patch.dict(os.environ, {"TEST_INT": "-42"}):
            assert get_int("TEST_INT") == -42
        
        # Test zero
        with patch.dict(os.environ, {"TEST_INT": "0"}):
            assert get_int("TEST_INT") == 0
        
        # Test invalid value raises ValidationError
        with patch.dict(os.environ, {"TEST_INT": "not_a_number"}):
            try:
                get_int("TEST_INT")
                assert False, "Should have raised ValidationError"  
            except ValidationError as e:
                assert "Invalid integer value" in str(e)
    
    def test_get_float_edge_cases(self):
        """Test edge cases for get_float function.""" 
        import os
        from unittest.mock import patch
        from provide.foundation.utils.env import get_float
        from provide.foundation.errors.config import ValidationError
        
        # Test scientific notation
        with patch.dict(os.environ, {"TEST_FLOAT": "1e-3"}):
            assert get_float("TEST_FLOAT") == 0.001
        
        # Test negative float
        with patch.dict(os.environ, {"TEST_FLOAT": "-3.14"}):
            assert get_float("TEST_FLOAT") == -3.14
        
        # Test invalid value
        with patch.dict(os.environ, {"TEST_FLOAT": "not_a_float"}):
            try:
                get_float("TEST_FLOAT")
                assert False, "Should have raised ValidationError"
            except ValidationError as e:
                assert "Invalid float value" in str(e)
    
    def test_get_str_with_default(self):
        """Test get_str with default value."""
        import os
        from unittest.mock import patch
        from provide.foundation.utils.env import get_str
        
        # Test with missing env var (should use default)
        result = get_str("NON_EXISTENT_STR", default="default_value")
        assert result == "default_value"
        
        # Test with existing env var
        with patch.dict(os.environ, {"TEST_STR": "actual_value"}):
            result = get_str("TEST_STR", default="default_value") 
            assert result == "actual_value"


class TestFormattingUtilsCoverage:
    """Coverage for formatting utilities."""
    
    def test_format_duration_edge_cases(self):
        """Test format_duration edge cases."""
        from provide.foundation.utils.formatting import format_duration
        
        # Test zero duration
        result = format_duration(0)
        assert "0ms" in result or "0s" in result
        
        # Test very small duration
        result = format_duration(0.0001)
        assert "ms" in result
        
        # Test very large duration (days)
        large_duration = 90061  # 1 day + 1 hour + 1 minute + 1 second
        result = format_duration(large_duration)
        assert "d" in result or "h" in result
    
    def test_format_bytes_edge_cases(self):
        """Test format_bytes edge cases."""
        from provide.foundation.utils.formatting import format_bytes
        
        # Test zero bytes
        result = format_bytes(0)
        assert "0 B" in result
        
        # Test 1 byte
        result = format_bytes(1)
        assert "1 B" in result
        
        # Test large values (TB, PB)
        tb_size = 1024 ** 4
        result = format_bytes(tb_size)
        assert "TB" in result
    
    def test_truncate_string_edge_cases(self):
        """Test truncate_string edge cases."""
        from provide.foundation.utils.formatting import truncate_string
        
        # Test with custom suffix
        result = truncate_string("very long string", max_length=5, suffix="...")
        assert result.endswith("...")
        assert len(result) <= 8  # 5 + len("...")
        
        # Test empty string
        result = truncate_string("", max_length=10)
        assert result == ""
        
        # Test None input
        result = truncate_string(None, max_length=10)
        assert result == "None"


class TestParsingUtilsMoreCoverage:
    """Additional parsing utilities coverage."""
    
    def test_parse_list_edge_cases(self):
        """Test parse_list edge cases."""
        from provide.foundation.utils.parsing import parse_list
        
        # Test with custom separator
        result = parse_list("a|b|c", separator="|")
        assert result == ["a", "b", "c"]
        
        # Test with trailing/leading whitespace
        result = parse_list("  a  ,  b  ,  c  ")
        assert result == ["a", "b", "c"]
        
        # Test empty elements
        result = parse_list("a,,c")
        assert result == ["a", "", "c"]
    
    def test_parse_dict_edge_cases(self):
        """Test parse_dict edge cases.""" 
        from provide.foundation.utils.parsing import parse_dict
        
        # Test with custom separators
        result = parse_dict("key1:val1;key2:val2", item_sep=";", key_val_sep=":")
        assert result == {"key1": "val1", "key2": "val2"}
        
        # Test with empty values
        result = parse_dict("key1=,key2=val2")
        assert result == {"key1": "", "key2": "val2"}
        
        # Test malformed pairs (missing =)
        result = parse_dict("key1=val1,invalid_pair,key3=val3")
        assert "key1" in result
        assert "key3" in result
        # Should skip malformed pair
    
    def test_parse_duration_edge_cases(self):
        """Test parse_duration edge cases."""
        from provide.foundation.utils.parsing import parse_duration
        
        # Test fractional values
        result = parse_duration("1.5s")
        assert result == 1.5
        
        # Test case insensitive units
        result = parse_duration("1H")  
        assert result == 3600
        
        result = parse_duration("1D")
        assert result == 86400
    
    def test_parse_size_edge_cases(self):
        """Test parse_size edge cases."""
        from provide.foundation.utils.parsing import parse_size
        
        # Test fractional sizes
        result = parse_size("1.5KB")
        assert result == int(1.5 * 1024)
        
        # Test case insensitive units  
        result = parse_size("1kb")
        assert result == 1024
        
        # Test with spaces
        result = parse_size("1 MB")
        assert result == 1024 * 1024


class TestStreamsUtilsCoverage:
    """Coverage for streams utilities."""
    
    def test_get_foundation_log_stream_edge_cases(self):
        """Test get_foundation_log_stream edge cases."""
        from provide.foundation.utils.streams import get_foundation_log_stream
        
        # Test with invalid target (should fall back to stderr)
        stream = get_foundation_log_stream("invalid_target")
        assert stream is not None
        
        # Test case insensitive
        stream = get_foundation_log_stream("STDOUT")
        assert stream is not None
        
        stream = get_foundation_log_stream("STDERR")
        assert stream is not None
    
    def test_terminal_detection_with_mocks(self):
        """Test terminal detection functions."""
        from unittest.mock import patch
        from provide.foundation.utils.streams import get_terminal_width, supports_color
        
        # Test terminal width fallback
        with patch('shutil.get_terminal_size', side_effect=OSError):
            width = get_terminal_width()
            assert width == 80  # Default fallback
        
        # Test color support detection
        with patch.dict('os.environ', {'TERM': 'xterm-256color'}):
            result = supports_color()
            assert isinstance(result, bool)


class TestTimingUtilsMoreCoverage:
    """Additional timing utilities coverage."""
    
    def test_timer_manual_start_stop(self):
        """Test Timer with manual start/stop."""
        from provide.foundation.utils.timing import Timer
        import time
        
        timer = Timer()
        timer.start()
        time.sleep(0.01)
        timer.stop()
        
        assert timer.elapsed > 0
        assert timer.start_time is not None
        assert timer.end_time is not None
    
    def test_measure_time_with_args(self):
        """Test measure_time with function arguments."""
        from provide.foundation.utils.timing import measure_time
        
        def add_numbers(a, b, multiplier=1):
            return (a + b) * multiplier
        
        result, elapsed = measure_time(add_numbers, 2, 3, multiplier=2)
        assert result == 10  # (2 + 3) * 2
        assert elapsed >= 0
    
    def test_format_elapsed_precision(self):
        """Test format_elapsed with different precision."""
        from provide.foundation.utils.formatting import format_duration
        
        # Test microsecond precision
        result = format_duration(0.000001)  # 1 microsecond
        assert "μs" in result or "us" in result or "ms" in result
