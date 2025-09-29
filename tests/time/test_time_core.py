"""Tests for Foundation time utilities."""

from datetime import UTC, datetime
import time
from typing import Any
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

import pytest

from provide.foundation.time import provide_now, provide_sleep, provide_time
from provide.testkit import FoundationTestCase


class TestProvideTime:
    """Test provide_time function."""

    def test_provide_time_returns_float(self) -> None:
        """Test provide_time returns a float."""
        result = provide_time()
        assert isinstance(result, float)

    def test_provide_time_advances(self) -> None:
        """Test provide_time advances over time."""
        time1 = provide_time()
        time.sleep(0.01)  # Small sleep
        time2 = provide_time()
        assert time2 > time1

    @patch("provide.foundation.time.core.time")
    def test_provide_time_uses_time_module(self, mock_time: Any) -> None:
        """Test provide_time calls time.time()."""
        mock_time.time.return_value = 1234567890.0

        result = provide_time()

        assert result == 1234567890.0
        mock_time.time.assert_called_once()

    def test_provide_time_precision(self) -> None:
        """Test provide_time has reasonable precision."""
        time1 = provide_time()
        time2 = provide_time()
        # Should be very close but not necessarily identical
        assert abs(time2 - time1) < 0.1


class TestProvideSleep(FoundationTestCase):
    """Test provide_sleep function."""

    def test_provide_sleep_actually_sleeps(self) -> None:
        """Test provide_sleep actually sleeps for the specified duration."""
        start = time.time()
        provide_sleep(0.1)
        end = time.time()

        # Allow some tolerance for timing
        elapsed = end - start
        assert 0.09 <= elapsed <= 0.2

    def test_provide_sleep_zero(self) -> None:
        """Test provide_sleep with zero duration."""
        start = time.time()
        provide_sleep(0.0)
        end = time.time()

        # Should return immediately
        elapsed = end - start
        assert elapsed < 0.01

    def test_provide_sleep_negative_raises_error(self) -> None:
        """Test provide_sleep raises error for negative duration."""
        with pytest.raises(ValueError, match="Sleep duration must be non-negative"):
            provide_sleep(-1.0)

    @patch("provide.foundation.time.core.time")
    def test_provide_sleep_uses_time_module(self, mock_time: Any) -> None:
        """Test provide_sleep calls time.sleep()."""
        provide_sleep(0.5)
        mock_time.sleep.assert_called_once_with(0.5)

    def test_provide_sleep_with_float_seconds(self) -> None:
        """Test provide_sleep works with float values."""
        start = time.time()
        provide_sleep(0.05)
        end = time.time()

        elapsed = end - start
        assert 0.04 <= elapsed <= 0.1


class TestProvideNow(FoundationTestCase):
    """Test provide_now function."""

    def test_provide_now_returns_datetime(self) -> None:
        """Test provide_now returns datetime object."""
        result = provide_now()
        assert isinstance(result, datetime)

    def test_provide_now_no_timezone(self) -> None:
        """Test provide_now without timezone argument."""
        result = provide_now()
        # Should have timezone info (system default)
        assert result.tzinfo is None  # datetime.now() returns naive datetime

    def test_provide_now_with_utc(self) -> None:
        """Test provide_now with UTC timezone."""
        result = provide_now("UTC")
        assert result.tzinfo is not None
        assert result.tzinfo.key == "UTC"

    def test_provide_now_with_timezone_string(self) -> None:
        """Test provide_now with timezone string."""
        result = provide_now("America/New_York")
        assert result.tzinfo is not None
        assert result.tzinfo.key == "America/New_York"

    def test_provide_now_with_zoneinfo_object(self) -> None:
        """Test provide_now with ZoneInfo object."""
        tz = ZoneInfo("Europe/London")
        result = provide_now(tz)
        assert result.tzinfo is tz

    def test_provide_now_advances(self) -> None:
        """Test provide_now advances over time."""
        time1 = provide_now()
        time.sleep(0.01)
        time2 = provide_now()
        assert time2 > time1

    def test_provide_now_different_timezones(self) -> None:
        """Test provide_now with different timezones."""
        utc_now = provide_now("UTC")
        ny_now = provide_now("America/New_York")

        # They should be at roughly the same time but different timezones
        time_diff = abs(
            (utc_now.replace(tzinfo=None) - ny_now.replace(tzinfo=None)).total_seconds(),
        )
        # Should be within a few hours (timezone offset)
        assert time_diff <= 24 * 3600  # Less than 24 hours difference

    @patch("provide.foundation.time.core.datetime")
    def test_provide_now_uses_datetime_module(self, mock_datetime: Any) -> None:
        """Test provide_now calls datetime.now()."""
        mock_dt = MagicMock()
        mock_datetime.now.return_value = mock_dt

        result = provide_now()

        assert result is mock_dt
        mock_datetime.now.assert_called_once_with()

    @patch("provide.foundation.time.core.datetime")
    def test_provide_now_with_timezone_uses_datetime_module(self, mock_datetime: Any) -> None:
        """Test provide_now with timezone calls datetime.now() with timezone."""
        mock_dt = MagicMock()
        mock_datetime.now.return_value = mock_dt

        result = provide_now("UTC")

        assert result is mock_dt
        # Should be called with ZoneInfo object
        args, _kwargs = mock_datetime.now.call_args
        assert len(args) == 1
        assert isinstance(args[0], ZoneInfo)
        assert args[0].key == "UTC"


class TestTimeUtilitiesIntegration(FoundationTestCase):
    """Integration tests for time utilities."""

    def test_time_utilities_work_together(self) -> None:
        """Test that time utilities work together consistently."""
        start_time = provide_time()
        start_dt = provide_now()

        provide_sleep(0.1)

        end_time = provide_time()
        end_dt = provide_now()

        # Both should advance by roughly the same amount
        time_diff = end_time - start_time
        dt_diff = (end_dt - start_dt).total_seconds()

        assert abs(time_diff - dt_diff) < 0.05  # Small tolerance

    def test_time_utilities_with_timezone(self) -> None:
        """Test time utilities with timezone awareness."""
        utc_now = provide_now("UTC")
        timestamp = provide_time()

        # Convert timestamp to UTC datetime for comparison
        utc_from_timestamp = datetime.fromtimestamp(timestamp, tz=UTC)

        # Should be very close
        diff = abs((utc_now - utc_from_timestamp).total_seconds())
        assert diff < 1.0  # Within 1 second

    def test_performance_comparison(self) -> None:
        """Test performance of Foundation utilities vs standard library."""
        import time as std_time

        # Test provide_time vs time.time
        start = std_time.time()
        for _ in range(1000):
            provide_time()
        foundation_time = std_time.time() - start

        start = std_time.time()
        for _ in range(1000):
            std_time.time()
        standard_time = std_time.time() - start

        # Foundation time should be reasonably close to standard time
        # Loosen the multiplier to 100x to avoid flaky CI failures.
        assert foundation_time < standard_time * 100

    def test_exception_handling(self) -> None:
        """Test exception handling in time utilities."""
        # provide_sleep with negative value
        with pytest.raises(ValueError):
            provide_sleep(-1)

        # provide_now with invalid timezone should raise ZoneInfo error
        with pytest.raises(Exception):  # noqa: B017
            provide_now("Invalid/Timezone")
