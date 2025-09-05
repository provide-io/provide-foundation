# Platform API Reference

Cross-platform detection and system information utilities for Foundation applications.

## Overview

The platform module provides utilities for detecting the operating system, architecture, and system capabilities. This enables applications to adapt behavior based on the runtime environment.

## Quick Start

```python
from provide.foundation.platform import get_platform_info, is_windows, is_macos, is_linux

# Get comprehensive platform information
info = get_platform_info()
print(f"Running on {info['platform']} {info['architecture']}")

# Quick platform checks
if is_windows():
    print("Windows-specific logic")
elif is_macos():
    print("macOS-specific logic") 
elif is_linux():
    print("Linux-specific logic")
```

## Functions

### `get_platform_info() -> dict[str, str]`

Returns comprehensive platform and system information.

**Returns**: Dictionary containing platform details

```python
from provide.foundation.platform import get_platform_info

info = get_platform_info()
# Returns:
{
    'platform': 'linux',           # OS name (linux/darwin/windows)
    'architecture': 'x86_64',      # CPU architecture  
    'python_version': '3.11.7',    # Python version
    'hostname': 'webapp-01',       # System hostname
    'processor': 'Intel64',        # Processor type
    'machine': 'AMD64',            # Machine type
    'system': 'Linux',             # System name
    'release': '5.4.0-89-generic', # OS release
    'version': '#100-Ubuntu'        # OS version
}
```

**Usage Examples**:

```python
# Environment-specific configuration
info = get_platform_info()
if info['platform'] == 'linux':
    config_file = '/etc/myapp/config.yaml'
elif info['platform'] == 'darwin':
    config_file = '~/Library/Application Support/MyApp/config.yaml'
elif info['platform'] == 'windows':
    config_file = r'%APPDATA%\MyApp\config.yaml'

# Architecture-specific optimizations
if info['architecture'] == 'arm64':
    # Use ARM-optimized code paths
    use_neon_instructions = True
```

### `is_windows() -> bool`

Check if running on Windows.

```python
from provide.foundation.platform import is_windows

if is_windows():
    # Windows-specific file paths
    data_dir = os.path.expandvars(r'%APPDATA%\MyApp')
    use_windows_auth = True
```

### `is_macos() -> bool`

Check if running on macOS.

```python
from provide.foundation.platform import is_macos

if is_macos():
    # macOS-specific integrations
    use_keychain = True
    enable_dark_mode_detection = True
```

### `is_linux() -> bool`

Check if running on Linux.

```python
from provide.foundation.platform import is_linux

if is_linux():
    # Linux-specific configurations
    use_systemd = True
    check_selinux_status = True
```

### `get_system_info() -> SystemInfo`

Returns detailed system information as a structured object.

```python
from provide.foundation.platform import get_system_info

sys_info = get_system_info()
print(f"OS: {sys_info.platform}")
print(f"CPU: {sys_info.processor}")
print(f"Python: {sys_info.python_version}")

# Convert to dictionary
info_dict = sys_info.to_dict()
```

## Data Classes

### `SystemInfo`

Structured system information container.

**Attributes**:
- `platform: str` - Operating system name
- `architecture: str` - CPU architecture
- `python_version: str` - Python version string
- `hostname: str` - System hostname
- `processor: str` - Processor information
- `machine: str` - Machine type
- `system: str` - System name
- `release: str` - OS release version
- `version: str` - OS version string

**Methods**:
- `to_dict() -> dict[str, str]` - Convert to dictionary
- `is_64bit() -> bool` - Check if 64-bit architecture
- `supports_color() -> bool` - Check terminal color support

```python
from provide.foundation.platform import get_system_info

info = get_system_info()

# Check capabilities
if info.is_64bit():
    enable_large_memory_buffers = True

if info.supports_color():
    use_colored_output = True

# Serialize for logging
logger.info("system_startup", **info.to_dict())
```

## Platform-Specific Utilities

### Path Resolution

```python
from provide.foundation.platform import get_platform_info

def get_config_path(app_name: str) -> str:
    """Get platform-appropriate config directory."""
    info = get_platform_info()
    
    if info['platform'] == 'windows':
        return f"{os.environ['APPDATA']}\\{app_name}"
    elif info['platform'] == 'darwin':
        return f"~/Library/Application Support/{app_name}"
    else:  # Linux/Unix
        return f"~/.config/{app_name.lower()}"

config_path = get_config_path("MyApp")
```

### Service Integration

```python
from provide.foundation.platform import is_windows, is_linux

def setup_logging_service():
    """Configure platform-appropriate logging."""
    
    if is_windows():
        # Windows Event Log
        import logging.handlers
        handler = logging.handlers.NTEventLogHandler("MyApp")
        
    elif is_linux():
        # systemd journal
        import systemd.journal
        handler = systemd.journal.JournalHandler()
        
    else:
        # Standard syslog
        import logging.handlers
        handler = logging.handlers.SysLogHandler()
    
    return handler
```

### Environment Detection

```python
from provide.foundation.platform import get_platform_info

def detect_container_environment():
    """Detect if running in containerized environment."""
    info = get_platform_info()
    
    indicators = {
        'docker': os.path.exists('/.dockerenv'),
        'kubernetes': 'KUBERNETES_SERVICE_HOST' in os.environ,
        'aws_lambda': 'AWS_LAMBDA_FUNCTION_NAME' in os.environ,
        'github_actions': 'GITHUB_ACTIONS' in os.environ,
    }
    
    return {
        'platform_info': info,
        'container_indicators': indicators,
        'is_containerized': any(indicators.values())
    }
```

