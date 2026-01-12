#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for OTLP resource creation and attribute management.

Tests all functionality in logger/otlp/resource.py including resource attribute
building and OpenTelemetry Resource instance creation."""

from __future__ import annotations

from provide.testkit.mocking import Mock, patch
import pytest

# Skip all tests in this module if opentelemetry is not installed
pytest.importorskip("opentelemetry")

from provide.foundation.logger.otlp.resource import (
    build_resource_attributes,
    create_otlp_resource,
)


class TestBuildResourceAttributes:
    """Tests for build_resource_attributes function."""

    def test_build_with_service_name_only(self) -> None:
        """Test building resource attributes with only service name."""
        attrs = build_resource_attributes("test-service")

        assert attrs == {"service.name": "test-service"}
        assert len(attrs) == 1

    def test_build_with_service_version(self) -> None:
        """Test building resource attributes with service name and version."""
        attrs = build_resource_attributes(
            "test-service",
            service_version="1.2.3",
        )

        assert attrs["service.name"] == "test-service"
        assert attrs["service.version"] == "1.2.3"
        assert len(attrs) == 2

    def test_build_with_environment(self) -> None:
        """Test building resource attributes with environment."""
        attrs = build_resource_attributes(
            "test-service",
            environment="production",
        )

        assert attrs["service.name"] == "test-service"
        assert attrs["deployment.environment"] == "production"
        assert len(attrs) == 2

    def test_build_with_all_standard_attributes(self) -> None:
        """Test building resource attributes with all standard attributes."""
        attrs = build_resource_attributes(
            "test-service",
            service_version="2.0.0",
            environment="staging",
        )

        assert attrs["service.name"] == "test-service"
        assert attrs["service.version"] == "2.0.0"
        assert attrs["deployment.environment"] == "staging"
        assert len(attrs) == 3

    def test_build_with_additional_attrs(self) -> None:
        """Test building resource attributes with additional custom attributes."""
        additional = {
            "team": "platform",
            "region": "us-east-1",
        }

        attrs = build_resource_attributes(
            "test-service",
            additional_attrs=additional,
        )

        assert attrs["service.name"] == "test-service"
        assert attrs["team"] == "platform"
        assert attrs["region"] == "us-east-1"
        assert len(attrs) == 3

    def test_build_with_all_parameters(self) -> None:
        """Test building resource attributes with all parameters."""
        additional = {
            "team": "platform",
            "custom.attribute": "value",
        }

        attrs = build_resource_attributes(
            "comprehensive-service",
            service_version="3.0.0",
            environment="development",
            additional_attrs=additional,
        )

        assert attrs["service.name"] == "comprehensive-service"
        assert attrs["service.version"] == "3.0.0"
        assert attrs["deployment.environment"] == "development"
        assert attrs["team"] == "platform"
        assert attrs["custom.attribute"] == "value"
        assert len(attrs) == 5

    def test_build_with_none_service_version(self) -> None:
        """Test that None service_version is not included in attributes."""
        attrs = build_resource_attributes(
            "test-service",
            service_version=None,
        )

        assert "service.version" not in attrs
        assert attrs == {"service.name": "test-service"}

    def test_build_with_none_environment(self) -> None:
        """Test that None environment is not included in attributes."""
        attrs = build_resource_attributes(
            "test-service",
            environment=None,
        )

        assert "deployment.environment" not in attrs
        assert attrs == {"service.name": "test-service"}

    def test_build_with_none_additional_attrs(self) -> None:
        """Test that None additional_attrs doesn't cause errors."""
        attrs = build_resource_attributes(
            "test-service",
            additional_attrs=None,
        )

        assert attrs == {"service.name": "test-service"}

    def test_build_with_empty_additional_attrs(self) -> None:
        """Test building with empty additional attributes dictionary."""
        attrs = build_resource_attributes(
            "test-service",
            additional_attrs={},
        )

        assert attrs == {"service.name": "test-service"}

    def test_build_additional_attrs_overwrites_standard(self) -> None:
        """Test that additional_attrs can overwrite standard attributes."""
        additional = {
            "service.name": "overridden-service",
        }

        attrs = build_resource_attributes(
            "original-service",
            additional_attrs=additional,
        )

        # additional_attrs are applied after standard attrs, so they overwrite
        assert attrs["service.name"] == "overridden-service"

    def test_build_with_various_environments(self) -> None:
        """Test building with various common environment names."""
        for env in ["dev", "staging", "production", "test", "local"]:
            attrs = build_resource_attributes(
                "test-service",
                environment=env,
            )
            assert attrs["deployment.environment"] == env

    def test_build_preserves_attribute_types(self) -> None:
        """Test that attribute types are preserved correctly."""
        additional = {
            "count": 123,
            "enabled": True,
            "ratio": 3.14,
        }

        attrs = build_resource_attributes(
            "test-service",
            additional_attrs=additional,
        )

        assert isinstance(attrs["count"], int)
        assert isinstance(attrs["enabled"], bool)
        assert isinstance(attrs["ratio"], float)


