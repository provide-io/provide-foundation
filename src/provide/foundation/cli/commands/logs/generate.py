from __future__ import annotations

import random
import threading
import time
from typing import TYPE_CHECKING, Any, NoReturn

from provide.foundation.logger import get_logger

if TYPE_CHECKING:
    import click

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None  # type: ignore[assignment]
    _HAS_CLICK = False

"""Command to generate logs for testing OpenObserve integration with Foundation's rate limiting."""

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


def generate_log_entry(index: int, style: str = "normal", error_rate: float = 0.1) -> dict[str, Any]:
    """Generate a single log entry with optional error simulation.

    Args:
        index: Log entry index
        style: Style of log generation ("normal" or "burroughs")
        error_rate: Probability of generating an error log (0.0 to 1.0)

    Returns:
        Dict containing log entry data

    """
    # Choose message based on style
    if style == "burroughs":
        message = random.choice(BURROUGHS_PHRASES)  # nosec B311 - Test data generation
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
        message = f"Successfully {random.choice(operations)} {random.choice(objects)}"  # nosec B311 - Test data

    # Generate error condition
    is_error = random.random() < error_rate  # nosec B311 - Test data generation

    # Base entry
    entry = {
        "message": message,
        "service": random.choice(SERVICE_NAMES),  # nosec B311 - Test data
        "operation": random.choice(OPERATIONS),  # nosec B311 - Test data
        "iteration": index,
        "trace_id": generate_trace_id() if index % 10 == 0 else f"trace_{(_trace_counter - 1):08d}",
        "span_id": generate_span_id(),
        "duration_ms": random.randint(10, 5000),  # nosec B311 - Test data
    }

    # Add error fields if this is an error
    if is_error:
        entry["level"] = "error"
        entry["error_code"] = random.choice([400, 404, 500, 503])  # nosec B311 - Test data
        entry["error_type"] = random.choice(  # nosec B311 - Test data
            [
                "ValidationError",
                "ServiceUnavailable",
                "TimeoutError",
                "DatabaseError",
                "RateLimitExceeded",
            ],
        )
    else:
        # Random log level for non-errors
        entry["level"] = random.choice(["debug", "info", "warning"])  # nosec B311 - Test data

    # Add domain/action/status for DAS emoji system
    entry["domain"] = random.choice(["user", "system", "data", "api", None])  # nosec B311 - Test data
    entry["action"] = random.choice(["create", "read", "update", "delete", None])  # nosec B311 - Test data
    entry["status"] = "error" if is_error else random.choice(["success", "pending", None])  # nosec B311 - Test data

    return entry


def _print_generation_config(
    count: int,
    rate: float,
    stream: str,
    style: str,
    error_rate: float,
    enable_rate_limit: bool,
    rate_limit: float,
) -> None:
    """Print the configuration for log generation."""
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

    click.echo("   Press Ctrl+C to stop\n")


def _configure_rate_limiter(enable_rate_limit: bool, rate_limit: float) -> None:
    """Configure Foundation's rate limiting if enabled."""
    if enable_rate_limit:
        from provide.foundation.logger.ratelimit import GlobalRateLimiter

        limiter = GlobalRateLimiter()
        limiter.configure(
            global_rate=rate_limit,
            global_capacity=rate_limit * 2,  # Allow burst up to 2x the rate
        )


def _send_log_entry(
    entry: dict[str, Any], logs_sent: int, logs_failed: int, logs_rate_limited: int
) -> tuple[int, int, int]:
    """Send a log entry and update counters."""
    try:
        service_logger = get_logger(f"generated.{entry['service']}")
        level = entry.pop("level", "info")
        message = entry.pop("message")
        getattr(service_logger, level)(message, **entry)
        logs_sent += 1
    except Exception as e:
        logs_failed += 1
        if "rate limit" in str(e).lower():
            logs_rate_limited += 1
    return logs_sent, logs_failed, logs_rate_limited


