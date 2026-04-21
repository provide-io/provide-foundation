# Unit Testing

Learn how to write comprehensive unit tests for Foundation applications using provide-testkit.

## Overview

Foundation provides `provide-testkit`, a comprehensive testing toolkit that ensures clean state between tests, proper resource cleanup, and easy log capture. It integrates seamlessly with pytest for a powerful testing experience.

**Key features:**
- **State reset** - Clean Foundation state for each test
- **Log capture** - Capture and verify log output
- **FoundationTestCase** - Base test class with setup/teardown
- **Async support** - Test async code easily
- **Fixture support** - Pytest fixtures for common patterns

## Prerequisites

Install testing dependencies:
```bash
uv add provide-testkit
uv add pytest
uv add pytest-asyncio
```

## Basic Test Setup

### Minimal Test

```python
import pytest
from provide.testkit import reset_foundation_setup_for_testing

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state before each test."""
    reset_foundation_setup_for_testing()

def test_simple_operation():
    """Test basic operation."""
    result = 2 + 2
    assert result == 4
```

### Testing with Logging

```python
from provide.foundation import logger

def test_logging():
    """Test logging works correctly."""
    reset_foundation_setup_for_testing()

    logger.info("test_event", value=123)
    # Logger is initialized and working
```

## Using FoundationTestCase

The base test class provides setup/teardown and utilities:

```python
from provide.testkit import FoundationTestCase

class TestMyFeature(FoundationTestCase):
    """Test suite for my feature."""

    def setup_method(self):
        """Set up test environment."""
        super().setup_method()  # IMPORTANT: Call parent
        self.test_data = {"key": "value"}
        self.counter = 0

    def test_basic_functionality(self):
        """Test basic feature."""
        assert self.test_data["key"] == "value"
        self.counter += 1
        assert self.counter == 1

    def test_another_feature(self):
        """Test another aspect."""
        # counter is 0 here - fresh setup for each test
        assert self.counter == 0

    def teardown_method(self):
        """Clean up after test."""
        # Cleanup code here
        super().teardown_method()  # IMPORTANT: Call parent
```

## Capturing Logs

### Basic Log Capture

```python
from provide.testkit import set_log_stream_for_testing
from io import StringIO

def test_log_output():
    """Test log output content."""
    reset_foundation_setup_for_testing()

    stream = StringIO()
    set_log_stream_for_testing(stream)

    from provide.foundation import logger
    logger.info("test_message", value=42)

    output = stream.getvalue()
    assert "test_message" in output
    assert "42" in output
```

### Structured Log Verification

```python
import json

def test_structured_logging():
    """Test structured log fields."""
    reset_foundation_setup_for_testing()

    stream = StringIO()
    set_log_stream_for_testing(stream)

    from provide.foundation import logger
    logger.info("user_login", user_id="user_123", success=True)

    # Parse JSON log output
    output = stream.getvalue()
    for line in output.strip().split("\n"):
        if "user_login" in line:
            log_entry = json.loads(line)
            assert log_entry["event"] == "user_login"
            assert log_entry["user_id"] == "user_123"
            assert log_entry["success"] is True
```

### Log Level Testing

```python
def test_log_levels():
    """Test different log levels."""
    reset_foundation_setup_for_testing()

    stream = StringIO()
    set_log_stream_for_testing(stream)

    from provide.foundation import logger
    logger.debug("debug_message")
    logger.info("info_message")
    logger.warning("warning_message")
    logger.error("error_message")

    output = stream.getvalue()
    assert "debug_message" in output
    assert "info_message" in output
    assert "warning_message" in output
    assert "error_message" in output
```

## Mocking and Patching

### Mock External Dependencies

```python
from unittest.mock import Mock, patch

def test_with_mock_database():
    """Test with mocked database."""
    reset_foundation_setup_for_testing()

    # Create mock
    mock_db = Mock()
    mock_db.query.return_value = [{"id": 1, "name": "Alice"}]

    # Inject mock
    service = UserService(database=mock_db)

    # Test
    users = service.get_all_users()
    assert len(users) == 1
    assert users[0]["name"] == "Alice"

    # Verify mock was called
    mock_db.query.assert_called_once_with("SELECT * FROM users")
```

### Patch Functions

```python
@patch('myapp.api.client.get_users')
def test_api_call(mock_get_users):
    """Test with patched API call."""
    reset_foundation_setup_for_testing()

    # Setup mock response
    mock_get_users.return_value = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]

    # Test
    from myapp.service import UserService
    service = UserService()
    users = service.fetch_users()

    assert len(users) == 2
    assert users[0]["name"] == "Alice"
```

### Context Manager Mocking

```python
from unittest.mock import MagicMock

def test_file_operations():
    """Test file operations with mock."""
    reset_foundation_setup_for_testing()

    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = "test content"

    with patch('builtins.open', return_value=mock_file):
        content = read_config_file("config.txt")
        assert content == "test content"
```

