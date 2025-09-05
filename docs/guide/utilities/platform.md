# Platform Detection

Platform detection and system information utilities.

## Overview

provide.foundation's platform module provides comprehensive system detection capabilities including OS identification, architecture details, Python environment information, and Docker/container detection. It ensures consistent platform handling across different environments.

## Basic Detection

### Platform Info

Get comprehensive platform information:

```python
from provide.foundation.platform import get_platform_info

info = get_platform_info()
# {
#     "os": "darwin",
#     "os_version": "23.1.0",
#     "arch": "arm64",
#     "python_version": "3.11.5",
#     "python_implementation": "CPython",
#     "hostname": "macbook.local",
#     "in_docker": False,
#     "in_kubernetes": False
# }

# Access specific info
print(f"Running on {info['os']} {info['arch']}")
```

### Quick Checks

Simple platform checks:

```python
from provide.foundation.platform import (
    is_linux,
    is_macos,
    is_windows,
    is_arm,
    is_x86,
    is_docker,
    is_kubernetes
)

if is_macos():
    print("Running on macOS")
elif is_linux():
    print("Running on Linux")
elif is_windows():
    print("Running on Windows")

if is_arm():
    print("ARM architecture detected")
elif is_x86():
    print("x86/x64 architecture detected")

if is_docker():
    print("Running inside Docker container")
```

## Environment Detection

### Container Environments

Detect containerized environments:

```python
from provide.foundation.platform import (
    detect_container,
    get_container_info
)

# Check if in container
container_type = detect_container()
if container_type:
    print(f"Running in {container_type}")
    
    # Get detailed container info
    info = get_container_info()
    # {
    #     "type": "docker",
    #     "id": "abc123...",
    #     "hostname": "container-host",
    #     "cgroup_limits": {...}
    # }
```

### Cloud Environments

Detect cloud platforms:

```python
from provide.foundation.platform import detect_cloud_provider

cloud = detect_cloud_provider()
if cloud:
    print(f"Running on {cloud}")
    # AWS, GCP, Azure, etc.
```

## System Resources

### CPU Information

```python
from provide.foundation.platform import get_cpu_info

cpu = get_cpu_info()
# {
#     "count": 8,
#     "physical_cores": 4,
#     "model": "Apple M1",
#     "frequency": "3.2 GHz",
#     "architecture": "arm64"
# }

print(f"CPU: {cpu['model']} with {cpu['count']} cores")
```

### Memory Information

```python
from provide.foundation.platform import get_memory_info

memory = get_memory_info()
# {
#     "total": 17179869184,  # bytes
#     "available": 8589934592,
#     "used": 8589934592,
#     "percent": 50.0,
#     "total_human": "16.0 GB",
#     "available_human": "8.0 GB"
# }

print(f"Memory: {memory['available_human']} / {memory['total_human']}")
```

## Python Environment

### Python Details

```python
from provide.foundation.platform import get_python_info

python = get_python_info()
# {
#     "version": "3.11.5",
#     "implementation": "CPython",
#     "executable": "/usr/bin/python3",
#     "prefix": "/usr",
#     "venv": "/path/to/venv",
#     "site_packages": ["/path/to/site-packages"],
#     "compile_flags": [...]
# }

# Check virtual environment
if python.get('venv'):
    print(f"Using venv: {python['venv']}")
```

### Package Information

```python
from provide.foundation.platform import get_package_versions

versions = get_package_versions([
    "structlog",
    "click",
    "attrs"
])
# {
#     "structlog": "23.1.0",
#     "click": "8.1.7",
#     "attrs": "23.1.0"
# }

for pkg, ver in versions.items():
    print(f"{pkg}: {ver}")
```

## Platform-Specific Code

### Conditional Logic

