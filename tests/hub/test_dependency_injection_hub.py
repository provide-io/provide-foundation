#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Hub and Container dependency injection.

Tests Hub.register(), Hub.resolve(), and Container class functionality."""

from __future__ import annotations

import pytest

from provide.foundation.errors.resources import NotFoundError
from provide.foundation.hub import Container, Hub, injectable
from provide.foundation.testmode import reset_foundation_for_testing


@pytest.fixture(autouse=True)
def reset_foundation() -> None:
    """Reset Foundation state before each test."""
    reset_foundation_for_testing()


# Test Classes for DI


@injectable
class DatabaseClient:
    """Mock database client."""

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    def query(self, sql: str) -> list[dict[str, object]]:
        return [{"result": "success"}]


@injectable
class Logger:
    """Mock logger."""

    def __init__(self, level: str = "INFO") -> None:
        self.level = level

    def info(self, msg: str) -> None:
        pass


@injectable
class Repository:
    """Repository with dependencies."""

    def __init__(self, db: DatabaseClient, logger: Logger) -> None:
        self.db = db
        self.logger = logger


@injectable
class ServiceWithMultipleDeps:
    """Service with multiple dependencies."""

    def __init__(self, repo: Repository, logger: Logger, db: DatabaseClient) -> None:
        self.repo = repo
        self.logger = logger
        self.db = db


@injectable
class ServiceNeedingDB:
    """Service needing DatabaseClient for testing missing dependency."""

    def __init__(self, db: DatabaseClient) -> None:
        self.db = db


# Tests for Hub.register() and Hub.resolve()


class TestHubDependencyInjection:
    """Tests for Hub dependency injection methods."""

    def test_register_and_resolve_simple(self) -> None:
        """Test registering and resolving a simple dependency."""
        hub = Hub()
        db = DatabaseClient("postgresql://localhost/test")
        hub.register(DatabaseClient, db)

        # Resolve should return the same instance
        resolved = hub._component_registry.get_by_type(DatabaseClient)
        assert resolved is db

    def test_resolve_with_single_dependency(self) -> None:
        """Test resolving a class with a single dependency."""
        hub = Hub()
        logger = Logger("DEBUG")
        hub.register(Logger, logger)

        @injectable
        class Service:
            def __init__(self, logger: Logger) -> None:
                self.logger = logger

        service = hub.resolve(Service)
        assert service.logger is logger

    def test_resolve_with_multiple_dependencies(self) -> None:
        """Test resolving a class with multiple dependencies."""
        hub = Hub()
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")
        hub.register(DatabaseClient, db)
        hub.register(Logger, logger)

        repo = hub.resolve(Repository)
        assert repo.db is db
        assert repo.logger is logger

    def test_resolve_with_nested_dependencies(self) -> None:
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

    def test_resolve_with_overrides(self) -> None:
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

    def test_resolve_missing_dependency(self) -> None:
        """Test that resolve raises NotFoundError for missing dependencies."""
        hub = Hub()
        # Don't register DatabaseClient

        with pytest.raises(NotFoundError) as exc_info:
            hub.resolve(ServiceNeedingDB)

        assert "DatabaseClient" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    def test_resolve_without_injectable_decorator(self) -> None:
        """Test that resolve works even without @injectable decorator."""
        hub = Hub()
        logger = Logger("INFO")
        hub.register(Logger, logger)

        # ServiceWithoutDecorator doesn't have @injectable
        class ServiceWithoutDecorator:
            def __init__(self, logger: Logger) -> None:
                self.logger = logger

        service = hub.resolve(ServiceWithoutDecorator)
        assert service.logger is logger


# Tests for Container class


class TestContainer:
    """Tests for the Container class."""

    def test_container_register_and_get(self) -> None:
        """Test Container.register() and Container.get()."""
        container = Container()
        db = DatabaseClient("postgresql://localhost/test")
        container.register(DatabaseClient, db)

        retrieved = container.get(DatabaseClient)
        assert retrieved is db

    def test_container_resolve(self) -> None:
        """Test Container.resolve() with dependencies."""
        container = Container()
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")
        container.register(DatabaseClient, db)
        container.register(Logger, logger)

        repo = container.resolve(Repository)
        assert repo.db is db
        assert repo.logger is logger

    def test_container_has(self) -> None:
        """Test Container.has() method."""
        container = Container()
        assert not container.has(DatabaseClient)

        db = DatabaseClient("postgresql://localhost/test")
        container.register(DatabaseClient, db)
        assert container.has(DatabaseClient)

    def test_container_method_chaining(self) -> None:
        """Test that Container.register() supports method chaining."""
        container = Container()
        db = DatabaseClient("postgresql://localhost/test")
        logger = Logger("INFO")

        # Method chaining
        result = container.register(DatabaseClient, db).register(Logger, logger)

        assert result is container
        assert container.has(DatabaseClient)
        assert container.has(Logger)

    def test_container_context_manager(self) -> None:
        """Test Container as context manager."""
        with Container() as container:
            db = DatabaseClient("postgresql://localhost/test")
            container.register(DatabaseClient, db)
            assert container.has(DatabaseClient)

    def test_container_clear(self) -> None:
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

    def test_full_di_workflow(self) -> None:
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

    def test_composition_root_pattern(self) -> None:
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

    def test_mixed_di_and_service_locator(self) -> None:
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


# 🧱🏗️🔚
