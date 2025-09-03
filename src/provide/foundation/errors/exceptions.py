"""Core exception hierarchy for Foundation.

Provides a comprehensive set of exception classes with rich context support,
semantic logging integration, and diagnostic capabilities.
"""

from typing import Any


class FoundationError(Exception):
    """Base exception for all Foundation errors.
    
    Args:
        message: Human-readable error message.
        code: Optional error code for programmatic handling.
        context: Optional context dictionary with diagnostic data.
        cause: Optional underlying exception that caused this error.
        **extra_context: Additional key-value pairs added to context.
    
    Examples:
        >>> raise FoundationError("Operation failed")
        >>> raise FoundationError("Operation failed", code="OP_001")
        >>> raise FoundationError("Operation failed", user_id=123, retry_count=3)
    """
    
    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any
    ):
        self.message = message
        self.code = code or self._default_code()
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)
    
    def _default_code(self) -> str:
        """Return default error code for this exception type."""
        return "FOUNDATION_ERROR"
    
    def add_context(self, key: str, value: Any) -> "FoundationError":
        """Add context data to the error.
        
        Args:
            key: Context key (use dots for namespacing, e.g., 'aws.region').
            value: Context value.
            
        Returns:
            Self for method chaining.
        """
        self.context[key] = value
        return self
    
    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.
        
        Returns:
            Dictionary representation suitable for logging/serialization.
        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }
        
        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value
        
        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__
            
        return result


class ConfigurationError(FoundationError):
    """Raised when configuration is invalid or cannot be loaded.
    
    Args:
        message: Error message describing the configuration issue.
        config_key: Optional configuration key that caused the error.
        config_source: Optional source of the configuration (file, env, etc.).
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise ConfigurationError("Missing required config")
        >>> raise ConfigurationError("Invalid timeout", config_key="timeout")
    """
    
    def __init__(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_source: str | None = None,
        **kwargs: Any
    ):
        if config_key:
            kwargs.setdefault('context', {})['config.key'] = config_key
        if config_source:
            kwargs.setdefault('context', {})['config.source'] = config_source
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "CONFIG_ERROR"


class ValidationError(FoundationError):
    """Raised when data validation fails.
    
    Args:
        message: Validation error message.
        field: Optional field name that failed validation.
        value: Optional invalid value.
        rule: Optional validation rule that failed.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise ValidationError("Invalid email format")
        >>> raise ValidationError("Value out of range", field="age", value=-1)
    """
    
    def __init__(
        self, 
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        rule: str | None = None,
        **kwargs: Any
    ):
        if field:
            kwargs.setdefault('context', {})['validation.field'] = field
        if value is not None:
            kwargs.setdefault('context', {})['validation.value'] = str(value)
        if rule:
            kwargs.setdefault('context', {})['validation.rule'] = rule
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "VALIDATION_ERROR"


class RuntimeError(FoundationError):
    """Raised for runtime operational errors.
    
    Args:
        message: Error message describing the runtime issue.
        operation: Optional operation that failed.
        retry_possible: Whether the operation can be retried.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise RuntimeError("Process failed")
        >>> raise RuntimeError("Lock timeout", operation="acquire_lock", retry_possible=True)
    """
    
    def __init__(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any
    ):
        if operation:
            kwargs.setdefault('context', {})['runtime.operation'] = operation
        kwargs.setdefault('context', {})['runtime.retry_possible'] = retry_possible
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "RUNTIME_ERROR"


class IntegrationError(FoundationError):
    """Raised when external service integration fails.
    
    Args:
        message: Error message describing the integration failure.
        service: Optional service name that failed.
        endpoint: Optional endpoint that was called.
        status_code: Optional HTTP status code.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise IntegrationError("API call failed")
        >>> raise IntegrationError("Auth failed", service="github", status_code=401)
    """
    
    def __init__(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any
    ):
        if service:
            kwargs.setdefault('context', {})['integration.service'] = service
        if endpoint:
            kwargs.setdefault('context', {})['integration.endpoint'] = endpoint
        if status_code:
            kwargs.setdefault('context', {})['integration.status_code'] = status_code
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "INTEGRATION_ERROR"


