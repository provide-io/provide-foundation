# Configuration Polling & Updates

Automatic configuration updates with real-time change detection and callback mechanisms.

## Automatic Updates

### Polling Configuration Manager

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

## Change Detection Strategies

### Etag-Based Change Detection

```python
import aiohttp
from typing import Optional, tuple

class EtagHTTPLoader:
    """HTTP loader with Etag-based change detection."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._etag_cache: dict[str, str] = {}
    
    async def load_if_changed(self, endpoint: str) -> tuple[dict[str, Any] | None, bool]:
        """
        Load configuration only if it has changed.
        
        Returns:
            Tuple of (config_data, has_changed)
        """
        
        headers = {}
        
        # Add If-None-Match header if we have a cached etag
        cached_etag = self._etag_cache.get(endpoint)
        if cached_etag:
            headers["If-None-Match"] = cached_etag
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}", headers=headers) as response:
                
                if response.status == 304:
                    # Not modified
                    return None, False
                
                response.raise_for_status()
                
                # Update etag cache
                etag = response.headers.get("ETag")
                if etag:
                    self._etag_cache[endpoint] = etag
                
                config_data = await response.json()
                return config_data, True

class EtagPollingManager(PollingConfigManager):
    """Polling manager using Etag-based change detection."""
    
    async def _poll_loop(self, config_name: str, loader_func: Callable):
        """Enhanced poll loop with etag support."""
        
        while True:
            try:
                # Load configuration if changed
                config_data, has_changed = await loader_func()
                
                if has_changed and config_data:
                    # Create new config instance
                    new_config = RemoteAppConfig(**config_data)
                    
                    # Get current configuration
                    current_config = await self.get(config_name)
                    
                    if current_config != new_config:
                        changes = current_config.diff(new_config) if current_config else {}
                        
                        await self.set(config_name, new_config)
                        
                        logger.info(f"Configuration updated via etag", 
                                   config_name=config_name)
                        
                        # Notify callbacks
                        await self._notify_callbacks(config_name, new_config, changes)
                
                # Wait for next poll
                await asyncio.sleep(self.poll_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Etag polling error", 
                           config_name=config_name, 
                           error=str(e))
                await asyncio.sleep(self.poll_interval)

async def etag_polling_example():
    """Example of Etag-based polling."""
    
    loader = EtagHTTPLoader("https://config.example.com")
    manager = EtagPollingManager(poll_interval=10.0)  # More frequent polling
    
    async def load_with_etag():
        return await loader.load_if_changed("/api/config/myapp.json")
    
    await manager.start_polling("app", load_with_etag)
    
    # This will only fetch when the server indicates changes
    await asyncio.sleep(120)
    
    await manager.stop_polling("app")
```

### Hash-Based Change Detection

```python
import hashlib
from typing import Any

class HashBasedLoader:
    """Configuration loader with hash-based change detection."""
    
    def __init__(self, loader_func: Callable):
        self.loader_func = loader_func
        self._content_hashes: dict[str, str] = {}
    
    async def load_if_changed(self, config_key: str) -> tuple[dict[str, Any] | None, bool]:
        """Load configuration only if content hash has changed."""
        
        # Load raw configuration
        config_data = await self.loader_func()
        
        # Calculate content hash
        import json
        content_str = json.dumps(config_data, sort_keys=True)
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()
        
        # Check if hash has changed
        cached_hash = self._content_hashes.get(config_key)
        
        if cached_hash == content_hash:
            return None, False  # No change
        
        # Update hash cache
        self._content_hashes[config_key] = content_hash
        
        return config_data, True

async def hash_detection_example():
    """Example of hash-based change detection."""
    
    async def load_raw_config():
        # Simulate loading from various sources
        loader = HTTPConfigLoader("https://config.example.com")
        return await loader.load("/api/config/myapp.json")
    
    hash_loader = HashBasedLoader(load_raw_config)
    
    # Check for changes
    for i in range(5):
        config_data, has_changed = await hash_loader.load_if_changed("myapp")
        
        if has_changed:
            print(f"Check {i + 1}: Configuration changed")
            config = RemoteAppConfig(**config_data)
            print(f"  New API URL: {config.api_url}")
        else:
            print(f"Check {i + 1}: No changes detected")
        
        await asyncio.sleep(5)
```

## Webhook-Based Updates

### Configuration Webhook Server