def _print_stats(
    current_time: float,
    last_stats_time: float,
    logs_sent: int,
    last_stats_sent: int,
    logs_failed: int,
    enable_rate_limit: bool,
    logs_rate_limited: int,
) -> tuple[float, int]:
    """Print generation statistics and return updated tracking values."""
    if current_time - last_stats_time >= 1.0:
        current_rate = (logs_sent - last_stats_sent) / (current_time - last_stats_time)

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def _print_final_stats(
    logs_sent: int,
    logs_failed: int,
    logs_rate_limited: int,
    total_time: float,
    rate: float,
    enable_rate_limit: bool,
) -> None:
    """Print final generation statistics."""
    actual_rate = logs_sent / total_time if total_time > 0 else 0

    click.echo("\n📊 Generation complete:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def _generate_continuous_logs(
    rate: float, style: str, error_rate: float, enable_rate_limit: bool, logs_rate_limited: int
) -> tuple[int, int, int]:
    """Generate logs in continuous mode."""
    logs_sent = 0
    logs_failed = 0
    start_time = time.time()
    last_stats_time = start_time
    last_stats_sent = 0
    index = 0

    while True:
        current_time = time.time()

        # Generate and send log entry
        entry = generate_log_entry(index, style, error_rate)
        index += 1
        logs_sent, logs_failed, logs_rate_limited = _send_log_entry(
            entry, logs_sent, logs_failed, logs_rate_limited
        )

        # Control rate
        elapsed = current_time - start_time
        expected_count = int(elapsed * rate)

        if logs_sent >= expected_count:
            next_time = start_time + (logs_sent / rate)
            sleep_time = next_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)

        # Print stats
        last_stats_time, last_stats_sent = _print_stats(
            current_time,
            last_stats_time,
            logs_sent,
            last_stats_sent,
            logs_failed,
            enable_rate_limit,
            logs_rate_limited,
        )


def _generate_fixed_count_logs(count: int, rate: float, style: str, error_rate: float) -> tuple[int, int, int]:
    """Generate a fixed number of logs."""
    logs_sent = 0
    logs_failed = 0
    logs_rate_limited = 0

    for i in range(count):
        entry = generate_log_entry(i, style, error_rate)
        logs_sent, logs_failed, logs_rate_limited = _send_log_entry(
            entry, logs_sent, logs_failed, logs_rate_limited
        )

        # Control rate
        if rate > 0:
            time.sleep(1.0 / rate)

        # Print progress
        if (i + 1) % max(1, count // 10) == 0:
            progress = (i + 1) / count * 100
            click.echo(f"Progress: {progress:.0f}% ({i + 1}/{count})")

    return logs_sent, logs_failed, logs_rate_limited


@click.command(name="generate")
@click.option("-n", "--count", default=100, help="Number of logs to generate (0 for continuous)")
@click.option("-r", "--rate", default=10.0, help="Logs per second rate")
@click.option("-s", "--stream", default="default", help="Target stream name")
@click.option(
    "--style",
    type=click.Choice(["normal", "burroughs"]),
    default="normal",
    help="Message generation style",
)
@click.option("-e", "--error-rate", default=0.1, help="Error rate (0.0 to 1.0)")
@click.option("--enable-rate-limit", is_flag=True, help="Enable Foundation's rate limiting")
@click.option("--rate-limit", default=100.0, help="Rate limit (logs/s) when enabled")
def generate_logs_command(
    count: int,
    rate: float,
    stream: str,
    style: str,
    error_rate: float,
    enable_rate_limit: bool,
    rate_limit: float,
) -> None:
    """Generate logs to test OpenObserve integration with Foundation's rate limiting."""
    _print_generation_config(count, rate, stream, style, error_rate, enable_rate_limit, rate_limit)
    _configure_rate_limiter(enable_rate_limit, rate_limit)

    start_time = time.time()
    logs_sent = logs_failed = logs_rate_limited = 0

    try:
        if count == 0:
            logs_sent, logs_failed, logs_rate_limited = _generate_continuous_logs(
                rate,
                style,
                error_rate,
                enable_rate_limit,
                logs_rate_limited,
            )
        else:
            logs_sent, logs_failed, logs_rate_limited = _generate_fixed_count_logs(
                count,
                rate,
                style,
                error_rate,
            )
    except KeyboardInterrupt:
        click.echo("\n\n⛔ Generation interrupted by user")
    finally:
        total_time = time.time() - start_time
        _print_final_stats(logs_sent, logs_failed, logs_rate_limited, total_time, rate, enable_rate_limit)


if not _HAS_CLICK:  # type: ignore[misc]

    def generate_logs_command(*args: object, **kwargs: object) -> NoReturn:
        raise ImportError("Click is required for CLI commands. Install with: pip install click")