## Testing Async Code

### Basic Async Test

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    reset_foundation_setup_for_testing()

    result = await async_operation()
    assert result == "success"
```

### Async with Mocks

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_api_call():
    """Test async API call."""
    reset_foundation_setup_for_testing()

    mock_client = AsyncMock()
    mock_client.get.return_value = {"status": "ok"}

    service = APIService(client=mock_client)
    result = await service.fetch_data()

    assert result["status"] == "ok"
    mock_client.get.assert_awaited_once()
```

## Parameterized Tests

### Basic Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input, expected):
    """Test square function with multiple inputs."""
    result = square(input)
    assert result == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("username,password,should_succeed", [
    ("alice", "correct_password", True),
    ("alice", "wrong_password", False),
    ("bob", "correct_password", True),
    ("invalid_user", "any_password", False),
])
def test_authentication(username, password, should_succeed):
    """Test authentication with various credentials."""
    reset_foundation_setup_for_testing()

    result = authenticate(username, password)
    assert result == should_succeed
```

### Parameterized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database(request):
    """Provide different database backends."""
    db = Database(backend=request.param)
    db.connect()
    yield db
    db.disconnect()

def test_database_operations(database):
    """Test operations work on all database backends."""
    database.execute("CREATE TABLE test (id INT)")
    database.execute("INSERT INTO test VALUES (1)")
    result = database.query("SELECT * FROM test")
    assert len(result) == 1
```

## Pytest Fixtures

### Shared Fixtures

```python
@pytest.fixture
def sample_user():
    """Provide sample user for tests."""
    return {
        "id": "user_123",
        "name": "Alice",
        "email": "alice@example.com"
    }

@pytest.fixture
def user_repository():
    """Provide user repository."""
    reset_foundation_setup_for_testing()
    from myapp.repositories import UserRepository
    return UserRepository(database=":memory:")

def test_create_user(user_repository, sample_user):
    """Test user creation."""
    user_repository.create(sample_user)
    retrieved = user_repository.get(sample_user["id"])
    assert retrieved["name"] == "Alice"
```

### Fixture Scope

```python
@pytest.fixture(scope="module")
def database_connection():
    """Single database connection for all tests in module."""
    db = Database(":memory:")
    db.connect()
    db.initialize_schema()
    yield db
    db.disconnect()

@pytest.fixture(scope="function")
def clean_database(database_connection):
    """Clean database before each test."""
    database_connection.execute("DELETE FROM users")
    return database_connection
```

### Fixture Factories

```python
@pytest.fixture
def user_factory():
    """Factory for creating test users."""
    def _create_user(name="TestUser", email=None):
        return {
            "id": f"user_{name.lower()}",
            "name": name,
            "email": email or f"{name.lower()}@test.com"
        }
    return _create_user

def test_multiple_users(user_factory):
    """Test with multiple users."""
    alice = user_factory(name="Alice")
    bob = user_factory(name="Bob")

    assert alice["name"] == "Alice"
    assert bob["email"] == "bob@test.com"
```

## Testing Exceptions

### Basic Exception Testing

```python
def test_raises_exception():
    """Test function raises expected exception."""
    with pytest.raises(ValueError):
        validate_email("invalid-email")

def test_exception_message():
    """Test exception message."""
    with pytest.raises(ValueError, match="Invalid email format"):
        validate_email("invalid-email")
```

### Exception Context

```python
def test_exception_details():
    """Test exception with detailed verification."""
    with pytest.raises(DatabaseError) as exc_info:
        connect_to_database("invalid://url")

    assert "connection failed" in str(exc_info.value)
    assert exc_info.value.error_code == "DB001"
```

## Test Organization

### Class-Based Organization

```python
class TestUserService(FoundationTestCase):
    """Test suite for UserService."""

    def setup_method(self):
        """Set up test dependencies."""
        super().setup_method()
        self.mock_repo = Mock()
        self.service = UserService(repository=self.mock_repo)

    def test_get_user(self):
        """Test getting user by ID."""
        self.mock_repo.get.return_value = {"id": "123", "name": "Alice"}

        user = self.service.get_user("123")
        assert user["name"] == "Alice"

    def test_create_user(self):
        """Test user creation."""
        user_data = {"name": "Bob", "email": "bob@example.com"}

        self.service.create_user(user_data)
        self.mock_repo.save.assert_called_once()

    def teardown_method(self):
        """Clean up."""
        super().teardown_method()
```

### Module-Level Organization

```python
# test_authentication.py

def test_login_success():
    """Test successful login."""
    pass

def test_login_failure():
    """Test failed login."""
    pass

def test_logout():
    """Test logout."""
    pass

# test_authorization.py

def test_has_permission():
    """Test permission check."""
    pass

def test_lacks_permission():
    """Test denied permission."""
    pass
```

