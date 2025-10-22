
class TestAuthenticationError(FoundationTestCase):
    """Test AuthenticationError class."""

    def test_basic_creation(self) -> None:
        """Test basic AuthenticationError."""
        error = AuthenticationError("Invalid credentials")
        assert error.message == "Invalid credentials"
        assert error.code == "AUTH_ERROR"

    def test_with_auth_method(self) -> None:
        """Test with auth_method parameter."""
        error = AuthenticationError("Token invalid", auth_method="jwt")
        assert error.context["auth.method"] == "jwt"

    def test_with_realm(self) -> None:
        """Test with realm parameter."""
        error = AuthenticationError("Access denied", realm="admin")
        assert error.context["auth.realm"] == "admin"


class TestAuthorizationError(FoundationTestCase):
    """Test AuthorizationError class."""

    def test_basic_creation(self) -> None:
        """Test basic AuthorizationError."""
        error = AuthorizationError("Permission denied")
        assert error.message == "Permission denied"
        assert error.code == "AUTHZ_ERROR"

    def test_with_required_permission(self) -> None:
        """Test with required_permission parameter."""
        error = AuthorizationError("Forbidden", required_permission="admin:write")
        assert error.context["authz.permission"] == "admin:write"

    def test_with_resource(self) -> None:
        """Test with resource parameter."""
        error = AuthorizationError("Cannot access", resource="/admin/users")
        assert error.context["authz.resource"] == "/admin/users"

    def test_with_actor(self) -> None:
        """Test with actor parameter."""
        error = AuthorizationError("Denied", actor="user:123")
        assert error.context["authz.actor"] == "user:123"


class TestNotFoundError(FoundationTestCase):
    """Test NotFoundError class."""

    def test_basic_creation(self) -> None:
        """Test basic NotFoundError."""
        error = NotFoundError("Resource not found")
        assert error.message == "Resource not found"
        assert error.code == "NOT_FOUND_ERROR"

    def test_with_resource_type(self) -> None:
        """Test with resource_type parameter."""
        error = NotFoundError("Not found", resource_type="user")
        assert error.context["notfound.type"] == "user"

    def test_with_resource_id(self) -> None:
        """Test with resource_id parameter."""
        error = NotFoundError("Missing", resource_id="usr_123")
        assert error.context["notfound.id"] == "usr_123"


class TestAlreadyExistsError(FoundationTestCase):
    """Test AlreadyExistsError class."""

    def test_basic_creation(self) -> None:
        """Test basic AlreadyExistsError."""
        error = AlreadyExistsError("Already exists")
        assert error.message == "Already exists"
        assert error.code == "ALREADY_EXISTS_ERROR"

    def test_with_resource_type(self) -> None:
        """Test with resource_type parameter."""
        error = AlreadyExistsError("Duplicate", resource_type="email")
        assert error.context["exists.type"] == "email"

    def test_with_resource_id(self) -> None:
        """Test with resource_id parameter."""
        error = AlreadyExistsError("Conflict", resource_id="user@example.com")
        assert error.context["exists.id"] == "user@example.com"

