# The Polyglot Dependency Injection Pattern

A core architectural philosophy of `provide.foundation` is to promote a dependency injection (DI) pattern that is consistent and idiomatic across multiple programming languages, specifically Python, Go, and Rust.

## Overview

Dependency Injection is a design pattern where objects receive their dependencies from external sources rather than creating them internally. Foundation embraces a **constructor injection** pattern that works identically across Python, Go, and Rust, making it easier for polyglot teams to maintain consistent architecture.

**Key benefits:**
- **Testability** - Easy to mock dependencies in tests
- **Flexibility** - Swap implementations without changing code
- **Clarity** - Dependencies are explicit and visible
- **Polyglot consistency** - Same pattern across languages
- **No magic** - Explicit wiring, no runtime reflection

## The Core Pattern

The polyglot DI pattern consists of two key principles:

### 1. Explicit Constructor Injection

Components declare their dependencies as constructor arguments:

**Python:**
```python
class UserService:
    def __init__(self, user_repo: UserRepository, logger: Logger):
        self.user_repo = user_repo
        self.logger = logger
```

**Go:**
```go
type UserService struct {
    userRepo *UserRepository
    logger   *Logger
}

func NewUserService(userRepo *UserRepository, logger *Logger) *UserService {
    return &UserService{userRepo: userRepo, logger: logger}
}
```

**Rust:**
```rust
struct UserService {
    user_repo: UserRepository,
    logger: Logger,
}

impl UserService {
    fn new(user_repo: UserRepository, logger: Logger) -> Self {
        Self { user_repo, logger }
    }
}
```

### 2. Composition Root

A single location (typically `main()`) creates and wires all components:

```python
def main():
    """Composition root - wire dependencies here."""
    # Create foundation components
    logger = get_logger()

    # Create infrastructure
    db = Database(connection_string)
    cache = RedisCache(redis_url)

    # Create repositories
    user_repo = UserRepository(db, logger)

    # Create services
    user_service = UserService(user_repo, logger, cache)

    # Create application
    app = Application(user_service, logger)
    app.run()
```

## The Polyglot Advantage

By adhering to this pattern, developers can immediately understand the architecture of a service regardless of implementation language.

### Python Example with Foundation Hub

Foundation provides the Hub for dependency injection and component management:

```python
from provide.foundation import get_hub, logger
from provide.foundation.hub import injectable

# Mark classes as injectable for automatic dependency resolution
@injectable
class Database:
    """Database connection."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._conn = None

    def connect(self):
        """Establish database connection."""
        self._conn = create_connection(self.connection_string)
        logger.info("database_connected")

@injectable
class UserRepository:
    """User data repository."""

    def __init__(self, db: Database):
        self.db = db

    def get_user(self, user_id: str):
        """Get user by ID."""
        return self.db.query("SELECT * FROM users WHERE id = ?", user_id)

@injectable
class UserService:
    """User business logic."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, user_id: str, password: str):
        """Authenticate user."""
        user = self.user_repo.get_user(user_id)
        return verify_password(user, password)

# Composition root
def main():
    hub = get_hub()
    hub.initialize_foundation()

    # Register infrastructure dependencies
    db = Database("postgresql://localhost/mydb")
    hub.register(Database, db)

    # Resolve service with automatic dependency injection
    user_service = hub.resolve(UserService)

    # Use service
    user_service.authenticate("user123", "password")
```

### Go Example (Manual Wiring)

The same pattern in Go, manually wired:

