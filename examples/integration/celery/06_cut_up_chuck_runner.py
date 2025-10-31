#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Celery Integration - Distributed Cut-Up Chuck Runner

This module orchestrates the distributed cut-up chuck log generation system,
demonstrating how the original continuous logging script can be transformed
into a scalable, distributed task processing system using Celery.

Part 6 of 6: Cut-Up Chuck Distributed Runner
- Orchestrates distributed log generation
- Real-time monitoring and metrics collection
- Worker coordination and load balancing
- Graceful shutdown and cleanup

Usage:
    python 06_cut_up_chuck_runner.py"""

from pathlib import Path
import random
import signal
import sys
import threading
import time

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

# Load modules by file path
import importlib.util

from provide.foundation import logger, pout


def load_module_from_file(name, filepath):
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


current_dir = Path(__file__).parent
setup_config = load_module_from_file("setup_and_config", current_dir / "01_setup_and_config.py")
metrics_signals = load_module_from_file("metrics_and_signals", current_dir / "02_metrics_and_signals.py")
cut_up_tasks = load_module_from_file("cut_up_chuck_tasks", current_dir / "05_cut_up_chuck_tasks.py")

# Extract needed objects
app = setup_config.app
metrics = metrics_signals.metrics
setup_signal_handlers = metrics_signals.setup_signal_handlers
generate_log_entry = cut_up_tasks.generate_log_entry
generate_batch = cut_up_tasks.generate_batch
detect_anomaly = cut_up_tasks.detect_anomaly
system_heartbeat = cut_up_tasks.system_heartbeat
continuous_generator = cut_up_tasks.continuous_generator
CUT_UP_PHRASES = cut_up_tasks.CUT_UP_PHRASES
LOGGER_CONTEXTS = cut_up_tasks.LOGGER_CONTEXTS

# Try to import Celery workflow tools
try:
    from celery import chain, group

    CELERY_WORKFLOWS_AVAILABLE = True
except ImportError:
    CELERY_WORKFLOWS_AVAILABLE = False

# Setup signal handlers
setup_signal_handlers(app)


class DistributedCutUpChuck:
    """Orchestrates distributed cut-up chuck log generation."""

    def __init__(self) -> None:
        self.logger = logger.get_logger("distributed.cutup")
        self.running = False
        self.shutdown_event = threading.Event()
        self.stats = {
            "start_time": 0,
            "total_tasks": 0,
            "batches_submitted": 0,
            "anomalies_detected": 0,
            "heartbeats_sent": 0,
            "errors": 0,
        }

    def start_worker(self) -> None:
        """Start the in-process Celery worker."""
        pout("\n🚀 Starting distributed cut-up chuck worker...")

        from celery.worker import WorkController

        def run_worker() -> None:
            try:
                worker = WorkController(app=app, loglevel="INFO")
                worker.start()
            except Exception as e:
                self.logger.error("worker_startup_failed", error=str(e))

        worker_thread = threading.Thread(target=run_worker, daemon=True)
        worker_thread.start()

        # Give worker time to start
        time.sleep(2)

        self.logger.info(
            "distributed_worker_started",
            phrases_available=len(CUT_UP_PHRASES),
            contexts_available=len(LOGGER_CONTEXTS),
            workflows_available=CELERY_WORKFLOWS_AVAILABLE,
        )

    def demonstrate_single_tasks(self) -> None:
        """Demonstrate individual task execution patterns."""
        pout("\n" + "=" * 60)
        pout("🎯 Demonstrating Individual Cut-Up Tasks")
        pout("=" * 60)

        # 1. Single log entry generation
        pout("\n1️⃣ Single Log Entry Generation")
        entry_task = generate_log_entry.delay(1001)
        self.stats["total_tasks"] += 1

        try:
            result = entry_task.get(timeout=10)
            self.logger.info(
                "single_entry_completed",
                iteration=result["iteration"],
                phrase_length=len(result["phrase"]),
                context=result["context"],
            )
            pout(f"   Generated: {result['phrase'][:50]}...")
        except Exception as e:
            self.logger.error("single_entry_failed", error=str(e))
            self.stats["errors"] += 1

        # 2. Batch generation
        pout("\n2️⃣ Batch Log Generation")
        batch_task = generate_batch.delay("demo_batch_001", 5)
        self.stats["total_tasks"] += 1
        self.stats["batches_submitted"] += 1

        try:
            result = batch_task.get(timeout=30)
            self.logger.info(
                "batch_completed",
                batch_id=result["batch_id"],
                entries_generated=result["entries_generated"],
                success_rate=result["success_rate"],
            )
            pout(
                f"   Batch completed: {result['entries_generated']} entries, "
                f"{result['success_rate']:.1%} success rate"
            )
        except Exception as e:
            self.logger.error("batch_failed", error=str(e))
            self.stats["errors"] += 1

        # 3. Anomaly detection
        pout("\n3️⃣ Anomaly Detection")
        anomaly_task = detect_anomaly.delay("Gamma")
        self.stats["total_tasks"] += 1
        self.stats["anomalies_detected"] += 1

        try:
            result = anomaly_task.get(timeout=10)
            self.logger.info(
                "anomaly_completed",
                anomaly_type=result["anomaly_type"],
                confidence=result["confidence"],
            )
            pout(f"   Detected: Type-{result['anomaly_type']} ({result['confidence']:.1f}% confidence)")
        except Exception as e:
            self.logger.error("anomaly_failed", error=str(e))
            self.stats["errors"] += 1

        # 4. System heartbeat
        pout("\n4️⃣ System Heartbeat")
        heartbeat_task = system_heartbeat.delay("demo_worker_01")
        self.stats["total_tasks"] += 1
        self.stats["heartbeats_sent"] += 1

        try:
            result = heartbeat_task.get(timeout=10)
            self.logger.info(
                "heartbeat_completed",
                uptime=result["uptime_seconds"],
                cpu_load=result["cpu_load"],
                worker_id=result["worker_id"],
            )
            pout(f"   Heartbeat: {result['uptime_seconds']}s uptime, {result['cpu_load']:.1f}% CPU")
        except Exception as e:
            self.logger.error("heartbeat_failed", error=str(e))
            self.stats["errors"] += 1

    def demonstrate_parallel_workflows(self) -> None:
        """Demonstrate parallel task workflows."""
        if not CELERY_WORKFLOWS_AVAILABLE:
            pout("\n5️⃣ Parallel Workflows: Skipped (Celery workflows not available)")
            return

        pout("\n5️⃣ Parallel Workflow Patterns")

        # Parallel batch generation
        pout("   📊 Parallel Batch Generation")
        batch_group = group(generate_batch.s(f"parallel_batch_{i}", random.randint(3, 6)) for i in range(4))
        batch_results = batch_group.apply_async()
        self.stats["total_tasks"] += 4
        self.stats["batches_submitted"] += 4

        try:
            results = batch_results.get(timeout=60)
            total_entries = sum(r["entries_generated"] for r in results)
            avg_success_rate = sum(r["success_rate"] for r in results) / len(results)

            self.logger.info(
                "parallel_batches_completed",
                batches_count=len(results),
                total_entries=total_entries,
                avg_success_rate=avg_success_rate,
            )
            pout(f"   Completed {len(results)} batches with {total_entries} total entries")
        except Exception as e:
            self.logger.error("parallel_batches_failed", error=str(e))
            self.stats["errors"] += 1

        # Mixed task chain
        pout("   🔗 Mixed Task Chain")
        mixed_chain = chain(
            generate_log_entry.s(2001),
            detect_anomaly.s(),
            system_heartbeat.s("chain_worker"),
        )
        chain_result = mixed_chain.apply_async()
        self.stats["total_tasks"] += 3

        try:
            result = chain_result.get(timeout=30)
            self.logger.info("mixed_chain_completed", final_result=result)
            pout("   Chain completed successfully")
        except Exception as e:
            self.logger.error("mixed_chain_failed", error=str(e))
            self.stats["errors"] += 1

    def demonstrate_continuous_generation(self, duration_minutes: float = 1.0) -> None:
        """Demonstrate continuous log generation."""
        pout(f"\n6️⃣ Continuous Generation ({duration_minutes} minutes)")

        continuous_task = continuous_generator.delay(
            duration_minutes=duration_minutes,
            entries_per_minute=20,
        )
        self.stats["total_tasks"] += 1

        # Monitor progress
        start_time = time.time()
        while not continuous_task.ready():
            time.sleep(5)
            elapsed = time.time() - start_time
            pout(f"   Running continuous generation... {elapsed:.1f}s elapsed")

            if elapsed > (duration_minutes * 60 + 30):  # Timeout after duration + 30s
                pout("   ⚠️  Continuous generation timeout")
                continuous_task.revoke(terminate=True)
                break

        try:
            if continuous_task.ready():
                result = continuous_task.get()
                self.logger.info(
                    "continuous_generation_completed",
                    duration=result["duration_seconds"],
                    total_entries=result["total_entries"],
                    actual_rate=result["actual_rate_per_minute"],
                )
                pout(
                    f"   Generated {result['total_entries']} entries "
                    f"at {result['actual_rate_per_minute']:.1f} entries/min"
                )
        except Exception as e:
            self.logger.error("continuous_generation_failed", error=str(e))
            self.stats["errors"] += 1

    def display_final_metrics(self) -> None:
        """Display final execution metrics."""
        pout("\n📊 Distributed Cut-Up Chuck Metrics")
        pout("=" * 50)

        duration = time.time() - self.stats["start_time"]

        pout("\n📈 Execution Summary:")
        pout(f"   Duration: {duration:.1f}s")
        pout(f"   Total Tasks: {self.stats['total_tasks']}")
        pout(f"   Batches: {self.stats['batches_submitted']}")
        pout(f"   Anomalies: {self.stats['anomalies_detected']}")
        pout(f"   Heartbeats: {self.stats['heartbeats_sent']}")
        pout(f"   Errors: {self.stats['errors']}")
        pout(f"   Task Rate: {self.stats['total_tasks'] / duration:.1f} tasks/sec")

        # Display Celery metrics
        celery_stats = metrics.get_stats()
        if celery_stats:
            pout("\n📊 Celery Task Metrics:")
            for task_name, stats in celery_stats.items():
                if "cut_up" in task_name.lower() or task_name in [
                    "generate_log_entry",
                    "generate_batch",
                    "detect_anomaly",
                    "system_heartbeat",
                    "continuous_generator",
                ]:
                    pout(f"   {task_name}:")
                    pout(f"     Executions: {stats['count']}")
                    pout(f"     Success Rate: {stats['success_rate']}%")
                    pout(f"     Avg Duration: {stats['avg_duration_ms']}ms")

        self.logger.info(
            "distributed_cutup_completed",
            total_duration=duration,
            final_metrics=self.stats,
            celery_metrics=celery_stats,
        )

    def setup_signal_handlers(self) -> None:
        """Setup graceful shutdown signal handlers."""

        def signal_handler(signum, frame) -> None:
            pout(f"\n🛑 Received signal {signum}, initiating graceful shutdown...")
            self.shutdown_event.set()
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def run(self) -> None:
        """Run the complete distributed cut-up chuck demonstration."""
        self.setup_signal_handlers()
        self.running = True
        self.stats["start_time"] = time.time()

        pout("""
