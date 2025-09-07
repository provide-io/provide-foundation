# Basic Context Binding

Fundamental context operations and simple context management patterns.

## Overview

Context management enables you to:

- 🔗 **Bind Context** - Attach metadata to all logs in a scope
- 🌍 **Global Context** - Set application-wide context
- 🧵 **Thread-Local Context** - Maintain context per thread
- 🔄 **Context Propagation** - Pass context across boundaries
- 📦 **Context Inheritance** - Build hierarchical context

## Basic Context Binding

### Temporary Context

```python
from provide.foundation import logger

# Add context for a block of code
with logger.bind(request_id="req_123", user_id="user_456"):
    logger.info("processing_started")
    # All logs in this block include request_id and user_id
    
    process_request()
    
    logger.info("processing_completed")
    # Still includes the context

# Context is removed here
logger.info("other_operation")  # No request_id or user_id
```

### Permanent Context

```python
# Create logger with permanent context
api_logger = logger.bind(
    service="payment-api",
    version="2.1.0",
    environment="production"
)

# All logs from api_logger include the bound context
api_logger.info("service_started")
api_logger.info("request_processed", endpoint="/charge")
```

### Nested Context

```python
# Context can be nested and combined
with logger.bind(request_id="req_001"):
    logger.info("request_received")
    
    with logger.bind(user_id="usr_123"):
        logger.info("user_authenticated")
        # Has both request_id and user_id
        
        with logger.bind(transaction_id="txn_456"):
            logger.info("transaction_started")
            # Has all three IDs
```

