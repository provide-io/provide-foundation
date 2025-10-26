# How to Use Platform Detection

Foundation provides cross-platform detection and system information utilities.

## Platform Detection

### OS Detection

```python
from provide.foundation.platform import (
    is_linux,
    is_macos,
    is_windows,
    is_64bit,
    is_arm
)

# Check operating system
if is_linux():
    print("Running on Linux")
elif is_macos():
    print("Running on macOS")
elif is_windows():
    print("Running on Windows")

# Check architecture
if is_64bit():
    print("64-bit system")

if is_arm():
    print("ARM processor")
```

### Platform Information

```python
from provide.foundation.platform import (
    get_os_name,
    get_os_version,
    get_arch_name,
    get_platform_string
)

# Get OS details
os = get_os_name()         # "linux", "darwin", "windows"
version = get_os_version()  # "22.04", "13.0", etc.
arch = get_arch_name()      # "x86_64", "arm64", etc.

# Get combined platform string
platform = get_platform_string()
# "linux_x86_64", "darwin_arm64", etc.
```

## System Information

### Get Complete System Info

```python
from provide.foundation.platform import get_system_info, SystemInfo

info: SystemInfo = get_system_info()

print(f"OS: {info.os_name} {info.os_version}")
print(f"Architecture: {info.architecture}")
print(f"CPU: {info.cpu_brand}")
print(f"CPU Cores: {info.cpu_count}")
print(f"64-bit: {info.is_64bit}")
```

## CPU Information

**Requires**: `provide-foundation[platform]` extra

```python
from provide.foundation.platform import (
    get_cpu_info,
    get_cpu_brand,
    get_cpu_count,
    has_cpu_flag
)

# Get CPU brand
brand = get_cpu_brand()
# "Intel(R) Core(TM) i7-9750H"

# Get CPU count
count = get_cpu_count()
# 12

# Check CPU features
if has_cpu_flag("avx2"):
    print("AVX2 supported")
```

## Systemd Integration (Linux)

**Requires**: `systemd` on Linux systems

```python
from provide.foundation.platform import (
    has_systemd,
    notify_ready,
    notify_status,
    notify_stopping,
    notify_watchdog
)

if has_systemd():
    # Notify systemd that service is ready
    notify_ready()

    # Send status updates
    notify_status("Processing requests...")

    # Send watchdog ping
    notify_watchdog()

    # Notify before stopping
    notify_stopping()
```

## Best Practices

### ✅ DO: Use Platform Detection for OS-Specific Code

```python
# ✅ Good: Platform-specific paths
from provide.foundation.platform import is_windows, is_linux

if is_windows():
    config_dir = "C:\\ProgramData\\myapp"
elif is_linux():
    config_dir = "/etc/myapp"
else:
    config_dir = "~/myapp"
```

### ✅ DO: Log Platform Information

```python
# ✅ Good: Log system info at startup
from provide.foundation import logger
from provide.foundation.platform import get_system_info

info = get_system_info()
logger.info(
    "application_started",
    os=info.os_name,
    arch=info.architecture,
    cpu=info.cpu_brand
)
```

## Next Steps

- **[Process Execution](../process/subprocess.md)**: Platform-aware process execution
- **[Configuration](../configuration/env-variables.md)**: Platform-specific configuration

---

**Tip**: Install `provide-foundation[platform]` for full CPU detection capabilities.
