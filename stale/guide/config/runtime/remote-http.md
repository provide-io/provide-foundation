# HTTP Configuration Loading

Load configuration from HTTP endpoints including REST APIs and authenticated services.

## Basic HTTP Loading

```python
import asyncio
from provide.foundation.config import BaseConfig, ConfigManager, field
from provide.foundation.config.loaders import HTTPConfigLoader
from attrs import define

@define
class RemoteAppConfig(BaseConfig):
    """Configuration loaded from remote HTTP source."""
    
    api_url: str = field(description="API endpoint URL")
    timeout_seconds: int = field(description="Request timeout")
    max_retries: int = field(description="Maximum retry attempts")
    enable_caching: bool = field(description="Enable response caching")
    debug_mode: bool = field(description="Debug mode flag")

async def load_http_config():
    """Load configuration from HTTP endpoint."""
    
    # Create HTTP loader
    loader = HTTPConfigLoader(
        base_url="https://config.example.com",
        timeout=30.0,
        max_retries=3
    )
    
    # Load configuration from remote endpoint
    config_data = await loader.load("/api/config/myapp.json")
    
    # Create configuration instance
    config = RemoteAppConfig(**config_data)
    
    print(f"Loaded remote config:")
    print(f"  API URL: {config.api_url}")
    print(f"  Timeout: {config.timeout_seconds}s")
    print(f"  Debug: {config.debug_mode}")
    
    return config

# Usage
remote_config = asyncio.run(load_http_config())
```

## Authenticated HTTP Loading

```python
import asyncio
from typing import Any
from provide.foundation.config.loaders import AuthenticatedHTTPLoader
from provide.foundation.config import BaseConfig
from attrs import define

@define
class SecureRemoteConfig(BaseConfig):
    """Configuration loaded from authenticated endpoint."""
    
    database_url: str = field(description="Database connection URL")
    api_keys: dict[str, str] = field(factory=dict, description="API keys")
    feature_flags: dict[str, bool] = field(factory=dict, description="Feature toggles")

class AuthenticatedHTTPLoader:
    """HTTP loader with authentication support."""
    
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token
    
    async def load(self, endpoint: str) -> dict[str, Any]:
        """Load configuration with authentication."""
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{self.base_url}{endpoint}") as response:
                response.raise_for_status()
                return await response.json()

async def load_authenticated_config():
    """Load configuration from authenticated service."""
    
    # Get authentication token (from environment, secret store, etc.)
    auth_token = "your-auth-token-here"
    
    # Create authenticated loader
    loader = AuthenticatedHTTPLoader(
        base_url="https://secure-config.example.com",
        auth_token=auth_token
    )
    
    try:
        # Load secure configuration
        config_data = await loader.load("/api/v1/config/production")
        config = SecureRemoteConfig(**config_data)
        
        print("Loaded secure configuration:")
        print(f"  Database URL: {config.database_url[:20]}...")
        print(f"  API Keys: {len(config.api_keys)} keys loaded")
        print(f"  Feature Flags: {len(config.feature_flags)} flags loaded")
        
        return config
        
    except Exception as e:
        print(f"Failed to load secure configuration: {e}")
        raise

# Usage
secure_config = asyncio.run(load_authenticated_config())
```

## Advanced Authentication Methods

### OAuth2 Authentication

