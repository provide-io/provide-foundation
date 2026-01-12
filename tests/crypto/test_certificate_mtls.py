#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
import pytest

# Fixtures will be available via tests.fixtures through conftest.py
# from tests.fixtures.crypto import client_cert, server_cert


class TestCertificateMTLS(FoundationTestCase):
    """Test certificate mTLS functionality."""

    @pytest.mark.asyncio
    async def test_load_client_certificate(self, client_cert: Any) -> None:
        """Ensure the client certificate loads correctly."""
        assert client_cert.subject, "Client certificate subject should not be empty"
        assert client_cert.issuer, "Client certificate issuer should not be empty"

    @pytest.mark.asyncio
    async def test_load_server_certificate(self, server_cert: Any) -> None:
        """Ensure the server certificate loads correctly."""
        assert server_cert.subject, "Server certificate subject should not be empty"
        assert server_cert.issuer, "Server certificate issuer should not be empty"


# 🧱🏗️🔚
