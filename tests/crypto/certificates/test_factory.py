#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for certificate factory functions.

Run with: pytest tests/crypto/certificates/test_factory.py -v"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.crypto.certificates.base import CertificateError
from provide.foundation.crypto.certificates.factory import (
    create_ca,
    create_ca_certificate,
    create_self_signed,
    create_self_signed_client_cert,
    create_self_signed_server_cert,
    create_signed_certificate,
)


class TestCreateCACertificate(FoundationTestCase):
    """Tests for create_ca_certificate function."""

    def test_create_ca_certificate_success(self) -> None:
        """Test successful CA certificate creation."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
        )

        assert ca_cert is not None
        assert ca_cert.is_ca is True
        assert "Test CA" in ca_cert.subject
        assert "Test Org" in ca_cert.subject

    def test_create_ca_certificate_with_rsa(self) -> None:
        """Test CA creation with RSA key type."""
        ca_cert = create_ca_certificate(
            common_name="RSA CA",
            organization_name="Test Org",
            validity_days=365,
            key_type="rsa",
            key_size=2048,
        )

        assert ca_cert is not None
        assert ca_cert.is_ca is True

    def test_create_ca_certificate_with_ecdsa(self) -> None:
        """Test CA creation with ECDSA key type."""
        ca_cert = create_ca_certificate(
            common_name="ECDSA CA",
            organization_name="Test Org",
            validity_days=365,
            key_type="ecdsa",
            ecdsa_curve="secp256r1",
        )

        assert ca_cert is not None
        assert ca_cert.is_ca is True

    def test_create_ca_certificate_alt_names(self) -> None:
        """Test CA certificate includes common name in alt names."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
        )

        assert "Test CA" in ca_cert.alt_names


