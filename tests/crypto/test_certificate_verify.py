#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest

# Removed: import sys
# Removed: from cryptography.hazmat.primitives.asymmetric import ec
# Removed: from cryptography.exceptions import InvalidSignature
from provide.foundation.crypto import (
    Certificate,
    CertificateBase,
    CertificateConfig,
    CertificateError,
    KeyType,
)

# Fixtures will be available via tests.fixtures through conftest.py
# from tests.fixtures.crypto import client_cert, server_cert


class TestCertificateVerify(FoundationTestCase):
    """Test certificate verification functionality."""

    @pytest.mark.asyncio
    async def test_verify_single_certificate_in_trust_chain(
        self,
        client_cert: Any,
        server_cert: Any,
    ) -> None:
        """Test basic trust chain verification with a single certificate."""
        # Add server cert to client's trust chain
        client_cert.trust_chain = [server_cert]
        assert client_cert.verify_trust(server_cert)

    @pytest.mark.asyncio
    async def test_verify_certificate_not_in_trust_chain(self, client_cert: Any, server_cert: Any) -> None:
        """Test verification fails when certificate is not in trust chain."""
        # Ensure empty trust chain
        client_cert.trust_chain = []
        assert not client_cert.verify_trust(server_cert)

    @pytest.mark.asyncio
    async def test_verify_certificate_chain_error(self, client_cert: Any, server_cert: Any) -> None:
        """Ensure verification fails for an untrusted certificate."""
        assert not client_cert.verify_trust(server_cert), "Expected verification to fail"

    @pytest.mark.asyncio
    async def test_verify_trust_chain_ordering(self, client_cert: Any, server_cert: Any) -> None:
        """Test trust chain verification is directional - A trusting B doesn't mean B trusts A."""
        # Set up one-way trust: client trusts server
        client_cert.trust_chain = [server_cert]
        server_cert.trust_chain = []

        # Client should be able to verify server
        assert client_cert.verify_trust(server_cert), (
            "Client should verify server when server is in client's trust chain"
        )

        # But server should not verify client
        assert not server_cert.verify_trust(client_cert), (
            "Server should not verify client when client is not in server's trust chain"
        )

    @pytest.mark.asyncio
    async def test_verify_bidirectional_trust_chain(self, client_cert: Any, server_cert: Any) -> None:
        """Test certificates can be configured to trust each other."""
        # Set up two-way trust
        client_cert.trust_chain = [server_cert]
        server_cert.trust_chain = [client_cert]

        # Both should verify each other
        assert client_cert.verify_trust(server_cert), "Client should verify server"
        assert server_cert.verify_trust(client_cert), "Server should verify client"

    @pytest.mark.asyncio
    async def test_verify_empty_trust_chain(self, client_cert: Any, server_cert: Any) -> None:
        """Test verification with empty trust chain."""
        client_cert.trust_chain = []
        server_cert.trust_chain = []
        assert not client_cert.verify_trust(server_cert)
        assert not server_cert.verify_trust(client_cert)

    @pytest.mark.asyncio
    async def test_verify_self_trust_chain(self, client_cert: Any) -> None:
        """Test certificate can verify itself if in its own trust chain."""
        # Add cert to its own trust chain
        client_cert.trust_chain = [client_cert]
        assert client_cert.verify_trust(client_cert)

    @pytest.mark.asyncio
    async def test_verify_mutual_trust_chain(self, client_cert: Any, server_cert: Any) -> None:
        """Test mutual trust chain verification."""
        # Set up mutual trust
        client_cert.trust_chain = [server_cert]
        server_cert.trust_chain = [client_cert]

        # Both should verify against each other
        assert client_cert.verify_trust(server_cert)
        assert server_cert.verify_trust(client_cert)

    @pytest.mark.asyncio
    async def test_verify_trust_chain_after_modification(self, client_cert: Any, server_cert: Any) -> None:
        """Test trust chain verification after modifying the chain."""
        # Start with no trust
        client_cert.trust_chain = []
        assert not client_cert.verify_trust(server_cert)

        # Add trust
        client_cert.trust_chain.append(server_cert)
        assert client_cert.verify_trust(server_cert)

        # Remove trust
        client_cert.trust_chain.clear()
        assert not client_cert.verify_trust(server_cert)

    @pytest.mark.asyncio
    async def test_verify_multiple_certificates_in_trust_chain(
        self,
        client_cert: Any,
        server_cert: Any,
    ) -> None:
        """Test verification with multiple certificates in trust chain."""
        # Create a trust chain with both certs
        client_cert.trust_chain = [client_cert, server_cert]

        # Should verify against any cert in the chain
        assert client_cert.verify_trust(client_cert)
        assert client_cert.verify_trust(server_cert)

    @pytest.mark.asyncio
    async def test_verify_subject_issuer_relationship(self, client_cert: Any, server_cert: Any) -> None:
        """Test verification considers subject/issuer relationship."""
        # Document the relationship
        is_self_signed_server = server_cert.subject == server_cert.issuer

        # Add to trust chain
        client_cert.trust_chain = [server_cert]

        # Verify behavior matches self-signed status
        result = client_cert.verify_trust(server_cert)
        assert result == (is_self_signed_server and server_cert in client_cert.trust_chain)

    @pytest.mark.asyncio
    async def test_verify_public_key_types(self, client_cert: Any, server_cert: Any) -> None:
        """Test verification with different public key types."""
        # Document the key types
        client_key_type = type(client_cert.public_key)
        server_key_type = type(server_cert.public_key)

        # Add to trust chain
        client_cert.trust_chain = [server_cert]
        result = client_cert.verify_trust(server_cert)

        # Log the key types used
        print(f"Client key type: {client_key_type}")
        print(f"Server key type: {server_key_type}")

        # Key type shouldn't prevent verification if in trust chain
        assert result, "Verification should succeed regardless of key type if in trust chain"

    @pytest.mark.asyncio
    async def test_verify_self_signed_rsa(self) -> None:
        """Test verification of RSA self-signed certificate."""
        cert = Certificate.generate(key_type="rsa")
        cert.trust_chain = [cert]
        assert cert.verify_trust(cert)

    @pytest.mark.asyncio
    async def test_verify_self_signed_ec(self) -> None:
        """Test verification of EC self-signed certificate."""
        cert = Certificate.generate(key_type="ecdsa")
        cert.trust_chain = [cert]
        assert cert.verify_trust(cert)

    @pytest.mark.asyncio
    async def test_verify_unsupported_key_type(self) -> None:
        """Test verification with unsupported key type."""
        cert = Certificate.generate()

        # Create a new mock certificate for verification
        mock_cert = MagicMock()
        mock_cert._cert = MagicMock()
        mock_cert.public_key = None  # Force unsupported key type

        with pytest.raises(
            CertificateError,
            match="Cannot verify trust: Other certificate has no public key",
        ):
            cert.verify_trust(mock_cert)

    @pytest.mark.asyncio
    async def test_self_signed_certificate_verification(self) -> None:
        """Ensure self-signed certificates are properly recognized and verify themselves."""
        cert = Certificate.generate(key_type="rsa")

        assert cert.subject == cert.issuer, "Certificate should be self-signed"

        cert.trust_chain.append(cert)  # Explicitly add to trust chain
        assert cert.verify_trust(cert), "Self-signed cert should verify itself when in its own trust chain"

    @pytest.mark.asyncio
    async def test_corrupt_certificate(self) -> None:
        """Ensure corrupted certificates raise errors."""
        with pytest.raises(CertificateError):
            Certificate.from_pem(
                cert_pem="-----BEGIN CERTIFICATE-----\nINVALID DATA\n-----END CERTIFICATE-----",
            )

    @pytest.mark.asyncio
    async def test_verify_invalid_public_key(self) -> None:
        """Ensure verification fails when public key is None."""
        cert = Certificate.generate()
        with pytest.raises(CertificateError, match="Cannot verify trust"):
            cert.verify_trust(None)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_certificate_naive_datetime(self) -> None:
        """Ensure naive datetime is converted to UTC."""
        naive_time = datetime.now()  # No tzinfo
        config = CertificateConfig(
            common_name="test",
            organization="test",
            alt_names=["localhost"],
            key_type=KeyType.RSA,
            not_valid_before=naive_time,
            not_valid_after=naive_time + timedelta(days=365),
        )
        base, _ = CertificateBase.create(config)
        assert base.not_valid_before.tzinfo is UTC
        assert base.not_valid_after.tzinfo is UTC

    @pytest.mark.asyncio
    async def test_certificate_mismatched_issuer(self) -> None:
        cert1 = Certificate.generate(key_type="rsa", common_name="Cert1")
        cert2 = Certificate.generate(key_type="rsa", common_name="Cert2")
        cert1.trust_chain = []
        assert not cert1.verify_trust(cert2), "Expected verification to fail due to mismatched issuer"

    # @pytest.mark.xfail( # Intentionally keeping this xfail for now to see current behavior
    #     reason="Persistently difficult to mock EllipticCurvePublicKey.verify to test exception handling in _validate_signature"
    # )
    @pytest.mark.asyncio
    async def test_certificate_self_signature_validation(self) -> None:
        """Ensure a generated self-signed certificate's signature is valid."""
        cert = Certificate.generate(
            key_type="ecdsa",
            ecdsa_curve="secp384r1",
        )  # Using a common type

        # A freshly generated self-signed certificate should have a valid signature
        # when verified against its own public key.
        is_actually_valid = cert._validate_signature(signed_cert=cert, signing_cert=cert)

        # If this assertion fails, it means _validate_signature is incorrectly
        # reporting a valid self-signed signature as invalid.
        assert is_actually_valid, (
            "Self-signed certificate signature should be valid, but _validate_signature returned False."
        )

    @pytest.mark.asyncio
    async def test_certificate_key_usage_extension_failure(self) -> None:
        """Ensure Key Usage extension failure raises CertificateError."""
        cert = Certificate.generate()

        with (
            patch(
                "cryptography.x509.CertificateBuilder.add_extension",
                side_effect=Exception("Mock failure"),
            ),
            pytest.raises(CertificateError, match="Failed to create"),
        ):
            cert._create_x509_certificate()

    @pytest.mark.asyncio
    async def test_certificate_equality(self) -> None:
        """Ensure certificates are equal only if subject and serial number match."""
        cert1 = Certificate.generate()
        cert2 = Certificate.generate()

        assert cert1 != cert2, "Different certificates should not be equal"

        # Force serial number and subject to be identical
        cert2._base = cert1._base
        assert cert1 == cert2, "Certificates with identical serial and subject should be equal"


# 🧱🏗️🔚
