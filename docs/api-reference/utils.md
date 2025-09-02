# Utilities API

The `provide.foundation.utils` module provides utility functions for timing, performance measurement, and other common operations.

## Overview

The utilities module provides:
- Context managers for timing code blocks
- Performance measurement tools
- Retry utilities
- Data validation helpers
- String manipulation utilities
- File system helpers

## Quick Start

```python
from provide.foundation.utils import timed_block
from provide.foundation import plog

# Time a code block
with timed_block("data_processing") as timer:
    process_large_dataset()
    plog.info(f"Processed in {timer.elapsed:.2f}s")

# Use with async code
async with timed_block("api_call", async_mode=True):
    await fetch_remote_data()
```

## Timing Utilities

### timed_block

A context manager for timing code execution with automatic logging:

```python
from provide.foundation.utils import timed_block
from provide.foundation import plog
import time

# Basic usage
with timed_block("operation"):
    time.sleep(1)
# Logs: "operation took 1.00s"

# With custom logging
with timed_block("database_query", log_level="DEBUG"):
    result = query_database()
    
# Access timing information
with timed_block("calculation") as timer:
    perform_calculation()
    if timer.elapsed > 5.0:
        plog.warning(f"Slow calculation: {timer.elapsed:.2f}s")

# Disable automatic logging
with timed_block("silent_op", log_output=False) as timer:
    do_work()
    # Manually handle timing
    metrics.record("operation_time", timer.elapsed)

# With additional context
with timed_block("api_request", endpoint="/users", method="GET"):
    response = make_request()
# Logs with endpoint and method in structured fields
```

### Async Support

```python
import asyncio
from provide.foundation.utils import timed_block

# Time async operations
async def fetch_data():
    async with timed_block("fetch_data"):
        await asyncio.sleep(1)
        return "data"

# Time multiple async operations
async def process_batch():
    async with timed_block("batch_processing") as timer:
        tasks = [fetch_item(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        plog.info(f"Processed {len(results)} items in {timer.elapsed:.2f}s")
```

### Nested Timing

```python
from provide.foundation.utils import timed_block

with timed_block("full_pipeline"):
    with timed_block("step_1_load"):
        data = load_data()
    
    with timed_block("step_2_process"):
        processed = process_data(data)
    
    with timed_block("step_3_save"):
        save_results(processed)

# Logs each step's timing and total pipeline time
```

## Performance Measurement

### Timer Class

A reusable timer for performance measurement:

```python
from provide.foundation.utils import Timer

# Create a timer
timer = Timer()

# Start timing
timer.start()
do_work()
elapsed = timer.stop()
print(f"Work took {elapsed:.3f} seconds")

# Use as context manager
timer = Timer()
with timer:
    perform_operation()
print(f"Operation took {timer.elapsed:.3f}s")

# Multiple measurements
timer = Timer()
for item in items:
    timer.start()
    process_item(item)
    timer.stop()
    
print(f"Average time: {timer.average:.3f}s")
print(f"Total time: {timer.total:.3f}s")
print(f"Min/Max: {timer.min:.3f}s / {timer.max:.3f}s")
```

### Benchmarking

```python
from provide.foundation.utils import benchmark
import time

@benchmark(iterations=1000)
def slow_function():
    """Function to benchmark."""
    time.sleep(0.001)
    return "result"

# Automatically runs 1000 iterations and reports statistics
result = slow_function()
# Logs: "slow_function: avg=1.00ms, min=0.99ms, max=1.02ms, std=0.01ms"

# Manual benchmarking
from provide.foundation.utils import Benchmark

bench = Benchmark("algorithm_comparison")

# Test different implementations
with bench.measure("algorithm_a"):
    result_a = algorithm_a(data)

with bench.measure("algorithm_b"):
    result_b = algorithm_b(data)

# Get comparison
report = bench.report()
print(report)
# Shows comparative performance of both algorithms
```

## Retry Utilities

### Simple Retry

```python
from provide.foundation.utils import retry_operation

# Basic retry
result = retry_operation(
    lambda: unreliable_function(),
    max_attempts=3,
    delay=1.0
)

# With exponential backoff
result = retry_operation(
    lambda: api_call(),
    max_attempts=5,
    delay=1.0,
    backoff_factor=2.0,  # 1s, 2s, 4s, 8s, 16s
    max_delay=30.0
)

# Retry on specific exceptions
result = retry_operation(
    lambda: network_operation(),
    max_attempts=3,
    exceptions=(ConnectionError, TimeoutError),
    on_retry=lambda attempt, error: plog.warning(
        f"Retry {attempt} after {error}"
    )
)
```

### Advanced Retry Logic

