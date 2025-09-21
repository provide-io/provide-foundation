"""Comprehensive tests for OpenObserve OTLP integration module."""

from unittest.mock import Mock, patch


class TestOTLPConstants:
    """Test OTLP module constants and feature detection."""

    def test_has_otel_logs_flag_exists(self) -> None:
        """Test that _HAS_OTEL_LOGS flag exists."""
        from provide.foundation.integrations.openobserve.otlp import _HAS_OTEL_LOGS

        assert isinstance(_HAS_OTEL_LOGS, bool)

    def test_module_imports_correctly(self) -> None:
        """Test that module can be imported without errors."""
        import provide.foundation.integrations.openobserve.otlp as otlp_module

        assert hasattr(otlp_module, "send_log_otlp")
        assert hasattr(otlp_module, "send_log_bulk")
        assert hasattr(otlp_module, "send_log")
        assert hasattr(otlp_module, "create_otlp_logger_provider")


class TestSendLogOTLP:
    """Test send_log_otlp function."""

    def test_send_log_otlp_without_otel_returns_false(self) -> None:
        """Test that function returns False when OpenTelemetry is not available."""
        from provide.foundation.integrations.openobserve.otlp import send_log_otlp

        with patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", False):
            result = send_log_otlp("Test message")
            assert result is False

    def test_send_log_otlp_without_endpoint_returns_false(self) -> None:
        """Test that function returns False when no OTLP endpoint is configured."""
        from provide.foundation.integrations.openobserve.otlp import send_log_otlp

        mock_config = Mock()
        mock_config.otlp_endpoint = None

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
        ):
            mock_from_env.return_value = mock_config

            result = send_log_otlp("Test message")
            assert result is False

    def test_send_log_otlp_success_basic(self) -> None:
        """Test successful OTLP log sending with basic configuration."""
        from provide.foundation.integrations.openobserve.otlp import send_log_otlp

        # Mock configuration
        mock_config = Mock()
        mock_config.otlp_endpoint = "http://localhost:4318"
        mock_config.otlp_traces_endpoint = None
        mock_config.service_name = "test-service"
        mock_config.service_version = "1.0.0"
        mock_config.openobserve_org = "default"
        mock_config.openobserve_stream = "default"
        mock_config.get_otlp_headers_dict.return_value = {"Authorization": "Bearer token"}

        # Mock OpenTelemetry components
        mock_resource = Mock()
        mock_exporter = Mock()
        mock_logger_provider = Mock()
        mock_otel_logger = Mock()
        mock_span_context = Mock()
        mock_span_context.trace_id = 12345
        mock_span_context.span_id = 67890
        mock_current_span = Mock()
        mock_current_span.is_recording.return_value = True
        mock_current_span.get_span_context.return_value = mock_span_context

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.Resource") as mock_resource_class,
            patch("provide.foundation.integrations.openobserve.otlp.OTLPLogExporter") as mock_exporter_class,
            patch("provide.foundation.integrations.openobserve.otlp.LoggerProvider") as mock_provider_class,
            patch("provide.foundation.integrations.openobserve.otlp.BatchLogRecordProcessor"),
            patch(
                "provide.foundation.integrations.openobserve.otlp.ResourceAttributes"
            ) as mock_resource_attrs,
            patch("provide.foundation.integrations.openobserve.otlp.trace") as mock_trace,
        ):
            mock_from_env.return_value = mock_config
            mock_resource_class.create.return_value = mock_resource
            mock_exporter_class.return_value = mock_exporter
            mock_provider_class.return_value = mock_logger_provider
            mock_logger_provider.get_logger.return_value = mock_otel_logger
            mock_resource_attrs.SERVICE_NAME = "service.name"
            mock_resource_attrs.SERVICE_VERSION = "service.version"
            mock_trace.get_current_span.return_value = mock_current_span

            result = send_log_otlp(
                message="Test OTLP message",
                level="INFO",
                service="custom-service",
                attributes={"key": "value"},
            )

            assert result is True

            # Verify resource creation
            mock_resource_class.create.assert_called_once()

            # Verify exporter creation
            mock_exporter_class.assert_called_once_with(
                endpoint="http://localhost:4318/v1/logs",
                headers={"Authorization": "Bearer token", "organization": "default", "stream-name": "default"},
            )

            # Verify log emission
            mock_otel_logger.emit.assert_called_once()
            call_args = mock_otel_logger.emit.call_args[1]
            assert call_args["severity_number"] == 9  # INFO
            assert call_args["severity_text"] == "INFO"
            assert call_args["body"] == "Test OTLP message"
            assert "key" in call_args["attributes"]
            assert "trace_id" in call_args["attributes"]

            # Verify flush
            mock_logger_provider.force_flush.assert_called_once()

    def test_send_log_otlp_with_traces_endpoint(self) -> None:
        """Test OTLP log sending when traces endpoint is configured."""
        from provide.foundation.integrations.openobserve.otlp import send_log_otlp

        mock_config = Mock()
        mock_config.otlp_endpoint = "http://localhost:4318"
        mock_config.otlp_traces_endpoint = "http://localhost:4318/v1/traces"
        mock_config.service_name = "test-service"
        mock_config.service_version = None
        mock_config.openobserve_org = None
        mock_config.get_otlp_headers_dict.return_value = {}

        mock_exporter = Mock()
        mock_logger_provider = Mock()
        mock_otel_logger = Mock()

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.Resource"),
            patch("provide.foundation.integrations.openobserve.otlp.OTLPLogExporter") as mock_exporter_class,
            patch("provide.foundation.integrations.openobserve.otlp.LoggerProvider") as mock_provider_class,
            patch("provide.foundation.integrations.openobserve.otlp.BatchLogRecordProcessor"),
            patch("provide.foundation.integrations.openobserve.otlp.trace") as mock_trace,
        ):
            mock_from_env.return_value = mock_config
            mock_exporter_class.return_value = mock_exporter
            mock_provider_class.return_value = mock_logger_provider
            mock_logger_provider.get_logger.return_value = mock_otel_logger
            mock_trace.get_current_span.return_value = Mock(is_recording=Mock(return_value=False))

            result = send_log_otlp("Test message")

            assert result is True

            # Verify logs endpoint derived from traces endpoint
            mock_exporter_class.assert_called_once_with(endpoint="http://localhost:4318/v1/logs", headers={})

    def test_send_log_otlp_level_mapping(self) -> None:
        """Test severity level mapping for different log levels."""
        from provide.foundation.integrations.openobserve.otlp import send_log_otlp

        mock_config = Mock()
        mock_config.otlp_endpoint = "http://localhost:4318"
        mock_config.otlp_traces_endpoint = None
        mock_config.service_name = "test-service"
        mock_config.service_version = None
        mock_config.openobserve_org = None
        mock_config.get_otlp_headers_dict.return_value = {}

        mock_otel_logger = Mock()
        mock_logger_provider = Mock()
        mock_logger_provider.get_logger.return_value = mock_otel_logger

        test_levels = [
            ("TRACE", 1),
            ("DEBUG", 5),
            ("INFO", 9),
            ("WARN", 13),
            ("WARNING", 13),
            ("ERROR", 17),
            ("FATAL", 21),
            ("CRITICAL", 21),
            ("UNKNOWN", 9),  # Default fallback
        ]

        for level, expected_severity in test_levels:
            with (
                patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
                patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
                patch("provide.foundation.integrations.openobserve.otlp.Resource"),
                patch("provide.foundation.integrations.openobserve.otlp.OTLPLogExporter"),
                patch(
                    "provide.foundation.integrations.openobserve.otlp.LoggerProvider"
                ) as mock_provider_class,
                patch("provide.foundation.integrations.openobserve.otlp.BatchLogRecordProcessor"),
                patch("provide.foundation.integrations.openobserve.otlp.trace") as mock_trace,
            ):
                mock_from_env.return_value = mock_config
                mock_provider_class.return_value = mock_logger_provider
                mock_trace.get_current_span.return_value = Mock(is_recording=Mock(return_value=False))

                result = send_log_otlp(f"Test {level} message", level=level)

                assert result is True

                # Verify severity mapping
                call_args = mock_otel_logger.emit.call_args[1]
                assert call_args["severity_number"] == expected_severity
                assert call_args["severity_text"] == level.upper()

                mock_otel_logger.reset_mock()

    def test_send_log_otlp_exception_handling(self) -> None:
        """Test exception handling in OTLP log sending."""
        from provide.foundation.integrations.openobserve.otlp import send_log_otlp

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
        ):
            # Mock config to raise exception
            mock_from_env.side_effect = Exception("Config error")

            result = send_log_otlp("Test message")

            assert result is False


