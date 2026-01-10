#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from attrs import define
from provide.testkit import FoundationTestCase
import pytest

# Fixtures will be available via tests.fixtures through conftest.py
# from tests.fixtures.crypto import client_cert, server_cert


@define
class MockChannelCredentials:
    """Mock implementation of SSL channel credentials."""

    root_certificates: bytes | None
    private_key: bytes | None
    certificate_chain: bytes | None


@define
class MockServerCredentials:
    """Mock implementation of SSL server credentials."""

    private_key_certificate_chain_pairs: list[tuple[bytes, bytes]]
    root_certificates: bytes | None
    require_client_auth: bool


# Convert async functions to regular functions since they don't need to be async
def mock_ssl_channel_credentials(
    root_certificates: bytes | None = None,
    private_key: bytes | None = None,
    certificate_chain: bytes | None = None,
) -> MockChannelCredentials:
    """Mock implementation of grpc.ssl_channel_credentials."""
    return MockChannelCredentials(
        root_certificates=root_certificates,
        private_key=private_key,
        certificate_chain=certificate_chain,
    )


def mock_ssl_server_credentials(
    private_key_certificate_chain_pairs: list[tuple[bytes, bytes]],
    root_certificates: bytes | None = None,
    require_client_auth: bool = False,
) -> MockServerCredentials:
    """Mock implementation of grpc.ssl_server_credentials."""
    if require_client_auth and root_certificates is None:
        raise ValueError(
            "root_certificates is required when require_client_auth is True",
        )

    if not private_key_certificate_chain_pairs:
        raise ValueError("At least one private_key_certificate_chain_pair is required")

    # Validate all pairs have correct format
    for private_key, certificate_chain in private_key_certificate_chain_pairs:
        if not isinstance(private_key, bytes) or not isinstance(
            certificate_chain,
            bytes,
        ):
            raise TypeError("private_key and certificate_chain must be bytes")

    return MockServerCredentials(
        private_key_certificate_chain_pairs=private_key_certificate_chain_pairs,
        root_certificates=root_certificates,
        require_client_auth=require_client_auth,
    )


class TestCertificateCredentials(FoundationTestCase):
    """Test certificate credentials functionality."""

    # Tests using conftest fixtures
    def test_mock_channel_credentials_with_client_cert(self, client_cert) -> None:
        """Test creating channel credentials using client certificate fixture."""
        creds = mock_ssl_channel_credentials(
            root_certificates=client_cert.cert_pem.encode(),
            private_key=client_cert.key_pem.encode(),
            certificate_chain=client_cert.cert_pem.encode(),
        )
        assert isinstance(creds.root_certificates, bytes)
        assert isinstance(creds.private_key, bytes)
        assert isinstance(creds.certificate_chain, bytes)
        assert creds.root_certificates == client_cert.cert_pem.encode()
        assert creds.private_key == client_cert.key_pem.encode()
        assert creds.certificate_chain == client_cert.cert_pem.encode()

    def test_mock_server_credentials_with_server_cert(self, server_cert, client_cert) -> None:
        """Test creating server credentials using server certificate fixture."""
        pairs = [(server_cert.key_pem.encode(), server_cert.cert_pem.encode())]
        creds = mock_ssl_server_credentials(
            private_key_certificate_chain_pairs=pairs,
            root_certificates=client_cert.cert_pem.encode(),  # For client authentication
            require_client_auth=True,
        )
        assert isinstance(creds.private_key_certificate_chain_pairs[0][0], bytes)
        assert isinstance(creds.private_key_certificate_chain_pairs[0][1], bytes)
        assert isinstance(creds.root_certificates, bytes)
        assert creds.private_key_certificate_chain_pairs == pairs
        assert creds.root_certificates == client_cert.cert_pem.encode()
        assert creds.require_client_auth is True

    def test_mock_server_credentials_multiple_certs(self, server_cert, client_cert) -> None:
        """Test creating server credentials with multiple certificate pairs."""
        # Using both server and client certs as pairs for testing
        pairs = [
            (server_cert.key_pem.encode(), server_cert.cert_pem.encode()),
            (client_cert.key_pem.encode(), client_cert.cert_pem.encode()),
        ]
        creds = mock_ssl_server_credentials(
            private_key_certificate_chain_pairs=pairs,
            root_certificates=client_cert.cert_pem.encode(),
            require_client_auth=True,
        )
        assert len(creds.private_key_certificate_chain_pairs) == 2
        assert creds.private_key_certificate_chain_pairs == pairs

    def test_mock_server_credentials_validation_with_certs(
        self,
        server_cert,
        client_cert,
    ) -> None:
        """Test validation rules with real certificates."""
        # Test requiring client auth without root certs
        with pytest.raises(ValueError):
            mock_ssl_server_credentials(
                private_key_certificate_chain_pairs=[
                    (server_cert.key_pem.encode(), server_cert.cert_pem.encode()),
                ],
                require_client_auth=True,  # Should fail without root_certificates
            )

        # Test with invalid pair types
        with pytest.raises(TypeError):
            mock_ssl_server_credentials(
                private_key_certificate_chain_pairs=[
                    (server_cert.key_pem, server_cert.cert_pem),  # Not encoded to bytes
                ],
            )

    def test_mock_channel_credentials_none_values(self, client_cert) -> None:
        """Test channel credentials with optional parameters as None."""
        creds = mock_ssl_channel_credentials(
            root_certificates=client_cert.cert_pem.encode(),
            # Omitting private_key and certificate_chain
        )
        assert isinstance(creds.root_certificates, bytes)
        assert creds.private_key is None
        assert creds.certificate_chain is None


# 🧱🏗️🔚
