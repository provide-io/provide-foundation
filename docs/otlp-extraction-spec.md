# OTLP Extraction Implementation Specification

## Overview

This document specifies the complete implementation for extracting common OTLP/OpenTelemetry logic from the OpenObserve integration into the core logger module.

**Status**: ✅ Package structure created, severity mapping implemented
**Remaining**: 10 modules + tests + documentation

---

## File-by-File Implementation Specification

### ✅ COMPLETED: `logger/otlp/severity.py` (120 lines)

**Status**: Implemented and tested
**Purpose**: Map log levels to/from OTLP severity numbers
**Code Quality**: ✅ Passed ruff, mypy

---

### 1. `logger/otlp/resource.py` (~80 lines)

**Purpose**: OpenTelemetry Resource creation and service attribute management

**Dependencies**:
```python
from typing import Any
# Optional: from opentelemetry.sdk.resources import Resource, ResourceAttributes
```

**Public API**:
```python
def build_resource_attributes(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Returns standard OpenTelemetry resource attributes with:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes
    """

def create_otlp_resource(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Returns:
        Resource instance if opentelemetry SDK available, None otherwise

    Handles ImportError gracefully for environments without OpenTelemetry.
    """
```

**Implementation Notes**:
- Must handle `ImportError` gracefully (OpenTelemetry SDK is optional)
- Use constants from `ResourceAttributes` if available, fallback to strings
- Standard attributes: `service.name`, `service.version`, `deployment.environment`
- Allow custom attributes via `additional_attrs`

**Extracted From**:
- `integrations/openobserve/otlp_helpers.py::create_otlp_resource()` (lines 37-60)

**Testing**:
- Test with OpenTelemetry SDK available
- Test without OpenTelemetry SDK (should return None gracefully)
- Test attribute building with various combinations
- Verify standard attribute keys match OpenTelemetry spec

---

### 2. `logger/otlp/helpers.py` (~150 lines)

**Purpose**: Generic OTLP helper functions for trace context, endpoints, and log formatting

**Dependencies**:
```python
from typing import Any
from datetime import datetime
# Optional: from opentelemetry import trace
```

**Public API**:
```python
def extract_trace_context() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry or Foundation tracer.

    Tries (in order):
    1. OpenTelemetry trace context
    2. Foundation tracer context
    3. Returns None if no trace context available

    Returns:
        Dict with 'trace_id' and optionally 'span_id', or None
    """

def add_trace_context_to_attributes(attributes: dict[str, Any]) -> None:
    """Add trace context to attributes dict (modifies in place).

    Extracts trace context and adds trace_id/span_id to attributes.
    Safe to call even if no trace context is available (no-op).
    """

def build_otlp_endpoint(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Handles:
    - Trailing slashes
    - Existing /v1/{signal} paths (idempotent)
    """

def build_otlp_headers(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token

    Returns:
        Complete headers dict with Content-Type and auth
    """

def normalize_attributes(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts:
    - Non-serializable types to strings
    - Nested dicts to JSON strings
    - Lists to JSON strings
    - None values to empty strings

    Returns new dict (doesn't modify input).
    """
```

**Implementation Notes**:
- Trace context extraction must try multiple sources (OpenTelemetry, Foundation)
- Must handle `ImportError` for optional dependencies gracefully
- Endpoint building should be idempotent (handle URLs that already have /v1/logs)
- Attribute normalization ensures OTLP compatibility

**Extracted From**:
- `integrations/openobserve/otlp_helpers.py::add_trace_context_to_log_entry()` (lines 99-135)
- `integrations/openobserve/otlp_helpers.py::add_trace_attributes()` (lines 63-75)
- `integrations/openobserve/otlp_helpers.py::configure_otlp_exporter()` (lines 12-34) - partially

**Testing**:
- Test trace context extraction with/without OpenTelemetry
- Test trace context extraction with/without Foundation tracer
- Test endpoint building with various URL formats
- Test attribute normalization with complex types
- Test header building with/without authentication

