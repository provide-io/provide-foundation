# Integration Patterns

Common patterns for integrating provide.foundation logging with various frameworks and systems.

## Web Framework Integration

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

## Database Integration

### SQLAlchemy Integration

```python
import time
from typing import Any, Optional
from sqlalchemy import event, Engine
from sqlalchemy.engine import Connection
from sqlalchemy.pool import Pool

from provide.foundation import get_logger

class SQLAlchemyLoggingIntegration:
    """Comprehensive SQLAlchemy logging integration."""
    
    def __init__(self, logger_name: str = "database.sqlalchemy"):
        self.logger = get_logger(logger_name)
        self.query_times: dict[str, float] = {}
    
    def setup_engine_logging(self, engine: Engine):
        """Setup logging for SQLAlchemy engine events."""
        
        # Connection events
        event.listen(engine, "connect", self._on_connect)
        event.listen(engine, "checkout", self._on_checkout)
        event.listen(engine, "checkin", self._on_checkin)
        
        # Statement execution events  
        event.listen(engine, "before_cursor_execute", self._before_cursor_execute)
        event.listen(engine, "after_cursor_execute", self._after_cursor_execute)
        
        # Pool events
        if hasattr(engine.pool, 'size'):
            event.listen(engine.pool, "connect", self._on_pool_connect)
            event.listen(engine.pool, "checkout", self._on_pool_checkout)
            event.listen(engine.pool, "checkin", self._on_pool_checkin)
    
    def _on_connect(self, dbapi_connection, connection_record):
        """Handle new database connections."""
        self.logger.info("Database connection established",
            domain="database",
            action="connect",
            status="success",
            connection_id=id(dbapi_connection)
        )
    
    def _on_checkout(self, dbapi_connection, connection_record, connection_proxy):
        """Handle connection checkout from pool."""
        self.logger.debug("Connection checked out from pool",
            domain="database", 
            action="checkout",
            status="success",
            connection_id=id(dbapi_connection),
            pool_size=getattr(connection_record.info, 'pool_size', 'unknown'),
            checked_out_connections=getattr(connection_record.info, 'checked_out', 'unknown')
        )
    
    def _on_checkin(self, dbapi_connection, connection_record):
        """Handle connection checkin to pool."""
        self.logger.debug("Connection returned to pool",
            domain="database",
            action="checkin", 
            status="success",
            connection_id=id(dbapi_connection)
        )
    
    def _before_cursor_execute(self, conn: Connection, cursor, statement: str, 
                             parameters, context, executemany: bool):
        """Log before SQL execution."""
        
        # Generate unique execution ID
        execution_id = f"{id(cursor)}_{time.time()}"
        
        # Store start time
        self.query_times[execution_id] = time.time()
        
        # Parse query type
        query_type = self._extract_query_type(statement)
        
        # Log query start
        self.logger.debug("SQL query starting",
            domain="database",
            action="query",
            status="started",
            execution_id=execution_id,
            query_type=query_type,
            statement=self._sanitize_statement(statement)[:500],  # Truncate long queries
            parameter_count=len(parameters) if parameters else 0,
            executemany=executemany
        )
        
        # Store execution context
        context.execution_id = execution_id
        context.query_type = query_type
    
    def _after_cursor_execute(self, conn: Connection, cursor, statement: str,
                            parameters, context, executemany: bool):
        """Log after SQL execution."""
        
        execution_id = getattr(context, 'execution_id', 'unknown')
        query_type = getattr(context, 'query_type', 'unknown')
        
        # Calculate duration
        start_time = self.query_times.pop(execution_id, time.time())
        duration = time.time() - start_time
        
        # Get row count if available
        try:
            row_count = cursor.rowcount if cursor.rowcount >= 0 else None
        except:
            row_count = None
        
        # Determine if query was slow
        is_slow = duration > 1.0  # Configurable threshold
        log_level = "warning" if is_slow else "debug"
        
        # Log query completion
        getattr(self.logger, log_level)("SQL query completed",
            domain="database",
            action="query",
            status="success",
            execution_id=execution_id,
            query_type=query_type,
            duration_ms=round(duration * 1000, 2),
            row_count=row_count,
            is_slow=is_slow,
            executemany=executemany
        )
    
    def _on_pool_connect(self, dbapi_connection, connection_record):
        """Handle pool connection events."""
        self.logger.debug("Pool connection created",
            domain="database",
            action="pool_connect",
            status="success",
            connection_id=id(dbapi_connection)
        )
    
    def _on_pool_checkout(self, dbapi_connection, connection_record, connection_proxy):
        """Handle pool checkout events."""
        pool = connection_record.pool
        
        self.logger.debug("Pool connection checkout", 
            domain="database",
            action="pool_checkout",
            status="success",
            connection_id=id(dbapi_connection),
            pool_size=pool.size(),
            checked_out=pool.checkedout(),
            overflow=pool.overflow(),
            checked_in=pool.checkedin()
        )
    
    def _on_pool_checkin(self, dbapi_connection, connection_record):
        """Handle pool checkin events."""
        self.logger.debug("Pool connection checkin",
            domain="database", 
            action="pool_checkin",
            status="success",
            connection_id=id(dbapi_connection)
        )
    
    def _extract_query_type(self, statement: str) -> str:
        """Extract query type from SQL statement."""
        statement_upper = statement.strip().upper()
        
        if statement_upper.startswith('SELECT'):
            return 'select'
        elif statement_upper.startswith('INSERT'):
            return 'insert'
        elif statement_upper.startswith('UPDATE'):
            return 'update'
        elif statement_upper.startswith('DELETE'):
            return 'delete'
        elif statement_upper.startswith('CREATE'):
            return 'create'
        elif statement_upper.startswith('DROP'):
            return 'drop'
        elif statement_upper.startswith('ALTER'):
            return 'alter'
        else:
            return 'other'
    
    def _sanitize_statement(self, statement: str) -> str:
        """Sanitize SQL statement for logging."""
        # Remove excessive whitespace
        import re
        statement = re.sub(r'\\s+', ' ', statement.strip())
        
        # Could add more sanitization here
        # (e.g., mask sensitive data in queries)
        
        return statement

# Usage example
def setup_database_logging():
    """Setup database with comprehensive logging."""
    from sqlalchemy import create_engine
    
    # Create engine
    engine = create_engine(
        "postgresql://user:pass@localhost/mydb",
        pool_size=10,
        pool_pre_ping=True,
        echo=False  # Disable SQLAlchemy's built-in logging
    )
    
    # Setup Foundation logging
    db_logging = SQLAlchemyLoggingIntegration()
    db_logging.setup_engine_logging(engine)
    
    return engine
```

