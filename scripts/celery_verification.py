#!/usr/bin/env python3
"""
Celery-Based Script Verification System

This module creates a distributed verification system for all Foundation scripts
using Celery tasks. It transforms the existing performance and testing scripts
into distributed tasks that can run across multiple workers, providing
comprehensive verification of Foundation's capabilities at scale.

Features:
- Distributed benchmark execution
- Parallel performance testing
- Cross-worker metrics aggregation
- Real-time verification monitoring
- Comprehensive result reporting

Usage:
    python scripts/celery_verification.py
"""

import json
from pathlib import Path
import random
import sys
import threading
import time
from typing import Any

# Add src to path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Setup Celery app (reuse Celery integration setup)
sys.path.insert(0, str(project_root / "examples/integration/celery"))
from setup_and_config import app, CeleryTaskLogger
from metrics_and_signals import setup_signal_handlers

from provide.foundation import logger, pout

# Setup signal handlers
setup_signal_handlers(app)


@app.task(bind=True)
def verify_benchmark_segment(self, test_name: str, iterations: int = 1000) -> dict[str, Any]:
    """
    Execute a segment of benchmark_performance.py as a distributed task.

    Args:
        test_name: Name of the benchmark test to run
        iterations: Number of iterations for the benchmark

    Returns:
        Dict containing benchmark results
    """
    task_logger = CeleryTaskLogger("verify_benchmark_segment")

    task_logger.logger.info("benchmark_segment_started",
        test_name=test_name,
        iterations=iterations,
        worker_id=self.request.hostname
    )

    start_time = time.perf_counter()

    try:
        # Import benchmark functions dynamically
        sys.path.insert(0, str(project_root / "scripts"))

        if test_name == "basic_logging":
            from benchmark_performance import benchmark_basic_logging
            result = benchmark_basic_logging()
        elif test_name == "json_formatting":
            from benchmark_performance import benchmark_json_formatting
            result = benchmark_json_formatting()
        elif test_name == "emoji_processing":
            from benchmark_performance import benchmark_emoji_processing
            result = benchmark_emoji_processing()
        elif test_name == "level_filtering":
            from benchmark_performance import benchmark_level_filtering
            result = benchmark_level_filtering()
        elif test_name == "large_payloads":
            from benchmark_performance import benchmark_large_payloads
            result = benchmark_large_payloads()
        else:
            # Custom benchmark - simulate intensive logging
            from provide.foundation import setup_telemetry
            from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

            config = TelemetryConfig(
                service_name=f"verification-{test_name}",
                logging=LoggingConfig(default_level="INFO")
            )
            setup_telemetry(config)

            test_logger = logger.get_logger(f"verification.{test_name}")

            for i in range(iterations):
                test_logger.info(f"verification_log_{i}",
                    iteration=i,
                    test_name=test_name,
                    worker_id=self.request.hostname,
                    random_data=random.randint(1, 10000)
                )

            result = {
                "test_name": test_name,
                "iterations": iterations,
                "custom_benchmark": True
            }

        duration = time.perf_counter() - start_time
        result.update({
            "duration_seconds": duration,
            "worker_id": self.request.hostname,
            "task_id": self.request.id,
            "throughput_per_second": iterations / duration if duration > 0 else 0
        })

        task_logger.logger.info("benchmark_segment_completed",
            test_name=test_name,
            duration_seconds=duration,
            throughput=result["throughput_per_second"]
        )

        return result

    except Exception as e:
        task_logger.logger.error("benchmark_segment_failed",
            test_name=test_name,
            error=str(e),
            duration=time.perf_counter() - start_time
        )
        raise


