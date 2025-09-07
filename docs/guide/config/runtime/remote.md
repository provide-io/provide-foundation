# Remote Configuration

Loading and managing configuration from remote sources including URLs, APIs, and cloud services.

## HTTP Configuration Loading

### Basic HTTP Loading

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

### Authenticated HTTP Loading

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

## Cloud Service Integration

### AWS Parameter Store

```python
import asyncio
import boto3
from botocore.exceptions import ClientError
from provide.foundation.config import BaseConfig, ConfigManager
from attrs import define

@define
class AWSConfig(BaseConfig):
    """Configuration loaded from AWS Parameter Store."""
    
    region: str = field(description="AWS region")
    environment: str = field(description="Environment name")
    service_config: dict[str, Any] = field(factory=dict, description="Service configuration")

class AWSParameterStoreLoader:
    """Load configuration from AWS Systems Manager Parameter Store."""
    
    def __init__(self, region: str = "us-west-2"):
        self.ssm = boto3.client("ssm", region_name=region)
        self.region = region
    
    async def load_parameters(self, path_prefix: str) -> dict[str, Any]:
        """Load parameters with given path prefix."""
        try:
            paginator = self.ssm.get_paginator("get_parameters_by_path")
            
            config_data = {}
            
            for page in paginator.paginate(
                Path=path_prefix,
                Recursive=True,
                WithDecryption=True
            ):
                for param in page["Parameters"]:
                    # Convert parameter name to config key
                    key = param["Name"].replace(path_prefix, "").lstrip("/")
                    key = key.replace("/", "_")
                    
                    # Handle different parameter types
                    value = param["Value"]
                    if param.get("Type") == "StringList":
                        value = value.split(",")
                    
                    config_data[key] = value
            
            return config_data
            
        except ClientError as e:
            print(f"Error loading from Parameter Store: {e}")
            raise

async def load_aws_config():
    """Load configuration from AWS Parameter Store."""
    
    loader = AWSParameterStoreLoader(region="us-west-2")
    
    # Load parameters for our application
    config_data = await loader.load_parameters("/myapp/prod")
    
    # Additional AWS metadata
    config_data.update({
        "region": loader.region,
        "environment": "production"
    })
    
    config = AWSConfig(**config_data)
    
    print(f"Loaded AWS configuration from {config.region}:")
    print(f"  Environment: {config.environment}")
    print(f"  Parameters loaded: {len(config.service_config)}")
    
    return config

# Usage  
aws_config = asyncio.run(load_aws_config())
```

### Consul Integration

```python
import asyncio
import aiohttp
from typing import Any
from provide.foundation.config import BaseConfig
from attrs import define

@define
class ConsulConfig(BaseConfig):
    """Configuration loaded from HashiCorp Consul."""
    
    consul_url: str = field(description="Consul server URL")
    service_config: dict[str, Any] = field(factory=dict, description="Service configuration")
    metadata: dict[str, str] = field(factory=dict, description="Consul metadata")

class ConsulConfigLoader:
    """Load configuration from Consul KV store."""
    
    def __init__(self, consul_url: str = "http://localhost:8500"):
        self.consul_url = consul_url.rstrip("/")
    
    async def load_kv(self, key_prefix: str) -> dict[str, Any]:
        """Load configuration from Consul KV store."""
        
        async with aiohttp.ClientSession() as session:
            # Get all keys under prefix
            url = f"{self.consul_url}/v1/kv/{key_prefix}?recurse=true"
            
            async with session.get(url) as response:
                if response.status == 404:
                    return {}  # No keys found
                
                response.raise_for_status()
                kv_data = await response.json()
        
        # Process Consul KV response
        config_data = {}
        
        for item in kv_data:
            key = item["Key"]
            value = item.get("Value", "")
            
            # Decode base64 value
            if value:
                import base64
                decoded_value = base64.b64decode(value).decode("utf-8")
                
                # Try to parse as JSON
                try:
                    import json
                    parsed_value = json.loads(decoded_value)
                except json.JSONDecodeError:
                    parsed_value = decoded_value
            else:
                parsed_value = None
            
            # Convert key path to nested dict structure
            key_parts = key.replace(key_prefix + "/", "").split("/")
            current = config_data
            
            for part in key_parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            current[key_parts[-1]] = parsed_value
        
        return config_data

async def load_consul_config():
    """Load configuration from Consul."""
    
    loader = ConsulConfigLoader("http://consul.service.consul:8500")
    
    # Load application configuration
    app_config = await loader.load_kv("config/myapp")
    
    config = ConsulConfig(
        consul_url=loader.consul_url,
        service_config=app_config,
        metadata={
            "loader_type": "consul_kv",
            "timestamp": str(asyncio.get_event_loop().time())
        }
    )
    
    print(f"Loaded Consul configuration:")
    print(f"  Consul URL: {config.consul_url}")
    print(f"  Configuration keys: {len(config.service_config)}")
    
    return config

# Usage
consul_config = asyncio.run(load_consul_config())
```

## Configuration Polling

### Automatic Updates

