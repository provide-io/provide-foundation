"""
Centralized default values for Foundation configuration.
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

# =================================
# Telemetry defaults
# =================================
DEFAULT_TELEMETRY_GLOBALLY_DISABLED = False
DEFAULT_TRACING_ENABLED = True
DEFAULT_METRICS_ENABLED = True
DEFAULT_OTLP_PROTOCOL = "http/protobuf"
DEFAULT_TRACE_SAMPLE_RATE = 1.0

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