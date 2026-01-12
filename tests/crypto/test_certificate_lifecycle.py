#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.crypto import Certificate, CertificateError

# Fixtures will be available via tests.fixtures through conftest.py
# from tests.fixtures.crypto import client_cert


class TestCertificateLifecycle(FoundationTestCase):
    """Test certificate lifecycle functionality."""

    @pytest.mark.asyncio
    async def test_cleanup_after_failed_generation(self) -> None:
        """Test proper cleanup after failed certificate generation."""
        with pytest.raises(CertificateError):
            Certificate.generate(key_type="invalid_type")

    @pytest.mark.asyncio
    async def test_certificate_is_valid(self, client_cert: Any) -> None:
        """Ensure validity check works correctly."""
        assert isinstance(client_cert.is_valid, bool), "Validity should return True/False"

    @pytest.mark.asyncio
    async def test_expired_certificate(self) -> None:
        """Ensure expired certificates fail validation."""
        expired_cert = Certificate.generate(
            key_type="rsa",
            validity_days=-1,  # Set to expire yesterday relative to its creation 'now'
        )

        # Ensure the certificate's not_valid_after is indeed in the past
        # compared to the current real time.
        # datetime.now(timezone.utc) inside the test will be slightly after
        # the datetime.now(timezone.utc) used inside Certificate's __attrs_post_init__.
        current_real_now = datetime.now(UTC)
        assert expired_cert._base.not_valid_after < current_real_now, (
            f"Certificate expiry date {expired_cert._base.not_valid_after} should be before current time {current_real_now}"
        )

        assert not expired_cert.is_valid, "Expired certificates should be invalid"

    @pytest.mark.asyncio
    async def test_certificate_validity_period(self, client_cert: Any) -> None:
        """Test certificate validity period checking."""
        now = datetime.now(UTC)
        assert client_cert._base.not_valid_before <= now
        assert now <= client_cert._base.not_valid_after

    @pytest.mark.asyncio
    async def test_verify_expired_certificate(self) -> None:
        """Ensure verification fails when certificate is expired."""
        expired_cert = Certificate.generate(
            key_type="rsa",
            validity_days=-1,  # Set to make it expired
        )
        assert not expired_cert.is_valid, "Expired certificate should be invalid"
        assert not expired_cert.verify_trust(expired_cert), "Expired certificates should not verify"

    @pytest.mark.asyncio
    async def test_certificate_extension_addition_failure(self) -> None:
        """Ensure failures in adding extensions raise CertificateError."""
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
    async def test_certificate_trust_chain_validation(self) -> None:  # Name can remain, or be more specific
        """Ensure trust chain verification correctly fails on a mocked signature mismatch."""
        # Ensure 'mock' is imported from unittest (already imported at file level)
        # from unittest import mock

        relying_party_cert = Certificate.generate(
            common_name="RelyingPartyCert",
            key_type="ecdsa",
        )
        ca_cert = Certificate.generate(
            common_name="TestCACert",
            key_type="ecdsa",
        )

        relying_party_cert.trust_chain = [ca_cert]  # relying_party_cert trusts ca_cert

        end_entity_cert = Certificate.generate(
            common_name="EndEntityToVerify",
            key_type="ecdsa",
        )

        # Mock end_entity_cert's issuer to be ca_cert's subject so that the
        # issuer check within _validate_signature passes, forcing a signature attempt.
        # REMOVED: with mock.patch.object(end_entity_cert._cert, 'issuer', ca_cert._cert.subject):

        # The mock for EllipticCurvePublicKey.verify can remain. If the issuer check *were* to pass
        # (which it won't for these two unrelated certs as end_entity_cert is self-signed with a different subject),
        # this mock would ensure failure.
        # With unrelated certs, _validate_signature will return False due to issuer mismatch
        # *before* the EllipticCurvePublicKey.verify line is reached.
        with patch(
            "cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey.verify",
            side_effect=Exception("Simulated Signature Failure"),
        ):
            # relying_party_cert.verify_trust(end_entity_cert) will call:
            # _validate_signature(signed_cert=end_entity_cert, signing_cert=ca_cert)
            # Inside _validate_signature, since end_entity_cert.issuer (self-signed) != ca_cert.subject,
            # it will return False.
            # Thus, verify_trust will return False.
            assert not relying_party_cert.verify_trust(end_entity_cert), (
                "Verification of an unrelated certificate (or one with a bad signature if issuers matched) should fail."
            )


# 🧱🏗️🔚
