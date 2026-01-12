#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Configuration and Pipeline tests for hub components module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock, Mock
import pytest

from provide.foundation.hub.components import (
    ComponentCategory,
    get_component_registry,
    get_processor_pipeline,
    get_processors_for_stage,
    load_all_configs,
)


class TestAsyncConfigLoading(FoundationTestCase):
    """Test async configuration loading functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    @pytest.mark.asyncio
    async def test_load_all_configs_async_sources(self) -> None:
        """Test load_all_configs with async config sources."""
        registry = get_component_registry()

        async_source = Mock()
        async_source.load_config = AsyncMock(return_value={"async_key": "async_value"})

        sync_source = Mock()
        sync_source.load_config = Mock(return_value={"sync_key": "sync_value"})

        registry.register(
            name="async_source",
            value=async_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 2},
        )

        registry.register(
            name="sync_source",
            value=sync_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1},
        )

        configs = await load_all_configs()

        assert "async_key" in configs
        assert "sync_key" in configs
        assert configs["async_key"] == "async_value"
        assert configs["sync_key"] == "sync_value"

    @pytest.mark.asyncio
    async def test_load_all_configs_with_exception(self) -> None:
        """Test load_all_configs handles source exceptions."""
        registry = get_component_registry()

        failing_source = Mock()
        failing_source.load_config = Mock(side_effect=Exception("Config load failed"))

        working_source = Mock()
        working_source.load_config = Mock(return_value={"working_key": "working_value"})

        registry.register(
            name="failing_source",
            value=failing_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 2},
        )

        registry.register(
            name="working_source",
            value=working_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1},
        )

        configs = await load_all_configs()

        # Should continue loading other sources despite exception
        assert "working_key" in configs
        assert configs["working_key"] == "working_value"


class TestProcessorPipeline(FoundationTestCase):
    """Test processor pipeline functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_get_processor_pipeline(self) -> None:
        """Test get_processor_pipeline returns processors ordered by priority."""
        registry = get_component_registry()

        proc1 = Mock()
        proc2 = Mock()
        proc3 = Mock()

        registry.register(
            name="proc1",
            value=proc1,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 1},
        )

        registry.register(
            name="proc2",
            value=proc2,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 3},
        )

        registry.register(
            name="proc3",
            value=proc3,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 2},
        )

        pipeline = get_processor_pipeline()

        assert len(pipeline) == 3
        # Should be ordered by priority (highest first)
        assert pipeline[0].value is proc2  # priority 3
        assert pipeline[1].value is proc3  # priority 2
        assert pipeline[2].value is proc1  # priority 1

    def test_get_processors_for_stage(self) -> None:
        """Test get_processors_for_stage filters by stage."""
        registry = get_component_registry()

        pre_proc = Mock()
        post_proc = Mock()
        format_proc = Mock()

        registry.register(
            name="pre_processor",
            value=pre_proc,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 1, "stage": "pre_format"},
        )

        registry.register(
            name="post_processor",
            value=post_proc,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 2, "stage": "post_format"},
        )

        registry.register(
            name="format_processor",
            value=format_proc,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 3, "stage": "format"},
        )

        pre_processors = get_processors_for_stage("pre_format")
        post_processors = get_processors_for_stage("post_format")
        format_processors = get_processors_for_stage("format")

        assert len(pre_processors) == 1
        assert pre_processors[0].value is pre_proc

        assert len(post_processors) == 1
        assert post_processors[0].value is post_proc

        assert len(format_processors) == 1
        assert format_processors[0].value is format_proc


# 🧱🏗️🔚
