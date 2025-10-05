from __future__ import annotations

from provide.foundation.concurrency.locks import LockManager, get_lock_manager

"""Central lock registry for Foundation.

Registers all Foundation locks with the LockManager to ensure proper
lock ordering and prevent deadlocks. All locks must be registered here
with appropriate order numbers.

Lock Ordering Convention:
- 0-99: Infrastructure (streams, system resources)
- 100-199: Core components (logger, hub, registry)
- 200-299: State management
- 300-399: Application logic
- 400-499: Utilities and helpers
"""

# Lock order constants
LOCK_ORDER_STREAM = 10
LOCK_ORDER_LOGGER_LAZY = 100
LOCK_ORDER_HUB_INIT = 110
LOCK_ORDER_REGISTRY = 120
LOCK_ORDER_STATE = 200
LOCK_ORDER_CACHE = 400
LOCK_ORDER_RATELIMIT = 410


def register_foundation_locks() -> LockManager:
    """Register all Foundation locks with the lock manager.

    This should be called once during Foundation initialization.

    Returns:
        The global LockManager instance

    """
    manager = get_lock_manager()

    # Register locks in order
    manager.register_lock(
        name="foundation.stream",
        order=LOCK_ORDER_STREAM,
        description="Log stream management lock",
    )

    manager.register_lock(
        name="foundation.logger.lazy",
        order=LOCK_ORDER_LOGGER_LAZY,
        description="Logger lazy initialization lock",
    )

    manager.register_lock(
        name="foundation.hub.init",
        order=LOCK_ORDER_HUB_INIT,
        description="Hub initialization lock",
    )

    manager.register_lock(
        name="foundation.registry",
        order=LOCK_ORDER_REGISTRY,
        description="Component registry lock",
    )

    manager.register_lock(
        name="foundation.state",
        order=LOCK_ORDER_STATE,
        description="State management lock",
    )

    manager.register_lock(
        name="foundation.cache",
        order=LOCK_ORDER_CACHE,
        description="Caching utilities lock",
    )

    manager.register_lock(
        name="foundation.ratelimit",
        order=LOCK_ORDER_RATELIMIT,
        description="Rate limiting lock",
    )

    return manager
