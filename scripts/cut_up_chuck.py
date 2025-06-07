#
# cut_up_chuck.py
#
"""
Continuously emits diverse log messages every second until Ctrl+C.

This script serves as a demonstration and a simple load test for the
pyvider.telemetry logging system. It showcases various logging features,
including different log levels, named loggers, DAS (Domain-Action-Status)
logging, and the custom trace level.
"""
#!/usr/bin/env python3
#
# cut_up_chuck.py
#
# Note: The `depy` persona mandates this header. If direct execution is desired,
# the shebang `#!/usr/bin/env python3` would typically be the first line.
#
import asyncio
from collections.abc import Callable  # For type hinting log_level_method
import os
import random
import sys
import time  # For iteration count in a long-running scenario
from typing import Any  # For type hinting chosen_logger

# Ensure the package can be found
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger,  # This is the global PyviderLogger instance
    setup_telemetry,
    shutdown_pyvider_telemetry,
)

# --- Configuration ---
SERVICE_NAME: str = "interzone-cafe-terminal-continuous"
config: TelemetryConfig = TelemetryConfig(
    service_name=SERVICE_NAME,
    logging=LoggingConfig(default_level="DEBUG", console_formatter="key_value"),
)

# --- Loggers ---
# Get specific loggers for different contexts. These will have their names automatically.
reception_log = logger.get_logger("Interzone.Reception")
kitchen_log = logger.get_logger("Interzone.Kitchen")
reality_studio_log = logger.get_logger("RealityStudio.Control")

# --- Cut-Up Phrases ---
phrases: list[str] = [
    "mutated Soft Machine prescribed within data stream.",
    "pre-recorded talking asshole dissolved into under neon hum.",
    "the viral Word carrying a new strain of reality.",
    "equations of control flickering on a broken monitor.",
    "memory banks spilling future-pasts onto the terminal floor.",
    "a thousand junk units screaming in unison.",
    "the algebra of need computed by the Nova Mob.",
    "subliminal commands embedded in the white noise.",
    "the Biologic Courts passing sentence in a dream.",
    "Nova Police raiding the reality studio.",
    "the soft typewriter of the Other Half.",
    "a flickering hologram of Hassan i Sabbah.",
    "Contaminated data feed from the Crab Nebula.",
    "Thought-forms materializing in the Interzone.",
    "Frequency shift reported by Sector 5.",
]

async def generate_log_entries_continuously() -> None:
    """Generates a stream of diverse log entries indefinitely."""
    reception_log.info("⚙️➡️✅ Continuous Terminal Feed Online. Press Ctrl+C to stop.",
                       log_level_cfg=config.logging.default_level) # log_level_cfg is illustrative, not used by logger
    print("-" * 70)

    iteration_count: int = 0
    try:
        while True: # Loop indefinitely
            iteration_count += 1
            phrase: str = random.choice(phrases)

            chosen_logger: Any = random.choice([reception_log, kitchen_log, reality_studio_log])
            log_level_method_name: str = random.choice(["debug", "info", "warning", "error", "critical"])
            log_level_method: Callable[..., None] = getattr(chosen_logger, log_level_method_name)

            log_level_method(
                f"Iter {iteration_count:03d} :: {phrase}",
                current_phrase_idx=phrases.index(phrase),
                random_val=random.randint(1, 1000),
                domain="transmission",
                action="broadcast",
                status="nominal" if log_level_method_name not in ["error", "critical"] else "degraded"
            )

            if iteration_count % 5 == 0:
                logger.trace(
                    "Anomalous energy signature detected.",
                    _pyvider_logger_name="Interzone.Anomalies",
                    signature_type=f"Type-{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])}",
                    confidence=f"{random.random()*100:.1f}%",
                    domain="sensor_grid", action="detect", status="trace_event"
                )

            if iteration_count % 7 == 0:
                logger.trace(
                    "System heartbeat.",
                    uptime_seconds=int(time.time() % (60*60*24)),
                    cpu_load=f"{random.random()*100:.1f}%",
                    domain="system_health", action="heartbeat", status="internal_trace"
                )

            print("-" * 70)
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        reception_log.warning("🛑 User initiated shutdown (Ctrl+C). Loop terminating.")
    except Exception as e:
        app_error_log = logger.get_logger("Interzone.MainControl.Error")
        app_error_log.exception(f"💥 Unhandled exception in generate_log_entries_continuously: {e}")
    finally:
        reception_log.info("🏁➡️🛑 Continuous Terminal Feed Offline.")


async def main_async_loop() -> None:
    """Main asynchronous routine for the log generation demo."""
    print("🚀 Initializing Pyvider Telemetry...")
    setup_telemetry(config)

    try:
        await generate_log_entries_continuously()
    finally:
        print("🔌 Shutting down Pyvider Telemetry...")
        await shutdown_pyvider_telemetry()
        print("Pyvider Telemetry shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main_async_loop())
    except KeyboardInterrupt:
        print("\n🛑 Main execution cancelled by user.")
    except Exception as e:
        print(f"💥 CRITICAL SCRIPT ERROR (main): {e}", file=sys.stderr)
    finally:
        print("🎬 Example script finished.")

# 📜☕