---

### 3. `logger/otlp/circuit.py` (~200 lines)

**Purpose**: Circuit breaker pattern for OTLP reliability

**Implementation**: **MOVE** from `integrations/openobserve/otlp_circuit.py` with minimal changes

**Changes Required**:
1. Update module docstring to indicate generic usage
2. Remove OpenObserve-specific references in comments
3. Keep all existing functionality (class, global instance, functions)
4. Update imports if needed

**Public API** (unchanged):
```python
class OTLPCircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60.0, half_open_timeout=10.0): ...
    def can_attempt(self) -> bool: ...
    def record_success(self) -> None: ...
    def record_failure(self, error: Exception | None = None) -> None: ...
    def reset(self) -> None: ...
    def get_stats(self) -> dict[str, Any]: ...

def get_otlp_circuit_breaker() -> OTLPCircuitBreaker: ...
def reset_otlp_circuit_breaker() -> None: ...
```

**Testing**:
- **COPY** existing tests from `tests/integrations/openobserve/test_otlp_circuit.py`
- Move to `tests/logger/otlp/test_circuit.py`
- Update imports only
- All existing tests should pass without modification

---

### 4. `logger/otlp/client.py` (~350 lines)

**Purpose**: Generic OTLP client for any OpenTelemetry-compatible backend

**Dependencies**:
```python
from typing import Any
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.otlp.circuit import get_otlp_circuit_breaker
from provide.foundation.logger.otlp.severity import map_level_to_severity
from provide.foundation.logger.otlp.resource import create_otlp_resource
from provide.foundation.logger.otlp.helpers import (
    extract_trace_context,
    build_otlp_endpoint,
    build_otlp_headers,
    normalize_attributes,
)
# Optional: from opentelemetry.sdk._logs import LoggerProvider, ...
```

**Public API**:
```python
class OTLPLogClient:
    """Generic OTLP client for any OpenTelemetry-compatible backend."""

    def __init__(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        service_name: str = "foundation",
        service_version: str | None = None,
        environment: str | None = None,
        timeout: float = 30.0,
        use_circuit_breaker: bool = True,
    ) -> None:
        """Initialize OTLP client.

        Args:
            endpoint: OTLP endpoint URL (e.g., "https://api.example.com/v1/logs")
            headers: Optional custom headers (auth, organization, etc.)
            service_name: Service name for resource attributes
            service_version: Optional service version
            environment: Optional environment (dev, staging, prod)
            timeout: Request timeout in seconds
            use_circuit_breaker: Enable circuit breaker pattern
        """

    @classmethod
    def from_config(
        cls,
        config: TelemetryConfig,
        additional_headers: dict[str, str] | None = None,
    ) -> OTLPLogClient:
        """Create client from TelemetryConfig.

        Args:
            config: TelemetryConfig instance
            additional_headers: Additional headers to merge with config headers

        Returns:
            Configured OTLPLogClient instance

        Raises:
            ValueError: If config.otlp_endpoint is not set
        """

    def send_log(
        self,
        message: str,
        level: str = "INFO",
        attributes: dict[str, Any] | None = None,
    ) -> bool:
        """Send single log via OTLP.

        Args:
            message: Log message
            level: Log level (DEBUG, INFO, WARN, ERROR, FATAL)
            attributes: Optional log attributes

        Returns:
            True if sent successfully, False otherwise

        Circuit breaker pattern:
        - Checks circuit before attempting
        - Records success/failure
        - Automatically disables after threshold failures
        - Auto-recovers with exponential backoff
        """

    def create_logger_provider(self) -> Any | None:
        """Create persistent LoggerProvider for continuous logging.

        Returns:
            LoggerProvider if OpenTelemetry SDK available, None otherwise

        Use this for long-running applications that need persistent OTLP logging.
        The provider can be used with structlog processors for automatic OTLP export.

        Circuit breaker:
        - Returns None if circuit is open
        - Records success if provider created
        - Records failure if exception occurs
        """

    def is_available(self) -> bool:
        """Check if OTLP is available (SDK installed and circuit not open)."""

    def get_stats(self) -> dict[str, Any]:
        """Get client statistics including circuit breaker state."""
```

