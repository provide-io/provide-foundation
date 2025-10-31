#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

from provide.foundation.errors.decorators import resilient
from provide.foundation.hub.categories import ComponentCategory
from provide.foundation.profiling.defaults import DEFAULT_PROFILING_SAMPLE_RATE
from provide.foundation.profiling.metrics import ProfileMetrics
from provide.foundation.profiling.processor import ProfilingProcessor

if TYPE_CHECKING:
    from provide.foundation.hub.manager import Hub

"""Hub component for profiling management.

Provides Foundation Hub integration for performance profiling with
automatic registration and lifecycle management.
"""


class ProfilingComponent:
    """Hub component for managing Foundation performance profiling.

    Integrates profiling functionality into Foundation's Hub architecture,
    providing centralized configuration and lifecycle management for
    performance monitoring.

    Example:
        >>> from provide.foundation.hub import Hub
        >>> from provide.foundation.profiling import register_profiling
        >>>
        >>> hub = Hub()
        >>> register_profiling(hub)
        >>> profiler = hub.get_component("profiler")
        >>> profiler.enable()

        >>> # Metrics are automatically collected
        >>> metrics = profiler.get_metrics()
        >>> print(f"Throughput: {metrics.messages_per_second:.0f} msg/sec")

    """

    def __init__(self, sample_rate: float = DEFAULT_PROFILING_SAMPLE_RATE) -> None:
        """Initialize profiling component.

        Args:
            sample_rate: Fraction of messages to sample for metrics

        """
        self.processor = ProfilingProcessor(sample_rate=sample_rate)
        self.enabled = False

    @resilient(
        fallback=None,
        context_provider=lambda: {"component": "profiler"},
    )
    def enable(self) -> None:
        """Enable profiling metrics collection.

        This method is safe to call multiple times - it will not
        re-enable if already enabled.

        """
        if self.enabled:
            return

        # Enable the processor
        self.processor.enable()
        self.enabled = True

        # Log that profiling is enabled using Foundation's logger
        try:
            from provide.foundation import logger

            logger.info("Profiling enabled", emoji="📊", component="profiler")
        except (ImportError, AttributeError):
            # Don't fail if logging isn't available or not fully initialized
            pass

    @resilient(
        fallback=None,
        context_provider=lambda: {"component": "profiler"},
    )
    def disable(self) -> None:
        """Disable profiling metrics collection."""
        if not self.enabled:
            return

        # Disable the processor
        self.processor.disable()
        self.enabled = False

        # Log that profiling is disabled
        try:
            from provide.foundation import logger

            logger.info("Profiling disabled", emoji="📊", component="profiler")
        except (ImportError, AttributeError):
            # Don't fail if logging isn't available or not fully initialized
            pass

    def get_metrics(self) -> ProfileMetrics:
        """Get current profiling metrics.

        Returns:
            Current ProfileMetrics instance with collected data

        """
        return self.processor.get_metrics()

    @resilient(
        fallback=None,
        context_provider=lambda: {"component": "profiler", "operation": "reset"},
    )
    def reset(self) -> None:
        """Reset profiling metrics to initial values.

        Useful for testing and periodic metric collection.

        """
        self.processor.reset()

        # Log the reset operation
        try:
            from provide.foundation import logger

            logger.debug("Profiling metrics reset", emoji="🔄", component="profiler")
        except (ImportError, AttributeError):
            # Don't fail if logging isn't available or not fully initialized
            pass

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = "enabled" if self.enabled else "disabled"
        sample_rate = self.processor.sample_rate
        return f"ProfilingComponent(enabled={status}, sample_rate={sample_rate})"


@resilient(
    fallback=None,
    context_provider=lambda: {"operation": "register_profiling"},
)
def register_profiling(hub: Hub, sample_rate: float = DEFAULT_PROFILING_SAMPLE_RATE) -> None:
    """Register profiling component with Hub and add CLI command.

    Args:
        hub: The Hub instance to register with
        sample_rate: Sampling rate for metrics collection

    Example:
        >>> from provide.foundation.hub import Hub
        >>> from provide.foundation.profiling.component import register_profiling
        >>>
        >>> hub = Hub()
        >>> register_profiling(hub)

    """
    # Create and register the profiling component instance
    profiler = ProfilingComponent(sample_rate=sample_rate)

    # Register directly with the hub's component registry
    hub._component_registry.register(
        name="profiler",
        value=profiler,
        dimension=ComponentCategory.COMPONENT.value,
        metadata={"type": "profiling", "sample_rate": sample_rate},
    )

    # Register CLI command
    try:
        from provide.foundation.profiling.cli import register_profile_command

        register_profile_command(hub)

    except ImportError:
        # CLI components may not be available in all environments
        pass


# 🧱🏗️🔚
