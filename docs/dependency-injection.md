# Dependency Injection in Provide Foundation

Provide Foundation supports **two complementary patterns** for managing dependencies:

1. **Service Locator Pattern** - Simple, global access for framework infrastructure
2. **Dependency Injection Pattern** - Explicit, testable dependencies for application code

This hybrid approach gives you the best of both worlds: the convenience of Service Locator for cross-cutting concerns, and the explicitness and testability of Dependency Injection for your application logic.

## Table of Contents

- [Quick Start](#quick-start)
- [When to Use Which Pattern](#when-to-use-which-pattern)
- [Service Locator Pattern](#service-locator-pattern)
- [Dependency Injection Pattern](#dependency-injection-pattern)
- [Polyglot Mental Model](#polyglot-mental-model)
- [Testing with DI](#testing-with-di)
- [API Reference](#api-reference)

## Quick Start

### Service Locator (Framework Code)

```python
from provide.foundation import logger, get_hub

# Global logger access
logger.info("Processing request")

# Global hub access
hub = get_hub()
component = hub.get_component("my_component")
```

### Dependency Injection (Application Code)

```python
from provide.foundation.hub import Container, injectable

@injectable
class UserService:
    def __init__(self, db: Database, logger: Logger):
        self.db = db
        self.logger = logger

# Composition Root (main.py)
def main():
    container = Container()
    container.register(Database, Database("postgresql://localhost/app"))
    container.register(Logger, Logger("INFO"))

    # Auto-inject dependencies
    service = container.resolve(UserService)
    service.process_users()
```

## When to Use Which Pattern

### Use Service Locator For:

- **Framework infrastructure** - Logging, configuration, event bus
- **Cross-cutting concerns** - Things needed everywhere in your code
- **Lazy initialization** - Components that should initialize on first access
- **Simple scripts** - One-off utilities where explicitness isn't critical

### Use Dependency Injection For:

- **Application business logic** - Your domain services and use cases
- **Testable components** - Code that needs isolated unit testing
- **Clear dependencies** - When you want constructor signatures to show requirements
- **Composition Root** - Application entry points (main.py, app initialization)

## Service Locator Pattern

The Service Locator pattern provides **global access** to framework services through the Hub.

### Example: Framework Infrastructure

```python
from provide.foundation import logger
from provide.foundation.hub import get_hub

def process_request(request_id: str):
    # Logger is globally accessible
    logger.info("Processing request", request_id=request_id)

    # Hub is globally accessible
    hub = get_hub()
    config = hub.get_foundation_config()

    # Use config...
    logger.debug("Config loaded", env=config.env)
```

### Advantages

✅ **Simple** - No boilerplate, just import and use
✅ **Convenient** - Available everywhere without passing around
✅ **Lazy** - Services initialize on first access
✅ **Familiar** - Common pattern in Python frameworks

### Trade-offs

⚠️ **Hidden dependencies** - Not clear what a function/class needs
⚠️ **Global state** - Can make testing harder
⚠️ **Coupling** - Direct dependency on Hub singleton

## Dependency Injection Pattern

The Dependency Injection pattern makes dependencies **explicit** through constructor parameters.

### Example: Application Services

```python
from provide.foundation.hub import Container, injectable

# Step 1: Mark classes as injectable
@injectable
class DatabaseClient:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def query(self, sql: str) -> list[dict]:
        # ... query implementation

@injectable
class UserRepository:
    def __init__(self, db: DatabaseClient, logger: Logger):
        self.db = db
        self.logger = logger

    def find_user(self, user_id: int) -> User:
        self.logger.info("Finding user", user_id=user_id)
        return self.db.query(f"SELECT * FROM users WHERE id = {user_id}")

@injectable
class UserService:
    def __init__(self, repository: UserRepository, logger: Logger):
        self.repository = repository
        self.logger = logger

    def get_user(self, user_id: int) -> User:
        return self.repository.find_user(user_id)

# Step 2: Composition Root (main.py)
def main():
    # Create container
    container = Container()

    # Register infrastructure
    container.register(DatabaseClient, DatabaseClient("postgresql://localhost/myapp"))
    container.register(Logger, Logger("INFO"))

    # Register application services
    repository = container.resolve(UserRepository)
    container.register(UserRepository, repository)

    # Resolve main service
    service = container.resolve(UserService)

    # Run application
    user = service.get_user(42)
    print(f"Found user: {user.name}")

if __name__ == "__main__":
    main()
```

### Advantages

✅ **Explicit** - Constructor shows exactly what's needed
✅ **Testable** - Easy to inject mocks/stubs
✅ **Type-safe** - IDE autocomplete and static type checking
✅ **Modular** - Components are truly independent
✅ **Portable** - Same pattern works in Go, Rust, Java, C#

### Trade-offs

⚠️ **More verbose** - Requires registration in Composition Root
⚠️ **Setup overhead** - Need to wire dependencies explicitly
⚠️ **Learning curve** - Requires understanding DI concepts

## Polyglot Mental Model

One of the key goals of Foundation's DI support is to create a **"golden cage"** - a mental model that works identically across Python, Go, and Rust. This makes it easier for teams working in multiple languages to maintain consistency.

### The Pattern (Python)

```python
@injectable
class UserService:
    def __init__(self, db: Database, logger: Logger):
        self.db = db
        self.logger = logger

# Composition Root
container = Container()
container.register(Database, db_instance)
container.register(Logger, logger_instance)
service = container.resolve(UserService)
```

### The Pattern (Go)

```go
type UserService struct {
    db     *Database
    logger *Logger
}

func NewUserService(db *Database, logger *Logger) *UserService {
    return &UserService{db: db, logger: logger}
}

// Composition Root (main function)
func main() {
    db := NewDatabase("postgresql://localhost/app")
    logger := NewLogger("INFO")
    service := NewUserService(db, logger)
}
```

### The Pattern (Rust)

```rust
struct UserService<'a> {
    db: &'a Database,
    logger: &'a Logger,
}

impl<'a> UserService<'a> {
    fn new(db: &'a Database, logger: &'a Logger) -> Self {
        Self { db, logger }
    }
}

// Composition Root (main function)
fn main() {
    let db = Database::new("postgresql://localhost/app");
    let logger = Logger::new("INFO");
    let service = UserService::new(&db, &logger);
}
```

**The structure is identical** across all three languages:
1. Define dependencies in constructor/new function
2. Create dependencies in Composition Root
3. Pass dependencies explicitly
4. No hidden global state

This consistency means:
- ✅ Teams can onboard faster across languages
- ✅ Architecture patterns are directly transferable
- ✅ Code reviews are easier across polyglot codebases
- ✅ Documentation and training apply to all languages

## Testing with DI

Dependency Injection makes testing **dramatically simpler** by allowing you to inject test doubles.

### Without DI (Hard to Test)

```python
from provide.foundation.hub import get_hub

class UserService:
    def get_user(self, user_id: int) -> User:
        # Hard-coded dependency on global hub
        hub = get_hub()
        db = hub.get_component("database")
        return db.query(f"SELECT * FROM users WHERE id = {user_id}")

# Testing requires mocking the global hub - messy!
```

### With DI (Easy to Test)

```python
@injectable
class UserService:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def get_user(self, user_id: int) -> User:
        return self.db.query(f"SELECT * FROM users WHERE id = {user_id}")

# Testing is simple - just inject a mock!
def test_get_user():
    mock_db = MockDatabase()
    service = UserService(mock_db)

    user = service.get_user(42)

    assert user.id == 42
    assert mock_db.query_called_with("SELECT * FROM users WHERE id = 42")
```

### Using test_scope() for Integration Tests

```python
from provide.foundation.testmode import test_scope

def test_user_service_integration():
    with test_scope() as hub:
        # Register test dependencies
        hub.register(DatabaseClient, test_db_instance)
        hub.register(Logger, test_logger)

        # Resolve service with test dependencies
        service = hub.resolve(UserService)

        # Test with isolated dependencies
        user = service.get_user(42)
        assert user.name == "Test User"
```

## API Reference

### `@injectable` Decorator

Marks a class as suitable for dependency injection.

```python
@injectable
class MyService:
    def __init__(self, dependency: SomeType):
        self.dependency = dependency
```

**Requirements:**
- Class must define its own `__init__` method
- All constructor parameters (except `self`) must have type hints
- Type hints must be resolvable types (not forward references unless available at runtime)

**Raises:**
- `ValidationError` if requirements aren't met

### `Container` Class

A dependency injection container for registering and resolving dependencies.

```python
container = Container()
```

#### `container.register(type_hint, instance, name=None)`

Register a dependency by type.

```python
container.register(Database, db_instance)
container.register(Logger, logger_instance, name="app_logger")
```

**Parameters:**
- `type_hint` (type): Type to register under
- `instance` (Any): Instance to register
- `name` (str, optional): Optional name for named registration

**Returns:** `Container` (for method chaining)

#### `container.resolve(cls, **overrides)`

Resolve a class with automatic dependency injection.

```python
service = container.resolve(UserService)
# Or with overrides:
service = container.resolve(UserService, logger=custom_logger)
```

**Parameters:**
- `cls` (type): Class to instantiate
- `**overrides`: Explicitly provided dependencies (override registry)

**Returns:** Instance of `cls` with dependencies injected

**Raises:**
- `NotFoundError` if required dependency not registered
- `ValidationError` if instantiation fails

#### `container.get(type_hint)`

Get a registered instance by type.

```python
db = container.get(Database)
```

**Returns:** Registered instance or `None` if not found

#### `container.has(type_hint)`

Check if a type is registered.

```python
if container.has(Database):
    db = container.get(Database)
```

**Returns:** `bool`

### `Hub.register()` and `Hub.resolve()`

The Hub itself supports DI methods:

```python
from provide.foundation.hub import get_hub

hub = get_hub()
hub.register(Database, db_instance)
service = hub.resolve(UserService)
```

This allows mixing Service Locator and DI patterns in the same codebase.

## Best Practices

### 1. Use Composition Root Pattern

Create all dependencies in one place (usually `main.py`):

```python
def main():
    container = Container()

    # Infrastructure
    container.register(Database, Database.from_env())
    container.register(Cache, RedisCache.from_env())
    container.register(Logger, Logger("INFO"))

    # Services
    repo = container.resolve(UserRepository)
    container.register(UserRepository, repo)

    # Entry point
    app = container.resolve(Application)
    app.run()
```

### 2. Keep @injectable Classes Pure

Don't mix Service Locator and DI in the same class:

```python
# ❌ BAD: Mixing patterns
@injectable
class MyService:
    def __init__(self, db: Database):
        self.db = db
        self.logger = get_hub().get_foundation_logger()  # Service Locator!

# ✅ GOOD: Pure DI
@injectable
class MyService:
    def __init__(self, db: Database, logger: Logger):
        self.db = db
        self.logger = logger
```

### 3. Use Service Locator for Cross-Cutting Concerns

```python
from provide.foundation import logger  # Global logger is fine!

@injectable
class UserService:
    def __init__(self, db: Database):
        self.db = db

    def process_user(self, user_id: int):
        # Using global logger is acceptable for logging
        logger.info("Processing user", user_id=user_id)
        user = self.db.get_user(user_id)
        # ...
```

### 4. Test with Dependency Injection

Always use DI in tests:

```python
def test_user_service():
    mock_db = MockDatabase()
    service = UserService(mock_db)  # Easy to inject mock

    service.process_user(42)

    assert mock_db.get_user.called_with(42)
```

## Migration Guide

### From Service Locator to DI

If you have existing code using Service Locator and want to migrate:

**Before:**
```python
class UserService:
    def process(self):
        hub = get_hub()
        db = hub.get_component("database")
        logger = hub.get_foundation_logger()
        # ... use db and logger
```

**After:**
```python
@injectable
class UserService:
    def __init__(self, db: Database, logger: Logger):
        self.db = db
        self.logger = logger

    def process(self):
        # ... use self.db and self.logger
```

**Update main.py:**
```python
def main():
    container = Container()
    container.register(Database, Database.from_env())
    container.register(Logger, Logger("INFO"))

    service = container.resolve(UserService)
    service.process()
```

## Common Criticisms and Responses

### "Why not pure Dependency Injection everywhere?"

**The Pure DI Argument:**
"Global state is harmful. Everything should be explicitly injected for testability and clarity."

**Our Response:**
Pure DI is architecturally clean but pragmatically impractical for framework infrastructure. Consider what happens if we inject logger everywhere:

```python
# Pure DI - Theoretically clean, practically painful
class UserRepository:
    def __init__(self, db: Database, logger: Logger):
        self.db = db
        self.logger = logger

class EmailService:
    def __init__(self, smtp: SMTPClient, logger: Logger):
        self.smtp = smtp
        self.logger = logger

class NotificationService:
    def __init__(self, email: EmailService, logger: Logger):
        self.email = email
        self.logger = logger  # Passed down from above

class UserService:
    def __init__(self, repo: UserRepository, notif: NotificationService, logger: Logger):
        self.repo = repo
        self.notif = notif
        self.logger = logger  # Passed down from above

# In Composition Root - Every class needs logger!
def main():
    logger = Logger("INFO")
    db = Database(...)
    repo = UserRepository(db, logger)
    smtp = SMTPClient(...)
    email = EmailService(smtp, logger)
    notif = NotificationService(email, logger)
    service = UserService(repo, notif, logger)
```

**Problems with this approach:**
- Logger pollutes every constructor signature
- Logger is passed down through layers that don't use it
- No testability benefit (logging isn't what you're testing)
- Massive boilerplate for a cross-cutting concern

**Our pragmatic solution:**
```python
from provide.foundation import logger  # Global logger for cross-cutting concern

@injectable
class UserService:
    def __init__(self, repo: UserRepository, notif: NotificationService):
        # Only inject what matters to business logic
        self.repo = repo
        self.notif = notif

    def process_user(self, user_id: int):
        # Use global logger for cross-cutting concern
        logger.info("Processing user", user_id=user_id)
        user = self.repo.find(user_id)
        self.notif.send(user)
```

### "Global state makes testing impossible"

**The Criticism:**
"Global singletons can't be isolated in tests."

**Our Response:**
Foundation provides comprehensive testing infrastructure that properly isolates global state:

```python
from provide.foundation.testmode import reset_foundation_for_testing, test_scope

@pytest.fixture(autouse=True)
def reset_foundation():
    """Automatic reset before each test."""
    reset_foundation_for_testing()

def test_with_isolated_hub():
    """Tests can use isolated Hub instances."""
    with test_scope() as hub:
        # This hub is isolated from global state
        hub.register(Database, mock_db)
        service = hub.resolve(MyService)
        # Test with mock dependencies
```

The global state is **managed**, not **unmanaged**. This is a critical distinction.

### "This violates the Dependency Inversion Principle"

**The Criticism:**
"High-level modules should not depend on low-level modules (like a global logger)."

**Our Response:**
The Dependency Inversion Principle applies to **business logic dependencies**, not to **infrastructure**. Logging is infrastructure, not a business dependency.

Consider:
- **Business dependency**: "This UserService depends on a UserRepository" - Should use DI
- **Infrastructure concern**: "This code needs to log events" - Can use global logger

The distinction is important. Your business logic doesn't *depend on logging* - it would work fine without it. Logging is an optional, cross-cutting concern that observes your code but doesn't affect its behavior.

### "The Bootstrapping Problem is solvable with pure DI"

**The Criticism:**
"Just instantiate everything manually in main() without any global access."

**Our Response:**
This works for toy examples but fails in real systems where:

1. **The framework itself needs initialization** before your code runs
   ```python
   # How do you initialize Foundation without get_hub()?
   # The logger, config, and error handling must exist FIRST
   from provide.foundation.hub import get_hub

   def main():
       hub = get_hub()  # This initializes the Foundation system
       hub.initialize_foundation()  # Sets up logging, config, events

       # NOW your application can use DI
       container = Container()
       # ...
   ```

2. **Plugin systems need a well-known registration point**
   ```python
   # Plugins can't know about your Container instance
   # They need a global registry
   from provide.foundation.hub import get_hub

   class MyPlugin:
       def register(self):
           hub = get_hub()
           hub.add_command(my_command, "my-cmd")
   ```

3. **Third-party libraries dictate callback signatures**
   ```python
   import third_party_lib

   def my_callback(event_data: dict):
       # Signature is controlled by third_party_lib
       # Can't add DI parameters
       # Service Locator provides access to your app's services
       from provide.foundation.hub import get_hub
       db = get_hub().get_component("database")
       db.save(event_data)

   third_party_lib.register_callback(my_callback)
   ```

## Pattern Decision Tree

Use this decision tree to choose the right pattern:

```
Need to use a component?
│
├─ Is it framework infrastructure (logging, config, Hub)?
│  └─ ✅ Use Service Locator: get_hub(), logger
│
├─ Is it a cross-cutting concern (logging, metrics)?
│  └─ ✅ Use Service Locator: logger
│
├─ Is it a callback/middleware where you don't control the signature?
│  └─ ✅ Use Service Locator: get_hub()
│
├─ Is it business logic (services, repositories, use cases)?
│  └─ ✅ Use Dependency Injection: @injectable, Container
│
└─ Do you need to test it in isolation with mocks?
   └─ ✅ Use Dependency Injection: @injectable, Container
```

## Mixed Pattern Example (Best Practice)

Here's a realistic example showing appropriate use of both patterns:

```python
from provide.foundation import logger  # Global logger - OK for cross-cutting concern
from provide.foundation.hub import Container, injectable

# Infrastructure
@injectable
class DatabaseClient:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        logger.debug("Database initialized", connection=connection_string)

    def query(self, sql: str) -> list[dict]:
        logger.debug("Executing query", sql=sql)
        # ... query implementation

# Business Logic - Uses DI for business dependencies, SL for logging
@injectable
class UserRepository:
    def __init__(self, db: DatabaseClient):
        # Inject business dependency
        self.db = db

    def find_user(self, user_id: int) -> User:
        # Use global logger for cross-cutting concern
        logger.info("Finding user", user_id=user_id)
        rows = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
        if not rows:
            logger.warning("User not found", user_id=user_id)
            return None
        return User.from_dict(rows[0])

@injectable
class NotificationService:
    def __init__(self, email_client: EmailClient):
        self.email_client = email_client

    def notify_user(self, user: User, message: str):
        logger.info("Sending notification", user_id=user.id, message_preview=message[:50])
        self.email_client.send(user.email, message)
        logger.debug("Notification sent", user_id=user.id)

@injectable
class UserService:
    def __init__(self, repository: UserRepository, notifications: NotificationService):
        # Only inject business dependencies
        self.repository = repository
        self.notifications = notifications

    def activate_user(self, user_id: int):
        logger.info("Activating user", user_id=user_id)

        user = self.repository.find_user(user_id)
        if not user:
            logger.error("Cannot activate non-existent user", user_id=user_id)
            raise ValueError(f"User {user_id} not found")

        user.active = True
        self.repository.save(user)
        self.notifications.notify_user(user, "Your account has been activated!")

        logger.info("User activated successfully", user_id=user_id)

# Composition Root
def main():
    # Use Service Locator for framework initialization
    from provide.foundation.hub import get_hub
    hub = get_hub()
    hub.initialize_foundation()

    # Use DI for application wiring
    container = Container()
    container.register(DatabaseClient, DatabaseClient("postgresql://localhost/app"))
    container.register(EmailClient, EmailClient("smtp.example.com"))

    repository = container.resolve(UserRepository)
    container.register(UserRepository, repository)

    notifications = container.resolve(NotificationService)
    container.register(NotificationService, notifications)

    service = container.resolve(UserService)

    # Run application
    service.activate_user(42)

if __name__ == "__main__":
    main()
```

**What makes this a good pattern:**
- ✅ Business dependencies (`DatabaseClient`, `UserRepository`) use DI - explicit and testable
- ✅ Cross-cutting concerns (`logger`) use Service Locator - convenient and non-intrusive
- ✅ Framework initialization (`get_hub()`) uses Service Locator - solves bootstrapping
- ✅ Clear separation between business logic and infrastructure
- ✅ Easy to test: inject mocks for business dependencies, global logger doesn't interfere

## Summary

Provide Foundation's hybrid approach gives you **flexibility**:

- Use **Service Locator** for framework infrastructure (logger, config, events)
- Use **Dependency Injection** for application logic (services, repositories, use cases)
- Mix patterns in the same codebase
- Adopt the polyglot mental model for consistency across languages

This approach balances **convenience** (Service Locator) with **explicitness** (Dependency Injection), giving you the best tool for each job.

**The hybrid pattern is not a compromise** - it's a deliberate architectural decision that recognizes:
1. Framework infrastructure has different needs than application logic
2. Not all dependencies are equal (business vs infrastructure)
3. Pragmatism beats dogma when both approaches are well-implemented

For complete examples, see:
- `examples/di/01_polyglot_di_pattern.py` (Python)
- `examples/di/01_polyglot_di_pattern.go` (Go)
- `examples/di/01_polyglot_di_pattern.rs` (Rust)
