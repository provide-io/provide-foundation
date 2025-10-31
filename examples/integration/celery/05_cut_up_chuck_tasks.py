#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Celery Integration - Distributed Cut-Up Chuck Tasks

This module transforms the original cut_up_chuck.py script into distributed
Celery tasks, demonstrating how provide.foundation structured logging works
across a distributed task processing system.

Part 5 of 6: Cut-Up Chuck Distributed Tasks
- Individual log generation tasks
- Batch log generation with parallelization
- Anomaly detection tasks
- System heartbeat tasks
- Phrase selection and processing

Usage:
    from examples.integration.celery.cut_up_chuck_tasks import generate_log_entry, generate_batch"""

from pathlib import Path
import random
import sys
import time
from typing import Any

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Add current directory to path for local imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Load setup_and_config module by file path
import importlib.util


def load_module_from_file(name, filepath):
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


current_dir = Path(__file__).parent
setup_config = load_module_from_file("setup_and_config", current_dir / "01_setup_and_config.py")
app = setup_config.app
CeleryTaskLogger = setup_config.CeleryTaskLogger
from provide.foundation import logger

# Cut-Up Phrases (from original cut_up_chuck.py)
CUT_UP_PHRASES: list[str] = [
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

# Logger contexts (from original cut_up_chuck.py)
LOGGER_CONTEXTS: list[str] = [
    "Interzone.Reception",
    "Interzone.Kitchen",
    "RealityStudio.Control",
]

LOG_LEVELS: list[str] = [
    "debug",
    "info",
    "warning",
    "error",
    "critical",
]


@app.task(bind=True)
def generate_log_entry(self, iteration: int, context_override: str | None = None) -> dict[str, Any]:
    """Generate a single cut-up phrase log entry with structured data.

    Args:
        iteration: Iteration number for tracking
        context_override: Optional specific logger context to use

    Returns:
        Dict containing the log entry details and metadata

    """
    task_logger = CeleryTaskLogger("generate_log_entry")

    # Select random elements
    phrase = random.choice(CUT_UP_PHRASES)
    context = context_override or random.choice(LOGGER_CONTEXTS)
    log_level = random.choice(LOG_LEVELS)

    # Get context-specific logger
    context_logger = logger.get_logger(context)
    log_method = getattr(context_logger, log_level)

    # Generate the log entry
    log_method(
        f"Iter {iteration:03d} :: {phrase}",
        current_phrase_idx=CUT_UP_PHRASES.index(phrase),
        random_val=random.randint(1, 1000),
        domain="transmission",
        action="broadcast",
        status="nominal" if log_level not in ["error", "critical"] else "degraded",
        iteration=iteration,
        context=context,
        task_id=self.request.id,
    )

    task_logger.logger.info(
        "cut_up_log_generated",
        iteration=iteration,
        phrase_index=CUT_UP_PHRASES.index(phrase),
        context=context,
        log_level=log_level,
        phrase_length=len(phrase),
    )

    return {
        "iteration": iteration,
        "phrase": phrase,
        "context": context,
        "log_level": log_level,
        "timestamp": time.time(),
        "task_id": self.request.id,
    }


@app.task(bind=True)
def generate_batch(self, batch_id: str, batch_size: int, context_filter: str | None = None) -> dict[str, Any]:
    """Generate a batch of cut-up phrase log entries in parallel.

    Args:
        batch_id: Unique identifier for this batch
        batch_size: Number of log entries to generate
        context_filter: Optional context to restrict all entries to

    Returns:
        Dict containing batch results and statistics

    """
    task_logger = CeleryTaskLogger("generate_batch")

    task_logger.logger.info(
        "batch_generation_started",
        batch_id=batch_id,
        batch_size=batch_size,
        context_filter=context_filter,
    )

    start_time = time.time()
    entries_generated = []

    # Generate batch entries
    for i in range(batch_size):
        iteration = int(start_time * 1000) + i  # Unique iteration based on timestamp

        try:
            # Use subtask for each entry (could be parallelized)
            result = generate_log_entry.apply_async(
                args=[iteration, context_filter],
                countdown=random.uniform(0.1, 1.0),  # Stagger execution
            ).get(timeout=10)

            entries_generated.append(result)

        except Exception as e:
            task_logger.logger.warning(
                "batch_entry_failed",
                batch_id=batch_id,
                iteration=i,
                error=str(e),
            )

    duration = time.time() - start_time

    task_logger.logger.info(
        "batch_generation_completed",
        batch_id=batch_id,
        entries_generated=len(entries_generated),
        duration_seconds=duration,
        entries_per_second=len(entries_generated) / duration if duration > 0 else 0,
    )

    return {
        "batch_id": batch_id,
        "entries_generated": len(entries_generated),
        "entries": entries_generated,
        "duration_seconds": duration,
        "success_rate": len(entries_generated) / batch_size if batch_size > 0 else 0,
    }


@app.task(bind=True)
def detect_anomaly(self, anomaly_type: str | None = None) -> dict[str, Any]:
    """Generate anomaly detection log entries (equivalent to trace events in original).

    Args:
        anomaly_type: Optional specific anomaly type, otherwise random

    Returns:
        Dict containing anomaly detection results

    """
    task_logger = CeleryTaskLogger("detect_anomaly")

    anomaly_types = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"]
    selected_type = anomaly_type or random.choice(anomaly_types)
    confidence = random.random() * 100

    # Generate anomaly log
    logger.trace(
        "Anomalous energy signature detected.",
        _foundation_logger_name="Interzone.Anomalies",
        signature_type=f"Type-{selected_type}",
        confidence=f"{confidence:.1f}%",
        domain="sensor_grid",
        action="detect",
        status="trace_event",
        task_id=self.request.id,
        detection_method="distributed_scanner",
    )

    task_logger.logger.info(
        "anomaly_detected",
        anomaly_type=selected_type,
        confidence_pct=confidence,
        detection_timestamp=time.time(),
    )

    return {
        "anomaly_type": selected_type,
        "confidence": confidence,
        "timestamp": time.time(),
        "task_id": self.request.id,
    }


@app.task(bind=True)
def system_heartbeat(self, worker_id: str | None = None) -> dict[str, Any]:
    """Generate system heartbeat log entries with health metrics.

    Args:
        worker_id: Optional worker identifier

    Returns:
        Dict containing system health data

    """
    task_logger = CeleryTaskLogger("system_heartbeat")

    uptime = int(time.time() % (60 * 60 * 24))  # Uptime in seconds (mod 24h)
    cpu_load = random.random() * 100
    memory_usage = random.uniform(20, 80)  # Mock memory usage

    # Generate heartbeat log
    logger.trace(
        "System heartbeat.",
        uptime_seconds=uptime,
        cpu_load=f"{cpu_load:.1f}%",
        memory_usage=f"{memory_usage:.1f}%",
        domain="system_health",
        action="heartbeat",
        status="internal_trace",
        worker_id=worker_id or f"worker_{random.randint(1, 5)}",
        task_id=self.request.id,
    )

    task_logger.logger.info(
        "heartbeat_generated",
        uptime_seconds=uptime,
        cpu_load_pct=cpu_load,
        memory_usage_pct=memory_usage,
        worker_id=worker_id,
    )

    return {
        "uptime_seconds": uptime,
        "cpu_load": cpu_load,
        "memory_usage": memory_usage,
        "worker_id": worker_id,
        "timestamp": time.time(),
        "task_id": self.request.id,
    }


@app.task(bind=True)
def continuous_generator(self, duration_minutes: int = 2, entries_per_minute: int = 30) -> dict[str, Any]:
    """Orchestrate continuous log generation for a specified duration.

    Args:
        duration_minutes: How long to run the generator
        entries_per_minute: Target rate of log generation

    Returns:
        Dict containing generation statistics

    """
    task_logger = CeleryTaskLogger("continuous_generator")

    task_logger.logger.info(
        "continuous_generation_started",
        duration_minutes=duration_minutes,
        target_rate=entries_per_minute,
    )

    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    total_entries = 0
    total_batches = 0
    total_anomalies = 0
    total_heartbeats = 0

    iteration = 0
    while time.time() < end_time:
        iteration += 1

        # Regular log entries (bulk of traffic)
        if iteration % 5 == 0:
            # Generate batch every 5 iterations
            generate_batch.delay(
                f"continuous_{int(time.time())}_{total_batches}",
                random.randint(3, 8),
            )
            total_batches += 1
        else:
            # Generate individual entries
            generate_log_entry.delay(iteration)
            total_entries += 1

        # Anomaly detection (every 7 iterations, like original)
        if iteration % 7 == 0:
            detect_anomaly.delay()
            total_anomalies += 1

        # System heartbeat (every 10 iterations)
        if iteration % 10 == 0:
            system_heartbeat.delay()
            total_heartbeats += 1

        # Sleep to maintain rate (approximate)
        sleep_time = 60.0 / entries_per_minute  # Base sleep time
        sleep_time += random.uniform(-0.2, 0.2)  # Add jitter
        time.sleep(max(0.1, sleep_time))

    actual_duration = time.time() - start_time

    task_logger.logger.info(
        "continuous_generation_completed",
        actual_duration_seconds=actual_duration,
        total_entries=total_entries,
        total_batches=total_batches,
        total_anomalies=total_anomalies,
        total_heartbeats=total_heartbeats,
        actual_rate=total_entries / (actual_duration / 60) if actual_duration > 0 else 0,
    )

    return {
        "duration_seconds": actual_duration,
        "total_entries": total_entries,
        "total_batches": total_batches,
        "total_anomalies": total_anomalies,
        "total_heartbeats": total_heartbeats,
        "actual_rate_per_minute": total_entries / (actual_duration / 60) if actual_duration > 0 else 0,
    }


if __name__ == "__main__":
    from provide.foundation import pout

    pout("🎯 Distributed Cut-Up Chuck Tasks Available:")
    pout("• generate_log_entry - Single cut-up phrase log entry")
    pout("• generate_batch - Batch of log entries with parallelization")
    pout("• detect_anomaly - Anomaly detection with trace logging")
    pout("• system_heartbeat - System health monitoring logs")
    pout("• continuous_generator - Orchestrate continuous log generation")
    pout(f"• {len(CUT_UP_PHRASES)} cut-up phrases available")
    pout(f"• {len(LOGGER_CONTEXTS)} logger contexts available")

# 🧱🏗️🔚
