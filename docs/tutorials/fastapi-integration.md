# Tutorials

## Logging in a FastAPI Web Application

This tutorial will walk you through integrating `provide.foundation` into a simple **FastAPI** web application, step by step. We will cover everything from setting up the application to logging requests and timing business logic.

By the end of this tutorial, you will have a solid foundation for producing beautiful, structured, and semantic logs in any web application.

### Prerequisites

Before you begin, make sure you have the necessary libraries installed:

```bash
pip install provide-foundation fastapi "uvicorn[standard]"
```

### Step 1: Basic FastAPI App Setup

First, create a file named `main.py` and set up a basic FastAPI application.

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### Step 2: Initializing the Logger on Startup

The best place to configure `provide.foundation` is when your application starts. We will use FastAPI's `lifespan` event to ensure `setup_telemetry` is called only once when the server boots up.

In this step, we will also enable the `http` and `database` semantic layers.

```python
# main.py
import contextlib
from fastapi import FastAPI

from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

# Set up the logger within the lifespan event
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print("Setting up telemetry on application startup...")
    config = TelemetryConfig(
        service_name="my-fastapi-app",
        logging=LoggingConfig(
            default_level="INFO",
            # Enable the http and database semantic layers
            enabled_semantic_layers=["http", "database"],
        ),
    )
    setup_telemetry(config)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### Step 3: Logging Requests with Middleware

Automatically logging every incoming request and its response is an incredibly powerful pattern. We can achieve this using FastAPI middleware.

```python
# main.py (append to previous code)
import time
from fastapi import Request
from provide.foundation import logger

# ... (FastAPI setup and lifespan from above)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000

    logger.info(
        "HTTP request handled",
        **{
            "http.method": request.method,
            "http.url": str(request.url),
            "http.status_code": response.status_code,
            "http.response_time_ms": round(duration_ms, 2),
            "client.address": request.client.host,
        },
    )

    return response

# ... (root and endpoints below)
```

### Step 4: Logging in Endpoints

Next, we'll add a `/users` endpoint to create a user. In this endpoint, we will use `timed_block` to time our business logic and log both validation errors and success events.

```python
# main.py (append to previous code)
from fastapi import Body
from typing import Annotated

from provide.foundation.errors import ValidationError
from provide.foundation.utils.timing import timed_block

# ... (all previous code from above)

@app.post("/users")
def create_user(username: Annotated[str, Body()])-> dict:
    """An endpoint to create a new user."""
    with timed_block(logger, "create_user_endpoint", initial_kvs={"username": username}) as ctx:
        # 1. Validate input
        if not username or len(username) < 3:
            # Log the validation failure
            logger.warning(
                "Invalid username provided",
                domain="validation",
                action="input",
                status="failure",
                username=username,
            )
            # This error will be caught and turned into a 400 response
            raise ValidationError("Username must be at least 3 characters long")

        # 2. Simulate a database operation
        ctx["db_operation"] = "insert"
        logger.info(
            "User created in database",
            **{
                "db.system": "postgres",
                "db.operation": "insert",
                "db.table": "users",
                "db.outcome": "success",
            },
        )

        return {"status": "user created", "username": username}

# An exception handler to make FastAPI handle our ValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message},
    )
```

### Step 5: Running the App and Seeing the Logs

Now our full application is ready. Run it using `uvicorn` in your terminal:

```bash
uvicorn main:app --reload
```

Next, send some requests to your API using `curl` or a web browser.

**A successful request:**

```bash
curl -X POST -H "Content-Type: application/json" -d '"provide-user"' http://127.0.0.1:8000/users
```

Your console logs will look like this:

```
[🐘][➕][✅] User created in database db.table=users
[▶️] create_user_endpoint completed username=provide-user db_operation=insert duration_seconds=0.0
[➡️][✅] HTTP request handled http.url=http://127.0.0.1:8000/users http.response_time_ms=2.5 client.address=127.0.0.1
```

**A failing request (validation error):**

```bash
curl -X POST -H "Content-Type: application/json" -d '"a"' http://127.0.0.1:8000/users
```

Your console logs will look like this:

```
[🛡️][➡️][❌] Invalid username provided username=a
[▶️] create_user_endpoint completed username=a duration_seconds=0.0
[➡️][⚠️CLIENT] HTTP request handled http.url=http://127.0.0.1:8000/users http.response_time_ms=1.5 client.address=127.0.0.1
```

### Conclusion

Congratulations! In this tutorial, you have learned how to:

*   Configure `provide.foundation` on FastAPI application startup.
*   Automatically log all HTTP requests using middleware.
*   Time the performance of specific operations using `timed_block`.
*   Log semantic events related to your business logic (validation, success).

These patterns provide a powerful foundation for robust, observable logging in any web application.