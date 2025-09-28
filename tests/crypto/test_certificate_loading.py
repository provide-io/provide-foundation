# pyvider/rpcplugin/tests/crypto/test_certificate_loading.py

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.crypto import Certificate, CertificateError

# Fixtures will be available via tests.fixtures through conftest.py
# from tests.fixtures.crypto import client_cert, temporary_cert_file, valid_cert_pem, temporary_key_file, invalid_cert_pem, malformed_cert_pem, empty_cert


class TestCertificateLoading(FoundationTestCase):
    """Test certificate loading functionality."""

    @pytest.mark.asyncio
    async def test_load_invalid_pem(self) -> None:
        with pytest.raises(CertificateError):
            Certificate(cert_pem_or_uri="INVALID DATA", key_pem_or_uri="INVALID DATA")

    @pytest.mark.asyncio
    async def test_load_pem_certificate(self, client_cert: Any) -> None:
        """Ensure a valid PEM certificate loads correctly."""
        assert client_cert.subject, "Certificate subject should not be empty"
        assert client_cert.issuer, "Certificate issuer should not be empty"

    @pytest.mark.asyncio
    async def test_load_pem_private_key(self, client_cert: Any) -> None:
        """Ensure a valid PEM private key loads correctly."""
        assert client_cert.public_key, "Certificate should have a valid public key"

    @pytest.mark.asyncio
    async def test_load_certificate_from_file(self, temporary_cert_file: Any) -> None:
        """Ensure a certificate loads correctly from a file:// path."""
        cert = Certificate(cert_pem_or_uri=temporary_cert_file)
        assert cert.subject, "Certificate subject should not be empty"

    @pytest.mark.asyncio
    async def test_load_key_value_error(self, valid_cert_pem: Any) -> None:
        """Test ValueError in private key loading."""
        with (
            mock.patch(
                "cryptography.hazmat.primitives.serialization.load_pem_private_key",
                side_effect=ValueError("Invalid key format"),
            ),
            pytest.raises(CertificateError, match="Failed to initialize certificate"),
        ):
            Certificate(
                cert_pem_or_uri=valid_cert_pem,
                key_pem_or_uri="-----BEGIN PRIVATE KEY-----\nINVALID\n-----END PRIVATE KEY-----",
            )

    @pytest.mark.asyncio
    async def test_load_key_type_error(
        self,
        valid_cert_pem: Any,
    ) -> None:  # Added valid_cert_pem fixture
        """Test TypeError in private key loading."""
        with (
            mock.patch(
                "cryptography.hazmat.primitives.serialization.load_pem_private_key",
                side_effect=TypeError("Password required"),
            ),
            pytest.raises(CertificateError, match="Failed to initialize certificate"),
        ):
            Certificate(cert_pem_or_uri=valid_cert_pem, key_pem_or_uri="SOME_KEY")

    @pytest.mark.asyncio
    async def test_load_cert_with_windows_line_endings(self, client_cert: Any) -> None:
        """Ensure certificate loading works with Windows-style line endings."""
        # Use the actual certificate content from the fixture
        cert_pem = client_cert.cert.replace("\n", "\r\n")
        cert = Certificate(cert_pem_or_uri=cert_pem)
        assert cert.subject, "Windows line endings should not break parsing"

    @pytest.mark.asyncio
    async def test_load_private_key_from_file(self, temporary_key_file: Any, client_cert: Any) -> None:
        """Ensure a private key loads correctly from a file:// path."""
        # Create cert from the fixture's actual certificate
        cert = Certificate(
            cert_pem_or_uri=client_cert.cert,
            key_pem_or_uri=temporary_key_file,
        )
        assert cert.public_key, "Certificate should have a valid private key"

    @pytest.mark.asyncio
    async def test_invalid_certificate_raises_error(self, invalid_cert_pem: Any) -> None:
        """Ensure an invalid PEM certificate raises CertificateError."""
        with pytest.raises(CertificateError):
            Certificate(cert_pem_or_uri=invalid_cert_pem)

    @pytest.mark.asyncio
    async def test_load_cert_with_malformed_pem(self, malformed_cert_pem: Any) -> None:
        """Test loading certificate with malformed PEM format."""
        with pytest.raises(CertificateError, match="Failed to initialize certificate"):
            Certificate(cert_pem_or_uri=malformed_cert_pem)

    @pytest.mark.asyncio
    async def test_malformed_certificate_raises_error(self, malformed_cert_pem: Any) -> None:
        """Ensure a malformed PEM certificate raises CertificateError."""
        with pytest.raises(CertificateError):
            Certificate(cert_pem_or_uri=malformed_cert_pem)

    @pytest.mark.asyncio
    async def test_empty_certificate_raises_error(self, empty_cert: Any) -> None:
        """Ensure an empty certificate raises CertificateError."""
        with pytest.raises(CertificateError):
            Certificate(cert_pem_or_uri=empty_cert)

    @pytest.mark.asyncio
    async def test_missing_certificate_file_raises_error(self) -> None:
        """Ensure a missing certificate file raises CertificateError."""
        with pytest.raises(CertificateError):
            Certificate(cert_pem_or_uri="file:///nonexistent/path/cert.pem")

    @pytest.mark.asyncio
    async def test_load_cert_with_utf8_bom(
        self,
        client_cert: Any,
    ) -> None:  # Added client_cert fixture
        """Ensure certificate loading works with UTF-8 BOM characters."""
        cert_with_bom = "\ufeff" + client_cert.cert  # Correctly use the cert string from the fixture
        cert = Certificate(cert_pem_or_uri=cert_with_bom)  # Use the modified string
        assert cert.subject, "UTF-8 BOM should not break certificate parsing"

    @pytest.mark.asyncio
    async def test_malformed_certificate_loading(self) -> None:
        """Ensure malformed certificates raise CertificateError."""
        with pytest.raises(CertificateError, match="Failed to initialize certificate"):
            Certificate(
                cert_pem_or_uri="-----BEGIN CERTIFICATE-----\nINVALID\n-----END CERTIFICATE-----",
            )

    @pytest.mark.asyncio
    async def test_load_cert_with_extra_whitespace(self, client_cert: Any) -> None:
        """Ensure certificate loading is robust against extra whitespace."""
        # Use cert.cert instead of cert directly
        cert_pem = f"\n\n{client_cert.cert}\n\n"
        cert = Certificate(cert_pem_or_uri=cert_pem)
        assert cert.subject, "Whitespace should not affect certificate loading"


### 🐍🏗🧪️


# 🐍🔌🧪🪄