class TestCreateSignedCertificate(FoundationTestCase):
    """Tests for create_signed_certificate function."""

    def test_create_signed_certificate_success(self) -> None:
        """Test successful signed certificate creation."""
        # First create a CA
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
        )

        # Create a signed certificate
        signed_cert = create_signed_certificate(
            ca_certificate=ca_cert,
            common_name="test.example.com",
            organization_name="Test Org",
            validity_days=90,
        )

        assert signed_cert is not None
        assert signed_cert.is_ca is False
        assert "test.example.com" in signed_cert.subject

    def test_create_signed_certificate_with_alt_names(self) -> None:
        """Test signed certificate with alternative names."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
        )

        signed_cert = create_signed_certificate(
            ca_certificate=ca_cert,
            common_name="test.example.com",
            organization_name="Test Org",
            validity_days=90,
            alt_names=["test.example.com", "www.example.com", "api.example.com"],
        )

        assert "test.example.com" in signed_cert.alt_names
        assert "www.example.com" in signed_cert.alt_names
        assert "api.example.com" in signed_cert.alt_names

    def test_create_signed_certificate_client_cert(self) -> None:
        """Test signed client certificate creation."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
        )

        client_cert = create_signed_certificate(
            ca_certificate=ca_cert,
            common_name="client@example.com",
            organization_name="Test Org",
            validity_days=90,
            is_client_cert=True,
        )

        assert client_cert is not None
        assert client_cert.is_ca is False

    def test_create_signed_certificate_no_private_key(self) -> None:
        """Test error when CA has no private key."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
        )
        # Remove private key to simulate missing key
        ca_cert._private_key = None

        with pytest.raises(CertificateError, match="private key is not available"):
            create_signed_certificate(
                ca_certificate=ca_cert,
                common_name="test.example.com",
                organization_name="Test Org",
                validity_days=90,
            )

    def test_create_signed_certificate_with_non_ca(self) -> None:
        """Test warning when signing cert is not marked as CA."""
        # Create a regular cert (not a CA)
        server_cert = create_self_signed_server_cert(
            common_name="server.example.com",
            organization_name="Test Org",
            validity_days=365,
        )

        # Should log warning but still create cert
        signed_cert = create_signed_certificate(
            ca_certificate=server_cert,
            common_name="test.example.com",
            organization_name="Test Org",
            validity_days=90,
        )

        assert signed_cert is not None

    def test_create_signed_certificate_with_rsa(self) -> None:
        """Test signed certificate with RSA key."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
            key_type="rsa",
        )

        signed_cert = create_signed_certificate(
            ca_certificate=ca_cert,
            common_name="test.example.com",
            organization_name="Test Org",
            validity_days=90,
            key_type="rsa",
            key_size=2048,
        )

        assert signed_cert is not None

    def test_create_signed_certificate_with_ecdsa(self) -> None:
        """Test signed certificate with ECDSA key."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
            key_type="ecdsa",
        )

        signed_cert = create_signed_certificate(
            ca_certificate=ca_cert,
            common_name="test.example.com",
            organization_name="Test Org",
            validity_days=90,
            key_type="ecdsa",
            ecdsa_curve="secp256r1",
        )

        assert signed_cert is not None


class TestCreateSelfSignedServerCert(FoundationTestCase):
    """Tests for create_self_signed_server_cert function."""

    def test_create_self_signed_server_cert_success(self) -> None:
        """Test successful self-signed server certificate creation."""
        server_cert = create_self_signed_server_cert(
            common_name="server.example.com",
            organization_name="Test Org",
            validity_days=365,
        )

        assert server_cert is not None
        assert server_cert.is_ca is False
        assert "server.example.com" in server_cert.subject

    def test_create_self_signed_server_cert_with_alt_names(self) -> None:
        """Test server cert with alternative names."""
        server_cert = create_self_signed_server_cert(
            common_name="server.example.com",
            organization_name="Test Org",
            validity_days=365,
            alt_names=["server.example.com", "*.example.com"],
        )

        assert "server.example.com" in server_cert.alt_names
        assert "*.example.com" in server_cert.alt_names

    def test_create_self_signed_server_cert_with_rsa(self) -> None:
        """Test server cert with RSA key."""
        server_cert = create_self_signed_server_cert(
            common_name="server.example.com",
            organization_name="Test Org",
            validity_days=365,
            key_type="rsa",
            key_size=2048,
        )

        assert server_cert is not None

    def test_create_self_signed_server_cert_with_ecdsa(self) -> None:
        """Test server cert with ECDSA key."""
        server_cert = create_self_signed_server_cert(
            common_name="server.example.com",
            organization_name="Test Org",
            validity_days=365,
            key_type="ecdsa",
            ecdsa_curve="secp384r1",
        )

        assert server_cert is not None


class TestCreateSelfSignedClientCert(FoundationTestCase):
    """Tests for create_self_signed_client_cert function."""

    def test_create_self_signed_client_cert_success(self) -> None:
        """Test successful self-signed client certificate creation."""
        client_cert = create_self_signed_client_cert(
            common_name="client@example.com",
            organization_name="Test Org",
            validity_days=365,
        )

        assert client_cert is not None
        assert client_cert.is_ca is False
        assert "client@example.com" in client_cert.subject

    def test_create_self_signed_client_cert_with_alt_names(self) -> None:
        """Test client cert with alternative names."""
        client_cert = create_self_signed_client_cert(
            common_name="client@example.com",
            organization_name="Test Org",
            validity_days=365,
            alt_names=["client@example.com", "user@example.com"],
        )

        assert "client@example.com" in client_cert.alt_names
        assert "user@example.com" in client_cert.alt_names

    def test_create_self_signed_client_cert_with_rsa(self) -> None:
        """Test client cert with RSA key."""
        client_cert = create_self_signed_client_cert(
            common_name="client@example.com",
            organization_name="Test Org",
            validity_days=365,
            key_type="rsa",
            key_size=2048,
        )

        assert client_cert is not None

    def test_create_self_signed_client_cert_with_ecdsa(self) -> None:
        """Test client cert with ECDSA key."""
        client_cert = create_self_signed_client_cert(
            common_name="client@example.com",
            organization_name="Test Org",
            validity_days=365,
            key_type="ecdsa",
            ecdsa_curve="secp256r1",
        )

        assert client_cert is not None


class TestConvenienceFunctions(FoundationTestCase):
    """Tests for convenience functions."""

    def test_create_self_signed_default_params(self) -> None:
        """Test create_self_signed with default parameters."""
        cert = create_self_signed()

        assert cert is not None
        assert "localhost" in cert.subject

    def test_create_self_signed_with_custom_params(self) -> None:
        """Test create_self_signed with custom parameters."""
        cert = create_self_signed(
            common_name="test.example.com",
            organization="Test Organization",
            validity_days=180,
            key_type="ecdsa",
        )

        assert cert is not None
        assert "test.example.com" in cert.subject
        assert "Test Organization" in cert.subject

    def test_create_self_signed_with_alt_names(self) -> None:
        """Test create_self_signed with alternative names."""
        cert = create_self_signed(
            common_name="test.example.com",
            alt_names=["test.example.com", "*.test.example.com"],
        )

        assert "test.example.com" in cert.alt_names
        assert "*.test.example.com" in cert.alt_names

    def test_create_ca_default_params(self) -> None:
        """Test create_ca with minimal parameters."""
        ca_cert = create_ca(common_name="Test CA")

        assert ca_cert is not None
        assert ca_cert.is_ca is True
        assert "Test CA" in ca_cert.subject

    def test_create_ca_with_custom_params(self) -> None:
        """Test create_ca with custom parameters."""
        ca_cert = create_ca(
            common_name="Custom CA",
            organization="Custom Org",
            validity_days=730,
            key_type="ecdsa",
        )

        assert ca_cert is not None
        assert ca_cert.is_ca is True
        assert "Custom CA" in ca_cert.subject
        assert "Custom Org" in ca_cert.subject


class TestFactoryLogging(FoundationTestCase):
    """Tests for factory logging."""

    def test_create_ca_logs_creation(self) -> None:
        """Test CA creation logs appropriate messages."""
        with patch("provide.foundation.crypto.certificates.factory.logger") as mock_logger:
            create_ca_certificate(
                common_name="Test CA",
                organization_name="Test Org",
                validity_days=365,
            )

            # Verify logging calls
            assert mock_logger.info.called
            call_args = [str(call) for call in mock_logger.info.call_args_list]
            assert any("Creating new CA certificate" in str(arg) for arg in call_args)

    def test_create_signed_certificate_logs_creation(self) -> None:
        """Test signed certificate creation logs messages."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
        )

        with patch("provide.foundation.crypto.certificates.factory.logger") as mock_logger:
            create_signed_certificate(
                ca_certificate=ca_cert,
                common_name="test.example.com",
                organization_name="Test Org",
                validity_days=90,
            )

            # Verify logging calls
            assert mock_logger.info.called

    def test_create_server_cert_logs_creation(self) -> None:
        """Test server cert creation logs messages."""
        with patch("provide.foundation.crypto.certificates.factory.logger") as mock_logger:
            create_self_signed_server_cert(
                common_name="server.example.com",
                organization_name="Test Org",
                validity_days=365,
            )

            assert mock_logger.info.called

    def test_create_client_cert_logs_creation(self) -> None:
        """Test client cert creation logs messages."""
        with patch("provide.foundation.crypto.certificates.factory.logger") as mock_logger:
            create_self_signed_client_cert(
                common_name="client@example.com",
                organization_name="Test Org",
                validity_days=365,
            )

            assert mock_logger.info.called


