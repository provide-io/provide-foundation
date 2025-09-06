# Configuration Schema API

Schema definition and validation system with async validators, type checking, and comprehensive field validation.

## Overview

The schema system provides:

- **Type validation** - Ensure fields match expected types
- **Custom validators** - Both sync and async validation functions
- **Field constraints** - Min/max values, choices, patterns
- **Required fields** - Mark fields as mandatory
- **Auto-generation** - Generate schemas from configuration classes
- **Async support** - Validators can perform async operations (database checks, API calls)

## Classes

### SchemaField

Defines validation rules for a single configuration field.

```python
@define
class SchemaField:
    """Schema definition for a configuration field."""
    
    name: str
    type: type | None = None
    required: bool = False
    default: Any = None
    description: str | None = None
    validator: Callable[[Any], bool | Awaitable[bool]] | None = None
    choices: list[Any] | None = None
    min_value: Any = None
    max_value: Any = None
    pattern: str | None = None
    sensitive: bool = False
```

#### Field Attributes

##### name: str
Field name (must match configuration class attribute).

##### type: type | None
Expected Python type (int, str, bool, etc.).

##### required: bool
Whether the field must have a non-None value.

##### default: Any
Default value if field is not provided.

##### description: str | None
Human-readable field description.

##### validator: Callable | None
Custom validation function (sync or async).

##### choices: list[Any] | None
List of allowed values.

##### min_value / max_value: Any
Minimum and maximum allowed values (for comparable types).

##### pattern: str | None
Regular expression pattern for string validation.

##### sensitive: bool
Whether field contains sensitive data (affects logging/export).

#### Methods

##### validate(value)

Validate a value against this field's rules.

```python
async def validate(self, value: Any) -> None:
    """
    Validate a value against this schema field.
    
    Args:
        value: Value to validate
        
    Raises:
        ConfigValidationError: If validation fails
    """
```

**Validation order:**
1. Required field check
2. Type validation
3. Choice validation
4. Min/max value validation
5. Pattern validation (for strings)
6. Custom validator function

#### Usage Examples

```python
from provide.foundation.config.schema import SchemaField

# Basic type validation
name_field = SchemaField(
    name="name",
    type=str,
    required=True,
    description="Application name"
)

# Numeric constraints
port_field = SchemaField(
    name="port",
    type=int,
    min_value=1000,
    max_value=65535,
    default=8000
)

# Choice validation
log_level_field = SchemaField(
    name="log_level",
    type=str,
    choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    default="INFO"
)

# Pattern validation
email_field = SchemaField(
    name="email",
    type=str,
    pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    required=True
)

# Custom validator
async def validate_database_connection(url: str) -> bool:
    """Validate database URL by testing connection."""
    try:
        # Attempt to connect to database
        async with get_connection(url) as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False

db_field = SchemaField(
    name="database_url",
    type=str,
    validator=validate_database_connection,
    required=True
)
```

### ConfigSchema

Container for multiple schema fields with validation methods.

```python
class ConfigSchema:
    """Schema definition for configuration classes."""
    
    def __init__(self, fields: list[SchemaField] | None = None) -> None:
        """
        Initialize configuration schema.
        
        Args:
            fields: List of schema fields
        """
```

#### Methods

##### add_field(field)

Add a field to the schema.

```python
def add_field(self, field: SchemaField) -> None:
    """Add a field to the schema."""
```

##### validate(data)

Validate configuration data against the schema.

```python
async def validate(self, data: ConfigDict) -> None:
    """
    Validate configuration data against schema.
    
    Args:
        data: Configuration data to validate
        
    Raises:
        ConfigValidationError: If validation fails
    """
```

##### apply_defaults(data)

Apply default values to configuration data.

```python
def apply_defaults(self, data: ConfigDict) -> ConfigDict:
    """
    Apply default values to configuration data.
    
    Args:
        data: Configuration data
        
    Returns:
        Data with defaults applied
    """
```

##### filter_extra_fields(data)

Remove fields not defined in the schema.