```python
from provide.foundation.utils import RetryPolicy

# Create a retry policy
policy = RetryPolicy(
    max_attempts=5,
    delay=1.0,
    backoff_factor=2.0,
    max_delay=60.0,
    jitter=True  # Add random jitter to prevent thundering herd
)

# Apply to function
@policy.apply
def flaky_operation():
    if random.random() < 0.7:
        raise ConnectionError("Network issue")
    return "success"

# Use policy manually
for attempt in policy:
    try:
        result = make_request()
        break
    except Exception as e:
        if not policy.should_retry(e):
            raise
        policy.wait()
```

## Data Validation

### Type Checking

```python
from provide.foundation.utils import (
    ensure_type,
    ensure_list,
    ensure_dict,
    validate_email,
    validate_url
)

# Ensure correct types
value = ensure_type(user_input, str, default="")
items = ensure_list(data.get("items"), item_type=int)
config = ensure_dict(raw_config, required_keys=["host", "port"])

# Validate formats
if not validate_email(email):
    raise ValueError(f"Invalid email: {email}")

if not validate_url(webhook_url, require_https=True):
    raise ValueError(f"Invalid HTTPS URL: {webhook_url}")
```

### Data Sanitization

```python
from provide.foundation.utils import (
    sanitize_filename,
    sanitize_path,
    truncate_string,
    remove_ansi_codes
)

# Clean file names
safe_name = sanitize_filename("my/file:name?.txt")
# Returns: "my_file_name_.txt"

# Sanitize paths
safe_path = sanitize_path("../../etc/passwd")
# Returns safe relative path within boundaries

# Truncate long strings
summary = truncate_string(long_text, max_length=100, suffix="...")

# Remove ANSI color codes
clean_text = remove_ansi_codes(colored_terminal_output)
```

## String Utilities

### Text Processing

```python
from provide.foundation.utils import (
    slugify,
    camel_to_snake,
    snake_to_camel,
    pluralize,
    humanize_bytes,
    humanize_duration
)

# Create URL-safe slugs
slug = slugify("Hello World! 123")  # "hello-world-123"

# Case conversion
snake = camel_to_snake("MyClassName")  # "my_class_name"
camel = snake_to_camel("my_function_name")  # "myFunctionName"

# Pluralization
print(pluralize("item", count=0))  # "items"
print(pluralize("item", count=1))  # "item"
print(pluralize("item", count=5))  # "items"

# Human-readable formats
print(humanize_bytes(1536))  # "1.5 KB"
print(humanize_bytes(1048576))  # "1.0 MB"

print(humanize_duration(90))  # "1m 30s"
print(humanize_duration(3661))  # "1h 1m 1s"
```

### Template Rendering

```python
from provide.foundation.utils import render_template

# Simple template substitution
template = "Hello, {name}! You have {count} messages."
result = render_template(
    template,
    name="Alice",
    count=5
)
# "Hello, Alice! You have 5 messages."

# With default values
template = "Server: {host:localhost}:{port:8080}"
result = render_template(template, host="api.example.com")
# "Server: api.example.com:8080"
```

## File System Helpers

### Safe File Operations

```python
from provide.foundation.utils import (
    safe_write,
    safe_read,
    atomic_write,
    ensure_directory
)

# Safe file writing with backup
safe_write(
    "config.json",
    json.dumps(config),
    backup=True,  # Creates config.json.bak
    mode=0o600   # Restricted permissions
)

# Safe file reading with fallback
content = safe_read(
    "data.txt",
    default="",  # Return if file doesn't exist
    encoding="utf-8"
)

# Atomic file write (write to temp, then rename)
atomic_write(
    "critical_data.db",
    binary_data,
    sync=True  # fsync before rename
)

# Ensure directory exists
ensure_directory("logs/2024/01", mode=0o755)
```

### File Discovery

```python
from provide.foundation.utils import (
    find_files,
    find_project_root,
    get_relative_path
)

# Find files by pattern
python_files = find_files(
    root_dir="src",
    pattern="*.py",
    recursive=True,
    exclude_dirs=[".git", "__pycache__"]
)

# Find project root (looks for markers like .git, pyproject.toml)
project_root = find_project_root(start_path=__file__)

# Get relative path from project root
rel_path = get_relative_path(
    "/home/user/project/src/module.py",
    base="/home/user/project"
)
# Returns: "src/module.py"
```

## Caching Utilities

### Simple Cache

```python
from provide.foundation.utils import memoize, LRUCache

# Memoize function results
@memoize(maxsize=128, ttl=300)  # Cache 128 items for 5 minutes
def expensive_calculation(x, y):
    time.sleep(1)  # Simulate expensive operation
    return x * y

# First call takes 1 second
result = expensive_calculation(5, 10)

# Subsequent calls return immediately
result = expensive_calculation(5, 10)

# Manual cache management
cache = LRUCache(maxsize=100)

# Store values
cache.set("user:123", user_data, ttl=3600)

# Retrieve values
user = cache.get("user:123", default=None)

# Clear cache
cache.clear()
```

## Environment Utilities

### Environment Variables