```go
type Database struct {
    connString string
    conn       *sql.DB
}

func NewDatabase(connString string) *Database {
    return &Database{connString: connString}
}

func (d *Database) Connect() error {
    conn, err := sql.Open("postgres", d.connString)
    if err != nil {
        return err
    }
    d.conn = conn
    log.Println("database_connected")
    return nil
}

type UserRepository struct {
    db *Database
}

func NewUserRepository(db *Database) *UserRepository {
    return &UserRepository{db: db}
}

func (r *UserRepository) GetUser(userID string) (*User, error) {
    var user User
    err := r.db.conn.QueryRow("SELECT * FROM users WHERE id = $1", userID).Scan(&user)
    return &user, err
}

type UserService struct {
    userRepo *UserRepository
}

func NewUserService(userRepo *UserRepository) *UserService {
    return &UserService{userRepo: userRepo}
}

func (s *UserService) Authenticate(userID, password string) (bool, error) {
    user, err := s.userRepo.GetUser(userID)
    if err != nil {
        return false, err
    }
    return verifyPassword(user, password), nil
}

// Composition root
func main() {
    // Create infrastructure
    db := NewDatabase("postgresql://localhost/mydb")
    if err := db.Connect(); err != nil {
        log.Fatal(err)
    }

    // Create repositories
    userRepo := NewUserRepository(db)

    // Create services
    userService := NewUserService(userRepo)

    // Use service
    authenticated, _ := userService.Authenticate("user123", "password")
}
```

The mental model is **identical** across both languages, which is a powerful advantage for polyglot teams.

## Python Implementation Patterns

### Constructor Injection

Declare dependencies in `__init__`:

```python
class EmailService:
    """Send emails via SMTP."""

    def __init__(self, smtp_client: SMTPClient, template_engine: TemplateEngine):
        self.smtp = smtp_client
        self.templates = template_engine

    def send_welcome_email(self, user: User):
        """Send welcome email to new user."""
        template = self.templates.render("welcome.html", user=user)
        self.smtp.send(user.email, "Welcome!", template)
```

### Property Injection (Avoid)

While Python supports property injection, **avoid it** for the polyglot pattern:

```python
# ❌ Bad: Property injection (doesn't translate to Go/Rust)
class BadService:
    smtp: SMTPClient  # Set after construction

    def send_email(self):
        self.smtp.send(...)  # Could be None!

# ✅ Good: Constructor injection
class GoodService:
    def __init__(self, smtp: SMTPClient):
        self.smtp = smtp  # Guaranteed to exist
```

### Interface-Based Dependencies

Use abstract base classes for flexibility:

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    """Abstract user repository."""

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        """Get user by ID."""
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        """Save user."""
        pass

class PostgresUserRepository(UserRepository):
    """PostgreSQL implementation."""

    def __init__(self, db: Database):
        self.db = db

    def get_user(self, user_id: str) -> User:
        return self.db.query_one("SELECT * FROM users WHERE id = ?", user_id)

    def save_user(self, user: User) -> None:
        self.db.execute("INSERT INTO users VALUES (?, ?)", user.id, user.name)

class InMemoryUserRepository(UserRepository):
    """In-memory implementation for testing."""

    def __init__(self):
        self.users = {}

    def get_user(self, user_id: str) -> User:
        return self.users.get(user_id)

    def save_user(self, user: User) -> None:
        self.users[user.id] = user

# Service depends on interface, not implementation
class UserService:
    def __init__(self, user_repo: UserRepository):  # Abstract type
        self.user_repo = user_repo
```

## Composition Root Patterns

### Simple Main Function

For CLI applications:

```python
def main():
    """Application entry point and composition root."""
    # Initialize Foundation
    hub = get_hub()
    hub.initialize_foundation()

    # Configuration
    config = load_config()

    # Infrastructure
    db = Database(config.database_url)
    cache = RedisCache(config.redis_url)

    # Repositories
    user_repo = PostgresUserRepository(db)
    session_repo = CacheSessionRepository(cache)

    # Services
    auth_service = AuthService(user_repo, session_repo)
    email_service = EmailService(SMTPClient(config.smtp), TemplateEngine())

    # Application
    cli = CLI(auth_service, email_service)
    cli.run()

if __name__ == "__main__":
    main()