**Implementation Notes**:
- Must handle missing OpenTelemetry SDK gracefully (return False/None)
- Circuit breaker integration (check before send, record after)
- Suppress OpenTelemetry internal logging (stdlib_logging levels to CRITICAL)
- Use `BatchLogRecordProcessor` for efficiency
- Force flush after single log sends (ensure delivery)
- Extract trace context automatically
- Normalize attributes before sending

**Implementation Strategy**:
Extract core logic from `integrations/openobserve/otlp.py`:
- `send_log_otlp()` (lines 54-145) → `OTLPLogClient.send_log()`
- `create_otlp_logger_provider()` (lines 247-307) → `OTLPLogClient.create_logger_provider()`
- Remove OpenObserve-specific configuration (move to adapter)

**Testing**:
- Test with/without OpenTelemetry SDK
- Test circuit breaker integration (success, failure, open, recovery)
- Test from_config() factory method
- Test attribute normalization
- Test trace context extraction
- Test logger provider creation
- Mock OTLP exporter for integration tests

---

### 5. `integrations/openobserve/otlp_adapter.py` (~200 lines)

**Purpose**: OpenObserve-specific OTLP adapter extending generic client

**Dependencies**:
```python
from typing import Any
from provide.foundation.logger.otlp import OTLPLogClient
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
```

**Public API**:
```python
class OpenObserveOTLPClient(OTLPLogClient):
    """OpenObserve-specific OTLP client with vendor customizations."""

    @classmethod
    def from_openobserve_config(
        cls,
        oo_config: OpenObserveConfig,
        telemetry_config: TelemetryConfig,
    ) -> OpenObserveOTLPClient:
        """Create OTLP client configured for OpenObserve.

        Derives OTLP settings from OpenObserve configuration:
        - Builds OTLP endpoint from OpenObserve URL
        - Adds OpenObserve headers (organization, stream)
        - Configures Basic auth from credentials

        Args:
            oo_config: OpenObserve configuration
            telemetry_config: Telemetry configuration

        Returns:
            Configured OpenObserveOTLPClient
        """

    @classmethod
    def from_env(cls) -> OpenObserveOTLPClient | None:
        """Create client from environment variables.

        Returns:
            Configured client if OpenObserve is configured, None otherwise
        """

def get_openobserve_otlp_endpoint(base_url: str) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Returns OTLP logs endpoint.
    """

def build_openobserve_headers(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)
    """
```

**Implementation Notes**:
- Extends `OTLPLogClient` with OpenObserve-specific configuration
- Handles OpenObserve URL → OTLP endpoint derivation
- Adds OpenObserve-specific headers (org, stream, auth)
- Factory methods for convenience

**Extracted From**:
- `integrations/openobserve/otlp_helpers.py::configure_otlp_exporter()` - OpenObserve parts
- Logic scattered in `otlp.py` around lines 87-109, 267-291

**Testing**:
- Test endpoint derivation from various OpenObserve URLs
- Test header building with org/stream/auth
- Test from_openobserve_config() factory
- Test from_env() factory
- Verify inherits all OTLPLogClient functionality

---

### 6. `integrations/openobserve/bulk_api.py` (~100 lines)

**Purpose**: OpenObserve-specific bulk API (non-OTLP fallback)

**Implementation**: **EXTRACT** `send_log_bulk()` from `otlp.py`

**Public API**:
```python
def send_log_bulk(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.
    """

def build_bulk_request(
    message: str,
    level: str,
    service: str,
    attributes: dict[str, Any] | None,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload."""

def build_bulk_url(client: OpenObserveClient) -> str:
    """Build bulk API URL from client configuration."""
```

