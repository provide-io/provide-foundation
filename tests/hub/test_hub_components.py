"""Tests for component registration functionality."""

import pytest

from provide.foundation.errors import AlreadyExistsError
from provide.foundation.hub.components import (
    BaseComponent,
    discover_components,
    register_component,
)
from provide.foundation.hub.manager import clear_hub, get_hub


class TestComponentRegistration:
    """Test component registration and discovery."""

    def setup_method(self) -> None:
        """Clear the hub before each test."""
        clear_hub()

    def test_register_component_decorator(self) -> None:
        """Test the @register_component decorator."""

        @register_component("my_resource")
        class MyResource:
            """A test resource."""

            pass

        hub = get_hub()
        component = hub.get_component("my_resource")

        assert component is MyResource
        assert hasattr(MyResource, "__registry_name__")
        assert MyResource.__registry_name__ == "my_resource"
        assert hasattr(MyResource, "__registry_dimension__")
        assert MyResource.__registry_dimension__ == "component"

    def test_register_component_with_dimension(self) -> None:
        """Test registering component with specific dimension."""

        @register_component("my_data", dimension="data_source")
        class MyDataSource:
            pass

        hub = get_hub()
        component = hub.get_component("my_data", dimension="data_source")

        assert component is MyDataSource
        assert MyDataSource.__registry_dimension__ == "data_source"

    def test_register_component_auto_name(self) -> None:
        """Test component registration with auto-generated name."""

        @register_component()
        class AutoNamedComponent:
            pass

        hub = get_hub()
        component = hub.get_component("AutoNamedComponent")

        assert component is AutoNamedComponent

    def test_register_component_with_metadata(self) -> None:
        """Test component registration with metadata."""

        @register_component(
            "versioned_component",
            version="1.0.0",
            author="test",
            tags=["test", "example"],
        )
        class VersionedComponent:
            """A component with metadata."""

            pass

        hub = get_hub()
        entry = hub._component_registry.get_entry("versioned_component")

        assert entry is not None
        assert entry.metadata["version"] == "1.0.0"
        assert entry.metadata["author"] == "test"
        assert entry.metadata["tags"] == ["test", "example"]
        assert entry.metadata["description"] == "A component with metadata."

    def test_register_component_with_base_class(self) -> None:
        """Test registering component that extends BaseComponent."""

        @register_component("base_resource")
        class MyBaseResource(BaseComponent):
            def __init__(self, name: str) -> None:
                super().__init__(name=name)
                self.resource_type = "test"

            def _setup(self) -> None:
                """Setup implementation."""
                pass

        hub = get_hub()
        component_class = hub.get_component("base_resource")

        assert issubclass(component_class, BaseComponent)

        # Test instantiation
        instance = component_class("test_instance")
        assert instance.name == "test_instance"
        assert instance.resource_type == "test"

    def test_component_info_stored(self) -> None:
        """Test that ComponentInfo is properly stored."""

        @register_component("info_component", version="2.0")
        class InfoComponent:
            """Component with info."""

            pass

        hub = get_hub()
        entry = hub._component_registry.get_entry("info_component")
        info = entry.metadata.get("info")

        assert info is not None
        assert info.name == "info_component"
        assert info.component_class is InfoComponent
        assert info.version == "2.0"
        assert info.description == "Component with info."

    def test_register_duplicate_component_fails(self) -> None:
        """Test that registering duplicate component fails by default."""

        @register_component("duplicate")
        class Component1:
            pass

        with pytest.raises(AlreadyExistsError, match="already registered"):

            @register_component("duplicate")
            class Component2:
                pass

    def test_register_component_with_replace(self) -> None:
        """Test replacing existing component registration."""

        @register_component("replaceable")
        class OldComponent:
            pass

        @register_component("replaceable", replace=True)
        class NewComponent:
            pass

        hub = get_hub()
        component = hub.get_component("replaceable")

        assert component is NewComponent
        assert component is not OldComponent

    def test_list_components_by_dimension(self) -> None:
        """Test listing components filtered by dimension."""

        @register_component("comp1", dimension="component")
        class Comp1:
            pass

        @register_component("res1", dimension="resource")
        class Res1:
            pass

        @register_component("res2", dimension="resource")
        class Res2:
            pass

        hub = get_hub()

        components = hub.list_components(dimension="component")
        assert components == ["comp1"]

        resources = hub.list_components(dimension="resource")
        assert set(resources) == {"res1", "res2"}

    def test_discover_components_from_entry_points(self, monkeypatch) -> None:
        """Test discovering components from entry points."""
        from tests.mocks.components import MockEntryPoint

        class TestResource:
            pass

        class TestDataSource:
            pass

        mock_eps = [
            MockEntryPoint("test_resource", TestResource),
            MockEntryPoint("test_datasource", TestDataSource),
        ]

        def mock_entry_points():
            class EPGroup:
                def select(self, group):
                    if group == "provide.components":
                        return mock_eps
                    return []

            return EPGroup()

        # Patch at the importlib.metadata level since that's where it's imported from
        monkeypatch.setattr("importlib.metadata.entry_points", mock_entry_points)

        discovered = discover_components("provide.components")

        assert "test_resource" in discovered
        assert discovered["test_resource"] is TestResource
        assert "test_datasource" in discovered
        assert discovered["test_datasource"] is TestDataSource

        hub = get_hub()
        assert hub.get_component("test_resource") is TestResource
        assert hub.get_component("test_datasource") is TestDataSource

    def test_component_inheritance_chain(self) -> None:
        """Test that component inheritance works correctly."""

        @register_component("base")
        class BaseResource(BaseComponent):
            resource_type = "base"

        @register_component("derived")
        class DerivedResource(BaseResource):
            resource_type = "derived"

        hub = get_hub()

        base_class = hub.get_component("base")
        derived_class = hub.get_component("derived")

        assert issubclass(derived_class, base_class)
        assert issubclass(derived_class, BaseComponent)

        # Test instantiation
        derived = derived_class(name="test")
        assert derived.resource_type == "derived"
        assert derived.name == "test"

    def test_component_factory_pattern(self) -> None:
        """Test using components with factory pattern."""

        @register_component("factory_component")
        class FactoryComponent(BaseComponent):
            @classmethod
            def create(cls, config: dict):
                """Factory method to create component."""
                return cls(name=config.get("name", "default"))

        hub = get_hub()
        component_class = hub.get_component("factory_component")

        instance = component_class.create({"name": "from_factory"})
        assert instance.name == "from_factory"
        assert isinstance(instance, BaseComponent)
