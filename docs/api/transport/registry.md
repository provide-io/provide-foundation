# Transport Registry

Hub-based transport registration and discovery system for protocol-agnostic communication.

## Overview

The Transport Registry provides a unified system for registering, discovering, and managing transport implementations using the Foundation Hub. It enables dynamic transport selection based on URI schemes and supports extensible transport protocols.

## Core Functions

### register_transport()

Register a transport implementation in the Hub registry.

```python
from provide.foundation.transport.registry import register_transport
from provide.foundation.transport.types import TransportType

def register_transport(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata
) -> None
```

**Parameters:**
- `transport_type`: The primary transport type identifier
- `transport_class`: Transport implementation class
- `schemes`: List of URI schemes this transport handles (defaults to transport_type.value)
- `**metadata`: Additional metadata for the transport

**Example:**
```python
from provide.foundation.transport.registry import register_transport
from provide.foundation.transport.types import TransportType
from myapp.transports import WebSocketTransport

# Register WebSocket transport
register_transport(
    transport_type=TransportType.WS,
    transport_class=WebSocketTransport,
    schemes=["ws", "wss"],
    version="1.0.0",
    description="WebSocket transport implementation"
)
```

### get_transport_for_scheme()

Get transport class for a specific URI scheme.

```python
from provide.foundation.transport.registry import get_transport_for_scheme

def get_transport_for_scheme(scheme: str) -> type[Transport]
```

**Parameters:**
- `scheme`: URI scheme (e.g., 'http', 'https', 'ws')

**Returns:**
- Transport class that handles the scheme

**Raises:**
- `TransportNotFoundError`: If no transport is registered for the scheme

**Example:**
```python
# Get HTTP transport class
transport_class = get_transport_for_scheme("https")
transport = transport_class()
```

### get_transport()

Get transport instance for a URI.

```python
from provide.foundation.transport.registry import get_transport

def get_transport(uri: str) -> Transport
```

**Parameters:**
- `uri`: Full URI to get transport for

**Returns:**
- Transport instance ready to use

**Raises:**
- `TransportNotFoundError`: If no transport supports the URI scheme

**Example:**
```python
# Get transport for specific URI
transport = get_transport("https://api.example.com/data")
await transport.connect()

# Use transport
request = Request(uri="https://api.example.com/data", method="GET")
response = await transport.execute(request)
```

### list_registered_transports()

List all registered transports with their metadata.

```python
from provide.foundation.transport.registry import list_registered_transports

def list_registered_transports() -> dict[str, dict[str, Any]]
```

**Returns:**
- Dictionary mapping transport names to their information

**Example:**
```python
transports = list_registered_transports()
for name, info in transports.items():
    print(f"Transport: {name}")
    print(f"  Class: {info['class'].__name__}")
    print(f"  Schemes: {info['schemes']}")
    print(f"  Type: {info['transport_type']}")
```

### get_transport_info()

Get detailed information about a specific transport.

```python
from provide.foundation.transport.registry import get_transport_info

def get_transport_info(scheme_or_name: str) -> dict[str, Any] | None
```

**Parameters:**
- `scheme_or_name`: URI scheme or transport name

**Returns:**
- Transport information dictionary or None if not found

**Example:**
```python
# Get info by scheme
http_info = get_transport_info("https")
if http_info:
    print(f"Transport: {http_info['name']}")
    print(f"Schemes: {http_info['schemes']}")

# Get info by name
transport_info = get_transport_info("http")
```

## Transport Implementation

### Creating Custom Transports

To create a custom transport, implement the Transport abstract base class:

```python
from provide.foundation.transport.base import Transport, Request, Response
from provide.foundation.transport.registry import register_transport
from provide.foundation.transport.types import TransportType

class CustomTransport(Transport):
    """Custom transport implementation."""
    
    async def connect(self) -> None:
        """Establish transport connection."""
        # Initialize connection
        pass
    
    async def disconnect(self) -> None:
        """Close transport connection."""
        # Cleanup connection
        pass
    
    async def execute(self, request: Request) -> Response:
        """Execute request and return response."""
        # Implement request handling
        response = Response(
            status=200,
            headers={},
            body=b"response data"
        )
        return response
    
    async def stream(self, request: Request) -> AsyncIterator[bytes]:
        """Stream response data."""
        # Implement streaming
        yield b"chunk1"
        yield b"chunk2"

# Register the custom transport
register_transport(
    transport_type=TransportType("custom"),
    transport_class=CustomTransport,
    schemes=["custom", "custom-secure"],
    description="Custom protocol transport"
)
```

### Transport Discovery

Transports are automatically discovered based on URI schemes:

```python
from provide.foundation.transport import get

# Automatically uses HTTP transport
response = await get("https://api.example.com/data")

# Automatically uses registered custom transport
response = await get("custom://service.example.com/data")
```

## Hub Integration

The transport registry integrates with Foundation Hub for component management:

```python
from provide.foundation.hub import get_component_registry
from provide.foundation.hub.components import ComponentCategory

# Access transport registry through Hub
registry = get_component_registry()

# Find all transport components
for entry in registry:
    if entry.dimension == ComponentCategory.TRANSPORT.value:
        print(f"Transport: {entry.name}")
        print(f"  Class: {entry.value}")
        print(f"  Schemes: {entry.metadata.get('schemes', [])}")
```

## Configuration

Transports can include configuration metadata during registration:

```python
register_transport(
    transport_type=TransportType.HTTP,
    transport_class=HTTPTransport,
    schemes=["http", "https"],
    # Configuration metadata
    default_timeout=30.0,
    pool_connections=10,
    verify_ssl=True,
    version="2.0.0"
)
```

## Error Handling

Registry operations use Foundation's error handling:

```python
from provide.foundation.transport.errors import TransportNotFoundError
from provide.foundation.transport.registry import get_transport_for_scheme

try:
    transport_class = get_transport_for_scheme("unknown")
except TransportNotFoundError as e:
    logger.error("transport_not_found", scheme=e.scheme)
    # Handle missing transport
```

## Registry State

The registry supports re-registration and runtime updates:

```python
# Re-register transport (replaces existing)
register_transport(
    transport_type=TransportType.HTTP,
    transport_class=NewHTTPTransport,
    schemes=["http", "https"],
    replace=True  # Implicit - always allows re-registration
)

# Check registration status
transports = list_registered_transports()
if "http" in transports:
    print("HTTP transport is registered")
```

## See Also

- [Transport Client](client.md) - UniversalClient for making requests
- [Transport Middleware](middleware.md) - Request/response processing pipeline
- [Hub System](../hub/api-index.md) - Component registry foundation
- [Error Handling](../errors/api-index.md) - Transport error types