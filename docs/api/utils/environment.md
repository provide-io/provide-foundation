# Environment Utilities

Type-safe environment variable parsing with support for various data types.

## Environment Variable Parsing Functions

### `get_str(key, default="", prefix=None)`

Get string value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (str): Default value if not found (default: "")
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `str`: Environment variable value or default

**Example:**
```python
from provide.foundation.utils import get_str

# Basic usage
api_key = get_str("API_KEY", "default-key")
host = get_str("HOST", "localhost")

# With prefix
db_host = get_str("HOST", "localhost", prefix="DB")  # Looks for DB_HOST
```

### `get_int(key, default=0, prefix=None)`

Get integer value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (int): Default value if not found or invalid (default: 0)
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `int`: Parsed integer value or default

**Example:**
```python
from provide.foundation.utils import get_int

port = get_int("PORT", 8000)
workers = get_int("WORKERS", 4)
timeout = get_int("TIMEOUT", 30, prefix="API")  # API_TIMEOUT
```

### `get_float(key, default=0.0, prefix=None)`

Get float value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (float): Default value if not found or invalid
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `float`: Parsed float value or default

### `get_bool(key, default=False, prefix=None)`

Get boolean value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (bool): Default value if not found
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `bool`: Parsed boolean value or default

**Supported Values:**
- **True**: `true`, `True`, `1`, `yes`, `Yes`, `on`, `On`
- **False**: `false`, `False`, `0`, `no`, `No`, `off`, `Off`

**Example:**
```python
from provide.foundation.utils import get_bool

debug = get_bool("DEBUG", False)
ssl_enabled = get_bool("SSL_ENABLED", True)
auto_reload = get_bool("RELOAD", False, prefix="DEV")  # DEV_RELOAD
```

### `get_list(key, default=None, separator=",", prefix=None)`

Get list value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (list, optional): Default value if not found
- `separator` (str): List item separator (default: ",")
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `list[str]`: Parsed list or default

**Example:**
```python
from provide.foundation.utils import get_list

# Basic usage
allowed_hosts = get_list("ALLOWED_HOSTS", ["localhost"])
# ALLOWED_HOSTS=example.com,api.example.com -> ["example.com", "api.example.com"]

# Custom separator
features = get_list("FEATURES", [], separator="|")
# FEATURES=auth|logging|metrics -> ["auth", "logging", "metrics"]
```

### `get_dict(key, default=None, item_sep=",", kv_sep="=", prefix=None)`

Get dictionary value from environment variable.

**Parameters:**
- `key` (str): Environment variable name  
- `default` (dict, optional): Default value if not found
- `item_sep` (str): Item separator (default: ",")
- `kv_sep` (str): Key-value separator (default: "=")
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `dict[str, str]`: Parsed dictionary or default

**Example:**
```python
from provide.foundation.utils import get_dict

# Basic usage
db_config = get_dict("DB_CONFIG", {})
# DB_CONFIG=host=localhost,port=5432,name=mydb
# -> {"host": "localhost", "port": "5432", "name": "mydb"}

# Custom separators  
headers = get_dict("HTTP_HEADERS", {}, item_sep="|", kv_sep=":")
# HTTP_HEADERS=Content-Type:application/json|Authorization:Bearer token
```

### `get_path(key, default=None, prefix=None)`

Get Path object from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (Path, optional): Default Path if not found  
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `Path | None`: Path object or default

**Example:**
```python
from provide.foundation.utils import get_path

config_dir = get_path("CONFIG_DIR", Path("/etc/myapp"))
data_path = get_path("DATA_PATH", prefix="APP")  # APP_DATA_PATH
```

## Best Practices

1. **Use Type-Safe Environment Parsing**: Always use the appropriate `get_*` function for your data type instead of raw `os.getenv()`.

2. **Consistent Naming with Prefixes**: Use prefixes to group related environment variables and avoid naming conflicts.

3. **Provide Sensible Defaults**: Always provide appropriate default values for environment variables to ensure your application works out-of-the-box.