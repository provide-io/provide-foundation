"""
Generate test logs command for Foundation CLI.

Incorporates creative prose inspired by William S. Burroughs and the cut-up technique.
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

from provide.foundation.logger import get_logger

log = get_logger(__name__)


# Cut-up phrases inspired by Burroughs
BURROUGHS_PHRASES = [
    "mutated Soft Machine prescribed within data stream",
    "pre-recorded talking asshole dissolved into under neon hum",
    "the viral Word carrying a new strain of reality",
    "equations of control flickering on a broken monitor",
    "memory banks spilling future-pasts onto the terminal floor",
    "a thousand junk units screaming in unison",
    "the algebra of need computed by the Nova Mob",
    "subliminal commands embedded in the white noise",
    "the Biologic Courts passing sentence in a dream",
    "Nova Police raiding the reality studio",
    "the soft typewriter of the Other Half",
    "a flickering hologram of Hassan i Sabbah",
    "contaminated data feed from the Crab Nebula",
    "thought-forms materializing in the Interzone",
    "frequency shift reported by Sector 5",
]

# Standard technical messages
TECHNICAL_MESSAGES = [
    "Request processed successfully",
    "Database connection established",
    "Cache invalidated",
    "User authenticated",
    "Session initiated",
    "Transaction completed",
    "Queue message processed",
    "Health check passed",
    "Metrics exported",
    "Configuration reloaded",
    "Backup completed",
    "Index rebuilt",
    "Connection pool recycled",
    "Rate limit enforced",
    "Circuit breaker triggered",
]

# Services and operations for realistic logs
SERVICES = [
    "api-gateway",
    "auth-service",
    "payment-processor",
    "user-service",
    "notification-engine",
    "data-pipeline",
    "cache-layer",
    "search-index",
    "reality-studio",
    "interzone-terminal",
    "nova-police",
    "soft-machine",
]

OPERATIONS = [
    "handle_request",
    "process_data",
    "validate_input",
    "execute_query",
    "send_notification",
    "update_cache",
    "compute_metrics",
    "sync_state",
    "transmit_signal",
    "decode_reality",
    "intercept_word",
    "scan_frequency",
]

DOMAINS = [
    "transmission",
    "control",
    "reality",
    "system",
    "network",
    "quantum",
    "temporal",
    "dimensional",
    "biologic",
    "viral",
]

ACTIONS = [
    "broadcast",
    "receive",
    "process",
    "analyze",
    "detect",
    "mutate",
    "dissolve",
    "compute",
    "raid",
    "intercept",
]

STATUSES = [
    "nominal",
    "degraded",
    "critical",
    "optimal",
    "unstable",
    "fluctuating",
    "synchronized",
    "divergent",
    "contaminated",
    "clean",
]


if _HAS_CLICK:

    @click.command("generate")
    @click.option(
        "--count",
        "-n",
        type=int,
        default=100,
        help="Number of logs to generate (0 for continuous)",
    )
    @click.option(
        "--rate",
        "-r",
        type=float,
        default=10.0,
        help="Target logs per second (can go up to 10000/s)",
    )
    @click.option(
        "--style",
        type=click.Choice(["technical", "burroughs", "mixed"]),
        default="mixed",
        help="Log message style",
    )
    @click.option(
        "--error-rate",
        type=float,
        default=0.1,
        help="Percentage of error logs (0.0 to 1.0)",
    )
    @click.option(
        "--services",
        help="Comma-separated list of services (uses defaults if not provided)",
    )
    @click.option(
        "--stream",
        default="default",
        help="Target stream for logs",
    )
    @click.option(
        "--batch-size",
        type=int,
        default=10,
        help="Number of logs to send in each batch",
    )
    @click.option(
        "--with-traces",
        is_flag=True,
        default=True,
        help="Generate trace IDs for correlation",
    )
    @click.pass_context
    def generate_command(
        ctx, count, rate, style, error_rate, services, stream, batch_size, with_traces
    ):
        """Generate test logs with optional Burroughs-inspired prose.

        Examples:
            # Generate 100 test logs
            foundation logs generate -n 100

            # Generate continuous logs at 5/second
            foundation logs generate -n 0 -r 5

            # Generate with Burroughs-style messages
            foundation logs generate --style burroughs

            # Generate with 20% error rate
            foundation logs generate --error-rate 0.2

            # Generate for specific services
            foundation logs generate --services "api,auth,payment"
        """

        client = ctx.obj.get("client")

        # Parse services
        if services:
            service_list = [s.strip() for s in services.split(",")]
        else:
            service_list = SERVICES

        click.echo("🚀 Starting log generation...")
        click.echo(f"   Style: {style}")
        click.echo(f"   Error rate: {error_rate * 100:.0f}%")
        click.echo(f"   Target stream: {stream}")
        if count == 0:
            click.echo(f"   Mode: Continuous at {rate} logs/second")
        else:
            click.echo(f"   Count: {count} logs")
        click.echo("   Press Ctrl+C to stop\n")

        def generate_message(style: str, index: int) -> tuple[str, str]:
            """Generate a log message based on style."""
            if style == "burroughs":
                message = random.choice(BURROUGHS_PHRASES)
                level = random.choice(["TRACE", "DEBUG", "INFO", "WARN", "ERROR"])
            elif style == "technical":
                message = random.choice(TECHNICAL_MESSAGES)
                level = random.choice(["DEBUG", "INFO", "WARN"] * 3 + ["ERROR"])
            else:  # mixed
                if random.random() > 0.7:
                    message = random.choice(BURROUGHS_PHRASES)
                    level = random.choice(["TRACE", "DEBUG", "INFO", "WARN", "ERROR"])
                else:
                    message = random.choice(TECHNICAL_MESSAGES)
                    level = random.choice(["DEBUG", "INFO", "WARN"] * 3 + ["ERROR"])

            # Override level based on error rate
            if random.random() < error_rate:
                level = "ERROR"
                if style != "burroughs":
                    message = f"Error: {message}"

            return message, level

        def generate_log_entry(index: int) -> dict[str, Any]:
            """Generate a single log entry."""
            message, level = generate_message(style, index)
            service = random.choice(service_list)
            operation = random.choice(OPERATIONS)

            entry = {
                "message": f"[{service}] {message}",
                "level": level,
                "service": service,
                "operation": operation,
                "domain": random.choice(DOMAINS),
                "action": random.choice(ACTIONS),
                "status": "degraded" if level == "ERROR" else random.choice(STATUSES),
                "duration_ms": random.randint(10, 5000),
                "iteration": index,
            }

            # Add trace correlation
            if with_traces:
                # Group logs by trace (5-10 logs per trace)
                trace_group = index // random.randint(5, 10)
                entry["trace_id"] = f"trace_{trace_group:08x}"
                entry["span_id"] = f"span_{index:08x}"

            # Add error details
            if level == "ERROR":
                entry["error_code"] = random.choice([400, 404, 500, 502, 503])
                entry["error_type"] = random.choice(
                    [
                        "ConnectionTimeout",
                        "ValidationError",
                        "DatabaseError",
                        "ServiceUnavailable",
                    ]
                )

            return entry

        try:
            logs_sent = 0
            logs_failed = 0
            logs_rate_limited = 0
            start_time = time.time()
            last_stats_time = start_time
            last_stats_sent = 0

            # Set up rate limiter
            # Configure with the target rate and a reasonable burst size
            rate_limiter = SimpleSyncRateLimiter(
                capacity=min(
                    rate * 2, 1000
                ),  # Allow burst up to 2 seconds worth or 1000
                refill_rate=rate,  # tokens per second
            )

            # Track rate limiting
            rate_limit_detected = False
            consecutive_failures = 0

            def send_log_with_tracking(entry):
                """Send log using Foundation's logger and track success/failure."""
                nonlocal \
                    logs_sent, \
                    logs_failed, \
                    logs_rate_limited, \
                    rate_limit_detected, \
                    consecutive_failures

                try:
                    # Get a logger for the service
                    service_logger = get_logger(f"generated.{entry['service']}")

                    # Use Foundation's logger with appropriate level
                    level = entry["level"].lower()
                    message = entry["message"]

                    # Remove message and level from attributes since they're passed separately
                    attrs = {
                        k: v for k, v in entry.items() if k not in ["message", "level"]
                    }

                    # Call the appropriate log level method
                    if level == "trace":
                        service_logger.trace(message, **attrs)
                    elif level == "debug":
                        service_logger.debug(message, **attrs)
                    elif level == "info":
                        service_logger.info(message, **attrs)
                    elif level == "warn" or level == "warning":
                        service_logger.warning(message, **attrs)
                    elif level == "error":
                        service_logger.error(message, **attrs)
                    elif level == "critical":
                        service_logger.critical(message, **attrs)
                    else:
                        service_logger.info(message, **attrs)

                    # Also send to OpenObserve if configured
                    if client:
                        from provide.foundation.observability.openobserve.otlp import (
                            send_log_bulk,
                        )

                        success = send_log_bulk(
                            message=message,
                            level=entry["level"],
                            service=entry["service"],
                            attributes=attrs,
                            client=client,
                        )
                        if not success:
                            logs_failed += 1
                            consecutive_failures += 1
                            if consecutive_failures >= 5 and not rate_limit_detected:
                                rate_limit_detected = True
                                logs_rate_limited = logs_failed
                            elif rate_limit_detected:
                                logs_rate_limited += 1
                            return False

                    logs_sent += 1
                    consecutive_failures = 0
                    return True

                except Exception as e:
                    log.debug(f"Failed to send log: {e}")
                    logs_failed += 1
                    consecutive_failures += 1
                    return False

            if count == 0:
                # Continuous mode using Foundation's rate limiter with async workers
                index = 0
                import concurrent.futures
                import queue

                # Work queue for async processing
                work_queue = queue.Queue(
                    maxsize=int(rate * 2)
                )  # Buffer up to 2 seconds of logs

                # Use thread pool for high-speed sending
                # More workers for higher rates
                num_workers = min(50, max(4, int(rate / 100)))

                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=num_workers
                ) as executor:
                    # Start worker threads
                    futures = []

                    def worker():
                        """Worker thread that processes logs from queue."""
                        while True:
                            try:
                                entry = work_queue.get(timeout=1)
                                if entry is None:  # Shutdown signal
                                    break
                                send_log_with_tracking(entry)
                                work_queue.task_done()
                            except queue.Empty:
                                continue

                    # Start workers
                    for _ in range(num_workers):
                        futures.append(executor.submit(worker))

                    while True:
                        current_time = time.time()

                        # Try to acquire a token from the rate limiter
                        if rate_limiter.acquire():
                            # Token acquired, generate and queue log
                            entry = generate_log_entry(index)
                            try:
                                work_queue.put_nowait(entry)
                                index += 1
                            except queue.Full:
                                # Queue is full, we're generating faster than sending
                                logs_rate_limited += 1
                                if not rate_limit_detected:
                                    rate_limit_detected = True
                                    log.warning(
                                        "⚠️ Queue full - cannot keep up with target rate"
                                    )
                        else:
                            # Rate limited - track it
                            logs_rate_limited += 1
                            if not rate_limit_detected:
                                rate_limit_detected = True
                                log.debug(
                                    "⚠️ Rate limiter activated - target rate exceeded"
                                )

                            # Small sleep to prevent busy waiting
                            time.sleep(0.0001)

                        # Print stats every second
                        if current_time - last_stats_time >= 1.0:
                            current_sent = logs_sent
                            current_rate = (current_sent - last_stats_sent) / (
                                current_time - last_stats_time
                            )
                            tokens_available = rate_limiter.tokens
                            queue_size = work_queue.qsize()

                            status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s | Tokens: {tokens_available:.0f}/{rate_limiter.capacity} | Queue: {queue_size}"
                            if logs_failed > 0:
                                status += f" | Failed: {logs_failed:,}"
                            if rate_limit_detected:
                                status += f" | ⚠️ RATE LIMITED ({logs_rate_limited:,} throttled)"

                            click.echo(status)
                            last_stats_time = current_time
                            last_stats_sent = current_sent

            else:
                # Fixed count mode using Foundation's rate limiter with async workers
                import concurrent.futures
                import queue

                # Work queue for async processing
                work_queue = queue.Queue(maxsize=min(1000, count))

                # Use thread pool for high-speed sending
                num_workers = min(50, max(4, int(rate / 100)))

                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=num_workers
                ) as executor:
                    # Start worker threads
                    def worker():
                        """Worker thread that processes logs from queue."""
                        while True:
                            try:
                                entry = work_queue.get(timeout=1)
                                if entry is None:  # Shutdown signal
                                    break
                                send_log_with_tracking(entry)
                                work_queue.task_done()
                            except queue.Empty:
                                continue

                    # Start workers
                    workers = [executor.submit(worker) for _ in range(num_workers)]

                    # Generate and queue logs
                    for i in range(count):
                        # Wait for rate limiter token
                        while not rate_limiter.acquire():
                            logs_rate_limited += 1
                            if not rate_limit_detected:
                                rate_limit_detected = True
                                log.debug(
                                    "⚠️ Rate limiter activated - target rate exceeded"
                                )
                            time.sleep(
                                0.0001
                            )  # Very small sleep to prevent busy waiting

                        # Generate and queue log
                        entry = generate_log_entry(i)
                        work_queue.put(entry)

                        # Print progress
                        if (i + 1) % 100 == 0:
                            current_time = time.time()
                            elapsed = current_time - start_time
                            current_rate = logs_sent / elapsed if elapsed > 0 else 0
                            tokens_available = rate_limiter.tokens
                            queue_size = work_queue.qsize()

                            status = f"📊 Progress: {i + 1}/{count} | Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s | Queue: {queue_size} | Tokens: {tokens_available:.0f}"
                            if logs_failed > 0:
                                status += f" | Failed: {logs_failed}"
                            if rate_limit_detected:
                                status += f" | ⚠️ THROTTLED ({logs_rate_limited:,})"

                            click.echo(status)

                    # Wait for queue to empty
                    click.echo("⏳ Waiting for queue to empty...")
                    work_queue.join()

                    # Shutdown workers
                    for _ in range(num_workers):
                        work_queue.put(None)

                    # Wait for workers to finish
                    concurrent.futures.wait(workers)

            elapsed = time.time() - start_time
            rate_actual = logs_sent / elapsed if elapsed > 0 else 0

            click.echo("\n📊 Generation complete:")
            click.echo(f"   Total sent: {logs_sent:,} logs")
            click.echo(f"   Total failed: {logs_failed:,} logs")
            if rate_limit_detected:
                click.echo(f"   ⚠️  Rate limited: {logs_rate_limited:,} logs")
            click.echo(f"   Time: {elapsed:.2f}s")
            click.echo(f"   Target rate: {rate:.0f} logs/second")
            click.echo(f"   Actual rate: {rate_actual:.1f} logs/second")
            if rate_limit_detected and rate_actual < rate * 0.5:
                click.echo(
                    f"   ⚠️  Rate limiting detected - actual rate is {(rate_actual / rate) * 100:.0f}% of target"
                )

        except KeyboardInterrupt:
            click.echo(f"\n✋ Stopped. Generated {logs_sent} logs.")
        except Exception as e:
            click.echo(f"Generation failed: {e}", err=True)
            return 1

else:

    def generate_command(*args, **kwargs):
        """Generate command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. "
            "Install with: pip install 'provide-foundation[cli]'"
        )
