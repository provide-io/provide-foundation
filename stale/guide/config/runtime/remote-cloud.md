# Cloud Service Integration

Integration with cloud configuration services including AWS Parameter Store, Consul, and other cloud platforms.

## AWS Parameter Store

### Basic Parameter Loading

```python
import asyncio
import boto3
from botocore.exceptions import ClientError
from provide.foundation.config import BaseConfig, ConfigManager
from attrs import define

@define
class AWSConfig(BaseConfig):
    """Configuration loaded from AWS Parameter Store."""
    
    region: str = field(description="AWS region")
    environment: str = field(description="Environment name")
    service_config: dict[str, Any] = field(factory=dict, description="Service configuration")

class AWSParameterStoreLoader:
    """Load configuration from AWS Systems Manager Parameter Store."""
    
    def __init__(self, region: str = "us-west-2"):
        self.ssm = boto3.client("ssm", region_name=region)
        self.region = region
    
    async def load_parameters(self, path_prefix: str) -> dict[str, Any]:
        """Load parameters with given path prefix."""
        try:
            paginator = self.ssm.get_paginator("get_parameters_by_path")
            
            config_data = {}
            
            for page in paginator.paginate(
                Path=path_prefix,
                Recursive=True,
                WithDecryption=True
            ):
                for param in page["Parameters"]:
                    # Convert parameter name to config key
                    key = param["Name"].replace(path_prefix, "").lstrip("/")
                    key = key.replace("/", "_")
                    
                    # Handle different parameter types
                    value = param["Value"]
                    if param.get("Type") == "StringList":
                        value = value.split(",")
                    
                    config_data[key] = value
            
            return config_data
            
        except ClientError as e:
            print(f"Error loading from Parameter Store: {e}")
            raise

async def load_aws_config():
    """Load configuration from AWS Parameter Store."""
    
    loader = AWSParameterStoreLoader(region="us-west-2")
    
    # Load parameters for our application
    config_data = await loader.load_parameters("/myapp/prod")
    
    # Additional AWS metadata
    config_data.update({
        "region": loader.region,
        "environment": "production"
    })
    
    config = AWSConfig(**config_data)
    
    print(f"Loaded AWS configuration from {config.region}:")
    print(f"  Environment: {config.environment}")
    print(f"  Parameters loaded: {len(config.service_config)}")
    
    return config

# Usage  
aws_config = asyncio.run(load_aws_config())
```

### AWS Secrets Manager Integration

```python
import boto3
import json
from botocore.exceptions import ClientError

class AWSSecretsLoader:
    """Load configuration from AWS Secrets Manager."""
    
    def __init__(self, region: str = "us-west-2"):
        self.secrets = boto3.client("secretsmanager", region_name=region)
        self.region = region
    
    async def load_secret(self, secret_name: str) -> dict[str, Any]:
        """Load and parse a secret from Secrets Manager."""
        try:
            response = self.secrets.get_secret_value(SecretId=secret_name)
            
            # Parse JSON secret value
            secret_string = response["SecretString"]
            return json.loads(secret_string)
            
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                raise ConfigurationNotFoundError(f"Secret not found: {secret_name}")
            else:
                raise ConfigurationLoadError(f"Failed to load secret: {e}")
    
    async def load_multiple_secrets(self, secret_names: list[str]) -> dict[str, Any]:
        """Load multiple secrets and merge them."""
        merged_config = {}
        
        for secret_name in secret_names:
            try:
                secret_data = await self.load_secret(secret_name)
                merged_config.update(secret_data)
            except ConfigurationNotFoundError as e:
                print(f"Warning: {e}")
                continue
        
        return merged_config

async def aws_secrets_example():
    """Example of loading configuration from AWS Secrets Manager."""
    
    loader = AWSSecretsLoader()
    
    # Load multiple secrets
    secrets = await loader.load_multiple_secrets([
        "myapp/database-credentials",
        "myapp/api-keys",
        "myapp/external-services"
    ])
    
    # Create configuration with secrets
    config = SecureRemoteConfig(
        database_url=secrets.get("database_url"),
        api_keys=secrets.get("api_keys", {}),
        feature_flags=secrets.get("feature_flags", {})
    )
    
    return config
```

## HashiCorp Consul Integration

### Consul KV Store