```python
def filter_extra_fields(self, data: ConfigDict) -> ConfigDict:
    """
    Remove fields not defined in schema.
    
    Args:
        data: Configuration data
        
    Returns:
        Filtered data
    """
```

##### from_config_class(config_class)

Generate schema automatically from a configuration class.

```python
@classmethod
def from_config_class(cls, config_class: type[BaseConfig]) -> ConfigSchema:
    """
    Generate schema from configuration class.
    
    Args:
        config_class: Configuration class
        
    Returns:
        Generated schema
    """
```

#### Usage Examples

```python
from provide.foundation.config.schema import ConfigSchema, SchemaField

# Manual schema creation
schema = ConfigSchema([
    SchemaField("name", str, required=True),
    SchemaField("port", int, min_value=1000, max_value=9999),
    SchemaField("debug", bool, default=False),
])

# Auto-generation from config class
@define(frozen=True)
class DatabaseConfig(BaseConfig):
    host: str = field(default="localhost", description="Database host")
    port: int = field(default=5432, description="Database port")
    username: str = field(description="Database username")
    password: str = field(sensitive=True, description="Database password")

schema = ConfigSchema.from_config_class(DatabaseConfig)

# Validation
config_data = {"host": "postgres.example.com", "port": 5432}

# Apply defaults
config_data = schema.apply_defaults(config_data)

# Validate
try:
    await schema.validate(config_data)
    print("Configuration is valid")
except ConfigValidationError as e:
    print(f"Validation failed: {e}")
```

## Validation Functions

### validate_schema(config, schema)

Validate a configuration instance against a schema.

```python
async def validate_schema(config: BaseConfig, schema: ConfigSchema) -> None:
    """
    Validate configuration instance against schema.
    
    Args:
        config: Configuration instance
        schema: Schema to validate against
        
    Raises:
        ConfigValidationError: If validation fails
    """
```

### Built-in Validators

The module provides common validation functions:

#### validate_port(value)

Validate port number (1-65535).

```python
def validate_port(value: int) -> bool:
    """Validate port number."""
    return 1 <= value <= 65535
```

#### validate_url(value)

Validate URL format.

```python
def validate_url(value: str) -> bool:
    """Validate URL format."""
    # Checks for scheme and netloc presence
```

#### validate_email(value)

Validate email address format.

```python
def validate_email(value: str) -> bool:
    """Validate email format."""
    # Uses regex pattern for email validation
```

#### validate_path(value)

Validate file path.

```python
def validate_path(value: str) -> bool:
    """Validate file path."""
    # Checks if path can be parsed by pathlib
```

#### validate_version(value)

Validate Contextual version format.

```python
def validate_version(value: str) -> bool:
    """Validate Contextual version."""
    # Validates format: MAJOR.MINOR.PATCH[-prerelease][+build]
```

#### validate_url_accessible(value) (async)

Example async validator that checks URL accessibility.

```python
async def validate_url_accessible(value: str) -> bool:
    """Validate URL is accessible (example async validator)."""
    # Would typically use aiohttp to check URL
```

## Usage Patterns

### Application Configuration Schema

```python
from provide.foundation.config.schema import ConfigSchema, SchemaField, validate_port, validate_email

# Define comprehensive application schema
app_schema = ConfigSchema([
    # Basic fields
    SchemaField(
        name="name",
        type=str,
        required=True,
        description="Application name"
    ),
    
    # Network configuration
    SchemaField(
        name="host",
        type=str,
        default="0.0.0.0",
        description="Bind address"
    ),
    SchemaField(
        name="port",
        type=int,
        validator=validate_port,
        default=8000,
        description="HTTP port"
    ),
    
    # Environment settings
    SchemaField(
        name="environment",
        type=str,
        choices=["development", "staging", "production"],
        default="development",
        description="Deployment environment"
    ),
    
    # Feature flags
    SchemaField(
        name="debug",
        type=bool,
        default=False,
        description="Enable debug mode"
    ),
    
    # Contact information
    SchemaField(
        name="admin_email",
        type=str,
        validator=validate_email,
        required=True,
        description="Administrator email"
    ),
])

# Use with ConfigManager
await manager.register("app", schema=app_schema)
```

