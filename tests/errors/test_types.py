"""Tests for provide.foundation.errors.types module."""

import json
from datetime import datetime
from unittest.mock import patch

import pytest

from provide.foundation.errors.types import (
    BackoffStrategy,
    ErrorCode,
    ErrorMetadata,
    ErrorResponse,
    RetryPolicy,
)


class TestErrorCode:
    """Test ErrorCode enum."""
    
    def test_config_error_codes(self):
        """Test configuration error codes."""
        assert ErrorCode.CONFIG_INVALID.value == "CFG_001"
        assert ErrorCode.CONFIG_MISSING.value == "CFG_002"
        assert ErrorCode.CONFIG_PARSE_ERROR.value == "CFG_003"
        assert ErrorCode.CONFIG_TYPE_ERROR.value == "CFG_004"
    
    def test_validation_error_codes(self):
        """Test validation error codes."""
        assert ErrorCode.VALIDATION_TYPE.value == "VAL_001"
        assert ErrorCode.VALIDATION_RANGE.value == "VAL_002"
        assert ErrorCode.VALIDATION_FORMAT.value == "VAL_003"
        assert ErrorCode.VALIDATION_REQUIRED.value == "VAL_004"
        assert ErrorCode.VALIDATION_CONSTRAINT.value == "VAL_005"
    
    def test_integration_error_codes(self):
        """Test integration error codes."""
        assert ErrorCode.INTEGRATION_TIMEOUT.value == "INT_001"
        assert ErrorCode.INTEGRATION_AUTH.value == "INT_002"
        assert ErrorCode.INTEGRATION_UNAVAILABLE.value == "INT_003"
        assert ErrorCode.INTEGRATION_RATE_LIMIT.value == "INT_004"
        assert ErrorCode.INTEGRATION_PROTOCOL.value == "INT_005"
    
    def test_resource_error_codes(self):
        """Test resource error codes."""
        assert ErrorCode.RESOURCE_NOT_FOUND.value == "RES_001"
        assert ErrorCode.RESOURCE_LOCKED.value == "RES_002"
        assert ErrorCode.RESOURCE_PERMISSION.value == "RES_003"
        assert ErrorCode.RESOURCE_EXHAUSTED.value == "RES_004"
        assert ErrorCode.RESOURCE_CONFLICT.value == "RES_005"
    
    def test_auth_error_codes(self):
        """Test authentication/authorization error codes."""
        assert ErrorCode.AUTH_INVALID_CREDENTIALS.value == "AUTH_001"
        assert ErrorCode.AUTH_TOKEN_EXPIRED.value == "AUTH_002"
        assert ErrorCode.AUTH_INSUFFICIENT_PERMISSION.value == "AUTH_003"
        assert ErrorCode.AUTH_SESSION_INVALID.value == "AUTH_004"
        assert ErrorCode.AUTH_MFA_REQUIRED.value == "AUTH_005"
    
    def test_system_error_codes(self):
        """Test system error codes."""
        assert ErrorCode.SYSTEM_UNAVAILABLE.value == "SYS_001"
        assert ErrorCode.SYSTEM_OVERLOAD.value == "SYS_002"
        assert ErrorCode.SYSTEM_MAINTENANCE.value == "SYS_003"
        assert ErrorCode.SYSTEM_INTERNAL.value == "SYS_004"
        assert ErrorCode.SYSTEM_PANIC.value == "SYS_005"
    
    def test_error_code_is_string(self):
        """Test that error codes are strings."""
        assert isinstance(ErrorCode.CONFIG_INVALID.value, str)
        assert ErrorCode.VALIDATION_TYPE.value == "VAL_001"


class TestErrorMetadata:
    """Test ErrorMetadata class."""
    
    def test_default_creation(self):
        """Test creating ErrorMetadata with defaults."""
        meta = ErrorMetadata()
        
        assert meta.request_id is None
        assert meta.user_id is None
        assert meta.session_id is None
        assert meta.correlation_id is None
        assert meta.retry_count == 0
        assert meta.retry_after is None
        assert meta.help_url is None
        assert meta.support_id is None
    
    def test_creation_with_values(self):
        """Test creating ErrorMetadata with values."""
        meta = ErrorMetadata(
            request_id="req_123",
            user_id="usr_456",
            session_id="sess_789",
            correlation_id="corr_abc",
            retry_count=3,
            retry_after=30.0,
            help_url="https://help.example.com",
            support_id="ticket_xyz"
        )
        
        assert meta.request_id == "req_123"
        assert meta.user_id == "usr_456"
        assert meta.session_id == "sess_789"
        assert meta.correlation_id == "corr_abc"
        assert meta.retry_count == 3
        assert meta.retry_after == 30.0
        assert meta.help_url == "https://help.example.com"
        assert meta.support_id == "ticket_xyz"
    
    def test_to_dict_excludes_none(self):
        """Test that to_dict excludes None values."""
        meta = ErrorMetadata(
            request_id="req_123",
            retry_count=2
        )
        
        result = meta.to_dict()
        
        assert result == {
            "request_id": "req_123",
            "retry_count": 2
        }
        assert "user_id" not in result
        assert "session_id" not in result
    
    def test_to_dict_includes_zero_values(self):
        """Test that to_dict includes zero/false values."""
        meta = ErrorMetadata(retry_count=0, retry_after=0.0)
        
        result = meta.to_dict()
        
        assert result["retry_count"] == 0
        assert result["retry_after"] == 0.0


