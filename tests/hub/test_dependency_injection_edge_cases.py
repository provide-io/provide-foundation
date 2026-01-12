#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for dependency injection edge cases.

Tests advanced scenarios, error handling, and boundary conditions."""

from __future__ import annotations

import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.hub import injectable, is_injectable
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


@injectable
class Logger:
    """Mock logger."""

    def __init__(self, level: str = "INFO") -> None:
        self.level = level


# Edge cases


class TestDependencyInjectionEdgeCases:
    """Tests for edge cases in DI system."""

    def test_circular_dependency_detection(self) -> None:
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

    def test_multiple_instances_same_type(self) -> None:
        """Test registering multiple instances of the same type."""
        from provide.foundation.hub import Container

        container = Container()
        db1 = DatabaseClient("postgresql://localhost/db1")
        db2 = DatabaseClient("postgresql://localhost/db2")

        # Last registration wins
        container.register(DatabaseClient, db1)
        container.register(DatabaseClient, db2)

        retrieved = container.get(DatabaseClient)
        assert retrieved is db2  # Most recent registration

    def test_resolve_with_default_parameters(self) -> None:
        """Test resolving classes with default parameters."""
        from provide.foundation.hub import Container

        @injectable
        class ServiceWithDefaults:
            def __init__(self, logger: Logger, debug: bool = False) -> None:
                self.logger = logger
                self.debug = debug

        container = Container()
        logger = Logger("INFO")
        container.register(Logger, logger)

        service = container.resolve(ServiceWithDefaults)
        assert service.logger is logger
        assert service.debug is False  # Default value used

    def test_resolve_with_none_type_hint(self) -> None:
        """Test that resolve handles None type hints gracefully."""
        from provide.foundation.hub import Container

        @injectable
        class ServiceWithOptional:
            def __init__(self, logger: Logger, optional: str | None = None) -> None:
                self.logger = logger
                self.optional = optional

        container = Container()
        logger = Logger("INFO")
        container.register(Logger, logger)

        service = container.resolve(ServiceWithOptional)
        assert service.logger is logger
        assert service.optional is None

    def test_injectable_with_forward_reference_error(self) -> None:
        """Test injectable with unresolvable forward reference."""

        # Create a class with a forward reference that can't be resolved
        # This should not raise during decoration (line 88-91 coverage)
        @injectable
        class ServiceWithForwardRef:
            def __init__(self, dep: SomeUnknownType) -> None:  # noqa: F821
                self.dep = dep

        # The decorator should succeed - error happens at resolution time
        assert is_injectable(ServiceWithForwardRef)

    def test_resolve_dependencies_with_forward_reference_string(self) -> None:
        """Test resolve_dependencies with string forward references."""
        from provide.foundation.hub.injection import resolve_dependencies
        from provide.foundation.hub.registry import Registry

        # Create a class in the current module with a forward reference
        @injectable
        class ServiceWithStringRef:
            def __init__(self, dep: Logger) -> None:  # String annotation
                self.dep = dep

        registry = Registry()
        logger = Logger("INFO")
        registry.register_type(Logger, logger)

        # Should resolve the string reference by looking it up in the module
        deps = resolve_dependencies(ServiceWithStringRef, registry, allow_missing=False)

        assert "dep" in deps
        assert deps["dep"] is logger

    def test_resolve_dependencies_unresolvable_forward_ref(self) -> None:
        """Test resolve_dependencies with unresolvable forward reference."""
        from provide.foundation.hub.injection import resolve_dependencies
        from provide.foundation.hub.registry import Registry

        @injectable
        class ServiceWithBadRef:
            def __init__(self, dep: CompletelyUnknownType) -> None:  # noqa: F821
                self.dep = dep

        registry = Registry()

        with pytest.raises(ValidationError) as exc_info:
            resolve_dependencies(ServiceWithBadRef, registry, allow_missing=False)

        assert "Forward reference" in str(exc_info.value)
        assert "could not be resolved" in str(exc_info.value)

    def test_resolve_dependencies_allow_missing_forward_ref(self) -> None:
        """Test resolve_dependencies with allow_missing for forward refs."""
        from provide.foundation.hub.injection import resolve_dependencies
        from provide.foundation.hub.registry import Registry

        @injectable
        class ServiceWithBadRef:
            def __init__(self, dep: UnknownType) -> None:  # noqa: F821
                self.dep = dep

        registry = Registry()

        # Should not raise when allow_missing=True
        deps = resolve_dependencies(ServiceWithBadRef, registry, allow_missing=True)

        assert "dep" not in deps  # Missing dependency skipped

    def test_resolve_dependencies_missing_type_hint_error(self) -> None:
        """Test resolve_dependencies raises error for missing type hint."""
        from provide.foundation.hub.injection import resolve_dependencies
        from provide.foundation.hub.registry import Registry

        # Create a class without @injectable to bypass decorator validation
        class UntypedService:
            def __init__(self, untyped_param) -> None:
                self.untyped_param = untyped_param

        registry = Registry()

        with pytest.raises(ValidationError) as exc_info:
            resolve_dependencies(UntypedService, registry, allow_missing=False)

        assert "has no type hint" in str(exc_info.value)
        assert "untyped_param" in str(exc_info.value)

    def test_resolve_dependencies_allow_missing_type_hint(self) -> None:
        """Test resolve_dependencies with allow_missing for untyped params."""
        from provide.foundation.hub.injection import resolve_dependencies
        from provide.foundation.hub.registry import Registry

        class UntypedService:
            def __init__(self, untyped_param) -> None:
                self.untyped_param = untyped_param

        registry = Registry()

        # Should not raise when allow_missing=True
        deps = resolve_dependencies(UntypedService, registry, allow_missing=True)

        assert "untyped_param" not in deps

    def test_register_function(self) -> None:
        """Test the register() convenience function."""
        from provide.foundation.hub.injection import register
        from provide.foundation.hub.registry import Registry

        registry = Registry()
        logger = Logger("INFO")

        # Register using convenience function
        register(registry, Logger, logger)

        # Should be retrievable by type
        retrieved = registry.get_by_type(Logger)
        assert retrieved is logger

    def test_register_function_with_custom_name(self) -> None:
        """Test register() with custom name."""
        from provide.foundation.hub.injection import register
        from provide.foundation.hub.registry import Registry

        registry = Registry()
        logger = Logger("INFO")

        # Register with custom name
        register(registry, Logger, logger, name="custom_logger")

        # Should be retrievable
        retrieved = registry.get_by_type(Logger)
        assert retrieved is logger

    def test_create_instance_with_exception(self) -> None:
        """Test create_instance handles instantiation errors."""
        from provide.foundation.hub.injection import create_instance
        from provide.foundation.hub.registry import Registry

        @injectable
        class FailingService:
            def __init__(self, logger: Logger) -> None:
                raise RuntimeError("Constructor failed!")

        registry = Registry()
        logger = Logger("INFO")
        registry.register_type(Logger, logger)

        with pytest.raises(ValidationError) as exc_info:
            create_instance(FailingService, registry)

        assert "Failed to create instance" in str(exc_info.value)
        assert "Constructor failed!" in str(exc_info.value)

    def test_create_instance_reraises_validation_error(self) -> None:
        """Test create_instance re-raises ValidationError without wrapping."""
        from provide.foundation.hub.injection import create_instance
        from provide.foundation.hub.registry import Registry

        @injectable
        class ServiceWithMissingDep:
            def __init__(self, missing: MissingType) -> None:  # noqa: F821
                self.missing = missing

        registry = Registry()

        # Should re-raise ValidationError from resolve_dependencies
        with pytest.raises(ValidationError) as exc_info:
            create_instance(ServiceWithMissingDep, registry)

        # Should be the original ValidationError, not wrapped
        assert "Forward reference" in str(exc_info.value)
        assert "could not be resolved" in str(exc_info.value)

    def test_resolve_dependencies_with_name_error(self) -> None:
        """Test resolve_dependencies handles NameError during type hint resolution."""
        from provide.foundation.hub.injection import resolve_dependencies
        from provide.foundation.hub.registry import Registry

        # Create a class that will cause a NameError when getting type hints
        # This happens when there's a forward reference to an undefined type
        @injectable
        class ServiceWithNameError:
            def __init__(self, dep: UndefinedForwardRef) -> None:  # noqa: F821
                self.dep = dep

        registry = Registry()

        # The NameError should be caught and handled (lines 173-182)
        # We expect a ValidationError about unresolvable forward reference
        with pytest.raises(ValidationError):
            resolve_dependencies(ServiceWithNameError, registry, allow_missing=False)


# 🧱🏗️🔚