**Extracted From**:
- `integrations/openobserve/otlp.py::send_log_bulk()` (lines 148-214)
- `integrations/openobserve/otlp_helpers.py::build_bulk_url()` (lines 172-183)
- `integrations/openobserve/otlp_helpers.py::build_log_entry()` (lines 137-169)

**Testing**:
- Test bulk request formatting
- Test URL building
- Mock HTTP client responses
- Test error handling

---

### 7. `integrations/openobserve/auto_config.py` (~80 lines)

**Purpose**: Auto-configure OTLP from OpenObserve environment variables

**Dependencies**:
```python
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from attrs import evolve
```

**Public API**:
```python
def auto_configure_otlp_from_openobserve(
    config: TelemetryConfig,
) -> TelemetryConfig:
    """Auto-configure OTLP settings from OpenObserve if available.

    If config.otlp_endpoint is already set, returns config unchanged.
    If OpenObserve is configured (env vars), derives OTLP settings from it.

    This provides backward compatibility for users who set OpenObserve
    env vars but don't explicitly configure OTLP.

    Args:
        config: Current TelemetryConfig

    Returns:
        Config with OTLP settings derived from OpenObserve (if applicable)
    """

def should_auto_configure_otlp(config: TelemetryConfig) -> bool:
    """Check if OTLP should be auto-configured from OpenObserve."""

def get_openobserve_derived_otlp_config() -> dict[str, Any] | None:
    """Get OTLP configuration derived from OpenObserve env vars.

    Returns:
        Dict with otlp_endpoint, otlp_headers, etc., or None if not configured
    """
```

**Implementation Notes**:
- Only auto-configure if `config.otlp_endpoint` is None/empty
- Check OpenObserve env vars (OPENOBSERVE_URL, OPENOBSERVE_ORG, etc.)
- Derive OTLP endpoint, headers from OpenObserve config
- Use `attrs.evolve()` to create new config (immutable)
- Set `otlp_vendor = "openobserve"` when auto-configured

**Integration Point**:
Called from `TelemetryConfig.from_env()` or `Hub.initialize_foundation()`

**Testing**:
- Test with OpenObserve env vars set
- Test with OpenObserve env vars not set
- Test when otlp_endpoint already configured (should not override)
- Test derived endpoint/headers match OpenObserve config

---

### 8. Update `logger/processors/otlp.py` (~50 lines changed)

**Purpose**: Update existing OTLP processor to use new generic client

**Current Implementation**: Creates inline LoggerProvider
**New Implementation**: Use `OTLPLogClient`

**Changes**:
```python
# OLD (current):
def create_otlp_processor(config: TelemetryConfig) -> Any | None:
    # ... inline LoggerProvider creation ...
    from opentelemetry.sdk._logs import LoggerProvider
    # ... 40 lines of setup code ...

# NEW (proposed):
from provide.foundation.logger.otlp import OTLPLogClient

def create_otlp_processor(config: TelemetryConfig) -> Any | None:
    """Create OTLP processor using generic client."""
    if not config.otlp_endpoint:
        return None

    # Create client from config
    client = OTLPLogClient.from_config(config)
    if not client.is_available():
        return None

    # Create logger provider
    logger_provider = client.create_logger_provider()
    if not logger_provider:
        return None

    # Return structlog processor
    return OTLPStructlogProcessor(logger_provider)
```

**Testing**:
- Verify existing OTLP processor tests still pass
- Test with generic OTLP endpoint (not OpenObserve)
- Test auto-configuration from OpenObserve

---

### 9. Update `integrations/openobserve/otlp.py` (~100 lines)

**Purpose**: Update to use new adapter and keep high-level API

**Changes**:
- Remove low-level OTLP implementation
- Keep `send_log()` function as convenience wrapper
- Import from `otlp_adapter` and `bulk_api`

