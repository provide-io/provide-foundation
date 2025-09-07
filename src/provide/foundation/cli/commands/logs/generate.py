#
# generate.py
#
"""
Command to generate logs for testing OpenObserve integration with Foundation's rate limiting.
"""

import random
import time
from typing import Any

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False

import threading

from provide.foundation.logger import get_logger

log = get_logger(__name__)

# Cut-up phrases inspired by Burroughs
BURROUGHS_PHRASES = [
    "mutated Soft Machine prescribed within data stream",
    "pre-recorded talking asshole dissolved into under neon hum",
    "the viral Word carrying a new strain of reality",
    "memory banks spilling future-pasts onto the terminal floor",
    "the soft typewriter of the Other Half",
    "control mechanisms broadcast in reversed time signatures",
    "equations of control flickering on a broken monitor",
    "semantic disturbances in Sector 9",
    "the Biologic Courts passing sentence in a dream",
    "a thousand junk units screaming in unison",
    "frequency shift reported by Sector 5",
    "the algebra of need written in neural static",
]

# Service names
SERVICE_NAMES = [
    "api-gateway",
    "auth-service",
    "user-service",
    "payment-processor",
    "notification-service",
    "search-index",
    "cache-layer",
    "data-pipeline",
    "ml-inference",
    "report-generator",
    "webhook-handler",
    "queue-processor",
    "stream-analyzer",
    "batch-job",
    "cron-scheduler",
    "interzone-terminal",
    "nova-police",
    "reality-studio",
]

# Operations
OPERATIONS = [
    "process_request",
    "validate_input",
    "execute_query",
    "transform_data",
    "send_notification",
    "update_cache",
    "sync_state",
    "aggregate_metrics",
    "encode_response",
    "decode_request",
    "authorize_access",
    "refresh_token",
    "persist_data",
    "emit_event",
    "handle_error",
    "transmit_signal",
    "intercept_word",
    "decode_reality",
]

# Trace and span ID tracking
_trace_counter = 0
_span_counter = 0
_trace_lock = threading.Lock()


def generate_trace_id() -> str:
    """Generate a unique trace ID."""
    global _trace_counter
    with _trace_lock:
        trace_id = f"trace_{_trace_counter:08d}"
        _trace_counter += 1
    return trace_id


def generate_span_id() -> str:
    """Generate a unique span ID."""
    global _span_counter
    with _trace_lock:
        span_id = f"span_{_span_counter:08d}"
        _span_counter += 1
    return span_id


def generate_log_entry(
    index: int, style: str = "normal", error_rate: float = 0.1
) -> dict[str, Any]:
    """
    Generate a single log entry with optional error simulation.

    Args:
        index: Log entry index
        style: Style of log generation ("normal" or "burroughs")
        error_rate: Probability of generating an error log (0.0 to 1.0)

    Returns:
        Dict containing log entry data
    """
    # Choose message based on style
    if style == "burroughs":
        message = random.choice(BURROUGHS_PHRASES)
    else:
        # Normal tech-style messages
        operations = [
            "processed",
            "validated",
            "executed",
            "transformed",
            "cached",
            "synced",
        ]
        objects = ["request", "query", "data", "event", "message", "transaction"]
        message = f"Successfully {random.choice(operations)} {random.choice(objects)}"

    # Generate error condition
    is_error = random.random() < error_rate

    # Base entry
    entry = {
        "message": message,
        "service": random.choice(SERVICE_NAMES),
        "operation": random.choice(OPERATIONS),
        "iteration": index,
        "trace_id": generate_trace_id()
        if index % 10 == 0
        else f"trace_{(_trace_counter - 1):08d}",
        "span_id": generate_span_id(),
        "duration_ms": random.randint(10, 5000),
    }

    # Add error fields if this is an error
    if is_error:
        entry["level"] = "error"
        entry["error_code"] = random.choice([400, 404, 500, 503])
        entry["error_type"] = random.choice(
            [
                "ValidationError",
                "ServiceUnavailable",
                "TimeoutError",
                "DatabaseError",
                "RateLimitExceeded",
            ]
        )
    else:
        # Random log level for non-errors
        entry["level"] = random.choice(["debug", "info", "warning"])

    # Add domain/action/status for DAS emoji system
    entry["domain"] = random.choice(["user", "system", "data", "api", None])
    entry["action"] = random.choice(["create", "read", "update", "delete", None])
    entry["status"] = (
        "error" if is_error else random.choice(["success", "pending", None])
    )

    return entry


