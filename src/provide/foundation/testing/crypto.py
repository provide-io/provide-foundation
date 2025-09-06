"""
Crypto Testing Fixtures for Foundation.

Provides comprehensive pytest fixtures for testing certificate functionality,
including valid/invalid certificates, keys, chains, and edge cases.
"""

import pytest

from provide.foundation import logger
from provide.foundation.crypto import Certificate


@pytest.fixture(scope="module")
def client_cert():
    """Create a client certificate for testing."""
    cert_pem = """-----BEGIN CERTIFICATE-----
MIIB+jCCAYGgAwIBAgIJAPsxOr78BIU0MAoGCCqGSM49BAMEMCgxEjAQBgNVBAoM
CUhhc2hpQ29ycDESMBAGA1UEAwwJbG9jYWxob3N0MB4XDTI1MDIwNTIzMTkzN1oX
DTI2MDIwNTIzMTkzN1owKDESMBAGA1UECgwJSGFzaGlDb3JwMRIwEAYDVQQDDAls
b2NhbGhvc3QwdjAQBgcqhkjOPQIBBgUrgQQAIgNiAARCi3SNYYDpSeScRM52tFYr
URzsPOE/ad8BzvpvL+mfy1c5oHQhh6KPnxpoo1WyDJGYplwPTGS68DvvWmolrPAt
C7I7r7spgyJS1358E5fA2NWk9/YPaiUzK2gsyrL9dKajdzB1MA8GA1UdEwEB/wQF
MAMBAf8wFAYDVR0RBA0wC4IJbG9jYWxob3N0MB0GA1UdJQQWMBQGCCsGAQUFBwMC
BggrBgEFBQcDATAOBgNVHQ8BAf8EBAMCA6gwHQYDVR0OBBYEFOwuttXPh5kTPSpX
a2ex0+VKjlpaMAoGCCqGSM49BAMEA2cAMGQCMGbN17Zt1GxZ41cXTaQOKuv/BIQd
nkaRz51XrITKaULNie4bgW6gT94cTUFQ9SNwEAIwOpmKeZqYG9WHcqol4QEUmMVM
MY3jxMiLpb9Mt/ysstXmsrQY7UoLu+c6zfKwyTEJ
-----END CERTIFICATE-----"""

    key_pem = """-----BEGIN EC PRIVATE KEY-----
MIGkAgEBBDAkxo19KczdciRiJjOWEKGY5mH9s1D0aUS5XBdvktcaonIOdqNrkCt1
BC5YjEAVLNWgBwYFK4EEACKhZANiAARCi3SNYYDpSeScRM52tFYrURzsPOE/ad8B
zvpvL+mfy1c5oHQhh6KPnxpoo1WyDJGYplwPTGS68DvvWmolrPAtC7I7r7spgyJS
1358E5fA2NWk9/YPaiUzK2gsyrL9dKY=
-----END EC PRIVATE KEY-----"""

    logger.debug(f"Created CLIENT_CERT fixture: {cert_pem[:30]}...")
    return Certificate(cert_pem_or_uri=cert_pem, key_pem_or_uri=key_pem)


@pytest.fixture(scope="module")
def server_cert():
    """Create a server certificate for testing."""
    cert_pem = """-----BEGIN CERTIFICATE-----
MIIB+jCCAYGgAwIBAgIJAKrIoEQw7N9LMAoGCCqGSM49BAMEMCgxEjAQBgNVBAoM
CUhhc2hpQ29ycDESMBAGA1UEAwwJbG9jYWxob3N0MB4XDTI1MDIwNTIzMTkzN1oX
DTI2MDIwNTIzMTkzN1owKDESMBAGA1UECgwJSGFzaGlDb3JwMRIwEAYDVQQDDAls
b2NhbGhvc3QwdjAQBgcqhkjOPQIBBgUrgQQAIgNiAARMxEVmGX3a4IWPOAJ2MX2s
2Wj3KZ0Io5EwUPMkxknGheO2e55qeHp/tkEFzYt9AH8du1xJLKKFbsGV5q9vipGN
x5XMbj2RMdH5VXHTAdc/bLFFy9kybQqo300Rv6ViW2KjdzB1MA8GA1UdEwEB/wQF
MAMBAf8wFAYDVR0RBA0wC4IJbG9jYWxob3N0MB0GA1UdJQQWMBQGCCsGAQUFBwMC
BggrBgEFBQcDATAOBgNVHQ8BAf8EBAMCA6gwHQYDVR0OBBYEFJy7Iz7whfiALYDB
TsM+IHXb1E8+MAoGCCqGSM49BAMEA2cAMGQCMFwxBS3lZSUprvrNGfJL83oGVY97
emQpHy/SEWpHBK8awn1XeTf+ZAwLaxc3K+AKqwIwPwIbIlmstd69zAYMFNHtzceN
XOzBx35sWRw92gr/hbE4hYeDBqEUwstSFNZ6MZu0
-----END CERTIFICATE-----"""

    key_pem = """-----BEGIN EC PRIVATE KEY-----
MIGkAgEBBDDZ1MORWFVI0HtgKv+zZys/5e1HVmfcs4bwdp3VEsuwS6an3gTwGnSP
Ce+bI6f/TvGgBwYFK4EEACKhZANiAARMxEVmGX3a4IWPOAJ2MX2s2Wj3KZ0Io5Ew
UPMkxknGheO2e55qeHp/tkEFzYt9AH8du1xJLKKFbsGV5q9vipGNx5XMbj2RMdH5
VXHTAdc/bLFFy9kybQqo300Rv6ViW2I=
-----END EC PRIVATE KEY-----"""

    logger.debug(f"Created SERVER_CERT fixture: {cert_pem[:30]}...")
    return Certificate(cert_pem_or_uri=cert_pem, key_pem_or_uri=key_pem)