class TestSendLogBulk:
    """Test send_log_bulk function."""

    def test_send_log_bulk_success(self) -> None:
        """Test successful bulk API log sending."""
        from provide.foundation.integrations.openobserve.otlp import send_log_bulk

        # Mock dependencies
        mock_client = Mock()
        mock_client.url = "http://localhost:5080"
        mock_client.organization = "default"
        mock_client.timeout = 30
        mock_client.session.headers = {"Authorization": "Basic token"}

        mock_config = Mock()
        mock_config.service_name = "bulk-service"
        mock_config.openobserve_stream = "logs"

        mock_response = Mock()
        mock_response.status_code = 200

        with (
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.datetime") as mock_datetime,
            patch("requests.post") as mock_post,
        ):
            mock_from_env.return_value = mock_config
            mock_datetime.now.return_value.timestamp.return_value = 1234567890.123456
            mock_post.return_value = mock_response

            result = send_log_bulk(
                message="Bulk test message",
                level="ERROR",
                service="custom-service",
                attributes={"error_code": 500},
                client=mock_client,
            )

            assert result is True

            # Verify requests.post call
            mock_post.assert_called_once()
            call_args = mock_post.call_args

            # First argument is the URL
            assert call_args[0][0] == "http://localhost:5080/api/default/_bulk"

            # Keyword arguments
            assert call_args[1]["headers"] == {"Authorization": "Basic token"}
            assert call_args[1]["timeout"] == 30

            # Verify bulk data format contains expected log entry
            bulk_data = call_args[1]["data"]
            assert "Bulk test message" in bulk_data
            assert "ERROR" in bulk_data
            assert "custom-service" in bulk_data

    def test_send_log_bulk_creates_client_when_none_provided(self) -> None:
        """Test that bulk function creates client when none provided."""
        from provide.foundation.integrations.openobserve.otlp import send_log_bulk

        # Mock client with required attributes
        mock_client = Mock()
        mock_client.url = "http://test-client:5080"
        mock_client.organization = "test-org"
        mock_client.timeout = 30
        mock_client.session.headers = {"Authorization": "Bearer test-token"}

        # Mock config
        mock_config = Mock()
        mock_config.service_name = "test-service"
        mock_config.openobserve_stream = "test-stream"

        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200

        with (
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.OpenObserveClient") as mock_client_class,
            patch("provide.foundation.integrations.openobserve.otlp.datetime") as mock_datetime,
            patch("requests.post") as mock_post,
        ):
            mock_from_env.return_value = mock_config
            mock_client_class.from_config.return_value = mock_client
            mock_datetime.now.return_value.timestamp.return_value = 1234567890.0
            mock_post.return_value = mock_response

            result = send_log_bulk("Test message")

            assert result is True
            mock_client_class.from_config.assert_called_once()

    def test_send_log_bulk_exception_handling(self) -> None:
        """Test exception handling in bulk log sending."""
        from provide.foundation.integrations.openobserve.otlp import send_log_bulk

        # Mock client with required attributes
        mock_client = Mock()
        mock_client.url = "http://error-test:5080"
        mock_client.organization = "error-org"
        mock_client.timeout = 30
        mock_client.session.headers = {"Authorization": "Bearer error-token"}

        # Mock config
        mock_config = Mock()
        mock_config.service_name = "error-service"
        mock_config.openobserve_stream = "error-stream"

        with (
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.datetime") as mock_datetime,
            patch("requests.post") as mock_post,
        ):
            mock_from_env.return_value = mock_config
            mock_datetime.now.return_value.timestamp.return_value = 1234567890.0
            mock_post.side_effect = Exception("Bulk API error")

            result = send_log_bulk("Test message", client=mock_client)

            assert result is False


