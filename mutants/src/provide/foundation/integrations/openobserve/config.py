# provide/foundation/integrations/openobserve/config.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from attrs import define

from provide.foundation.config.base import field
from provide.foundation.config.env import RuntimeConfig

"""OpenObserve integration configuration."""
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


@define(slots=True, repr=False)
class OpenObserveConfig(RuntimeConfig):
    """Configuration for OpenObserve integration."""

    url: str | None = field(
        default=None,
        env_var="OPENOBSERVE_URL",
        description="OpenObserve URL endpoint",
    )
    org: str | None = field(
        default=None,
        env_var="OPENOBSERVE_ORG",
        description="OpenObserve organization",
    )
    user: str | None = field(
        default=None,
        env_var="OPENOBSERVE_USER",
        description="OpenObserve username",
    )
    password: str | None = field(
        default=None,
        env_var="OPENOBSERVE_PASSWORD",
        description="OpenObserve password",
    )
    stream: str | None = field(
        default=None,
        env_var="OPENOBSERVE_STREAM",
        description="OpenObserve stream name",
    )

    def is_configured(self) -> bool:
        """Check if OpenObserve is configured with required settings.

        Returns:
            True if URL, user, and password are all set

        """
        return bool(self.url and self.user and self.password)

    def get_otlp_endpoint(self) -> str | None:
        """Get OTLP endpoint derived from OpenObserve URL.

        Returns:
            OTLP endpoint URL or None if not configured

        """
        if not self.url:
            return None

        # Remove /api/{org} suffix if present
        base_url = self.url
        if "/api/" in base_url:
            # Extract base URL before /api/
            base_url = base_url.split("/api/")[0]

        # Construct OTLP endpoint
        org = self.org or "default"
        return f"{base_url}/api/{org}"

    def is_available(self) -> bool:
        """Test if OpenObserve is available and reachable.

        Returns:
            True if connection test succeeds

        """
        if not self.is_configured():
            return False

        try:
            # Import here to avoid circular dependency
            import asyncio

            from provide.foundation.integrations.openobserve.client import OpenObserveClient

            client = OpenObserveClient(
                url=self.url,  # type: ignore[arg-type]
                username=self.user,  # type: ignore[arg-type]
                password=self.password,  # type: ignore[arg-type]
                organization=self.org or "default",
            )
            return asyncio.run(client.test_connection())
        except Exception:
            return False


# <3 🧱🤝🔌🪄
