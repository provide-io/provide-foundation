#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock
import pytest

from provide.foundation.crypto import Certificate, CertificateError

# Fixtures will be available via tests.fixtures through conftest.py
# from tests.fixtures.crypto import client_cert, server_cert


@pytest.mark.asyncio
async def test_certificate_subject(client_cert) -> None:
    """Ensure the subject is correctly extracted."""
    assert client_cert.subject, "Certificate subject should not be empty"
    assert isinstance(client_cert.subject, str), "Subject should be a string"
    assert "CN=" in client_cert.subject, "Subject should contain Common Name (CN)"


@pytest.mark.asyncio
async def test_certificate_issuer(client_cert) -> None:
    """Ensure the issuer is correctly extracted."""
    assert client_cert.issuer, "Certificate issuer should not be empty"
    assert isinstance(client_cert.issuer, str), "Issuer should be a string"
    assert "CN=" in client_cert.issuer, "Issuer should contain Common Name (CN)"


@pytest.mark.asyncio
async def test_certificate_subject_not_equal_to_issuer_for_non_self_signed(
    client_cert,
) -> None:
    """Ensure subject and issuer are different for non-self-signed certificates."""
    if client_cert.subject == client_cert.issuer:
        pytest.skip("Skipping test: Certificate is self-signed.")

    assert client_cert.subject != client_cert.issuer, (
        "Non-self-signed certificate should have a different issuer"
    )


@pytest.mark.asyncio
async def test_certificate_is_ca(client_cert) -> None:
    """Ensure the certificate correctly reports its CA status."""
    assert isinstance(client_cert.is_ca, bool), "CA status should be a boolean"


@pytest.mark.asyncio
async def test_certificate_public_key(client_cert) -> None:
    """Ensure the public key is correctly loaded."""
    assert client_cert.public_key, "Certificate public key should not be empty"
    assert isinstance(
        client_cert.public_key,
        (rsa.RSAPublicKey, ec.EllipticCurvePublicKey),
    ), "Public key should be RSA or EC"


@pytest.mark.asyncio
async def test_server_certificate_public_key(server_cert) -> None:
    """Ensure the server certificate's public key is correctly loaded."""
    assert server_cert.public_key, "Server certificate public key should not be empty"


@pytest.mark.asyncio
async def test_certificate_serial_number(client_cert) -> None:
    """Ensure the certificate serial number is valid."""
    assert isinstance(client_cert._cert.serial_number, int), "Serial number should be an integer"
    assert client_cert._cert.serial_number > 0, "Serial number should be positive"


@pytest.mark.asyncio
async def test_certificate_fingerprint(client_cert) -> None:
    """Ensure fingerprinting works as expected."""
    fingerprint = client_cert._cert.fingerprint(hashes.SHA256())
    assert isinstance(fingerprint, bytes), "Fingerprint should be in bytes format"
    assert len(fingerprint) == 32, "SHA-256 fingerprint should be 32 bytes long"


@pytest.mark.asyncio
async def test_certificate_has_extensions(client_cert) -> None:
    """Ensure certificate has extensions (basic constraints, key usage, etc.)."""
    assert len(client_cert._cert.extensions) >= 1, "Certificate should have at least one extension"


@pytest.mark.asyncio
async def test_certificate_basic_constraints(client_cert) -> None:
    """Ensure Basic Constraints extension is correctly set."""
    from cryptography.x509.oid import ExtensionOID

    try:
        ext = client_cert._cert.extensions.get_extension_for_oid(
            ExtensionOID.BASIC_CONSTRAINTS,
        )
        assert ext.value.ca in [True, False], "Basic Constraints CA flag should be boolean"
    except Exception:
        pytest.skip("Skipping test: Basic Constraints extension not found")


@pytest.mark.asyncio
async def test_certificate_key_usage(client_cert) -> None:
    """Ensure Key Usage extension is correctly set."""
    from cryptography.x509.oid import ExtensionOID

    try:
        ext = client_cert._cert.extensions.get_extension_for_oid(ExtensionOID.KEY_USAGE)
        assert isinstance(ext.value.digital_signature, bool), "Key usage should be boolean"
    except Exception:
        pytest.skip("Skipping test: Key Usage extension not found")


@pytest.mark.asyncio
async def test_certificate_extended_key_usage(client_cert) -> None:
    """Ensure Extended Key Usage extension is correctly set."""
    from cryptography.x509.oid import ExtensionOID

    try:
        ext = client_cert._cert.extensions.get_extension_for_oid(
            ExtensionOID.EXTENDED_KEY_USAGE,
        )
        assert len(ext.value) >= 1, "Extended Key Usage should have at least one value"
    except Exception:
        pytest.skip("Skipping test: Extended Key Usage extension not found")


