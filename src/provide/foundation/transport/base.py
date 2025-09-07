"""
Core transport abstractions.
"""

import time
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any, Protocol, runtime_checkable

from attrs import define, field

from provide.foundation.logger import get_logger
from provide.foundation.transport.types import Data, Headers, Params, TransportType

log = get_logger(__name__)


@define
class Request:
    """Protocol-agnostic request."""
    
    uri: str
    method: str = "GET"
    headers: Headers = field(factory=dict)
    params: Params = field(factory=dict)
    body: Data = None
    timeout: float | None = None
    metadata: dict[str, Any] = field(factory=dict)
    
    @property
    def transport_type(self) -> TransportType:
        """Infer transport type from URI scheme."""
        scheme = self.uri.split("://")[0].lower()
        try:
            return TransportType(scheme)
        except ValueError:
            log.trace(f"Unknown scheme '{scheme}', defaulting to HTTP")
            return TransportType.HTTP
    
    @property
    def base_url(self) -> str:
        """Extract base URL from URI."""
        parts = self.uri.split("/")
        if len(parts) >= 3:
            return f"{parts[0]}//{parts[2]}"
        return self.uri


@define
class Response:
    """Protocol-agnostic response."""
    
    status: int
    headers: Headers = field(factory=dict)
    body: bytes | str | None = None
    metadata: dict[str, Any] = field(factory=dict)
    elapsed_ms: float = 0
    request: Request | None = None
    
    def is_success(self) -> bool:
        """Check if response indicates success."""
        return 200 <= self.status < 300
    
    def json(self) -> Any:
        """Parse response body as JSON."""
        import json
        
        if isinstance(self.body, bytes):
            return json.loads(self.body.decode('utf-8'))
        elif isinstance(self.body, str):
            return json.loads(self.body)
        else:
            raise ValueError("Response body is not JSON-parseable")
    
    @property
    def text(self) -> str:
        """Get response body as text."""
        if isinstance(self.body, bytes):
            return self.body.decode('utf-8')
        elif isinstance(self.body, str):
            return self.body
        else:
            return str(self.body or "")
    
    def raise_for_status(self) -> None:
        """Raise error if response status indicates failure."""
        if not self.is_success():
            from provide.foundation.transport.errors import HTTPResponseError
            raise HTTPResponseError(
                f"Request failed with status {self.status}",
                status_code=self.status,
                response=self,
            )


@runtime_checkable
class Transport(Protocol):
    """Abstract transport protocol."""
    
    async def execute(self, request: Request) -> Response:
        """Execute a request and return response."""
        ...
    
    async def stream(self, request: Request) -> AsyncIterator[bytes]:
        """Stream response data."""
        ...
    
    async def connect(self) -> None:
        """Establish connection if needed."""
        ...
    
    async def disconnect(self) -> None:
        """Close connection if needed."""
        ...
    
    def supports(self, transport_type: TransportType) -> bool:
        """Check if this transport handles the given type."""
        ...
    
    async def __aenter__(self) -> "Transport":
        """Context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        await self.disconnect()


class TransportBase(ABC):
    """Base class for transport implementations."""
    
    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)
    
    @abstractmethod
    async def execute(self, request: Request) -> Response:
        """Execute a request and return response."""
        pass
    
    @abstractmethod
    def supports(self, transport_type: TransportType) -> bool:
        """Check if this transport handles the given type."""
        pass
    
    async def connect(self) -> None:
        """Default connect implementation."""
        self._logger.trace("Transport connecting")
    
    async def disconnect(self) -> None:
        """Default disconnect implementation."""
        self._logger.trace("Transport disconnecting")
    
    async def stream(self, request: Request) -> AsyncIterator[bytes]:
        """Default streaming implementation (not supported)."""
        raise NotImplementedError(f"{self.__class__.__name__} does not support streaming")
    
    async def __aenter__(self) -> "TransportBase":
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()


__all__ = [
    "Request",
    "Response", 
    "Transport",
    "TransportBase",
]