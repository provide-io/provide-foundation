# Cookbook

Welcome to the provide.foundation Cookbook! This section contains practical recipes, examples, and patterns for using provide.foundation in real-world applications.

## What You'll Find Here

The cookbook is organized into three main sections:

### 📚 [Recipes](recipes/index.md)

Step-by-step guides for integrating provide.foundation with popular frameworks and platforms:

- **Web Frameworks**: FastAPI, Django, Flask integration
- **Task Queues**: Celery and background job logging
- **Infrastructure**: Docker, Kubernetes logging strategies
- **CI/CD**: Pipeline integration and test logging
- **Testing**: Comprehensive testing strategies

### 💡 [Examples](examples/index.md)

Complete, working examples of different application types:

- **Web Applications**: Full-stack app with structured logging
- **CLI Tools**: Command-line applications with rich output
- **Data Pipelines**: ETL and data processing with telemetry
- **Microservices**: Distributed system logging
- **Machine Learning**: Model training and inference logging
- **Async Services**: High-performance async application patterns

### 🎯 [Patterns](patterns/index.md)

Design patterns and best practices:

- **Error Boundaries**: Graceful error handling
- **Context Propagation**: Request tracing across services
- **Performance Monitoring**: Metrics and profiling
- **Audit Logging**: Compliance and security logging

## Quick Examples

### Web Application Logging

```python
from provide.foundation import logger
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("http_request_started", 
                method=request.method,
                path=request.url.path)
    
    response = await call_next(request)
    
    logger.info("http_request_completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code)
    
    return response
```

### CLI Tool with Rich Output

```python
from provide.foundation.cli import register_command
from provide.foundation import pout, perr, logger

@register_command("process.data")
def process_data(input_file: str, output_file: str):
    """Process data with progress tracking."""
    
    logger.info("data_processing_started", 
                input=input_file, 
                output=output_file)
    
    try:
        # Process data...
        pout(f"✅ Processed {input_file} → {output_file}")
        logger.info("data_processing_completed")
    except Exception as e:
        perr(f"❌ Failed to process: {e}")
        logger.error("data_processing_failed", error=str(e))
        raise
```

### Async Service Pattern

```python
import asyncio
from provide.foundation import logger

async def process_item(item_id: str):
    async with logger.bind(item_id=item_id):
        logger.debug("item_processing_started")
        
        try:
            # Async processing...
            await asyncio.sleep(1)
            logger.info("item_processing_completed")
        except Exception as e:
            logger.error("item_processing_failed", error=str(e))
            raise
```

## Navigation

- **New to provide.foundation?** Start with [Getting Started](../getting-started/index.md)
- **Looking for API docs?** Check the [API Reference](../api/index.md)
- **Need help?** Visit [Troubleshooting](../troubleshooting/index.md)

## Contributing

Have a great recipe or pattern? We'd love to include it! See our [Contributing Guide](../development/contributing.md) for details.