class TestSendLog:
    """Test send_log function (main entry point)."""

    def test_send_log_prefer_otlp_success(self) -> None:
        """Test send_log with OTLP preference when OTLP succeeds."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.integrations.openobserve.otlp.send_log_otlp") as mock_otlp,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_otlp.return_value = True

            result = send_log("Test message", prefer_otlp=True)

            assert result is True
            mock_otlp.assert_called_once_with("Test message", "INFO", None, None)
            mock_bulk.assert_not_called()

    def test_send_log_otlp_fails_fallback_to_bulk(self) -> None:
        """Test send_log falls back to bulk API when OTLP fails."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.integrations.openobserve.otlp.send_log_otlp") as mock_otlp,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_otlp.return_value = False
            mock_bulk.return_value = True

            result = send_log("Test message", prefer_otlp=True)

            assert result is True
            mock_otlp.assert_called_once()
            mock_bulk.assert_called_once_with("Test message", "INFO", None, None, None)

    def test_send_log_prefer_bulk_skips_otlp(self) -> None:
        """Test send_log skips OTLP when prefer_otlp=False."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        with (
            patch("provide.foundation.integrations.openobserve.otlp.send_log_otlp") as mock_otlp,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_bulk.return_value = True

            result = send_log("Test message", prefer_otlp=False)

            assert result is True
            mock_otlp.assert_not_called()
            mock_bulk.assert_called_once()

    def test_send_log_no_otel_fallback_to_bulk(self) -> None:
        """Test send_log uses bulk API when OpenTelemetry not available."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", False),
            patch("provide.foundation.integrations.openobserve.otlp.send_log_otlp") as mock_otlp,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_bulk.return_value = True

            result = send_log("Test message", prefer_otlp=True)

            assert result is True
            mock_otlp.assert_not_called()
            mock_bulk.assert_called_once()