```python
from aiohttp import web
import asyncio
from typing import Callable

class ConfigWebhookServer:
    """HTTP server to receive configuration update webhooks."""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.app = web.Application()
        self.app.router.add_post('/webhook/config', self.handle_config_webhook)
        self._update_callbacks: dict[str, list[Callable]] = {}
        self.server = None
    
    async def start(self):
        """Start the webhook server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        
        print(f"Webhook server listening on port {self.port}")
    
    def on_config_update(self, config_name: str, callback: Callable):
        """Register callback for configuration updates."""
        if config_name not in self._update_callbacks:
            self._update_callbacks[config_name] = []
        
        self._update_callbacks[config_name].append(callback)
    
    async def handle_config_webhook(self, request):
        """Handle incoming configuration update webhook."""
        
        try:
            payload = await request.json()
            
            config_name = payload.get('config_name')
            config_data = payload.get('config_data')
            
            if not config_name or not config_data:
                return web.Response(text="Missing required fields", status=400)
            
            # Notify registered callbacks
            if config_name in self._update_callbacks:
                for callback in self._update_callbacks[config_name]:
                    try:
                        await callback(config_name, config_data)
                    except Exception as e:
                        logger.error(f"Webhook callback failed", 
                                   config_name=config_name, 
                                   error=str(e))
            
            return web.Response(text="OK", status=200)
            
        except Exception as e:
            logger.error(f"Webhook processing error", error=str(e))
            return web.Response(text="Internal error", status=500)

class WebhookConfigManager(ConfigManager):
    """Configuration manager with webhook support."""
    
    def __init__(self):
        super().__init__()
        self.webhook_server = ConfigWebhookServer()
    
    async def start_webhook_listener(self):
        """Start listening for webhook updates."""
        await self.webhook_server.start()
        
        # Register webhook callback
        self.webhook_server.on_config_update("*", self._handle_webhook_update)
    
    async def _handle_webhook_update(self, config_name: str, config_data: dict):
        """Handle configuration update from webhook."""
        
        logger.info(f"Received webhook update", config_name=config_name)
        
        # Create configuration instance
        config = RemoteAppConfig(**config_data)
        
        # Get current configuration for comparison
        current_config = await self.get(config_name)
        
        # Update configuration
        await self.set(config_name, config)
        
        # Log changes
        if current_config:
            changes = current_config.diff(config)
            if changes:
                logger.info(f"Configuration changes from webhook",
                           config_name=config_name,
                           changes=changes)

async def webhook_config_example():
    """Example of webhook-based configuration updates."""
    
    manager = WebhookConfigManager()
    
    # Start webhook listener
    await manager.start_webhook_listener()
    
    # The server will now receive POST requests at /webhook/config
    # Example payload:
    # {
    #   "config_name": "myapp",
    #   "config_data": {
    #     "api_url": "https://new-api.example.com",
    #     "timeout_seconds": 45,
    #     "debug_mode": true
    #   }
    # }
    
    # Keep server running
    try:
        await asyncio.sleep(3600)  # Run for 1 hour
    except KeyboardInterrupt:
        print("Shutting down webhook server")
```

## Advanced Polling Strategies

### Adaptive Polling Intervals

```python
class AdaptivePollingManager(PollingConfigManager):
    """Polling manager with adaptive intervals based on change frequency."""
    
    def __init__(self, 
                 base_interval: float = 60.0,
                 min_interval: float = 10.0,
                 max_interval: float = 300.0):
        super().__init__(base_interval)
        self.min_interval = min_interval
        self.max_interval = max_interval
        self._change_history: dict[str, list[float]] = {}
    
    async def _poll_loop(self, config_name: str, loader_func: Callable):
        """Poll loop with adaptive intervals."""
        
        current_interval = self.poll_interval
        
        while True:
            try:
                poll_start = asyncio.get_event_loop().time()
                
                # Load and check for changes
                new_config = await loader_func()
                current_config = await self.get(config_name)
                
                has_changed = (current_config != new_config)
                
                if has_changed:
                    # Record change time
                    if config_name not in self._change_history:
                        self._change_history[config_name] = []
                    
                    self._change_history[config_name].append(poll_start)
                    
                    # Update configuration
                    await self.set(config_name, new_config)
                    
                    # Adapt polling interval based on recent changes
                    current_interval = self._adapt_interval(config_name)
                    
                    logger.info(f"Configuration changed, adapted interval to {current_interval}s",
                               config_name=config_name)
                
                # Wait for next poll
                await asyncio.sleep(current_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Adaptive polling error", 
                           config_name=config_name, 
                           error=str(e))
                await asyncio.sleep(current_interval)
    
    def _adapt_interval(self, config_name: str) -> float:
        """Adapt polling interval based on change history."""
        
        if config_name not in self._change_history:
            return self.poll_interval
        
        changes = self._change_history[config_name]
        current_time = asyncio.get_event_loop().time()
        
        # Keep only recent changes (last hour)
        recent_changes = [t for t in changes if current_time - t < 3600]
        self._change_history[config_name] = recent_changes
        
        if len(recent_changes) <= 1:
            # Few changes, increase interval
            return min(self.max_interval, self.poll_interval * 1.5)
        
        elif len(recent_changes) >= 5:
            # Frequent changes, decrease interval
            return max(self.min_interval, self.poll_interval * 0.5)
        
        else:
            # Moderate changes, keep current interval
            return self.poll_interval

async def adaptive_polling_example():
    """Example of adaptive polling intervals."""
    
    manager = AdaptivePollingManager(
        base_interval=60.0,
        min_interval=10.0,
        max_interval=300.0
    )
    
    async def load_config():
        # Simulate varying change frequency
        import random
        return RemoteAppConfig(
            api_url=f"https://api-v{random.randint(1, 3)}.example.com",
            timeout_seconds=30,
            max_retries=3,
            enable_caching=True,
            debug_mode=random.choice([True, False])
        )
    
    await manager.start_polling("adaptive", load_config)
    
    # Let it run and adapt
    await asyncio.sleep(600)  # 10 minutes
    
    await manager.stop_polling("adaptive")
```