## Message Queue Integration

### Celery Integration

```python
import time
from typing import Any, Optional
from celery import Celery
from celery.signals import (
    task_prerun, task_postrun, task_failure, 
    worker_ready, worker_shutdown
)

from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Setup telemetry for Celery
def setup_celery_logging():
    """Configure logging for Celery workers."""
    config = TelemetryConfig(
        service_name="celery-worker",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            module_levels={
                "celery.worker": "INFO",
                "celery.task": "INFO", 
                "celery.beat": "INFO",
                "billiard": "WARNING",
                "kombu": "WARNING"
            }
        )
    )
    setup_telemetry(config)

setup_celery_logging()

# Create Celery app
app = Celery('myapp')
app.config_from_object('celeryconfig')

class CeleryTaskLogger:
    """Helper for task-specific logging."""
    
    def __init__(self, task_name: str):
        self.logger = get_logger(f"celery.task.{task_name}")
        self.task_name = task_name
    
    def log_task_start(self, task_id: str, args: tuple, kwargs: dict):
        """Log task execution start."""
        self.logger.info("Task started",
            domain="celery",
            action="task", 
            status="started",
            task_id=task_id,
            task_name=self.task_name,
            args_count=len(args),
            kwargs_count=len(kwargs),
            args_preview=str(args)[:200] if args else None,
            kwargs_preview=str(kwargs)[:200] if kwargs else None
        )
    
    def log_task_success(self, task_id: str, result: Any, duration: float):
        """Log successful task completion."""
        self.logger.info("Task completed successfully",
            domain="celery",
            action="task",
            status="success", 
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            result_type=type(result).__name__,
            result_preview=str(result)[:200] if result is not None else None
        )
    
    def log_task_failure(self, task_id: str, error: Exception, traceback: str, duration: float):
        """Log task failure."""
        self.logger.error("Task failed",
            domain="celery", 
            action="task",
            status="error",
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            error_type=type(error).__name__,
            error_message=str(error),
            traceback=traceback[:1000]  # Truncate long tracebacks
        )
    
    def log_task_retry(self, task_id: str, error: Exception, retry_count: int, eta: Optional[str]):
        """Log task retry."""
        self.logger.warning("Task retry scheduled",
            domain="celery",
            action="task",
            status="retry",
            task_id=task_id,
            task_name=self.task_name,
            retry_count=retry_count,
            error_type=type(error).__name__,
            error_message=str(error),
            retry_eta=eta
        )

# Global task tracking
task_start_times: dict[str, float] = {}
task_loggers: dict[str, CeleryTaskLogger] = {}

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Handle task pre-run signal."""
    task_start_times[task_id] = time.time()
    
    # Get or create task logger
    task_name = task.name if task else sender
    if task_name not in task_loggers:
        task_loggers[task_name] = CeleryTaskLogger(task_name)
    
    # Log task start
    task_loggers[task_name].log_task_start(task_id, args or (), kwargs or {})

@task_postrun.connect  
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, 
                        kwargs=None, retval=None, state=None, **kwds):
    """Handle task post-run signal."""
    start_time = task_start_times.pop(task_id, time.time())
    duration = time.time() - start_time
    
    task_name = task.name if task else sender
    if task_name in task_loggers:
        if state == 'SUCCESS':
            task_loggers[task_name].log_task_success(task_id, retval, duration)
        # Note: Failures are handled by task_failure signal

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwds):
    """Handle task failure signal."""
    start_time = task_start_times.pop(task_id, time.time())
    duration = time.time() - start_time
    
    task_name = sender.name if sender else "unknown"
    if task_name not in task_loggers:
        task_loggers[task_name] = CeleryTaskLogger(task_name)
    
    task_loggers[task_name].log_task_failure(
        task_id, exception, str(traceback), duration
    )

@worker_ready.connect
def worker_ready_handler(sender=None, **kwargs):
    """Handle worker ready signal."""
    logger = get_logger("celery.worker")
    logger.info("Celery worker ready",
        domain="celery",
        action="worker", 
        status="ready",
        hostname=sender.hostname if sender else "unknown"
    )

@worker_shutdown.connect
def worker_shutdown_handler(sender=None, **kwargs):
    """Handle worker shutdown signal."""
    logger = get_logger("celery.worker")  
    logger.info("Celery worker shutting down",
        domain="celery",
        action="worker",
        status="shutdown",
        hostname=sender.hostname if sender else "unknown"
    )

# Example task with comprehensive logging
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_user_data(self, user_id: int, data: dict):
    """Example Celery task with integrated logging."""
    
    # Task-specific logger (automatically configured by signals)
    logger = get_logger(f"celery.task.{self.name}")
    
    try:
        # Log processing steps
        logger.info("Processing user data",
            domain="users",
            action="process",
            status="started", 
            user_id=user_id,
            data_size=len(data),
            task_id=self.request.id
        )
        
        # Simulate processing steps
        validation_result = validate_user_data(user_id, data, logger)
        
        if not validation_result.valid:
            logger.warning("User data validation failed",
                domain="users",
                action="validate",
                status="failed",
                user_id=user_id,
                validation_errors=validation_result.errors
            )
            return {"success": False, "errors": validation_result.errors}
        
        # Process the data
        result = perform_data_processing(user_id, data, logger)
        
        logger.info("User data processed successfully",
            domain="users", 
            action="process",
            status="success",
            user_id=user_id,
            processed_records=result.get("record_count", 0)
        )
        
        return {"success": True, "result": result}
        
    except TemporaryProcessingError as e:
        # Retry for temporary errors
        logger.warning("Temporary processing error, retrying",
            domain="users",
            action="process", 
            status="retry",
            user_id=user_id,
            error_message=str(e),
            retry_count=self.request.retries,
            max_retries=self.max_retries
        )
        
        task_loggers[self.name].log_task_retry(
            self.request.id, e, self.request.retries, 
            str(self.retry(countdown=60))
        )
        
        raise self.retry(exc=e, countdown=60)
        
    except Exception as e:
        # Log and re-raise for permanent errors
        logger.error("Permanent processing error",
            domain="users",
            action="process",
            status="error", 
            user_id=user_id,
            error_type=type(e).__name__,
            error_message=str(e)
        )
        raise

def validate_user_data(user_id: int, data: dict, logger) -> Any:
    """Validate user data with logging."""
    logger.debug("Validating user data",
        domain="users",
        action="validate",
        status="started",
        user_id=user_id
    )
    
    # Mock validation
    class ValidationResult:
        def __init__(self, valid: bool, errors: list = None):
            self.valid = valid
            self.errors = errors or []
    
    return ValidationResult(True, [])

def perform_data_processing(user_id: int, data: dict, logger) -> dict:
    """Process user data with logging."""
    logger.debug("Processing user data",
        domain="users",
        action="transform",
        status="started", 
        user_id=user_id
    )
    
    # Mock processing
    return {"record_count": 42, "status": "processed"}

class TemporaryProcessingError(Exception):
    """Temporary processing error that should trigger retry."""
    pass
```