```

### Factory Pattern

For complex construction:

```python
class ServiceFactory:
    """Factory for creating services with dependencies."""

    def __init__(self, config: Config):
        self.config = config
        self._db = None
        self._cache = None

    @property
    def database(self) -> Database:
        """Lazy database singleton."""
        if not self._db:
            self._db = Database(self.config.database_url)
            self._db.connect()
        return self._db

    @property
    def cache(self) -> Cache:
        """Lazy cache singleton."""
        if not self._cache:
            self._cache = RedisCache(self.config.redis_url)
        return self._cache

    def create_user_service(self) -> UserService:
        """Create user service with dependencies."""
        user_repo = PostgresUserRepository(self.database)
        return UserService(user_repo, self.cache)

    def create_email_service(self) -> EmailService:
        """Create email service with dependencies."""
        smtp = SMTPClient(self.config.smtp)
        templates = TemplateEngine()
        return EmailService(smtp, templates)

# Usage
def main():
    config = load_config()
    factory = ServiceFactory(config)

    user_service = factory.create_user_service()
    email_service = factory.create_email_service()

    app = Application(user_service, email_service)
    app.run()
```

### Hub-Based Composition

Using Foundation's Hub for automatic dependency resolution:

```python
from provide.foundation import get_hub
from provide.foundation.hub import injectable

# Mark components as injectable
@injectable
class Database:
    def __init__(self, url: str):
        self.url = url

@injectable
class UserRepository:
    def __init__(self, db: Database):  # Auto-resolved
        self.db = db

@injectable
class UserService:
    def __init__(self, repo: UserRepository):  # Auto-resolved
        self.repo = repo

# Composition root
def main():
    hub = get_hub()
    hub.initialize_foundation()

    # Register infrastructure dependencies by type
    db = Database("postgresql://localhost/db")
    hub.register(Database, db)

    # Resolve service (dependencies auto-injected via type hints)
    user_service = hub.resolve(UserService)
```

## Testing with Dependency Injection

DI makes testing trivial by allowing mock injection:

### Unit Testing with Mocks

```python
import pytest
from unittest.mock import Mock

def test_user_service_authentication():
    """Test user authentication with mocked repository."""
    # Create mocks
    mock_repo = Mock(spec=UserRepository)
    mock_repo.get_user.return_value = User(id="123", password_hash="hashed")

    mock_cache = Mock(spec=Cache)

    # Inject mocks
    service = UserService(mock_repo, mock_cache)

    # Test
    result = service.authenticate("123", "password")

    # Verify
    assert result is True
    mock_repo.get_user.assert_called_once_with("123")
    mock_cache.set.assert_called()
```

### Integration Testing with Test Implementations

```python
def test_user_service_integration():
    """Integration test with real implementations."""
    # Use in-memory implementations
    user_repo = InMemoryUserRepository()
    cache = InMemoryCache()

    # Create service
    service = UserService(user_repo, cache)

    # Setup test data
    user = User(id="123", name="Alice")
    user_repo.save_user(user)

    # Test
    result = service.get_user("123")
    assert result.name == "Alice"
```

### Test Fixtures

```python
@pytest.fixture
def database():
    """Provide test database."""
    db = Database(":memory:")  # SQLite in-memory
    db.initialize_schema()
    yield db
    db.close()

@pytest.fixture
def user_repository(database):
    """Provide user repository with test database."""
    return PostgresUserRepository(database)

@pytest.fixture
def user_service(user_repository):
    """Provide user service with test dependencies."""
    cache = InMemoryCache()
    return UserService(user_repository, cache)

def test_with_fixtures(user_service):
    """Test using injected fixtures."""
    user = user_service.create_user("Alice", "alice@example.com")
    assert user.name == "Alice"
```

## Common Patterns

### Service Layer Pattern

Organize business logic into services:

```python
# Domain layer
class User:
    """User domain model."""
    pass

# Repository layer
class UserRepository:
    """Data access."""
    def __init__(self, db: Database):
        self.db = db

