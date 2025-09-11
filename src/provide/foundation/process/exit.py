"""Process exit utilities for standardized exit handling."""

import sys

from provide.foundation.config.defaults import EXIT_SUCCESS, EXIT_ERROR, EXIT_SIGINT


def _get_logger():
    """Get logger instance lazily to avoid circular imports."""
    from provide.foundation.logger import logger
    return logger


def exit_success(message: str | None = None) -> None:
    """Exit with success status.
    
    Args:
        message: Optional message to log before exiting
    """
    if message:
        logger = _get_logger()
        logger.info(f"Exiting successfully: {message}")
    sys.exit(EXIT_SUCCESS)


def exit_error(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.
    
    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)
    """
    if message:
        logger = _get_logger()
        logger.error(f"Exiting with error: {message}", exit_code=code)
    sys.exit(code)


def exit_interrupted(message: str = "Process interrupted") -> None:
    """Exit due to interrupt signal (SIGINT).
    
    Args:
        message: Message to log before exiting
    """
    logger = _get_logger()
    logger.warning(f"Exiting due to interrupt: {message}")
    sys.exit(EXIT_SIGINT)