```python
from provide.foundation.platform import Platform

def get_config_path():
    """Get platform-specific config path."""
    platform = Platform.current()
    
    if platform.is_windows:
        return Path.home() / "AppData" / "Local" / "myapp"
    elif platform.is_macos:
        return Path.home() / "Library" / "Application Support" / "myapp"
    else:  # Linux/Unix
        return Path.home() / ".config" / "myapp"

# Platform-specific command execution
def open_file(path: str):
    platform = Platform.current()
    
    if platform.is_windows:
        subprocess.run(["start", path], shell=True)
    elif platform.is_macos:
        subprocess.run(["open", path])
    else:  # Linux
        subprocess.run(["xdg-open", path])
```

### Feature Detection

```python
from provide.foundation.platform import has_feature

# Check for specific features
if has_feature("color_terminal"):
    print("\033[32mColor output supported\033[0m")

if has_feature("unicode"):
    print("✅ Unicode supported")

if has_feature("async_io"):
    print("Async I/O available")
```

## Complete Examples

### System Report

```python
from provide.foundation.platform import (
    get_platform_info,
    get_cpu_info,
    get_memory_info,
    get_python_info
)

def generate_system_report():
    """Generate comprehensive system report."""
    report = {
        "platform": get_platform_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "python": get_python_info()
    }
    
    print("System Report")
    print("=" * 50)
    
    # Platform
    p = report["platform"]
    print(f"OS: {p['os']} {p['os_version']} ({p['arch']})")
    print(f"Hostname: {p['hostname']}")
    
    # CPU
    c = report["cpu"]
    print(f"CPU: {c['model']}")
    print(f"Cores: {c['count']} ({c['physical_cores']} physical)")
    
    # Memory
    m = report["memory"]
    print(f"Memory: {m['available_human']} / {m['total_human']}")
    print(f"Usage: {m['percent']:.1f}%")
    
    # Python
    py = report["python"]
    print(f"Python: {py['version']} ({py['implementation']})")
    if py.get('venv'):
        print(f"Venv: {py['venv']}")
    
    return report
```

### Environment Adapter

```python
from provide.foundation.platform import Platform
from provide.foundation import logger

class EnvironmentAdapter:
    """Adapt behavior to environment."""
    
    def __init__(self):
        self.platform = Platform.current()
        self._configure_for_environment()
    
    def _configure_for_environment(self):
        """Configure based on environment."""
        # Docker optimizations
        if self.platform.in_docker:
            logger.info("Docker detected, optimizing...")
            self.enable_container_mode()
        
        # Cloud-specific setup
        if self.platform.cloud_provider:
            logger.info(f"Running on {self.platform.cloud_provider}")
            self.configure_cloud_features()
        
        # Architecture-specific
        if self.platform.is_arm:
            logger.info("ARM architecture, using optimized libs")
            self.use_arm_optimizations()
    
    def get_storage_path(self):
        """Get appropriate storage path."""
        if self.platform.in_docker:
            # Use volume mount
            return Path("/data")
        elif self.platform.is_windows:
            return Path.home() / "AppData" / "Local" / "MyApp"
        elif self.platform.is_macos:
            return Path.home() / "Library" / "MyApp"
        else:
            return Path.home() / ".local" / "share" / "myapp"
```

## Best Practices

### 1. Cache Platform Info

```python
# Good: Cache expensive checks
from functools import lru_cache

@lru_cache(maxsize=1)
def get_platform_details():
    return Platform.current()

# Bad: Repeated detection
def process():
    if Platform.current().is_windows:
        # Detects every time
        pass
```

### 2. Graceful Degradation

```python
# Good: Handle missing features
if has_feature("color_terminal"):
    print_with_color()
else:
    print_plain_text()

# Bad: Assume features exist
print("\033[32mGreen\033[0m")  # May not work
```

### 3. Environment Variables

```python
# Good: Allow override
import os

def detect_environment():
    # Allow manual override
    if env := os.getenv("APP_ENVIRONMENT"):
        return env
    
    # Auto-detect
    if is_docker():
        return "docker"
    elif is_kubernetes():
        return "kubernetes"
    else:
        return "local"
```

## Related Topics

- [Configuration](../configuration/index.md) - Platform-specific config
- [Process Management](process.md) - Process utilities
- [Logging](../logging/basic.md) - Platform-aware logging