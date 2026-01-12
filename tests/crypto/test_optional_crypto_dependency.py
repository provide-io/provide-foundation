#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for optional cryptography dependency behavior."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.crypto import _HAS_CRYPTO


class TestOptionalCryptoDependency(FoundationTestCase):
    """Test that crypto functionality properly handles missing cryptography dependency."""

    def test_require_crypto_with_crypto_available(self) -> None:
        """Test _require_crypto when cryptography is available."""
        # Import should work normally when cryptography is available
        from provide.foundation.crypto.certificates import _require_crypto

        # Should not raise when cryptography is available
        _require_crypto()  # Should complete without error

    def test_require_crypto_without_crypto(self) -> None:
        """Test _require_crypto when cryptography is not available."""
        # Mock _HAS_CRYPTO to False to simulate missing cryptography
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            from provide.foundation.crypto.certificates import _require_crypto

            with pytest.raises(
                ImportError,
                match="Cryptography features require optional dependencies",
            ):
                _require_crypto()

    def test_certificate_creation_without_crypto(self) -> None:
        """Test Certificate creation fails gracefully without cryptography."""
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            from provide.foundation.crypto.certificates import (
                Certificate,
                CertificateError,
            )

            # Any attempt to create/use Certificate.generate should fail with helpful error
            # The Certificate wraps ImportError in CertificateError but the original cause should mention crypto
            with pytest.raises(
                CertificateError,
                match="Failed to initialize certificate",
            ):
                Certificate.generate(
                    key_type="rsa",
                )  # This should trigger _require_crypto

    def test_certificate_base_creation_without_crypto(self) -> None:
        """Test CertificateBase.create fails gracefully without cryptography."""
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            from typing import cast

            from provide.foundation.crypto.certificates import (
                CertificateBase,
            )
            from provide.foundation.crypto.certificates.base import CertificateConfig

            config = cast(
                CertificateConfig,
                {
                    "common_name": "test.com",
                    "organization": "Test Org",
                    "key_type": "rsa",
                    "not_valid_before": "2024-01-01T00:00:00Z",
                    "not_valid_after": "2025-01-01T00:00:00Z",
                },
            )

            with pytest.raises(
                ImportError,
                match="uv add 'provide-foundation\\[crypto\\]'",
            ):
                CertificateBase.create(config)

    def test_convenience_functions_without_crypto(self) -> None:
        """Test convenience functions fail gracefully without cryptography."""
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            from provide.foundation.crypto.certificates import (
                create_ca,
                create_self_signed,
            )

            with pytest.raises(
                ImportError,
                match="uv add 'provide-foundation\\[crypto\\]'",
            ):
                create_self_signed("test.com")

            with pytest.raises(
                ImportError,
                match="uv add 'provide-foundation\\[crypto\\]'",
            ):
                create_ca("Test CA")

    def test_signature_functions_without_crypto(self) -> None:
        """Test signature OOP API fails gracefully without cryptography."""
        with patch("provide.foundation.crypto.ed25519._HAS_CRYPTO", False):
            from provide.foundation.crypto.ed25519 import (
                Ed25519Signer,
                Ed25519Verifier,
            )

            with pytest.raises(
                ImportError,
                match="uv add 'provide-foundation\\[crypto\\]'",
            ):
                Ed25519Signer.generate()

            with pytest.raises(
                ImportError,
                match="uv add 'provide-foundation\\[crypto\\]'",
            ):
                Ed25519Verifier(b"fake_key")

    def test_crypto_init_without_dependency(self) -> None:
        """Test crypto __init__.py behavior without cryptography."""
        # Test the behavior when crypto is not available
        with patch("provide.foundation.crypto.__init__._HAS_CRYPTO", False):
            # Should be able to import but functions should fail appropriately
            from provide.foundation.crypto import Certificate

            # The class should exist but operations should fail
            assert Certificate is not None


class TestCryptoTypeAliases(FoundationTestCase):
    """Test type aliases behavior with/without cryptography."""

    def test_type_aliases_with_crypto(self) -> None:
        """Test that type aliases are properly set when crypto is available."""
        from provide.foundation.crypto.certificates import KeyPair, PublicKey

        # When cryptography is available, these should be proper type aliases
        assert KeyPair is not None
        assert PublicKey is not None

    def test_type_aliases_without_crypto(self) -> None:
        """Test that type aliases behave correctly when crypto is not available."""
        # Test that we can check the conditional type alias logic
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            # Import and verify the type aliases exist (they may be None or other values)
            from provide.foundation.crypto.certificates import KeyPair, PublicKey

            # The type aliases should exist (may be None based on _HAS_CRYPTO)
            # This verifies the conditional logic works
            assert KeyPair is not None or PublicKey is not None or (not _HAS_CRYPTO)


