# provide/foundation/integrations/openobserve/otlp_adapter.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""OpenObserve-specific OTLP adapter extending generic client.

Provides OpenObserveOTLPClient that extends OTLPLogClient with OpenObserve-specific
configuration and customizations.
"""

from __future__ import annotations

import base64

from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.otlp.client import OTLPLogClient
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


def x_get_openobserve_otlp_endpoint__mutmut_orig(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_1(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = None

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_2(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip(None)

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_3(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.lstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_4(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("XX/XX")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_5(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "XX/api/XX" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_6(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/API/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_7(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" not in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_8(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = None

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_9(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split(None)[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_10(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("XX/api/XX")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_11(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/API/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_12(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[1]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_13(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = None
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_14(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org and "default"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_15(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "XXdefaultXX"
    return f"{url}/api/{org_name}/v1/logs"


def x_get_openobserve_otlp_endpoint__mutmut_16(base_url: str, org: str | None = None) -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP logs endpoint

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "DEFAULT"
    return f"{url}/api/{org_name}/v1/logs"


x_get_openobserve_otlp_endpoint__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_openobserve_otlp_endpoint__mutmut_1": x_get_openobserve_otlp_endpoint__mutmut_1,
    "x_get_openobserve_otlp_endpoint__mutmut_2": x_get_openobserve_otlp_endpoint__mutmut_2,
    "x_get_openobserve_otlp_endpoint__mutmut_3": x_get_openobserve_otlp_endpoint__mutmut_3,
    "x_get_openobserve_otlp_endpoint__mutmut_4": x_get_openobserve_otlp_endpoint__mutmut_4,
    "x_get_openobserve_otlp_endpoint__mutmut_5": x_get_openobserve_otlp_endpoint__mutmut_5,
    "x_get_openobserve_otlp_endpoint__mutmut_6": x_get_openobserve_otlp_endpoint__mutmut_6,
    "x_get_openobserve_otlp_endpoint__mutmut_7": x_get_openobserve_otlp_endpoint__mutmut_7,
    "x_get_openobserve_otlp_endpoint__mutmut_8": x_get_openobserve_otlp_endpoint__mutmut_8,
    "x_get_openobserve_otlp_endpoint__mutmut_9": x_get_openobserve_otlp_endpoint__mutmut_9,
    "x_get_openobserve_otlp_endpoint__mutmut_10": x_get_openobserve_otlp_endpoint__mutmut_10,
    "x_get_openobserve_otlp_endpoint__mutmut_11": x_get_openobserve_otlp_endpoint__mutmut_11,
    "x_get_openobserve_otlp_endpoint__mutmut_12": x_get_openobserve_otlp_endpoint__mutmut_12,
    "x_get_openobserve_otlp_endpoint__mutmut_13": x_get_openobserve_otlp_endpoint__mutmut_13,
    "x_get_openobserve_otlp_endpoint__mutmut_14": x_get_openobserve_otlp_endpoint__mutmut_14,
    "x_get_openobserve_otlp_endpoint__mutmut_15": x_get_openobserve_otlp_endpoint__mutmut_15,
    "x_get_openobserve_otlp_endpoint__mutmut_16": x_get_openobserve_otlp_endpoint__mutmut_16,
}


def get_openobserve_otlp_endpoint(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_openobserve_otlp_endpoint__mutmut_orig,
        x_get_openobserve_otlp_endpoint__mutmut_mutants,
        args,
        kwargs,
    )
    return result


get_openobserve_otlp_endpoint.__signature__ = _mutmut_signature(x_get_openobserve_otlp_endpoint__mutmut_orig)
x_get_openobserve_otlp_endpoint__mutmut_orig.__name__ = "x_get_openobserve_otlp_endpoint"


def x_build_openobserve_headers__mutmut_orig(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_1(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = None

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_2(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(None)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_3(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = None

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_4(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["XXorganizationXX"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_5(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["ORGANIZATION"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_6(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = None

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_7(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["XXstream-nameXX"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_8(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["STREAM-NAME"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_9(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user or oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_10(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = None
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_11(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = None
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_12(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode(None)
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_13(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(None).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_14(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("XXasciiXX")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_15(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ASCII")
        headers["authorization"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_16(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = None

    return headers


def x_build_openobserve_headers__mutmut_17(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["XXauthorizationXX"] = f"Basic {encoded}"

    return headers


def x_build_openobserve_headers__mutmut_18(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["AUTHORIZATION"] = f"Basic {encoded}"

    return headers


x_build_openobserve_headers__mutmut_mutants: ClassVar[MutantDict] = {
    "x_build_openobserve_headers__mutmut_1": x_build_openobserve_headers__mutmut_1,
    "x_build_openobserve_headers__mutmut_2": x_build_openobserve_headers__mutmut_2,
    "x_build_openobserve_headers__mutmut_3": x_build_openobserve_headers__mutmut_3,
    "x_build_openobserve_headers__mutmut_4": x_build_openobserve_headers__mutmut_4,
    "x_build_openobserve_headers__mutmut_5": x_build_openobserve_headers__mutmut_5,
    "x_build_openobserve_headers__mutmut_6": x_build_openobserve_headers__mutmut_6,
    "x_build_openobserve_headers__mutmut_7": x_build_openobserve_headers__mutmut_7,
    "x_build_openobserve_headers__mutmut_8": x_build_openobserve_headers__mutmut_8,
    "x_build_openobserve_headers__mutmut_9": x_build_openobserve_headers__mutmut_9,
    "x_build_openobserve_headers__mutmut_10": x_build_openobserve_headers__mutmut_10,
    "x_build_openobserve_headers__mutmut_11": x_build_openobserve_headers__mutmut_11,
    "x_build_openobserve_headers__mutmut_12": x_build_openobserve_headers__mutmut_12,
    "x_build_openobserve_headers__mutmut_13": x_build_openobserve_headers__mutmut_13,
    "x_build_openobserve_headers__mutmut_14": x_build_openobserve_headers__mutmut_14,
    "x_build_openobserve_headers__mutmut_15": x_build_openobserve_headers__mutmut_15,
    "x_build_openobserve_headers__mutmut_16": x_build_openobserve_headers__mutmut_16,
    "x_build_openobserve_headers__mutmut_17": x_build_openobserve_headers__mutmut_17,
    "x_build_openobserve_headers__mutmut_18": x_build_openobserve_headers__mutmut_18,
}


def build_openobserve_headers(*args, **kwargs):
    result = _mutmut_trampoline(
        x_build_openobserve_headers__mutmut_orig, x_build_openobserve_headers__mutmut_mutants, args, kwargs
    )
    return result


build_openobserve_headers.__signature__ = _mutmut_signature(x_build_openobserve_headers__mutmut_orig)
x_build_openobserve_headers__mutmut_orig.__name__ = "x_build_openobserve_headers"


class OpenObserveOTLPClient(OTLPLogClient):
    """OpenObserve-specific OTLP client with vendor customizations.

    Extends the generic OTLPLogClient with OpenObserve-specific configuration
    and header management.

    Examples:
        >>> from provide.foundation.integrations.openobserve.config import OpenObserveConfig
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> oo_config = OpenObserveConfig.from_env()
        >>> telemetry_config = TelemetryConfig.from_env()
        >>> client = OpenObserveOTLPClient.from_openobserve_config(
        ...     oo_config, telemetry_config
        ... )
        >>> client.send_log("Hello OpenObserve!")
        True
    """

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

        Raises:
            ValueError: If OpenObserve URL is not set

        Examples:
            >>> oo_config = OpenObserveConfig(
            ...     url="https://api.openobserve.ai",
            ...     org="my-org",
            ...     user="admin",
            ...     password="secret",
            ... )
            >>> telemetry_config = TelemetryConfig(service_name="my-service")
            >>> client = OpenObserveOTLPClient.from_openobserve_config(
            ...     oo_config, telemetry_config
            ... )
        """
        if not oo_config.url:
            msg = "OpenObserve URL must be set"
            raise ValueError(msg)

        # Build OTLP endpoint from OpenObserve URL
        endpoint = get_openobserve_otlp_endpoint(oo_config.url, oo_config.org)

        # Build headers with OpenObserve metadata
        headers = build_openobserve_headers(oo_config)

        # Merge with telemetry config headers
        if telemetry_config.otlp_headers:
            headers.update(telemetry_config.otlp_headers)

        return cls(
            endpoint=endpoint,
            headers=headers,
            service_name=telemetry_config.service_name or "foundation",
            service_version=telemetry_config.service_version,
        )

    @classmethod
    def from_env(cls) -> OpenObserveOTLPClient | None:
        """Create client from environment variables.

        Returns:
            Configured client if OpenObserve is configured, None otherwise

        Examples:
            >>> # With env vars set:
            >>> # OPENOBSERVE_URL=https://api.openobserve.ai
            >>> # OPENOBSERVE_ORG=my-org
            >>> # OPENOBSERVE_USER=admin
            >>> # OPENOBSERVE_PASSWORD=secret
            >>> client = OpenObserveOTLPClient.from_env()
            >>> if client:
            ...     client.send_log("Hello!")
        """
        try:
            oo_config = OpenObserveConfig.from_env()
            if not oo_config.is_configured():
                return None

            telemetry_config = TelemetryConfig.from_env()

            return cls.from_openobserve_config(oo_config, telemetry_config)
        except Exception:
            return None


__all__ = [
    "OpenObserveOTLPClient",
    "build_openobserve_headers",
    "get_openobserve_otlp_endpoint",
]


# <3 🧱🤝🔌🪄
