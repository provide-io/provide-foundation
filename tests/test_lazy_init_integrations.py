#
# tests/test_lazy_initialization_integration.py
#

"""
Integration tests for lazy initialization with complete workflow scenarios.

This module tests end-to-end scenarios that combine lazy initialization with
real-world usage patterns, ensuring the feature works in practical applications.
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import contextlib
import json
import os
import threading
import time
from typing import Any
from unittest.mock import patch

import pytest
from pytest import CaptureFixture  # Added for capsys

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger as global_logger,
    setup_telemetry,
    shutdown_pyvider_telemetry,
)
from pyvider.telemetry.core import reset_pyvider_setup_for_testing


class TestRealWorldScenarios:
    """Tests that simulate real-world application scenarios."""

    def test_web_application_startup_scenario(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization in a web application startup scenario."""
        reset_pyvider_setup_for_testing()

        # Simulate web app startup sequence
        global_logger.info("Starting web application")

        # Simulate middleware initialization
        middleware_logger = global_logger.get_logger("app.middleware")
        middleware_logger.info("Initializing authentication middleware")
        middleware_logger.info("Initializing CORS middleware")

        # Simulate route registration
        routes_logger = global_logger.get_logger("app.routes")
        routes_logger.debug("Registering /api/users route")
        routes_logger.debug("Registering /api/auth route")

        # Simulate database connection
        db_logger = global_logger.get_logger("app.database")
        db_logger.info("Connecting to database", host="localhost", port=5432)

        # Simulate server startup completion
        global_logger.info("Web application started successfully", port=8080)

        captured = capsys.readouterr()
        assert "Starting web application" in captured.err
        assert "Initializing authentication middleware" in captured.err
        assert "Web application started successfully" in captured.err

    def test_microservice_with_environment_config(self, capsys: CaptureFixture) -> None:
        """Test microservice startup with environment-based configuration."""
        reset_pyvider_setup_for_testing()

        # Simulate microservice environment
        with patch.dict(os.environ, {
            "PYVIDER_SERVICE_NAME": "user-service",
            "PYVIDER_LOG_LEVEL": "INFO",
            "PYVIDER_LOG_CONSOLE_FORMATTER": "json",
            "PYVIDER_LOG_MODULE_LEVELS": "app.auth:DEBUG,app.external:WARNING",
            "PYVIDER_LOG_DAS_EMOJI_ENABLED": "true",
        }):
            # Service startup logging
            global_logger.info("User service starting up")

            # Auth module (DEBUG level)
            auth_logger = global_logger.get_logger("app.auth")
            auth_logger.debug("Loading JWT configuration")  # Should appear
            auth_logger.info("JWT configuration loaded")    # Should appear

            # External module (WARNING level)
            external_logger = global_logger.get_logger("app.external")
            external_logger.info("Connecting to external API")  # Should be filtered
            external_logger.warning("External API rate limit reached")  # Should appear

            # Business logic with DAS
            global_logger.info(
                "User registration processed",
                domain="user",
                action="register",
                status="success",
                user_id=12345
            )

        captured = capsys.readouterr()

        # Parse JSON logs
        json_lines = []
        for line in captured.err.splitlines():
            if line.strip() and not line.startswith("["):
                with contextlib.suppress(json.JSONDecodeError):
                    json_lines.append(json.loads(line))

        # Verify service name injection
        service_logs = [log for log in json_lines if "service_name" in log]
        assert len(service_logs) > 0
        assert all(log["service_name"] == "user-service" for log in service_logs)

        # Verify module-level filtering
        assert any("Loading JWT configuration" in log.get("event", "") for log in json_lines)
        assert not any("Connecting to external API" in log.get("event", "") for log in json_lines)
        assert any("External API rate limit reached" in log.get("event", "") for log in json_lines)

        # Verify DAS emoji processing
        user_reg_logs = [log for log in json_lines if "User registration processed" in log.get("event", "")]
        assert len(user_reg_logs) == 1
        assert "[👤][⚙️][✅]" in user_reg_logs[0]["event"]

    def test_data_processing_pipeline_scenario(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization in a data processing pipeline."""
        reset_pyvider_setup_for_testing()

        # Simulate data pipeline stages
        global_logger.get_logger("pipeline.main")

        # Stage 1: Data ingestion
        ingestion_logger = global_logger.get_logger("pipeline.ingestion")
        ingestion_logger.info("Starting data ingestion", source="s3://data-bucket")

        for i in range(3):
            ingestion_logger.debug(f"Processing file {i+1}/3")

        ingestion_logger.info("Data ingestion completed", files_processed=3)

        # Stage 2: Data transformation
        transform_logger = global_logger.get_logger("pipeline.transform")
        transform_logger.info("Starting data transformation")

        try:
            # Simulate processing error
            raise ValueError("Invalid data format in record 42")
        except ValueError:
            transform_logger.exception("Data transformation failed", record_id=42)

        # Stage 3: Data export (after error recovery)
        export_logger = global_logger.get_logger("pipeline.export")
        export_logger.info("Starting data export", destination="postgres://warehouse")
        export_logger.info("Data export completed", records_exported=1000)

        captured = capsys.readouterr()

        # Verify all stages logged
        assert "Starting data ingestion" in captured.err
        assert "Data ingestion completed" in captured.err
        assert "Starting data transformation" in captured.err
        assert "Data transformation failed" in captured.err
        assert "ValueError: Invalid data format in record 42" in captured.err
        assert "Starting data export" in captured.err
        assert "Data export completed" in captured.err

    def test_concurrent_workers_scenario(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization with concurrent worker processes."""
        reset_pyvider_setup_for_testing()

        def worker_task(worker_id: int, task_count: int) -> list[str]:
            """Simulate worker task with logging."""
            worker_logger = global_logger.get_logger(f"worker.{worker_id}")
            messages = []

            worker_logger.info(f"Worker {worker_id} starting", task_count=task_count)

            for task_id in range(task_count):
                worker_logger.debug(f"Processing task {task_id}")

                # Simulate some work with occasional errors
                if task_id % 5 == 4:  # Every 5th task fails
                    worker_logger.warning(f"Task {task_id} retrying", retry_count=1)

                worker_logger.info(f"Task {task_id} completed", worker_id=worker_id)
                messages.append(f"Worker {worker_id} task {task_id}")

            worker_logger.info(f"Worker {worker_id} finished")
            return messages

        # Run concurrent workers
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(worker_task, worker_id, 5)
                for worker_id in range(4)
            ]

            all_messages = []
            for future in as_completed(futures):
                all_messages.extend(future.result())

        captured = capsys.readouterr()

        # Verify all workers logged
        for worker_id in range(4):
            assert f"Worker {worker_id} starting" in captured.err
            assert f"Worker {worker_id} finished" in captured.err

        # Verify task completion
        assert len(all_messages) == 4 * 5  # 4 workers x 5 tasks each

    @pytest.mark.asyncio
    async def test_async_web_server_scenario(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization in async web server scenario."""
        reset_pyvider_setup_for_testing()

        # Simulate async web server
        server_logger = global_logger.get_logger("server.async")

        async def handle_request(request_id: int, endpoint: str) -> None:
            """Simulate async request handling."""
            request_logger = global_logger.get_logger(f"server.request.{request_id}")

            request_logger.info(
                "Request started",
                request_id=request_id,
                endpoint=endpoint,
                domain="server",
                action="request",
                status="started"
            )

            # Simulate async work
            await asyncio.sleep(0.01)

            # Simulate database query
            db_logger = global_logger.get_logger("server.database")
            db_logger.debug(f"Executing query for request {request_id}")

            # Simulate response
            request_logger.info(
                "Request completed",
                request_id=request_id,
                response_time_ms=10,
                status_code=200,
                domain="server",
                action="request",
                status="success"
            )

        # Simulate multiple concurrent requests
        server_logger.info("Async server starting")

        tasks = [
            handle_request(1, "/api/users"),
            handle_request(2, "/api/posts"),
            handle_request(3, "/api/comments"),
        ]

        await asyncio.gather(*tasks)
        server_logger.info("All requests processed")

        captured = capsys.readouterr()

        # Verify async logging worked
        assert "Async server starting" in captured.err
        assert "All requests processed" in captured.err

        for _request_id in [1, 2, 3]:
            assert "Request started" in captured.err
            assert "Request completed" in captured.err

    def test_library_integration_scenario(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization when used as a library component."""
        reset_pyvider_setup_for_testing()

        # Simulate library that uses pyvider for internal logging
        class DataProcessor:
            def __init__(self) -> None:
                self.logger = global_logger.get_logger("dataprocessor.lib")
                self.logger.info("DataProcessor initialized")

            def process_data(self, data: dict[str, Any]) -> dict[str, Any]:
                self.logger.debug("Starting data processing", input_size=len(data))

                try:
                    # Simulate processing
                    result = {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}

                    self.logger.info(
                        "Data processing completed",
                        input_size=len(data),
                        output_size=len(result),
                        domain="data",
                        action="process",
                        status="success"
                    )
                    return result

                except Exception as e:
                    self.logger.exception(
                        "Data processing failed",
                        error_type=type(e).__name__,
                        domain="data",
                        action="process",
                        status="error"
                    )
                    raise

        # Use the library without explicit telemetry setup
        processor = DataProcessor()

        test_data = {"name": "john", "age": 30, "city": "portland"}
        result = processor.process_data(test_data)

        expected_result = {"name": "JOHN", "age": 30, "city": "PORTLAND"}
        assert result == expected_result

        captured = capsys.readouterr()
        assert "DataProcessor initialized" in captured.err
        assert "Data processing completed" in captured.err


class TestMigrationFromExplicitSetup:
    """Tests migration scenarios from explicit setup to lazy initialization."""

    def test_gradual_migration_scenario(self, capsys: CaptureFixture) -> None:
        """Test gradual migration from explicit setup to lazy initialization."""
        reset_pyvider_setup_for_testing()

        # Phase 1: Old code with explicit setup
        explicit_config = TelemetryConfig(
            service_name="migration-test",
            logging=LoggingConfig(
                default_level="DEBUG",
                console_formatter="json"
            )
        )
        setup_telemetry(explicit_config)

        # Old-style logging
        global_logger.info("Legacy logging with explicit setup")

        # Phase 2: New code assumes lazy initialization (should work fine)
        new_component_logger = global_logger.get_logger("new.component")
        new_component_logger.info("New component using existing setup")

        captured = capsys.readouterr()

        # Both should work
        assert "Legacy logging with explicit setup" in captured.err
        assert "New component using existing setup" in captured.err

        # Should be JSON format from explicit setup
        json_lines = [line for line in captured.err.splitlines()
                     if line.strip() and not line.startswith("[")]
        assert len(json_lines) >= 2

        for line in json_lines:
            log_data = json.loads(line)
            assert log_data["service_name"] == "migration-test"

    def test_mixed_initialization_order(self, capsys: CaptureFixture) -> None:
        """Test different initialization orders work correctly."""
        reset_pyvider_setup_for_testing()

        # Scenario 1: Lazy init first, then explicit setup
        global_logger.info("Message via lazy init")

        captured_lazy = capsys.readouterr()
        assert "Message via lazy init" in captured_lazy.err

        # Now explicit setup (should override)
        explicit_config = TelemetryConfig(
            service_name="explicit-override",
            logging=LoggingConfig(console_formatter="json")
        )
        setup_telemetry(explicit_config)

        global_logger.info("Message after explicit setup")

        captured_explicit = capsys.readouterr()
        assert "Message after explicit setup" in captured_explicit.err

        # Should be JSON format with service name
        json_lines = [line for line in captured_explicit.err.splitlines()
                     if line.strip() and not line.startswith("[")]
        log_data = json.loads(json_lines[0])
        assert log_data["service_name"] == "explicit-override"

    def test_configuration_precedence(self, capsys: CaptureFixture) -> None:
        """Test that explicit setup takes precedence over lazy initialization."""
        reset_pyvider_setup_for_testing()

        # Set environment for lazy init
        with patch.dict(os.environ, {
            "PYVIDER_SERVICE_NAME": "env-service",
            "PYVIDER_LOG_CONSOLE_FORMATTER": "key_value",
            "PYVIDER_LOG_LEVEL": "WARNING",
        }):
            # Trigger lazy init first
            global_logger.warning("Lazy init message")

            # Verify lazy config was used
            captured_lazy = capsys.readouterr()
            assert "Lazy init message" in captured_lazy.err
            # Should be key_value format (no JSON structure)

            # Now explicit setup with different config
            explicit_config = TelemetryConfig(
                service_name="explicit-service",
                logging=LoggingConfig(
                    console_formatter="json",
                    default_level="DEBUG"
                )
            )
            setup_telemetry(explicit_config)

            # Test that explicit config takes precedence
            global_logger.debug("Explicit setup message")  # Should appear (DEBUG level)

            captured_explicit = capsys.readouterr()
            assert "Explicit setup message" in captured_explicit.err

            # Should be JSON format with explicit service name
            json_lines = [line for line in captured_explicit.err.splitlines()
                         if line.strip() and not line.startswith("[")]
            log_data = json.loads(json_lines[0])
            assert log_data["service_name"] == "explicit-service"


class TestProductionReadinessScenarios:
    """Tests that verify production readiness of lazy initialization."""

    def test_high_throughput_scenario(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization under high throughput."""
        reset_pyvider_setup_for_testing()

        # Simulate high-throughput logging
        start_time = time.time()
        message_count = 1000

        for i in range(message_count):
            global_logger.info(f"High throughput message {i}", iteration=i)

        end_time = time.time()
        duration = end_time - start_time

        captured = capsys.readouterr()

        # Verify all messages were logged
        log_lines = [line for line in captured.err.splitlines()
                    if "High throughput message" in line]
        assert len(log_lines) == message_count

        # Verify reasonable performance
        messages_per_second = message_count / duration
        assert messages_per_second > 100, f"Too slow: {messages_per_second:.1f} msg/sec"

    def test_memory_stability_scenario(self, capsys: CaptureFixture) -> None:
        """Test memory stability with lazy initialization over time."""
        reset_pyvider_setup_for_testing()

        import gc

        # Baseline memory
        gc.collect()
        initial_objects = len(gc.get_objects())

        # Create many logger instances and log messages
        for i in range(100):
            logger_instance = global_logger.get_logger(f"memory.test.{i}")
            logger_instance.info(f"Memory test message {i}")

            # Periodically force garbage collection
            if i % 20 == 0:
                gc.collect()

        # Final memory check
        gc.collect()
        final_objects = len(gc.get_objects())

        object_growth = final_objects - initial_objects

        # Growth should be reasonable (not linear with logger count)
        assert object_growth < 500, f"Excessive memory growth: {object_growth} objects"

    def test_error_resilience_scenario(self, capsys: CaptureFixture) -> None:
        """Test error resilience in production-like conditions."""
        reset_pyvider_setup_for_testing()

        # Simulate various error conditions
        error_scenarios = [
            ("network_error", ConnectionError("Network unavailable")),
            ("data_error", ValueError("Invalid data format")),
            ("permission_error", PermissionError("Access denied")),
            ("system_error", OSError("System resource unavailable")),
        ]

        for error_name, exception in error_scenarios:
            try:
                raise exception
            except Exception:
                global_logger.exception(
                    f"Handling {error_name}",
                    error_type=error_name,
                    domain="system",
                    action="error_handling",
                    status="handled"
                )

        # Continue normal logging after errors
        global_logger.info("System recovered after error handling")

        captured = capsys.readouterr()

        # Verify all errors were logged with tracebacks
        for error_name, _ in error_scenarios:
            assert f"Handling {error_name}" in captured.err
            assert "Traceback" in captured.err

        assert "System recovered after error handling" in captured.err

    def test_graceful_shutdown_scenario(self, capsys: CaptureFixture) -> None:
        """Test graceful shutdown with lazy initialization."""
        reset_pyvider_setup_for_testing()

        # Simulate application lifecycle
        global_logger.info("Application starting with lazy init")

        # Simulate some work
        for i in range(5):
            worker_logger = global_logger.get_logger(f"worker.{i}")
            worker_logger.info(f"Worker {i} processing")

        # Test graceful shutdown
        async def test_shutdown() -> None:
            await shutdown_pyvider_telemetry()

        # Run shutdown
        import asyncio
        asyncio.run(test_shutdown())

        # Log after shutdown (should still work)
        global_logger.info("Message after shutdown")

        captured = capsys.readouterr()
        assert "Application starting with lazy init" in captured.err
        assert "Message after shutdown" in captured.err


class TestDocumentedBehaviorCompliance:
    """Tests that verify compliance with documented lazy initialization behavior."""

    def test_documented_environment_variables(self, capsys: CaptureFixture) -> None:
        """Test all documented environment variables work with lazy initialization."""
        reset_pyvider_setup_for_testing()

        documented_env_vars = {
            "PYVIDER_LOG_LEVEL": "DEBUG",
            "PYVIDER_LOG_CONSOLE_FORMATTER": "json",
            "PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED": "false",
            "PYVIDER_LOG_DAS_EMOJI_ENABLED": "true",
            "PYVIDER_LOG_OMIT_TIMESTAMP": "true",
            "PYVIDER_LOG_MODULE_LEVELS": "test.module:ERROR",
            "PYVIDER_SERVICE_NAME": "documented-service",
            "PYVIDER_TELEMETRY_DISABLED": "false",
        }

        with patch.dict(os.environ, documented_env_vars):
            # Test each documented feature
            global_logger.debug("Debug message")  # Should appear (DEBUG level)

            # Test module-specific level
            test_logger = global_logger.get_logger("test.module")
            test_logger.warning("Module warning")  # Should be filtered (ERROR level only)
            test_logger.error("Module error")  # Should appear

            # Test DAS with disabled logger name emoji
            global_logger.info(
                "DAS test",
                domain="auth",
                action="login",
                status="success"
            )

        captured = capsys.readouterr()

        # Parse JSON output
        json_lines = []
        for line in captured.err.splitlines():
            if line.strip() and not line.startswith("["):
                with contextlib.suppress(json.JSONDecodeError):
                    json_lines.append(json.loads(line))

        # Verify documented behavior
        debug_logs = [log for log in json_lines if log.get("level") == "debug"]
        assert len(debug_logs) > 0, "DEBUG level should appear"

        # Verify service name injection
        service_logs = [log for log in json_lines if "service_name" in log]
        assert all(log["service_name"] == "documented-service" for log in service_logs)

        # Verify timestamp omission
        assert all("timestamp" not in log for log in json_lines), "Timestamps should be omitted"

        # Verify module filtering
        assert not any("Module warning" in log.get("event", "") for log in json_lines)
        assert any("Module error" in log.get("event", "") for log in json_lines)

        # Verify DAS emoji without logger name emoji
        das_logs = [log for log in json_lines if "DAS test" in log.get("event", "")]
        assert len(das_logs) == 1
        assert "[🔑][➡️][✅]" in das_logs[0]["event"]
        # Should NOT have logger name emoji prefix before DAS

    def test_backward_compatibility_promise(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization maintains backward compatibility."""
        reset_pyvider_setup_for_testing()

        # Old code pattern: immediate logging without setup
        global_logger.info("Legacy immediate logging")

        # Old code pattern: named logger creation
        legacy_logger = global_logger.get_logger("legacy.component")
        legacy_logger.warning("Legacy component warning")

        # Old code pattern: exception logging
        try:
            raise RuntimeError("Legacy exception")
        except RuntimeError:
            legacy_logger.exception("Legacy exception handling")

        # Should work exactly as before
        captured = capsys.readouterr()
        assert "Legacy immediate logging" in captured.err
        assert "Legacy component warning" in captured.err
        assert "Legacy exception handling" in captured.err
        assert "RuntimeError: Legacy exception" in captured.err

    def test_thread_safety_guarantees(self, capsys: CaptureFixture) -> None:
        """Test documented thread safety guarantees."""
        reset_pyvider_setup_for_testing()

        import time

        # Stress test with many threads starting simultaneously
        thread_count = 50
        barrier = threading.Barrier(thread_count)
        results: dict[int, bool] = {}
        errors: list[Exception] = []

        def stress_worker(worker_id: int) -> None:
            try:
                # Synchronize start time for maximum contention
                barrier.wait()

                # Each thread creates its own logger and logs
                worker_logger = global_logger.get_logger(f"stress.worker.{worker_id}")

                for i in range(10):
                    worker_logger.info(f"Worker {worker_id} message {i}")
                    time.sleep(0.001)  # Small delay to increase contention

                results[worker_id] = True

            except Exception as e:
                errors.append(e)
                results[worker_id] = False

        # Start all threads
        threads = []
        for i in range(thread_count):
            thread = threading.Thread(target=stress_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=30.0)
            assert not thread.is_alive(), "Thread failed to complete"

        # Verify thread safety
        assert len(errors) == 0, f"Thread safety violated with errors: {errors}"
        assert len(results) == thread_count
        assert all(results.values()), "Some threads failed"

        # Verify all messages were logged
        captured = capsys.readouterr()
        for worker_id in range(thread_count):
            for i in range(10):
                assert f"Worker {worker_id} message {i}" in captured.err

    def test_performance_requirements(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization meets performance requirements."""
        reset_pyvider_setup_for_testing()

        import time

        # Test initialization overhead
        start_time = time.time()

        # First log should include initialization time
        global_logger.info("First message triggers initialization")

        init_time = time.time() - start_time

        # Subsequent logs should be fast
        start_time = time.time()

        for i in range(100):
            global_logger.info(f"Performance test message {i}")

        subsequent_time = time.time() - start_time

        # Performance requirements
        assert init_time < 0.1, f"Initialization too slow: {init_time:.3f}s"

        messages_per_second = 100 / subsequent_time
        assert messages_per_second > 1000, f"Subsequent logging too slow: {messages_per_second:.1f} msg/sec"

        captured = capsys.readouterr()
        assert "First message triggers initialization" in captured.err


class TestLazyInitializationDocumentation:
    """Tests that verify examples from documentation work correctly."""

    def test_basic_usage_example(self, capsys: CaptureFixture) -> None:
        """Test the basic usage example from documentation."""
        reset_pyvider_setup_for_testing()

        # Example from docs: immediate logging without setup
        from pyvider.telemetry import logger

        logger.info("Application started", version="1.0.0")
        logger.debug("Debug information", component="main")
        logger.warning("This is a warning", code="W001")
        logger.error("An error occurred", error_code="E123")

        captured = capsys.readouterr()
        assert "Application started" in captured.err
        assert "This is a warning" in captured.err
        assert "An error occurred" in captured.err
        # Debug might be filtered depending on default level

    def test_named_logger_example(self, capsys: CaptureFixture) -> None:
        """Test the named logger example from documentation."""
        reset_pyvider_setup_for_testing()

        # Example from docs: component-specific loggers
        from pyvider.telemetry import logger

        auth_logger = logger.get_logger("auth.service")
        db_logger = logger.get_logger("database.connection")
        api_logger = logger.get_logger("api.handlers")

        auth_logger.info("User authentication successful", user_id=12345)
        db_logger.warning("Connection timeout", host="localhost", timeout_ms=5000)
        api_logger.debug("Request processed", endpoint="/api/users", duration_ms=23)

        captured = capsys.readouterr()
        assert "User authentication successful" in captured.err
        assert "Connection timeout" in captured.err

    def test_environment_config_example(self, capsys: CaptureFixture) -> None:
        """Test the environment configuration example from documentation."""
        reset_pyvider_setup_for_testing()

        # Example from docs: environment-based configuration
        with patch.dict(os.environ, {
            "PYVIDER_SERVICE_NAME": "my-service",
            "PYVIDER_LOG_LEVEL": "INFO",
            "PYVIDER_LOG_CONSOLE_FORMATTER": "json",
            "PYVIDER_LOG_MODULE_LEVELS": "auth:DEBUG,db:ERROR",
        }):
            from pyvider.telemetry import logger

            logger.info("Service started")

            auth_logger = logger.get_logger("auth")
            auth_logger.debug("Auth debug message")  # Should appear

            db_logger = logger.get_logger("db")
            db_logger.warning("DB warning")  # Should be filtered
            db_logger.error("DB error")  # Should appear

        captured = capsys.readouterr()

        # Parse JSON output
        json_lines = []
        for line in captured.err.splitlines():
            if line.strip() and not line.startswith("["):
                with contextlib.suppress(json.JSONDecodeError):
                    json_lines.append(json.loads(line))

        # Verify example worked as documented
        service_logs = [log for log in json_lines if "service_name" in log]
        assert all(log["service_name"] == "my-service" for log in service_logs)

        assert any("Auth debug message" in log.get("event", "") for log in json_lines)
        assert not any("DB warning" in log.get("event", "") for log in json_lines)
        assert any("DB error" in log.get("event", "") for log in json_lines)

    def test_migration_example(self, capsys: CaptureFixture) -> None:
        """Test the migration example from documentation."""
        reset_pyvider_setup_for_testing()

        # Example from docs: gradual migration
        from pyvider.telemetry import (
            LoggingConfig,
            TelemetryConfig,
            logger,
            setup_telemetry,
        )

        # Old code: works immediately without setup
        logger.info("Legacy code logging")

        # New code: explicit setup still works
        config = TelemetryConfig(
            service_name="migrated-service",
            logging=LoggingConfig(console_formatter="json")
        )
        setup_telemetry(config)

        # Both old and new code work together
        logger.info("After explicit setup")

        captured = capsys.readouterr()
        assert "Legacy code logging" in captured.err
        assert "After explicit setup" in captured.err

        # After explicit setup, should be JSON format
        json_lines = [line for line in captured.err.splitlines()
                     if line.strip() and not line.startswith("[") and "After explicit setup" in line]
        assert len(json_lines) > 0

        log_data = json.loads(json_lines[0])
        assert log_data["service_name"] == "migrated-service"

# 🧪🎯