```python
import asyncio
import aiohttp
from typing import Any
from provide.foundation.config import BaseConfig
from attrs import define

@define
class ConsulConfig(BaseConfig):
    """Configuration loaded from HashiCorp Consul."""
    
    consul_url: str = field(description="Consul server URL")
    service_config: dict[str, Any] = field(factory=dict, description="Service configuration")
    metadata: dict[str, str] = field(factory=dict, description="Consul metadata")

class ConsulConfigLoader:
    """Load configuration from Consul KV store."""
    
    def __init__(self, consul_url: str = "http://localhost:8500"):
        self.consul_url = consul_url.rstrip("/")
    
    async def load_kv(self, key_prefix: str) -> dict[str, Any]:
        """Load configuration from Consul KV store."""
        
        async with aiohttp.ClientSession() as session:
            # Get all keys under prefix
            url = f"{self.consul_url}/v1/kv/{key_prefix}?recurse=true"
            
            async with session.get(url) as response:
                if response.status == 404:
                    return {}  # No keys found
                
                response.raise_for_status()
                kv_data = await response.json()
        
        # Process Consul KV response
        config_data = {}
        
        for item in kv_data:
            key = item["Key"]
            value = item.get("Value", "")
            
            # Decode base64 value
            if value:
                import base64
                decoded_value = base64.b64decode(value).decode("utf-8")
                
                # Try to parse as JSON
                try:
                    import json
                    parsed_value = json.loads(decoded_value)
                except json.JSONDecodeError:
                    parsed_value = decoded_value
            else:
                parsed_value = None
            
            # Convert key path to nested dict structure
            key_parts = key.replace(key_prefix + "/", "").split("/")
            current = config_data
            
            for part in key_parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            current[key_parts[-1]] = parsed_value
        
        return config_data

async def load_consul_config():
    """Load configuration from Consul."""
    
    loader = ConsulConfigLoader("http://consul.service.consul:8500")
    
    # Load application configuration
    app_config = await loader.load_kv("config/myapp")
    
    config = ConsulConfig(
        consul_url=loader.consul_url,
        service_config=app_config,
        metadata={
            "loader_type": "consul_kv",
            "timestamp": str(asyncio.get_event_loop().time())
        }
    )
    
    print(f"Loaded Consul configuration:")
    print(f"  Consul URL: {config.consul_url}")
    print(f"  Configuration keys: {len(config.service_config)}")
    
    return config

# Usage
consul_config = asyncio.run(load_consul_config())
```

### Consul Service Discovery Integration

```python
class ConsulServiceLoader(ConsulConfigLoader):
    """Extended Consul loader with service discovery."""
    
    async def discover_service(self, service_name: str) -> list[dict[str, Any]]:
        """Discover service instances from Consul."""
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.consul_url}/v1/health/service/{service_name}?passing=true"
            
            async with session.get(url) as response:
                response.raise_for_status()
                services = await response.json()
        
        # Extract service information
        service_instances = []
        
        for service in services:
            service_info = service["Service"]
            node_info = service["Node"]
            
            instance = {
                "id": service_info["ID"],
                "address": service_info["Address"] or node_info["Address"],
                "port": service_info["Port"],
                "tags": service_info.get("Tags", []),
                "meta": service_info.get("Meta", {}),
                "node": node_info["Node"]
            }
            
            service_instances.append(instance)
        
        return service_instances
    
    async def load_service_config(self, service_name: str, key_prefix: str) -> dict[str, Any]:
        """Load configuration including service discovery data."""
        
        # Load KV configuration
        kv_config = await self.load_kv(key_prefix)
        
        # Load service discovery data
        service_instances = await self.discover_service(service_name)
        
        # Combine configuration
        return {
            "service_discovery": {
                service_name: service_instances
            },
            "configuration": kv_config
        }

async def consul_service_discovery_example():
    """Example of Consul with service discovery."""
    
    loader = ConsulServiceLoader()
    
    # Load configuration with service discovery
    config_data = await loader.load_service_config(
        service_name="database",
        key_prefix="config/myapp"
    )
    
    # Extract database instances
    db_instances = config_data["service_discovery"]["database"]
    
    if db_instances:
        primary_db = db_instances[0]  # Use first healthy instance
        database_url = f"postgresql://{primary_db['address']}:{primary_db['port']}/myapp"
        
        print(f"Using database: {database_url}")
        print(f"Available DB instances: {len(db_instances)}")
    
    return config_data
```

## Google Cloud Configuration

### Google Secret Manager

