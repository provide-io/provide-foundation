# Explanation: The Polyglot Dependency Injection Pattern

A core architectural philosophy of `provide.foundation` is to promote a dependency injection (DI) pattern that is consistent and idiomatic across multiple programming languages, specifically Python, Go, and Rust.

## The Core Pattern

1.  **Explicit Constructor Injection:** Components declare their dependencies as arguments to their constructor (`__init__` in Python, `New...` functions in Go/Rust).
2.  **Composition Root:** A single location in the application (typically `main()`) is responsible for creating all components and "wiring" them together.

## The Polyglot Advantage

By adhering to this pattern, a developer can immediately understand the architecture of a similar service written in Go or Rust.

### Python Example (`@injectable` and `Container`)

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
    user_repo = container.resolve(UserRepository)
```

### Go Example (Manual Wiring)

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
    userRepo := NewUserRepository(database, logger)
}
```
The mental model is the same across all languages, which is a powerful advantage for polyglot teams.
