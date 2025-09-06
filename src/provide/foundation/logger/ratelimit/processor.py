#
# processor.py
#
"""
Structlog processor for rate limiting log messages.
"""

import time
from typing import Any

import structlog

from provide.foundation.logger.ratelimit.limiters import GlobalRateLimiter


class RateLimiterProcessor:
    """
    Structlog processor that applies rate limiting to log messages.
    Can be configured with global and per-logger rate limits.
    """
    
    def __init__(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
    ):
        """
        Initialize the rate limiter processor.
        
        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds
        
        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}
        
        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = 60.0  # Emit summary every 60 seconds
    
    def __call__(
        self, 
        logger: Any, 
        method_name: str, 
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """
        Process a log event, applying rate limiting.
        
        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary
            
        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited
        """
        logger_name = event_dict.get("logger_name", "unknown")
        
        # Check if this log is allowed
        allowed, reason = self.rate_limiter.is_allowed(logger_name)
        
        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1
            
            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)
                
                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now
                    
                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }
            
            # Drop the event
            raise structlog.DropEvent
        
        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            if self.suppressed_counts:
                # Log summary of suppressed messages
                # This will be processed in the next iteration
                self._emit_summary()
                self.last_summary_time = now
        
        return event_dict
    
    def _emit_summary(self):
        """Emit a summary of rate-limited messages."""
        if not self.suppressed_counts:
            return
            
        total_suppressed = sum(self.suppressed_counts.values())
        
        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger
            summary_logger = get_logger("provide.foundation.ratelimit.summary")
            
            summary_logger.info(
                f"📊 Rate limit summary: {total_suppressed} messages suppressed",
                suppressed_by_logger=dict(self.suppressed_counts),
                stats=self.rate_limiter.get_stats(),
            )
            
            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()


def create_rate_limiter_processor(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
) -> RateLimiterProcessor:
    """
    Factory function to create and configure a rate limiter processor.
    
    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        
    Returns:
        Configured RateLimiterProcessor instance
    """
    processor = RateLimiterProcessor(emit_warning_on_limit=emit_warnings)
    
    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
    )
    
    return processor