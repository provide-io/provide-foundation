# Platform Detection API

The `provide.foundation.platform` module provides cross-platform system detection and information gathering utilities.

## Overview

The platform module helps you:
- Detect operating system and architecture
- Get normalized platform strings
- Gather system information
- Handle platform-specific logic

## Quick Start

```python
from provide.foundation import platform

# Get platform information
os_name = platform.get_os_name()        # "darwin", "linux", or "windows"
arch = platform.get_arch_name()         # "amd64", "arm64", "x86", etc.
platform_str = platform.get_platform_string()  # "darwin_arm64"

# Get detailed system info
info = platform.get_system_info()
print(f"Running on {info.os_name} {info.os_version} ({info.cpu_type})")
print(f"System has {info.num_cpus} CPUs and {info.total_memory} bytes of RAM")
```

## Core Functions

### `get_os_name() -> str`

Returns the normalized operating system name.

**Returns:**
- `"darwin"` for macOS
- `"linux"` for Linux
- `"windows"` for Windows
- Original lowercase name for other platforms

**Example:**
```python
os_name = platform.get_os_name()
if os_name == "darwin":
    print("Running on macOS")
```

### `get_arch_name() -> str`

Returns the normalized CPU architecture.

**Returns:**
- `"amd64"` for x86_64
- `"arm64"` for ARM 64-bit (aarch64)
- `"x86"` for 32-bit x86 (i686, i586, i486)
- `"i386"` for i386
- Original lowercase name for other architectures

**Example:**
```python
arch = platform.get_arch_name()
if arch == "arm64":
    print("Running on ARM 64-bit")
```

### `get_platform_string() -> str`

Returns a normalized platform string combining OS and architecture.

**Returns:** String in format `"{os}_{arch}"`, e.g., `"linux_amd64"`, `"darwin_arm64"`

**Example:**
```python
platform_str = platform.get_platform_string()
# Use for platform-specific downloads or configurations
binary_url = f"https://example.com/releases/app-{platform_str}.tar.gz"
```

### `get_os_version() -> str | None`

Returns the OS version if available.

**Returns:**
- macOS: Version string like `"14.2.1"`
- Linux: Kernel version like `"5.15"`
- Windows: Version string like `"10.0.19045"`
- `None` if version cannot be determined

**Example:**
```python
version = platform.get_os_version()
if version:
    print(f"OS Version: {version}")
```

### `get_cpu_type() -> str | None`

Returns the CPU type/family if available.

**Returns:**
- Intel CPUs: `"Intel Core i7"`, `"Intel"`, etc.
- AMD CPUs: `"AMD Ryzen 9"`, `"AMD"`, etc.
- Apple Silicon: `"Apple M1"`, `"Apple M2"`, etc.
- `None` if CPU type cannot be determined

**Example:**
```python
cpu = platform.get_cpu_type()
if cpu and "Apple" in cpu:
    print("Running on Apple Silicon")
```

### `normalize_platform_components(os_name: str, arch_name: str) -> tuple[str, str]`

Normalizes OS and architecture names to standard format.

**Parameters:**
- `os_name`: Operating system name to normalize
- `arch_name`: Architecture name to normalize

**Returns:** Tuple of `(normalized_os, normalized_arch)`

**Example:**
```python
os_norm, arch_norm = platform.normalize_platform_components("Darwin", "x86_64")
# Returns: ("darwin", "amd64")
```

### `get_system_info() -> SystemInfo`

Gathers comprehensive system information.

**Returns:** `SystemInfo` object with attributes:
- `os_name`: Normalized OS name
- `arch`: Normalized architecture
- `platform`: Platform string
- `os_version`: OS version (if available)
- `cpu_type`: CPU type (if available)
- `python_version`: Python version
- `hostname`: System hostname (if available)
- `username`: Current user (if available)
- `home_dir`: User home directory
- `temp_dir`: Temporary directory
- `num_cpus`: Number of CPU cores (if available)
- `total_memory`: Total RAM in bytes (requires psutil)
- `available_memory`: Available RAM in bytes (requires psutil)
- `disk_usage`: Dictionary of disk usage by path (if available)

**Example:**
```python
info = platform.get_system_info()

print(f"Platform: {info.platform}")
print(f"Python: {info.python_version}")
print(f"CPUs: {info.num_cpus}")
print(f"User: {info.username}@{info.hostname}")

if info.disk_usage:
    for path, usage in info.disk_usage.items():
        free_gb = usage['free'] / (1024**3)
        print(f"{path}: {free_gb:.1f} GB free")
```

## Error Handling

### `PlatformError`

Raised when platform detection fails.

```python
from provide.foundation.platform.detection import PlatformError

try:
    os_name = platform.get_os_name()
except PlatformError as e:
    print(f"Failed to detect OS: {e}")
    # Fall back to default behavior
```

## Use Cases

### Platform-Specific Downloads

```python
def download_binary():
    platform_str = platform.get_platform_string()
    url = f"https://github.com/org/repo/releases/latest/tool-{platform_str}.tar.gz"
    # Download platform-specific binary
```

### System Requirements Check

```python
def check_requirements():
    info = platform.get_system_info()
    
    # Check OS
    if info.os_name not in ["linux", "darwin"]:
        raise SystemError("Only Linux and macOS are supported")
    
    # Check architecture
    if info.arch not in ["amd64", "arm64"]:
        raise SystemError("Only 64-bit systems are supported")
    
    # Check resources
    if info.num_cpus and info.num_cpus < 4:
        print("Warning: Less than 4 CPUs detected")
    
    if info.total_memory and info.total_memory < 8 * 1024**3:
        print("Warning: Less than 8GB RAM detected")
```

### Platform-Specific Configuration

```python
def get_config_path():
    info = platform.get_system_info()
    
    if info.os_name == "windows":
        return Path(os.environ.get("APPDATA")) / "MyApp"
    elif info.os_name == "darwin":
        return Path(info.home_dir) / "Library" / "Application Support" / "MyApp"
    else:  # Linux and others
        return Path(info.home_dir) / ".config" / "myapp"
```

## Best Practices

1. **Cache platform information** - It won't change during runtime:
   ```python
   _platform_info = None
   
   def get_cached_platform():
       global _platform_info
       if _platform_info is None:
           _platform_info = platform.get_system_info()
       return _platform_info
   ```

2. **Handle None values** - Some information may not be available:
   ```python
   info = platform.get_system_info()
   cpu_count = info.num_cpus or os.cpu_count() or 1
   ```

3. **Use normalization** - Always normalize platform strings for consistency:
   ```python
   os_name, arch = platform.normalize_platform_components(
       platform.system(), 
       platform.machine()
   )
   ```

## See Also

- [Process Execution](process.md) - For running platform-specific commands
- [Configuration](config.md) - For platform-specific configuration