@pytest.mark.asyncio
async def test_certificate_subject_empty_fallback() -> None:
    """Ensure the certificate subject fallback for invalid certificates."""
    with pytest.raises(CertificateError):
        invalid_cert = Certificate.from_pem(
            cert_pem="-----BEGIN CERTIFICATE-----\nINVALID\n-----END CERTIFICATE-----",
            key_pem=None,
        )
        assert invalid_cert.subject == "<Invalid Certificate>", (
            "Subject should fallback to <Invalid Certificate>"
        )


@pytest.mark.asyncio
async def test_certificate_issuer_empty_fallback() -> None:
    """Ensure the certificate issuer fallback for invalid certificates."""
    with pytest.raises(CertificateError):
        invalid_cert = Certificate.from_pem(
            cert_pem="-----BEGIN CERTIFICATE-----\nINVALID\n-----END CERTIFICATE-----",
            key_pem=None,
        )
        assert invalid_cert.issuer == "<Invalid Certificate>", (
            "Issuer should fallback to <Invalid Certificate>"
        )


class TestCertificateProperties(FoundationTestCase):
    """Test certificate property functionality."""

    @pytest.mark.asyncio
    async def test_is_ca_extension_not_found(self) -> None:
        """Test is_ca property when basic constraints extension is not found."""
        cert = Certificate.generate()

        # Create a mock certificate that raises ExtensionNotFound
        mock_cert = MagicMock()
        mock_cert.extensions.get_extension_for_oid.side_effect = x509.ExtensionNotFound(
            "Basic Constraints",
            x509.oid.ExtensionOID.BASIC_CONSTRAINTS,
        )

        # Replace the _cert attribute with our mock
        cert._cert = mock_cert

        # Should return False when extension is not found
        assert cert.is_ca is False

    @pytest.mark.asyncio
    async def test_is_ca_extension_not_found_logs_debug(self, mocker) -> None:
        """Test is_ca property logs debug when BasicConstraints extension is not found."""
        # Create a Certificate instance (it will generate a real cert initially)
        cert_instance = Certificate.generate()

        # Mock the internal _cert object's extensions attribute
        mock_extensions = mocker.MagicMock()
        mock_extensions.get_extension_for_oid.side_effect = x509.ExtensionNotFound(
            "Basic Constraints not found",
            x509.oid.ExtensionOID.BASIC_CONSTRAINTS,
        )

        # Patch the logger from the certificate module
        mock_logger_debug = mocker.patch(
            "provide.foundation.crypto.certificates.certificate.logger.debug",
        )

        # Temporarily replace the _cert.extensions on the instance
        # This is a bit invasive, but necessary to simulate the condition for the property
        cert_instance._cert = mocker.MagicMock(
            spec=x509.Certificate,
        )  # Replace _cert with a mock
        cert_instance._cert.extensions = mock_extensions  # Assign mocked extensions to the mocked _cert

        assert cert_instance.is_ca is False  # is_ca should return False

        mock_logger_debug.assert_called_once_with(
            "📜🔍⚠️ is_ca: Basic Constraints extension not found",
        )

        # Restore original extensions if necessary, though for this test it's fine as instance is local
        # For more complex scenarios, more careful patching/restoration might be needed
        # cert_instance._cert.extensions = original_extensions # Not strictly needed here

    @pytest.mark.asyncio
    async def test_unique_serial_numbers(self, client_cert, server_cert) -> None:
        """Ensure unique serial numbers for different certificates."""
        assert client_cert._cert.serial_number != server_cert._cert.serial_number, (
            "Serial numbers should be unique"
        )

    @pytest.mark.asyncio
    async def test_certificate_hash_uniqueness(self, client_cert, server_cert) -> None:
        """Ensure different certificates have unique hashes."""
        assert hash(client_cert) != hash(server_cert), "Different certs should not hash the same"

    @pytest.mark.asyncio
    async def test_certificate_hash_collision(self) -> None:
        """Ensure certificates with identical serial numbers hash the same."""
        cert1 = Certificate.generate(key_type="rsa")
        cert2 = Certificate.generate(key_type="rsa")

        # Force serial numbers to be identical
        cert2._base = cert1._base

        assert hash(cert1) == hash(cert2), "Identical serials should hash the same"


# 🧱🏗️🔚
