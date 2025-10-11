# Integration Patterns

Advanced integration with frameworks and services, including FastAPI, Django, Celery, and custom configuration sources.

## FastAPI Integration

```python
from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import time
import uuid
from provide.foundation import get_logger, Context, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

class LoggingMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for request logging."""
    
    def __init__(self, app, logger_name: str = "api"):
        super().__init__(app)
        self.logger = get_logger(logger_name)
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Log request start
        self.logger.info("Request started",
                        request_id=request_id,
                        method=request.method,
                        url=str(request.url),
                        headers=dict(request.headers),
                        client_ip=request.client.host)
        
        try:
            # Process request
            response = await call_next(request)
            
            # Log successful response
            duration = time.time() - start_time
            self.logger.info("Request completed",
                           request_id=request_id,
                           status_code=response.status_code,
                           duration_seconds=duration)
            
            return response
            
        except Exception as e:
            # Log error
            duration = time.time() - start_time
            self.logger.error("Request failed",
                            request_id=request_id,
                            exception=str(e),
                            duration_seconds=duration)
            raise

# Setup FastAPI with logging
def create_app():
    # Configure logging
    config = TelemetryConfig(
        service_name="my-api",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json"
        )
    )
    setup_telemetry(config)
    
    # Create app with middleware
    app = FastAPI(title="My API")
    app.add_middleware(LoggingMiddleware)
    
    return app

app = create_app()
api_log = get_logger("api")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    api_log.info("Fetching user", user_id=user_id)
    
    # Simulate database lookup
    await asyncio.sleep(0.05)
    
    user = {"id": user_id, "name": f"User {user_id}"}
    api_log.info("User fetched successfully", user_id=user_id, user=user)
    
    return user
```

## Django Integration

```python
import logging
import time
from django.utils.deprecation import MiddlewareMixin
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

class DjangoFoundationLoggingMiddleware(MiddlewareMixin):
    """Django middleware for provide.foundation logging."""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = get_logger("django")
        
    def process_request(self, request):
        request.start_time = time.time()
        request.logger = self.logger.bind(
            request_id=getattr(request, 'id', 'unknown'),
            path=request.path,
            method=request.method
        )
        
        request.logger.info("Request started",
                          user=getattr(request.user, 'username', 'anonymous') if hasattr(request, 'user') else 'unknown',
                          ip=request.META.get('REMOTE_ADDR'))
        
    def process_response(self, request, response):
        if hasattr(request, 'start_time') and hasattr(request, 'logger'):
            duration = time.time() - request.start_time
            request.logger.info("Request completed",
                              status_code=response.status_code,
                              duration_seconds=duration)
        return response
    
    def process_exception(self, request, exception):
        if hasattr(request, 'logger'):
            request.logger.error("Request failed",
                                exception=str(exception),
                                exception_type=type(exception).__name__)

# Django settings integration
class FoundationLoggingConfig:
    """Django settings for provide.foundation."""
    
    @classmethod
    def setup(cls, debug=False, log_level="INFO"):
        """Setup provide.foundation for Django."""
        config = TelemetryConfig(
            service_name="django-app",
            debug=debug,
            logging=LoggingConfig(
                default_level=log_level,
                console_formatter="json" if not debug else "key_value",
                module_levels={
                    "django.db.backends": "WARNING",  # Reduce SQL query logs
                    "django.request": "INFO"
                }
            )
        )
        setup_telemetry(config)

# In Django views
from django.http import JsonResponse
from provide.foundation import get_logger

def user_view(request, user_id):
    log = get_logger("views.user")
    
    log.info("Fetching user", user_id=user_id)
    
    try:
        # Simulate user lookup
        user_data = {"id": user_id, "name": f"User {user_id}"}
        
        log.info("User retrieved successfully", user_id=user_id)
        return JsonResponse(user_data)
        
    except Exception as e:
        log.error("Failed to retrieve user", user_id=user_id, error=str(e))
        return JsonResponse({"error": "User not found"}, status=404)
```

## Celery Integration

```python
from celery import Celery
from celery.signals import task_prerun, task_postrun, task_failure
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
import time

# Configure logging for Celery
config = TelemetryConfig(
    service_name="celery-worker",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json"
    )
)
setup_telemetry(config)

app = Celery('myapp')
celery_log = get_logger("celery")

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Log task start."""
    celery_log.info("Task started",
                   task_id=task_id,
                   task_name=task.name,
                   args=args,
                   kwargs=kwargs)

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, 
                        retval=None, state=None, **kwds):
    """Log task completion."""
    celery_log.info("Task completed",
                   task_id=task_id,
                   task_name=task.name,
                   state=state,
                   result_type=type(retval).__name__)

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwds):
    """Log task failure."""
    celery_log.error("Task failed",
                    task_id=task_id,
                    task_name=sender.name,
                    exception=str(exception),
                    exception_type=type(exception).__name__)

@app.task
def process_data(data_id: int):
    """Example Celery task with logging."""
    task_log = get_logger("tasks.process_data")
    
    task_log.info("Processing data", data_id=data_id)
    
    try:
        # Simulate data processing
        time.sleep(2)
        
        result = {"data_id": data_id, "processed": True, "timestamp": time.time()}
        
        task_log.info("Data processing completed", 
                     data_id=data_id,
                     result=result)
        
        return result
        
    except Exception as e:
        task_log.error("Data processing failed", 
                      data_id=data_id,
                      error=str(e))
        raise
```