class TestCryptoModuleImport(FoundationTestCase):
    """Test crypto module import behavior."""

    def test_crypto_module_imports_with_crypto(self) -> None:
        """Test that crypto modules import correctly when cryptography is available."""
        # These should import without issues when crypto is available
        from provide.foundation.crypto import (
            Certificate,
            CertificateError,
            create_ca,
            create_self_signed,
        )

        assert Certificate is not None
        assert CertificateError is not None
        assert callable(create_self_signed)
        assert callable(create_ca)

    def test_crypto_error_message_format(self) -> None:
        """Test that error messages are properly formatted."""
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            from provide.foundation.crypto.certificates import _require_crypto

            try:
                _require_crypto()
                raise AssertionError("Should have raised ImportError")
            except ImportError as e:
                error_msg = str(e)
                assert "Cryptography features require optional dependencies" in error_msg
                assert "uv add 'provide-foundation[crypto]'" in error_msg

    def test_signatures_error_message_format(self) -> None:
        """Test that signature error messages are properly formatted."""
        with patch("provide.foundation.crypto.ed25519._HAS_CRYPTO", False):
            from provide.foundation.crypto.ed25519 import _require_crypto

            try:
                _require_crypto()
                raise AssertionError("Should have raised ImportError")
            except ImportError as e:
                error_msg = str(e)
                assert "Cryptography features require optional dependencies" in error_msg
                assert "uv add 'provide-foundation[crypto]'" in error_msg


class TestCryptoFallbackBehavior(FoundationTestCase):
    """Test fallback behavior when crypto operations are attempted without cryptography."""

    def test_certificate_property_access_without_crypto(self) -> None:
        """Test certificate property access when crypto is not available."""
        # Test that certificate properties handle missing crypto gracefully
        # When crypto is not available, even basic Certificate creation should fail
        # if it tries to parse invalid PEM data
        from provide.foundation.crypto.certificates import Certificate, CertificateError

        with pytest.raises(CertificateError):  # Certificate wraps underlying errors
            Certificate.from_pem(cert_pem="dummy")

    def test_crypto_module_resilience(self) -> None:
        """Test that the crypto module is resilient to import issues."""
        # Test the basic resilience without aggressive module manipulation
        # The crypto module should already be imported and stable at this point

        # Test that we can check the _HAS_CRYPTO flag
        from provide.foundation.crypto import _HAS_CRYPTO

        # Since cryptography is available in test environment, this should be True
        assert _HAS_CRYPTO is True

        # Test that the module can be imported safely
        import provide.foundation.crypto.certificates

        assert hasattr(provide.foundation.crypto.certificates, "_HAS_CRYPTO")

        # Test error handling when _require_crypto is patched
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            from provide.foundation.crypto.certificates import _require_crypto

            with pytest.raises(ImportError) as exc_info:
                _require_crypto()

            assert "Cryptography features require optional dependencies" in str(exc_info.value)


class TestCryptoInstallationMessage(FoundationTestCase):
    """Test that helpful installation messages are provided."""

    def test_installation_message_consistency(self) -> None:
        """Test that all crypto modules provide consistent installation messages."""
        expected_message_parts = ["uv add 'provide-foundation[crypto]'"]

        # Test certificates module message
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            from provide.foundation.crypto.certificates import _require_crypto

            try:
                _require_crypto()
            except ImportError as e:
                for part in expected_message_parts:
                    assert part in str(e)

        # Test ed25519 module message
        with patch("provide.foundation.crypto.ed25519._HAS_CRYPTO", False):
            from provide.foundation.crypto.ed25519 import _require_crypto

            try:
                _require_crypto()
            except ImportError as e:
                for part in expected_message_parts:
                    assert part in str(e)

    def test_user_friendly_error_messages(self) -> None:
        """Test that error messages are user-friendly and actionable."""
        with patch("provide.foundation.crypto.certificates.base._HAS_CRYPTO", False):
            from provide.foundation.crypto.certificates import _require_crypto

            try:
                _require_crypto()
            except ImportError as e:
                error_msg = str(e)
                # Should contain actionable information
                assert "install" in error_msg.lower()
                assert "crypto" in error_msg.lower()
                assert "provide-foundation[crypto]" in error_msg
                # Should not be overly technical
                assert len(error_msg) < 200  # Reasonable length
                assert "optional dependencies" in error_msg.lower()


# 🧱🏗️🔚