@app.task(bind=True)
def verify_extreme_test_segment(self, test_type: str, duration_seconds: int = 10) -> dict[str, Any]:
    """
    Execute a segment of extreme_performance_test.py as a distributed task.

    Args:
        test_type: Type of extreme test to run
        duration_seconds: Duration to run the test

    Returns:
        Dict containing extreme test results
    """
    task_logger = CeleryTaskLogger("verify_extreme_test_segment")

    task_logger.logger.info("extreme_test_started",
        test_type=test_type,
        duration_seconds=duration_seconds
    )

    start_time = time.time()
    message_count = 0
    error_count = 0

    try:
        # Setup high-throughput logger
        from provide.foundation import setup_telemetry
        from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

        config = TelemetryConfig(
            service_name=f"extreme-test-{test_type}",
            logging=LoggingConfig(default_level="DEBUG")
        )
        setup_telemetry(config)

        extreme_logger = logger.get_logger(f"extreme.{test_type}")
        end_time = start_time + duration_seconds

        # Run extreme logging
        while time.time() < end_time:
            try:
                extreme_logger.info(f"extreme_test_message_{message_count}",
                    test_type=test_type,
                    message_id=message_count,
                    timestamp=time.time(),
                    worker_id=self.request.hostname,
                    large_payload="x" * random.randint(100, 1000),  # Variable payload size
                    nested_data={
                        "level_1": {
                            "level_2": {
                                "level_3": f"deep_value_{message_count}"
                            }
                        }
                    }
                )
                message_count += 1

                # Extreme test - minimal sleep
                if message_count % 100 == 0:
                    time.sleep(0.001)  # Tiny pause every 100 messages

            except Exception:
                error_count += 1
                if error_count > 10:  # Stop if too many errors
                    break

        actual_duration = time.time() - start_time

        result = {
            "test_type": test_type,
            "duration_seconds": actual_duration,
            "messages_generated": message_count,
            "errors": error_count,
            "messages_per_second": message_count / actual_duration if actual_duration > 0 else 0,
            "worker_id": self.request.hostname,
            "task_id": self.request.id
        }

        task_logger.logger.info("extreme_test_completed",
            test_type=test_type,
            messages_generated=message_count,
            rate=result["messages_per_second"],
            errors=error_count
        )

        return result

    except Exception as e:
        task_logger.logger.error("extreme_test_failed",
            test_type=test_type,
            error=str(e),
            messages_generated=message_count
        )
        raise


@app.task(bind=True)
def verify_cut_up_chuck_segment(self, duration_seconds: int = 30) -> dict[str, Any]:
    """
    Execute a segment of cut_up_chuck.py as a distributed task.

    Args:
        duration_seconds: Duration to run cut-up chuck generation

    Returns:
        Dict containing cut-up chuck results
    """
    task_logger = CeleryTaskLogger("verify_cut_up_chuck_segment")

    task_logger.logger.info("cutup_verification_started",
        duration_seconds=duration_seconds
    )

    start_time = time.time()

    try:
        # Import cut-up chuck tasks
        from cut_up_chuck_tasks import generate_log_entry, generate_batch, detect_anomaly

        entries_generated = 0
        batches_generated = 0
        anomalies_detected = 0
        end_time = start_time + duration_seconds

        iteration = 0
        while time.time() < end_time:
            iteration += 1

            # Mix of different task types
            if iteration % 5 == 0:
                # Generate batch
                generate_batch.delay(f"verify_batch_{iteration}", random.randint(3, 7))
                batches_generated += 1
            else:
                # Generate single entry
                generate_log_entry.delay(iteration + 10000)  # Offset to avoid collision
                entries_generated += 1

            # Occasional anomaly
            if iteration % 8 == 0:
                detect_anomaly.delay()
                anomalies_detected += 1

            # Small delay to prevent overwhelming
            time.sleep(random.uniform(0.1, 0.3))

        actual_duration = time.time() - start_time

        result = {
            "duration_seconds": actual_duration,
            "entries_generated": entries_generated,
            "batches_generated": batches_generated,
            "anomalies_detected": anomalies_detected,
            "total_tasks": entries_generated + batches_generated + anomalies_detected,
            "task_rate": (entries_generated + batches_generated + anomalies_detected) / actual_duration if actual_duration > 0 else 0,
            "worker_id": self.request.hostname,
            "task_id": self.request.id
        }

        task_logger.logger.info("cutup_verification_completed",
            duration=actual_duration,
            total_tasks=result["total_tasks"],
            task_rate=result["task_rate"]
        )

        return result

    except Exception as e:
        task_logger.logger.error("cutup_verification_failed",
            error=str(e),
            duration=time.time() - start_time
        )
        raise