@pytest.fixture(scope="module")
def ca_cert():
    """Create a self-signed CA certificate for testing."""
    return Certificate.create_ca(
        common_name="Test CA", organization_name="Test Organization", validity_days=365
    )


@pytest.fixture(scope="module")
def valid_key_pem(client_cert):
    """Get a valid key PEM from the client cert fixture."""
    return client_cert.key


@pytest.fixture
def valid_cert_pem(client_cert):
    """Get a valid certificate PEM from the client cert fixture."""
    return client_cert.cert


@pytest.fixture
def invalid_key_pem() -> str:
    """Returns an invalid PEM key."""
    return "INVALID KEY DATA"


@pytest.fixture
def invalid_cert_pem() -> str:
    """Returns an invalid PEM certificate."""
    return "INVALID CERTIFICATE DATA"


@pytest.fixture
def malformed_cert_pem() -> str:
    """Returns a PEM certificate with incorrect headers."""
    return "-----BEGIN CERT-----\nMALFORMED DATA\n-----END CERT-----"


@pytest.fixture
def empty_cert() -> str:
    """Returns an empty certificate string."""
    return ""


@pytest.fixture
def temporary_cert_file(tmp_path, client_cert) -> str:
    """Creates a temporary file containing the client certificate."""
    cert_file = tmp_path / "client_cert.pem"
    cert_file.write_text(client_cert.cert)
    return f"file://{cert_file}"


@pytest.fixture
def temporary_key_file(tmp_path, client_cert) -> str:
    """Creates a temporary file containing the client private key."""
    key_file = tmp_path / "client_key.pem"
    key_file.write_text(client_cert.key)
    return f"file://{key_file}"


@pytest.fixture
def cert_with_windows_line_endings(client_cert) -> str:
    """Returns a certificate PEM with Windows line endings."""
    return client_cert.cert.replace("\n", "\r\n")


@pytest.fixture
def cert_with_utf8_bom(client_cert) -> str:
    """Returns a certificate PEM with UTF-8 BOM."""
    return "\ufeff" + client_cert.cert


@pytest.fixture
def cert_with_extra_whitespace(client_cert) -> str:
    """Returns a certificate PEM with extra whitespace."""
    return f"   {client_cert.cert}   \n\n  "


@pytest.fixture(scope="module")
def external_ca_pem() -> str:
    """Provides an externally generated CA certificate PEM."""
    return """-----BEGIN CERTIFICATE-----
MIIB4TCCAYegAwIBAgIJAPZ9vcVfR8AdMAoGCCqGSM49BAMCMFExCzAJBgNVBAYT
AlVTMQswCQYDVQQIDAJDQTEUMBIGA1UEBwwLU2FuIEZyYW5jaXNjbzEOMAwGA1UE
CgwFTXlPcmcxEzARBgNVBAMMCkV4dGVybmFsIENBMB4XDTI0MDgwMjEwNTgwMVoX
DTM0MDczMDEwNTgwMVowUTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMREwDwYD
VQQHDAhTYW5EaWVnbzEOMAwGA1UECgwFTXlPcmcxEzARBgNVBAMMCkV4dGVybmFs
IENBMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEgyF5Y8upm+M3ZzO8P4n7q2sS+L4c
mhl5XGg3vIOwFf7lG8XZCgJ6Xy4t1t8oD3zY0m9X8H8Z4YhY7K6b7c8Y7Xv6Y9fV
Q8M7Jg9nJ0x5c1N40zQwZzKjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8E
BTADAQH/MB0GA1UdDgQWBBTGX00Gq7b09y/0C9eK0XgJp0mY7DAKBggqhkjOPQQD
AgNJADBGAiEAx1xH/b83/u5t7r29a/THZnFjQ7pvT2N0L4hG4BgGgXACIQD02W2+
MHB78ZWM+JOgikYj99qD6nLp0nkMyGmkSC7RYg==
-----END CERTIFICATE-----"""