class TestFactoryEdgeCases(FoundationTestCase):
    """Tests for edge cases in factory functions."""

    def test_create_ca_with_minimal_validity(self) -> None:
        """Test CA creation with short validity period."""
        ca_cert = create_ca_certificate(
            common_name="Short-lived CA",
            organization_name="Test Org",
            validity_days=1,
        )

        assert ca_cert is not None

    def test_create_signed_certificate_with_long_common_name(self) -> None:
        """Test signed certificate with long common name (within X.509 limits)."""
        ca_cert = create_ca_certificate(
            common_name="Test CA",
            organization_name="Test Org",
            validity_days=365,
        )

        # Use a long but valid common name (under 64 char limit)
        long_cn = "very-long-subdomain-name.example.com"  # 37 chars, under 64 limit
        signed_cert = create_signed_certificate(
            ca_certificate=ca_cert,
            common_name=long_cn,
            organization_name="Test Org",
            validity_days=90,
        )

        assert signed_cert is not None
        assert long_cn in signed_cert.subject

    def test_create_self_signed_with_wildcard(self) -> None:
        """Test self-signed cert with wildcard domain."""
        cert = create_self_signed(
            common_name="*.example.com",
            alt_names=["*.example.com", "example.com"],
        )

        assert cert is not None
        assert "*.example.com" in cert.alt_names


__all__ = [
    "TestConvenienceFunctions",
    "TestCreateCACertificate",
    "TestCreateSelfSignedClientCert",
    "TestCreateSelfSignedServerCert",
    "TestCreateSignedCertificate",
    "TestFactoryEdgeCases",
    "TestFactoryLogging",
]

# 🧱🏗️🔚
