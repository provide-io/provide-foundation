# Serialization API

Data serialization utilities supporting multiple formats with type safety and performance optimization.

## Overview

The `serialization` module provides robust serialization and deserialization capabilities for various data formats including JSON, YAML, TOML, MessagePack, and Protobuf. It offers type-safe serialization with automatic validation and performance optimizations.

## Key Features

- **Multiple Formats**: JSON, YAML, TOML, MessagePack, Protobuf support
- **Type Safety**: Automatic type validation and conversion
- **Schema Validation**: Built-in schema validation capabilities
- **Performance Optimization**: Efficient serialization for high-throughput scenarios
- **Streaming Support**: Handle large datasets with streaming serialization
- **Custom Serializers**: Extensible serialization system

## Basic Usage

### JSON Serialization

```python
from provide.foundation.serialization import json_serializer

# Basic JSON operations
data = {"name": "John", "age": 30, "active": True}
json_string = json_serializer.dumps(data)
parsed_data = json_serializer.loads(json_string)

# Type-safe serialization with validation
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    active: bool = True

user = User(name="John", age=30)
json_data = json_serializer.serialize(user)
restored_user = json_serializer.deserialize(json_data, User)
```

### YAML Serialization

```python
from provide.foundation.serialization import yaml_serializer

# YAML operations
config_data = {
    "database": {"host": "localhost", "port": 5432},
    "redis": {"host": "redis", "port": 6379}
}

yaml_string = yaml_serializer.dumps(config_data)
config = yaml_serializer.loads(yaml_string)

# File operations
yaml_serializer.dump_file("config.yaml", config_data)
loaded_config = yaml_serializer.load_file("config.yaml")
```

## Advanced Serialization

### Schema-Based Validation

```python
from provide.foundation.serialization import schema_serializer
from provide.foundation.serialization.schema import Schema, Field

# Define schema
user_schema = Schema([
    Field("name", str, required=True, min_length=1),
    Field("age", int, required=True, min_value=0, max_value=150),
    Field("email", str, pattern=r"^[^@]+@[^@]+\.[^@]+$"),
    Field("active", bool, default=True)
])

# Serialize with validation
serializer = schema_serializer.SchemaSerializer(user_schema)

try:
    data = serializer.serialize(user_data)
    user = serializer.deserialize(data, validate=True)
except ValidationError as e:
    logger.error("validation_failed", errors=e.errors)
```

### Custom Type Serializers

```python
from provide.foundation.serialization import custom_serializer
from datetime import datetime
import uuid

# Register custom type serializers
@custom_serializer.register(datetime)
def serialize_datetime(dt: datetime) -> str:
    return dt.isoformat()

@custom_serializer.register(uuid.UUID)
def serialize_uuid(uid: uuid.UUID) -> str:
    return str(uid)

# Custom deserializers
@custom_serializer.deserializer(datetime)
def deserialize_datetime(data: str) -> datetime:
    return datetime.fromisoformat(data)

# Use with any serializer
data = {"created_at": datetime.now(), "id": uuid.uuid4()}
serialized = json_serializer.dumps(data)  # Custom serializers applied automatically
```

## High-Performance Serialization

### MessagePack Serialization

```python
from provide.foundation.serialization import msgpack_serializer

# High-performance binary serialization
data = {"users": [{"id": i, "name": f"user_{i}"} for i in range(10000)]}

# Faster than JSON for large datasets
binary_data = msgpack_serializer.dumps(data)
restored_data = msgpack_serializer.loads(binary_data)

# Streaming support for large datasets
async def stream_serialize():
    async with msgpack_serializer.stream_writer("output.msgpack") as writer:
        for chunk in large_dataset:
            await writer.write(chunk)
```

### Protobuf Serialization

```python
from provide.foundation.serialization import protobuf_serializer

# Define protobuf schema
user_pb = protobuf_serializer.define_schema("""
syntax = "proto3";

message User {
    string name = 1;
    int32 age = 2;
    bool active = 3;
    repeated string tags = 4;
}
""")

# Serialize to protobuf
user_data = {"name": "John", "age": 30, "active": True, "tags": ["admin", "user"]}
pb_data = protobuf_serializer.serialize(user_data, user_pb)
restored = protobuf_serializer.deserialize(pb_data, user_pb)
```

## Streaming Serialization

### Large Dataset Handling

```python
from provide.foundation.serialization import streaming

# Stream JSON arrays
async def process_large_json():
    async with streaming.json_array_writer("large_output.json") as writer:
        async for item in large_data_source():
            await writer.write_item(item)

    # Stream read large JSON arrays
    async with streaming.json_array_reader("large_output.json") as reader:
        async for item in reader:
            await process_item(item)
```

### Chunked Serialization

```python
# Serialize data in chunks
chunked_serializer = streaming.ChunkedSerializer(
    format="json",
    chunk_size=1000,
    output_pattern="data_chunk_{}.json"
)

await chunked_serializer.serialize_chunks(large_dataset)

# Read chunks back
chunks = await chunked_serializer.read_chunks("data_chunk_*.json")
```

## Format-Specific Features

### TOML Configuration

```python
from provide.foundation.serialization import toml_serializer

# Configuration serialization
app_config = {
    "app": {
        "name": "MyApp",
        "version": "1.0.0"
    },
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp_db"
    }
}

toml_string = toml_serializer.dumps(app_config)
config = toml_serializer.loads(toml_string)

# File operations with validation
toml_serializer.dump_file("config.toml", app_config, validate=True)
```

### XML Serialization

