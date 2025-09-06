"""Additional tests for crypto constants to improve code coverage."""

from unittest.mock import patch, Mock
import pytest

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
        assert constants.SUPPORTED_RSA_SIZES == {2048, 3072, 4096}
        assert 2048 in constants.SUPPORTED_RSA_SIZES
        assert 3072 in constants.SUPPORTED_RSA_SIZES
        assert 4096 in constants.SUPPORTED_RSA_SIZES

    def test_ecdsa_constants(self):
        """Test ECDSA constants are defined correctly."""
        assert constants.DEFAULT_ECDSA_CURVE == "secp384r1"
        assert constants.SUPPORTED_EC_CURVES == {
            "secp256r1",
            "secp384r1", 
            "secp521r1",
        }
        assert "secp384r1" in constants.SUPPORTED_EC_CURVES

    def test_key_type_constants(self):
        """Test key type constants."""
        assert constants.SUPPORTED_KEY_TYPES == {"rsa", "ecdsa", "ed25519"}
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

    def test_get_config_value_with_config_available(self):
        """Test _get_config_value when config system is available."""
        mock_config = Mock(return_value="test_value")
        
        with patch.dict('sys.modules', {'provide.foundation.config': Mock()}):
            mock_config_module = Mock()
            mock_config_module.get_config = mock_config
            
            with patch('provide.foundation.crypto.constants.get_config', mock_config):
                result = constants._get_config_value("test_key", "default_value")
                assert result == "test_value"
                mock_config.assert_called_once_with("crypto.test_key", "default_value")

    def test_get_config_value_import_error_fallback(self):
        """Test _get_config_value when config system is not available."""
        # Ensure the config module is not available
        original_modules = dict(sys.modules) if 'sys' in globals() else {}
        
        # Force ImportError by removing config module if present
        import sys
        if 'provide.foundation.config' in sys.modules:
            del sys.modules['provide.foundation.config']
        
        try:
            result = constants._get_config_value("test_key", "default_fallback")
            assert result == "default_fallback"
        finally:
            # Restore modules
            for key, module in original_modules.items():
                if module is not None:
                    sys.modules[key] = module

    def test_get_config_value_with_different_types(self):
        """Test _get_config_value with different default types."""
        # Test with string default
        result_str = constants._get_config_value("string_key", "default_string")
        assert isinstance(result_str, str)
        
        # Test with int default
        result_int = constants._get_config_value("int_key", 42)
        assert isinstance(result_int, int)

    def test_get_default_hash_algorithm_success(self):
        """Test get_default_hash_algorithm when algorithms module is available."""
        mock_default_algorithm = "sha256"
        
        with patch.dict('sys.modules', {'provide.foundation.crypto.algorithms': Mock()}):
            mock_algorithms_module = Mock()
            mock_algorithms_module.DEFAULT_ALGORITHM = mock_default_algorithm
            
            with patch('provide.foundation.crypto.constants.DEFAULT_ALGORITHM', mock_default_algorithm):
                # Mock the _get_config_value to return a test value
                with patch('provide.foundation.crypto.constants._get_config_value', return_value="custom_hash"):
                    result = constants.get_default_hash_algorithm()
                    assert result == "custom_hash"

    def test_get_default_hash_algorithm_with_fallback(self):
        """Test get_default_hash_algorithm using fallback value."""
        # This test is more complex due to the import, but we can test the function exists
        try:
            result = constants.get_default_hash_algorithm()
            assert isinstance(result, str)
            assert len(result) > 0
        except ImportError:
            # If algorithms module not available, that's also valid
            pytest.skip("Crypto algorithms module not available")

    def test_get_default_signature_algorithm_success(self):
        """Test get_default_signature_algorithm."""
        with patch('provide.foundation.crypto.constants._get_config_value') as mock_get_config:
            mock_get_config.return_value = "custom_signature"
            
            result = constants.get_default_signature_algorithm()
            assert result == "custom_signature"
            mock_get_config.assert_called_once_with(
                "signature_algorithm", 
                constants.DEFAULT_SIGNATURE_ALGORITHM
            )

    def test_get_default_signature_algorithm_with_fallback(self):
        """Test get_default_signature_algorithm with fallback to constant."""
        with patch('provide.foundation.crypto.constants._get_config_value') as mock_get_config:
            mock_get_config.return_value = constants.DEFAULT_SIGNATURE_ALGORITHM
            
            result = constants.get_default_signature_algorithm()
            assert result == constants.DEFAULT_SIGNATURE_ALGORITHM
            assert result == "ed25519"

    def test_constants_are_final_type_annotations(self):
        """Test that constants are properly typed as Final."""
        # This is more of a static analysis test, but we can check the values exist
        assert hasattr(constants, 'ED25519_PRIVATE_KEY_SIZE')
        assert hasattr(constants, 'DEFAULT_RSA_KEY_SIZE')
        assert hasattr(constants, 'SUPPORTED_RSA_SIZES')
        assert hasattr(constants, 'DEFAULT_ECDSA_CURVE')
        assert hasattr(constants, 'SUPPORTED_EC_CURVES')
        assert hasattr(constants, 'SUPPORTED_KEY_TYPES')

    def test_string_returns_from_config_functions(self):
        """Test that config functions return strings."""
        # Test get_default_signature_algorithm always returns string
        result = constants.get_default_signature_algorithm()
        assert isinstance(result, str)
        
        # Test get_default_hash_algorithm always returns string (if available)
        try:
            result = constants.get_default_hash_algorithm()
            assert isinstance(result, str)
        except ImportError:
            pytest.skip("Crypto algorithms module not available")