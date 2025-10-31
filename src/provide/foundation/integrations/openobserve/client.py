#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OpenObserve API client using Foundation's transport system."""

from __future__ import annotations

from provide.foundation.integrations.openobserve.client_base import OpenObserveClientBase
from provide.foundation.integrations.openobserve.client_metrics_mixin import (
    MetricsOperationsMixin,
)
from provide.foundation.integrations.openobserve.client_search_mixin import (
    SearchOperationsMixin,
)


class OpenObserveClient(SearchOperationsMixin, MetricsOperationsMixin, OpenObserveClientBase):
    """Async client for interacting with OpenObserve API.

    Uses Foundation's transport system for all HTTP operations.
    Combines search/streams operations and Prometheus metrics API.
    """


# 🧱🏗️🔚
