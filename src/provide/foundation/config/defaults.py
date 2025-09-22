from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.logger.config.logging import LoggingConfig

"""Centralized default values for Foundation configuration.
All defaults are defined here instead of inline in field definitions.
"""

# =================================
# Logging defaults
# =================================
DEFAULT_LOG_LEVEL = "WARNING"
DEFAULT_CONSOLE_FORMATTER = "key_value"
DEFAULT_LOGGER_NAME_EMOJI_ENABLED = True
DEFAULT_DAS_EMOJI_ENABLED = True
DEFAULT_OMIT_TIMESTAMP = False
DEFAULT_FOUNDATION_SETUP_LOG_LEVEL = "INFO"
DEFAULT_FOUNDATION_LOG_OUTPUT = "stderr"
DEFAULT_RATE_LIMIT_ENABLED = False
DEFAULT_RATE_LIMIT_EMIT_WARNINGS = True
DEFAULT_RATE_LIMIT_GLOBAL = 5.0
DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY = 1000
DEFAULT_RATE_LIMIT_OVERFLOW_POLICY = "drop_oldest"

# Logger system specific defaults
DEFAULT_FALLBACK_LOG_LEVEL = "INFO"
DEFAULT_FALLBACK_LOG_LEVEL_NUMERIC = 20

# =================================
# Telemetry defaults
# =================================
DEFAULT_TELEMETRY_GLOBALLY_DISABLED = False
DEFAULT_TRACING_ENABLED = True
DEFAULT_METRICS_ENABLED = True
DEFAULT_OTLP_PROTOCOL = "http/protobuf"
DEFAULT_TRACE_SAMPLE_RATE = 1.0

# =================================
# Profiling defaults
# =================================
DEFAULT_PROFILING_SAMPLE_RATE = 0.01  # 1% sampling
DEFAULT_PROFILING_ENABLED = False
DEFAULT_PROFILING_TRACK_MEMORY = False
DEFAULT_PROFILING_BUFFER_SIZE = 1000
DEFAULT_PROFILING_FLUSH_INTERVAL_SECONDS = 30
DEFAULT_PROFILING_MAX_MEMORY_MB = 100
DEFAULT_PROFILING_ENABLE_FAST_PATH = True
DEFAULT_PROFILING_BACKGROUND_PROCESSING = True
DEFAULT_PROFILING_CLI_ENABLED = True

# Export defaults
DEFAULT_PROFILING_BATCH_SIZE = 100
DEFAULT_PROFILING_EXPORT_TIMEOUT_SECONDS = 30
DEFAULT_PROFILING_MAX_RETRIES = 3

# =================================
# Process defaults
# =================================
DEFAULT_PROCESS_READLINE_TIMEOUT = 2.0
DEFAULT_PROCESS_READCHAR_TIMEOUT = 1.0
DEFAULT_PROCESS_TERMINATE_TIMEOUT = 7.0
DEFAULT_PROCESS_WAIT_TIMEOUT = 10.0

# =================================
# File/Lock defaults
# =================================
DEFAULT_FILE_LOCK_TIMEOUT = 10.0

# =================================
# Resilience defaults
# =================================
DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT = 60.0

# =================================
# Integration defaults (OpenObserve)
# =================================
DEFAULT_OPENOBSERVE_TIMEOUT = 30
DEFAULT_OPENOBSERVE_MAX_RETRIES = 3

# =================================
# Testing defaults
# =================================
DEFAULT_TEST_WAIT_TIMEOUT = 5.0
DEFAULT_TEST_PARALLEL_TIMEOUT = 10.0
DEFAULT_TEST_CHECKPOINT_TIMEOUT = 5.0

# =================================
# Exit codes
# =================================
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_SIGINT = 130  # Standard exit code for SIGINT

# =================================
# Temporary file/directory defaults
# =================================
DEFAULT_TEMP_PREFIX = "provide_"
DEFAULT_TEMP_SUFFIX = ""
DEFAULT_TEMP_CLEANUP = True
DEFAULT_TEMP_TEXT_MODE = False

# =================================
# Directory operation defaults
# =================================
DEFAULT_DIR_MODE = 0o755
DEFAULT_DIR_PARENTS = True
DEFAULT_MISSING_OK = True

# =================================
# Atomic write defaults
# =================================
DEFAULT_ATOMIC_MODE = 0o644
DEFAULT_ATOMIC_ENCODING = "utf-8"

# =================================
# Factory functions for mutable defaults
# =================================


def default_empty_dict() -> dict[str, str]:
    """Factory for empty string dictionaries."""
    return {}


def default_module_levels() -> dict[str, str]:
    """Factory for module log levels dictionary."""
    return {
        "asyncio": "INFO",  # Suppress asyncio DEBUG messages (e.g., selector events)
    }


def default_rate_limits() -> dict[str, tuple[float, float]]:
    """Factory for per-logger rate limits dictionary."""
    return {}


def default_otlp_headers() -> dict[str, str]:
    """Factory for OTLP headers dictionary."""
    return {}


def default_logging_config() -> LoggingConfig:
    """Factory for LoggingConfig instance."""
    # Import here to avoid circular imports
    from provide.foundation.logger.config.logging import LoggingConfig

    return LoggingConfig.from_env()


# =================================
# Crypto module defaults
# =================================
DEFAULT_CERTIFICATE_KEY_TYPE = None
DEFAULT_CERTIFICATE_VALIDITY_DAYS = 365
DEFAULT_ECDSA_CURVE = None
DEFAULT_RSA_KEY_SIZE = 2048
DEFAULT_SIGNATURE_ALGORITHM = None
DEFAULT_ED25519_PRIVATE_KEY_SIZE = 32
DEFAULT_ED25519_PUBLIC_KEY_SIZE = 32
DEFAULT_ED25519_SIGNATURE_SIZE = 64


def default_supported_ec_curves() -> set[str]:
    """Factory for supported EC curves set."""
    return set()


def default_supported_key_types() -> set[str]:
    """Factory for supported key types set."""
    return set()


def default_supported_rsa_sizes() -> set[int]:
    """Factory for supported RSA sizes set."""
    return set()


# =================================
# Converter functions (to replace lambdas)
# =================================


def path_converter(x: str | None) -> Path | None:
    """Convert string to Path or None."""
    return Path(x) if x else None
