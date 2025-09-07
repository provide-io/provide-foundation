# Crypto Testing Fixtures

Comprehensive certificate and key testing data for TLS and authentication testing scenarios.

## Certificate Fixtures

### Core Certificate Objects

**Available fixtures**:
- `client_cert` - Client certificate for authentication testing
- `server_cert` - Server certificate for TLS testing  
- `ca_cert` - Certificate Authority for certificate chain testing

```python
def test_certificate_validation(client_cert, server_cert):
    """Test certificate validation logic."""
    # Client cert fixture provides Certificate object
    assert client_cert.is_valid()
    assert client_cert.common_name == "localhost"
    
    # Server cert for TLS scenarios
    assert server_cert.is_valid()
    assert not server_cert.is_expired()

def test_certificate_chain(ca_cert):
    """Test certificate chain validation."""
    # CA cert can be used to create signed certificates
    issued_cert = ca_cert.issue_certificate(
        common_name="service.example.com",
        validity_days=90
    )
    
    assert issued_cert.verify_chain([ca_cert])
```

### Certificate Properties

```python
def test_certificate_properties(client_cert, server_cert, ca_cert):
    """Test certificate property access."""
    
    # Client certificate properties
    assert client_cert.common_name == "localhost"
    assert client_cert.is_valid()
    assert not client_cert.is_expired()
    
    # Server certificate properties
    assert server_cert.subject_alt_names == ["localhost", "127.0.0.1"]
    assert server_cert.key_usage == ["digital_signature", "key_encipherment"]
    
    # CA certificate properties
    assert ca_cert.is_ca_certificate()
    assert ca_cert.can_sign_certificates()
```

## PEM Content Fixtures

### Valid PEM Data

**Available fixtures**:
- `valid_cert_pem` - Valid certificate PEM content
- `valid_key_pem` - Valid private key PEM content

```python
def test_pem_parsing(valid_cert_pem, valid_key_pem):
    """Test PEM content parsing."""
    # Valid PEM should parse successfully
    cert = Certificate.from_pem(valid_cert_pem)
    assert cert.is_valid()
    
    # Valid key should be usable
    key = PrivateKey.from_pem(valid_key_pem)
    assert key.is_valid()
    
    # Key should match certificate
    assert key.matches_certificate(cert)
```

### Invalid PEM Data

**Available fixtures**:
- `invalid_cert_pem` - Invalid certificate for error testing
- `invalid_key_pem` - Invalid key for error testing
- `malformed_cert_pem` - Malformed certificate data
- `empty_cert` - Empty certificate content

```python
def test_invalid_pem_handling(invalid_cert_pem, invalid_key_pem, malformed_cert_pem):
    """Test handling of invalid PEM content."""
    
    # Invalid PEM should raise appropriate error
    with pytest.raises(CertificateError):
        Certificate.from_pem(invalid_cert_pem)
    
    # Invalid key should fail validation
    with pytest.raises(KeyError):
        PrivateKey.from_pem(invalid_key_pem)
    
    # Malformed PEM should be detected
    with pytest.raises(PEMFormatError):
        Certificate.from_pem(malformed_cert_pem)

def test_empty_content(empty_cert):
    """Test handling of empty certificate content."""
    with pytest.raises(EmptyContentError):
        Certificate.from_pem(empty_cert)
```

## File-Based Fixtures

### Temporary Certificate Files

**Available fixtures**:
- `temporary_cert_file` - Temporary file with certificate
- `temporary_key_file` - Temporary file with private key

```python
def test_certificate_file_loading(temporary_cert_file, temporary_key_file):
    """Test loading certificates from files."""
    # Load from temporary files
    cert = Certificate.from_file(temporary_cert_file)
    key = PrivateKey.from_file(temporary_key_file)
    
    assert cert.is_valid()
    assert key.matches_certificate(cert)

def test_file_path_handling(temporary_cert_file):
    """Test file path handling."""
    # Test with Path object
    from pathlib import Path
    cert_path = Path(temporary_cert_file)
    cert = Certificate.from_file(cert_path)
    assert cert.is_valid()
    
    # Test with string path
    cert_str = Certificate.from_file(str(cert_path))
    assert cert_str.fingerprint() == cert.fingerprint()
```

### Format Edge Cases

**Available fixtures**:
- `cert_with_windows_line_endings` - Certificate with Windows CRLF
- `cert_with_utf8_bom` - Certificate with UTF-8 BOM
- `cert_with_extra_whitespace` - Certificate with formatting issues