@click.command(name="generate")
@click.option(
    "-n", "--count", default=100, help="Number of logs to generate (0 for continuous)"
)
@click.option("-r", "--rate", default=10.0, help="Logs per second rate")
@click.option("-s", "--stream", default="default", help="Target stream name")
@click.option(
    "--style",
    type=click.Choice(["normal", "burroughs"]),
    default="normal",
    help="Message generation style",
)
@click.option("-e", "--error-rate", default=0.1, help="Error rate (0.0 to 1.0)")
@click.option(
    "--enable-rate-limit", is_flag=True, help="Enable Foundation's rate limiting"
)
@click.option("--rate-limit", default=100.0, help="Rate limit (logs/s) when enabled")
def generate_logs_command(
    count: int,
    rate: float,
    stream: str,
    style: str,
    error_rate: float,
    enable_rate_limit: bool,
    rate_limit: float,
):
    """Generate logs to test OpenObserve integration with Foundation's rate limiting."""

    click.echo("🚀 Starting log generation...")
    click.echo(f"   Style: {style}")
    click.echo(f"   Error rate: {int(error_rate * 100)}%")
    click.echo(f"   Target stream: {stream}")

    if count == 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

        # Configure Foundation's rate limiting
        from provide.foundation.logger.ratelimit import GlobalRateLimiter

        limiter = GlobalRateLimiter()
        limiter.configure(
            global_rate=rate_limit,
            global_capacity=rate_limit * 2,  # Allow burst up to 2x the rate
        )

    click.echo("   Press Ctrl+C to stop\n")

    # Track statistics
    logs_sent = 0
    logs_failed = 0
    logs_rate_limited = 0
    start_time = time.time()
    last_stats_time = start_time
    last_stats_sent = 0

    try:
        if count == 0:
            # Continuous mode
            index = 0
            while True:
                current_time = time.time()

                # Generate log entry
                entry = generate_log_entry(index, style, error_rate)
                index += 1

                # Send using Foundation's logger
                try:
                    service_logger = get_logger(f"generated.{entry['service']}")

                    # Extract level and remove from entry
                    level = entry.pop("level", "info")
                    message = entry.pop("message")

                    # Log at appropriate level
                    getattr(service_logger, level)(message, **entry)
                    logs_sent += 1

                except Exception as e:
                    logs_failed += 1
                    if "rate limit" in str(e).lower():
                        logs_rate_limited += 1

                # Control rate
                target_interval = 1.0 / rate
                elapsed = current_time - start_time
                expected_count = int(elapsed * rate)

                if logs_sent < expected_count:
                    # We're behind, no sleep
                    pass
                else:
                    # We're on track or ahead, sleep until next interval
                    next_time = start_time + (logs_sent / rate)
                    sleep_time = next_time - time.time()
                    if sleep_time > 0:
                        time.sleep(sleep_time)

                # Print stats every second
                if current_time - last_stats_time >= 1.0:
                    current_rate = (logs_sent - last_stats_sent) / (
                        current_time - last_stats_time
                    )

                    status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
                    if logs_failed > 0:
                        status += f" | Failed: {logs_failed:,}"
                    if enable_rate_limit and logs_rate_limited > 0:
                        status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

                    click.echo(status)
                    last_stats_time = current_time
                    last_stats_sent = logs_sent

        else:
            # Fixed count mode
            for i in range(count):
                # Generate log entry
                entry = generate_log_entry(i, style, error_rate)

                # Send using Foundation's logger
                try:
                    service_logger = get_logger(f"generated.{entry['service']}")

                    # Extract level and remove from entry
                    level = entry.pop("level", "info")
                    message = entry.pop("message")

                    # Log at appropriate level
                    getattr(service_logger, level)(message, **entry)
                    logs_sent += 1

                except Exception as e:
                    logs_failed += 1
                    if "rate limit" in str(e).lower():
                        logs_rate_limited += 1

                # Control rate
                if rate > 0:
                    time.sleep(1.0 / rate)

                # Print progress
                if (i + 1) % max(1, count // 10) == 0:
                    progress = (i + 1) / count * 100
                    click.echo(f"Progress: {progress:.0f}% ({i + 1}/{count})")

    except KeyboardInterrupt:
        click.echo("\n\n⛔ Generation interrupted by user")

    finally:
        # Print final statistics
        total_time = time.time() - start_time
        actual_rate = logs_sent / total_time if total_time > 0 else 0

        click.echo("\n📊 Generation complete:")
        click.echo(f"   Total sent: {logs_sent} logs")
        click.echo(f"   Total failed: {logs_failed} logs")
        if enable_rate_limit:
            click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
        click.echo(f"   Time: {total_time:.2f}s")
        click.echo(f"   Target rate: {rate} logs/second")
        click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


if not _HAS_CLICK:

    def generate_logs_command(*args, **kwargs):
        raise ImportError(
            "Click is required for CLI commands. Install with: pip install click"
        )