class TestCreateOTLPLoggerProvider:
    """Test create_otlp_logger_provider function."""

    def test_create_otlp_logger_provider_without_otel_returns_none(self) -> None:
        """Test that function returns None when OpenTelemetry is not available."""
        from provide.foundation.integrations.openobserve.otlp import create_otlp_logger_provider

        with patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", False):
            result = create_otlp_logger_provider()
            assert result is None

    def test_create_otlp_logger_provider_without_endpoint_returns_none(self) -> None:
        """Test that function returns None when no OTLP endpoint is configured."""
        from provide.foundation.integrations.openobserve.otlp import create_otlp_logger_provider

        mock_config = Mock()
        mock_config.otlp_endpoint = None

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
        ):
            mock_from_env.return_value = mock_config

            result = create_otlp_logger_provider()
            assert result is None

    def test_create_otlp_logger_provider_success(self) -> None:
        """Test successful OTLP logger provider creation."""
        from provide.foundation.integrations.openobserve.otlp import create_otlp_logger_provider

        mock_config = Mock()
        mock_config.otlp_endpoint = "http://localhost:4318"
        mock_config.otlp_traces_endpoint = None
        mock_config.service_name = "provider-service"
        mock_config.service_version = "2.0.0"
        mock_config.openobserve_org = "test-org"
        mock_config.openobserve_stream = "test-stream"
        mock_config.get_otlp_headers_dict.return_value = {"auth": "token"}

        mock_logger_provider = Mock()
        mock_resource = Mock()
        mock_exporter = Mock()

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.Resource") as mock_resource_class,
            patch("provide.foundation.integrations.openobserve.otlp.OTLPLogExporter") as mock_exporter_class,
            patch("provide.foundation.integrations.openobserve.otlp.LoggerProvider") as mock_provider_class,
            patch("provide.foundation.integrations.openobserve.otlp.BatchLogRecordProcessor"),
        ):
            mock_from_env.return_value = mock_config
            mock_resource_class.create.return_value = mock_resource
            mock_exporter_class.return_value = mock_exporter
            mock_provider_class.return_value = mock_logger_provider

            result = create_otlp_logger_provider()

            assert result == mock_logger_provider

            # Verify configuration
            mock_resource_class.create.assert_called_once()
            mock_exporter_class.assert_called_once_with(
                endpoint="http://localhost:4318/v1/logs",
                headers={"auth": "token", "organization": "test-org", "stream-name": "test-stream"},
            )
            mock_logger_provider.add_log_record_processor.assert_called_once()

    def test_create_otlp_logger_provider_exception_handling(self) -> None:
        """Test exception handling in logger provider creation."""
        from provide.foundation.integrations.openobserve.otlp import create_otlp_logger_provider

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
        ):
            mock_from_env.side_effect = Exception("Provider creation error")

            result = create_otlp_logger_provider()

            assert result is None