## Async Application Patterns

### AsyncIO Integration

```python
import asyncio
import signal
import sys
from contextlib import AsyncExitStack
from typing import Any, Optional

from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

class AsyncApplicationBase:
    """Base class for async applications with comprehensive logging."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"app.{name}")
        self.exit_stack = AsyncExitStack()
        self._shutdown_event = asyncio.Event()
        self._tasks: set[asyncio.Task] = set()
        
        # Setup telemetry
        self._setup_logging()
        
        # Setup signal handlers
        self._setup_signal_handlers()
    
    def _setup_logging(self):
        """Setup application logging."""
        config = TelemetryConfig(
            service_name=self.name,
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="key_value",
                das_emoji_prefix_enabled=True,
                module_levels={
                    f"app.{self.name}": "DEBUG",
                    "asyncio": "WARNING"
                }
            )
        )
        setup_telemetry(config)
    
    def _setup_signal_handlers(self):
        """Setup graceful shutdown signal handlers."""
        if sys.platform != "win32":
            loop = asyncio.get_event_loop()
            
            for sig in (signal.SIGTERM, signal.SIGINT):
                loop.add_signal_handler(
                    sig, 
                    lambda s=sig: asyncio.create_task(self._signal_handler(s))
                )
    
    async def _signal_handler(self, sig):
        """Handle shutdown signals."""
        self.logger.info("Shutdown signal received",
            domain="app",
            action="shutdown",
            status="started",
            signal=sig.name
        )
        self._shutdown_event.set()
    
    async def start(self):
        """Start the application."""
        self.logger.info("Application starting",
            domain="app", 
            action="startup",
            status="started",
            app_name=self.name
        )
        
        try:
            async with self.exit_stack:
                # Initialize application components
                await self.initialize()
                
                # Start background tasks
                await self.start_background_tasks()
                
                self.logger.info("Application started successfully",
                    domain="app",
                    action="startup", 
                    status="success",
                    app_name=self.name,
                    active_tasks=len(self._tasks)
                )
                
                # Wait for shutdown signal
                await self._shutdown_event.wait()
                
                self.logger.info("Application shutdown initiated",
                    domain="app",
                    action="shutdown",
                    status="started", 
                    app_name=self.name
                )
                
        except Exception as e:
            self.logger.error("Application startup failed",
                domain="app",
                action="startup",
                status="error",
                app_name=self.name,
                error_type=type(e).__name__,
                error_message=str(e)
            )
            raise
        finally:
            await self.cleanup()
    
    async def initialize(self):
        """Initialize application components. Override in subclasses."""
        pass
    
    async def start_background_tasks(self):
        """Start background tasks. Override in subclasses."""
        pass
    
    async def cleanup(self):
        """Cleanup application resources."""
        self.logger.info("Application cleanup started",
            domain="app",
            action="cleanup",
            status="started",
            app_name=self.name
        )
        
        # Cancel all background tasks
        for task in self._tasks:
            if not task.done():
                task.cancel()
        
        # Wait for tasks to complete
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        
        self.logger.info("Application cleanup completed",
            domain="app", 
            action="cleanup",
            status="success",
            app_name=self.name
        )
    
    def create_task(self, coro, *, name: Optional[str] = None) -> asyncio.Task:
        """Create and track a background task."""
        task = asyncio.create_task(coro, name=name)
        self._tasks.add(task)
        
        # Remove completed tasks
        def remove_task(t):
            self._tasks.discard(t)
        
        task.add_done_callback(remove_task)
        
        return task

# Example application
class DataProcessorApp(AsyncApplicationBase):
    """Example async application with background processing."""
    
    async def initialize(self):
        """Initialize data processor components."""
        self.logger.info("Initializing data processor",
            domain="app",
            action="initialize",
            status="started"
        )
        
        # Initialize components (databases, queues, etc.)
        await self._init_database()
        await self._init_message_queue()
        
        self.logger.info("Data processor initialized",
            domain="app",
            action="initialize", 
            status="success"
        )
    
    async def start_background_tasks(self):
        """Start background processing tasks."""
        self.logger.info("Starting background tasks",
            domain="app",
            action="start_tasks",
            status="started"
        )
        
        # Start various background tasks
        self.create_task(self.data_processor_loop(), name="data_processor")
        self.create_task(self.health_check_loop(), name="health_check")
        self.create_task(self.metrics_reporter_loop(), name="metrics_reporter")
        
        self.logger.info("Background tasks started",
            domain="app",
            action="start_tasks",
            status="success",
            task_count=len(self._tasks)
        )
    
    async def _init_database(self):
        """Initialize database connection."""
        self.logger.debug("Initializing database connection",
            domain="database",
            action="connect",
            status="started"
        )
        
        # Mock database initialization
        await asyncio.sleep(0.1)
        
        self.logger.info("Database connection established",
            domain="database", 
            action="connect",
            status="success"
        )
    
    async def _init_message_queue(self):
        """Initialize message queue connection."""  
        self.logger.debug("Connecting to message queue",
            domain="queue",
            action="connect",
            status="started"
        )
        
        # Mock queue initialization
        await asyncio.sleep(0.1)
        
        self.logger.info("Message queue connected",
            domain="queue",
            action="connect", 
            status="success"
        )
    
    async def data_processor_loop(self):
        """Main data processing loop."""
        self.logger.info("Data processor loop started",
            domain="processor",
            action="start",
            status="started"
        )
        
        try:
            while not self._shutdown_event.is_set():
                try:
                    # Process batch of data
                    batch_size = await self.process_data_batch()
                    
                    if batch_size > 0:
                        self.logger.debug("Data batch processed",
                            domain="processor",
                            action="process",
                            status="success", 
                            batch_size=batch_size
                        )
                    
                    # Wait before next batch
                    await asyncio.sleep(1.0)
                    
                except Exception as e:
                    self.logger.error("Data processing error",
                        domain="processor",
                        action="process",
                        status="error",
                        error_type=type(e).__name__,
                        error_message=str(e)
                    )
                    await asyncio.sleep(5.0)  # Back off on error
                    
        except asyncio.CancelledError:
            self.logger.info("Data processor loop cancelled",
                domain="processor", 
                action="stop",
                status="cancelled"
            )
            raise
    
    async def health_check_loop(self):
        """Health check reporting loop."""
        while not self._shutdown_event.is_set():
            try:
                # Perform health checks
                health_status = await self.check_system_health()
                
                self.logger.info("Health check completed",
                    domain="health",
                    action="check",
                    status="success" if health_status else "warning",
                    healthy=health_status
                )
                
                await asyncio.sleep(30.0)  # Check every 30 seconds
                
            except asyncio.CancelledError:
                self.logger.info("Health check loop cancelled",
                    domain="health",
                    action="stop", 
                    status="cancelled"
                )
                raise
            except Exception as e:
                self.logger.error("Health check error",
                    domain="health",
                    action="check",
                    status="error",
                    error_type=type(e).__name__,
                    error_message=str(e)
                )
                await asyncio.sleep(10.0)
    
    async def metrics_reporter_loop(self):
        """Metrics reporting loop."""
        while not self._shutdown_event.is_set():
            try:
                # Collect and report metrics
                metrics = await self.collect_metrics()
                
                self.logger.info("Metrics reported",
                    domain="metrics",
                    action="report",
                    status="success",
                    **metrics
                )
                
                await asyncio.sleep(60.0)  # Report every minute
                
            except asyncio.CancelledError:
                self.logger.info("Metrics reporter cancelled",
                    domain="metrics", 
                    action="stop",
                    status="cancelled"
                )
                raise
            except Exception as e:
                self.logger.error("Metrics reporting error",
                    domain="metrics",
                    action="report",
                    status="error",
                    error_type=type(e).__name__,
                    error_message=str(e)
                )
                await asyncio.sleep(30.0)
    
    async def process_data_batch(self) -> int:
        """Process a batch of data."""
        # Mock data processing
        await asyncio.sleep(0.1)
        return 10  # Mock batch size
    
    async def check_system_health(self) -> bool:
        """Check system health."""
        # Mock health check
        return True
    
    async def collect_metrics(self) -> dict[str, Any]:
        """Collect system metrics."""
        # Mock metrics collection
        return {
            "active_tasks": len(self._tasks),
            "memory_usage_mb": 256,
            "cpu_usage_percent": 15.5
        }

# Run the application
async def main():
    app = DataProcessorApp("data-processor")
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
```