╔══════════════════════════════════════════════════════════════════╗
║              Distributed Cut-Up Chuck Generator                 ║
║           Comprehensive Celery + Foundation Example             ║
╚══════════════════════════════════════════════════════════════════╝

Transforms the original cut_up_chuck.py into a distributed task system:
• Individual task execution with structured logging
• Batch processing with parallel execution
• Anomaly detection and system monitoring
• Continuous generation patterns
• Real-time metrics and monitoring
• Graceful shutdown and cleanup
""")

        try:
            # Start the worker
            self.start_worker()

            # Run demonstrations
            if self.running:
                self.demonstrate_single_tasks()

            if self.running:
                self.demonstrate_parallel_workflows()

            if self.running:
                self.demonstrate_continuous_generation(duration_minutes=0.5)

            # Wait a bit for all tasks to complete
            if self.running:
                pout("\n⏳ Waiting for remaining tasks to complete...")
                time.sleep(3)

        except KeyboardInterrupt:
            pout("\n🛑 User initiated shutdown (Ctrl+C)")
        except Exception as e:
            self.logger.error("distributed_cutup_error", error=str(e))
            pout(f"\n💥 Error: {e}")
        finally:
            self.display_final_metrics()
            pout("\n🎯 Demonstrated Patterns:")
            pout("   • Distributed log generation across workers")
            pout("   • Parallel batch processing")
            pout("   • Task chains and workflows")
            pout("   • Real-time anomaly detection")
            pout("   • System health monitoring")
            pout("   • Continuous generation patterns")
            pout("   • Comprehensive metrics collection")
            pout("   • Graceful shutdown handling")


def main() -> None:
    """Main entry point."""
    chuck = DistributedCutUpChuck()
    chuck.run()


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
