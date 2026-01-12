#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for crypto module dependency handling and stubs."""

from __future__ import annotations

import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.crypto import _HAS_CRYPTO
from provide.foundation.errors import DependencyError

# Skip message for when cryptography is available
SKIP_REASON = (
    "Tests verify behavior without cryptography dependency - "
    "skipping because cryptography is currently installed"
)


# Display the header immediately when module is imported

print("\n" + "=" * 60, file=sys.stderr)
print("🔒 CRYPTOGRAPHY DEPENDENCY TESTS", file=sys.stderr)
print("=" * 60, file=sys.stderr)
if _HAS_CRYPTO:
    print("⚠️  These tests verify behavior when cryptography is NOT installed", file=sys.stderr)
    print("💡 This is expected and correct behavior", file=sys.stderr)
else:
    print("⚠️  Cryptography is NOT installed - running dependency stub tests", file=sys.stderr)
print("=" * 60, file=sys.stderr)


@pytest.mark.skipif(_HAS_CRYPTO, reason=SKIP_REASON)
class TestCryptoDependencyStubs(FoundationTestCase):
    """Test cases for crypto module stub implementations when cryptography is not available."""

    def setup_method(self) -> None:
        """Reset module state before each test."""
        # Remove crypto modules from cache to force re-import
        modules_to_remove = [
            "provide.foundation.crypto",
            "provide.foundation.crypto.certificates",
            "provide.foundation.crypto.defaults",
            "provide.foundation.crypto.keys",
            "provide.foundation.crypto.ed25519",
        ]
        for module in modules_to_remove:
            if module in sys.modules:
                del sys.modules[module]

    def test_certificate_stub_init_raises_dependency_error(self) -> None:
        """Test that Certificate.__init__ raises DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            # Mock the import to fail
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import Certificate

            with pytest.raises(DependencyError) as exc_info:
                Certificate()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"
            assert "cryptography" in str(error)
            assert "crypto" in str(error)
            assert "provide-foundation[crypto]" in str(error)

    def test_certificate_stub_new_raises_dependency_error(self) -> None:
        """Test that Certificate.__new__ raises DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import Certificate

            with pytest.raises(DependencyError) as exc_info:
                Certificate.__new__(Certificate)

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

    def test_certificate_class_methods_raise_dependency_error(self) -> None:
        """Test that Certificate class methods raise DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import Certificate

            # Test create_self_signed_client_cert
            with pytest.raises(DependencyError) as exc_info:
                Certificate.create_self_signed_client_cert()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"
            assert "cryptography" in str(error)

            # Test create_self_signed_server_cert
            with pytest.raises(DependencyError) as exc_info:
                Certificate.create_self_signed_server_cert()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

    def test_certificate_base_stub_raises_dependency_error(self) -> None:
        """Test that CertificateBase raises DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import CertificateBase

            with pytest.raises(DependencyError) as exc_info:
                CertificateBase()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

    def test_certificate_config_stub_raises_dependency_error(self) -> None:
        """Test that CertificateConfig raises DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import CertificateConfig

            with pytest.raises(DependencyError) as exc_info:
                CertificateConfig()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

    def test_certificate_error_stub_is_regular_exception(self) -> None:
        """Test that CertificateError is a regular exception for compatibility."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import CertificateError

            # Should be able to create and raise CertificateError normally
            error = CertificateError("test error")
            assert str(error) == "test error"
            assert isinstance(error, Exception)

    def test_curve_type_stub_raises_dependency_error(self) -> None:
        """Test that CurveType raises DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import CurveType

            with pytest.raises(DependencyError) as exc_info:
                CurveType()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

    def test_key_type_stub_raises_dependency_error(self) -> None:
        """Test that KeyType raises DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import KeyType

            with pytest.raises(DependencyError) as exc_info:
                KeyType()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

    def test_certificate_functions_raise_dependency_error(self) -> None:
        """Test that certificate functions raise DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import create_ca, create_self_signed

            # Test create_ca
            with pytest.raises(DependencyError) as exc_info:
                create_ca()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

            # Test create_self_signed
            with pytest.raises(DependencyError) as exc_info:
                create_self_signed()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

    def test_key_generation_functions_raise_dependency_error(self) -> None:
        """Test that key generation functions raise DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import (
                generate_ec_keypair,
                generate_ed25519_keypair,
                generate_key_pair,
                generate_keypair,
                generate_rsa_keypair,
                generate_signing_keypair,
                generate_tls_keypair,
            )

            functions = [
                generate_ec_keypair,
                generate_ed25519_keypair,
                generate_key_pair,
                generate_keypair,
                generate_rsa_keypair,
                generate_signing_keypair,
                generate_tls_keypair,
            ]

            for func in functions:
                with pytest.raises(DependencyError) as exc_info:
                    func()

                error = exc_info.value
                assert error.code == "DEPENDENCY_MISSING"
                assert "cryptography" in str(error)

    def test_hash_algorithm_functions_raise_dependency_error(self) -> None:
        """Test that hash algorithm functions raise DependencyError when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import (
                get_default_hash_algorithm,
                get_default_signature_algorithm,
            )

            # Test get_default_hash_algorithm
            with pytest.raises(DependencyError) as exc_info:
                get_default_hash_algorithm()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

            # Test get_default_signature_algorithm
            with pytest.raises(DependencyError) as exc_info:
                get_default_signature_algorithm()

            error = exc_info.value
            assert error.code == "DEPENDENCY_MISSING"

    def test_constants_have_sensible_defaults(self) -> None:
        """Test that constants have sensible default values when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
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

            # Test that constants have expected default values
            assert DEFAULT_CERTIFICATE_KEY_TYPE == "ecdsa"
            assert DEFAULT_CERTIFICATE_VALIDITY_DAYS == 365
            assert DEFAULT_ECDSA_CURVE == "secp384r1"
            assert DEFAULT_RSA_KEY_SIZE == 2048
            assert DEFAULT_SIGNATURE_ALGORITHM == "ed25519"
            assert ED25519_PRIVATE_KEY_SIZE == 32
            assert ED25519_PUBLIC_KEY_SIZE == 32
            assert ED25519_SIGNATURE_SIZE == 64
            assert {"secp256r1", "secp384r1", "secp521r1"} == SUPPORTED_EC_CURVES
            assert {"rsa", "ecdsa", "ed25519"} == SUPPORTED_KEY_TYPES
            assert {2048, 3072, 4096} == SUPPORTED_RSA_SIZES

    def test_has_crypto_flag_is_false_without_cryptography(self) -> None:
        """Test that _HAS_CRYPTO flag is False when cryptography not available."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import _HAS_CRYPTO

            assert _HAS_CRYPTO is False

    def test_imports_work_without_cryptography(self) -> None:
        """Test that all crypto module imports work even without cryptography."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            # Should be able to import all symbols without ImportError
            from provide.foundation.crypto import (
                Certificate,
                CertificateBase,
                CertificateConfig,
                CertificateError,
                CurveType,
                KeyType,
            )

            # All imports should succeed
            assert Certificate is not None
            assert CertificateBase is not None
            assert CertificateConfig is not None
            assert CertificateError is not None
            assert CurveType is not None
            assert KeyType is not None

    def test_dependency_error_contains_proper_context(self) -> None:
        """Test that DependencyError contains proper context information."""
        with (
            patch.dict(sys.modules, {"cryptography": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'cryptography'")),
        ):
            from provide.foundation.crypto import Certificate

            with pytest.raises(DependencyError) as exc_info:
                Certificate()

            error = exc_info.value
            assert error.context["dependency.package"] == "cryptography"
            assert error.context["dependency.feature"] == "crypto"
            assert "provide-foundation[crypto]" in error.context["dependency.install_command"]


# 🧱🏗️🔚
