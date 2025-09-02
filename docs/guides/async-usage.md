# 🧑‍💻 Guides

## Asynchronous Usage

`provide.foundation` is designed from the ground up to be fully compatible with modern asynchronous Python applications using `asyncio`. The logging calls are non-blocking and thread-safe, ensuring that they won't become a bottleneck in your async code.

### Logging in an `asyncio` Application

You can use the global `logger` instance directly within your `async` functions just as you would in synchronous code. No special configuration or handling is required.

Here is an example of a simple async application with multiple concurrent tasks that are all logging messages.

```python
import asyncio
import random
from provide.foundation import logger

async def worker(name: str):
    """A simulated worker task that performs some work and logs its progress."""
    log = logger.get_logger(f"worker.{name}") # Use a named logger for clarity
    log.info("Starting work")
    
    # Simulate some async work with a random delay
    delay = random.uniform(0.5, 2.0)
    await asyncio.sleep(delay)
    
    # Log completion with structured context
    log.info(
        "Work complete",
        duration_ms=int(delay * 1000),
        status="success",
    )

async def main():
    """Run several worker tasks concurrently."""
    logger.info("Main application starting, dispatching workers...")
    
    # Create and run tasks concurrently
    tasks = [
        worker("alpha"),
        worker("bravo"),
        worker("charlie"),
    ]
    await asyncio.gather(*tasks)
    
    logger.info("All workers have finished.")

if __name__ == "__main__":
    # To see the concurrent nature of the logs, you might want to enable timestamps
    # from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig
    # setup_telemetry(TelemetryConfig(logging=LoggingConfig(omit_timestamp=False)))
    
    asyncio.run(main())

```

### Understanding the Output

When you run this script, you will see the log messages from `main` and all three `worker` tasks interleaved as they execute concurrently. The use of named loggers ensures you can easily tell which message came from which task.

```
[▶️] Main application starting, dispatching workers...
[👷] Starting work
[👷] Starting work
[👷] Starting work
[✅] Work complete duration_ms=867 status=success
[✅] Work complete duration_ms=1523 status=success
[✅] Work complete duration_ms=1981 status=success
[▶️] All workers have finished.
```
*(Note: The emojis for the named loggers `worker.alpha`, `worker.bravo`, and `worker.charlie` might deterministically hash to the same emoji if their names are similar, as seen with `👷` here. This is expected behavior.)*

### Graceful Shutdown

While `provide.foundation` does not currently require an explicit shutdown for standard console logging, some advanced configurations (especially those involving network-based log shippers, which may be supported in the future) might require a graceful shutdown process.

The library provides an `async` function, `shutdown_foundation_telemetry`, for this purpose.

```python
import asyncio
from provide.foundation import logger, shutdown_foundation_telemetry

async def main():
    logger.info("Application running...")
    # ... your application logic ...
    logger.info("Application shutting down.")
    await shutdown_foundation_telemetry()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Caught interrupt, shutting down.")
        # Ensure shutdown is called even on interrupt
        asyncio.run(shutdown_foundation_telemetry())
```

While not strictly necessary for basic usage, adopting this pattern can make your application more robust and ready for future enhancements to the telemetry system.

---

Next, learn how to handle and log errors effectively in the [**Exception Logging**](./exception-logging.md) guide.
