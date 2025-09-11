# Celery Integration with provide.foundation

This directory contains a comprehensive example of integrating provide.foundation structured logging with Celery task processing. The example is split into multiple focused modules for better maintainability.

## Installation Requirements

```bash
# Install Celery (required)
pip install celery

# Optional: Redis for production mode
# For demo mode, Redis is not required (uses in-memory broker)
```

## File Structure

- **`01_setup_and_config.py`** - Celery app configuration and logging setup
- **`02_metrics_and_signals.py`** - Task metrics tracking and signal handlers  
- **`03_tasks.py`** - Example task definitions with real-world patterns
- **`04_demo_runner.py`** - Demo runner and workflow orchestration

## Quick Start

### Demo Mode (No Redis Required)

```bash
# Run with in-memory broker for demonstration
python examples/integration/celery/04_demo_runner.py --demo
```

### Production Mode (Requires Redis)

```bash
# 1. Start Redis
redis-server

# 2. Start Celery worker
celery -A examples.integration.celery.01_setup_and_config worker --loglevel=info --pool=solo

# 3. Run the demo
python examples/integration/celery/04_demo_runner.py
```

## Featured Patterns

### 1. **Payment Processing with Retries** (`process_payment`)
- Automatic retry with exponential backoff
- Transient error handling
- Detailed transaction logging

### 2. **Report Generation with Progress** (`generate_report`) 
- Long-running task with progress tracking
- Real-time status updates
- Step-by-step execution logging

### 3. **Multi-Channel Notifications** (`send_notification`)
- Parallel delivery across multiple channels (email, SMS, push)
- Per-channel success/failure tracking
- Delivery confirmation logging

### 4. **Batch Processing** (`process_batch_data`)
- Item-level error handling
- Success rate calculation
- Failed item tracking and reporting

### 5. **Data Cleanup Operations** (`cleanup_old_data`)
- Scheduled maintenance tasks
- Space utilization tracking
- Multi-category cleanup reporting

### 6. **Task Workflows**
- Task chains (sequential execution)
- Parallel task groups
- Complex workflow orchestration

## Key Features Demonstrated

- **📊 Comprehensive Metrics**: Task execution tracking, success rates, performance metrics
- **🔄 Signal Handlers**: Worker lifecycle monitoring, health checks
- **⚡ Progress Tracking**: Real-time progress updates for long-running tasks
- **🔥 Retry Logic**: Exponential backoff with detailed retry logging
- **🎯 Error Handling**: Graceful error handling with context preservation
- **📈 Health Monitoring**: Periodic worker health reporting
- **🔗 Task Workflows**: Chains, groups, and complex task orchestration

## Structured Logging Output

All task operations produce structured JSON logs with rich context:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456Z",
  "level": "info", 
  "event": "task_completed",
  "task_id": "abc123",
  "task_name": "process_payment",
  "duration_ms": 1250.5,
  "success": true,
  "order_id": "order_123",
  "amount": 99.99,
  "transaction_id": "txn_order_123_1705312245"
}
```

## Configuration

The example supports extensive configuration through environment variables:

```bash
# Service identification  
export PROVIDE_SERVICE_NAME="celery-worker"
export PROVIDE_LOG_LEVEL="INFO"

# Logging format
export PROVIDE_LOG_CONSOLE_FORMATTER="json"

# Module-specific log levels
export PROVIDE_LOG_MODULE_LEVELS="celery.worker:INFO,celery.task:INFO"
```

## Metrics and Monitoring

The example includes a comprehensive metrics system that tracks:

- Task execution counts
- Average execution duration
- Success/failure rates  
- Retry counts
- Worker health status

Metrics are logged periodically and on worker shutdown for operational visibility.

## Integration Notes

This example demonstrates how to:

1. **Configure Celery** with provide.foundation logging
2. **Set up signal handlers** for comprehensive task lifecycle tracking
3. **Implement retry logic** with structured logging
4. **Track metrics** across task executions
5. **Monitor worker health** with periodic reporting
6. **Handle errors gracefully** while preserving context
7. **Use task workflows** (chains, groups, chords)

The patterns shown here can be adapted for production use cases requiring reliable task processing with comprehensive observability.