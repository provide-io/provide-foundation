"""Tests for dependency injection functionality.

Tests the @injectable decorator, Container class, and Hub.resolve() method.
"""

from __future__ import annotations

import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.resources import NotFoundError
from provide.foundation.hub import Container, Hub, injectable, is_injectable
from provide.foundation.testmode import reset_foundation_for_testing


@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state before each test."""
    reset_foundation_for_testing()


# Test Classes for DI


class SimpleService:
    """Service without @injectable decorator."""

    def __init__(self, value: str):
        self.value = value


@injectable
class InjectableService:
    """Service with @injectable decorator."""

    def __init__(self, value: str):
        self.value = value


@injectable
class DatabaseClient:
    """Mock database client."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def query(self, sql: str) -> list[dict[str, object]]:
        return [{"result": "success"}]


@injectable
class Logger:
    """Mock logger."""

    def __init__(self, level: str = "INFO"):
        self.level = level

    def info(self, msg: str) -> None:
        pass


@injectable
class Repository:
    """Repository with dependencies."""

    def __init__(self, db: DatabaseClient, logger: Logger):
        self.db = db
        self.logger = logger


@injectable
class ServiceWithMultipleDeps:
    """Service with multiple dependencies."""

    def __init__(self, repo: Repository, logger: Logger, db: DatabaseClient):
        self.repo = repo
        self.logger = logger
        self.db = db


@injectable
class ServiceNeedingDB:
    """Service needing DatabaseClient for testing missing dependency."""

    def __init__(self, db: DatabaseClient):
        self.db = db


# Tests for @injectable decorator


class TestInjectableDecorator:
    """Tests for the @injectable decorator."""

    def test_injectable_marks_class(self):
        """Test that @injectable marks class correctly."""
        assert is_injectable(InjectableService)
        assert not is_injectable(SimpleService)

    def test_injectable_requires_type_hints(self):
        """Test that @injectable requires type hints on all parameters."""
        with pytest.raises(ValidationError) as exc_info:

            @injectable
            class NoTypeHints:
                def __init__(self, value):  # Missing type hint
                    self.value = value

        assert "untyped parameters" in str(exc_info.value).lower()
        assert "value" in str(exc_info.value)

    def test_injectable_allows_optional_params(self):
        """Test that @injectable allows parameters with defaults."""

        @injectable
        class WithDefaults:
            def __init__(self, value: str = "default"):
                self.value = value

        assert is_injectable(WithDefaults)

    def test_injectable_allows_args_kwargs(self):
        """Test that @injectable allows *args and **kwargs."""

        @injectable
        class WithVarArgs:
            def __init__(self, required: str, *args: int, **kwargs: str):
                self.required = required
                self.args = args
                self.kwargs = kwargs

        assert is_injectable(WithVarArgs)

    def test_injectable_requires_init_method(self):
        """Test that @injectable requires __init__ method."""
        with pytest.raises(ValidationError) as exc_info:

            @injectable
            class NoInit:
                pass

        assert "must define its own __init__ method" in str(exc_info.value).lower()

    def test_injectable_preserves_class_behavior(self):
        """Test that @injectable doesn't modify class behavior."""

        @injectable
        class MyClass:
            def __init__(self, value: str):
                self.value = value

            def get_value(self) -> str:
                return self.value

        instance = MyClass("test")
        assert instance.value == "test"
        assert instance.get_value() == "test"


# Tests for Hub.register() and Hub.resolve()