class ResourceError(FoundationError):
    """Raised when resource operations fail.
    
    Args:
        message: Error message describing the resource issue.
        resource_type: Optional type of resource (file, network, etc.).
        resource_path: Optional path or identifier of the resource.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise ResourceError("File not found")
        >>> raise ResourceError("Permission denied", resource_type="file", resource_path="/etc/config")
    """
    
    def __init__(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any
    ):
        if resource_type:
            kwargs.setdefault('context', {})['resource.type'] = resource_type
        if resource_path:
            kwargs.setdefault('context', {})['resource.path'] = resource_path
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "RESOURCE_ERROR"


class NetworkError(IntegrationError):
    """Raised for network-related failures.
    
    Args:
        message: Error message describing the network issue.
        host: Optional hostname or IP address.
        port: Optional port number.
        **kwargs: Additional context passed to IntegrationError.
    
    Examples:
        >>> raise NetworkError("Connection refused")
        >>> raise NetworkError("DNS resolution failed", host="api.example.com")
    """
    
    def __init__(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any
    ):
        if host:
            kwargs.setdefault('context', {})['network.host'] = host
        if port:
            kwargs.setdefault('context', {})['network.port'] = port
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "NETWORK_ERROR"


class TimeoutError(IntegrationError):
    """Raised when operations exceed time limits.
    
    Args:
        message: Error message describing the timeout.
        timeout_seconds: Optional timeout limit in seconds.
        elapsed_seconds: Optional actual elapsed time.
        **kwargs: Additional context passed to IntegrationError.
    
    Examples:
        >>> raise TimeoutError("Request timed out")
        >>> raise TimeoutError("Operation exceeded limit", timeout_seconds=30, elapsed_seconds=31.5)
    """
    
    def __init__(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any
    ):
        if timeout_seconds is not None:
            kwargs.setdefault('context', {})['timeout.limit'] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault('context', {})['timeout.elapsed'] = elapsed_seconds
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "TIMEOUT_ERROR"


class ProcessError(RuntimeError):
    """Raised when process execution fails.
    
    Args:
        message: Error message describing the process failure.
        command: Optional command that was executed.
        returncode: Optional process return code.
        stdout: Optional captured stdout.
        stderr: Optional captured stderr.
        **kwargs: Additional context passed to RuntimeError.
    
    Examples:
        >>> raise ProcessError("Command failed")
        >>> raise ProcessError("Build failed", command="make", returncode=2)
    """
    
    def __init__(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        returncode: int | None = None,
        stdout: str | None = None,
        stderr: str | None = None,
        **kwargs: Any
    ):
        if command:
            cmd_str = " ".join(command) if isinstance(command, list) else command
            kwargs.setdefault('context', {})['process.command'] = cmd_str
        if returncode is not None:
            kwargs.setdefault('context', {})['process.returncode'] = returncode
        if stdout:
            kwargs.setdefault('context', {})['process.stdout'] = stdout
        if stderr:
            kwargs.setdefault('context', {})['process.stderr'] = stderr
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "PROCESS_ERROR"


class BuildError(ProcessError):
    """Raised when build operations fail.
    
    Args:
        message: Error message describing the build failure.
        target: Optional build target.
        stage: Optional build stage that failed.
        **kwargs: Additional context passed to ProcessError.
    
    Examples:
        >>> raise BuildError("Compilation failed")
        >>> raise BuildError("Test failed", target="test", stage="unit-tests")
    """
    
    def __init__(
        self,
        message: str,
        *,
        target: str | None = None,
        stage: str | None = None,
        **kwargs: Any
    ):
        if target:
            kwargs.setdefault('context', {})['build.target'] = target
        if stage:
            kwargs.setdefault('context', {})['build.stage'] = stage
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "BUILD_ERROR"