```python
from google.cloud import secretmanager
from google.api_core import exceptions

class GCPSecretLoader:
    """Load configuration from Google Cloud Secret Manager."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()
    
    async def load_secret(self, secret_id: str, version: str = "latest") -> str:
        """Load a secret from Google Secret Manager."""
        try:
            name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version}"
            response = self.client.access_secret_version(request={"name": name})
            
            return response.payload.data.decode("UTF-8")
            
        except exceptions.NotFound:
            raise ConfigurationNotFoundError(f"Secret not found: {secret_id}")
        except Exception as e:
            raise ConfigurationLoadError(f"Failed to load secret {secret_id}: {e}")
    
    async def load_json_secret(self, secret_id: str) -> dict[str, Any]:
        """Load and parse JSON secret."""
        secret_value = await self.load_secret(secret_id)
        
        import json
        return json.loads(secret_value)
    
    async def load_multiple_secrets(self, secret_mapping: dict[str, str]) -> dict[str, Any]:
        """Load multiple secrets into configuration structure."""
        config = {}
        
        for config_key, secret_id in secret_mapping.items():
            try:
                if secret_id.endswith('.json'):
                    # Load as JSON
                    secret_id = secret_id[:-5]  # Remove .json suffix
                    config[config_key] = await self.load_json_secret(secret_id)
                else:
                    # Load as string
                    config[config_key] = await self.load_secret(secret_id)
            except ConfigurationNotFoundError as e:
                print(f"Warning: {e}")
                continue
        
        return config

async def gcp_secrets_example():
    """Example of loading configuration from GCP Secret Manager."""
    
    loader = GCPSecretLoader(project_id="my-project-123")
    
    # Define secret mapping
    secrets_mapping = {
        "database": "app-database-config.json",
        "api_key": "external-api-key",
        "jwt_secret": "jwt-signing-secret"
    }
    
    # Load all secrets
    config_data = await loader.load_multiple_secrets(secrets_mapping)
    
    print(f"Loaded {len(config_data)} configuration sections from GCP")
    
    return config_data
```

## Azure Key Vault Integration

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError

class AzureKeyVaultLoader:
    """Load configuration from Azure Key Vault."""
    
    def __init__(self, vault_url: str):
        self.vault_url = vault_url
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=credential)
    
    async def load_secret(self, secret_name: str) -> str:
        """Load a secret from Azure Key Vault."""
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
            
        except ResourceNotFoundError:
            raise ConfigurationNotFoundError(f"Secret not found: {secret_name}")
        except Exception as e:
            raise ConfigurationLoadError(f"Failed to load secret {secret_name}: {e}")
    
    async def load_configuration(self, secret_prefix: str) -> dict[str, str]:
        """Load all secrets with given prefix."""
        config = {}
        
        # List all secrets
        secret_properties = self.client.list_properties_of_secrets()
        
        for secret_property in secret_properties:
            if secret_property.name.startswith(secret_prefix):
                # Remove prefix from key name
                config_key = secret_property.name[len(secret_prefix):].lstrip('-_')
                
                try:
                    config[config_key] = await self.load_secret(secret_property.name)
                except ConfigurationNotFoundError:
                    continue
        
        return config

async def azure_keyvault_example():
    """Example of loading configuration from Azure Key Vault."""
    
    loader = AzureKeyVaultLoader("https://myapp-keyvault.vault.azure.net/")
    
    # Load all secrets with prefix
    config_data = await loader.load_configuration("myapp-config-")
    
    print(f"Loaded {len(config_data)} configuration values from Azure Key Vault")
    
    return config_data
```

## Best Practices

### 1. Handle Cloud Service Errors Gracefully

```python
# ✅ Good - Specific error handling for cloud services
async def load_cloud_config():
    try:
        return await load_aws_config()
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        if error_code == 'AccessDenied':
            logger.error("AWS access denied - check IAM permissions")
        elif error_code == 'ParameterNotFound':
            logger.warning("Configuration parameters not found, using defaults")
        else:
            logger.error(f"AWS error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading cloud config: {e}")
        raise

# ❌ Bad - Generic error handling
async def load_cloud_config():
    try:
        return await load_aws_config()
    except Exception as e:
        print(f"Error: {e}")  # Not informative
        raise
```

### 2. Use Appropriate IAM/Access Policies

```python
# ✅ Good - Least privilege principle
"""
Required AWS IAM policy for Parameter Store:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:GetParametersByPath"
            ],
            "Resource": "arn:aws:ssm:region:account:parameter/myapp/*"
        }
    ]
}
"""

# ❌ Bad - Overly broad permissions
"""
{
    "Effect": "Allow",
    "Action": "ssm:*",
    "Resource": "*"
}
"""
```

### 3. Implement Proper Secret Rotation

```python
class RotatingSecretLoader:
    """Loader that handles secret rotation gracefully."""
    
    def __init__(self, loader):
        self.loader = loader
        self._cached_secrets = {}
        self._secret_versions = {}
    
    async def load_secret_with_rotation(self, secret_name: str) -> str:
        """Load secret with automatic rotation handling."""
        
        try:
            # Try to load current version
            secret = await self.loader.load_secret(secret_name)
            
            # Cache successful load
            self._cached_secrets[secret_name] = secret
            return secret
            
        except ConfigurationLoadError:
            # If current version fails, try previous version
            if secret_name in self._cached_secrets:
                logger.warning(f"Using cached version of secret: {secret_name}")
                return self._cached_secrets[secret_name]
            
            raise
```

## Next Steps

- [HTTP Loading](remote-http.md) - Load configuration from HTTP endpoints
- [Polling & Updates](remote-polling.md) - Automatic configuration updates
- [Resilience Patterns](remote-resilience.md) - Circuit breakers and caching