class TestHubDependencyInjection:
    """Tests for Hub dependency injection methods."""

    def test_register_and_resolve_simple(self):
        """Test registering and resolving a simple dependency."""
        hub = Hub()
        db = DatabaseClient("postgresql://localhost/test")
        hub.register(DatabaseClient, db)

        # Resolve should return the same instance
        resolved = hub._component_registry.get_by_type(DatabaseClient)
        assert resolved is db

    def test_resolve_with_single_dependency(self):
        """Test resolving a class with a single dependency."""
        hub = Hub()
        logger = Logger("DEBUG")
        hub.register(Logger, logger)

        @injectable
        class Service:
            def __init__(self, logger: Logger):
                self.logger = logger

        service = hub.resolve(Service)
        assert service.logger is logger

    def test_resolve_with_multiple_dependencies(self):
        """Test resolving a class with multiple dependencies."""
        hub = Hub()
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")
        hub.register(DatabaseClient, db)
        hub.register(Logger, logger)

        repo = hub.resolve(Repository)
        assert repo.db is db
        assert repo.logger is logger

    def test_resolve_with_nested_dependencies(self):
        """Test resolving a class with nested dependencies."""
        hub = Hub()
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")
        hub.register(DatabaseClient, db)
        hub.register(Logger, logger)

        # Repository depends on db and logger
        repo = hub.resolve(Repository)
        hub.register(Repository, repo)

        # ServiceWithMultipleDeps depends on repo, logger, and db
        service = hub.resolve(ServiceWithMultipleDeps)
        assert service.repo is repo
        assert service.logger is logger
        assert service.db is db

    def test_resolve_with_overrides(self):
        """Test resolving with explicit overrides."""
        hub = Hub()
        db1 = DatabaseClient("postgresql://localhost/db1")
        db2 = DatabaseClient("postgresql://localhost/db2")
        logger = Logger("INFO")
        hub.register(DatabaseClient, db1)
        hub.register(Logger, logger)

        # Override db with db2
        repo = hub.resolve(Repository, db=db2)
        assert repo.db is db2  # Overridden
        assert repo.logger is logger  # From registry

    def test_resolve_missing_dependency(self):
        """Test that resolve raises NotFoundError for missing dependencies."""
        hub = Hub()
        # Don't register DatabaseClient

        with pytest.raises(NotFoundError) as exc_info:
            hub.resolve(ServiceNeedingDB)

        assert "DatabaseClient" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    def test_resolve_without_injectable_decorator(self):
        """Test that resolve works even without @injectable decorator."""
        hub = Hub()
        logger = Logger("INFO")
        hub.register(Logger, logger)

        # ServiceWithoutDecorator doesn't have @injectable
        class ServiceWithoutDecorator:
            def __init__(self, logger: Logger):
                self.logger = logger

        service = hub.resolve(ServiceWithoutDecorator)
        assert service.logger is logger


# Tests for Container class


class TestContainer:
    """Tests for the Container class."""

    def test_container_register_and_get(self):
        """Test Container.register() and Container.get()."""
        container = Container()
        db = DatabaseClient("postgresql://localhost/test")
        container.register(DatabaseClient, db)

        retrieved = container.get(DatabaseClient)
        assert retrieved is db

    def test_container_resolve(self):
        """Test Container.resolve() with dependencies."""
        container = Container()
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")
        container.register(DatabaseClient, db)
        container.register(Logger, logger)

        repo = container.resolve(Repository)
        assert repo.db is db
        assert repo.logger is logger

    def test_container_has(self):
        """Test Container.has() method."""
        container = Container()
        assert not container.has(DatabaseClient)

        db = DatabaseClient("postgresql://localhost/test")
        container.register(DatabaseClient, db)
        assert container.has(DatabaseClient)

    def test_container_method_chaining(self):
        """Test that Container.register() supports method chaining."""
        container = Container()
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")

        # Method chaining
        result = container.register(DatabaseClient, db).register(Logger, logger)

        assert result is container
        assert container.has(DatabaseClient)
        assert container.has(Logger)

    def test_container_context_manager(self):
        """Test Container as context manager."""
        with Container() as container:
            db = DatabaseClient("postgresql://localhost/test")
            container.register(DatabaseClient, db)
            assert container.has(DatabaseClient)

    def test_container_clear(self):
        """Test Container.clear() removes all registrations."""
        container = Container()
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")
        container.register(DatabaseClient, db)
        container.register(Logger, logger)

        assert container.has(DatabaseClient)
        assert container.has(Logger)

        container.clear()

        assert not container.has(DatabaseClient)
        assert not container.has(Logger)


# Integration tests


