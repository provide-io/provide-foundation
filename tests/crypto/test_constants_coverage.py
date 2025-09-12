"""Additional tests for crypto constants to improve code coverage."""

from unittest.mock import patch

from provide.foundation.crypto import constants


class TestCryptoConstantsCoverage:
    """Test crypto constants for improved coverage."""

    def test_ed25519_constants(self):
        """Test Ed25519 constants are defined correctly."""
        assert constants.ED25519_PRIVATE_KEY_SIZE == 32
        assert constants.ED25519_PUBLIC_KEY_SIZE == 32
        assert constants.ED25519_SIGNATURE_SIZE == 64

    def test_rsa_constants(self):
        """Test RSA constants are defined correctly."""
        assert constants.DEFAULT_RSA_KEY_SIZE == 2048
        assert {2048, 3072, 4096} == constants.SUPPORTED_RSA_SIZES
        assert 2048 in constants.SUPPORTED_RSA_SIZES
        assert 3072 in constants.SUPPORTED_RSA_SIZES
        assert 4096 in constants.SUPPORTED_RSA_SIZES

    def test_ecdsa_constants(self):
        """Test ECDSA constants are defined correctly."""
        assert constants.DEFAULT_ECDSA_CURVE == "secp384r1"
        assert {
            "secp256r1",
            "secp384r1",
            "secp521r1",
        } == constants.SUPPORTED_EC_CURVES
        assert "secp384r1" in constants.SUPPORTED_EC_CURVES

    def test_key_type_constants(self):
        """Test key type constants."""
        assert {"rsa", "ecdsa", "ed25519"} == constants.SUPPORTED_KEY_TYPES
        assert "ed25519" in constants.SUPPORTED_KEY_TYPES
        assert "rsa" in constants.SUPPORTED_KEY_TYPES
        assert "ecdsa" in constants.SUPPORTED_KEY_TYPES

    def test_default_algorithm_constants(self):
        """Test default algorithm constants."""
        assert constants.DEFAULT_SIGNATURE_ALGORITHM == "ed25519"
        assert constants.DEFAULT_CERTIFICATE_KEY_TYPE == "ecdsa"
        assert constants.DEFAULT_CERTIFICATE_CURVE == constants.DEFAULT_ECDSA_CURVE

    def test_certificate_validity_constants(self):
        """Test certificate validity constants."""
        assert constants.DEFAULT_CERTIFICATE_VALIDITY_DAYS == 365
        assert constants.MIN_CERTIFICATE_VALIDITY_DAYS == 1
        assert constants.MAX_CERTIFICATE_VALIDITY_DAYS == 3650

    def test_get_config_value_function_exists(self):
        """Test _get_config_value function exists and is callable."""
        assert hasattr(constants, "_get_config_value")
        assert callable(constants._get_config_value)

    def test_get_default_hash_algorithm_function_exists(self):
        """Test get_default_hash_algorithm function exists."""
        assert hasattr(constants, "get_default_hash_algorithm")
        assert callable(constants.get_default_hash_algorithm)

    def test_get_default_signature_algorithm_function_exists(self):
        """Test get_default_signature_algorithm function exists."""
        assert hasattr(constants, "get_default_signature_algorithm")
        assert callable(constants.get_default_signature_algorithm)

    def test_get_default_signature_algorithm_success(self):
        """Test get_default_signature_algorithm."""
        with patch(
            "provide.foundation.crypto.constants._get_config_value"
        ) as mock_get_config:
            mock_get_config.return_value = "custom_signature"

            result = constants.get_default_signature_algorithm()
            assert result == "custom_signature"
            mock_get_config.assert_called_once_with(
                "signature_algorithm", constants.DEFAULT_SIGNATURE_ALGORITHM
            )

    def test_get_default_signature_algorithm_with_fallback(self):
        """Test get_default_signature_algorithm with fallback to constant."""
        with patch(
            "provide.foundation.crypto.constants._get_config_value"
        ) as mock_get_config:
            mock_get_config.return_value = constants.DEFAULT_SIGNATURE_ALGORITHM

            result = constants.get_default_signature_algorithm()
            assert result == constants.DEFAULT_SIGNATURE_ALGORITHM
            assert result == "ed25519"

    def test_constants_are_final_type_annotations(self):
        """Test that constants are properly typed as Final."""
        # This is more of a static analysis test, but we can check the values exist
        assert hasattr(constants, "ED25519_PRIVATE_KEY_SIZE")
        assert hasattr(constants, "DEFAULT_RSA_KEY_SIZE")
        assert hasattr(constants, "SUPPORTED_RSA_SIZES")
        assert hasattr(constants, "DEFAULT_ECDSA_CURVE")
        assert hasattr(constants, "SUPPORTED_EC_CURVES")
        assert hasattr(constants, "SUPPORTED_KEY_TYPES")

    def test_string_returns_from_config_functions(self):
        """Test that config functions return strings."""
        # Mock _get_config_value to avoid dependency issues
        with patch(
            "provide.foundation.crypto.constants._get_config_value",
            return_value="test_algorithm",
        ):
            result = constants.get_default_signature_algorithm()
            assert isinstance(result, str)
            assert result == "test_algorithm"

    def test_get_config_value_with_import_error(self):
        """Test _get_config_value when config system is not available."""
        with patch("builtins.__import__", side_effect=ImportError):
            result = constants._get_config_value("test_key", "default_value")
            assert result == "default_value"

    def test_get_default_hash_algorithm_function_call(self):
        """Test get_default_hash_algorithm returns a string."""
        with patch(
            "provide.foundation.crypto.constants._get_config_value"
        ) as mock_get_config:
            mock_get_config.return_value = "test_hash_algo"

            result = constants.get_default_hash_algorithm()
            assert isinstance(result, str)
            assert result == "test_hash_algo"

    def test_get_default_signature_algorithm_calls_get_config_value(self):
        """Test get_default_signature_algorithm calls _get_config_value correctly."""
        with patch(
            "provide.foundation.crypto.constants._get_config_value"
        ) as mock_get_config:
            mock_get_config.return_value = "custom_sig_algo"

            result = constants.get_default_signature_algorithm()
            assert result == "custom_sig_algo"
            mock_get_config.assert_called_once_with(
                "signature_algorithm", constants.DEFAULT_SIGNATURE_ALGORITHM
            )