## Extension Points and Customization

### Custom Configuration Sources

```python
from provide.foundation import Context
from typing import Dict, Any
import requests
import json

class RemoteConfigSource:
    """Load configuration from remote service."""
    
    def __init__(self, config_url: str, api_key: str):
        self.config_url = config_url
        self.api_key = api_key
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from remote service."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(self.config_url, headers=headers)
        response.raise_for_status()
        return response.json()

class VaultConfigSource:
    """Load secrets from HashiCorp Vault."""
    
    def __init__(self, vault_url: str, vault_token: str):
        self.vault_url = vault_url
        self.vault_token = vault_token
    
    def load_secrets(self, path: str) -> Dict[str, Any]:
        """Load secrets from Vault."""
        headers = {"X-Vault-Token": self.vault_token}
        response = requests.get(f"{self.vault_url}/v1/{path}", headers=headers)
        response.raise_for_status()
        return response.json()["data"]

class AdvancedContext(Context):
    """Extended Context with remote configuration support."""
    
    def load_remote_config(self, config_source: RemoteConfigSource):
        """Load configuration from remote source."""
        try:
            config_data = config_source.load_config()
            
            # Update context with remote configuration
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    
        except Exception as e:
            # Log error but don't fail initialization
            print(f"Failed to load remote config: {e}")
    
    def load_vault_secrets(self, vault_source: VaultConfigSource, secret_path: str):
        """Load secrets from Vault."""
        try:
            secrets = vault_source.load_secrets(secret_path)
            
            # Apply secrets to context
            for key, value in secrets.items():
                setattr(self, f"secret_{key}", value)
                
        except Exception as e:
            print(f"Failed to load vault secrets: {e}")

# Usage
remote_source = RemoteConfigSource("https://config.example.com/api/config", "api-key")
vault_source = VaultConfigSource("https://vault.example.com", "vault-token")

ctx = AdvancedContext()
ctx.load_remote_config(remote_source)
ctx.load_vault_secrets(vault_source, "secret/myapp/config")
```

#### AWS Secrets Manager Integration

```python
from provide.foundation.config import BaseConfig, env_field
from attrs import define
import boto3
import json
from typing import Any

class AWSSecretsConfigLoader:
    """Load secrets from AWS Secrets Manager."""

    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("secretsmanager", region_name=region_name)

    def load_secret(self, secret_name: str) -> dict[str, Any]:
        """Load and parse secret from AWS Secrets Manager."""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)

            # Parse secret string (assumes JSON format)
            if "SecretString" in response:
                return json.loads(response["SecretString"])
            else:
                # Binary secrets (base64 decoded)
                import base64
                return json.loads(base64.b64decode(response["SecretBinary"]))

        except Exception as e:
            raise RuntimeError(f"Failed to load secret {secret_name}: {e}")

@define
class AppConfigWithAWS(BaseConfig):
    """Application configuration with AWS Secrets Manager integration."""

    database_url: str = env_field(env_var="DATABASE_URL")
    api_key: str = env_field(env_var="API_KEY")
    cache_ttl: int = env_field(env_var="CACHE_TTL", default=3600)

    @classmethod
    def from_aws_secrets(cls, secret_name: str, region: str = "us-east-1"):
        """Load configuration from AWS Secrets Manager."""
        loader = AWSSecretsConfigLoader(region_name=region)
        secrets = loader.load_secret(secret_name)

        # Merge with environment variables (env vars take precedence)
        import os
        config_dict = {
            "database_url": os.getenv("DATABASE_URL", secrets.get("database_url")),
            "api_key": os.getenv("API_KEY", secrets.get("api_key")),
            "cache_ttl": int(os.getenv("CACHE_TTL", secrets.get("cache_ttl", 3600))),
        }

        return cls(**config_dict)

# Usage
config = AppConfigWithAWS.from_aws_secrets("myapp/production", region="us-west-2")
print(f"Database: {config.database_url}")
print(f"Cache TTL: {config.cache_ttl}")
```

