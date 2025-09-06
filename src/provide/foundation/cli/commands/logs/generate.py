"""
Generate test logs command for Foundation CLI.

Incorporates creative prose inspired by William S. Burroughs and the cut-up technique.
"""

import asyncio
import random
import time
from datetime import datetime, timedelta
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
SERVICES = ["api-gateway", "auth-service", "payment-processor", "user-service", 
            "notification-engine", "data-pipeline", "cache-layer", "search-index",
            "reality-studio", "interzone-terminal", "nova-police", "soft-machine"]

OPERATIONS = ["handle_request", "process_data", "validate_input", "execute_query",
              "send_notification", "update_cache", "compute_metrics", "sync_state",
              "transmit_signal", "decode_reality", "intercept_word", "scan_frequency"]

DOMAINS = ["transmission", "control", "reality", "system", "network", 
           "quantum", "temporal", "dimensional", "biologic", "viral"]

ACTIONS = ["broadcast", "receive", "process", "analyze", "detect",
           "mutate", "dissolve", "compute", "raid", "intercept"]

STATUSES = ["nominal", "degraded", "critical", "optimal", "unstable",
            "fluctuating", "synchronized", "divergent", "contaminated", "clean"]


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
    def generate_command(ctx, count, rate, style, error_rate, services, stream, batch_size, with_traces):
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
        from provide.foundation.observability.openobserve.otlp import send_log
        
        client = ctx.obj.get("client")
        
        # Parse services
        if services:
            service_list = [s.strip() for s in services.split(",")]
        else:
            service_list = SERVICES
        
        click.echo(f"🚀 Starting log generation...")
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
                entry["error_type"] = random.choice([
                    "ConnectionTimeout", "ValidationError", 
                    "DatabaseError", "ServiceUnavailable"
                ])
            
            return entry
        
        try:
            logs_sent = 0
            logs_failed = 0
            logs_rate_limited = 0
            batch = []
            start_time = time.time()
            last_stats_time = start_time
            last_stats_sent = 0
            
            # For high-speed generation, use async batch sending
            import concurrent.futures
            import threading
            
            # Track rate limiting
            rate_limit_detected = False
            consecutive_failures = 0
            effective_rate = rate  # May be reduced if rate limiting detected
            
            def send_log_with_tracking(entry):
                """Send log and track success/failure."""
                nonlocal logs_sent, logs_failed, logs_rate_limited, rate_limit_detected, consecutive_failures
                
                success = send_log(
                    message=entry["message"],
                    level=entry["level"],
                    service=entry["service"],
                    attributes=entry,
                    client=client,
                )
                
                if success:
                    logs_sent += 1
                    consecutive_failures = 0
                    return True
                else:
                    logs_failed += 1
                    consecutive_failures += 1
                    
                    # Detect rate limiting (multiple consecutive failures)
                    if consecutive_failures >= 5 and not rate_limit_detected:
                        rate_limit_detected = True
                        logs_rate_limited = logs_failed
                    elif rate_limit_detected:
                        logs_rate_limited += 1
                    
                    return False
            
            if count == 0:
                # Continuous mode with high-speed support
                index = 0
                with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, int(rate/100) + 1)) as executor:
                    futures = []
                    
                    while True:
                        current_time = time.time()
                        
                        # Generate and submit logs at target rate
                        logs_this_second = 0
                        second_start = current_time
                        
                        while logs_this_second < effective_rate and (time.time() - second_start) < 1.0:
                            entry = generate_log_entry(index)
                            future = executor.submit(send_log_with_tracking, entry)
                            futures.append(future)
                            index += 1
                            logs_this_second += 1
                            
                            # Micro-sleep for very high rates
                            if rate > 100:
                                time.sleep(0.001)  # 1ms between submissions
                        
                        # Clean up completed futures
                        futures = [f for f in futures if not f.done()]
                        
                        # Print stats every second
                        if current_time - last_stats_time >= 1.0:
                            current_sent = logs_sent
                            current_rate = (current_sent - last_stats_sent) / (current_time - last_stats_time)
                            
                            status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
                            if logs_failed > 0:
                                status += f" | Failed: {logs_failed:,}"
                            if rate_limit_detected:
                                status += f" | ⚠️ RATE LIMITED ({logs_rate_limited:,})"
                                # Adjust effective rate down
                                effective_rate = max(effective_rate * 0.9, 10)
                            
                            click.echo(status)
                            last_stats_time = current_time
                            last_stats_sent = current_sent
                        
                        # Sleep remainder of second if needed
                        sleep_time = 1.0 - (time.time() - second_start)
                        if sleep_time > 0:
                            time.sleep(sleep_time)
                    
            else:
                # Fixed count mode with high-speed support
                with concurrent.futures.ThreadPoolExecutor(max_workers=min(20, int(rate/50) + 1)) as executor:
                    futures = []
                    
                    for i in range(count):
                        entry = generate_log_entry(i)
                        future = executor.submit(send_log_with_tracking, entry)
                        futures.append(future)
                        
                        # Control submission rate
                        if rate > 0:
                            time.sleep(1.0 / rate)
                        
                        # Print progress
                        if (i + 1) % 100 == 0 or i == count - 1:
                            # Wait for some futures to complete
                            completed = sum(1 for f in futures if f.done())
                            
                            status = f"📊 Progress: {i+1}/{count} submitted, {completed} completed"
                            if logs_sent > 0:
                                current_time = time.time()
                                elapsed = current_time - start_time
                                current_rate = logs_sent / elapsed if elapsed > 0 else 0
                                status += f" | Rate: {current_rate:.0f}/s"
                            if logs_failed > 0:
                                status += f" | Failed: {logs_failed}"
                            if rate_limit_detected:
                                status += f" | ⚠️ RATE LIMITED"
                            
                            click.echo(status)
                    
                    # Wait for all to complete
                    click.echo("⏳ Waiting for remaining logs to send...")
                    concurrent.futures.wait(futures)
            
            elapsed = time.time() - start_time
            rate_actual = logs_sent / elapsed if elapsed > 0 else 0
            
            click.echo(f"\n📊 Generation complete:")
            click.echo(f"   Total sent: {logs_sent:,} logs")
            click.echo(f"   Total failed: {logs_failed:,} logs")
            if rate_limit_detected:
                click.echo(f"   ⚠️  Rate limited: {logs_rate_limited:,} logs")
            click.echo(f"   Time: {elapsed:.2f}s")
            click.echo(f"   Target rate: {rate:.0f} logs/second")
            click.echo(f"   Actual rate: {rate_actual:.1f} logs/second")
            if rate_limit_detected and rate_actual < rate * 0.5:
                click.echo(f"   ⚠️  Rate limiting detected - actual rate is {(rate_actual/rate)*100:.0f}% of target")
            
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