**New Implementation**:
```python
from provide.foundation.logger.otlp import OTLPLogClient
from provide.foundation.integrations.openobserve.otlp_adapter import OpenObserveOTLPClient
from provide.foundation.integrations.openobserve.bulk_api import send_log_bulk

def send_log_otlp(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
) -> bool:
    """Send log via OTLP (OpenObserve-configured)."""
    client = OpenObserveOTLPClient.from_env()
    if not client or not client.is_available():
        return False

    return client.send_log(message, level, attributes)

def send_log(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
    prefer_otlp: bool = True,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OTLP or bulk API (preserved API)."""
    if prefer_otlp and send_log_otlp(message, level, service, attributes):
        return True

    return send_log_bulk(message, level, service, attributes, client)

def create_otlp_logger_provider() -> Any | None:
    """Create OTLP logger provider (OpenObserve-configured)."""
    client = OpenObserveOTLPClient.from_env()
    if not client or not client.is_available():
        return None

    return client.create_logger_provider()
```

**Testing**:
- All existing OpenObserve tests should pass
- Test OTLP send with OpenObserve
- Test bulk API fallback
- Test circuit breaker integration

---

### 10. Update `integrations/openobserve/otlp_helpers.py` (~30 lines)

**Purpose**: Remove generic helpers (moved to logger/otlp/)

**Changes**:
- Delete generic functions (moved to core)
- Keep only OpenObserve-specific helpers if any
- Most functions should be deleted (moved to logger/otlp/helpers.py)

**Preserved** (if anything):
- Functions specific to OpenObserve that don't fit in adapter

---

## Testing Strategy

### Unit Tests

#### `tests/logger/otlp/test_severity.py` (~50 lines)
```python
def test_map_level_to_severity_standard_levels()
def test_map_level_to_severity_case_insensitive()
def test_map_level_to_severity_unknown_fallback()
def test_map_severity_to_level()
def test_severity_roundtrip()
```

#### `tests/logger/otlp/test_resource.py` (~80 lines)
```python
def test_build_resource_attributes_minimal()
def test_build_resource_attributes_full()
def test_create_otlp_resource_with_sdk()
def test_create_otlp_resource_without_sdk()
def test_resource_custom_attributes()
```

#### `tests/logger/otlp/test_helpers.py` (~150 lines)
```python
def test_extract_trace_context_opentelemetry()
def test_extract_trace_context_foundation()
def test_extract_trace_context_none()
def test_add_trace_context_to_attributes()
def test_build_otlp_endpoint()
def test_build_otlp_headers()
def test_normalize_attributes()
```

#### `tests/logger/otlp/test_circuit.py` (~200 lines)
**MOVE** from `tests/integrations/openobserve/test_otlp_circuit.py`
- Update imports only
- All existing tests should pass

#### `tests/logger/otlp/test_client.py` (~300 lines)
```python
def test_client_initialization()
def test_client_from_config()
def test_send_log_success()
def test_send_log_circuit_open()
def test_send_log_without_sdk()
def test_create_logger_provider()
def test_circuit_breaker_integration()
def test_trace_context_automatic()
def test_attribute_normalization()
```

#### `tests/integrations/openobserve/test_otlp_adapter.py` (~150 lines)
```python
def test_adapter_from_openobserve_config()
def test_adapter_from_env()
def test_endpoint_derivation()
def test_header_building()
def test_inherits_client_functionality()
```

#### `tests/integrations/openobserve/test_bulk_api.py` (~100 lines)
```python
def test_build_bulk_request()
def test_build_bulk_url()
def test_send_log_bulk_success()
def test_send_log_bulk_failure()
```

#### `tests/integrations/openobserve/test_auto_config.py` (~80 lines)
```python
def test_auto_configure_from_openobserve()
def test_no_auto_configure_when_otlp_set()
def test_auto_configure_without_openobserve()
def test_derived_config_values()
```

### Integration Tests

