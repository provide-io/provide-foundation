"""
Generate test logs command for Foundation CLI.

Incorporates creative prose inspired by William S. Burroughs and the cut-up technique.
"""

import asyncio
import random
import time
from datetime import datetime, timedelta

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
        help="Logs per second (for continuous mode)",
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
            batch = []
            start_time = time.time()
            
            if count == 0:
                # Continuous mode
                index = 0
                while True:
                    entry = generate_log_entry(index)
                    success = send_log(
                        message=entry["message"],
                        level=entry["level"],
                        service=entry["service"],
                        attributes=entry,
                        client=client,
                    )
                    
                    if success:
                        logs_sent += 1
                        if logs_sent % 10 == 0:
                            click.echo(f"✅ Sent {logs_sent} logs...")
                    
                    index += 1
                    
                    # Rate limiting
                    time.sleep(1.0 / rate)
                    
            else:
                # Fixed count mode
                for i in range(count):
                    entry = generate_log_entry(i)
                    batch.append(entry)
                    
                    # Send batch when full or at end
                    if len(batch) >= batch_size or i == count - 1:
                        for log_entry in batch:
                            success = send_log(
                                message=log_entry["message"],
                                level=log_entry["level"],
                                service=log_entry["service"],
                                attributes=log_entry,
                                client=client,
                            )
                            if success:
                                logs_sent += 1
                        
                        click.echo(f"✅ Sent batch: {logs_sent}/{count} logs")
                        batch = []
            
            elapsed = time.time() - start_time
            rate_actual = logs_sent / elapsed if elapsed > 0 else 0
            
            click.echo(f"\n📊 Generation complete:")
            click.echo(f"   Total sent: {logs_sent} logs")
            click.echo(f"   Time: {elapsed:.2f}s")
            click.echo(f"   Rate: {rate_actual:.1f} logs/second")
            
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