### Custom Async Validators

```python
import aiohttp
from provide.foundation.config.schema import SchemaField

async def validate_api_endpoint(url: str) -> bool:
    """Validate API endpoint is accessible."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                return response.status < 500
    except Exception:
        return False

async def validate_database_connection(connection_string: str) -> bool:
    """Validate database connection string."""
    try:
        # Use your database library
        async with create_connection(connection_string) as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False

# Use in schema
integration_schema = ConfigSchema([
    SchemaField(
        name="api_endpoint",
        type=str,
        validator=validate_api_endpoint,
        required=True,
        description="External API endpoint"
    ),
    SchemaField(
        name="database_url",
        type=str,
        validator=validate_database_connection,
        required=True,
        sensitive=True,
        description="Database connection string"
    ),
])
```

### Dynamic Schema Generation

```python
def create_schema_for_environment(env: str) -> ConfigSchema:
    """Create schema based on deployment environment."""
    base_fields = [
        SchemaField("name", str, required=True),
        SchemaField("port", int, validator=validate_port),
    ]
    
    if env == "production":
        # Production requires additional fields
        base_fields.extend([
            SchemaField("ssl_cert", str, required=True),
            SchemaField("ssl_key", str, required=True, sensitive=True),
            SchemaField("admin_email", str, validator=validate_email, required=True),
        ])
    elif env == "development":
        # Development allows debug mode
        base_fields.append(
            SchemaField("debug", bool, default=True)
        )
    
    return ConfigSchema(base_fields)

# Usage
env = os.getenv("ENVIRONMENT", "development")
schema = create_schema_for_environment(env)
```

### Schema with ConfigManager Integration

```python
from provide.foundation.config.manager import ConfigManager

# Setup with comprehensive validation
async def setup_configuration():
    manager = ConfigManager()
    
    # Create schemas
    app_schema = ConfigSchema.from_config_class(AppConfig)
    db_schema = ConfigSchema([
        SchemaField("host", str, required=True),
        SchemaField("port", int, validator=validate_port),
        SchemaField("database", str, required=True),
        SchemaField("username", str, required=True),
        SchemaField("password", str, required=True, sensitive=True),
    ])
    
    # Register configurations with schemas
    await manager.register("app", schema=app_schema)
    await manager.register("database", schema=db_schema)
    
    # Load and validate
    try:
        app_config = await manager.load("app", AppConfig)
        db_config = await manager.load("database", DatabaseConfig)
        
        print("All configurations validated successfully")
        return app_config, db_config
        
    except ConfigValidationError as e:
        print(f"Configuration validation failed:")
        print(f"  Field: {e.field_name}")
        print(f"  Value: {e.field_value}")
        print(f"  Error: {e.message}")
        raise
```

## Error Handling

The schema system provides detailed validation errors:

```python
from provide.foundation.errors.config import ConfigValidationError

try:
    await schema.validate(config_data)
except ConfigValidationError as e:
    print(f"Validation failed for field '{e.field_name}'")
    print(f"Value: {e.field_value}")
    print(f"Error: {e.message}")
    
    # Access additional context
    if hasattr(e, 'context'):
        print(f"Context: {e.context}")
```

## Performance Considerations

- **Async validators**: Use for I/O operations (database, network checks)
- **Sync validators**: Use for CPU-bound validation (regex, type checks)
- **Validation caching**: Consider caching results for expensive validators
- **Schema reuse**: Generate schemas once and reuse across configuration instances

## Related Documentation

- [api-Configuration Base API](api-base.md) - BaseConfig and field definitions
- [api-Configuration Manager API](api-manager.md) - Using schemas with ConfigManager
- [api-Environment Config API](api-env.md) - Environment-specific validation
- [Configuration Best Practices](../../guide/config/best-practices.md) - Validation strategies