#### `tests/logger/otlp/test_otlp_integration.py` (~200 lines)
```python
def test_full_otlp_pipeline()
def test_otlp_with_structlog_processor()
def test_circuit_breaker_recovery()
def test_multiple_backends()
```

#### `tests/integrations/openobserve/test_otlp_integration.py` (~150 lines)
```python
def test_openobserve_otlp_end_to_end()
def test_fallback_to_bulk_api()
def test_auto_configuration()
```

### Backward Compatibility Tests

#### `tests/integrations/openobserve/test_otlp_backward_compat.py` (~100 lines)
```python
def test_existing_send_log_function()
def test_existing_send_log_otlp_function()
def test_existing_create_logger_provider()
def test_environment_variable_compatibility()
```

**Total Test Lines**: ~1,500 lines

---

## Migration Impact Analysis

### Breaking Changes: **NONE**

All existing public APIs are preserved:
- `send_log()` - ✅ Preserved
- `send_log_otlp()` - ✅ Preserved
- `send_log_bulk()` - ✅ Preserved (moved to bulk_api.py)
- `create_otlp_logger_provider()` - ✅ Preserved
- All environment variables - ✅ Work unchanged

### Internal Changes (Non-Breaking):

1. **Import Paths Changed** (internal only):
   - `integrations/openobserve/otlp_circuit.py` → `logger/otlp/circuit.py`
   - `integrations/openobserve/otlp_helpers.py` → Split between `logger/otlp/` modules

2. **File Deletions**:
   - `integrations/openobserve/otlp_helpers.py` (functionality moved)
   - Generic helpers extracted to logger/otlp/

3. **New Public APIs** (additions, not changes):
   - `provide.foundation.logger.otlp.OTLPLogClient` - ✨ New
   - `provide.foundation.logger.otlp.OTLPCircuitBreaker` - ♻️ Moved
   - Various helper functions in `logger/otlp/` - ♻️ Moved/refactored

### Deprecation Strategy

**Phase 1** (this implementation):
- All old APIs continue working
- New APIs available alongside
- No deprecation warnings

**Phase 2** (future, if desired):
- Add deprecation warnings to OpenObserve-specific OTLP functions
- Recommend using generic `OTLPLogClient` directly
- Timeline: 6+ months after Phase 1

**Phase 3** (distant future, if desired):
- Remove deprecated wrappers
- Keep OpenObserve adapter only
- Timeline: 12+ months after Phase 2

---

## Documentation Updates

### 1. Update `CLAUDE.md` (~20 lines added)

