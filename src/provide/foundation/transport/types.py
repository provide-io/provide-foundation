# provide/foundation/transport/types.py
#
# This is the provide.io LLC 2025 Copyright. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum
from typing import Any, TypeAlias

"""Transport type definitions and enums."""

Headers: TypeAlias = dict[str, str]
Params: TypeAlias = dict[str, Any]
Data: TypeAlias = dict[str, Any] | bytes | str | None


class TransportType(str, Enum):
    """Supported transport types."""

    HTTP = "http"
    HTTPS = "https"
    WS = "ws"
    WSS = "wss"
    GRPC = "grpc"
    GRAPHQL = "graphql"
    AMQP = "amqp"
    MQTT = "mqtt"


class HTTPMethod(str, Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


__all__ = [
    "Data",
    "HTTPMethod",
    "Headers",
    "Params",
    "TransportType",
]


# <3 🧱🤝🚚🪄