```python
import asyncio
import aiohttp
from typing import Optional
from provide.foundation.config import BaseConfig

class OAuth2HTTPLoader:
    """HTTP loader with OAuth2 authentication."""
    
    def __init__(self, 
                 base_url: str,
                 client_id: str, 
                 client_secret: str,
                 token_url: str):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None
    
    async def _get_access_token(self) -> str:
        """Get or refresh OAuth2 access token."""
        import time
        
        # Check if current token is still valid
        if (self._access_token and self._token_expires_at and 
            time.time() < self._token_expires_at - 300):  # 5 min buffer
            return self._access_token
        
        # Request new token
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, data=data) as response:
                response.raise_for_status()
                token_data = await response.json()
        
        self._access_token = token_data['access_token']
        self._token_expires_at = time.time() + token_data.get('expires_in', 3600)
        
        return self._access_token
    
    async def load(self, endpoint: str) -> dict[str, Any]:
        """Load configuration with OAuth2 authentication."""
        access_token = await self._get_access_token()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}", headers=headers) as response:
                response.raise_for_status()
                return await response.json()

async def oauth2_config_example():
    """Example of OAuth2-authenticated configuration loading."""
    
    loader = OAuth2HTTPLoader(
        base_url="https://api.example.com",
        client_id="your-client-id",
        client_secret="your-client-secret",
        token_url="https://auth.example.com/oauth2/token"
    )
    
    config_data = await loader.load("/config/application")
    config = RemoteAppConfig(**config_data)
    
    print(f"OAuth2 config loaded: {config.api_url}")
    return config
```

### API Key Authentication

```python
class APIKeyHTTPLoader:
    """HTTP loader with API key authentication."""
    
    def __init__(self, 
                 base_url: str,
                 api_key: str,
                 api_key_header: str = "X-API-Key"):
        self.base_url = base_url
        self.api_key = api_key
        self.api_key_header = api_key_header
    
    async def load(self, endpoint: str) -> dict[str, Any]:
        """Load configuration with API key authentication."""
        headers = {
            self.api_key_header: self.api_key,
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}", headers=headers) as response:
                response.raise_for_status()
                return await response.json()

async def api_key_config_example():
    """Example of API key authenticated configuration loading."""
    
    loader = APIKeyHTTPLoader(
        base_url="https://config-api.example.com",
        api_key="your-api-key-here",
        api_key_header="Authorization"  # Custom header name
    )
    
    config_data = await loader.load("/v1/configurations/production")
    return RemoteAppConfig(**config_data)
```

## Request Configuration and Error Handling

### Custom Request Configuration

```python
import asyncio
import aiohttp
from aiohttp import ClientTimeout
from provide.foundation.config import BaseConfig

class ConfigurableHTTPLoader:
    """HTTP loader with extensive configuration options."""
    
    def __init__(self,
                 base_url: str,
                 timeout: float = 30.0,
                 max_retries: int = 3,
                 retry_delay: float = 1.0,
                 verify_ssl: bool = True,
                 custom_headers: dict[str, str] = None):
        self.base_url = base_url.rstrip('/')
        self.timeout = ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.verify_ssl = verify_ssl
        self.custom_headers = custom_headers or {}
    
    async def load(self, endpoint: str) -> dict[str, Any]:
        """Load configuration with retry logic and error handling."""
        url = f"{self.base_url}{endpoint}"
        
        connector = aiohttp.TCPConnector(ssl=self.verify_ssl)
        
        async with aiohttp.ClientSession(
            timeout=self.timeout,
            headers=self.custom_headers,
            connector=connector
        ) as session:
            
            for attempt in range(self.max_retries + 1):
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status == 404:
                            raise ConfigurationNotFoundError(f"Configuration not found: {url}")
                        else:
                            response.raise_for_status()
                
                except aiohttp.ClientError as e:
                    if attempt == self.max_retries:
                        raise ConfigurationLoadError(f"Failed to load config after {self.max_retries + 1} attempts: {e}")
                    
                    # Wait before retry
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
        
        raise ConfigurationLoadError(f"Exhausted all retry attempts for {url}")

class ConfigurationNotFoundError(Exception):
    """Configuration endpoint not found."""
    pass

class ConfigurationLoadError(Exception):
    """Failed to load configuration."""
    pass

async def robust_http_config_example():
    """Example of robust HTTP configuration loading."""
    
    loader = ConfigurableHTTPLoader(
        base_url="https://config.example.com",
        timeout=15.0,
        max_retries=3,
        retry_delay=2.0,
        verify_ssl=True,
        custom_headers={
            "User-Agent": "MyApp-Config-Loader/1.0",
            "Accept": "application/json"
        }
    )
    
    try:
        config_data = await loader.load("/api/config/myapp.json")
        return RemoteAppConfig(**config_data)
    
    except ConfigurationNotFoundError as e:
        print(f"Configuration not found: {e}")
        # Use default configuration
        return RemoteAppConfig(
            api_url="http://localhost:8000",
            timeout_seconds=30,
            max_retries=3,
            enable_caching=False,
            debug_mode=True
        )
    
    except ConfigurationLoadError as e:
        print(f"Failed to load configuration: {e}")
        raise
```

