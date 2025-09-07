# Resilience Patterns

Circuit breakers, fallback mechanisms, and caching strategies for robust remote configuration loading.

## Circuit Breaker Pattern

### Basic Circuit Breaker

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

## Configuration Caching

### Basic Configuration Cache

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

### Multi-Level Caching

```python
from typing import Protocol
from abc import ABC, abstractmethod

class CacheBackend(Protocol):
    """Protocol for cache backends."""
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        ...
    
    async def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """Set value in cache."""
        ...
    
    async def delete(self, key: str):
        """Delete value from cache."""
        ...

class MemoryCache:
    """In-memory cache backend."""
    
    def __init__(self, default_ttl: float = 300.0):
        self.default_ttl = default_ttl
        self._cache: dict[str, dict] = {}
    
    async def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if time.time() > entry["expires_at"]:
            del self._cache[key]
            return None
        
        return entry["data"]
    
    async def set(self, key: str, value: Any, ttl: Optional[float] = None):
        ttl = ttl or self.default_ttl
        self._cache[key] = {
            "data": value,
            "expires_at": time.time() + ttl
        }
    
    async def delete(self, key: str):
        self._cache.pop(key, None)

class RedisCache:
    """Redis cache backend."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # In real implementation, would use aioredis
        self.redis_url = redis_url
    
    async def get(self, key: str) -> Optional[Any]:
        # Implementation would use Redis client
        import json
        # Placeholder implementation
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[float] = None):
        # Implementation would serialize and store in Redis
        pass
    
    async def delete(self, key: str):
        # Implementation would delete from Redis
        pass

class MultiLevelCache:
    """Multi-level cache with L1 (memory) and L2 (Redis) backends."""
    
    def __init__(self, l1_cache: CacheBackend, l2_cache: CacheBackend):
        self.l1_cache = l1_cache
        self.l2_cache = l2_cache
    
    async def get(self, key: str) -> Optional[Any]:
        """Get from L1, fallback to L2."""
        
        # Try L1 cache first
        value = await self.l1_cache.get(key)
        if value is not None:
            logger.debug(f"L1 cache hit", cache_key=key)
            return value
        
        # Try L2 cache
        value = await self.l2_cache.get(key)
        if value is not None:
            logger.debug(f"L2 cache hit", cache_key=key)
            
            # Store in L1 for future requests
            await self.l1_cache.set(key, value, ttl=60.0)  # Short L1 TTL
            
            return value
        
        logger.debug(f"Cache miss", cache_key=key)
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """Set in both L1 and L2 caches."""
        
        # Set in both caches
        await self.l1_cache.set(key, value, ttl=min(ttl or 300, 60))  # Short L1 TTL
        await self.l2_cache.set(key, value, ttl)  # Full TTL in L2
    
    async def delete(self, key: str):
        """Delete from both caches."""
        
        await self.l1_cache.delete(key)
        await self.l2_cache.delete(key)

async def multi_level_cache_example():
    """Example of multi-level caching."""
    
    # Create cache backends
    l1_cache = MemoryCache(default_ttl=60.0)    # 1 minute L1
    l2_cache = RedisCache()                      # Longer L2 TTL
    
    # Create multi-level cache
    cache = MultiLevelCache(l1_cache, l2_cache)
    
    # Create cached loader
    async def load_config():
        await asyncio.sleep(1)  # Simulate network delay
        return {"api_url": "https://api.example.com", "timeout": 30}
    
    cached_loader = CachedRemoteLoader(load_config, cache_ttl=300.0)
    cached_loader.cache = cache  # Use multi-level cache
    
    # Test cache performance
    for i in range(3):
        start = time.time()
        config = await cached_loader.load("test_config")
        duration = time.time() - start
        print(f"Load {i + 1}: {duration:.3f}s")
        
        await asyncio.sleep(0.1)
```

## Retry Strategies

### Exponential Backoff