```python
def test_format_handling(
    cert_with_windows_line_endings, 
    cert_with_utf8_bom,
    cert_with_extra_whitespace
):
    """Test handling various file formats."""
    
    # Should handle Windows line endings
    cert1 = Certificate.from_pem(cert_with_windows_line_endings)
    assert cert1.is_valid()
    
    # Should handle UTF-8 BOM
    cert2 = Certificate.from_pem(cert_with_utf8_bom) 
    assert cert2.is_valid()
    
    # Should handle extra whitespace
    cert3 = Certificate.from_pem(cert_with_extra_whitespace)
    assert cert3.is_valid()
    
    # All should be functionally equivalent
    assert cert1.fingerprint() == cert2.fingerprint() == cert3.fingerprint()
```

## Certificate Chain Testing

### Chain Validation

```python
def test_certificate_chain_validation(ca_cert, server_cert):
    """Test certificate chain validation."""
    
    # Create intermediate CA
    intermediate_ca = ca_cert.issue_certificate(
        common_name="Intermediate CA",
        is_ca=True,
        validity_days=365
    )
    
    # Create end entity certificate signed by intermediate
    end_cert = intermediate_ca.issue_certificate(
        common_name="example.com",
        validity_days=90
    )
    
    # Build and validate chain
    chain = [end_cert, intermediate_ca, ca_cert]
    assert end_cert.verify_chain(chain[1:])  # Without self
    
    # Test chain building
    built_chain = end_cert.build_chain([intermediate_ca, ca_cert])
    assert len(built_chain) == 3
    assert built_chain[0] == end_cert
    assert built_chain[-1] == ca_cert

def test_partial_chain_validation(ca_cert):
    """Test validation with partial chains."""
    # Create certificate signed by CA
    cert = ca_cert.issue_certificate(
        common_name="test.example.com",
        validity_days=30
    )
    
    # Should validate with just the CA
    assert cert.verify_chain([ca_cert])
    
    # Should fail without the CA
    with pytest.raises(ChainValidationError):
        cert.verify_chain([])
```

## TLS Testing Scenarios

### Server Configuration Testing

```python
def test_tls_server_config(server_cert, valid_key_pem):
    """Test TLS server configuration."""
    import ssl
    
    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # Load certificate and key
    with temporary_cert_file(server_cert.to_pem()) as cert_file:
        with temporary_key_file(valid_key_pem) as key_file:
            context.load_cert_chain(cert_file, key_file)
    
    # Verify context configuration
    assert context.check_hostname is True
    assert context.verify_mode == ssl.CERT_REQUIRED

def test_client_authentication(client_cert, ca_cert):
    """Test client certificate authentication."""
    
    # Verify client cert is signed by CA
    assert client_cert.verify_chain([ca_cert])
    
    # Test client authentication logic
    def authenticate_client(cert_pem: str) -> bool:
        try:
            cert = Certificate.from_pem(cert_pem)
            return cert.verify_chain([ca_cert]) and not cert.is_expired()
        except Exception:
            return False
    
    # Valid client cert should authenticate
    assert authenticate_client(client_cert.to_pem())
    
    # Expired cert should not authenticate
    expired_cert = ca_cert.issue_certificate(
        common_name="expired.example.com",
        validity_days=-1  # Already expired
    )
    assert not authenticate_client(expired_cert.to_pem())
```

### Certificate Rotation Testing

```python
def test_certificate_rotation(ca_cert):
    """Test certificate rotation scenarios."""
    
    # Create initial certificate
    old_cert = ca_cert.issue_certificate(
        common_name="service.example.com",
        validity_days=30
    )
    
    # Create new certificate for rotation
    new_cert = ca_cert.issue_certificate(
        common_name="service.example.com",
        validity_days=365
    )
    
    # Both should be valid
    assert old_cert.is_valid()
    assert new_cert.is_valid()
    
    # Different certificates but same subject
    assert old_cert.common_name == new_cert.common_name
    assert old_cert.fingerprint() != new_cert.fingerprint()
    
    # Test rotation logic
    def should_rotate_certificate(cert: Certificate, days_before_expiry: int = 30) -> bool:
        return cert.days_until_expiry() <= days_before_expiry
    
    # Simulate time-based rotation
    assert should_rotate_certificate(old_cert, days_before_expiry=60)  # Should rotate
    assert not should_rotate_certificate(new_cert, days_before_expiry=60)  # Should not rotate
```

## Error Testing Scenarios

### Certificate Validation Errors

