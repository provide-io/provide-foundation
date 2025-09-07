# Integration Patterns

Advanced integration with frameworks and services, including FastAPI, Django, Celery, and custom configuration sources.

## FastAPI Integration

```python
from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import time
import uuid
from provide.foundation import get_logger, Context, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

class LoggingMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for request logging."""
    
    def __init__(self, app, logger_name: str = "api"):
        super().__init__(app)
        self.logger = get_logger(logger_name)
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Log request start
        self.logger.info("Request started",
                        request_id=request_id,
                        method=request.method,
                        url=str(request.url),
                        headers=dict(request.headers),
                        client_ip=request.client.host)
        
        try:
            # Process request
            response = await call_next(request)
            
            # Log successful response
            duration = time.time() - start_time
            self.logger.info("Request completed",
                           request_id=request_id,
                           status_code=response.status_code,
                           duration_seconds=duration)
            
            return response
            
        except Exception as e:
            # Log error
            duration = time.time() - start_time
            self.logger.error("Request failed",
                            request_id=request_id,
                            exception=str(e),
                            duration_seconds=duration)
            raise

# Setup FastAPI with logging
def create_app():
    # Configure logging
    config = TelemetryConfig(
        service_name="my-api",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json"
        )
    )
    setup_telemetry(config)
    
    # Create app with middleware
    app = FastAPI(title="My API")
    app.add_middleware(LoggingMiddleware)
    
    return app

app = create_app()
api_log = get_logger("api")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    api_log.info("Fetching user", user_id=user_id)
    
    # Simulate database lookup
    await asyncio.sleep(0.05)
    
    user = {"id": user_id, "name": f"User {user_id}"}
    api_log.info("User fetched successfully", user_id=user_id, user=user)
    
    return user
```

## Django Integration

```python
import logging
import time
from django.utils.deprecation import MiddlewareMixin
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

class DjangoFoundationLoggingMiddleware(MiddlewareMixin):
    """Django middleware for provide.foundation logging."""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = get_logger("django")
        
    def process_request(self, request):
        request.start_time = time.time()
        request.logger = self.logger.bind(
            request_id=getattr(request, 'id', 'unknown'),
            path=request.path,
            method=request.method
        )
        
        request.logger.info("Request started",
                          user=getattr(request.user, 'username', 'anonymous') if hasattr(request, 'user') else 'unknown',
                          ip=request.META.get('REMOTE_ADDR'))
        
    def process_response(self, request, response):
        if hasattr(request, 'start_time') and hasattr(request, 'logger'):
            duration = time.time() - request.start_time
            request.logger.info("Request completed",
                              status_code=response.status_code,
                              duration_seconds=duration)
        return response
    
    def process_exception(self, request, exception):
        if hasattr(request, 'logger'):
            request.logger.error("Request failed",
                                exception=str(exception),
                                exception_type=type(exception).__name__)

# Django settings integration
class FoundationLoggingConfig:
    """Django settings for provide.foundation."""
    
    @classmethod
    def setup(cls, debug=False, log_level="INFO"):
        """Setup provide.foundation for Django."""
        config = TelemetryConfig(
            service_name="django-app",
            debug=debug,
            logging=LoggingConfig(
                default_level=log_level,
                console_formatter="json" if not debug else "key_value",
                module_levels={
                    "django.db.backends": "WARNING",  # Reduce SQL query logs
                    "django.request": "INFO"
                }
            )
        )
        setup_telemetry(config)

# In Django views
from django.http import JsonResponse
from provide.foundation import get_logger

def user_view(request, user_id):
    log = get_logger("views.user")
    
    log.info("Fetching user", user_id=user_id)
    
    try:
        # Simulate user lookup
        user_data = {"id": user_id, "name": f"User {user_id}"}
        
        log.info("User retrieved successfully", user_id=user_id)
        return JsonResponse(user_data)
        
    except Exception as e:
        log.error("Failed to retrieve user", user_id=user_id, error=str(e))
        return JsonResponse({"error": "User not found"}, status=404)
```

## Celery Integration

```python
from celery import Celery
from celery.signals import task_prerun, task_postrun, task_failure
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
import time

# Configure logging for Celery
config = TelemetryConfig(
    service_name="celery-worker",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json"
    )
)
setup_telemetry(config)

app = Celery('myapp')
celery_log = get_logger("celery")

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Log task start."""
    celery_log.info("Task started",
                   task_id=task_id,
                   task_name=task.name,
                   args=args,
                   kwargs=kwargs)

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, 
                        retval=None, state=None, **kwds):
    """Log task completion."""
    celery_log.info("Task completed",
                   task_id=task_id,
                   task_name=task.name,
                   state=state,
                   result_type=type(retval).__name__)

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwds):
    """Log task failure."""
    celery_log.error("Task failed",
                    task_id=task_id,
                    task_name=sender.name,
                    exception=str(exception),
                    exception_type=type(exception).__name__)

@app.task
def process_data(data_id: int):
    """Example Celery task with logging."""
    task_log = get_logger("tasks.process_data")
    
    task_log.info("Processing data", data_id=data_id)
    
    try:
        # Simulate data processing
        time.sleep(2)
        
        result = {"data_id": data_id, "processed": True, "timestamp": time.time()}
        
        task_log.info("Data processing completed", 
                     data_id=data_id,
                     result=result)
        
        return result
        
    except Exception as e:
        task_log.error("Data processing failed", 
                      data_id=data_id,
                      error=str(e))
        raise
```

## Extension Points and Customization

### Custom Configuration Sources

```python
from provide.foundation import Context
from typing import Dict, Any
import requests
import json

class RemoteConfigSource:
    """Load configuration from remote service."""
    
    def __init__(self, config_url: str, api_key: str):
        self.config_url = config_url
        self.api_key = api_key
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from remote service."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(self.config_url, headers=headers)
        response.raise_for_status()
        return response.json()

class VaultConfigSource:
    """Load secrets from HashiCorp Vault."""
    
    def __init__(self, vault_url: str, vault_token: str):
        self.vault_url = vault_url
        self.vault_token = vault_token
    
    def load_secrets(self, path: str) -> Dict[str, Any]:
        """Load secrets from Vault."""
        headers = {"X-Vault-Token": self.vault_token}
        response = requests.get(f"{self.vault_url}/v1/{path}", headers=headers)
        response.raise_for_status()
        return response.json()["data"]

class AdvancedContext(Context):
    """Extended Context with remote configuration support."""
    
    def load_remote_config(self, config_source: RemoteConfigSource):
        """Load configuration from remote source."""
        try:
            config_data = config_source.load_config()
            
            # Update context with remote configuration
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    
        except Exception as e:
            # Log error but don't fail initialization
            print(f"Failed to load remote config: {e}")
    
    def load_vault_secrets(self, vault_source: VaultConfigSource, secret_path: str):
        """Load secrets from Vault."""
        try:
            secrets = vault_source.load_secrets(secret_path)
            
            # Apply secrets to context
            for key, value in secrets.items():
                setattr(self, f"secret_{key}", value)
                
        except Exception as e:
            print(f"Failed to load vault secrets: {e}")

# Usage
remote_source = RemoteConfigSource("https://config.example.com/api/config", "api-key")
vault_source = VaultConfigSource("https://vault.example.com", "vault-token")

ctx = AdvancedContext()
ctx.load_remote_config(remote_source)
ctx.load_vault_secrets(vault_source, "secret/myapp/config")
```