```python
from provide.foundation.serialization import xml_serializer

# XML serialization with namespace support
data = {
    "user": {
        "@xmlns": "http://example.com/user",
        "name": "John Doe",
        "profile": {
            "age": 30,
            "active": True
        }
    }
}

xml_string = xml_serializer.dumps(data)
parsed_data = xml_serializer.loads(xml_string)
```

## Compression Integration

### Compressed Serialization

```python
from provide.foundation.serialization import compressed_serializer

# JSON with gzip compression
compressor = compressed_serializer.GzipSerializer(json_serializer)

compressed_data = compressor.dumps(large_data)  # Serialized + compressed
original_data = compressor.loads(compressed_data)  # Decompressed + deserialized

# Multiple compression algorithms
lz4_serializer = compressed_serializer.LZ4Serializer(msgpack_serializer)
zstd_serializer = compressed_serializer.ZstdSerializer(json_serializer)
```

## Async Serialization

### Async File Operations

```python
from provide.foundation.serialization import async_serializer

# Async file serialization
await async_serializer.dump_file_async("data.json", large_data)
data = await async_serializer.load_file_async("data.json")

# Async streaming
async with async_serializer.stream_writer("output.json") as writer:
    async for item in async_data_source():
        await writer.write(item)
```

## Error Handling

### Serialization Errors

```python
from provide.foundation.serialization.errors import (
    SerializationError,
    DeserializationError,
    ValidationError,
    FormatError
)

try:
    result = json_serializer.serialize(complex_object)
except SerializationError as e:
    logger.error("serialization_failed",
                error=str(e),
                error_type=type(e).__name__,
                object_type=type(complex_object).__name__)

try:
    data = json_serializer.deserialize(invalid_json, User)
except DeserializationError as e:
    logger.error("deserialization_failed",
                error=str(e),
                input_data=invalid_json[:100])  # Log first 100 chars
```

## Performance Optimization

### Serializer Configuration

```python
# High-performance configuration
fast_json = json_serializer.configure(
    ensure_ascii=False,
    separators=(',', ':'),  # No spaces
    sort_keys=False,        # Don't sort
    check_circular=False    # Skip circular reference check
)

# Optimized for specific use cases
compact_serializer = json_serializer.configure(
    compact=True,
    skip_validation=True,  # Skip type validation for speed
    use_c_extension=True   # Use C extension if available
)
```

### Caching Serializers

```python
from provide.foundation.serialization import cached_serializer

# Cache serialization results
@cached_serializer.cache(ttl=300)  # 5-minute cache
def serialize_user_profile(user):
    return json_serializer.serialize(complex_user_profile)

# Schema compilation caching
schema_cache = cached_serializer.SchemaCache()
compiled_schema = schema_cache.get_or_compile(schema_definition)
```

## Testing Support

### Serialization Testing

```python
from provide.foundation.serialization.testing import SerializationTestCase

class TestUserSerialization(SerializationTestCase):
    def test_user_roundtrip(self):
        """Test user serialization roundtrip."""
        original_user = User(name="John", age=30)
        
        # Test JSON roundtrip
        self.assert_roundtrip_equal(json_serializer, original_user)
        
        # Test YAML roundtrip
        self.assert_roundtrip_equal(yaml_serializer, original_user)
    
    def test_validation_errors(self):
        """Test validation error handling."""
        invalid_data = {"name": "", "age": -5}
        
        with self.assertRaises(ValidationError):
            schema_serializer.deserialize(invalid_data, User, validate=True)
```

## Integration Examples

### With Configuration System

```python
from provide.foundation.serialization import config_serializer
from provide.foundation.config import BaseConfig

@dataclass
class AppConfig(BaseConfig):
    database_url: str
    redis_host: str = "localhost"
    debug: bool = False

# Load configuration from multiple formats
config = config_serializer.load_config(
    ["config.yaml", "config.toml", "config.json"],
    schema=AppConfig
)
```

### With Logging

```python
from provide.foundation.serialization import logging_serializer
from provide.foundation import logger

# Serialize log data efficiently
@logging_serializer.log_serialized("data_processed")
def process_data(data):
    # Log entry automatically includes serialized data
    result = complex_processing(data)
    return result

# Custom log serialization
logger.info("user_data", 
           user=logging_serializer.serialize_for_logs(user_object))
```

## Best Practices

### Choose the Right Format
```python
# JSON: Human-readable, web-compatible
json_data = json_serializer.dumps(user_data)

# MessagePack: Binary, high-performance
binary_data = msgpack_serializer.dumps(user_data)

# YAML: Configuration files, human-readable
config_yaml = yaml_serializer.dumps(config_data)

# Protobuf: Schema validation, cross-language
pb_data = protobuf_serializer.serialize(data, schema)
```

### Error Handling
```python
def safe_serialize(data, serializer):
    try:
        return serializer.dumps(data)
    except SerializationError as e:
        logger.error("serialization_failed", error=str(e))
        # Return fallback serialization
        return json_serializer.dumps({"error": "serialization_failed"})
```

### Performance Considerations
```python
# For high-frequency serialization, reuse serializer instances
serializer = json_serializer.configure(optimized=True)

# Use streaming for large datasets
async with streaming.json_writer("large_file.json") as writer:
    async for item in large_dataset:
        await writer.write(item)
```

## API Reference

::: provide.foundation.serialization

## Related Documentation

- [Configuration Guide](../../guide/config/files-formats.md) - Configuration file serialization
- [Performance Guide](../../guide/concepts/performance.md) - Serialization performance optimization
- [Data Pipeline Example](../../examples/data-pipeline.md) - Serialization in data processing