```python
import asyncio
from typing import Callable
from provide.foundation.config import ConfigManager
from provide.foundation import get_logger

logger = get_logger(__name__)

class PollingConfigManager(ConfigManager):
    """Configuration manager with automatic polling for updates."""
    
    def __init__(self, poll_interval: float = 60.0):
        super().__init__()
        self.poll_interval = poll_interval
        self._polling_tasks: dict[str, asyncio.Task] = {}
        self._update_callbacks: dict[str, list[Callable]] = {}
    
    async def start_polling(self, config_name: str, loader_func: Callable):
        """Start polling for configuration updates."""
        
        if config_name in self._polling_tasks:
            logger.warning(f"Already polling {config_name}")
            return
        
        logger.info(f"Starting configuration polling", 
                   config_name=config_name, 
                   interval=self.poll_interval)
        
        task = asyncio.create_task(
            self._poll_loop(config_name, loader_func)
        )
        self._polling_tasks[config_name] = task
    
    async def stop_polling(self, config_name: str):
        """Stop polling for a configuration."""
        
        if config_name not in self._polling_tasks:
            return
        
        task = self._polling_tasks.pop(config_name)
        task.cancel()
        
        try:
            await task
        except asyncio.CancelledError:
            pass
        
        logger.info(f"Stopped configuration polling", config_name=config_name)
    
    def on_update(self, config_name: str, callback: Callable):
        """Register callback for configuration updates."""
        
        if config_name not in self._update_callbacks:
            self._update_callbacks[config_name] = []
        
        self._update_callbacks[config_name].append(callback)
    
    async def _poll_loop(self, config_name: str, loader_func: Callable):
        """Main polling loop for configuration updates."""
        
        while True:
            try:
                # Load fresh configuration
                new_config = await loader_func()
                
                # Get current configuration
                current_config = await self.get(config_name)
                
                # Check for changes
                if current_config is None:
                    # First time loading
                    await self.set(config_name, new_config)
                    logger.info(f"Initial configuration loaded", config_name=config_name)
                    
                elif current_config != new_config:
                    # Configuration changed
                    changes = current_config.diff(new_config) if hasattr(current_config, 'diff') else {}
                    
                    await self.set(config_name, new_config)
                    
                    logger.info(f"Configuration updated", 
                               config_name=config_name,
                               changes_count=len(changes))
                    
                    # Notify callbacks
                    if config_name in self._update_callbacks:
                        for callback in self._update_callbacks[config_name]:
                            try:
                                await callback(new_config, changes)
                            except Exception as e:
                                logger.error(f"Update callback failed", 
                                           config_name=config_name, 
                                           error=str(e))
                
                # Wait for next poll
                await asyncio.sleep(self.poll_interval)
                
            except asyncio.CancelledError:
                logger.info(f"Polling cancelled", config_name=config_name)
                break
            except Exception as e:
                logger.error(f"Polling error", 
                           config_name=config_name, 
                           error=str(e))
                await asyncio.sleep(self.poll_interval)

async def polling_config_example():
    """Example of automatic configuration polling."""
    
    manager = PollingConfigManager(poll_interval=30.0)
    
    # Define loader function
    async def load_remote_config():
        # Simulate remote config loading
        loader = HTTPConfigLoader(base_url="https://config.example.com")
        config_data = await loader.load("/api/config/myapp.json")
        return RemoteAppConfig(**config_data)
    
    # Register update callback
    async def on_config_updated(new_config, changes):
        print(f"Configuration updated!")
        for field_name, (old_val, new_val) in changes.items():
            print(f"  {field_name}: {old_val} -> {new_val}")
    
    manager.on_update("app", on_config_updated)
    
    # Start polling
    await manager.start_polling("app", load_remote_config)
    
    try:
        # Keep running
        await asyncio.sleep(300)  # Run for 5 minutes
    finally:
        await manager.stop_polling("app")

# Usage
asyncio.run(polling_config_example())
```

## Circuit Breaker Pattern

### Resilient Remote Loading