class TestCreateOtlpResource:
    """Tests for create_otlp_resource function."""

    @patch("opentelemetry.sdk.resources.Resource")
    def test_create_resource_with_sdk_available(self, mock_resource_class: Mock) -> None:
        """Test creating resource when OpenTelemetry SDK is available."""
        mock_resource = Mock()
        mock_resource_class.create.return_value = mock_resource

        result = create_otlp_resource("test-service")

        assert result == mock_resource
        mock_resource_class.create.assert_called_once()

        # Check the attributes passed to Resource.create()
        call_args = mock_resource_class.create.call_args[0][0]
        assert call_args["service.name"] == "test-service"

    @patch("opentelemetry.sdk.resources.Resource")
    def test_create_resource_with_version(self, mock_resource_class: Mock) -> None:
        """Test creating resource with service version."""
        mock_resource = Mock()
        mock_resource_class.create.return_value = mock_resource

        result = create_otlp_resource(
            "test-service",
            service_version="1.0.0",
        )

        assert result == mock_resource
        call_args = mock_resource_class.create.call_args[0][0]
        assert call_args["service.name"] == "test-service"
        assert call_args["service.version"] == "1.0.0"

    @patch("opentelemetry.sdk.resources.Resource")
    def test_create_resource_with_environment(self, mock_resource_class: Mock) -> None:
        """Test creating resource with environment."""
        mock_resource = Mock()
        mock_resource_class.create.return_value = mock_resource

        result = create_otlp_resource(
            "test-service",
            environment="production",
        )

        assert result == mock_resource
        call_args = mock_resource_class.create.call_args[0][0]
        assert call_args["service.name"] == "test-service"
        assert call_args["deployment.environment"] == "production"

    @patch("opentelemetry.sdk.resources.Resource")
    def test_create_resource_with_all_parameters(self, mock_resource_class: Mock) -> None:
        """Test creating resource with all parameters."""
        mock_resource = Mock()
        mock_resource_class.create.return_value = mock_resource

        additional = {"team": "platform", "region": "us-west-2"}

        result = create_otlp_resource(
            "comprehensive-service",
            service_version="2.0.0",
            environment="staging",
            additional_attrs=additional,
        )

        assert result == mock_resource
        call_args = mock_resource_class.create.call_args[0][0]
        assert call_args["service.name"] == "comprehensive-service"
        assert call_args["service.version"] == "2.0.0"
        assert call_args["deployment.environment"] == "staging"
        assert call_args["team"] == "platform"
        assert call_args["region"] == "us-west-2"

    def test_create_resource_without_sdk(self) -> None:
        """Test that None is returned when OpenTelemetry SDK is not available."""
        import sys

        # Save the original module
        original_module = sys.modules.get("opentelemetry.sdk.resources")

        try:
            # Remove the module to simulate it not being installed
            if "opentelemetry.sdk.resources" in sys.modules:
                del sys.modules["opentelemetry.sdk.resources"]

            # Make the import fail by removing from sys.modules and preventing reimport
            sys.modules["opentelemetry.sdk.resources"] = None  # type: ignore[assignment]

            # Now when create_otlp_resource tries to import, it will fail
            result = create_otlp_resource("test-service")
            assert result is None

        finally:
            # Restore the original module if it existed
            if original_module is not None:
                sys.modules["opentelemetry.sdk.resources"] = original_module
            elif "opentelemetry.sdk.resources" in sys.modules:
                del sys.modules["opentelemetry.sdk.resources"]

    @patch("opentelemetry.sdk.resources.Resource")
    def test_create_resource_calls_build_attributes(self, mock_resource_class: Mock) -> None:
        """Test that create_otlp_resource uses build_resource_attributes."""
        mock_resource = Mock()
        mock_resource_class.create.return_value = mock_resource

        # We can verify by checking the attributes passed to Resource.create
        create_otlp_resource(
            "test-service",
            service_version="1.0.0",
            environment="dev",
        )

        call_args = mock_resource_class.create.call_args[0][0]

        # These are the exact attributes that build_resource_attributes would create
        assert call_args["service.name"] == "test-service"
        assert call_args["service.version"] == "1.0.0"
        assert call_args["deployment.environment"] == "dev"

    @patch("opentelemetry.sdk.resources.Resource")
    def test_create_resource_with_complex_additional_attrs(self, mock_resource_class: Mock) -> None:
        """Test creating resource with complex additional attributes."""
        mock_resource = Mock()
        mock_resource_class.create.return_value = mock_resource

        additional = {
            "host.name": "server-01",
            "host.type": "physical",
            "service.namespace": "backend",
            "custom.metric.count": 100,
        }

        result = create_otlp_resource(
            "test-service",
            additional_attrs=additional,
        )

        assert result == mock_resource
        call_args = mock_resource_class.create.call_args[0][0]
        assert call_args["host.name"] == "server-01"
        assert call_args["host.type"] == "physical"
        assert call_args["service.namespace"] == "backend"
        assert call_args["custom.metric.count"] == 100


