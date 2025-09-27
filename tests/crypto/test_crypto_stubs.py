"""Tests for crypto module stub implementations when cryptography is not available."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from provide.foundation.errors import DependencyError


class TestCryptoStubImplementations:
    """Test that crypto stub implementations work correctly when cryptography is not available."""

    def test_certificate_stub_init_raises_dependency_error(self) -> None:
        """Test Certificate stub __init__ raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import Certificate

            with pytest.raises(DependencyError) as exc_info:
                Certificate()

            assert "cryptography" in str(exc_info.value)

    def test_certificate_stub_new_raises_dependency_error(self) -> None:
        """Test Certificate stub __new__ raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import Certificate

            with pytest.raises(DependencyError) as exc_info:
                Certificate()

            assert "cryptography" in str(exc_info.value)

    def test_certificate_class_methods_raise_dependency_error(self) -> None:
        """Test Certificate stub class methods raise DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import Certificate

            with pytest.raises(DependencyError):
                Certificate.create_self_signed_client_cert("test", "Test Org", 365)

            with pytest.raises(DependencyError):
                Certificate.create_self_signed_server_cert("test", "Test Org", 365)

    def test_certificate_base_stub_raises_dependency_error(self) -> None:
        """Test CertificateBase stub raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import CertificateBase

            with pytest.raises(DependencyError):
                # Just test the stub with minimal arguments - types don't matter for stubs
                CertificateBase(
                    subject=None,  # type: ignore[arg-type]
                    issuer=None,  # type: ignore[arg-type]
                    public_key="test_key",
                    not_valid_before=None,  # type: ignore[arg-type]
                    not_valid_after=None,  # type: ignore[arg-type]
                    serial_number=1
                )

    def test_certificate_config_stub_raises_dependency_error(self) -> None:
        """Test CertificateConfig stub raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import CertificateConfig

            with pytest.raises(DependencyError):
                config = {
                    "common_name": "test.com",
                    "organization": "Test Org",
                    "alt_names": ["test.com"],
                    "key_type": "rsa",
                    "not_valid_before": "2024-01-01T00:00:00Z",
                    "not_valid_after": "2025-01-01T00:00:00Z",
                }
                CertificateConfig(config)  # type: ignore[misc]

    def test_certificate_error_stub_is_regular_exception(self) -> None:
        """Test CertificateError stub is a regular exception."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import CertificateError

            # Should be able to instantiate as regular exception
            error = CertificateError("test error")
            assert str(error) == "test error"
            assert isinstance(error, Exception)

    def test_curve_type_stub_raises_dependency_error(self) -> None:
        """Test CurveType stub raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import CurveType

            with pytest.raises(DependencyError):
                CurveType("P256")

    def test_key_type_stub_raises_dependency_error(self) -> None:
        """Test KeyType stub raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import KeyType

            with pytest.raises(DependencyError):
                KeyType("RSA")

    def test_create_ca_stub_raises_dependency_error(self) -> None:
        """Test create_ca stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import create_ca

            with pytest.raises(DependencyError):
                create_ca("Test CA")

    def test_create_self_signed_stub_raises_dependency_error(self) -> None:
        """Test create_self_signed stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import create_self_signed

            with pytest.raises(DependencyError):
                create_self_signed("test.com")

    def test_generate_ec_keypair_stub_raises_dependency_error(self) -> None:
        """Test generate_ec_keypair stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import generate_ec_keypair

            with pytest.raises(DependencyError):
                generate_ec_keypair()

    def test_generate_ed25519_keypair_stub_raises_dependency_error(self) -> None:
        """Test generate_ed25519_keypair stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import generate_ed25519_keypair

            with pytest.raises(DependencyError):
                generate_ed25519_keypair()

    def test_generate_key_pair_stub_raises_dependency_error(self) -> None:
        """Test generate_key_pair stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import generate_key_pair

            with pytest.raises(DependencyError):
                generate_key_pair()

    def test_generate_keypair_stub_raises_dependency_error(self) -> None:
        """Test generate_keypair stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import generate_keypair

            with pytest.raises(DependencyError):
                generate_keypair("rsa")

    def test_generate_rsa_keypair_stub_raises_dependency_error(self) -> None:
        """Test generate_rsa_keypair stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import generate_rsa_keypair

            with pytest.raises(DependencyError):
                generate_rsa_keypair()

    def test_generate_signing_keypair_stub_raises_dependency_error(self) -> None:
        """Test generate_signing_keypair stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import generate_signing_keypair

            with pytest.raises(DependencyError):
                generate_signing_keypair()

    def test_generate_tls_keypair_stub_raises_dependency_error(self) -> None:
        """Test generate_tls_keypair stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import generate_tls_keypair

            with pytest.raises(DependencyError):
                generate_tls_keypair()

    def test_sign_data_stub_raises_dependency_error(self) -> None:
        """Test sign_data stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import sign_data

            with pytest.raises(DependencyError):
                sign_data(b"data", b"key")

    def test_verify_signature_stub_raises_dependency_error(self) -> None:
        """Test verify_signature stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import verify_signature

            with pytest.raises(DependencyError):
                verify_signature(b"data", b"signature", b"key")

    def test_get_default_hash_algorithm_stub_raises_dependency_error(self) -> None:
        """Test get_default_hash_algorithm stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import get_default_hash_algorithm

            with pytest.raises(DependencyError):
                get_default_hash_algorithm()

    def test_get_default_signature_algorithm_stub_raises_dependency_error(self) -> None:
        """Test get_default_signature_algorithm stub function raises DependencyError."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import get_default_signature_algorithm

            with pytest.raises(DependencyError):
                get_default_signature_algorithm()

    def test_constants_fallback_to_defaults(self) -> None:
        """Test that constants fallback to defaults when crypto is not available."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import (
                DEFAULT_CERTIFICATE_KEY_TYPE,
                DEFAULT_CERTIFICATE_VALIDITY_DAYS,
                DEFAULT_ECDSA_CURVE,
                DEFAULT_RSA_KEY_SIZE,
                DEFAULT_SIGNATURE_ALGORITHM,
                ED25519_PRIVATE_KEY_SIZE,
                ED25519_PUBLIC_KEY_SIZE,
                ED25519_SIGNATURE_SIZE,
                SUPPORTED_EC_CURVES,
                SUPPORTED_KEY_TYPES,
                SUPPORTED_RSA_SIZES,
            )

            # These should have reasonable defaults even without crypto
            assert DEFAULT_CERTIFICATE_KEY_TYPE is not None
            assert isinstance(DEFAULT_CERTIFICATE_VALIDITY_DAYS, int)
            assert DEFAULT_ECDSA_CURVE is not None
            assert isinstance(DEFAULT_RSA_KEY_SIZE, int)
            assert DEFAULT_SIGNATURE_ALGORITHM is not None
            assert isinstance(ED25519_PRIVATE_KEY_SIZE, int)
            assert isinstance(ED25519_PUBLIC_KEY_SIZE, int)
            assert isinstance(ED25519_SIGNATURE_SIZE, int)
            assert isinstance(SUPPORTED_EC_CURVES, list)
            assert isinstance(SUPPORTED_KEY_TYPES, list)
            assert isinstance(SUPPORTED_RSA_SIZES, list)

    def test_has_crypto_flag_accessible(self) -> None:
        """Test that _HAS_CRYPTO flag is accessible for conditional logic."""
        from provide.foundation.crypto import _HAS_CRYPTO

        # Should be a boolean
        assert isinstance(_HAS_CRYPTO, bool)
        # When testing with full dependencies, it should be True
        # When mocked to False, it should be False

    def test_all_exports_available(self) -> None:
        """Test that all crypto module exports are available even without cryptography."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import __all__

            # All items in __all__ should be importable
            for item_name in __all__:
                # Import should work even if usage fails
                import provide.foundation.crypto

                item = getattr(provide.foundation.crypto, item_name)
                assert item is not None

    def test_stub_implementations_provide_helpful_errors(self) -> None:
        """Test that stub implementations provide helpful error messages."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import create_ca, generate_keypair

            # All stub functions should raise DependencyError with helpful info
            with pytest.raises(DependencyError) as exc_info:
                create_ca("test")
            assert "cryptography" in str(exc_info.value).lower()

            with pytest.raises(DependencyError) as exc_info:
                generate_keypair("rsa")
            assert "cryptography" in str(exc_info.value).lower()

    def test_certificate_stub_with_arguments(self) -> None:
        """Test Certificate stub with various argument combinations."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import Certificate

            # All these should raise DependencyError regardless of arguments
            with pytest.raises(DependencyError):
                Certificate(cert_pem_or_uri="test")

            with pytest.raises(DependencyError):
                Certificate(generate_keypair=True)

            with pytest.raises(DependencyError):
                Certificate(cert_pem_or_uri="test", key_type="rsa")

    def test_enum_stubs_with_arguments(self) -> None:
        """Test enum stubs work with various argument combinations."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import CurveType, KeyType

            # All these should raise DependencyError regardless of arguments
            with pytest.raises(DependencyError):
                CurveType("P256")

            with pytest.raises(DependencyError):
                KeyType("RSA")

            with pytest.raises(DependencyError):
                CurveType("P256", some_arg="value")  # type: ignore[call-arg]

            with pytest.raises(DependencyError):
                KeyType("RSA", some_arg="value")  # type: ignore[call-arg]


class TestCryptoStubErrorMessages:
    """Test that crypto stub error messages are consistent and helpful."""

    def test_dependency_error_format(self) -> None:
        """Test that DependencyError has consistent format across stubs."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import Certificate, create_ca, generate_keypair

            # All should raise DependencyError with consistent fields
            functions_to_test = [
                lambda: Certificate(),
                lambda: create_ca("test"),
                lambda: generate_keypair("rsa"),
            ]

            for func in functions_to_test:
                with pytest.raises(DependencyError) as exc_info:
                    func()

                error = exc_info.value
                assert "cryptography" in str(error).lower()

    def test_dependency_error_inheritance(self) -> None:
        """Test that DependencyError is properly inherited."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import Certificate

            with pytest.raises(Exception) as exc_info:
                Certificate()

            # Should be a DependencyError which is a subclass of Exception
            assert isinstance(exc_info.value, DependencyError)
            assert isinstance(exc_info.value, Exception)


class TestCryptoStubDocumentation:
    """Test that crypto stubs provide proper documentation."""

    def test_stub_functions_have_docstrings(self) -> None:
        """Test that stub functions have descriptive docstrings."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import create_ca, generate_keypair

            # Stub functions should have helpful docstrings
            assert create_ca.__doc__ is not None
            assert "cryptography" in create_ca.__doc__.lower()

            assert generate_keypair.__doc__ is not None
            assert "cryptography" in generate_keypair.__doc__.lower()

    def test_stub_classes_have_docstrings(self) -> None:
        """Test that stub classes have descriptive docstrings."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import Certificate, CertificateBase

            # Stub classes should have helpful docstrings
            assert Certificate.__doc__ is not None
            assert "cryptography" in Certificate.__doc__.lower()

            assert CertificateBase.__doc__ is not None
            assert "cryptography" in CertificateBase.__doc__.lower()


class TestCryptoModuleIntegration:
    """Test crypto module integration with and without cryptography."""

    def test_crypto_module_conditional_imports(self) -> None:
        """Test that crypto module handles conditional imports correctly."""
        # This tests the try/except blocks in crypto/__init__.py
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            # Should be able to import the module
            import provide.foundation.crypto

            # Should have _HAS_CRYPTO flag
            assert hasattr(provide.foundation.crypto, "_HAS_CRYPTO")
            assert provide.foundation.crypto._HAS_CRYPTO is False

            # Should have all the expected exports
            assert hasattr(provide.foundation.crypto, "Certificate")
            assert hasattr(provide.foundation.crypto, "create_ca")
            assert hasattr(provide.foundation.crypto, "generate_keypair")

    def test_crypto_module_fallback_constants(self) -> None:
        """Test that crypto module provides fallback constants."""
        with patch("provide.foundation.crypto._HAS_CRYPTO", False):
            from provide.foundation.crypto import (
                DEFAULT_CERTIFICATE_KEY_TYPE,
                SUPPORTED_EC_CURVES,
                SUPPORTED_KEY_TYPES,
            )

            # Constants should be available from defaults
            assert DEFAULT_CERTIFICATE_KEY_TYPE is not None
            assert isinstance(SUPPORTED_EC_CURVES, list)
            assert isinstance(SUPPORTED_KEY_TYPES, list)
            assert len(SUPPORTED_EC_CURVES) > 0
            assert len(SUPPORTED_KEY_TYPES) > 0

    def test_crypto_all_exports_comprehensive(self) -> None:
        """Test that __all__ exports are comprehensive."""
        from provide.foundation.crypto import __all__

        # Key exports that should always be available
        expected_exports = [
            "Certificate",
            "create_ca",
            "create_self_signed",
            "generate_keypair",
            "sign_data",
            "verify_signature",
            "_HAS_CRYPTO",
            "DEFAULT_CERTIFICATE_KEY_TYPE",
        ]

        for export in expected_exports:
            assert export in __all__, f"Missing export: {export}"