**Best Practices:**
- Use IAM roles for authentication (avoid hardcoded credentials)
- Enable secret rotation in AWS Secrets Manager
- Cache secrets locally with TTL to reduce API calls
- Use environment variables for non-sensitive configuration

#### Azure Key Vault Integration

```python
from provide.foundation.config import BaseConfig, env_field
from attrs import define
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from typing import Any

class AzureKeyVaultLoader:
    """Load secrets from Azure Key Vault."""

    def __init__(self, vault_url: str):
        """
        Initialize Azure Key Vault client.

        Args:
            vault_url: Azure Key Vault URL (e.g., "https://myvault.vault.azure.net")
        """
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=self.credential)

    def load_secret(self, secret_name: str) -> str:
        """Load a single secret from Azure Key Vault."""
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            raise RuntimeError(f"Failed to load secret {secret_name}: {e}")

    def load_secrets(self, secret_names: list[str]) -> dict[str, str]:
        """Load multiple secrets from Azure Key Vault."""
        return {name: self.load_secret(name) for name in secret_names}

@define
class AppConfigWithAzure(BaseConfig):
    """Application configuration with Azure Key Vault integration."""

    database_host: str = env_field(env_var="DB_HOST")
    database_password: str = env_field(env_var="DB_PASSWORD")
    api_secret_key: str = env_field(env_var="API_SECRET_KEY")
    redis_url: str = env_field(env_var="REDIS_URL", default="redis://localhost:6379")

    @classmethod
    def from_azure_keyvault(cls, vault_url: str, secret_mapping: dict[str, str]):
        """
        Load configuration from Azure Key Vault.

        Args:
            vault_url: Azure Key Vault URL
            secret_mapping: Map of field names to Key Vault secret names
                           Example: {"database_password": "db-password", ...}
        """
        loader = AzureKeyVaultLoader(vault_url)

        # Load secrets from Key Vault
        secrets = {}
        for field_name, secret_name in secret_mapping.items():
            try:
                secrets[field_name] = loader.load_secret(secret_name)
            except Exception as e:
                # Log error but continue (allow env vars as fallback)
                print(f"Warning: Could not load {secret_name} from Key Vault: {e}")

        # Merge with environment variables (env vars take precedence)
        import os
        config_dict = {
            "database_host": os.getenv("DB_HOST", secrets.get("database_host", "localhost")),
            "database_password": os.getenv("DB_PASSWORD", secrets.get("database_password")),
            "api_secret_key": os.getenv("API_SECRET_KEY", secrets.get("api_secret_key")),
            "redis_url": os.getenv("REDIS_URL", secrets.get("redis_url", "redis://localhost:6379")),
        }

        return cls(**config_dict)

# Usage
config = AppConfigWithAzure.from_azure_keyvault(
    vault_url="https://myapp-vault.vault.azure.net",
    secret_mapping={
        "database_password": "myapp-db-password",
        "api_secret_key": "myapp-api-secret",
    }
)

print(f"Database host: {config.database_host}")
print(f"Redis URL: {config.redis_url}")
```

**Best Practices:**
- Use Managed Identity for Azure authentication (no credentials in code)
- Enable soft-delete and purge protection on Key Vault
- Use separate Key Vaults for different environments (dev/staging/prod)
- Cache secrets locally with TTL to reduce Key Vault API calls
- Use Azure RBAC for fine-grained access control

#### Comparison: Cloud Secret Managers

| Feature | AWS Secrets Manager | Azure Key Vault | HashiCorp Vault |
|---------|---------------------|-----------------|-----------------|
| **Authentication** | IAM roles, access keys | Managed Identity, Service Principal | Token, AppRole, K8s auth |
| **Secret Rotation** | ✅ Automatic | ✅ Automatic | ✅ Manual/automated |
| **Versioning** | ✅ Automatic | ✅ Automatic | ✅ Explicit versions |
| **Cost** | $0.40/secret/month | $0.03/10k operations | Self-hosted or Cloud |
| **Integration** | Native AWS SDK | Azure SDK | HTTP API, SDKs |
| **Best For** | AWS-native apps | Azure-native apps | Multi-cloud, K8s |

### Custom CLI Adapters

provide.foundation currently provides `ClickAdapter` for Click-based CLIs. You can create custom adapters for other CLI frameworks like Typer or argparse.

#### Creating a Typer Adapter