class TestDependencyInjectionIntegration:
    """Integration tests for DI system."""

    def test_full_di_workflow(self):
        """Test complete DI workflow from registration to resolution."""
        # Use existing test classes to avoid forward reference issues
        # Config, Cache, API defined at module level
        container = Container()

        # Use DatabaseClient as "Config", Repository as "Cache", ServiceWithMultipleDeps as "API"
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")
        container.register(DatabaseClient, db)
        container.register(Logger, logger)

        # Resolve Repository (depends on DatabaseClient, Logger)
        repo = container.resolve(Repository)
        assert repo.db is db
        assert repo.logger is logger
        container.register(Repository, repo)

        # Resolve ServiceWithMultipleDeps (depends on Repository, Logger, DatabaseClient)
        service = container.resolve(ServiceWithMultipleDeps)
        assert service.repo is repo
        assert service.logger is logger
        assert service.db is db

    def test_composition_root_pattern(self):
        """Test the Composition Root pattern."""
        # Composition Root using existing test classes
        def create_app() -> ServiceWithMultipleDeps:
            container = Container()

            # Register infrastructure
            container.register(DatabaseClient, DatabaseClient("postgresql://localhost/app"))
            container.register(Logger, Logger("INFO"))

            # Resolve application services (Repository acts as intermediate service)
            repo = container.resolve(Repository)
            container.register(Repository, repo)

            # Resolve main application entry point
            return container.resolve(ServiceWithMultipleDeps)

        app = create_app()
        assert isinstance(app, ServiceWithMultipleDeps)
        assert isinstance(app.db, DatabaseClient)
        assert isinstance(app.repo, Repository)
        assert isinstance(app.logger, Logger)

    def test_mixed_di_and_service_locator(self):
        """Test that DI and Service Locator patterns can coexist."""
        from provide.foundation.hub import get_hub

        # Use Service Locator pattern
        hub = get_hub()
        db = DatabaseClient("postgresql://localhost/test")
        hub.register(DatabaseClient, db)

        # Use DI pattern with the same hub
        logger = Logger("INFO")
        hub.register(Logger, logger)
        repo = hub.resolve(Repository)

        assert repo.db is db
        assert repo.logger is logger


# Edge cases


class TestDependencyInjectionEdgeCases:
    """Tests for edge cases in DI system."""

    def test_circular_dependency_detection(self):
        """Test that circular dependencies are documented as unsupported."""
        # Note: Current implementation doesn't detect circular dependencies
        # This test documents that users should avoid circular dependencies
        #
        # Example of circular dependency (DON'T DO THIS):
        # @injectable
        # class ServiceA:
        #     def __init__(self, b: ServiceB): ...
        # @injectable
        # class ServiceB:
        #     def __init__(self, a: ServiceA): ...
        #
        # This would cause infinite recursion. Instead, use:
        # 1. Factory pattern
        # 2. Lazy initialization
        # 3. Restructure dependencies to break the cycle
        pass  # Document only, no actual test

    def test_multiple_instances_same_type(self):
        """Test registering multiple instances of the same type."""
        container = Container()
        db1 = DatabaseClient("postgresql://localhost/db1")
        db2 = DatabaseClient("postgresql://localhost/db2")

        # Last registration wins
        container.register(DatabaseClient, db1)
        container.register(DatabaseClient, db2)

        retrieved = container.get(DatabaseClient)
        assert retrieved is db2  # Most recent registration

    def test_resolve_with_default_parameters(self):
        """Test resolving classes with default parameters."""

        @injectable
        class ServiceWithDefaults:
            def __init__(self, logger: Logger, debug: bool = False):
                self.logger = logger
                self.debug = debug

        container = Container()
        logger = Logger("INFO")
        container.register(Logger, logger)

        service = container.resolve(ServiceWithDefaults)
        assert service.logger is logger
        assert service.debug is False  # Default value used

    def test_resolve_with_none_type_hint(self):
        """Test that resolve handles None type hints gracefully."""

        @injectable
        class ServiceWithOptional:
            def __init__(self, logger: Logger, optional: str | None = None):
                self.logger = logger
                self.optional = optional

        container = Container()
        logger = Logger("INFO")
        container.register(Logger, logger)

        service = container.resolve(ServiceWithOptional)
        assert service.logger is logger
        assert service.optional is None
