# provide/foundation/transport/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any, Protocol, runtime_checkable

from attrs import define, field

from provide.foundation.logger import get_logger
from provide.foundation.serialization import json_loads
from provide.foundation.transport.types import Data, Headers, Params, TransportType

"""Core transport abstractions."""

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


@define(slots=True)
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


@define(slots=True)
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
        if isinstance(self.body, bytes):
            return json_loads(self.body.decode("utf-8"))
        if isinstance(self.body, str):
            return json_loads(self.body)
        raise ValueError("Response body is not JSON-parseable")

    @property
    def text(self) -> str:
        """Get response body as text."""
        if isinstance(self.body, bytes):
            return self.body.decode("utf-8")
        if isinstance(self.body, str):
            return self.body
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

    async def __aenter__(self) -> Transport:
        """Context manager entry."""
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Context manager exit."""
        await self.disconnect()


class TransportBase(ABC):
    """Base class for transport implementations."""

    def xǁTransportBaseǁ__init____mutmut_orig(self) -> None:
        self._logger = get_logger(self.__class__.__name__)

    def xǁTransportBaseǁ__init____mutmut_1(self) -> None:
        self._logger = None

    def xǁTransportBaseǁ__init____mutmut_2(self) -> None:
        self._logger = get_logger(None)

    xǁTransportBaseǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTransportBaseǁ__init____mutmut_1": xǁTransportBaseǁ__init____mutmut_1,
        "xǁTransportBaseǁ__init____mutmut_2": xǁTransportBaseǁ__init____mutmut_2,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTransportBaseǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁTransportBaseǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁTransportBaseǁ__init____mutmut_orig)
    xǁTransportBaseǁ__init____mutmut_orig.__name__ = "xǁTransportBaseǁ__init__"

    @abstractmethod
    async def execute(self, request: Request) -> Response:
        """Execute a request and return response."""

    @abstractmethod
    def supports(self, transport_type: TransportType) -> bool:
        """Check if this transport handles the given type."""

    async def xǁTransportBaseǁconnect__mutmut_orig(self) -> None:
        """Default connect implementation."""
        self._logger.trace("Transport connecting")

    async def xǁTransportBaseǁconnect__mutmut_1(self) -> None:
        """Default connect implementation."""
        self._logger.trace(None)

    async def xǁTransportBaseǁconnect__mutmut_2(self) -> None:
        """Default connect implementation."""
        self._logger.trace("XXTransport connectingXX")

    async def xǁTransportBaseǁconnect__mutmut_3(self) -> None:
        """Default connect implementation."""
        self._logger.trace("transport connecting")

    async def xǁTransportBaseǁconnect__mutmut_4(self) -> None:
        """Default connect implementation."""
        self._logger.trace("TRANSPORT CONNECTING")

    xǁTransportBaseǁconnect__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTransportBaseǁconnect__mutmut_1": xǁTransportBaseǁconnect__mutmut_1,
        "xǁTransportBaseǁconnect__mutmut_2": xǁTransportBaseǁconnect__mutmut_2,
        "xǁTransportBaseǁconnect__mutmut_3": xǁTransportBaseǁconnect__mutmut_3,
        "xǁTransportBaseǁconnect__mutmut_4": xǁTransportBaseǁconnect__mutmut_4,
    }

    def connect(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTransportBaseǁconnect__mutmut_orig"),
            object.__getattribute__(self, "xǁTransportBaseǁconnect__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    connect.__signature__ = _mutmut_signature(xǁTransportBaseǁconnect__mutmut_orig)
    xǁTransportBaseǁconnect__mutmut_orig.__name__ = "xǁTransportBaseǁconnect"

    async def xǁTransportBaseǁdisconnect__mutmut_orig(self) -> None:
        """Default disconnect implementation."""
        self._logger.trace("Transport disconnecting")

    async def xǁTransportBaseǁdisconnect__mutmut_1(self) -> None:
        """Default disconnect implementation."""
        self._logger.trace(None)

    async def xǁTransportBaseǁdisconnect__mutmut_2(self) -> None:
        """Default disconnect implementation."""
        self._logger.trace("XXTransport disconnectingXX")

    async def xǁTransportBaseǁdisconnect__mutmut_3(self) -> None:
        """Default disconnect implementation."""
        self._logger.trace("transport disconnecting")

    async def xǁTransportBaseǁdisconnect__mutmut_4(self) -> None:
        """Default disconnect implementation."""
        self._logger.trace("TRANSPORT DISCONNECTING")

    xǁTransportBaseǁdisconnect__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTransportBaseǁdisconnect__mutmut_1": xǁTransportBaseǁdisconnect__mutmut_1,
        "xǁTransportBaseǁdisconnect__mutmut_2": xǁTransportBaseǁdisconnect__mutmut_2,
        "xǁTransportBaseǁdisconnect__mutmut_3": xǁTransportBaseǁdisconnect__mutmut_3,
        "xǁTransportBaseǁdisconnect__mutmut_4": xǁTransportBaseǁdisconnect__mutmut_4,
    }

    def disconnect(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTransportBaseǁdisconnect__mutmut_orig"),
            object.__getattribute__(self, "xǁTransportBaseǁdisconnect__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    disconnect.__signature__ = _mutmut_signature(xǁTransportBaseǁdisconnect__mutmut_orig)
    xǁTransportBaseǁdisconnect__mutmut_orig.__name__ = "xǁTransportBaseǁdisconnect"

    async def xǁTransportBaseǁstream__mutmut_orig(self, request: Request) -> AsyncIterator[bytes]:
        """Stream response data incrementally.

        Note: This is an intentional design limitation. The base Transport class
        does not implement streaming. Subclasses may override this method to provide
        streaming support if needed for specific use cases.

        Raises:
            NotImplementedError: Streaming is not supported by this transport implementation
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support streaming. "
            f"Override this method in a subclass to implement streaming support."
        )

    async def xǁTransportBaseǁstream__mutmut_1(self, request: Request) -> AsyncIterator[bytes]:
        """Stream response data incrementally.

        Note: This is an intentional design limitation. The base Transport class
        does not implement streaming. Subclasses may override this method to provide
        streaming support if needed for specific use cases.

        Raises:
            NotImplementedError: Streaming is not supported by this transport implementation
        """
        raise NotImplementedError(None)

    xǁTransportBaseǁstream__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTransportBaseǁstream__mutmut_1": xǁTransportBaseǁstream__mutmut_1
    }

    def stream(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTransportBaseǁstream__mutmut_orig"),
            object.__getattribute__(self, "xǁTransportBaseǁstream__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    stream.__signature__ = _mutmut_signature(xǁTransportBaseǁstream__mutmut_orig)
    xǁTransportBaseǁstream__mutmut_orig.__name__ = "xǁTransportBaseǁstream"

    async def __aenter__(self) -> TransportBase:
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        await self.disconnect()


__all__ = [
    "Request",
    "Response",
    "Transport",
    "TransportBase",
]


# <3 🧱🤝🚚🪄