```python
import asyncio
import time
from enum import Enum
from typing import Optional
from provide.foundation.config import BaseConfig
from provide.foundation import get_logger

logger = get_logger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Failing, reject requests
    HALF_OPEN = "half_open"  # Test if service recovered

class CircuitBreaker:
    """Circuit breaker for remote configuration loading."""
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: float = 60.0,
                 expected_exception: type = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker moving to HALF_OPEN")
            else:
                raise Exception(f"Circuit breaker OPEN - failing fast")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
            
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        return (
            self.last_failure_time is not None and
            time.time() - self.last_failure_time >= self.recovery_timeout
        )
    
    def _on_success(self):
        """Handle successful operation."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        logger.debug("Circuit breaker SUCCESS - state CLOSED")
    
    def _on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker OPENED after {self.failure_count} failures")

class ResilientConfigLoader:
    """Configuration loader with circuit breaker and fallback."""
    
    def __init__(self, 
                 primary_loader: Callable,
                 fallback_config: Optional[BaseConfig] = None):
        self.primary_loader = primary_loader
        self.fallback_config = fallback_config
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=120.0
        )
    
    async def load_config(self) -> BaseConfig:
        """Load configuration with resilience patterns."""
        
        try:
            # Try primary loader with circuit breaker
            config = await self.circuit_breaker.call(self.primary_loader)
            
            logger.info("Configuration loaded from primary source")
            return config
            
        except Exception as e:
            logger.error(f"Primary config loading failed", error=str(e))
            
            if self.fallback_config:
                logger.warning("Using fallback configuration")
                return self.fallback_config
            
            # No fallback available
            logger.error("No fallback configuration available")
            raise

async def resilient_config_example():
    """Example of resilient remote configuration loading."""
    
    # Define fallback configuration
    fallback_config = RemoteAppConfig(
        api_url="http://localhost:8000",
        timeout_seconds=30,
        max_retries=3,
        enable_caching=True,
        debug_mode=False
    )
    
    # Define primary loader (may fail)
    async def primary_loader():
        # Simulate occasional failures
        import random
        if random.random() < 0.3:  # 30% failure rate
            raise ConnectionError("Remote config server unavailable")
        
        # Simulate successful load
        return RemoteAppConfig(
            api_url="https://api.production.com",
            timeout_seconds=60,
            max_retries=5,
            enable_caching=True,
            debug_mode=False
        )
    
    # Create resilient loader
    loader = ResilientConfigLoader(
        primary_loader=primary_loader,
        fallback_config=fallback_config
    )
    
    # Load configuration with resilience
    for attempt in range(10):
        try:
            config = await loader.load_config()
            print(f"Attempt {attempt + 1}: Loaded config from {config.api_url}")
            
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to load config - {e}")
        
        await asyncio.sleep(1)

# Usage
asyncio.run(resilient_config_example())
```

## Caching Strategies

### Configuration Caching

```python
import asyncio
import time
import hashlib
from typing import Optional, Any
from provide.foundation.config import BaseConfig
from provide.foundation import get_logger

logger = get_logger(__name__)

class ConfigCache:
    """Cache for remote configuration data."""
    
    def __init__(self, default_ttl: float = 300.0):
        self.default_ttl = default_ttl
        self._cache: dict[str, dict] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached configuration."""
        
        if key not in self._cache:
            return None
        
        cache_entry = self._cache[key]
        
        # Check if expired
        if time.time() > cache_entry["expires_at"]:
            del self._cache[key]
            logger.debug(f"Cache entry expired", cache_key=key)
            return None
        
        logger.debug(f"Cache hit", cache_key=key)
        return cache_entry["data"]
    
    def set(self, key: str, data: Any, ttl: Optional[float] = None):
        """Set cached configuration."""
        
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl
        
        self._cache[key] = {
            "data": data,
            "expires_at": expires_at,
            "created_at": time.time()
        }
        
        logger.debug(f"Cache set", cache_key=key, ttl=ttl)
    
    def invalidate(self, key: str):
        """Invalidate cached entry."""
        
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache invalidated", cache_key=key)
    
    def clear(self):
        """Clear all cached entries."""
        
        self._cache.clear()
        logger.debug("Cache cleared")

class CachedRemoteLoader:
    """Remote configuration loader with caching."""
    
    def __init__(self, 
                 loader_func: Callable,
                 cache_ttl: float = 300.0):
        self.loader_func = loader_func
        self.cache = ConfigCache(default_ttl=cache_ttl)
    
    async def load(self, cache_key: str) -> BaseConfig:
        """Load configuration with caching."""
        
        # Try cache first
        cached_config = self.cache.get(cache_key)
        if cached_config:
            return cached_config
        
        # Load from remote source
        logger.info(f"Loading fresh configuration", cache_key=cache_key)
        
        try:
            config = await self.loader_func()
            
            # Cache the result
            self.cache.set(cache_key, config)
            
            return config
            
        except Exception as e:
            logger.error(f"Failed to load configuration", 
                        cache_key=cache_key, 
                        error=str(e))
            raise
    
    def invalidate_cache(self, cache_key: str):
        """Force cache invalidation."""
        
        self.cache.invalidate(cache_key)
        logger.info(f"Cache invalidated", cache_key=cache_key)

async def cached_config_example():
    """Example of cached remote configuration loading."""
    
    # Define remote loader
    async def load_remote_config():
        logger.info("Fetching configuration from remote source")
        # Simulate network delay
        await asyncio.sleep(2)
        
        return RemoteAppConfig(
            api_url="https://api.example.com",
            timeout_seconds=30,
            max_retries=3,
            enable_caching=True,
            debug_mode=False
        )
    
    # Create cached loader
    cached_loader = CachedRemoteLoader(
        loader_func=load_remote_config,
        cache_ttl=60.0  # 1 minute cache
    )
    
    # Load configuration multiple times
    for i in range(5):
        start_time = time.time()
        
        config = await cached_loader.load("myapp_config")
        
        duration = time.time() - start_time
        print(f"Load {i + 1}: {duration:.3f}s - {config.api_url}")
        
        await asyncio.sleep(0.5)

# Usage
asyncio.run(cached_config_example())
```