class TestBackoffStrategy:
    """Test BackoffStrategy enum."""
    
    def test_strategy_values(self):
        """Test backoff strategy values."""
        assert BackoffStrategy.FIXED.value == "fixed"
        assert BackoffStrategy.LINEAR.value == "linear"
        assert BackoffStrategy.EXPONENTIAL.value == "exponential"
        assert BackoffStrategy.FIBONACCI.value == "fibonacci"


class TestRetryPolicy:
    """Test RetryPolicy class."""
    
    def test_default_creation(self):
        """Test creating RetryPolicy with defaults."""
        policy = RetryPolicy()
        
        assert policy.max_attempts == 3
        assert policy.backoff == BackoffStrategy.EXPONENTIAL
        assert policy.base_delay == 1.0
        assert policy.max_delay == 60.0
        assert policy.jitter is True
        assert policy.retryable_errors is None
    
    def test_creation_with_values(self):
        """Test creating RetryPolicy with custom values."""
        policy = RetryPolicy(
            max_attempts=5,
            backoff=BackoffStrategy.LINEAR,
            base_delay=2.0,
            max_delay=30.0,
            jitter=False,
            retryable_errors=(ValueError, KeyError)
        )
        
        assert policy.max_attempts == 5
        assert policy.backoff == BackoffStrategy.LINEAR
        assert policy.base_delay == 2.0
        assert policy.max_delay == 30.0
        assert policy.jitter is False
        assert policy.retryable_errors == (ValueError, KeyError)
    
    def test_calculate_delay_fixed(self):
        """Test fixed backoff strategy."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.FIXED,
            base_delay=5.0,
            jitter=False
        )
        
        assert policy.calculate_delay(1) == 5.0
        assert policy.calculate_delay(2) == 5.0
        assert policy.calculate_delay(3) == 5.0
    
    def test_calculate_delay_linear(self):
        """Test linear backoff strategy."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.LINEAR,
            base_delay=2.0,
            jitter=False
        )
        
        assert policy.calculate_delay(1) == 2.0
        assert policy.calculate_delay(2) == 4.0
        assert policy.calculate_delay(3) == 6.0
    
    def test_calculate_delay_exponential(self):
        """Test exponential backoff strategy."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=2.0,
            jitter=False
        )
        
        assert policy.calculate_delay(1) == 2.0  # 2 * 2^0
        assert policy.calculate_delay(2) == 4.0  # 2 * 2^1
        assert policy.calculate_delay(3) == 8.0  # 2 * 2^2
        assert policy.calculate_delay(4) == 16.0  # 2 * 2^3
    
    def test_calculate_delay_fibonacci(self):
        """Test fibonacci backoff strategy."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.FIBONACCI,
            base_delay=1.0,
            jitter=False
        )
        
        assert policy.calculate_delay(1) == 1.0  # fib(1) = 1
        assert policy.calculate_delay(2) == 1.0  # fib(2) = 1
        assert policy.calculate_delay(3) == 2.0  # fib(3) = 2
        assert policy.calculate_delay(4) == 3.0  # fib(4) = 3
        assert policy.calculate_delay(5) == 5.0  # fib(5) = 5
    
    def test_calculate_delay_max_cap(self):
        """Test that delay is capped at max_delay."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=10.0,
            max_delay=20.0,
            jitter=False
        )
        
        assert policy.calculate_delay(1) == 10.0
        assert policy.calculate_delay(2) == 20.0  # Would be 20, at cap
        assert policy.calculate_delay(3) == 20.0  # Would be 40, capped at 20
        assert policy.calculate_delay(10) == 20.0  # Still capped
    
    def test_calculate_delay_zero_attempt(self):
        """Test that zero or negative attempts return 0."""
        policy = RetryPolicy(jitter=False)
        
        assert policy.calculate_delay(0) == 0
        assert policy.calculate_delay(-1) == 0
    
    @patch('random.random')
    def test_calculate_delay_with_jitter(self, mock_random):
        """Test that jitter adds randomness."""
        # Mock random to return predictable values
        mock_random.return_value = 0.5  # Middle of range
        
        policy = RetryPolicy(
            backoff=BackoffStrategy.FIXED,
            base_delay=10.0,
            jitter=True
        )
        
        # With jitter, should be 10.0 * (0.75 + 0.5 * 0.5) = 10.0 * 1.0 = 10.0
        assert policy.calculate_delay(1) == 10.0
        
        # Test with different random value
        mock_random.return_value = 0.0  # Minimum
        assert policy.calculate_delay(1) == 7.5  # 10.0 * 0.75
        
        mock_random.return_value = 1.0  # Maximum
        assert policy.calculate_delay(1) == 12.5  # 10.0 * 1.25
    
    def test_calculate_delay_unknown_strategy(self):
        """Test fallback for unknown strategy."""
        policy = RetryPolicy(jitter=False)
        # Manually set invalid strategy
        policy.backoff = "invalid"  # type: ignore
        
        assert policy.calculate_delay(1) == 1.0  # Falls back to base_delay
    
    def test_should_retry_within_attempts(self):
        """Test should_retry within attempt limit."""
        policy = RetryPolicy(max_attempts=3)
        
        assert policy.should_retry(Exception(), 1) is True
        assert policy.should_retry(Exception(), 2) is True
        assert policy.should_retry(Exception(), 3) is False  # At limit
        assert policy.should_retry(Exception(), 4) is False  # Over limit
    
    def test_should_retry_with_retryable_errors(self):
        """Test should_retry with specific error types."""
        policy = RetryPolicy(
            max_attempts=5,
            retryable_errors=(ValueError, KeyError)
        )
        
        # Retryable errors
        assert policy.should_retry(ValueError(), 1) is True
        assert policy.should_retry(KeyError(), 1) is True
        
        # Non-retryable error
        assert policy.should_retry(TypeError(), 1) is False
        assert policy.should_retry(Exception(), 1) is False
    
    def test_should_retry_respects_both_conditions(self):
        """Test that both attempt limit and error type are checked."""
        policy = RetryPolicy(
            max_attempts=2,
            retryable_errors=(ValueError,)
        )
        
        # Within limit and retryable
        assert policy.should_retry(ValueError(), 1) is True
        
        # At limit but retryable type
        assert policy.should_retry(ValueError(), 2) is False
        
        # Within limit but not retryable
        assert policy.should_retry(TypeError(), 1) is False


class TestErrorResponse:
    """Test ErrorResponse class."""
    
    def test_creation_basic(self):
        """Test basic ErrorResponse creation."""
        response = ErrorResponse(
            error_code="VAL_001",
            message="Validation failed"
        )
        
        assert response.error_code == "VAL_001"
        assert response.message == "Validation failed"
        assert response.details is None
        assert response.metadata is None
        assert isinstance(response.timestamp, str)
    
    def test_creation_with_details(self):
        """Test ErrorResponse with details."""
        details = {"field": "email", "reason": "invalid format"}
        response = ErrorResponse(
            error_code="VAL_003",
            message="Email invalid",
            details=details
        )
        
        assert response.details == details
    
    def test_creation_with_metadata(self):
        """Test ErrorResponse with metadata."""
        meta = ErrorMetadata(request_id="req_123", retry_count=2)
        response = ErrorResponse(
            error_code="INT_001",
            message="Timeout",
            metadata=meta
        )
        
        assert response.metadata is meta
    
    def test_timestamp_format(self):
        """Test that timestamp is ISO format."""
        with patch('provide.foundation.errors.types.datetime') as mock_dt:
            mock_now = datetime(2024, 1, 1, 12, 0, 0)
            mock_dt.now.return_value = mock_now
            
            response = ErrorResponse(
                error_code="TEST",
                message="Test"
            )
            
            # The factory is called during class initialization
            # So we need to check the actual timestamp
            # It should be an ISO format string
            assert "T" in response.timestamp
            assert ":" in response.timestamp
    
    def test_to_dict_basic(self):
        """Test conversion to dictionary."""
        response = ErrorResponse(
            error_code="TEST_001",
            message="Test error",
            timestamp="2024-01-01T12:00:00"
        )
        
        result = response.to_dict()
        
        assert result == {
            "error_code": "TEST_001",
            "message": "Test error",
            "timestamp": "2024-01-01T12:00:00"
        }
    
    def test_to_dict_with_details(self):
        """Test to_dict with details."""
        response = ErrorResponse(
            error_code="TEST",
            message="Error",
            details={"key": "value"},
            timestamp="2024-01-01T12:00:00"
        )
        
        result = response.to_dict()
        
        assert result["details"] == {"key": "value"}
    
    def test_to_dict_with_metadata(self):
        """Test to_dict with metadata."""
        meta = ErrorMetadata(request_id="req_123", retry_count=1)
        response = ErrorResponse(
            error_code="TEST",
            message="Error",
            metadata=meta,
            timestamp="2024-01-01T12:00:00"
        )
        
        result = response.to_dict()
        
        assert result["metadata"] == {"request_id": "req_123", "retry_count": 1}
    
    def test_to_json(self):
        """Test JSON serialization."""
        response = ErrorResponse(
            error_code="TEST_001",
            message="Test error",
            details={"field": "value"},
            timestamp="2024-01-01T12:00:00"
        )
        
        json_str = response.to_json()
        parsed = json.loads(json_str)
        
        assert parsed["error_code"] == "TEST_001"
        assert parsed["message"] == "Test error"
        assert parsed["details"]["field"] == "value"
        assert parsed["timestamp"] == "2024-01-01T12:00:00"
    
    def test_to_json_formatting(self):
        """Test that JSON is properly formatted."""
        response = ErrorResponse(
            error_code="TEST",
            message="Error",
            timestamp="2024-01-01T12:00:00"
        )
        
        json_str = response.to_json()
        
        # Should be indented (2 spaces)
        assert "\n" in json_str
        assert "  " in json_str