## Testing Best Practices

### ✅ DO: Reset State Between Tests

```python
# ✅ Good: Clean state for each test
@pytest.fixture(autouse=True)
def reset_foundation():
    reset_foundation_setup_for_testing()

def test_operation_a():
    # Clean state
    pass

def test_operation_b():
    # Clean state, not affected by test_operation_a
    pass
```

### ✅ DO: Use Descriptive Test Names

```python
# ✅ Good: Clear test names
def test_user_login_with_valid_credentials_succeeds():
    pass

def test_user_login_with_invalid_password_fails():
    pass

# ❌ Bad: Unclear names
def test_login():
    pass

def test_login2():
    pass
```

### ✅ DO: Test One Thing Per Test

```python
# ✅ Good: Focused tests
def test_user_creation():
    user = create_user("Alice")
    assert user.name == "Alice"

def test_user_email_validation():
    with pytest.raises(ValueError):
        create_user("Alice", email="invalid")

# ❌ Bad: Testing multiple things
def test_user_everything():
    user = create_user("Alice")
    assert user.name == "Alice"
    with pytest.raises(ValueError):
        create_user("Bob", email="invalid")
    # Too much in one test
```

### ✅ DO: Use Fixtures for Setup

```python
# ✅ Good: Reusable fixtures
@pytest.fixture
def authenticated_user():
    return authenticate("alice", "password")

def test_api_call(authenticated_user):
    response = api.call(authenticated_user)
    assert response.status == 200

# ❌ Bad: Setup in each test
def test_api_call():
    user = authenticate("alice", "password")  # Repeated
    response = api.call(user)
    assert response.status == 200
```

### ❌ DON'T: Test Implementation Details

```python
# ❌ Bad: Testing internal implementation
def test_internal_cache():
    service = UserService()
    service.get_user("123")
    assert service._cache["123"] is not None  # Internal detail

# ✅ Good: Test behavior
def test_user_retrieval():
    service = UserService()
    user = service.get_user("123")
    assert user["id"] == "123"
```

### ❌ DON'T: Share State Between Tests

```python
# ❌ Bad: Shared mutable state
SHARED_DATA = []

def test_append():
    SHARED_DATA.append(1)
    assert len(SHARED_DATA) == 1  # Fails if test runs twice

# ✅ Good: Isolated state
def test_append():
    data = []
    data.append(1)
    assert len(data) == 1
```

## Coverage

### Running with Coverage

```bash
# Run tests with coverage
pytest --cov=myapp --cov-report=html

# Run with coverage threshold
pytest --cov=myapp --cov-fail-under=80
```

### Coverage Configuration

```ini
# pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

### Testing Untested Code

```python
def test_previously_untested_function():
    """Add test for uncovered function."""
    result = previously_untested_function(input_data)
    assert result == expected_output
```

## Common Patterns

### Testing Database Operations

```python
@pytest.fixture
def test_database():
    """Provide test database."""
    db = Database(":memory:")
    db.execute("CREATE TABLE users (id INT, name TEXT)")
    yield db
    db.close()

def test_save_user(test_database):
    """Test saving user to database."""
    test_database.execute("INSERT INTO users VALUES (1, 'Alice')")
    result = test_database.query("SELECT * FROM users WHERE id = 1")
    assert result[0]["name"] == "Alice"
```

### Testing HTTP Clients

```python
from unittest.mock import Mock

def test_http_get():
    """Test HTTP GET request."""
    mock_client = Mock()
    mock_client.get.return_value = Mock(
        status_code=200,
        json=lambda: {"data": "test"}
    )

    service = APIService(client=mock_client)
    response = service.fetch_data()

    assert response["data"] == "test"
    mock_client.get.assert_called_once_with("/api/data")
```

### Testing Time-Dependent Code

```python
from unittest.mock import patch
from datetime import datetime

@patch('myapp.utils.datetime')
def test_time_dependent(mock_datetime):
    """Test code that depends on current time."""
    # Fix time to specific value
    mock_datetime.now.return_value = datetime(2025, 10, 24, 10, 0, 0)

    result = get_greeting()
    assert result == "Good morning"  # Predictable result
```

## Next Steps

### Related Guides
- **[Testing CLI Commands](cli-tests.md)**: Test CLI applications
- **[Basic Logging](../logging/basic-logging.md)**: Understand logging for tests
- **[Dependency Injection](../../explanation/dependency-injection.md)**: DI makes testing easier

### Examples
- See `tests/` directory in the repository for comprehensive test examples
- See `examples/testing/` for testing patterns

---

**Tip**: Always reset Foundation state with `reset_foundation_setup_for_testing()` before each test. Use `FoundationTestCase` as your base class for automatic setup/teardown.
