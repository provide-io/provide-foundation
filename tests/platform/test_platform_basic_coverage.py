#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Basic coverage tests for platform modules."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest


class TestPlatformBasicCoverage(FoundationTestCase):
    """Basic coverage tests for platform modules."""

    def test_platform_init_imports(self) -> None:
        """Test platform __init__ module can be imported."""
        import provide.foundation.platform

        assert provide.foundation.platform is not None

    def test_detection_module_imports(self) -> None:
        """Test detection module can be imported."""
        from provide.foundation.platform import detection

        assert detection is not None

    def test_get_os_name_function_exists(self) -> None:
        """Test get_os_name function exists."""
        try:
            from provide.foundation.platform.detection import get_os_name

            assert get_os_name is not None
            assert callable(get_os_name)

            # Test basic functionality
            result = get_os_name()
            assert isinstance(result, str)
            assert len(result) > 0
        except ImportError:
            pytest.skip("get_os_name not available")

    def test_get_arch_name_function_exists(self) -> None:
        """Test get_arch_name function exists."""
        try:
            from provide.foundation.platform.detection import get_arch_name

            assert get_arch_name is not None
            assert callable(get_arch_name)

            # Test basic functionality
            result = get_arch_name()
            assert isinstance(result, str)
            assert len(result) > 0
        except ImportError:
            pytest.skip("get_arch_name not available")

    def test_info_module_imports(self) -> None:
        """Test info module can be imported."""
        from provide.foundation.platform import info

        assert info is not None

    def test_get_system_info_function_exists(self) -> None:
        """Test get_system_info function exists."""
        try:
            from provide.foundation.platform.info import get_system_info

            assert get_system_info is not None
            assert callable(get_system_info)

            # Test basic functionality
            result = get_system_info()
            assert result is not None
            assert hasattr(result, "os_name")
        except ImportError:
            pytest.skip("get_system_info not available")

    def test_platform_detection_functions(self) -> None:
        """Test platform detection functions."""
        try:
            from provide.foundation.platform.info import is_linux, is_macos, is_windows

            assert is_windows is not None and callable(is_windows)
            assert is_macos is not None and callable(is_macos)
            assert is_linux is not None and callable(is_linux)

            # Test basic functionality - exactly one should be true
            results = [is_windows(), is_macos(), is_linux()]
            assert sum(results) == 1  # Exactly one platform should be detected
        except ImportError:
            pytest.skip("platform detection functions not available")


class TestTracerBasicCoverage(FoundationTestCase):
    """Basic coverage tests for tracer modules."""

    def test_tracer_init_imports(self) -> None:
        """Test tracer __init__ module can be imported."""
        import provide.foundation.tracer

        assert provide.foundation.tracer is not None

    def test_context_module_imports(self) -> None:
        """Test context module can be imported."""
        from provide.foundation.tracer import context

        assert context is not None

    def test_get_current_span_function_exists(self) -> None:
        """Test get_current_span function exists."""
        from provide.foundation.tracer.context import get_current_span

        assert get_current_span is not None
        assert callable(get_current_span)

    def test_get_current_span_basic_call(self) -> None:
        """Test get_current_span can be called."""
        from provide.foundation.tracer.context import get_current_span

        # Should return None when no span is active
        result = get_current_span()
        assert result is None or hasattr(result, "span_id")

    def test_spans_module_imports(self) -> None:
        """Test spans module can be imported."""
        from provide.foundation.tracer import spans

        assert spans is not None

    def test_span_class_exists(self) -> None:
        """Test Span class exists."""
        from provide.foundation.tracer.spans import Span

        assert Span is not None
        assert callable(Span)

    def test_span_basic_creation(self) -> None:
        """Test Span can be created."""
        from provide.foundation.tracer.spans import Span

        span = Span(name="test_span")
        assert span is not None
        assert span.name == "test_span"
        assert hasattr(span, "span_id")
        assert hasattr(span, "trace_id")


# 🧱🏗️🔚
