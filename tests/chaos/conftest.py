#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Chaos testing configuration and fixtures for provide-foundation.

Configures Hypothesis settings and provides chaos-specific fixtures."""

from __future__ import annotations

from hypothesis import HealthCheck, Phase, Verbosity, settings
import pytest

# Register Hypothesis profiles for chaos testing
settings.register_profile(
    "chaos",
    max_examples=1000,
    verbosity=Verbosity.verbose,
    deadline=None,  # Disable for async tests
    report_multiple_bugs=True,
    phases=[Phase.explicit, Phase.reuse, Phase.generate, Phase.shrink],
    print_blob=True,  # Enable statistics printing
    suppress_health_check=[HealthCheck.too_slow],  # Suppress slow input generation warnings
)

settings.register_profile(
    "chaos_ci",
    max_examples=100,
    verbosity=Verbosity.normal,
    deadline=10000,
    report_multiple_bugs=False,
    phases=[Phase.explicit, Phase.reuse, Phase.generate, Phase.shrink],
    print_blob=True,  # Enable statistics printing
    suppress_health_check=[HealthCheck.too_slow],
)

settings.register_profile(
    "chaos_smoke",
    max_examples=20,
    verbosity=Verbosity.quiet,
    deadline=5000,
    report_multiple_bugs=False,
    phases=[Phase.explicit, Phase.generate],
    print_blob=True,  # Enable statistics printing
    suppress_health_check=[HealthCheck.too_slow],  # Suppress slow input generation for fast iteration
)


@pytest.fixture(scope="session", autouse=True)
def configure_hypothesis_for_chaos() -> None:
    """Auto-configure Hypothesis for chaos testing."""
    # Load chaos_smoke profile by default for faster dev iterations
    # Use --hypothesis-profile=chaos for full testing
    # Use --hypothesis-profile=chaos_ci for CI
    settings.load_profile("chaos_smoke")


# 🧱🏗️🔚