```python
from provide.foundation.cli.base import CLIAdapter
from provide.foundation.cli.registry import get_command_registry
from provide.foundation import logger
import typer
from typing import Any

class TyperAdapter(CLIAdapter):
    """CLI adapter for Typer framework."""

    def __init__(self, app_name: str = "app"):
        self.app = typer.Typer(name=app_name, help="CLI application powered by provide.foundation")
        self.registry = get_command_registry()
        self._register_commands()

    def _register_commands(self):
        """Register all commands from the command registry into Typer."""
        for command_name in self.registry.list_commands():
            command = self.registry.get_command(command_name)

            # Create Typer command wrapper
            def make_command_func(cmd):
                def command_func(**kwargs: Any):
                    """Execute command with provided arguments."""
                    try:
                        logger.info(f"Executing command: {cmd.name}", args=kwargs)
                        result = cmd.execute(**kwargs)

                        if result is not None:
                            typer.echo(result)

                        logger.info(f"Command completed: {cmd.name}")

                    except Exception as e:
                        logger.error(f"Command failed: {cmd.name}", error=str(e))
                        typer.echo(f"Error: {e}", err=True)
                        raise typer.Exit(code=1)

                return command_func

            # Register command with Typer
            self.app.command(name=command_name, help=command.description)(
                make_command_func(command)
            )

    def run(self, args: list[str] | None = None):
        """Run the Typer CLI application."""
        self.app()

    def add_command(self, name: str, func: Any, **kwargs: Any):
        """Add a command to the Typer app."""
        self.app.command(name=name, **kwargs)(func)

# Usage
from provide.foundation.cli.commands import Command

class GreetCommand(Command):
    """Greet a user."""

    name = "greet"
    description = "Greet a user by name"

    def execute(self, name: str, formal: bool = False):
        """Execute the greet command."""
        if formal:
            return f"Good day, {name}!"
        else:
            return f"Hello, {name}!"

# Register command
registry = get_command_registry()
registry.register(GreetCommand())

# Create and run Typer adapter
adapter = TyperAdapter(app_name="myapp")
adapter.run()
```

**Running the Typer CLI:**
```bash
$ python myapp.py greet --name "Alice"
Hello, Alice!

$ python myapp.py greet --name "Bob" --formal
Good day, Bob!

$ python myapp.py --help
Usage: myapp [OPTIONS] COMMAND [ARGS]...

  CLI application powered by provide.foundation

Commands:
  greet  Greet a user by name
```

#### Creating an argparse Adapter

```python
from provide.foundation.cli.base import CLIAdapter
from provide.foundation.cli.registry import get_command_registry
from provide.foundation import logger
import argparse
from typing import Any

class ArgparseAdapter(CLIAdapter):
    """CLI adapter for argparse."""

    def __init__(self, prog: str = "app", description: str = "CLI application"):
        self.parser = argparse.ArgumentParser(prog=prog, description=description)
        self.subparsers = self.parser.add_subparsers(dest="command", help="Available commands")
        self.registry = get_command_registry()
        self._register_commands()

    def _register_commands(self):
        """Register all commands from the command registry into argparse."""
        for command_name in self.registry.list_commands():
            command = self.registry.get_command(command_name)

            # Create subparser for this command
            subparser = self.subparsers.add_parser(
                command_name,
                help=command.description
            )

            # Add command-specific arguments
            # (In a real implementation, introspect command.execute signature)
            subparser.add_argument("--verbose", action="store_true", help="Verbose output")

            # Store command reference
            subparser.set_defaults(command_obj=command)

    def run(self, args: list[str] | None = None):
        """Run the argparse CLI application."""
        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return

        # Execute the command
        command = parsed_args.command_obj
        try:
            logger.info(f"Executing command: {command.name}")

            # Convert parsed args to kwargs (excluding internal fields)
            kwargs = {k: v for k, v in vars(parsed_args).items()
                     if k not in ["command", "command_obj"]}

            result = command.execute(**kwargs)

            if result is not None:
                print(result)

            logger.info(f"Command completed: {command.name}")

        except Exception as e:
            logger.error(f"Command failed: {command.name}", error=str(e))
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def add_command(self, name: str, func: Any, **kwargs: Any):
        """Add a custom command to argparse."""
        subparser = self.subparsers.add_parser(name, **kwargs)
        subparser.set_defaults(func=func)

# Usage
adapter = ArgparseAdapter(prog="myapp", description="My CLI Application")
adapter.run()
```

**Comparison: CLI Frameworks**

| Framework | Adapter Status | Type Hints | Async Support | Complexity |
|-----------|---------------|------------|---------------|------------|
| **Click** | ✅ Built-in (`ClickAdapter`) | Limited | ✅ Yes | Low |
| **Typer** | ⚠️ Custom (example above) | ✅ Native | ✅ Yes | Low |
| **argparse** | ⚠️ Custom (example above) | ❌ No | ❌ No | Medium |
| **Fire** | ⚠️ Custom (community) | ✅ Introspection | ❌ No | Very Low |

**See also:** [Limitations: CLI Adapter Ecosystem](../../architecture/limitations.md#cli-adapter-ecosystem)