# Web Framework Integration

Integration patterns for web frameworks and HTTP applications.

### FastAPI Integration

```python
import time
import uuid
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware

from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Setup telemetry for web application
def setup_web_logging():
    """Configure logging for web application."""
    config = TelemetryConfig(
        service_name="my-web-api",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",  # JSON for structured logs
            das_emoji_prefix_enabled=False,  # Disable emoji in production
            module_levels={
                "uvicorn.access": "WARNING",  # Reduce uvicorn noise
                "httpx": "WARNING",
                "fastapi": "INFO"
            }
        )
    )
    setup_telemetry(config)

setup_web_logging()

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that adds request context to all log messages."""
    
    def __init__(self, app, logger_name: str = "web.middleware"):
        super().__init__(app)
        self.logger = get_logger(logger_name)
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Start timing
        start_time = time.time()
        
        # Log request start
        self.logger.info("Request started",
            domain="web",
            action="request",
            status="started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent", "unknown")
        )
        
        # Store request context for use in endpoints
        request.state.request_id = request_id
        request.state.start_time = start_time
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Determine status category
            if response.status_code < 300:
                status = "success"
            elif response.status_code < 400:
                status = "redirect"  
            elif response.status_code < 500:
                status = "client_error"
            else:
                status = "server_error"
            
            # Log successful completion
            self.logger.info("Request completed",
                domain="web",
                action="request", 
                status=status,
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
                response_size=response.headers.get("content-length", "unknown")
            )
            
            return response
            
        except Exception as e:
            # Calculate duration for failed requests
            duration = time.time() - start_time
            
            # Log error
            self.logger.error("Request failed",
                domain="web",
                action="request",
                status="error", 
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                duration_ms=round(duration * 1000, 2),
                error_type=type(e).__name__,
                error_message=str(e)
            )
            
            raise

# Create FastAPI app with logging
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with logging."""
    logger = get_logger("web.app")
    
    logger.info("Application starting",
        domain="web",
        action="startup", 
        status="started"
    )
    
    yield
    
    logger.info("Application shutting down",
        domain="web", 
        action="shutdown",
        status="started"
    )

app = FastAPI(
    title="My API",
    lifespan=lifespan
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Helper function for endpoint logging
def get_request_logger(request: Request) -> Any:
    """Get logger with request context."""
    logger = get_logger("web.endpoint")
    
    # Return bound logger with request context
    return logger.bind(
        request_id=getattr(request.state, "request_id", "unknown"),
        method=request.method,
        path=request.url.path
    )

# Example endpoints with logging
@app.get("/users/{user_id}")
async def get_user(user_id: int, request: Request):
    """Get user with comprehensive logging."""
    logger = get_request_logger(request)
    
    logger.info("Fetching user",
        domain="users",
        action="fetch", 
        status="started",
        user_id=user_id
    )
    
    try:
        # Simulate database lookup
        user_data = await fetch_user_from_db(user_id, logger)
        
        logger.info("User fetched successfully",
            domain="users",
            action="fetch",
            status="success", 
            user_id=user_id,
            user_type=user_data.get("type", "unknown")
        )
        
        return user_data
        
    except UserNotFoundError:
        logger.warning("User not found",
            domain="users", 
            action="fetch",
            status="not_found",
            user_id=user_id
        )
        raise HTTPException(status_code=404, detail="User not found")
        
    except Exception as e:
        logger.error("Failed to fetch user", 
            domain="users",
            action="fetch",
            status="error",
            user_id=user_id,
            error_type=type(e).__name__,
            error_message=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")

async def fetch_user_from_db(user_id: int, logger) -> dict[str, Any]:
    """Simulate database fetch with logging."""
    logger.debug("Querying database",
        domain="database",
        action="query",
        status="started", 
        table="users",
        query_type="select"
    )
    
    # Simulate database operation
    await asyncio.sleep(0.1)
    
    if user_id == 999:
        raise UserNotFoundError(f"User {user_id} not found")
    
    user_data = {
        "id": user_id,
        "name": f"User {user_id}",
        "type": "premium" if user_id % 2 == 0 else "standard"
    }
    
    logger.debug("Database query completed",
        domain="database", 
        action="query",
        status="success",
        table="users",
        result_count=1
    )
    
    return user_data

class UserNotFoundError(Exception):
    """User not found error."""
    pass
```

### Django Integration