# Service layer
class UserService:
    """Business logic."""
    def __init__(self, user_repo: UserRepository, email_service: EmailService):
        self.user_repo = user_repo
        self.email_service = email_service

    def register_user(self, email: str, password: str) -> User:
        """Register new user."""
        user = User(email=email, password=hash_password(password))
        self.user_repo.save(user)
        self.email_service.send_welcome(user)
        return user

# Application layer
class Application:
    """Application orchestration."""
    def __init__(self, user_service: UserService):
        self.user_service = user_service
```

### Resource Management

Manage resource lifecycles:

```python
class DatabaseConnection:
    """Managed database connection."""

    def __init__(self, url: str):
        self.url = url
        self._conn = None

    def __enter__(self):
        """Acquire connection."""
        self._conn = connect(self.url)
        return self._conn

    def __exit__(self, *args):
        """Release connection."""
        if self._conn:
            self._conn.close()

class UserService:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_user(self, user_id: str):
        """Get user (connection auto-managed)."""
        with self.db as conn:
            return conn.query("SELECT * FROM users WHERE id = ?", user_id)
```

## Best Practices

### ✅ DO: Declare Dependencies in Constructor

```python
# ✅ Good: Dependencies explicit and required
class Service:
    def __init__(self, repo: Repository, logger: Logger):
        self.repo = repo
        self.logger = logger
```

### ✅ DO: Depend on Abstractions

```python
# ✅ Good: Depend on interface
class Service:
    def __init__(self, repo: UserRepository):  # Abstract base class
        self.repo = repo

# ❌ Bad: Depend on concrete implementation
class Service:
    def __init__(self, repo: PostgresUserRepository):  # Concrete class
        self.repo = repo
```

### ✅ DO: Keep Composition Root Simple

```python
# ✅ Good: Clear, explicit wiring
def main():
    db = Database(url)
    repo = UserRepository(db)
    service = UserService(repo)

# ❌ Bad: Complex logic in composition root
def main():
    if os.getenv("USE_POSTGRES"):
        db = PostgresDatabase(...)
    else:
        db = MySQLDatabase(...)
    # Too much conditional logic
```

### ❌ DON'T: Use Service Locator Pattern

```python
# ❌ Bad: Service locator (hidden dependencies)
class BadService:
    def do_work(self):
        repo = ServiceLocator.get(UserRepository)  # Hidden!
        repo.get_user("123")

# ✅ Good: Explicit injection
class GoodService:
    def __init__(self, repo: UserRepository):  # Visible!
        self.repo = repo

    def do_work(self):
        self.repo.get_user("123")
```

### ❌ DON'T: Create Dependencies Internally

```python
# ❌ Bad: Creates own dependencies
class BadService:
    def __init__(self):
        self.db = Database("hard-coded-url")  # Can't test!

# ✅ Good: Dependencies injected
class GoodService:
    def __init__(self, db: Database):  # Easy to test!
        self.db = db
```

## Comparison with Other Approaches

### vs. Singleton Pattern

```python
# ❌ Singleton: Hidden dependencies, hard to test
class Database:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Database()
        return cls._instance

class Service:
    def do_work(self):
        db = Database.get_instance()  # Hidden dependency

# ✅ DI: Explicit dependencies, easy to test
class Service:
    def __init__(self, db: Database):  # Clear dependency
        self.db = db
```

### vs. Global Variables

```python
# ❌ Global: Implicit coupling, hard to test
DATABASE = Database("url")

class Service:
    def do_work(self):
        DATABASE.query(...)  # Global dependency

# ✅ DI: Explicit injection
class Service:
    def __init__(self, db: Database):
        self.db = db
```

## Next Steps

### Related Guides
- **[Testing](../how-to-guides/testing/unit-tests.md)**: Testing with dependency injection
- **[Architecture](architecture.md)**: Overall Foundation architecture

### Examples
- See `examples/di/01_polyglot_di_pattern.py` for polyglot DI examples
- See `examples/cli/` for CLI applications using DI

---

**Tip**: Start with constructor injection and explicit wiring in your composition root. Use Foundation's Hub for automatic dependency resolution once you're comfortable with the pattern.