## Configuration Formats and Content Types

### Multiple Format Support

```python
import json
import yaml
from typing import Any

class MultiFormatHTTPLoader:
    """HTTP loader supporting multiple configuration formats."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    async def load_json(self, endpoint: str) -> dict[str, Any]:
        """Load JSON configuration."""
        headers = {"Accept": "application/json"}
        return await self._load_with_headers(endpoint, headers, self._parse_json)
    
    async def load_yaml(self, endpoint: str) -> dict[str, Any]:
        """Load YAML configuration."""
        headers = {"Accept": "application/x-yaml, text/yaml"}
        return await self._load_with_headers(endpoint, headers, self._parse_yaml)
    
    async def load_toml(self, endpoint: str) -> dict[str, Any]:
        """Load TOML configuration."""
        headers = {"Accept": "application/toml"}
        return await self._load_with_headers(endpoint, headers, self._parse_toml)
    
    async def _load_with_headers(self, endpoint: str, headers: dict, parser: callable) -> dict[str, Any]:
        """Load configuration with specific headers and parser."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}", headers=headers) as response:
                response.raise_for_status()
                content = await response.text()
                return parser(content)
    
    def _parse_json(self, content: str) -> dict[str, Any]:
        """Parse JSON content."""
        return json.loads(content)
    
    def _parse_yaml(self, content: str) -> dict[str, Any]:
        """Parse YAML content."""
        return yaml.safe_load(content)
    
    def _parse_toml(self, content: str) -> dict[str, Any]:
        """Parse TOML content."""
        import tomllib
        return tomllib.loads(content)

async def multi_format_example():
    """Example of loading different configuration formats."""
    
    loader = MultiFormatHTTPLoader("https://config.example.com")
    
    # Load JSON config
    json_config = await loader.load_json("/config/app.json")
    print(f"JSON config: {json_config}")
    
    # Load YAML config
    yaml_config = await loader.load_yaml("/config/app.yaml")
    print(f"YAML config: {yaml_config}")
    
    # Load TOML config
    toml_config = await loader.load_toml("/config/app.toml")
    print(f"TOML config: {toml_config}")
```

## Best Practices

### 1. Handle Network Errors Gracefully

```python
# ✅ Good - Proper error handling and fallbacks
async def load_config_with_fallback():
    try:
        config = await load_http_config()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.warning(f"Remote config failed, using local fallback: {e}")
        config = load_local_fallback_config()
    return config

# ❌ Bad - No error handling
async def load_config_unsafe():
    return await load_http_config()  # Will crash on network errors
```

### 2. Use Appropriate Timeouts

```python
# ✅ Good - Reasonable timeouts
loader = HTTPConfigLoader(
    base_url="https://config.example.com",
    timeout=15.0,      # 15 second timeout
    max_retries=3      # Limited retries
)

# ❌ Bad - No timeout limits
loader = HTTPConfigLoader(
    base_url="https://config.example.com",
    timeout=None,      # Could hang forever
    max_retries=10     # Too many retries
)
```

### 3. Secure Authentication Tokens

```python
import os

# ✅ Good - Use environment variables or secret stores
auth_token = os.getenv("CONFIG_AUTH_TOKEN")
if not auth_token:
    raise ValueError("CONFIG_AUTH_TOKEN environment variable required")

# ❌ Bad - Hardcoded tokens
auth_token = "hardcoded-token-123"  # Security risk
```

## Next Steps

- [Cloud Services](remote-cloud.md) - Integration with AWS, Consul, and other cloud services
- [Polling & Updates](remote-polling.md) - Automatic configuration updates
- [Resilience Patterns](remote-resilience.md) - Circuit breakers and caching