```python
import asyncio
import random
from typing import Callable, Any

class RetryConfig:
    """Configuration for retry behavior."""
    
    def __init__(self,
                 max_attempts: int = 3,
                 initial_delay: float = 1.0,
                 max_delay: float = 60.0,
                 backoff_multiplier: float = 2.0,
                 jitter: bool = True):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_multiplier = backoff_multiplier
        self.jitter = jitter

async def retry_with_backoff(
    func: Callable,
    retry_config: RetryConfig,
    exception_types: tuple = (Exception,)
) -> Any:
    """Execute function with exponential backoff retry."""
    
    last_exception = None
    
    for attempt in range(retry_config.max_attempts):
        try:
            return await func()
            
        except exception_types as e:
            last_exception = e
            
            if attempt == retry_config.max_attempts - 1:
                # Last attempt, re-raise
                raise
            
            # Calculate delay with exponential backoff
            delay = retry_config.initial_delay * (
                retry_config.backoff_multiplier ** attempt
            )
            
            # Apply maximum delay limit
            delay = min(delay, retry_config.max_delay)
            
            # Add jitter to prevent thundering herd
            if retry_config.jitter:
                delay = delay * (0.5 + random.random() * 0.5)
            
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s",
                          error=str(e))
            
            await asyncio.sleep(delay)
    
    # Should never reach here, but just in case
    raise last_exception

class RetryingConfigLoader:
    """Configuration loader with retry logic."""
    
    def __init__(self, 
                 loader_func: Callable,
                 retry_config: RetryConfig = None):
        self.loader_func = loader_func
        self.retry_config = retry_config or RetryConfig()
    
    async def load(self) -> BaseConfig:
        """Load configuration with retry logic."""
        
        return await retry_with_backoff(
            self.loader_func,
            self.retry_config,
            exception_types=(ConnectionError, TimeoutError, aiohttp.ClientError)
        )

async def retry_example():
    """Example of configuration loading with retries."""
    
    failure_count = 0
    
    async def unreliable_loader():
        nonlocal failure_count
        failure_count += 1
        
        # Fail first 2 attempts
        if failure_count <= 2:
            raise ConnectionError(f"Connection failed (attempt {failure_count})")
        
        # Succeed on 3rd attempt
        return RemoteAppConfig(
            api_url="https://api.example.com",
            timeout_seconds=30,
            max_retries=3,
            enable_caching=True,
            debug_mode=False
        )
    
    # Create retrying loader
    retry_config = RetryConfig(
        max_attempts=5,
        initial_delay=1.0,
        backoff_multiplier=2.0,
        max_delay=30.0,
        jitter=True
    )
    
    loader = RetryingConfigLoader(unreliable_loader, retry_config)
    
    try:
        config = await loader.load()
        print(f"Successfully loaded config after {failure_count} attempts")
        print(f"API URL: {config.api_url}")
    
    except Exception as e:
        print(f"Failed to load config after all retry attempts: {e}")

# Usage
asyncio.run(retry_example())
```

## Comprehensive Resilience Strategy

### Combined Resilient Loader