class TestOTLPIntegration:
    """Test OTLP integration scenarios and edge cases."""

    def test_trace_context_extraction(self) -> None:
        """Test trace context extraction in OTLP logging."""
        from provide.foundation.integrations.openobserve.otlp import send_log_otlp

        # Mock all the OTLP dependencies
        mock_config = Mock()
        mock_config.otlp_endpoint = "http://localhost:4318"
        mock_config.otlp_traces_endpoint = None
        mock_config.service_name = "trace-test"
        mock_config.service_version = None
        mock_config.openobserve_org = None
        mock_config.get_otlp_headers_dict.return_value = {}

        mock_otel_logger = Mock()
        mock_logger_provider = Mock()
        mock_logger_provider.get_logger.return_value = mock_otel_logger
        mock_logger_provider.force_flush.return_value = None

        # Test case 1: Active span that is recording (should extract trace context)
        mock_span_context = Mock()
        mock_span_context.trace_id = 12345
        mock_span_context.span_id = 269

        mock_current_span = Mock()
        mock_current_span.is_recording.return_value = True
        mock_current_span.get_span_context.return_value = mock_span_context

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.Resource"),
            patch("provide.foundation.integrations.openobserve.otlp.OTLPLogExporter"),
            patch("provide.foundation.integrations.openobserve.otlp.LoggerProvider") as mock_provider_class,
            patch("provide.foundation.integrations.openobserve.otlp.BatchLogRecordProcessor"),
            patch("provide.foundation.integrations.openobserve.otlp.trace") as mock_trace,
        ):
            mock_from_env.return_value = mock_config
            mock_provider_class.return_value = mock_logger_provider
            mock_trace.get_current_span.return_value = mock_current_span

            result = send_log_otlp("Test with trace context")

            assert result is True

            # Verify that emit was called with trace context
            mock_otel_logger.emit.assert_called_once()
            call_kwargs = mock_otel_logger.emit.call_args[1]
            attributes = call_kwargs["attributes"]

            # Verify trace context was added
            assert attributes["trace_id"] == "00000000000000000000000000003039"  # hex format of 12345
            assert attributes["span_id"] == "000000000000010d"  # hex format of 269

        # Test case 2: No active span (should not add trace context)
        mock_otel_logger.reset_mock()

        with (
            patch("provide.foundation.integrations.openobserve.otlp._HAS_OTEL_LOGS", True),
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.Resource"),
            patch("provide.foundation.integrations.openobserve.otlp.OTLPLogExporter"),
            patch("provide.foundation.integrations.openobserve.otlp.LoggerProvider") as mock_provider_class,
            patch("provide.foundation.integrations.openobserve.otlp.BatchLogRecordProcessor"),
            patch("provide.foundation.integrations.openobserve.otlp.trace") as mock_trace,
        ):
            mock_from_env.return_value = mock_config
            mock_provider_class.return_value = mock_logger_provider
            mock_trace.get_current_span.return_value = None

            result = send_log_otlp("Test without trace context")

            assert result is True

            # Verify that emit was called without trace context
            mock_otel_logger.emit.assert_called_once()
            call_kwargs = mock_otel_logger.emit.call_args[1]
            attributes = call_kwargs["attributes"]

            # Verify trace context was not added
            assert "trace_id" not in attributes
            assert "span_id" not in attributes

    def test_bulk_api_log_structure(self) -> None:
        """Test the structure of logs sent via bulk API."""
        from provide.foundation.integrations.openobserve.otlp import send_log_bulk

        mock_client = Mock()
        mock_client.url = "http://localhost:5080"
        mock_client.organization = "test-org"
        mock_client.session.headers = {"Authorization": "Bearer test-token"}
        mock_client.timeout = 30

        mock_config = Mock()
        mock_config.service_name = "structure-test"
        mock_config.openobserve_stream = "test-stream"

        mock_response = Mock()
        mock_response.status_code = 200

        with (
            patch("provide.foundation.logger.config.telemetry.TelemetryConfig.from_env") as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.datetime") as mock_datetime,
            patch("requests.post") as mock_post,
        ):
            mock_from_env.return_value = mock_config
            mock_datetime.now.return_value.timestamp.return_value = 1609459200.0  # 2021-01-01 00:00:00
            mock_post.return_value = mock_response

            result = send_log_bulk(
                message="Structure test",
                level="WARN",
                service=None,  # Should use config service name
                attributes={"custom": "attribute", "numeric": 42},
                client=mock_client,
            )

            assert result is True

            # Verify the requests.post was called correctly
            mock_post.assert_called_once()
            call_args = mock_post.call_args

            # Check URL construction
            expected_url = "http://localhost:5080/api/test-org/_bulk"
            assert call_args[0][0] == expected_url

            # Check headers
            assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

            # Check timeout
            assert call_args[1]["timeout"] == 30

            # Check bulk data structure
            bulk_data = call_args[1]["data"]
            lines = bulk_data.strip().split("\n")
            assert len(lines) == 2  # Index line + data line

            # Parse index line
            import json

            index_line = json.loads(lines[0])
            assert index_line == {"index": {"_index": "test-stream"}}

            # Parse data line
            log_record = json.loads(lines[1])
            assert log_record["_timestamp"] == 1609459200000000  # microseconds
            assert log_record["level"] == "WARN"
            assert log_record["message"] == "Structure test"
            assert log_record["service"] == "structure-test"  # From config
            assert log_record["custom"] == "attribute"
            assert log_record["numeric"] == 42
