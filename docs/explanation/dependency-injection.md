# Explanation: The Polyglot Dependency Injection Pattern

A core architectural philosophy of `provide.foundation` is to promote a dependency injection (DI) pattern that is consistent and idiomatic across multiple programming languages, specifically Python, Go, and Rust. We call this the **"golden cage"**: a well-defined, portable pattern for building testable and maintainable applications.

## The Core Pattern

The pattern is simple and consists of two main parts:

1.  **Explicit Constructor Injection:** Components declare their dependencies as arguments to their constructor (`__init__` in Python, `New...` functions in Go/Rust). There is no "magic"; dependencies are always visible in the constructor signature.

2.  **Composition Root:** A single location in the application (typically the `main()` function or an application factory) is responsible for creating all components and "wiring" them together by passing instances into constructors.

## Why This Pattern?

This approach provides the primary benefits of DI—decoupling and testability—without the complexity of a full-blown DI framework that relies on auto-wiring or reflection "magic." It keeps the flow of control simple and explicit.

## The Polyglot Advantage

By adhering to this pattern, a developer who understands how to build a service with `provide.foundation` in Python can immediately understand the architecture of a similar service written in Go or Rust.

### Python Example (`@injectable` and `Container`)

`provide.foundation` provides the `@injectable` decorator and a `Container` class as helpers to make this pattern more convenient in Python.

*From `examples/di/01_polyglot_di_pattern.py`:*
```python
@injectable
class UserRepository:
    def __init__(self, db: Database, logger: Logger):
        self.db = db
        self.logger = logger

def main():
    # Composition Root
    container = Container()
    container.register(Database, Database("..."))
    container.register(Logger, Logger("INFO"))

    # The container helps wire the dependencies
    user_repo = container.resolve(UserRepository)
```

### Go Example (Manual Wiring)

Go does not have a DI container, but the pattern is identical—you just wire it manually.

*From `examples/di/01_polyglot_di_pattern.go`:*
```go
type UserRepository struct {
  db     *Database
  logger *Logger
}

func NewUserRepository(db *Database, logger *Logger) *UserRepository {
  return &UserRepository{db: db, logger: logger}
}

func main() {
    // Composition Root
    database := NewDatabase("...")
    logger := NewLogger("INFO")

    // Manual wiring
    userRepo := NewUserRepository(database, logger)
}
```

### Rust Example (Manual Wiring)

Similarly, in Rust, the structure remains the same.

*From `examples/di/01_polyglot_di_pattern.rs`:*
```rust
struct UserRepository<'a> {
    db: &'a Database,
    logger: &'a Logger,
}

impl<'a> UserRepository<'a> {
    fn new(db: &'a Database, logger: &'a Logger) -> Self {
        Self { db, logger }
    }
}

fn main() {
    // Composition Root
    let database = Database::new("...".to_string());
    let logger = Logger::new("INFO".to_string());

    // Manual wiring
    let user_repo = UserRepository::new(&database, &logger);
}
```

The mental model is the same across all three, which is a powerful advantage for polyglot teams.
