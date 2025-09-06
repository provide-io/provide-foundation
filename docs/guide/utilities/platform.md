# Platform Detection

Platform detection and system information utilities.

## Overview

provide.foundation's platform module provides comprehensive system detection capabilities including OS identification, architecture details, Python environment information, and Docker/container detection. It ensures consistent platform handling across different environments.

## Basic Detection

### Platform Info

Get comprehensive system information:

```python
from provide.foundation.platform import get_system_info

info = get_system_info()
print(f"OS: {info.os_name} {info.os_version}")
print(f"Architecture: {info.arch}")
print(f"Platform: {info.platform_string}")
print(f"Python: {info.python_version}")
print(f"Hostname: {info.hostname}")

# Convert to dictionary for logging
info_dict = info.to_dict()
logger.info("System information", **info_dict)
```

### Quick Checks

Simple platform checks:

```python
from provide.foundation.platform import (
    is_linux,
    is_macos, 
    is_windows,
    is_arm,
    is_64bit,
    get_os_name,
    get_arch_name
)

if is_macos():
    print("Running on macOS")
elif is_linux():
    print("Running on Linux")
elif is_windows():
    print("Running on Windows")

# Get normalized names
os_name = get_os_name()  # "linux", "macos", "windows"
arch = get_arch_name()   # "x64", "arm64", "arm", "x86"

if is_arm():
    print("ARM architecture detected")
elif is_64bit():
    print("64-bit architecture detected")

print(f"Running on {os_name}-{arch}")
```

## Environment Detection

### Container Environments

Check for containerized environments by examining the system:

```python
import os
from pathlib import Path

def is_docker():
    """Check if running in Docker container."""
    return Path("/.dockerenv").exists()

def is_kubernetes():
    """Check if running in Kubernetes."""
    return (
        os.environ.get("KUBERNETES_SERVICE_HOST") is not None or
        Path("/var/run/secrets/kubernetes.io").exists()
    )

def detect_container_environment():
    """Detect container environment type."""
    if is_kubernetes():
        return "kubernetes"
    elif is_docker():
        return "docker"
    else:
        return None

env_type = detect_container_environment()
if env_type:
    print(f"Running in {env_type} environment")
```

### Cloud Environments

Detect cloud platforms via metadata services:

```python
import urllib.request

def detect_cloud_provider():
    """Detect cloud provider from metadata services."""
    
    # AWS EC2
    try:
        response = urllib.request.urlopen(
            "http://169.254.169.254/latest/meta-data/instance-id",
            timeout=1
        )
        if response.status == 200:
            return "aws"
    except:
        pass
    
    # Google Cloud
    try:
        req = urllib.request.Request(
            "http://metadata.google.internal/computeMetadata/v1/instance/id",
            headers={"Metadata-Flavor": "Google"}
        )
        response = urllib.request.urlopen(req, timeout=1)
        if response.status == 200:
            return "gcp"
    except:
        pass
    
    # Azure
    try:
        req = urllib.request.Request(
            "http://169.254.169.254/metadata/instance?api-version=2021-02-01",
            headers={"Metadata": "true"}
        )
        response = urllib.request.urlopen(req, timeout=1)
        if response.status == 200:
            return "azure"
    except:
        pass
    
    return None

cloud = detect_cloud_provider()
if cloud:
    print(f"Running on {cloud}")
```

## System Resources

### CPU Information

```python
from provide.foundation.platform import get_system_info

info = get_system_info()

# CPU count is available if psutil is installed
if info.cpu_count:
    print(f"CPU cores: {info.cpu_count}")
    
    # Use for configuration
    worker_count = min(info.cpu_count, 8)
    print(f"Recommended workers: {worker_count}")
else:
    print("CPU information not available (install psutil for details)")
    worker_count = 2  # Safe default
```

### Memory Information

```python
from provide.foundation.platform import get_system_info

info = get_system_info()

# Memory information requires psutil
if info.memory_total_gb:
    print(f"Total memory: {info.memory_total_gb:.1f} GB")
    
    # Calculate memory limits
    app_memory_limit_gb = info.memory_total_gb * 0.5  # Use 50% for app
    print(f"App memory limit: {app_memory_limit_gb:.1f} GB")
    
    # Check if enough memory
    if info.memory_total_gb < 1.0:
        print("Warning: Low memory system detected")
else:
    print("Memory information not available (install psutil for details)")
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

- [Configuration](../config/index.md) - Configuration system
- [Process Management](process.md) - Process utilities
- [Logging](../logging/basic.md) - Platform-aware logging