## Integration Examples

### Application Configuration

```python
from provide.foundation.platform import get_platform_info
from provide.foundation import logger

def configure_application():
    """Configure application based on platform."""
    
    info = get_platform_info()
    logger.info("platform_detected", **info)
    
    config = {}
    
    # Platform-specific defaults
    if info['platform'] == 'windows':
        config.update({
            'file_separator': '\\',
            'line_ending': '\r\n',
            'default_shell': 'cmd.exe',
            'supports_ansi': False
        })
    else:  # Unix-like
        config.update({
            'file_separator': '/',
            'line_ending': '\n', 
            'default_shell': '/bin/bash',
            'supports_ansi': True
        })
    
    # Architecture-specific settings
    if info['architecture'] in ('x86_64', 'amd64'):
        config['use_64bit_optimizations'] = True
    
    return config
```

### Performance Tuning

```python
from provide.foundation.platform import get_system_info

def optimize_for_platform():
    """Optimize performance based on platform."""
    
    info = get_system_info()
    
    # CPU-specific optimizations
    if 'Intel' in info.processor:
        enable_intel_optimizations = True
    elif 'AMD' in info.processor:
        enable_amd_optimizations = True
    elif 'ARM' in info.processor or info.architecture == 'arm64':
        enable_arm_optimizations = True
    
    # Memory optimizations
    if info.is_64bit():
        max_memory_pool_size = '8GB'
    else:
        max_memory_pool_size = '2GB'
    
    logger.info("platform_optimizations_applied",
               processor=info.processor,
               architecture=info.architecture,
               max_memory_pool=max_memory_pool_size)
```

### Cross-Platform Testing

```python
import pytest
from provide.foundation.platform import is_windows, is_macos, is_linux

@pytest.mark.skipif(not is_windows(), reason="Windows-specific test")
def test_windows_functionality():
    """Test Windows-specific features."""
    pass

@pytest.mark.skipif(not is_macos(), reason="macOS-specific test")
def test_macos_functionality():
    """Test macOS-specific features.""" 
    pass

@pytest.mark.skipif(not is_linux(), reason="Linux-specific test")
def test_linux_functionality():
    """Test Linux-specific features."""
    pass
```

## Best Practices

### 1. Graceful Degradation

```python
from provide.foundation.platform import get_platform_info

def setup_with_fallbacks():
    """Setup with platform-specific fallbacks."""
    
    info = get_platform_info()
    
    try:
        if info['platform'] == 'linux':
            # Try modern Linux features first
            setup_modern_linux_features()
        else:
            raise NotImplementedError("Platform not optimized")
            
    except Exception:
        # Fall back to cross-platform approach
        logger.warning("falling_back_to_generic_implementation",
                      platform=info['platform'])
        setup_generic_features()
```

### 2. Feature Detection

```python
def check_platform_capabilities():
    """Check what platform features are available."""
    
    capabilities = {
        'ansi_colors': False,
        'unicode_support': False,
        'file_watching': False,
        'process_signals': False
    }
    
    info = get_platform_info()
    
    if info['platform'] != 'windows':
        capabilities.update({
            'ansi_colors': True,
            'process_signals': True,
            'file_watching': True
        })
    
    # Test Unicode support
    try:
        '🔥'.encode('utf-8')
        capabilities['unicode_support'] = True
    except UnicodeError:
        capabilities['unicode_support'] = False
    
    return capabilities
```

### 3. Environment Adaptation

```python
def adapt_to_environment():
    """Adapt behavior to deployment environment."""
    
    info = get_platform_info()
    
    # Development vs Production
    is_development = (
        info['hostname'].startswith('dev-') or 
        'localhost' in info['hostname']
    )
    
    # Container detection
    is_container = os.path.exists('/.dockerenv')
    
    # CI/CD detection
    is_ci = any(var in os.environ for var in [
        'CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'JENKINS_URL'
    ])
    
    config = {
        'debug_mode': is_development,
        'log_level': 'DEBUG' if is_development else 'INFO',
        'enable_profiling': is_development and not is_ci,
        'use_file_logging': not is_container,
        'colorize_output': not is_ci and info.supports_color()
    }
    
    return config
```

## Error Handling

### Platform Detection Errors

```python
from provide.foundation.platform import get_platform_info
from provide.foundation.errors import PlatformError

try:
    info = get_platform_info()
except PlatformError as e:
    logger.error("platform_detection_failed", error=str(e))
    # Use safe defaults
    info = {
        'platform': 'unknown',
        'architecture': 'unknown'
    }
```

### Unsupported Platform Handling

```python
def handle_unsupported_platform():
    """Handle unsupported platform gracefully."""
    
    info = get_platform_info()
    
    if info['platform'] not in ('linux', 'darwin', 'windows'):
        logger.warning("unsupported_platform_detected",
                      platform=info['platform'],
                      architecture=info['architecture'])
        
        # Use most compatible settings
        return get_minimal_config()
    
    return get_optimized_config(info)
```

## Thread Safety

All platform detection functions are thread-safe and cache results:

```python
import threading
from provide.foundation.platform import get_platform_info

def worker():
    # Safe to call from multiple threads
    info = get_platform_info()  # Cached after first call
    process_with_platform_info(info)

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
```

## See Also

- [Process API](../process/) - Process execution utilities
- [Utils API](../utils/) - Environment variable utilities
- [Config API](../config/) - Platform-aware configuration
- [Platform Guide](../../guide/utilities/platform.md) - Platform detection patterns