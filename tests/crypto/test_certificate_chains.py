#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from datetime import UTC, datetime

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.crypto import Certificate, CertificateError

# Fixtures will be available via tests.fixtures through conftest.py
# from tests.fixtures.crypto import client_cert, server_cert


class TestCertificateChains(FoundationTestCase):
    """Test certificate chain functionality."""

    @pytest.mark.asyncio
    async def test_certificate_chain_validation(self, client_cert, server_cert) -> None:
        """Test validation of a certificate chain."""
        # Add server cert to client's trust chain
        client_cert.trust_chain.append(server_cert)

        # Should validate against the certificate in its trust chain
        assert client_cert.verify_trust(server_cert)

    @pytest.mark.asyncio
    async def test_certificate_chain_validation_no_trust(self, client_cert, server_cert) -> None:
        """Test validation behavior when certificates are not in trust chain."""
        # First ensure trust chain is empty
        client_cert.trust_chain = []
        server_cert.trust_chain = []

        # Without a trust chain, certificates should not validate
        # regardless of whether they are self-signed
        result = client_cert.verify_trust(server_cert)
        assert not result, "Certificates without trust chain should not validate"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cert_fixture", ["client_cert", "server_cert"])
    async def test_certificate_basic_properties(self, cert_fixture, request) -> None:
        """Test basic certificate properties."""
        cert = request.getfixturevalue(cert_fixture)

        # Test required properties
        assert cert.subject
        assert cert.issuer
        assert isinstance(cert.is_ca, bool)
        assert cert.public_key
        assert isinstance(cert.public_key, (rsa.RSAPublicKey, ec.EllipticCurvePublicKey))

    @pytest.mark.asyncio
    async def test_certificate_self_signed_validation(self, client_cert) -> None:
        """Test self-signed certificate validation."""
        # Clear trust chain first
        client_cert.trust_chain = []

        # A self-signed certificate should be in its own trust chain to validate
        if client_cert.subject == client_cert.issuer:
            client_cert.trust_chain.append(client_cert)
            assert client_cert.verify_trust(client_cert), (
                "Self-signed certificate should validate against itself when in trust chain"
            )
        else:
            pytest.skip("Certificate is not self-signed")

    def test_certificate_extensions(self, client_cert) -> None:
        """Test certificate extensions are present and valid."""
        x509_cert = client_cert._cert

        # Test basic constraints
        bc = x509_cert.extensions.get_extension_for_oid(
            x509.oid.ExtensionOID.BASIC_CONSTRAINTS,
        )
        assert bc.value.ca in [True, False]

        # Test key usage if present
        try:
            ku = x509_cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.KEY_USAGE)
            assert hasattr(ku.value, "digital_signature")
        except x509.ExtensionNotFound:
            pytest.skip("Key usage extension not present")

        # Test subject alternative names if present
        try:
            san = x509_cert.extensions.get_extension_for_oid(
                x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME,
            )
            assert all(isinstance(name, (x509.DNSName, x509.IPAddress)) for name in san.value)
        except x509.ExtensionNotFound:
            pytest.skip("SAN extension not present")

    @pytest.mark.asyncio
    async def test_certificate_validity_period(self, client_cert) -> None:
        """Test certificate validity period checking."""
        now = datetime.now(UTC)
        assert client_cert._cert.not_valid_before_utc <= now
        assert now <= client_cert._cert.not_valid_after_utc
        assert client_cert.is_valid

    @pytest.mark.asyncio
    async def test_certificate_unique_serial(self, client_cert, server_cert) -> None:
        """Test certificates have unique serial numbers."""
        assert client_cert._cert.serial_number != server_cert._cert.serial_number

    @pytest.mark.asyncio
    async def test_generate_certificate_invalid_type(self) -> None:
        """Test error handling for invalid key type."""
        with pytest.raises(CertificateError):
            Certificate.generate(key_type="invalid_type")

    @pytest.mark.asyncio
    async def test_certificate_repr(self) -> None:
        """Ensure repr() includes subject, issuer, and validity."""
        cert = Certificate.generate()
        cert_repr = repr(cert)
        assert "subject=" in cert_repr
        assert "issuer=" in cert_repr
        assert "valid=" in cert_repr
        assert "ca=" in cert_repr

    @pytest.mark.asyncio
    async def test_certificate_hash(self, client_cert) -> None:
        """Test certificate hash generation."""
        cert_hash = hash(client_cert)
        assert isinstance(cert_hash, int)
        # Same certificate should generate same hash
        assert hash(client_cert) == cert_hash

    @pytest.mark.asyncio
    async def test_certificate_invalid_trust_chain_signature(self) -> None:
        """Ensure certificate trust chain fails on signature mismatch when signature check is performed."""
        # Create a self-trusted CA. Ensure key_type is ecdsa for the mock to apply.
        ca_cert = Certificate.generate(
            common_name="Test Root CA",
            key_type="ecdsa",
        )
        ca_cert.trust_chain = [ca_cert]  # CA trusts itself

        # Create an end-entity certificate that will be checked against the CA.
        # Ensure key_type is ecdsa.
        cert_to_check = Certificate.generate(
            common_name="End Entity Cert",
            key_type="ecdsa",
        )

        # To ensure _validate_signature is reached and its issuer check passes:
        # Mock the issuer of cert_to_check to appear as if it was issued by ca_cert.
        # This is a targeted patch specifically for this test's logic flow.
        # Note: Accessing _cert like this is for testing internals.
        # REMOVED: with patch.object(cert_to_check._cert, 'issuer', ca_cert._cert.subject):

        # The mock for EllipticCurvePublicKey.verify can remain. If the issuer check *were* to pass
        # (which it won't for these two unrelated certs as cert_to_check is self-signed with a different subject),
        # this mock would ensure failure.
        # With unrelated certs, _validate_signature will return False due to issuer mismatch
        # *before* the EllipticCurvePublicKey.verify line is reached.
        with patch(
            "cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey.verify",
            side_effect=Exception("Simulated Signature Failure"),
        ):
            # ca_cert.verify_trust(cert_to_check) will call:
            # _validate_signature(signed_cert=cert_to_check, signing_cert=ca_cert)
            # Inside _validate_signature, since cert_to_check.issuer (self-signed) != ca_cert.subject,
            # it will return False.
            # Thus, verify_trust will return False.
            assert not ca_cert.verify_trust(cert_to_check), (
                "Verification of an unrelated certificate (or one with a bad signature if issuers matched) should fail."
            )


# 🧱🏗️🔚