Add section under "Logger System":
```markdown
### OTLP Support

Foundation provides first-class OpenTelemetry Protocol (OTLP) support:

- **Generic OTLP Client** (`logger/otlp/`): Works with any OTLP backend
- **Vendor Adapters** (`integrations/*/`): Vendor-specific customizations
- **Circuit Breaker**: Automatic failure handling and recovery
- **Auto-Configuration**: Derive OTLP from vendor configs (OpenObserve)

Usage:
```python
from provide.foundation.logger.otlp import OTLPLogClient

client = OTLPLogClient(
    endpoint="https://api.honeycomb.io/v1/logs",
    headers={"x-honeycomb-team": "YOUR_API_KEY"},
    service_name="my-service",
)

client.send_log("Hello OTLP!", level="INFO")
```

For OpenObserve-specific configuration, see `integrations/openobserve/README.md`.
```

### 2. Create `logger/otlp/README.md` (~150 lines)

New file documenting:
- OTLP overview
- OTLPLogClient usage
- Circuit breaker pattern
- Vendor adapter pattern
- How to add new OTLP backends

### 3. Update `integrations/openobserve/README.md` (~30 lines added)

Add section:
```markdown
## OTLP Support

OpenObserve integration provides automatic OTLP configuration.

### Automatic Configuration

If you set OpenObserve environment variables, OTLP is auto-configured:
```bash
export OPENOBSERVE_URL="https://api.openobserve.ai"
export OPENOBSERVE_ORG="my-org"
export OPENOBSERVE_STREAM="default"
export OPENOBSERVE_USER="user@example.com"
export OPENOBSERVE_PASSWORD="password"
```

Foundation automatically derives OTLP settings (no OTLP env vars needed).

### Manual OTLP Configuration

You can also configure OTLP directly:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.openobserve.ai/api/my-org/v1/logs"
export OTEL_EXPORTER_OTLP_HEADERS="authorization=Basic <base64>"
```

See `logger/otlp/README.md` for generic OTLP configuration.
```

### 4. Update Inline Docstrings

Update docstrings in modified files to reference new locations.

---

## Implementation Checklist

### Phase 1: Core OTLP Infrastructure
- [x] ✅ Create `logger/otlp/__init__.py`
- [x] ✅ Implement `logger/otlp/severity.py`
- [ ] Implement `logger/otlp/resource.py`
- [ ] Implement `logger/otlp/helpers.py`
- [ ] Move `logger/otlp/circuit.py` from OpenObserve
- [ ] Implement `logger/otlp/client.py`

### Phase 2: OpenObserve Refactor
- [ ] Create `integrations/openobserve/otlp_adapter.py`
- [ ] Create `integrations/openobserve/bulk_api.py`
- [ ] Create `integrations/openobserve/auto_config.py`
- [ ] Update `integrations/openobserve/otlp.py` (use new modules)
- [ ] Delete `integrations/openobserve/otlp_helpers.py` (functionality moved)

### Phase 3: Integration
- [ ] Update `logger/processors/otlp.py`
- [ ] Update `logger/config/telemetry.py` (add otlp_vendor field if needed)
- [ ] Integrate auto-configuration into `TelemetryConfig.from_env()`

### Phase 4: Testing
- [ ] Unit tests for all new modules (8 test files)
- [ ] Integration tests (2 test files)
- [ ] Backward compatibility tests (1 test file)
- [ ] Run full test suite and verify no regressions

### Phase 5: Documentation
- [ ] Update `CLAUDE.md`
- [ ] Create `logger/otlp/README.md`
- [ ] Update `integrations/openobserve/README.md`
- [ ] Update inline docstrings

### Phase 6: Code Quality
- [ ] Run ruff check/format on all new files
- [ ] Run mypy on all new files
- [ ] Verify test coverage (aim for 90%+)
- [ ] Final integration test run

---

## Success Criteria

1. ✅ All existing OpenObserve OTLP functionality works unchanged
2. ✅ New generic `OTLPLogClient` can send logs to non-OpenObserve backends
3. ✅ Circuit breaker pattern works across all OTLP backends
4. ✅ Zero breaking changes to public APIs
5. ✅ All tests pass (existing + new)
6. ✅ Code quality checks pass (ruff, mypy)
7. ✅ Documentation is comprehensive and up-to-date
8. ✅ Test coverage ≥90% for new code

---

## Estimated Effort

- **Core OTLP Infrastructure** (Phase 1): ~800 lines code, 6 hours
- **OpenObserve Refactor** (Phase 2): ~400 lines code, 3 hours
- **Integration** (Phase 3): ~150 lines changes, 2 hours
- **Testing** (Phase 4): ~1,500 lines tests, 8 hours
- **Documentation** (Phase 5): ~400 lines docs, 2 hours
- **Code Quality** (Phase 6): 2 hours

**Total**: ~3,250 lines code/tests/docs, ~23 hours

---

## Approval

**Status**: ⏸️ **AWAITING APPROVAL**

Please review this specification and approve/request changes before I proceed with implementation.

**Questions for Review**:
1. Does the API design for `OTLPLogClient` meet requirements?
2. Is the OpenObserve adapter approach appropriate?
3. Should auto-configuration be enabled by default?
4. Are there any additional vendor-specific features needed?
5. Is the testing strategy comprehensive enough?

**Approval Signature**: ___________________ Date: ___________
