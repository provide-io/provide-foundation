# Platform Detection

Platform detection and system information utilities.

## Overview

`provide.foundation`'s platform module provides comprehensive system detection capabilities including OS identification, architecture details, and Python environment information.

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

## System Resources

### CPU Information

```python
from provide.foundation.platform import get_system_info

info = get_system_info()

# CPU count is available if psutil is installed
if info.num_cpus:
    print(f"CPU cores: {info.num_cpus}")
```

### Memory Information

```python
from provide.foundation.platform import get_system_info

info = get_system_info()

# Memory information requires psutil
if info.total_memory:
    print(f"Total memory: {info.total_memory / (1024**3):.1f} GB")
```

## Related Topics

- [Configuration](../config/index.md) - Configuration system
- [Process Management](process.md) - Process utilities
- [Logging](../logging/basic.md) - Platform-aware logging