```python
def test_certificate_validation_errors(ca_cert):
    """Test various certificate validation error scenarios."""
    
    # Self-signed certificate (not signed by CA)
    self_signed = Certificate.create_self_signed("self-signed.example.com")
    
    with pytest.raises(ChainValidationError):
        self_signed.verify_chain([ca_cert])
    
    # Certificate with wrong CA
    wrong_ca = Certificate.create_ca("Wrong CA")
    wrong_cert = wrong_ca.issue_certificate("test.example.com")
    
    with pytest.raises(ChainValidationError):
        wrong_cert.verify_chain([ca_cert])
    
    # Expired certificate
    expired_cert = ca_cert.issue_certificate(
        common_name="expired.example.com",
        validity_days=-10  # Expired 10 days ago
    )
    
    with pytest.raises(CertificateExpiredError):
        expired_cert.validate_expiry()

def test_key_certificate_mismatch(valid_cert_pem, ca_cert):
    """Test key and certificate mismatch detection."""
    
    # Create certificate and unrelated key
    cert = Certificate.from_pem(valid_cert_pem)
    wrong_key = ca_cert.generate_key_pair()
    
    # Should detect mismatch
    assert not wrong_key.matches_certificate(cert)
    
    # Test in TLS context setup
    with pytest.raises(KeyCertificateMismatchError):
        validate_key_cert_pair(wrong_key.to_pem(), cert.to_pem())
```

## Integration Examples

### Complete TLS Testing Suite

```python
class TestTLSIntegration:
    """Complete TLS integration test suite."""
    
    def test_server_setup(self, server_cert, valid_key_pem, ca_cert):
        """Test complete TLS server setup."""
        
        # Create server with certificate
        server = TLSServer(
            cert_pem=server_cert.to_pem(),
            key_pem=valid_key_pem,
            ca_cert_pem=ca_cert.to_pem()
        )
        
        # Verify server configuration
        assert server.is_configured()
        assert server.can_accept_connections()
        
        # Test certificate properties
        assert server.certificate.common_name == "localhost"
        assert not server.certificate.is_expired()
    
    def test_client_connection(self, client_cert, valid_key_pem, ca_cert):
        """Test TLS client connection with mutual authentication."""
        
        client = TLSClient(
            client_cert_pem=client_cert.to_pem(),
            client_key_pem=valid_key_pem,
            ca_cert_pem=ca_cert.to_pem()
        )
        
        # Mock server connection
        mock_server = MockTLSServer(require_client_cert=True)
        
        # Test connection establishment
        connection = client.connect(mock_server.endpoint)
        assert connection.is_secure()
        assert connection.client_authenticated()
        
        # Verify mutual authentication
        assert connection.server_cert.verify_chain([ca_cert])
        assert connection.client_cert.verify_chain([ca_cert])
```

## Best Practices

### 1. Use Appropriate Fixtures

```python
# ✅ Good - Use specific fixtures
def test_certificates(client_cert, server_cert):
    # Certificate-specific fixtures
    pass

def test_pem_content(valid_cert_pem, invalid_cert_pem):
    # PEM content fixtures
    pass

# ❌ Bad - Manual certificate creation
def test_certificates():
    cert = Certificate.create_self_signed("test")
    # Manual setup, not reusable
```

### 2. Test Both Valid and Invalid Cases

```python
def test_certificate_scenarios(valid_cert_pem, invalid_cert_pem):
    """Test both valid and invalid certificate handling."""
    
    # Test valid case
    cert = Certificate.from_pem(valid_cert_pem)
    assert cert.is_valid()
    
    # Test invalid case
    with pytest.raises(CertificateError):
        Certificate.from_pem(invalid_cert_pem)
```

### 3. Verify Security Properties

```python
def test_security_properties(server_cert, client_cert, ca_cert):
    """Verify important security properties."""
    
    # Verify certificates are properly signed
    assert server_cert.verify_chain([ca_cert])
    assert client_cert.verify_chain([ca_cert])
    
    # Verify expiration dates are reasonable
    assert server_cert.days_until_expiry() > 0
    assert client_cert.days_until_expiry() > 0
    
    # Verify key usage is appropriate
    assert "digital_signature" in server_cert.key_usage
    assert "key_encipherment" in server_cert.key_usage
```

## Next Steps

- [Stream Testing](api-streams.md) - Stream redirection and output capture
- [Logger Management](api-logger.md) - Logger state management and isolation
- [Context Detection](api-context.md) - Testing environment detection