## Best Practices

### 1. Implement Graceful Degradation

```python
# ✅ Good - Graceful degradation when polling fails
class ResilientPollingManager(PollingConfigManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._failure_counts: dict[str, int] = {}
        self._max_failures = 5
    
    async def _poll_loop(self, config_name: str, loader_func: Callable):
        while True:
            try:
                new_config = await loader_func()
                
                # Reset failure count on success
                self._failure_counts[config_name] = 0
                
                # Process config update...
                
            except Exception as e:
                failure_count = self._failure_counts.get(config_name, 0) + 1
                self._failure_counts[config_name] = failure_count
                
                if failure_count >= self._max_failures:
                    logger.error(f"Too many polling failures, using cached config")
                    # Continue with cached configuration
                
                # Exponential backoff
                backoff_delay = min(300, self.poll_interval * (2 ** failure_count))
                await asyncio.sleep(backoff_delay)

# ❌ Bad - No error handling
async def _poll_loop(self, config_name: str, loader_func: Callable):
    while True:
        new_config = await loader_func()  # Will crash on error
        await self.set(config_name, new_config)
        await asyncio.sleep(self.poll_interval)
```

### 2. Minimize Configuration Drift

```python
# ✅ Good - Validate configuration consistency
async def validate_config_consistency(config: BaseConfig) -> bool:
    """Validate that new configuration is consistent."""
    
    # Check required fields
    if not hasattr(config, 'api_url') or not config.api_url:
        logger.error("Configuration missing required api_url")
        return False
    
    # Validate URLs
    if not config.api_url.startswith(('http://', 'https://')):
        logger.error(f"Invalid API URL format: {config.api_url}")
        return False
    
    # Check timeout ranges
    if not (1 <= config.timeout_seconds <= 300):
        logger.error(f"Timeout out of range: {config.timeout_seconds}")
        return False
    
    return True

# Use validation in polling loop
if await validate_config_consistency(new_config):
    await self.set(config_name, new_config)
else:
    logger.warning("Rejecting invalid configuration update")
```

### 3. Rate Limit Configuration Updates

```python
# ✅ Good - Rate limit configuration updates
class RateLimitedPollingManager(PollingConfigManager):
    def __init__(self, *args, max_updates_per_minute: int = 10, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_updates_per_minute = max_updates_per_minute
        self._update_timestamps: dict[str, list[float]] = {}
    
    async def _apply_config_update(self, config_name: str, new_config):
        """Apply configuration update with rate limiting."""
        
        current_time = time.time()
        
        # Initialize or clean update history
        if config_name not in self._update_timestamps:
            self._update_timestamps[config_name] = []
        
        # Remove timestamps older than 1 minute
        cutoff_time = current_time - 60
        self._update_timestamps[config_name] = [
            t for t in self._update_timestamps[config_name] 
            if t > cutoff_time
        ]
        
        # Check rate limit
        if len(self._update_timestamps[config_name]) >= self.max_updates_per_minute:
            logger.warning(f"Rate limit exceeded for config updates", 
                          config_name=config_name)
            return False
        
        # Record this update
        self._update_timestamps[config_name].append(current_time)
        
        # Apply update
        await self.set(config_name, new_config)
        return True
```

## Next Steps

- [HTTP Loading](remote-http.md) - Load configuration from HTTP endpoints
- [Cloud Services](remote-cloud.md) - Integration with cloud services
- [Resilience Patterns](remote-resilience.md) - Circuit breakers and caching