```python
import logging
import time
import uuid
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Django settings integration
def configure_django_logging():
    """Configure Django with provide.foundation logging."""
    
    # Setup foundation telemetry
    config = TelemetryConfig(
        service_name="django-app",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",  # More readable in development
            module_levels={
                "django.request": "INFO",
                "django.db.backends": "WARNING",  # Reduce SQL noise
                "django.security": "INFO",
                "django.server": "WARNING"
            }
        )
    )
    setup_telemetry(config)

class FoundationLoggingMiddleware(MiddlewareMixin):
    """Django middleware for request logging with Foundation."""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = get_logger("django.request")
    
    def process_request(self, request: HttpRequest):
        """Process incoming request."""
        
        # Generate request ID
        request_id = str(uuid.uuid4())
        request._foundation_request_id = request_id
        request._foundation_start_time = time.time()
        
        # Log request start
        self.logger.info("Django request started",
            domain="web",
            action="request",
            status="started", 
            request_id=request_id,
            method=request.method,
            path=request.path,
            remote_addr=self._get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "unknown")[:200],
            content_type=request.content_type,
            content_length=request.META.get("CONTENT_LENGTH", 0)
        )
    
    def process_response(self, request: HttpRequest, response: HttpResponse):
        """Process response."""
        
        request_id = getattr(request, "_foundation_request_id", "unknown")
        start_time = getattr(request, "_foundation_start_time", time.time())
        duration = time.time() - start_time
        
        # Determine status category
        status_code = response.status_code
        if status_code < 300:
            status = "success"
        elif status_code < 400:
            status = "redirect"
        elif status_code < 500:
            status = "client_error"
        else:
            status = "server_error"
        
        # Log response
        self.logger.info("Django request completed",
            domain="web",
            action="request",
            status=status,
            request_id=request_id,
            method=request.method,
            path=request.path,
            status_code=status_code,
            duration_ms=round(duration * 1000, 2),
            response_size=len(response.content) if hasattr(response, 'content') else 0
        )
        
        return response
    
    def process_exception(self, request: HttpRequest, exception: Exception):
        """Process unhandled exceptions."""
        
        request_id = getattr(request, "_foundation_request_id", "unknown")
        start_time = getattr(request, "_foundation_start_time", time.time())
        duration = time.time() - start_time
        
        self.logger.error("Django request exception",
            domain="web",
            action="request", 
            status="error",
            request_id=request_id,
            method=request.method,
            path=request.path,
            duration_ms=round(duration * 1000, 2),
            exception_type=type(exception).__name__,
            exception_message=str(exception)
        )
    
    def _get_client_ip(self, request: HttpRequest) -> str:
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip

# Django view integration
from django.http import JsonResponse
from django.views import View

class BaseAPIView(View):
    """Base view with integrated logging."""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger(f"django.view.{self.__class__.__name__}")
    
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to add logging context."""
        
        request_id = getattr(request, "_foundation_request_id", "unknown")
        
        # Bind logger with request context
        self.request_logger = self.logger.bind(
            request_id=request_id,
            view_name=self.__class__.__name__,
            method=request.method
        )
        
        return super().dispatch(request, *args, **kwargs)

class UserAPIView(BaseAPIView):
    """Example API view with logging."""
    
    def get(self, request, user_id):
        """Get user endpoint."""
        
        self.request_logger.info("Fetching user",
            domain="users",
            action="fetch",
            status="started",
            user_id=user_id
        )
        
        try:
            # Simulate user lookup
            user_data = self.get_user_from_db(user_id)
            
            self.request_logger.info("User fetched successfully",
                domain="users",
                action="fetch", 
                status="success",
                user_id=user_id,
                user_type=user_data.get("type", "unknown")
            )
            
            return JsonResponse(user_data)
            
        except User.DoesNotExist:
            self.request_logger.warning("User not found",
                domain="users",
                action="fetch",
                status="not_found", 
                user_id=user_id
            )
            return JsonResponse({"error": "User not found"}, status=404)
            
        except Exception as e:
            self.request_logger.error("Failed to fetch user",
                domain="users",
                action="fetch",
                status="error",
                user_id=user_id,
                exception_type=type(e).__name__, 
                exception_message=str(e)
            )
            return JsonResponse({"error": "Internal server error"}, status=500)
    
    def get_user_from_db(self, user_id):
        """Simulate database lookup."""
        self.request_logger.debug("Querying user database",
            domain="database",
            action="query", 
            status="started",
            table="auth_user",
            user_id=user_id
        )
        
        # Simulate database query
        if user_id == "999":
            from django.contrib.auth.models import User
            raise User.DoesNotExist()
        
        return {
            "id": user_id,
            "username": f"user{user_id}",
            "type": "premium"
        }

# Configure Django logging on startup
configure_django_logging()
```

