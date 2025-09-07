# Async Application Patterns

Integration patterns for asynchronous and concurrent applications.

### AsyncIO Integration

```python
import asyncio
import signal
import sys
from contextlib import AsyncExitStack
from typing import Any, Optional

from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

class AsyncApplicationBase:
    """Base class for async applications with comprehensive logging."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"app.{name}")
        self.exit_stack = AsyncExitStack()
        self._shutdown_event = asyncio.Event()
        self._tasks: set[asyncio.Task] = set()
        
        # Setup telemetry
        self._setup_logging()
        
        # Setup signal handlers
        self._setup_signal_handlers()
    
    def _setup_logging(self):
        """Setup application logging."""
        config = TelemetryConfig(
            service_name=self.name,
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="key_value",
                das_emoji_prefix_enabled=True,
                module_levels={
                    f"app.{self.name}": "DEBUG",
                    "asyncio": "WARNING"
                }
            )
        )
        setup_telemetry(config)
    
    def _setup_signal_handlers(self):
        """Setup graceful shutdown signal handlers."""
        if sys.platform != "win32":
            loop = asyncio.get_event_loop()
            
            for sig in (signal.SIGTERM, signal.SIGINT):
                loop.add_signal_handler(
                    sig, 
                    lambda s=sig: asyncio.create_task(self._signal_handler(s))
                )
    
    async def _signal_handler(self, sig):
        """Handle shutdown signals."""
        self.logger.info("Shutdown signal received",
            domain="app",
            action="shutdown",
            status="started",
            signal=sig.name
        )
        self._shutdown_event.set()
    
    async def start(self):
        """Start the application."""
        self.logger.info("Application starting",
            domain="app", 
            action="startup",
            status="started",
            app_name=self.name
        )
        
        try:
            async with self.exit_stack:
                # Initialize application components
                await self.initialize()
                
                # Start background tasks
                await self.start_background_tasks()
                
                self.logger.info("Application started successfully",
                    domain="app",
                    action="startup", 
                    status="success",
                    app_name=self.name,
                    active_tasks=len(self._tasks)
                )
                
                # Wait for shutdown signal
                await self._shutdown_event.wait()
                
                self.logger.info("Application shutdown initiated",
                    domain="app",
                    action="shutdown",
                    status="started", 
                    app_name=self.name
                )
                
        except Exception as e:
            self.logger.error("Application startup failed",
                domain="app",
                action="startup",
                status="error",
                app_name=self.name,
                error_type=type(e).__name__,
                error_message=str(e)
            )
            raise
        finally:
            await self.cleanup()
    
    async def initialize(self):
        """Initialize application components. Override in subclasses."""
        pass
    
    async def start_background_tasks(self):
        """Start background tasks. Override in subclasses."""
        pass
    
    async def cleanup(self):
        """Cleanup application resources."""
        self.logger.info("Application cleanup started",
            domain="app",
            action="cleanup",
            status="started",
            app_name=self.name
        )
        
        # Cancel all background tasks
        for task in self._tasks:
            if not task.done():
                task.cancel()
        
        # Wait for tasks to complete
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        
        self.logger.info("Application cleanup completed",
            domain="app", 
            action="cleanup",
            status="success",
            app_name=self.name
        )
    
    def create_task(self, coro, *, name: Optional[str] = None) -> asyncio.Task:
        """Create and track a background task."""
        task = asyncio.create_task(coro, name=name)
        self._tasks.add(task)
        
        # Remove completed tasks
        def remove_task(t):
            self._tasks.discard(t)
        
        task.add_done_callback(remove_task)
        
        return task

# Example application
class DataProcessorApp(AsyncApplicationBase):
    """Example async application with background processing."""
    
    async def initialize(self):
        """Initialize data processor components."""
        self.logger.info("Initializing data processor",
            domain="app",
            action="initialize",
            status="started"
        )
        
        # Initialize components (databases, queues, etc.)
        await self._init_database()
        await self._init_message_queue()
        
        self.logger.info("Data processor initialized",
            domain="app",
            action="initialize", 
            status="success"
        )
    
    async def start_background_tasks(self):
        """Start background processing tasks."""
        self.logger.info("Starting background tasks",
            domain="app",
            action="start_tasks",
            status="started"
        )
        
        # Start various background tasks
        self.create_task(self.data_processor_loop(), name="data_processor")
        self.create_task(self.health_check_loop(), name="health_check")
        self.create_task(self.metrics_reporter_loop(), name="metrics_reporter")
        
        self.logger.info("Background tasks started",
            domain="app",
            action="start_tasks",
            status="success",
            task_count=len(self._tasks)
        )
    
    async def _init_database(self):
        """Initialize database connection."""
        self.logger.debug("Initializing database connection",
            domain="database",
            action="connect",
            status="started"
        )
        
        # Mock database initialization
        await asyncio.sleep(0.1)
        
        self.logger.info("Database connection established",
            domain="database", 
            action="connect",
            status="success"
        )
    
    async def _init_message_queue(self):
        """Initialize message queue connection."""  
        self.logger.debug("Connecting to message queue",
            domain="queue",
            action="connect",
            status="started"
        )
        
        # Mock queue initialization
        await asyncio.sleep(0.1)
        
        self.logger.info("Message queue connected",
            domain="queue",
            action="connect", 
            status="success"
        )
    
    async def data_processor_loop(self):
        """Main data processing loop."""
        self.logger.info("Data processor loop started",
            domain="processor",
            action="start",
            status="started"
        )
        
        try:
            while not self._shutdown_event.is_set():
                try:
                    # Process batch of data
                    batch_size = await self.process_data_batch()
                    
                    if batch_size > 0:
                        self.logger.debug("Data batch processed",
                            domain="processor",
                            action="process",
                            status="success", 
                            batch_size=batch_size
                        )
                    
                    # Wait before next batch
                    await asyncio.sleep(1.0)
                    
                except Exception as e:
                    self.logger.error("Data processing error",
                        domain="processor",
                        action="process",
                        status="error",
                        error_type=type(e).__name__,
                        error_message=str(e)
                    )
                    await asyncio.sleep(5.0)  # Back off on error
                    
        except asyncio.CancelledError:
            self.logger.info("Data processor loop cancelled",
                domain="processor", 
                action="stop",
                status="cancelled"
            )
            raise
    
    async def health_check_loop(self):
        """Health check reporting loop."""
        while not self._shutdown_event.is_set():
            try:
                # Perform health checks
                health_status = await self.check_system_health()
                
                self.logger.info("Health check completed",
                    domain="health",
                    action="check",
                    status="success" if health_status else "warning",
                    healthy=health_status
                )
                
                await asyncio.sleep(30.0)  # Check every 30 seconds
                
            except asyncio.CancelledError:
                self.logger.info("Health check loop cancelled",
                    domain="health",
                    action="stop", 
                    status="cancelled"
                )
                raise
            except Exception as e:
                self.logger.error("Health check error",
                    domain="health",
                    action="check",
                    status="error",
                    error_type=type(e).__name__,
                    error_message=str(e)
                )
                await asyncio.sleep(10.0)
    
    async def metrics_reporter_loop(self):
        """Metrics reporting loop."""
        while not self._shutdown_event.is_set():
            try:
                # Collect and report metrics
                metrics = await self.collect_metrics()
                
                self.logger.info("Metrics reported",
                    domain="metrics",
                    action="report",
                    status="success",
                    **metrics
                )
                
                await asyncio.sleep(60.0)  # Report every minute
                
            except asyncio.CancelledError:
                self.logger.info("Metrics reporter cancelled",
                    domain="metrics", 
                    action="stop",
                    status="cancelled"
                )
                raise
            except Exception as e:
                self.logger.error("Metrics reporting error",
                    domain="metrics",
                    action="report",
                    status="error",
                    error_type=type(e).__name__,
                    error_message=str(e)
                )
                await asyncio.sleep(30.0)
    
    async def process_data_batch(self) -> int:
        """Process a batch of data."""
        # Mock data processing
        await asyncio.sleep(0.1)
        return 10  # Mock batch size
    
    async def check_system_health(self) -> bool:
        """Check system health."""
        # Mock health check
        return True
    
    async def collect_metrics(self) -> dict[str, Any]:
        """Collect system metrics."""
        # Mock metrics collection
        return {
            "active_tasks": len(self._tasks),
            "memory_usage_mb": 256,
            "cpu_usage_percent": 15.5
        }

# Run the application
async def main():
    app = DataProcessorApp("data-processor")
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
```