```python
class ComprehensiveResilientLoader:
    """Configuration loader with comprehensive resilience patterns."""
    
    def __init__(self,
                 primary_loader: Callable,
                 fallback_config: Optional[BaseConfig] = None,
                 cache_ttl: float = 300.0,
                 retry_config: RetryConfig = None,
                 circuit_breaker_config: dict = None):
        
        self.primary_loader = primary_loader
        self.fallback_config = fallback_config
        
        # Setup caching
        self.cache = ConfigCache(default_ttl=cache_ttl)
        
        # Setup retry logic
        self.retry_config = retry_config or RetryConfig()
        
        # Setup circuit breaker
        cb_config = circuit_breaker_config or {}
        self.circuit_breaker = CircuitBreaker(**cb_config)
        
        # Performance metrics
        self.metrics = {
            "cache_hits": 0,
            "cache_misses": 0,
            "primary_loads": 0,
            "fallback_uses": 0,
            "circuit_breaker_opens": 0
        }
    
    async def load_config(self, cache_key: str = "default") -> BaseConfig:
        """Load configuration with comprehensive resilience."""
        
        # 1. Try cache first
        cached_config = self.cache.get(cache_key)
        if cached_config:
            self.metrics["cache_hits"] += 1
            logger.debug("Configuration loaded from cache")
            return cached_config
        
        self.metrics["cache_misses"] += 1
        
        try:
            # 2. Try primary loader with circuit breaker and retry
            config = await self._load_with_resilience()
            
            # Cache successful result
            self.cache.set(cache_key, config)
            self.metrics["primary_loads"] += 1
            
            logger.info("Configuration loaded from primary source")
            return config
            
        except Exception as e:
            logger.error(f"Primary configuration loading failed", error=str(e))
            
            # 3. Try fallback configuration
            if self.fallback_config:
                self.metrics["fallback_uses"] += 1
                logger.warning("Using fallback configuration")
                
                # Cache fallback for short duration
                self.cache.set(cache_key, self.fallback_config, ttl=60.0)
                
                return self.fallback_config
            
            # 4. No fallback available
            logger.error("No fallback configuration available")
            raise
    
    async def _load_with_resilience(self) -> BaseConfig:
        """Load with circuit breaker and retry protection."""
        
        async def protected_loader():
            return await self.circuit_breaker.call(self.primary_loader)
        
        try:
            return await retry_with_backoff(
                protected_loader,
                self.retry_config,
                exception_types=(ConnectionError, TimeoutError, Exception)
            )
        except Exception as e:
            if self.circuit_breaker.state == CircuitState.OPEN:
                self.metrics["circuit_breaker_opens"] += 1
            raise
    
    def get_metrics(self) -> dict:
        """Get performance metrics."""
        return self.metrics.copy()
    
    def reset_metrics(self):
        """Reset performance metrics."""
        for key in self.metrics:
            self.metrics[key] = 0

async def comprehensive_resilience_example():
    """Example of comprehensive resilience patterns."""
    
    failure_simulation = 0
    
    async def simulated_primary_loader():
        nonlocal failure_simulation
        failure_simulation += 1
        
        # Simulate various failure scenarios
        if failure_simulation % 10 == 0:
            raise TimeoutError("Request timeout")
        elif failure_simulation % 7 == 0:
            raise ConnectionError("Connection refused")
        elif failure_simulation % 15 == 0:
            await asyncio.sleep(5)  # Slow response
        
        return RemoteAppConfig(
            api_url=f"https://api-v{failure_simulation}.example.com",
            timeout_seconds=30,
            max_retries=3,
            enable_caching=True,
            debug_mode=False
        )
    
    # Create comprehensive resilient loader
    fallback = RemoteAppConfig(
        api_url="http://localhost:8000",
        timeout_seconds=15,
        max_retries=1,
        enable_caching=False,
        debug_mode=True
    )
    
    loader = ComprehensiveResilientLoader(
        primary_loader=simulated_primary_loader,
        fallback_config=fallback,
        cache_ttl=120.0,
        retry_config=RetryConfig(max_attempts=3, initial_delay=0.5),
        circuit_breaker_config={"failure_threshold": 3, "recovery_timeout": 30.0}
    )
    
    # Load configuration multiple times
    for i in range(20):
        try:
            start_time = time.time()
            config = await loader.load_config("test")
            duration = time.time() - start_time
            
            print(f"Load {i + 1}: {duration:.3f}s - {config.api_url}")
            
        except Exception as e:
            print(f"Load {i + 1}: Failed - {e}")
        
        await asyncio.sleep(2)
    
    # Show performance metrics
    metrics = loader.get_metrics()
    print("\nPerformance Metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")

# Usage
asyncio.run(comprehensive_resilience_example())
```

## Best Practices

### 1. Layer Resilience Patterns

```python
# ✅ Good - Multiple resilience layers
loader = ComprehensiveResilientLoader(
    primary_loader=authenticated_http_loader,
    fallback_config=local_fallback_config,
    cache_ttl=300.0,                    # Cache layer
    retry_config=RetryConfig(),         # Retry layer  
    circuit_breaker_config={}           # Circuit breaker layer
)

# ❌ Bad - Single point of failure
loader = SimpleHTTPLoader("https://config.example.com")
```

### 2. Configure Appropriate Timeouts

```python
# ✅ Good - Reasonable timeouts
retry_config = RetryConfig(
    max_attempts=3,
    initial_delay=1.0,
    max_delay=30.0,        # Reasonable maximum
    backoff_multiplier=2.0
)

# ❌ Bad - Excessive timeouts
retry_config = RetryConfig(
    max_attempts=10,       # Too many attempts
    max_delay=600.0,       # 10 minutes is too long
    initial_delay=0.1      # Too aggressive
)
```

### 3. Monitor and Alert on Resilience Events

```python
# ✅ Good - Proper monitoring
class MonitoredResilientLoader(ComprehensiveResilientLoader):
    async def _load_with_resilience(self):
        try:
            return await super()._load_with_resilience()
        except Exception as e:
            # Send alert for resilience pattern activation
            if self.circuit_breaker.state == CircuitState.OPEN:
                send_alert("Circuit breaker opened for config loading")
            
            if self.metrics["fallback_uses"] > 0:
                send_alert("Using fallback configuration")
            
            raise

# ❌ Bad - Silent failures
# No monitoring of resilience pattern usage
```

## Next Steps

- [HTTP Loading](remote-http.md) - Load configuration from HTTP endpoints
- [Cloud Services](remote-cloud.md) - Integration with cloud services
- [Polling & Updates](remote-polling.md) - Automatic configuration updates