# Use Cases

## When to Use provide.foundation

### 🎯 Perfect For

#### CLI Applications
- **Command-line tools** that need structured logging and configuration
- **Developer tooling** requiring rich console output and error handling
- **Automation scripts** needing JSON output modes
- **System utilities** requiring cross-platform compatibility

#### Web Applications
- **FastAPI/Flask applications** needing structured logging
- **Async web services** requiring performance and observability  
- **API services** needing consistent error handling
- **Microservices** requiring distributed logging patterns

#### Enterprise Applications
- **Production systems** requiring robust error handling
- **Multi-environment deployments** needing flexible configuration
- **Compliance-heavy applications** requiring audit logging
- **High-performance systems** needing efficient logging

#### DevOps & Infrastructure
- **Deployment scripts** needing structured output
- **Monitoring tools** requiring consistent log formats
- **CI/CD pipelines** needing machine-readable output
- **System administration tools** requiring cross-platform support

### 🔧 Common Scenarios

#### Replace Multiple Libraries
Instead of managing separate libraries for:
- Logging (structlog + colorama + emoji)
- CLI (click + rich)
- Configuration (pydantic + python-dotenv)
- Process management (subprocess + psutil)

Use provide.foundation as a unified foundation.

#### Standardize Team Development
- **Consistent logging patterns** across all team projects
- **Shared CLI conventions** for all internal tools
- **Unified configuration approaches** for deployments
- **Common error handling patterns** for maintenance

#### Legacy System Modernization
- **Gradually replace** print statements with structured logging
- **Add configuration management** to hardcoded applications
- **Introduce error boundaries** to unstable systems
- **Standardize CLI interfaces** for operational tools

### ❌ Not Recommended For

#### Simple Scripts
- One-off scripts that don't need structured output
- Throwaway prototypes or proof-of-concepts
- Scripts with no error handling requirements

#### GUI Applications
- Desktop applications with GUI frameworks
- Mobile applications
- Browser-based applications (though APIs powering them are perfect)

#### Domain-Specific Frameworks
- Django applications (use Django's logging)
- Game development (use game engine logging)
- Data science notebooks (use notebook-specific tools)

### 🎨 Architecture Patterns

#### The Foundation Pattern
```python
# Start every project with foundation setup
from provide.foundation import logger, pout, perr
from provide.foundation.logger import TelemetryConfig

# Configure once, use everywhere
config = TelemetryConfig.from_env()
```

#### The CLI Tool Pattern
```python
# Build CLI tools with consistent patterns
from provide.foundation.hub import register_command

@register_command("deploy")
def deploy_application(environment: str):
    logger.info("deployment_started", env=environment)
    # Implementation
    logger.info("deployment_completed", env=environment)
```

#### The Service Pattern
```python
# Build services with structured logging
class UserService:
    def create_user(self, email: str) -> User:
        logger.info("user_creation_started", email=email)
        try:
            # Create user logic
            logger.info("user_created", email=email, user_id=user.id)
            return user
        except Exception as e:
            logger.exception("user_creation_failed", email=email)
            raise
```

## 🚀 Getting Started Decision Tree

1. **Do you need structured logging?** → ✅ Yes, use provide.foundation
2. **Building a CLI tool?** → ✅ Yes, use provide.foundation  
3. **Need configuration management?** → ✅ Yes, use provide.foundation
4. **Want consistent error handling?** → ✅ Yes, use provide.foundation
5. **Working on a simple script?** → ❓ Maybe stick with print()
6. **Building a GUI application?** → ❌ Use domain-specific tools