```python
from provide.foundation.utils import (
    get_env,
    get_env_bool,
    get_env_int,
    get_env_list,
    require_env
)

# Get with type conversion and defaults
debug = get_env_bool("DEBUG", default=False)
port = get_env_int("PORT", default=8080)
hosts = get_env_list("ALLOWED_HOSTS", separator=",")

# Require environment variable
api_key = require_env("API_KEY")  # Raises if not set

# Get with validation
database_url = get_env(
    "DATABASE_URL",
    default="sqlite:///db.sqlite",
    validator=lambda x: x.startswith(("sqlite://", "postgresql://"))
)
```

## Testing Utilities

### Test Helpers

```python
from provide.foundation.utils import (
    create_temp_directory,
    mock_time,
    capture_output
)

# Create temporary directory for tests
with create_temp_directory() as temp_dir:
    # temp_dir is created and cleaned up automatically
    test_file = temp_dir / "test.txt"
    test_file.write_text("test data")

# Mock time for testing
with mock_time(start="2024-01-01 00:00:00") as mock:
    # Time is frozen
    first = datetime.now()
    
    mock.advance(hours=1)
    second = datetime.now()
    
    assert (second - first).seconds == 3600

# Capture output
with capture_output() as output:
    print("Hello")
    plog.info("Test message")

assert "Hello" in output.stdout
assert "Test message" in output.stderr
```

## Async Utilities

### Async Helpers

```python
from provide.foundation.utils import (
    run_async,
    gather_with_timeout,
    async_retry
)

# Run async function from sync code
async def async_operation():
    await asyncio.sleep(1)
    return "result"

result = run_async(async_operation())

# Gather with timeout
async def fetch_multiple():
    tasks = [
        fetch_url(url) for url in urls
    ]
    results = await gather_with_timeout(
        tasks,
        timeout=10.0,
        return_exceptions=True
    )
    return results

# Async retry
@async_retry(max_attempts=3, delay=1.0)
async def flaky_async_operation():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## Best Practices

1. **Use context managers for timing**:
   ```python
   # Good - automatic cleanup
   with timed_block("operation"):
       perform_operation()
   
   # Less ideal - manual management
   start = time.time()
   perform_operation()
   print(f"Took {time.time() - start}s")
   ```

2. **Cache expensive operations**:
   ```python
   @memoize(ttl=300)
   def get_user_permissions(user_id):
       # Expensive database query
       return query_permissions(user_id)
   ```

3. **Use type validation for external data**:
   ```python
   # Validate and sanitize user input
   email = ensure_type(request.get("email"), str)
   if not validate_email(email):
       raise ValidationError("Invalid email")
   ```

4. **Handle retries gracefully**:
   ```python
   @retry_operation(
       max_attempts=3,
       on_retry=lambda a, e: plog.warning(f"Retry {a}: {e}")
   )
   def external_api_call():
       return make_request()
   ```

5. **Use atomic operations for critical files**:
   ```python
   # Ensure file consistency
   atomic_write("important.data", content, sync=True)
   ```

## Performance Considerations

### Efficient Caching

```python
from provide.foundation.utils import cached_property

class DataProcessor:
    @cached_property
    def expensive_config(self):
        """Computed once and cached."""
        return load_and_parse_config()
    
    def process(self, data):
        # Uses cached config
        return apply_config(data, self.expensive_config)
```

### Batch Operations

```python
from provide.foundation.utils import batch_process

# Process items in batches
results = batch_process(
    items,
    process_function,
    batch_size=100,
    parallel=True,
    max_workers=4
)
```

## API Reference

### Timing
- `timed_block(name, **kwargs)` - Context manager for timing
- `Timer()` - Reusable timer class
- `benchmark(iterations)` - Decorator for benchmarking

### Retry
- `retry_operation(func, **kwargs)` - Retry with configuration
- `RetryPolicy` - Configurable retry policy class
- `@async_retry` - Async retry decorator

### Validation
- `ensure_type(value, type, default)` - Type validation
- `validate_email(email)` - Email validation
- `validate_url(url)` - URL validation

### String Operations
- `slugify(text)` - Create URL-safe slugs
- `humanize_bytes(bytes)` - Human-readable bytes
- `humanize_duration(seconds)` - Human-readable duration

### File System
- `safe_write(path, content)` - Safe file writing
- `atomic_write(path, content)` - Atomic file operations
- `find_files(pattern)` - File discovery

### Caching
- `@memoize` - Function result caching
- `LRUCache` - Least recently used cache
- `@cached_property` - Cached property decorator

### Environment
- `get_env(name, default)` - Get environment variable
- `get_env_bool(name)` - Get boolean env var
- `require_env(name)` - Require env var

### Testing
- `create_temp_directory()` - Temporary directory
- `mock_time()` - Time mocking
- `capture_output()` - Output capture

## See Also

- [Logger](logger.md) - Logging integration
- [Errors](errors.md) - Error handling utilities
- [Performance Guide](../guides/performance-tuning.md) - Performance best practices