@app.task(bind=True)
def collect_verification_results(self, results: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Aggregate verification results from multiple workers.

    Args:
        results: List of individual verification results

    Returns:
        Dict containing aggregated results and analysis
    """
    task_logger = CeleryTaskLogger("collect_verification_results")

    task_logger.logger.info("results_collection_started",
        results_count=len(results)
    )

    try:
        # Categorize results by type
        benchmark_results = []
        extreme_results = []
        cutup_results = []

        for result in results:
            if "test_name" in result:
                benchmark_results.append(result)
            elif "test_type" in result:
                extreme_results.append(result)
            elif "entries_generated" in result:
                cutup_results.append(result)

        # Calculate aggregated metrics
        total_duration = sum(r.get("duration_seconds", 0) for r in results)
        total_throughput = sum(r.get("throughput_per_second", 0) or r.get("messages_per_second", 0) or r.get("task_rate", 0) for r in results)

        # Benchmark analysis
        benchmark_analysis = {}
        if benchmark_results:
            benchmark_analysis = {
                "total_benchmarks": len(benchmark_results),
                "avg_throughput": sum(r.get("throughput_per_second", 0) for r in benchmark_results) / len(benchmark_results),
                "tests_executed": [r.get("test_name") for r in benchmark_results]
            }

        # Extreme test analysis
        extreme_analysis = {}
        if extreme_results:
            total_messages = sum(r.get("messages_generated", 0) for r in extreme_results)
            extreme_analysis = {
                "total_tests": len(extreme_results),
                "total_messages": total_messages,
                "avg_message_rate": sum(r.get("messages_per_second", 0) for r in extreme_results) / len(extreme_results),
                "peak_message_rate": max(r.get("messages_per_second", 0) for r in extreme_results)
            }

        # Cut-up analysis
        cutup_analysis = {}
        if cutup_results:
            cutup_analysis = {
                "total_segments": len(cutup_results),
                "total_tasks": sum(r.get("total_tasks", 0) for r in cutup_results),
                "avg_task_rate": sum(r.get("task_rate", 0) for r in cutup_results) / len(cutup_results)
            }

        aggregated_results = {
            "verification_summary": {
                "total_results": len(results),
                "total_duration": total_duration,
                "total_throughput": total_throughput,
                "timestamp": time.time()
            },
            "benchmark_analysis": benchmark_analysis,
            "extreme_analysis": extreme_analysis,
            "cutup_analysis": cutup_analysis,
            "worker_distribution": list(set(r.get("worker_id") for r in results if r.get("worker_id"))),
            "raw_results": results
        }

        task_logger.logger.info("results_collection_completed",
            total_results=len(results),
            workers_involved=len(aggregated_results["worker_distribution"]),
            total_throughput=total_throughput
        )

        return aggregated_results

    except Exception as e:
        task_logger.logger.error("results_collection_failed",
            error=str(e),
            results_count=len(results)
        )
        raise


class CeleryVerificationRunner:
    """Orchestrates distributed verification of Foundation scripts."""

    def __init__(self):
        self.logger = logger.get_logger("celery.verification")
        self.results = []

    def start_worker(self):
        """Start the verification worker."""
        pout("\n🚀 Starting verification worker...")

        from celery.worker import WorkController

        def run_worker():
            try:
                worker = WorkController(app=app, loglevel='INFO')
                worker.start()
            except Exception as e:
                self.logger.error("verification_worker_failed", error=str(e))

        worker_thread = threading.Thread(target=run_worker, daemon=True)
        worker_thread.start()

        time.sleep(2)
        pout("✅ Verification worker started!\n")

    def run_distributed_benchmarks(self):
        """Run benchmark tests across distributed workers."""
        pout("\n📊 Running Distributed Benchmark Verification")
        pout("=" * 55)

        benchmark_tests = [
            "basic_logging",
            "json_formatting",
            "emoji_processing",
            "level_filtering",
            "large_payloads",
            "custom_mixed_workload"
        ]

        # Submit benchmark tasks
        benchmark_tasks = []
        for test_name in benchmark_tests:
            task = verify_benchmark_segment.delay(test_name, random.randint(500, 1500))
            benchmark_tasks.append(task)
            pout(f"   Submitted: {test_name}")

        # Collect results
        pout("\n   ⏳ Collecting benchmark results...")
        for i, task in enumerate(benchmark_tasks):
            try:
                result = task.get(timeout=120)
                self.results.append(result)
                pout(f"   ✅ {benchmark_tests[i]}: {result['throughput_per_second']:.1f} ops/sec")
            except Exception as e:
                self.logger.error("benchmark_task_failed", test=benchmark_tests[i], error=str(e))
                pout(f"   ❌ {benchmark_tests[i]}: Failed")

    def run_distributed_extreme_tests(self):
        """Run extreme performance tests across distributed workers."""
        pout("\n🔥 Running Distributed Extreme Performance Tests")
        pout("=" * 55)

        extreme_tests = [
            "high_throughput",
            "large_payloads",
            "nested_structures",
            "concurrent_stress"
        ]

        # Submit extreme test tasks
        extreme_tasks = []
        for test_type in extreme_tests:
            task = verify_extreme_test_segment.delay(test_type, random.randint(15, 25))
            extreme_tasks.append(task)
            pout(f"   Submitted: {test_type}")

        # Collect results
        pout("\n   ⏳ Collecting extreme test results...")
        for i, task in enumerate(extreme_tasks):
            try:
                result = task.get(timeout=60)
                self.results.append(result)
                pout(f"   ✅ {extreme_tests[i]}: {result['messages_per_second']:.1f} msg/sec")
            except Exception as e:
                self.logger.error("extreme_test_failed", test=extreme_tests[i], error=str(e))
                pout(f"   ❌ {extreme_tests[i]}: Failed")

    def run_distributed_cutup_verification(self):
        """Run cut-up chuck verification across distributed workers."""
        pout("\n✂️  Running Distributed Cut-Up Chuck Verification")
        pout("=" * 55)

        # Submit cut-up verification tasks
        cutup_tasks = []
        for i in range(3):  # 3 parallel segments
            task = verify_cut_up_chuck_segment.delay(random.randint(20, 40))
            cutup_tasks.append(task)
            pout(f"   Submitted: cut-up segment {i+1}")

        # Collect results
        pout("\n   ⏳ Collecting cut-up verification results...")
        for i, task in enumerate(cutup_tasks):
            try:
                result = task.get(timeout=90)
                self.results.append(result)
                pout(f"   ✅ Segment {i+1}: {result['task_rate']:.1f} tasks/sec")
            except Exception as e:
                self.logger.error("cutup_verification_failed", segment=i+1, error=str(e))
                pout(f"   ❌ Segment {i+1}: Failed")

    def generate_final_report(self):
        """Generate and display final verification report."""
        if not self.results:
            pout("\n❌ No results to aggregate")
            return

        pout("\n📋 Generating Final Verification Report")
        pout("=" * 45)

        # Collect and aggregate all results
        collect_task = collect_verification_results.delay(self.results)

        try:
            aggregated = collect_task.get(timeout=30)

            pout("\n📈 Verification Summary:")
            summary = aggregated["verification_summary"]
            pout(f"   Total Tests: {summary['total_results']}")
            pout(f"   Total Duration: {summary['total_duration']:.1f}s")
            pout(f"   Combined Throughput: {summary['total_throughput']:.1f} ops/sec")
            pout(f"   Workers Involved: {len(aggregated['worker_distribution'])}")

            # Detailed analysis
            if aggregated["benchmark_analysis"]:
                bench = aggregated["benchmark_analysis"]
                pout(f"\n🏁 Benchmark Analysis:")
                pout(f"   Tests Executed: {bench['total_benchmarks']}")
                pout(f"   Average Throughput: {bench['avg_throughput']:.1f} ops/sec")

            if aggregated["extreme_analysis"]:
                extreme = aggregated["extreme_analysis"]
                pout(f"\n🚀 Extreme Test Analysis:")
                pout(f"   Total Messages: {extreme['total_messages']:,}")
                pout(f"   Peak Message Rate: {extreme['peak_message_rate']:.1f} msg/sec")

            if aggregated["cutup_analysis"]:
                cutup = aggregated["cutup_analysis"]
                pout(f"\n✂️  Cut-Up Analysis:")
                pout(f"   Total Tasks: {cutup['total_tasks']}")
                pout(f"   Average Task Rate: {cutup['avg_task_rate']:.1f} tasks/sec")

            # Save detailed report
            report_file = project_root / "verification_report.json"
            with open(report_file, 'w') as f:
                json.dump(aggregated, f, indent=2, default=str)
            pout(f"\n📄 Detailed report saved: {report_file}")

        except Exception as e:
            self.logger.error("report_generation_failed", error=str(e))
            pout(f"\n❌ Report generation failed: {e}")

    def run_complete_verification(self):
        """Run the complete distributed verification suite."""
        pout("""
╔══════════════════════════════════════════════════════════════════╗
║                Celery Script Verification System                 ║
║           Distributed Testing of Foundation Scripts             ║
╚══════════════════════════════════════════════════════════════════╝

Verifies all Foundation scripts using distributed Celery tasks:
• Benchmark performance tests across workers
• Extreme performance stress testing
• Cut-up chuck distributed generation
• Cross-worker metrics aggregation
• Comprehensive result reporting
""")

        try:
            # Start worker
            self.start_worker()

            # Run verification suites
            self.run_distributed_benchmarks()
            self.run_distributed_extreme_tests()
            self.run_distributed_cutup_verification()

            # Generate final report
            self.generate_final_report()

            pout("\n✅ Complete Verification Suite Finished!")
            pout("\n🎯 Verification Coverage:")
            pout("   • Benchmark performance across all test types")
            pout("   • Extreme performance under stress conditions")
            pout("   • Cut-up chuck distributed generation")
            pout("   • Cross-worker coordination and metrics")
            pout("   • Result aggregation and analysis")
            pout("   • Comprehensive reporting")

        except Exception as e:
            self.logger.error("verification_suite_failed", error=str(e))
            pout(f"\n💥 Verification suite error: {e}")


def main():
    """Main entry point."""
    verifier = CeleryVerificationRunner()
    verifier.run_complete_verification()


if __name__ == '__main__':
    main()
