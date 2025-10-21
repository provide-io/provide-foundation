# provide/foundation/integrations/openobserve/client.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""OpenObserve API client using Foundation's transport system."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urljoin

from provide.foundation.errors.decorators import resilient
from provide.foundation.hub import get_hub
from provide.foundation.integrations.openobserve.auth import (
    get_auth_headers,
    validate_credentials,
)
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveConfigError,
    OpenObserveConnectionError,
    OpenObserveQueryError,
)
from provide.foundation.integrations.openobserve.models import (
    SearchQuery,
    SearchResponse,
    StreamInfo,
    parse_relative_time,
)
from provide.foundation.logger import get_logger
from provide.foundation.transport import UniversalClient
from provide.foundation.transport.errors import (
    TransportConnectionError,
    TransportError,
    TransportTimeoutError,
)

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class OpenObserveClient:
    """Async client for interacting with OpenObserve API.

    Uses Foundation's transport system for all HTTP operations.
    """

    def xǁOpenObserveClientǁ__init____mutmut_orig(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_1(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "XXdefaultXX",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_2(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "DEFAULT",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_3(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 31,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_4(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = None
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_5(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip(None)
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_6(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.lstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_7(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("XX/XX")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_8(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = None
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_9(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(None, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_10(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, None)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_11(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_12(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, )
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_13(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = None

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_14(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = None

    def xǁOpenObserveClientǁ__init____mutmut_15(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=None,
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_16(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=None,
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_17(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=None,
        )

    def xǁOpenObserveClientǁ__init____mutmut_18(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_19(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_20(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            )

    def xǁOpenObserveClientǁ__init____mutmut_21(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(None, self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_22(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, None),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_23(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.password),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_24(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, ),
            default_timeout=float(timeout),
        )

    def xǁOpenObserveClientǁ__init____mutmut_25(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(None),
        )
    
    xǁOpenObserveClientǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenObserveClientǁ__init____mutmut_1': xǁOpenObserveClientǁ__init____mutmut_1, 
        'xǁOpenObserveClientǁ__init____mutmut_2': xǁOpenObserveClientǁ__init____mutmut_2, 
        'xǁOpenObserveClientǁ__init____mutmut_3': xǁOpenObserveClientǁ__init____mutmut_3, 
        'xǁOpenObserveClientǁ__init____mutmut_4': xǁOpenObserveClientǁ__init____mutmut_4, 
        'xǁOpenObserveClientǁ__init____mutmut_5': xǁOpenObserveClientǁ__init____mutmut_5, 
        'xǁOpenObserveClientǁ__init____mutmut_6': xǁOpenObserveClientǁ__init____mutmut_6, 
        'xǁOpenObserveClientǁ__init____mutmut_7': xǁOpenObserveClientǁ__init____mutmut_7, 
        'xǁOpenObserveClientǁ__init____mutmut_8': xǁOpenObserveClientǁ__init____mutmut_8, 
        'xǁOpenObserveClientǁ__init____mutmut_9': xǁOpenObserveClientǁ__init____mutmut_9, 
        'xǁOpenObserveClientǁ__init____mutmut_10': xǁOpenObserveClientǁ__init____mutmut_10, 
        'xǁOpenObserveClientǁ__init____mutmut_11': xǁOpenObserveClientǁ__init____mutmut_11, 
        'xǁOpenObserveClientǁ__init____mutmut_12': xǁOpenObserveClientǁ__init____mutmut_12, 
        'xǁOpenObserveClientǁ__init____mutmut_13': xǁOpenObserveClientǁ__init____mutmut_13, 
        'xǁOpenObserveClientǁ__init____mutmut_14': xǁOpenObserveClientǁ__init____mutmut_14, 
        'xǁOpenObserveClientǁ__init____mutmut_15': xǁOpenObserveClientǁ__init____mutmut_15, 
        'xǁOpenObserveClientǁ__init____mutmut_16': xǁOpenObserveClientǁ__init____mutmut_16, 
        'xǁOpenObserveClientǁ__init____mutmut_17': xǁOpenObserveClientǁ__init____mutmut_17, 
        'xǁOpenObserveClientǁ__init____mutmut_18': xǁOpenObserveClientǁ__init____mutmut_18, 
        'xǁOpenObserveClientǁ__init____mutmut_19': xǁOpenObserveClientǁ__init____mutmut_19, 
        'xǁOpenObserveClientǁ__init____mutmut_20': xǁOpenObserveClientǁ__init____mutmut_20, 
        'xǁOpenObserveClientǁ__init____mutmut_21': xǁOpenObserveClientǁ__init____mutmut_21, 
        'xǁOpenObserveClientǁ__init____mutmut_22': xǁOpenObserveClientǁ__init____mutmut_22, 
        'xǁOpenObserveClientǁ__init____mutmut_23': xǁOpenObserveClientǁ__init____mutmut_23, 
        'xǁOpenObserveClientǁ__init____mutmut_24': xǁOpenObserveClientǁ__init____mutmut_24, 
        'xǁOpenObserveClientǁ__init____mutmut_25': xǁOpenObserveClientǁ__init____mutmut_25
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenObserveClientǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁOpenObserveClientǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁOpenObserveClientǁ__init____mutmut_orig)
    xǁOpenObserveClientǁ__init____mutmut_orig.__name__ = 'xǁOpenObserveClientǁ__init__'

    @classmethod
    def from_config(cls) -> OpenObserveClient:
        """Create client from OpenObserveConfig.

        Returns:
            Configured OpenObserveClient instance

        Raises:
            OpenObserveConfigError: If configuration is missing

        """
        from provide.foundation.integrations.openobserve.config import OpenObserveConfig

        config = OpenObserveConfig.from_env()

        if not config.url:
            raise OpenObserveConfigError(
                "OpenObserve URL not configured. Set OPENOBSERVE_URL environment variable.",
            )

        if not config.user or not config.password:
            raise OpenObserveConfigError(
                "OpenObserve credentials not configured. "
                "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
            )

        return cls(
            url=config.url,
            username=config.user,
            password=config.password,
            organization=config.org or "default",
        )

    def xǁOpenObserveClientǁ_extract_error_message__mutmut_orig(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "message" in error_data:
                return error_data["message"]
        except Exception:
            pass
        return default_msg

    def xǁOpenObserveClientǁ_extract_error_message__mutmut_1(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = None
            if isinstance(error_data, dict) and "message" in error_data:
                return error_data["message"]
        except Exception:
            pass
        return default_msg

    def xǁOpenObserveClientǁ_extract_error_message__mutmut_2(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) or "message" in error_data:
                return error_data["message"]
        except Exception:
            pass
        return default_msg

    def xǁOpenObserveClientǁ_extract_error_message__mutmut_3(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "XXmessageXX" in error_data:
                return error_data["message"]
        except Exception:
            pass
        return default_msg

    def xǁOpenObserveClientǁ_extract_error_message__mutmut_4(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "MESSAGE" in error_data:
                return error_data["message"]
        except Exception:
            pass
        return default_msg

    def xǁOpenObserveClientǁ_extract_error_message__mutmut_5(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "message" not in error_data:
                return error_data["message"]
        except Exception:
            pass
        return default_msg

    def xǁOpenObserveClientǁ_extract_error_message__mutmut_6(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "message" in error_data:
                return error_data["XXmessageXX"]
        except Exception:
            pass
        return default_msg

    def xǁOpenObserveClientǁ_extract_error_message__mutmut_7(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "message" in error_data:
                return error_data["MESSAGE"]
        except Exception:
            pass
        return default_msg
    
    xǁOpenObserveClientǁ_extract_error_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenObserveClientǁ_extract_error_message__mutmut_1': xǁOpenObserveClientǁ_extract_error_message__mutmut_1, 
        'xǁOpenObserveClientǁ_extract_error_message__mutmut_2': xǁOpenObserveClientǁ_extract_error_message__mutmut_2, 
        'xǁOpenObserveClientǁ_extract_error_message__mutmut_3': xǁOpenObserveClientǁ_extract_error_message__mutmut_3, 
        'xǁOpenObserveClientǁ_extract_error_message__mutmut_4': xǁOpenObserveClientǁ_extract_error_message__mutmut_4, 
        'xǁOpenObserveClientǁ_extract_error_message__mutmut_5': xǁOpenObserveClientǁ_extract_error_message__mutmut_5, 
        'xǁOpenObserveClientǁ_extract_error_message__mutmut_6': xǁOpenObserveClientǁ_extract_error_message__mutmut_6, 
        'xǁOpenObserveClientǁ_extract_error_message__mutmut_7': xǁOpenObserveClientǁ_extract_error_message__mutmut_7
    }
    
    def _extract_error_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenObserveClientǁ_extract_error_message__mutmut_orig"), object.__getattribute__(self, "xǁOpenObserveClientǁ_extract_error_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_error_message.__signature__ = _mutmut_signature(xǁOpenObserveClientǁ_extract_error_message__mutmut_orig)
    xǁOpenObserveClientǁ_extract_error_message__mutmut_orig.__name__ = 'xǁOpenObserveClientǁ_extract_error_message'

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_orig(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_1(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status != 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_2(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 402:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_3(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError(None)

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_4(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("XXAuthentication failed. Check credentials.XX")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_5(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("authentication failed. check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_6(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("AUTHENTICATION FAILED. CHECK CREDENTIALS.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_7(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_8(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = None
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_9(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(None, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_10(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, None)
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_11(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_12(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, )
            raise OpenObserveQueryError(f"API error: {error_msg}")

    def xǁOpenObserveClientǁ_check_response_errors__mutmut_13(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(None)
    
    xǁOpenObserveClientǁ_check_response_errors__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenObserveClientǁ_check_response_errors__mutmut_1': xǁOpenObserveClientǁ_check_response_errors__mutmut_1, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_2': xǁOpenObserveClientǁ_check_response_errors__mutmut_2, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_3': xǁOpenObserveClientǁ_check_response_errors__mutmut_3, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_4': xǁOpenObserveClientǁ_check_response_errors__mutmut_4, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_5': xǁOpenObserveClientǁ_check_response_errors__mutmut_5, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_6': xǁOpenObserveClientǁ_check_response_errors__mutmut_6, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_7': xǁOpenObserveClientǁ_check_response_errors__mutmut_7, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_8': xǁOpenObserveClientǁ_check_response_errors__mutmut_8, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_9': xǁOpenObserveClientǁ_check_response_errors__mutmut_9, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_10': xǁOpenObserveClientǁ_check_response_errors__mutmut_10, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_11': xǁOpenObserveClientǁ_check_response_errors__mutmut_11, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_12': xǁOpenObserveClientǁ_check_response_errors__mutmut_12, 
        'xǁOpenObserveClientǁ_check_response_errors__mutmut_13': xǁOpenObserveClientǁ_check_response_errors__mutmut_13
    }
    
    def _check_response_errors(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenObserveClientǁ_check_response_errors__mutmut_orig"), object.__getattribute__(self, "xǁOpenObserveClientǁ_check_response_errors__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _check_response_errors.__signature__ = _mutmut_signature(xǁOpenObserveClientǁ_check_response_errors__mutmut_orig)
    xǁOpenObserveClientǁ_check_response_errors__mutmut_orig.__name__ = 'xǁOpenObserveClientǁ_check_response_errors'

    async def xǁOpenObserveClientǁ_make_request__mutmut_orig(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_1(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = None

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_2(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(None, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_3(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, None)

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_4(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_5(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, )

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_6(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = None

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_7(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=None,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_8(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=None,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_9(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=None,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_10(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=None,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_11(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_12(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_13(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_14(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_15(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(None)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_16(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_17(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(None) from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_18(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(None) from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_19(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(None) from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def xǁOpenObserveClientǁ_make_request__mutmut_20(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(None) from e
    
    xǁOpenObserveClientǁ_make_request__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenObserveClientǁ_make_request__mutmut_1': xǁOpenObserveClientǁ_make_request__mutmut_1, 
        'xǁOpenObserveClientǁ_make_request__mutmut_2': xǁOpenObserveClientǁ_make_request__mutmut_2, 
        'xǁOpenObserveClientǁ_make_request__mutmut_3': xǁOpenObserveClientǁ_make_request__mutmut_3, 
        'xǁOpenObserveClientǁ_make_request__mutmut_4': xǁOpenObserveClientǁ_make_request__mutmut_4, 
        'xǁOpenObserveClientǁ_make_request__mutmut_5': xǁOpenObserveClientǁ_make_request__mutmut_5, 
        'xǁOpenObserveClientǁ_make_request__mutmut_6': xǁOpenObserveClientǁ_make_request__mutmut_6, 
        'xǁOpenObserveClientǁ_make_request__mutmut_7': xǁOpenObserveClientǁ_make_request__mutmut_7, 
        'xǁOpenObserveClientǁ_make_request__mutmut_8': xǁOpenObserveClientǁ_make_request__mutmut_8, 
        'xǁOpenObserveClientǁ_make_request__mutmut_9': xǁOpenObserveClientǁ_make_request__mutmut_9, 
        'xǁOpenObserveClientǁ_make_request__mutmut_10': xǁOpenObserveClientǁ_make_request__mutmut_10, 
        'xǁOpenObserveClientǁ_make_request__mutmut_11': xǁOpenObserveClientǁ_make_request__mutmut_11, 
        'xǁOpenObserveClientǁ_make_request__mutmut_12': xǁOpenObserveClientǁ_make_request__mutmut_12, 
        'xǁOpenObserveClientǁ_make_request__mutmut_13': xǁOpenObserveClientǁ_make_request__mutmut_13, 
        'xǁOpenObserveClientǁ_make_request__mutmut_14': xǁOpenObserveClientǁ_make_request__mutmut_14, 
        'xǁOpenObserveClientǁ_make_request__mutmut_15': xǁOpenObserveClientǁ_make_request__mutmut_15, 
        'xǁOpenObserveClientǁ_make_request__mutmut_16': xǁOpenObserveClientǁ_make_request__mutmut_16, 
        'xǁOpenObserveClientǁ_make_request__mutmut_17': xǁOpenObserveClientǁ_make_request__mutmut_17, 
        'xǁOpenObserveClientǁ_make_request__mutmut_18': xǁOpenObserveClientǁ_make_request__mutmut_18, 
        'xǁOpenObserveClientǁ_make_request__mutmut_19': xǁOpenObserveClientǁ_make_request__mutmut_19, 
        'xǁOpenObserveClientǁ_make_request__mutmut_20': xǁOpenObserveClientǁ_make_request__mutmut_20
    }
    
    def _make_request(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenObserveClientǁ_make_request__mutmut_orig"), object.__getattribute__(self, "xǁOpenObserveClientǁ_make_request__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _make_request.__signature__ = _mutmut_signature(xǁOpenObserveClientǁ_make_request__mutmut_orig)
    xǁOpenObserveClientǁ_make_request__mutmut_orig.__name__ = 'xǁOpenObserveClientǁ_make_request'

    async def xǁOpenObserveClientǁsearch__mutmut_orig(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_1(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 101,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_2(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 1,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_3(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = None

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_4(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is not None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_5(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = None
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_6(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "XX-1hXX"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_7(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1H"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_8(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is not None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_9(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = None

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_10(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "XXnowXX"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_11(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "NOW"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_12(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = None
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_13(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(None, now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_14(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), None) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_15(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_16(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), ) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_17(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(None), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_18(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = None

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_19(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(None, now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_20(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), None) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_21(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_22(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), ) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_23(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(None), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_24(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = None

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_25(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=None,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_26(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=None,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_27(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=None,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_28(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=None,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_29(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=None,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_30(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_31(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_32(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_33(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_34(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_35(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(None)

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_36(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = None

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_37(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method=None,
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_38(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint=None,
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_39(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params=None,
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_40(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=None,
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_41(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_42(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_43(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_44(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_45(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="XXPOSTXX",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_46(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="post",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_47(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="XX_searchXX",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_48(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_SEARCH",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_49(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"XXis_ui_histogramXX": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_50(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"IS_UI_HISTOGRAM": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_51(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "XXfalseXX", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_52(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "FALSE", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_53(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "XXis_multi_stream_searchXX": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_54(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "IS_MULTI_STREAM_SEARCH": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_55(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "XXfalseXX"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_56(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "FALSE"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_57(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "XXerrorXX" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_58(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "ERROR" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_59(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" not in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_60(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(None)

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_61(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['XXerrorXX']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_62(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['ERROR']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_63(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = None

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_64(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(None)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_65(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(None)

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def xǁOpenObserveClientǁsearch__mutmut_66(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(None)

        return result
    
    xǁOpenObserveClientǁsearch__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenObserveClientǁsearch__mutmut_1': xǁOpenObserveClientǁsearch__mutmut_1, 
        'xǁOpenObserveClientǁsearch__mutmut_2': xǁOpenObserveClientǁsearch__mutmut_2, 
        'xǁOpenObserveClientǁsearch__mutmut_3': xǁOpenObserveClientǁsearch__mutmut_3, 
        'xǁOpenObserveClientǁsearch__mutmut_4': xǁOpenObserveClientǁsearch__mutmut_4, 
        'xǁOpenObserveClientǁsearch__mutmut_5': xǁOpenObserveClientǁsearch__mutmut_5, 
        'xǁOpenObserveClientǁsearch__mutmut_6': xǁOpenObserveClientǁsearch__mutmut_6, 
        'xǁOpenObserveClientǁsearch__mutmut_7': xǁOpenObserveClientǁsearch__mutmut_7, 
        'xǁOpenObserveClientǁsearch__mutmut_8': xǁOpenObserveClientǁsearch__mutmut_8, 
        'xǁOpenObserveClientǁsearch__mutmut_9': xǁOpenObserveClientǁsearch__mutmut_9, 
        'xǁOpenObserveClientǁsearch__mutmut_10': xǁOpenObserveClientǁsearch__mutmut_10, 
        'xǁOpenObserveClientǁsearch__mutmut_11': xǁOpenObserveClientǁsearch__mutmut_11, 
        'xǁOpenObserveClientǁsearch__mutmut_12': xǁOpenObserveClientǁsearch__mutmut_12, 
        'xǁOpenObserveClientǁsearch__mutmut_13': xǁOpenObserveClientǁsearch__mutmut_13, 
        'xǁOpenObserveClientǁsearch__mutmut_14': xǁOpenObserveClientǁsearch__mutmut_14, 
        'xǁOpenObserveClientǁsearch__mutmut_15': xǁOpenObserveClientǁsearch__mutmut_15, 
        'xǁOpenObserveClientǁsearch__mutmut_16': xǁOpenObserveClientǁsearch__mutmut_16, 
        'xǁOpenObserveClientǁsearch__mutmut_17': xǁOpenObserveClientǁsearch__mutmut_17, 
        'xǁOpenObserveClientǁsearch__mutmut_18': xǁOpenObserveClientǁsearch__mutmut_18, 
        'xǁOpenObserveClientǁsearch__mutmut_19': xǁOpenObserveClientǁsearch__mutmut_19, 
        'xǁOpenObserveClientǁsearch__mutmut_20': xǁOpenObserveClientǁsearch__mutmut_20, 
        'xǁOpenObserveClientǁsearch__mutmut_21': xǁOpenObserveClientǁsearch__mutmut_21, 
        'xǁOpenObserveClientǁsearch__mutmut_22': xǁOpenObserveClientǁsearch__mutmut_22, 
        'xǁOpenObserveClientǁsearch__mutmut_23': xǁOpenObserveClientǁsearch__mutmut_23, 
        'xǁOpenObserveClientǁsearch__mutmut_24': xǁOpenObserveClientǁsearch__mutmut_24, 
        'xǁOpenObserveClientǁsearch__mutmut_25': xǁOpenObserveClientǁsearch__mutmut_25, 
        'xǁOpenObserveClientǁsearch__mutmut_26': xǁOpenObserveClientǁsearch__mutmut_26, 
        'xǁOpenObserveClientǁsearch__mutmut_27': xǁOpenObserveClientǁsearch__mutmut_27, 
        'xǁOpenObserveClientǁsearch__mutmut_28': xǁOpenObserveClientǁsearch__mutmut_28, 
        'xǁOpenObserveClientǁsearch__mutmut_29': xǁOpenObserveClientǁsearch__mutmut_29, 
        'xǁOpenObserveClientǁsearch__mutmut_30': xǁOpenObserveClientǁsearch__mutmut_30, 
        'xǁOpenObserveClientǁsearch__mutmut_31': xǁOpenObserveClientǁsearch__mutmut_31, 
        'xǁOpenObserveClientǁsearch__mutmut_32': xǁOpenObserveClientǁsearch__mutmut_32, 
        'xǁOpenObserveClientǁsearch__mutmut_33': xǁOpenObserveClientǁsearch__mutmut_33, 
        'xǁOpenObserveClientǁsearch__mutmut_34': xǁOpenObserveClientǁsearch__mutmut_34, 
        'xǁOpenObserveClientǁsearch__mutmut_35': xǁOpenObserveClientǁsearch__mutmut_35, 
        'xǁOpenObserveClientǁsearch__mutmut_36': xǁOpenObserveClientǁsearch__mutmut_36, 
        'xǁOpenObserveClientǁsearch__mutmut_37': xǁOpenObserveClientǁsearch__mutmut_37, 
        'xǁOpenObserveClientǁsearch__mutmut_38': xǁOpenObserveClientǁsearch__mutmut_38, 
        'xǁOpenObserveClientǁsearch__mutmut_39': xǁOpenObserveClientǁsearch__mutmut_39, 
        'xǁOpenObserveClientǁsearch__mutmut_40': xǁOpenObserveClientǁsearch__mutmut_40, 
        'xǁOpenObserveClientǁsearch__mutmut_41': xǁOpenObserveClientǁsearch__mutmut_41, 
        'xǁOpenObserveClientǁsearch__mutmut_42': xǁOpenObserveClientǁsearch__mutmut_42, 
        'xǁOpenObserveClientǁsearch__mutmut_43': xǁOpenObserveClientǁsearch__mutmut_43, 
        'xǁOpenObserveClientǁsearch__mutmut_44': xǁOpenObserveClientǁsearch__mutmut_44, 
        'xǁOpenObserveClientǁsearch__mutmut_45': xǁOpenObserveClientǁsearch__mutmut_45, 
        'xǁOpenObserveClientǁsearch__mutmut_46': xǁOpenObserveClientǁsearch__mutmut_46, 
        'xǁOpenObserveClientǁsearch__mutmut_47': xǁOpenObserveClientǁsearch__mutmut_47, 
        'xǁOpenObserveClientǁsearch__mutmut_48': xǁOpenObserveClientǁsearch__mutmut_48, 
        'xǁOpenObserveClientǁsearch__mutmut_49': xǁOpenObserveClientǁsearch__mutmut_49, 
        'xǁOpenObserveClientǁsearch__mutmut_50': xǁOpenObserveClientǁsearch__mutmut_50, 
        'xǁOpenObserveClientǁsearch__mutmut_51': xǁOpenObserveClientǁsearch__mutmut_51, 
        'xǁOpenObserveClientǁsearch__mutmut_52': xǁOpenObserveClientǁsearch__mutmut_52, 
        'xǁOpenObserveClientǁsearch__mutmut_53': xǁOpenObserveClientǁsearch__mutmut_53, 
        'xǁOpenObserveClientǁsearch__mutmut_54': xǁOpenObserveClientǁsearch__mutmut_54, 
        'xǁOpenObserveClientǁsearch__mutmut_55': xǁOpenObserveClientǁsearch__mutmut_55, 
        'xǁOpenObserveClientǁsearch__mutmut_56': xǁOpenObserveClientǁsearch__mutmut_56, 
        'xǁOpenObserveClientǁsearch__mutmut_57': xǁOpenObserveClientǁsearch__mutmut_57, 
        'xǁOpenObserveClientǁsearch__mutmut_58': xǁOpenObserveClientǁsearch__mutmut_58, 
        'xǁOpenObserveClientǁsearch__mutmut_59': xǁOpenObserveClientǁsearch__mutmut_59, 
        'xǁOpenObserveClientǁsearch__mutmut_60': xǁOpenObserveClientǁsearch__mutmut_60, 
        'xǁOpenObserveClientǁsearch__mutmut_61': xǁOpenObserveClientǁsearch__mutmut_61, 
        'xǁOpenObserveClientǁsearch__mutmut_62': xǁOpenObserveClientǁsearch__mutmut_62, 
        'xǁOpenObserveClientǁsearch__mutmut_63': xǁOpenObserveClientǁsearch__mutmut_63, 
        'xǁOpenObserveClientǁsearch__mutmut_64': xǁOpenObserveClientǁsearch__mutmut_64, 
        'xǁOpenObserveClientǁsearch__mutmut_65': xǁOpenObserveClientǁsearch__mutmut_65, 
        'xǁOpenObserveClientǁsearch__mutmut_66': xǁOpenObserveClientǁsearch__mutmut_66
    }
    
    def search(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenObserveClientǁsearch__mutmut_orig"), object.__getattribute__(self, "xǁOpenObserveClientǁsearch__mutmut_mutants"), args, kwargs, self)
        return result 
    
    search.__signature__ = _mutmut_signature(xǁOpenObserveClientǁsearch__mutmut_orig)
    xǁOpenObserveClientǁsearch__mutmut_orig.__name__ = 'xǁOpenObserveClientǁsearch'

    async def xǁOpenObserveClientǁlist_streams__mutmut_orig(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_1(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = None

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_2(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method=None,
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_3(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint=None,
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_4(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_5(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_6(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="XXGETXX",
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_7(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="get",
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_8(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint="XXstreamsXX",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_9(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint="STREAMS",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_10(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint="streams",
        )

        streams = None
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_11(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = None
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_12(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(None)
                            streams.append(stream_info)

        return streams

    async def xǁOpenObserveClientǁlist_streams__mutmut_13(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(None)

        return streams
    
    xǁOpenObserveClientǁlist_streams__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenObserveClientǁlist_streams__mutmut_1': xǁOpenObserveClientǁlist_streams__mutmut_1, 
        'xǁOpenObserveClientǁlist_streams__mutmut_2': xǁOpenObserveClientǁlist_streams__mutmut_2, 
        'xǁOpenObserveClientǁlist_streams__mutmut_3': xǁOpenObserveClientǁlist_streams__mutmut_3, 
        'xǁOpenObserveClientǁlist_streams__mutmut_4': xǁOpenObserveClientǁlist_streams__mutmut_4, 
        'xǁOpenObserveClientǁlist_streams__mutmut_5': xǁOpenObserveClientǁlist_streams__mutmut_5, 
        'xǁOpenObserveClientǁlist_streams__mutmut_6': xǁOpenObserveClientǁlist_streams__mutmut_6, 
        'xǁOpenObserveClientǁlist_streams__mutmut_7': xǁOpenObserveClientǁlist_streams__mutmut_7, 
        'xǁOpenObserveClientǁlist_streams__mutmut_8': xǁOpenObserveClientǁlist_streams__mutmut_8, 
        'xǁOpenObserveClientǁlist_streams__mutmut_9': xǁOpenObserveClientǁlist_streams__mutmut_9, 
        'xǁOpenObserveClientǁlist_streams__mutmut_10': xǁOpenObserveClientǁlist_streams__mutmut_10, 
        'xǁOpenObserveClientǁlist_streams__mutmut_11': xǁOpenObserveClientǁlist_streams__mutmut_11, 
        'xǁOpenObserveClientǁlist_streams__mutmut_12': xǁOpenObserveClientǁlist_streams__mutmut_12, 
        'xǁOpenObserveClientǁlist_streams__mutmut_13': xǁOpenObserveClientǁlist_streams__mutmut_13
    }
    
    def list_streams(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenObserveClientǁlist_streams__mutmut_orig"), object.__getattribute__(self, "xǁOpenObserveClientǁlist_streams__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_streams.__signature__ = _mutmut_signature(xǁOpenObserveClientǁlist_streams__mutmut_orig)
    xǁOpenObserveClientǁlist_streams__mutmut_orig.__name__ = 'xǁOpenObserveClientǁlist_streams'

    async def xǁOpenObserveClientǁget_search_history__mutmut_orig(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_1(
        self,
        stream_name: str | None = None,
        size: int = 101,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_2(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = None

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_3(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is not None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_4(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = None
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_5(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "XX-1hXX"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_6(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1H"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_7(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is not None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_8(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = None

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_9(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "XXnowXX"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_10(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "NOW"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_11(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = None
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_12(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(None, now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_13(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), None) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_14(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_15(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), ) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_16(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(None), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_17(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = None

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_18(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(None, now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_19(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), None) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_20(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_21(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), ) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_22(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(None), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_23(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = None

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_24(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "XXsizeXX": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_25(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "SIZE": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_26(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "XXstart_timeXX": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_27(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "START_TIME": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_28(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "XXend_timeXX": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_29(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "END_TIME": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_30(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = None

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_31(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["XXstream_nameXX"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_32(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["STREAM_NAME"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_33(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = None

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_34(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method=None,
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_35(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint=None,
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_36(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=None,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_37(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_38(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_39(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_40(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="XXPOSTXX",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_41(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="post",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_42(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="XX_search_historyXX",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_43(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_SEARCH_HISTORY",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    async def xǁOpenObserveClientǁget_search_history__mutmut_44(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(None)
    
    xǁOpenObserveClientǁget_search_history__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenObserveClientǁget_search_history__mutmut_1': xǁOpenObserveClientǁget_search_history__mutmut_1, 
        'xǁOpenObserveClientǁget_search_history__mutmut_2': xǁOpenObserveClientǁget_search_history__mutmut_2, 
        'xǁOpenObserveClientǁget_search_history__mutmut_3': xǁOpenObserveClientǁget_search_history__mutmut_3, 
        'xǁOpenObserveClientǁget_search_history__mutmut_4': xǁOpenObserveClientǁget_search_history__mutmut_4, 
        'xǁOpenObserveClientǁget_search_history__mutmut_5': xǁOpenObserveClientǁget_search_history__mutmut_5, 
        'xǁOpenObserveClientǁget_search_history__mutmut_6': xǁOpenObserveClientǁget_search_history__mutmut_6, 
        'xǁOpenObserveClientǁget_search_history__mutmut_7': xǁOpenObserveClientǁget_search_history__mutmut_7, 
        'xǁOpenObserveClientǁget_search_history__mutmut_8': xǁOpenObserveClientǁget_search_history__mutmut_8, 
        'xǁOpenObserveClientǁget_search_history__mutmut_9': xǁOpenObserveClientǁget_search_history__mutmut_9, 
        'xǁOpenObserveClientǁget_search_history__mutmut_10': xǁOpenObserveClientǁget_search_history__mutmut_10, 
        'xǁOpenObserveClientǁget_search_history__mutmut_11': xǁOpenObserveClientǁget_search_history__mutmut_11, 
        'xǁOpenObserveClientǁget_search_history__mutmut_12': xǁOpenObserveClientǁget_search_history__mutmut_12, 
        'xǁOpenObserveClientǁget_search_history__mutmut_13': xǁOpenObserveClientǁget_search_history__mutmut_13, 
        'xǁOpenObserveClientǁget_search_history__mutmut_14': xǁOpenObserveClientǁget_search_history__mutmut_14, 
        'xǁOpenObserveClientǁget_search_history__mutmut_15': xǁOpenObserveClientǁget_search_history__mutmut_15, 
        'xǁOpenObserveClientǁget_search_history__mutmut_16': xǁOpenObserveClientǁget_search_history__mutmut_16, 
        'xǁOpenObserveClientǁget_search_history__mutmut_17': xǁOpenObserveClientǁget_search_history__mutmut_17, 
        'xǁOpenObserveClientǁget_search_history__mutmut_18': xǁOpenObserveClientǁget_search_history__mutmut_18, 
        'xǁOpenObserveClientǁget_search_history__mutmut_19': xǁOpenObserveClientǁget_search_history__mutmut_19, 
        'xǁOpenObserveClientǁget_search_history__mutmut_20': xǁOpenObserveClientǁget_search_history__mutmut_20, 
        'xǁOpenObserveClientǁget_search_history__mutmut_21': xǁOpenObserveClientǁget_search_history__mutmut_21, 
        'xǁOpenObserveClientǁget_search_history__mutmut_22': xǁOpenObserveClientǁget_search_history__mutmut_22, 
        'xǁOpenObserveClientǁget_search_history__mutmut_23': xǁOpenObserveClientǁget_search_history__mutmut_23, 
        'xǁOpenObserveClientǁget_search_history__mutmut_24': xǁOpenObserveClientǁget_search_history__mutmut_24, 
        'xǁOpenObserveClientǁget_search_history__mutmut_25': xǁOpenObserveClientǁget_search_history__mutmut_25, 
        'xǁOpenObserveClientǁget_search_history__mutmut_26': xǁOpenObserveClientǁget_search_history__mutmut_26, 
        'xǁOpenObserveClientǁget_search_history__mutmut_27': xǁOpenObserveClientǁget_search_history__mutmut_27, 
        'xǁOpenObserveClientǁget_search_history__mutmut_28': xǁOpenObserveClientǁget_search_history__mutmut_28, 
        'xǁOpenObserveClientǁget_search_history__mutmut_29': xǁOpenObserveClientǁget_search_history__mutmut_29, 
        'xǁOpenObserveClientǁget_search_history__mutmut_30': xǁOpenObserveClientǁget_search_history__mutmut_30, 
        'xǁOpenObserveClientǁget_search_history__mutmut_31': xǁOpenObserveClientǁget_search_history__mutmut_31, 
        'xǁOpenObserveClientǁget_search_history__mutmut_32': xǁOpenObserveClientǁget_search_history__mutmut_32, 
        'xǁOpenObserveClientǁget_search_history__mutmut_33': xǁOpenObserveClientǁget_search_history__mutmut_33, 
        'xǁOpenObserveClientǁget_search_history__mutmut_34': xǁOpenObserveClientǁget_search_history__mutmut_34, 
        'xǁOpenObserveClientǁget_search_history__mutmut_35': xǁOpenObserveClientǁget_search_history__mutmut_35, 
        'xǁOpenObserveClientǁget_search_history__mutmut_36': xǁOpenObserveClientǁget_search_history__mutmut_36, 
        'xǁOpenObserveClientǁget_search_history__mutmut_37': xǁOpenObserveClientǁget_search_history__mutmut_37, 
        'xǁOpenObserveClientǁget_search_history__mutmut_38': xǁOpenObserveClientǁget_search_history__mutmut_38, 
        'xǁOpenObserveClientǁget_search_history__mutmut_39': xǁOpenObserveClientǁget_search_history__mutmut_39, 
        'xǁOpenObserveClientǁget_search_history__mutmut_40': xǁOpenObserveClientǁget_search_history__mutmut_40, 
        'xǁOpenObserveClientǁget_search_history__mutmut_41': xǁOpenObserveClientǁget_search_history__mutmut_41, 
        'xǁOpenObserveClientǁget_search_history__mutmut_42': xǁOpenObserveClientǁget_search_history__mutmut_42, 
        'xǁOpenObserveClientǁget_search_history__mutmut_43': xǁOpenObserveClientǁget_search_history__mutmut_43, 
        'xǁOpenObserveClientǁget_search_history__mutmut_44': xǁOpenObserveClientǁget_search_history__mutmut_44
    }
    
    def get_search_history(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenObserveClientǁget_search_history__mutmut_orig"), object.__getattribute__(self, "xǁOpenObserveClientǁget_search_history__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_search_history.__signature__ = _mutmut_signature(xǁOpenObserveClientǁget_search_history__mutmut_orig)
    xǁOpenObserveClientǁget_search_history__mutmut_orig.__name__ = 'xǁOpenObserveClientǁget_search_history'

    @resilient(
        fallback=False,
        suppress=(Exception,),
        reraise=False,
        context={"method": "test_connection"},
    )
    async def test_connection(self) -> bool:
        """Test connection to OpenObserve.

        Uses the @resilient decorator for standardized error handling and logging.

        Returns:
            True if connection successful, False otherwise

        """
        # Try to list streams as a simple test
        await self.list_streams()
        return True


# <3 🧱🤝🔌🪄
