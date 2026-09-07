"""An IP address in `alt_names` has to become an IP SAN, not a DNS SAN.

`x509.DNSName("127.0.0.1")` is a certificate that vouches for a *hostname*
spelled like an address. No TLS client matches it when connecting to that
address, because an IP connection is checked against iPAddress entries. The
certificate looks correct in every listing and fails every handshake.

Found from the other end: a gRPC client dialling 127.0.0.1 could not verify a
server certificate carrying only `DNS:localhost`, and the obvious repair --
adding "127.0.0.1" to alt_names -- produced a certificate that still did not
verify, with nothing to say why.

SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
SPDX-License-Identifier: Apache-2.0
"""

from __future__ import annotations

import ipaddress

from cryptography import x509
from cryptography.hazmat.primitives import serialization
import pytest

from provide.foundation.crypto.certificates import Certificate


def _san(certificate: Certificate) -> x509.SubjectAlternativeName:
    parsed = x509.load_pem_x509_certificate(certificate.cert_pem.encode())
    return parsed.extensions.get_extension_for_class(x509.SubjectAlternativeName).value


@pytest.fixture(scope="module")
def mixed_cert() -> Certificate:
    return Certificate.create_self_signed_server_cert(
        common_name="test.server",
        organization_name="Test",
        validity_days=1,
        alt_names=["localhost", "127.0.0.1", "::1"],
    )


def test_ipv4_alt_name_becomes_an_ip_san(mixed_cert: Certificate) -> None:
    addresses = _san(mixed_cert).get_values_for_type(x509.IPAddress)
    assert ipaddress.ip_address("127.0.0.1") in addresses


def test_ipv6_alt_name_becomes_an_ip_san(mixed_cert: Certificate) -> None:
    addresses = _san(mixed_cert).get_values_for_type(x509.IPAddress)
    assert ipaddress.ip_address("::1") in addresses


def test_hostname_alt_name_stays_a_dns_san(mixed_cert: Certificate) -> None:
    assert "localhost" in _san(mixed_cert).get_values_for_type(x509.DNSName)


def test_an_address_is_not_also_emitted_as_a_hostname(mixed_cert: Certificate) -> None:
    """A DNS SAN spelled like an address is the bug this prevents."""
    names = _san(mixed_cert).get_values_for_type(x509.DNSName)
    assert "127.0.0.1" not in names
    assert "::1" not in names


def test_a_hostname_only_certificate_is_unchanged() -> None:
    """The existing shape keeps working: no IP SAN appears from nowhere."""
    cert = Certificate.create_self_signed_server_cert(
        common_name="test.server",
        organization_name="Test",
        validity_days=1,
        alt_names=["localhost"],
    )
    san = _san(cert)
    assert san.get_values_for_type(x509.DNSName) == ["localhost"]
    assert san.get_values_for_type(x509.IPAddress) == []


def test_serialization_round_trip_preserves_the_ip_san(mixed_cert: Certificate) -> None:
    """The SAN survives PEM, which is how it reaches a plugin handshake line."""
    parsed = x509.load_pem_x509_certificate(mixed_cert.cert_pem.encode())
    reloaded = x509.load_pem_x509_certificate(parsed.public_bytes(serialization.Encoding.PEM))
    san = reloaded.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
    assert ipaddress.ip_address("127.0.0.1") in san.get_values_for_type(x509.IPAddress)