class TestIntegration:
    """Integration tests for resource creation workflow."""

    @patch("opentelemetry.sdk.resources.Resource")
    def test_full_resource_creation_workflow(self, mock_resource_class: Mock) -> None:
        """Test complete workflow from attributes to resource creation."""
        mock_resource = Mock()
        mock_resource.attributes = {}
        mock_resource_class.create.return_value = mock_resource

        # Create resource with typical production configuration
        additional = {
            "deployment.region": "us-east-1",
            "deployment.zone": "us-east-1a",
            "team": "platform",
        }

        resource = create_otlp_resource(
            service_name="api-gateway",
            service_version="3.2.1",
            environment="production",
            additional_attrs=additional,
        )

        # Verify resource was created
        assert resource is not None
        assert resource == mock_resource

        # Verify all attributes were passed correctly
        call_args = mock_resource_class.create.call_args[0][0]
        assert call_args["service.name"] == "api-gateway"
        assert call_args["service.version"] == "3.2.1"
        assert call_args["deployment.environment"] == "production"
        assert call_args["deployment.region"] == "us-east-1"
        assert call_args["deployment.zone"] == "us-east-1a"
        assert call_args["team"] == "platform"

    def test_attribute_building_workflow(self) -> None:
        """Test attribute building for various scenarios."""
        # Development environment
        dev_attrs = build_resource_attributes(
            "dev-service",
            service_version="0.1.0-dev",
            environment="development",
        )
        assert dev_attrs["deployment.environment"] == "development"

        # Production environment with additional metadata
        prod_attrs = build_resource_attributes(
            "prod-service",
            service_version="1.0.0",
            environment="production",
            additional_attrs={
                "team": "backend",
                "cost.center": "engineering",
            },
        )
        assert prod_attrs["deployment.environment"] == "production"
        assert prod_attrs["team"] == "backend"

        # Minimal configuration
        minimal_attrs = build_resource_attributes("minimal-service")
        assert len(minimal_attrs) == 1
        assert minimal_attrs["service.name"] == "minimal-service"


# 🧱🏗️🔚