class AuthenticationError(FoundationError):
    """Raised when authentication fails.
    
    Args:
        message: Error message describing the authentication failure.
        auth_method: Optional authentication method used.
        realm: Optional authentication realm.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise AuthenticationError("Invalid credentials")
        >>> raise AuthenticationError("Token expired", auth_method="jwt")
    """
    
    def __init__(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any
    ):
        if auth_method:
            kwargs.setdefault('context', {})['auth.method'] = auth_method
        if realm:
            kwargs.setdefault('context', {})['auth.realm'] = realm
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "AUTH_ERROR"


class AuthorizationError(FoundationError):
    """Raised when authorization fails.
    
    Args:
        message: Error message describing the authorization failure.
        required_permission: Optional required permission.
        resource: Optional resource being accessed.
        actor: Optional actor (user/service) attempting access.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise AuthorizationError("Access denied")
        >>> raise AuthorizationError("Insufficient permissions", required_permission="admin")
    """
    
    def __init__(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any
    ):
        if required_permission:
            kwargs.setdefault('context', {})['authz.permission'] = required_permission
        if resource:
            kwargs.setdefault('context', {})['authz.resource'] = resource
        if actor:
            kwargs.setdefault('context', {})['authz.actor'] = actor
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "AUTHZ_ERROR"


class NotFoundError(FoundationError):
    """Raised when a requested resource cannot be found.
    
    Args:
        message: Error message describing what was not found.
        resource_type: Optional type of resource.
        resource_id: Optional resource identifier.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise NotFoundError("User not found")
        >>> raise NotFoundError("Entity missing", resource_type="user", resource_id="123")
    """
    
    def __init__(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any
    ):
        if resource_type:
            kwargs.setdefault('context', {})['notfound.type'] = resource_type
        if resource_id:
            kwargs.setdefault('context', {})['notfound.id'] = resource_id
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "NOT_FOUND_ERROR"


class AlreadyExistsError(FoundationError):
    """Raised when attempting to create a resource that already exists.
    
    Args:
        message: Error message describing the conflict.
        resource_type: Optional type of resource.
        resource_id: Optional resource identifier.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise AlreadyExistsError("User already registered")
        >>> raise AlreadyExistsError("Duplicate key", resource_type="user", resource_id="john@example.com")
    """
    
    def __init__(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any
    ):
        if resource_type:
            kwargs.setdefault('context', {})['exists.type'] = resource_type
        if resource_id:
            kwargs.setdefault('context', {})['exists.id'] = resource_id
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "ALREADY_EXISTS_ERROR"


class StateError(FoundationError):
    """Raised when an operation is invalid for the current state.
    
    Args:
        message: Error message describing the state issue.
        current_state: Optional current state.
        expected_state: Optional expected state.
        transition: Optional attempted transition.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise StateError("Invalid state transition")
        >>> raise StateError("Not ready", current_state="initializing", expected_state="ready")
    """
    
    def __init__(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any
    ):
        if current_state:
            kwargs.setdefault('context', {})['state.current'] = current_state
        if expected_state:
            kwargs.setdefault('context', {})['state.expected'] = expected_state
        if transition:
            kwargs.setdefault('context', {})['state.transition'] = transition
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "STATE_ERROR"


class ConcurrencyError(FoundationError):
    """Raised when concurrency conflicts occur.
    
    Args:
        message: Error message describing the concurrency issue.
        conflict_type: Optional type of conflict (lock, version, etc.).
        version_expected: Optional expected version.
        version_actual: Optional actual version.
        **kwargs: Additional context passed to FoundationError.
    
    Examples:
        >>> raise ConcurrencyError("Optimistic lock failure")
        >>> raise ConcurrencyError("Version mismatch", version_expected=1, version_actual=2)
    """
    
    def __init__(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any
    ):
        if conflict_type:
            kwargs.setdefault('context', {})['concurrency.type'] = conflict_type
        if version_expected is not None:
            kwargs.setdefault('context', {})['concurrency.version_expected'] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault('context', {})['concurrency.version_actual'] = str(version_actual)
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "CONCURRENCY_ERROR"