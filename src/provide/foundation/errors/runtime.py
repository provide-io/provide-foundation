"""Runtime and process execution exceptions."""

from typing import Any

from provide.foundation.errors.base import FoundationError


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
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "RUNTIME_ERROR"


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
        **kwargs: Any,
    ) -> None:
        # Store as attributes for compatibility
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

        # Also store in context for structured logging
        if command:
            cmd_str = " ".join(command) if isinstance(command, list) else command
            kwargs.setdefault("context", {})["process.command"] = cmd_str
        if returncode is not None:
            kwargs.setdefault("context", {})["process.returncode"] = returncode
        if stdout:
            kwargs.setdefault("context", {})["process.stdout"] = stdout
        if stderr:
            kwargs.setdefault("context", {})["process.stderr"] = stderr
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "PROCESS_ERROR"


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
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
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
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(
                version_expected
            )
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(
                version_actual
            )
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "CONCURRENCY_ERROR"
